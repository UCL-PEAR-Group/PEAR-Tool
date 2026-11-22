"""Predict arterial load response and diagnose assumed pump valve phases.

Finite chamber-pressure transitions are deliberately unresolved. Consequently
phase force extrema are conditional, not a complete-cycle actuator rating.
"""
import copy
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from build_smooth_waveforms import COEFFICIENTS, phase_profile, TRAP

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'pressure_cycle'
MMHG = 133.322


def read_reference():
    with (ROOT/'heart_reference_harmonics.csv').open() as f:
        return np.array([[float(v) for v in row] for row in list(csv.reader(f))[1:]])


def reference(u, data, side):
    cols = (1, 2, 3, 4) if side == 'systemic' else (5, 6, 7, 8)
    signals=[]
    for a, p in [cols[:2],cols[2:]]:
        signals.append(data[0,a]+np.sum(data[1:,a]*np.cos(2*np.pi*np.asarray(u)[...,None]*data[1:,0]+data[1:,p]),axis=-1))
    return signals


def windkessel(t, q, load):
    """Periodic 3-element load; exact updates for piecewise-linear input flow."""
    R1, R2, C, pr = (load[k] for k in ('R1_mmhg_s_ml','R2_mmhg_s_ml','C_ml_mmhg','return_pressure_mmhg'))
    tau = R2*C
    dt=np.diff(t)
    a=np.exp(-dt/tau)
    one_minus=-np.expm1(-dt/tau)
    # Duplicate phase-join samples have dt=0 and identical outlet flow (zero).
    ramp=np.zeros_like(dt)
    moving=dt>0
    ramp[moving]=1-tau/dt[moving]*one_minus[moving]
    b=R2*(q[:-1]*one_minus+np.diff(q)*ramp)
    z=np.zeros(len(t))
    for i in range(len(dt)): z[i+1]=a[i]*z[i]+b[i]
    z0=z[-1]/(-np.expm1(-(t[-1]-t[0])/tau))
    y=z+z0*np.exp(-(t-t[0])/tau)
    return pr+y+R1*q, pr+y


def path_coefficients(path, rho):
    av=np.pi*(path['valve_diameter_mm']/1000)**2/4
    at=np.pi*(path['tube_diameter_mm']/1000)**2/4
    # Coefficients below take Q in mL/s and dQ/dt in mL/s², yielding mmHg.
    B=rho/2*((1/(path['Cd']*av))**2+path['K']/at**2)*1e-12/MMHG
    I=rho*path['length_m']/at*1e-6/MMHG
    return path['R_mmhg_s_ml'],B,I


def calculate(cfg, side, shape='published_harmonics', epsilon=.05, n=4000):
    T=60/cfg['bpm']; sv=1000*cfg['qmean_l_min']/cfg['bpm']; te=cfg['ejection_fraction']*T
    u=np.linspace(0,1,n+1); times=[]; flows=[]; slopes=[]
    for j,duration in enumerate([te,T-te]):
        g,dg=phase_profile(u,COEFFICIENTS[shape][j],epsilon)
        times.append(u*duration+(te if j else 0))
        flows.append(sv/duration*g); slopes.append(sv/duration**2*dg)
    t=np.concatenate(times); phase=np.r_[np.zeros(n+1,dtype=int),np.ones(n+1,dtype=int)]
    qo=np.r_[flows[0],np.zeros(n+1)]; qi=np.r_[np.zeros(n+1),flows[1]]
    dqo=np.r_[slopes[0],np.zeros(n+1)]; dqi=np.r_[np.zeros(n+1),slopes[1]]
    load=cfg['loads'][side]; pa,pw=windkessel(t,qo,load)
    ro,bo,io=path_coefficients(cfg['outlet'],cfg['density_kg_m3'])
    ri,bi,ii=path_coefficients(cfg['inlet'],cfg['density_kg_m3'])
    dpout=ro*qo+bo*qo**2+io*dqo
    dpin=ri*qi+bi*qi**2+ii*dqi
    pc=np.where(phase==0,pa+dpout,load['inlet_pressure_mmhg']-dpin)
    area=np.pi*(cfg['piston_diameter_mm']/1000)**2/4
    force=area*(pc-cfg['rear_pressure_mmhg'])*MMHG
    # Check only the branch ASSUMED CLOSED. An open branch can decelerate
    # against an adverse pressure gradient; this is not itself a violation.
    violation=np.where(phase==0,np.maximum(load['inlet_pressure_mmhg']-pc,0),np.maximum(pc-pa,0))
    e=phase==0; f=~e
    metrics={'side':side,'shape':shape,'epsilon':epsilon,'qmean_l_min':cfg['qmean_l_min'],
      'arterial_mean_mmhg':float(TRAP(pa,t)/T),'arterial_min_mmhg':float(pa.min()),'arterial_max_mmhg':float(pa.max()),
      'arterial_pulse_mmhg':float(np.ptp(pa)), 'arterial_peak_time_s':float(t[pa.argmax()]),
      'outlet_peak_ml_s':float(qo.max()),'flow_peak_time_s':float(t[qo.argmax()]),
      'chamber_min_mmhg':float(pc.min()),'chamber_max_mmhg':float(pc.max()),
      'phase_max_abs_hydraulic_force_n':float(abs(force).max()),
      'max_closed_valve_violation_mmhg':float(violation.max()),
      'violating_time_fraction':float(TRAP((violation>1e-8).astype(float),t)/T),
      'ejection_to_filling_pressure_jump_mmhg':float(pc[n+1]-pc[n]),
      'cycle_wrap_pressure_jump_mmhg':float(pc[0]-pc[-1]),
      'periodic_load_residual_mmhg':float(pw[-1]-pw[0]),
      'ejection_volume_ml':float(TRAP(qo,t)),'filling_volume_ml':float(TRAP(qi,t)),
      'whole_cycle_force_resolved':False}
    predicted_mean=load['return_pressure_mmhg']+(load['R1_mmhg_s_ml']+load['R2_mmhg_s_ml'])*cfg['qmean_l_min']/0.06
    assert abs(metrics['arterial_mean_mmhg']-predicted_mean)<.003
    assert abs(metrics['periodic_load_residual_mmhg'])<1e-10
    if n>=4000:
        assert max(abs(metrics[x]-sv) for x in ('ejection_volume_ml','filling_volume_ml'))<1e-4
    # Energy check on the afterload, independent of the chamber valve assumption.
    supplied=TRAP((pa-load['return_pressure_mmhg'])*qo,t)
    dissipated=TRAP(load['R1_mmhg_s_ml']*qo**2+(pw-load['return_pressure_mmhg'])**2/load['R2_mmhg_s_ml'],t)
    metrics['load_energy_relative_residual']=float((supplied-dissipated)/supplied)
    assert abs(metrics['load_energy_relative_residual'])<2e-4
    arrays={'time_s':t,'phase':phase,'outlet_flow_ml_s':qo,'inlet_flow_ml_s':qi,'outlet_flow_slope_ml_s2':dqo,'inlet_flow_slope_ml_s2':dqi,
            'arterial_pressure_mmhg':pa,'compliance_pressure_mmhg':pw,'chamber_pressure_mmhg':pc,'hydraulic_force_n':force,'closed_valve_violation_mmhg':violation,
            'outlet_loss_mmhg':ro*qo+bo*qo**2,'outlet_inertia_mmhg':io*dqo}
    return metrics,arrays


def main():
    OUT.mkdir(exist_ok=True)
    cfg=json.loads((ROOT/'pressure_cycle_inputs.json').read_text())
    data=read_reference(); uref=np.linspace(0,1,8001)
    reference_metrics={}; refsignals={}
    for side in cfg['loads']:
        q,p=reference(uref,data,side); refsignals[side]=(q,p)
        reference_metrics[side]={'bpm':75,'qmean_l_min':float(TRAP(q,uref)*.06),
          'pressure_mean_mmhg':float(TRAP(p,uref)),'pressure_max_mmhg':float(p.max()),'pressure_min_mmhg':float(p.min()),
          'pulse_pressure_mmhg':float(np.ptp(p)),'flow_peak_ml_s':float(q.max()),'pressure_peak_time_s':float(uref[p.argmax()]*.8),
          'flow_peak_time_s':float(uref[q.argmax()]*.8)}
        assert abs(TRAP(q,uref)-110)<1e-10
        assert abs(TRAP(p,uref)-data[0,3 if side=='systemic' else 7])<1e-10
    metrics=[]; baseline={}; convergence=[]; sensitivity=[]
    for side in cfg['loads']:
        for shape in COEFFICIENTS:
            for eps in (0,.05):
                m,a=calculate(cfg,side,shape,eps); metrics.append(m)
                if shape=='published_harmonics' and eps==.05: baseline[side]=(m,a)
        for n in (400,800,1600,3200):
            m,_=calculate(cfg,side,n=n)
            convergence.append({'side':side,'phase_intervals':n,'force_n':m['phase_max_abs_hydraulic_force_n'],'pmax_mmhg':m['arterial_max_mmhg'],'pmin_mmhg':m['arterial_min_mmhg']})
        for factor in (.5,1,2):
            c=copy.deepcopy(cfg);c['loads'][side]['C_ml_mmhg']*=factor
            m,_=calculate(c,side);sensitivity.append({'change':'compliance_factor','factor':factor,**m})
        for bore in (16,24,32):
            c=copy.deepcopy(cfg);c['inlet']['valve_diameter_mm']=bore;c['outlet']['valve_diameter_mm']=bore
            m,_=calculate(c,side);sensitivity.append({'change':'both_valve_bores_mm','bore':bore,**m})
    fig,ax=plt.subplots(3,2,figsize=(12,10),sharex=True)
    for j,side in enumerate(cfg['loads']):
        m,a=baseline[side];t=a['time_s'];phase=a['phase'];qref,pref=refsignals[side]
        ax[0,j].plot(uref*.8,qref*.06,color='#757F89',ls='--',label='Published reference: 6.6 L/min')
        ax[0,j].plot(t,a['outlet_flow_ml_s']*.06,color='#176B72',label='Pump command: 5 L/min')
        ax[0,j].set_title('Systemic / aortic' if j==0 else 'Pulmonary arterial')
        ax[0,j].legend(fontsize=8)
        ax[1,j].plot(uref*.8,pref,color='#757F89',ls='--',label='Published arterial reference')
        ax[1,j].plot(t,a['arterial_pressure_mmhg'],color='#176B72',label='Calculated arterial load')
        for phase_number in (0,1):
            mask=phase==phase_number
            ax[1,j].plot(t[mask],a['chamber_pressure_mmhg'][mask],color='#B8622E',label='Conditional chamber pressure' if phase_number==0 else None)
            ax[2,j].plot(t[mask],a['hydraulic_force_n'][mask],color='#B8622E',label='Conditional hydraulic force' if phase_number==0 else None)
        bad=a['closed_valve_violation_mmhg']>1e-8
        if np.any(bad):
            ax[2,j].scatter(t[bad][::20],a['hydraulic_force_n'][bad][::20],s=8,color='#B32335',label='Assumed closed valve would open')
        ax[1,j].legend(fontsize=8);ax[2,j].legend(fontsize=8)
        for k in range(3):
            ax[k,j].axvline(cfg['ejection_fraction']*60/cfg['bpm'],color='#C6CDD3',lw=.8)
            ax[k,j].grid(alpha=.18);ax[k,j].spines[['top','right']].set_visible(False)
        ax[2,j].set_xlabel(f"Time (s); pump {cfg['bpm']:g}/min, reference 75/min")
    ax[0,0].set_ylabel('Outlet flow (L/min)');ax[1,0].set_ylabel('Pressure (mmHg gauge)');ax[2,0].set_ylabel('Hydraulic force (N)')
    fig.suptitle('Physiological reference and first pump pressure calculation',fontsize=15)
    fig.text(.5,.012,'Illustrative loads and 50 mm piston. Chamber transition intervals unresolved; force curves are phase diagnostics, not ratings.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.035,1,.96]);fig.savefig(OUT/'pressure_reference_comparison.png',dpi=150);plt.close(fig)
    # Only the reconstructed benchmark data are exported here, without any rescaling.
    with (OUT/'heart_reference_samples.csv').open('w',newline='') as f:
        wr=csv.writer(f,lineterminator='\n');wr.writerow(['time_s','aortic_flow_ml_s','aortic_pressure_mmhg','pulmonary_flow_ml_s','pulmonary_pressure_mmhg'])
        for i in range(0,len(uref),10):wr.writerow([uref[i]*.8,*[refsignals[s][k][i] for s in cfg['loads'] for k in (0,1)]])
    with (OUT/'pressure_cycle_samples.csv').open('w',newline='') as f:
        wr=csv.writer(f,lineterminator='\n');keys=list(baseline['systemic'][1]);wr.writerow(['side']+keys)
        for side,(_,a) in baseline.items():
            nphase=len(a['time_s'])//2
            indices=sorted(set(range(0,len(a['time_s']),10))|{nphase-1,nphase,len(a['time_s'])-1})
            for i in indices:wr.writerow([side]+[a[k][i] for k in keys])
    # An independent limiting case verifies the periodic solver: steady input.
    t=np.linspace(0,.8,101);load=cfg['loads']['systemic'];constant=np.full_like(t,100.)
    p,_=windkessel(t,constant,load)
    assert np.max(abs(p-(load['return_pressure_mmhg']+(load['R1_mmhg_s_ml']+load['R2_mmhg_s_ml'])*100)))<1e-10
    report={'status':'Numerical verification and physiological comparison only; no calibrated or validated pump',
            'inputs':cfg,'reference_metrics':reference_metrics,'phase_metrics':metrics,'baseline':{s:baseline[s][0] for s in baseline},
            'grid_convergence':convergence,'sensitivity':sensitivity,'constant_flow_limit_passed':True,
            'reference_origin':'Qureshi 2018 Appendix A Table A1, reproducing Milnor 1989. 10-harmonic functional reference, not newly acquired clinical data.',
            'no_parameter_fitting':True,'valve_transition_model_implemented':False,'gas_model_in_this_study':False}
    (OUT/'pressure_cycle_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'reference':reference_metrics,'pump':report['baseline'],'grid_convergence':convergence},indent=2))


if __name__=='__main__':main()

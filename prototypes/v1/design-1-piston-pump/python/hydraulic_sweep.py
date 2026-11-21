"""Exploratory piston hydraulic loads. SI constitutive coefficients converted to
mmHg, mL and seconds internally. No motor, linkage, seal friction or solid inertia.
Run: python hydraulic_sweep.py --test OR --sweep
"""
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import argparse, json, time
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

OUT=Path(__file__).resolve().parents[1]/'results'/'python'
MMHG=133.322387415

@dataclass(frozen=True)
class Case:
    f: float=75.
    diameter_mm: float=50.
    swept_ml: float=5000/75
    valve_in_mm: float=16.
    valve_out_mm: float=16.
    gas_ref_ml: float=10.
    pin_mmhg: float=10.
    pout_mmhg: float=90.
    gas_ref_pressure_mmhg: float=10.
    atmosphere_mmhg: float=760.
    n: float=1.2
    rho: float=1000.
    Cd: float=.7
    tube_d_mm: float=20.
    tube_l_m: float=.2
    line_loss_K: float=1.
    ejection_fraction: float=.4
    residual_ml: float=40.
    pressure_floor_abs_mmhg: float=50.

def motion(t,c):
    T=60/c.f
    ph=np.asarray(t)%T
    te=c.ejection_fraction*T
    eject=ph<te
    dt=np.where(eject,te,T-te)
    z=np.where(eject,ph/te,(ph-te)/(T-te))
    h=10*z**3-15*z**4+6*z**5
    hp=30*z**2*(1-z)**2
    hpp=60*z*(1-z)*(1-2*z)
    u=c.swept_ml*np.where(eject,h,1-h)
    q=c.swept_ml*np.where(eject,1.,-1.)*hp/dt
    dq=c.swept_ml*np.where(eject,1.,-1.)*hpp/dt**2
    return u,q,dq

def coeff(c,dv):
    At=np.pi*(c.tube_d_mm*.001)**2/4
    Av=np.pi*(dv*.001)**2/4
    B=c.rho/2*(1/(c.Cd*Av)**2+c.line_loss_K/At**2)*1e-12/MMHG
    I=c.rho*c.tube_l_m/At*1e-6/MMHG
    return B,I

def gas(p,c):
    return c.gas_ref_ml*((c.atmosphere_mmhg+c.gas_ref_pressure_mmhg)/(c.atmosphere_mmhg+p))**(1/c.n)

def pressure_force(p,c):
    return np.asarray(p)*MMHG*np.pi*(c.diameter_mm*.001)**2/4

def full_fill(c, npts=4001):
    """Imposed incompressible displacement, instantaneous ideal valve switching.
    Baseline only; screen minimum pressure before accepting hydraulic feasibility.
    """
    T=60/c.f
    t=np.linspace(0,T,npts,endpoint=False)
    u,q,dq=motion(t,c)
    Bi,Ii=coeff(c,c.valve_in_mm);Bo,Io=coeff(c,c.valve_out_mm)
    eject=t<c.ejection_fraction*T
    p=np.where(eject,c.pout_mmhg+Bo*q*q+Io*dq,c.pin_mmhg-Bi*q*q+Ii*dq)
    return {'pc_peak_mmhg':float(p.max()),'pc_min_mmhg':float(p.min()),
            'force_peak_N':float(pressure_force(p,c).max()),'force_absmax_N':float(np.abs(pressure_force(p,c)).max()),
            'Q_Lmin':c.f*c.swept_ml/1000,'eta':1.,
            'pressure_screen_pass':bool(p.min()+c.atmosphere_mmhg>=c.pressure_floor_abs_mmhg)}

def simulate(c,rtol=2e-7,max_step_div=120,max_cycles=24,npoints=2401,keep_trace=False):
    T=60/c.f
    Bi,Ii=coeff(c,c.valve_in_mm);Bo,Io=coeff(c,c.valve_out_mm)
    y=np.array([c.pin_mmhg,0.,0.,0.,0.])
    opened=[False,False]
    opening_tol=1e-6 # mmHg, only avoids zero-time event chatter
    status='not_periodic'
    periodic=np.inf
    segs=[]
    start_y=y.copy()
    for cycle in range(max_cycles):
        start_y=y.copy(); y[3:]=0.
        start_y[3:]=0.
        segs=[]; t=cycle*T; end=(cycle+1)*T; nevents=0
        while t<end-1e-12:
            active=opened.copy()
            def rhs(tt,yy):
                p,qi,qo=yy[:3]
                vg=gas(p,c)
                C=vg/(c.n*(c.atmosphere_mmhg+p))
                vp=float(motion(tt,c)[1])
                dp=(qi-qo+vp)/C
                dqi=(c.pin_mmhg-p-Bi*qi*abs(qi))/Ii if active[0] else 0.
                dqo=(p-c.pout_mmhg-Bo*qo*abs(qo))/Io if active[1] else 0.
                return [dp,dqi,dqo,qi,qo]
            evs=[]
            for j in range(2):
                if active[j]:
                    def event(tt,yy,j=j):return yy[j+1]
                    event.direction=-1.
                else:
                    def event(tt,yy,j=j):
                        return (c.pin_mmhg-yy[0] if j==0 else yy[0]-c.pout_mmhg)-opening_tol
                    event.direction=1.
                event.terminal=True;evs.append(event)
            def floor(tt,yy):return yy[0]+c.atmosphere_mmhg-c.pressure_floor_abs_mmhg
            floor.direction=-1.;floor.terminal=True;evs.append(floor)
            def empty(tt,yy):
                return c.residual_ml+c.swept_ml-float(motion(tt,c)[0])-gas(yy[0],c)-.1
            empty.direction=-1.;empty.terminal=True;evs.append(empty)
            sol=solve_ivp(rhs,(t,end),y,method='Radau',rtol=rtol,
                          atol=[1e-7,1e-7,1e-7,1e-8,1e-8],max_step=T/max_step_div,
                          dense_output=True,events=evs)
            if not sol.success:raise RuntimeError(sol.message)
            segs.append(sol);prev=t;t=float(sol.t[-1]);y=sol.y[:,-1].copy()
            if sol.status==1:
                hits=[j for j,a in enumerate(sol.t_events) if len(a)]
                j=hits[0]
                if j>=2:
                    status='low_pressure_guard' if j==2 else 'liquid_inventory_guard'
                    return {**asdict(c),'status':status,'cycles':cycle+1}
                opened[j]=not opened[j]
                y[j+1]=0.
                nevents+=1
                if nevents>30 or (t==prev and nevents>2):raise RuntimeError('Valve event chatter')
            elif t>=end-1e-12:break
        scales=np.array([100.,max(c.swept_ml/T,1.),max(c.swept_ml/T,1.)])
        periodic=float(np.max(np.abs(y[:3]-start_y[:3])/scales))
        if cycle>=2 and periodic<2e-7:
            status='periodic';break
    if status!='periodic':return {**asdict(c),'status':status,'cycles':cycle+1,'periodic_residual':periodic}
    ts=np.linspace(cycle*T,(cycle+1)*T,npoints)
    ys=np.empty((5,len(ts)))
    for k,tt in enumerate(ts):
        ss=next((s for s in segs if s.t[0]-1e-12<=tt<=s.t[-1]+1e-12),segs[-1])
        ys[:,k]=ss.sol(tt)
    u,qp,_=motion(ts,c)
    vg=gas(ys[0],c);vl=c.residual_ml+c.swept_ml-u-vg
    F=pressure_force(ys[0],c)
    # Chamber mass balance, including the gas-state change; all volumes in mL.
    storage_resid=vl-vl[0]-(ys[3]-ys[4])
    # End of geometric filling is the last sample, even if inlet flow persists.
    target_liquid=c.residual_ml+c.swept_ml-gas(c.pin_mmhg,c)
    result={**asdict(c),'status':status,'cycles':cycle+1,'periodic_residual':periodic,
            'pc_peak_mmhg':float(ys[0].max()),'pc_min_mmhg':float(ys[0].min()),
            'force_peak_N':float(F.max()),'force_min_N':float(F.min()),'force_absmax_N':float(np.abs(F).max()),
            'delivered_ml':float(ys[4,-1]),'inlet_ml':float(ys[3,-1]),
            'Q_Lmin':float(c.f*ys[4,-1]/1000),'eta':float(ys[4,-1]/c.swept_ml),
            'qout_peak_Lmin':float(ys[2].max()*.06),'qin_peak_Lmin':float(ys[1].max()*.06),
            'fill_deficit_ml':float(max(0,target_liquid-vl[-1])),
            'liquid_min_ml':float(vl.min()),'gas_max_ml':float(vg.max()),
            'balance_error_ml':float(np.max(np.abs(storage_resid))),
            'net_cycle_error_ml':float(abs(ys[3,-1]-ys[4,-1])),
            'min_flow_ml_s':float(ys[1:3].min())}
    if keep_trace:
        result['trace']={'time_s':(ts-cycle*T).tolist(),'phase':((ts-cycle*T)/T).tolist(),
                         'pc_gauge_mmhg':ys[0].tolist(),'pressure_force_N':F.tolist(),
                         'qin_Lmin':(ys[1]*.06).tolist(),'qout_Lmin':(ys[2]*.06).tolist(),
                         'piston_displacement_ml':u.tolist(),'gas_ml':vg.tolist(),'liquid_ml':vl.tolist()}
    return result

def tests():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[Case(),Case(f=180),Case(f=180,valve_in_mm=8,valve_out_mm=8),Case(f=180,valve_in_mm=8,valve_out_mm=8,gas_ref_ml=20)]
    for c in cases:
        st=time.time();a=simulate(c,keep_trace=True)
        print({k:a.get(k) for k in ['f','valve_in_mm','gas_ref_ml','status','cycles','pc_peak_mmhg','pc_min_mmhg','force_peak_N','Q_Lmin','eta','fill_deficit_ml','balance_error_ml','net_cycle_error_ml','min_flow_ml_s']},'sec',round(time.time()-st,2),flush=True)
        (OUT/f'test_{c.f:g}_{c.valve_in_mm:g}_{c.gas_ref_ml:g}.json').write_text(json.dumps(a))
    c=Case(f=180,valve_in_mm=8,valve_out_mm=8)
    a=simulate(c);b=simulate(c,rtol=2e-9,max_step_div=360,npoints=7201)
    print('Refinement', {k: [a[k],b[k],100*abs(a[k]-b[k])/max(abs(b[k]),1e-9)] for k in ['force_peak_N','Q_Lmin','pc_min_mmhg']},flush=True)
    (OUT/'verification.json').write_text(json.dumps({'coarse':a,'refined':b},indent=2))

def sweep():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[];traces={}
    cases=[]
    for vg in [1.,10.,20.]:
        for d in [8.,12.,16.,20.]:
            for f in [40.,60.,75.,90.,120.,150.,180.]:cases.append(('main',Case(f=f,valve_in_mm=d,valve_out_mm=d,gas_ref_ml=vg)))
    for po in [120.,200.]:
        for f in [75.,180.]:
            for d in [8.,12.,16.,20.]:cases.append(('outlet_load',Case(f=f,valve_in_mm=d,valve_out_mm=d,pout_mmhg=po)))
    for n in [1.,1.4]:
        for f,d in [(75.,16.),(180.,16.),(180.,8.)]:cases.append(('thermal',Case(f=f,valve_in_mm=d,valve_out_mm=d,n=n)))
    for cd in [.6,.8]:
        for f,d in [(75.,16.),(180.,16.),(180.,8.)]:cases.append(('discharge_coefficient',Case(f=f,valve_in_mm=d,valve_out_mm=d,Cd=cd)))
    for tefrac in [.3,.5]:
        for f,d in [(75.,16.),(180.,16.),(180.,8.)]:cases.append(('timing',Case(f=f,valve_in_mm=d,valve_out_mm=d,ejection_fraction=tefrac)))
    for j,(group,c) in enumerate(cases):
        keep=(group=='main' and c.gas_ref_ml==10. and (c.f,c.valve_in_mm) in [(75.,16.),(180.,16.),(180.,8.)])
        r=simulate(c,keep_trace=keep);r['group']=group
        if 'trace' in r:traces[f'f{c.f:g}_d{c.valve_in_mm:g}']=r.pop('trace')
        rows.append(r)
        if j%8==0:print(f'{j+1}/{len(cases)} cases; {r["status"]}',flush=True)
        pd.DataFrame(rows).to_csv(OUT/'case_results.csv',index=False)
    (OUT/'waveforms.json').write_text(json.dumps(traces))
    full=[]
    for d in [8.,12.,16.,20.]:
        for f in [40.,60.,75.,90.,120.,150.,180.]:
            c=Case(f=f,valve_in_mm=d,valve_out_mm=d)
            full.append({**asdict(c),**full_fill(c)})
    pd.DataFrame(full).to_csv(OUT/'full_fill_reference.csv',index=False)
    print(pd.DataFrame(rows).groupby('status').size().to_string(),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--test',action='store_true');ap.add_argument('--sweep',action='store_true');a=ap.parse_args()
    if a.test:tests()
    if a.sweep:sweep()

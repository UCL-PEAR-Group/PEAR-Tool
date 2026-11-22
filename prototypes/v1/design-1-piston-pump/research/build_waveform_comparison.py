"""Compare analytical command shapes; this does not simulate the hydraulic circuit."""
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / 'waveforms'
OUT.mkdir(exist_ok=True)
Q_MEAN_L_MIN = 5.0
RATE_PER_MIN = 75.0
FILL_FRACTION = 0.60  # Interpretation of user's 60:40 fallback: filling:ejection.
PERIOD = 60.0 / RATE_PER_MIN
TF = FILL_FRACTION * PERIOD
TE = PERIOD - TF
SV_ML = 1000 * Q_MEAN_L_MIN / RATE_PER_MIN

def harmonic(u, coefficients):
    k = np.arange(1, len(coefficients)+1)
    c = np.asarray(coefficients)
    integral = np.sum(c * (1-(-1.)**k) / (k*np.pi))
    phase = np.asarray(u)[..., None] * k*np.pi
    shape = np.sum(c*np.sin(phase), axis=-1)/integral
    derivative = np.sum(c*k*np.pi*np.cos(phase), axis=-1)/integral
    cumulative = np.sum(c*(1-np.cos(phase))/(k*np.pi), axis=-1)/integral
    return shape, derivative, cumulative

def quintic(u):
    u = np.asarray(u)
    return 30*u**2*(1-u)**2, 60*u*(1-u)*(1-2*u), 10*u**3-15*u**4+6*u**5

profiles = {
    'half_sine': {'label': 'Half-sine reference', 'colour': '#2577A9', 'e': lambda u: harmonic(u,[1.]), 'f': lambda u: harmonic(u,[1.])},
    'published_harmonics': {'label': 'Published harmonic shapes', 'colour': '#C9602B', 'e': lambda u: harmonic(u,[.924,.230,.092]), 'f': lambda u: harmonic(u,[.520,.257,.479])},
    'quintic': {'label': 'Smooth polynomial reference', 'colour': '#287E63', 'e': quintic, 'f': quintic},
}

grid=np.linspace(0,1,10001)
metrics=[]
csv_rows=[]
for name,p in profiles.items():
    fe, de, xe = p['e'](grid)
    ff, df, xf = p['f'](grid)
    assert np.min(fe)>-1e-12 and np.min(ff)>-1e-12
    # Numerical integration checks against exact harmonic / polynomial integrals.
    trap=getattr(np,'trapezoid',None) or np.trapz
    assert abs(trap(fe,grid)-1)<1e-7
    assert abs(trap(ff,grid)-1)<1e-7
    assert abs(xe[0])<1e-12 and abs(xe[-1]-1)<1e-12
    assert abs(xf[0])<1e-12 and abs(xf[-1]-1)<1e-12
    qe=SV_ML/TE*fe; qi=SV_ML/TF*ff
    # Signed displacement-flow derivative on each side of the two joins.
    end_e=SV_ML/TE**2*de[-1]
    start_f=-SV_ML/TF**2*df[0]
    end_f=-SV_ML/TF**2*df[-1]
    start_e=SV_ML/TE**2*de[0]
    metrics.append({'profile':name,'ejection_peak_L_min':float(qe.max()*.06),
                    'ejection_peak_fraction':float(grid[qe.argmax()]),
                    'filling_peak_L_min':float(qi.max()*.06),
                    'ejection_volume_mL':float(trap(qe,grid*TE)),
                    'filling_volume_mL':float(trap(qi,grid*TF)),
                    'eject_to_fill_flow_slope_jump_mL_s2':float(start_f-end_e),
                    'fill_to_eject_flow_slope_jump_mL_s2':float(start_e-end_f)})
    for phase,duration,func in [('ejection',TE,p['e']),('filling',TF,p['f'])]:
        u=np.linspace(0,1,201)
        f,df,cumulative=func(u)
        for j in range(len(u)):
            csv_rows.append([name,phase,float(u[j]*duration),float(SV_ML/duration*f[j]),float(SV_ML/duration**2*df[j]),float(cumulative[j] if phase=='ejection' else 1-cumulative[j])])

with (OUT/'waveform_samples.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['profile','phase','phase_time_s','forward_flow_mL_s','forward_flow_derivative_mL_s2','piston_x_over_stroke']);w.writerows(csv_rows)
metadata={'status':'Analytical command comparison; no hydraulic simulation or physical validation',
          'mean_flow_L_min':Q_MEAN_L_MIN,'circuit_pulses_per_min':RATE_PER_MIN,
          'architecture':'One dedicated ventricular chamber; not shared alternating R/L timing',
          'fallback_interpretation':'60% filling : 40% ejection, no dwell',
          'period_s':PERIOD,'ejection_s':TE,'filling_s':TF,'delivery_mL':SV_ML,
          'source':'Franzetti et al. 2019, supplied article p. 5, Eqs 13–15; shapes independently volume-normalised here',
          'quintic_status':'Engineering reference from existing exploratory motion; not measured physiology',
          'continuity_warning':'Volume normalisation does not match acceleration at phase joins; inspect slope jumps before commanding hardware',
          'normalisation_verification':'10001-point quadrature agrees with unit-area analytical integrals within 1e-7',
          'metrics':metrics}
(OUT/'waveform_verification.json').write_text(json.dumps(metadata,indent=2)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#24384A','text.color':'#24384A','axes.titleweight':'bold'})
fig,axes=plt.subplots(1,2,figsize=(11.8,5.3))
for name,p in profiles.items():
    for ax,duration,fun in [(axes[0],TE,p['e']),(axes[1],TF,p['f'])]:
        shape,_,_=fun(grid)
        ax.plot(grid*duration,SV_ML/duration*shape*.06,label=p['label'],color=p['colour'],lw=2.2,ls='--' if name=='quintic' else '-')
for ax,duration,title in [(axes[0],TE,'Ejection — outlet flow'),(axes[1],TF,'Filling — inlet flow')]:
    ax.set(title=title,xlabel='Time within phase (s)',ylabel='Forward flow (L/min)',xlim=(0,duration),ylim=(0,26))
    ax.grid(alpha=.18);ax.set_axisbelow(True)
axes[0].text(.03,.95,'Swanson–Clark shape',transform=axes[0].transAxes,color='#C9602B',va='top',fontsize=9)
axes[1].text(.03,.95,'Talukder–Reul shape',transform=axes[1].transAxes,color='#C9602B',va='top',fontsize=9)
fig.suptitle('Same delivery and timing; different waveform shapes',fontsize=16,fontweight='bold',y=.98)
fig.text(.5,.91,'5 L/min • 75 pulses/min • ejection 0.32 s • filling 0.48 s • 66.67 mL in each phase',ha='center',fontsize=10)
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.085),ncol=3,frameon=False)
fig.text(.08,.045,'Full-fill analytical commands; coefficients from Franzetti (2019), Eqs 13–15. Orange phases are scaled separately.',fontsize=8.3)
fig.text(.08,.018,'No load or valve dynamics solved. Harmonic phase joins still require acceleration matching; these are not validated motor commands.',fontsize=8.3)
fig.subplots_adjust(top=.80,bottom=.25,left=.08,right=.98,wspace=.24)
fig.savefig(OUT/'waveform_comparison.png',dpi=130,facecolor='white')
plt.close(fig)
print(json.dumps(metadata,indent=2))

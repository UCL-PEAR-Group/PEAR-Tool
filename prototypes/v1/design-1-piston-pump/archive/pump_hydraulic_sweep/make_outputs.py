from pathlib import Path
import json, math, textwrap, shutil, zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

P=Path(__file__).resolve().parent
df=pd.read_csv(P/'case_results.csv'); full=pd.read_csv(P/'full_fill_reference.csv')
waves=json.loads((P/'waveforms.json').read_text())
main=df[(df.group=='main')&(df.status=='periodic')]
base=main[main.gas_ref_ml==10]
NAVY='#17324d'; TEAL='#007f85'; ORANGE='#ce7228'; PURPLE='#7962a6'; BLUE='#447cad'
colours={8.:ORANGE,12.:PURPLE,16.:TEAL,20.:BLUE}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':NAVY,
 'axes.labelcolor':NAVY,'axes.edgecolor':'#abb8c4','axes.spines.top':False,
 'axes.spines.right':False,'axes.titleweight':'bold','axes.titlesize':12,
 'legend.fontsize':8.5,'grid.color':'#dfe5eb','grid.linewidth':.6,'pdf.fonttype':42})

def case(f,d,vg=10,po=90):
    r=df[(df.f==f)&(df.valve_in_mm==d)&(df.valve_out_mm==d)&(df.gas_ref_ml==vg)&(df.pout_mmhg==po)&(df.n==1.2)&(df.Cd==.7)&(df.ejection_fraction==.4)&(df.status=='periodic')]
    return r.iloc[0]

def setup(title,subtitle):
    fig,ax=plt.subplots(2,2,figsize=(13,9.6))
    fig.subplots_adjust(left=.075,right=.975,top=.80,bottom=.13,wspace=.24,hspace=.42)
    fig.text(.075,.955,title,fontsize=20,weight='bold')
    fig.text(.075,.918,subtitle,fontsize=11)
    fig.text(.075,.885,'Exploratory simulation | prescribed displacement | ideal check valves | uncalibrated coefficients',fontsize=9.5,color='#53677d')
    for a in ax.flat:a.grid(True);a.set_axisbelow(True)
    return fig,ax

fig,ax=setup('Hydraulic force: first parameter sweep','66.7 mL geometric stroke | 50 mm piston face unless varied | 10 mL reference air pocket')
a=ax[0,0]
for d in [8.,12.,16.,20.]:
 r=base[base.valve_in_mm==d].sort_values('f')
 a.plot(r.f,r.force_absmax_N,'o-',lw=2,color=colours[d],label=f'{d:g} mm valves')
a.set(xlabel='Delivery frequency (events/min)',ylabel='Maximum |pressure force| per cycle (N)',yscale='log',xlim=(40,180))
a.set_title('A  Frequency and valve restriction',loc='left',pad=13)
a.set_yticks([25,50,100,200,400,800]);a.yaxis.set_major_formatter(ScalarFormatter());a.legend(frameon=False,loc='upper left')

a=ax[0,1]
for f,col in [(75,TEAL),(180,ORANGE)]:
 r=base[base.f==f].sort_values('valve_in_mm')
 a.plot(r.valve_in_mm,r.force_absmax_N,'o-',lw=2,color=col,label=f'{f}/min')
 for _,s in r.iterrows():a.annotate(f'{s.force_absmax_N:.0f} N',(s.valve_in_mm,s.force_absmax_N),xytext=(0,7),textcoords='offset points',ha='center',fontsize=8,color=col)
a.set(xlabel='Inlet and outlet clear bore (mm)',ylabel='Maximum |pressure force| per cycle (N)',yscale='log',xlim=(7,21),ylim=(20,1000))
a.set_title('B  Larger valves: diminishing gains',loc='left',pad=13)
a.set_xticks([8,12,16,20]);a.set_yticks([25,50,100,200,400,800]);a.yaxis.set_major_formatter(ScalarFormatter());a.legend(frameon=False)

a=ax[1,0];D=np.linspace(30,70,100)
for f,po,col,label in [(75,90,TEAL,'75/min; outlet 90 mmHg'),(180,90,ORANGE,'180/min; outlet 90 mmHg'),(180,200,PURPLE,'180/min; outlet 200 mmHg')]:
 r=case(f,16,po=po)
 a.plot(D,r.force_absmax_N*(D/50)**2,lw=2.2,color=col,label=label)
a.set(xlabel='Piston-face diameter (mm)',ylabel='Maximum |pressure force| per cycle (N)',xlim=(30,70),ylim=(0,None))
a.set_title('C  Diameter increases force at fixed volume',loc='left',pad=13)
a.legend(frameon=False,loc='upper left',fontsize=8)
a.text(.02,.02,'16 mm valves; travel changes to retain 66.7 mL',transform=a.transAxes,fontsize=8.5,color='#53677d')

a=ax[1,1]
a.axhspan(2,7,color=TEAL,alpha=.08,label='PDS mean-flow range')
for d in [8.,12.,16.,20.]:
 r=base[base.valve_in_mm==d].sort_values('f')
 a.plot(r.f,r.Q_Lmin,'o-',color=colours[d],lw=1.7,label=f'{d:g} mm valves')
f=np.linspace(40,180,100);a.plot(f,f*(5000/75)/1000,'--',color=NAVY,lw=1.2,label='Geometric displacement flow')
a.axhline(5,color='#778899',ls=':',lw=1)
a.set(xlabel='Delivery frequency (events/min)',ylabel='Net delivered mean flow (L/min)',xlim=(40,180),ylim=(0,14))
a.set_title('D  Fixed travel increases flow with frequency',loc='left',pad=13)
a.legend(frameon=False,fontsize=7.8,loc='upper left',ncol=2)
fig.text(.075,.052,'Baseline boundary pressures: inlet 10 and outlet 90 mmHg gauge; constant test loads, not physiological waveforms.',fontsize=9)
fig.text(.075,.030,'Force = chamber gauge pressure × piston area, with atmospheric rear pressure. Excludes seals, solid inertia and converter loads.',fontsize=9)
fig.text(.075,.010,'High-force cases show demanded internal pressure under ideal motion tracking; they are not verified feasible operating points.',fontsize=9,color='#53677d')
fig.savefig(P/'Hydraulic_force_trends.png',dpi=180,facecolor='white');plt.close(fig)

fig,ax=setup('Within-cycle forces and the air pocket','Signed pressure force: positive advancing load; negative pressure load acts in the opposite direction')
for a,key,title in zip(ax.flat[:3],['f75_d16','f180_d16','f180_d8'],['A  75/min, 16 mm valves','B  180/min, 16 mm valves','C  180/min, 8 mm valves']):
 tr=waves[key];phase=np.array(tr['phase']);F=np.array(tr['pressure_force_N']);j=int(np.argmax(np.abs(F)))
 a.axvspan(.4,1,color='#e7eef4',alpha=.7)
 a.axhline(0,color='#8b9ba9',lw=.8)
 a.plot(phase,F,color=TEAL if '75_' in key else ORANGE,lw=2)
 a.scatter([phase[j]],[F[j]],color=NAVY,s=25,zorder=5)
 a.annotate(f'{F[j]:.1f} N',(phase[j],F[j]),xytext=(8,-19),textcoords='offset points',fontsize=10)
 a.set(xlabel='Cycle fraction, t/T',ylabel='Signed pressure force (N)',xlim=(0,1))
 a.set_title(title,loc='left',pad=13)
 a.text(.68,.94,'Retraction',transform=a.transAxes,ha='center',va='top',fontsize=9,color='#6e7f90')
 a.text(.18,.94,'Advance',transform=a.transAxes,ha='center',va='top',fontsize=9,color='#6e7f90')

a=ax[1,1]
for f,d,col,label in [(75,16,TEAL,'75/min, 16 mm'),(180,16,PURPLE,'180/min, 16 mm'),(180,8,ORANGE,'180/min, 8 mm')]:
 r=main[(main.f==f)&(main.valve_in_mm==d)].sort_values('gas_ref_ml')
 a.plot(r.gas_ref_ml,r.force_absmax_N,'o-',color=col,lw=2,label=label)
 ref=full[(full.f==f)&(full.valve_in_mm==d)].iloc[0]
 if ref.pressure_screen_pass:a.scatter([0],[ref.force_absmax_N],marker='x',s=60,lw=1.5,color=col,zorder=5)
a.plot([],[],marker='x',color=NAVY,ls='',label='Gas-free imposed-fill reference')
a.set(xlabel='Reference gas volume at 10 mmHg gauge (mL)',ylabel='Maximum |pressure force| per cycle (N)',yscale='log',xlim=(-1,21))
a.set_title('D  Air-volume sensitivity is case-dependent',loc='left',pad=13)
a.set_xticks([0,1,10,20]);a.set_yticks([25,50,100,200,400,800]);a.yaxis.set_major_formatter(ScalarFormatter());a.legend(frameon=False)
fig.text(.075,.052,'A–C use different vertical scales. T = 0.80 s at 75/min and 0.333 s at 180/min. Outlet pressure held at 90 mmHg gauge.',fontsize=9)
fig.text(.075,.030,'Motion: quintic advance over 40% of T, return over 60%; both endpoint velocity and acceleration are zero.',fontsize=9)
fig.text(.075,.010,'Gas exponent n = 1.2 assumed. Missing 8 mm / 180/min points at 0 and 1 mL fail the chosen chamber-pressure screen.',fontsize=9,color='#53677d')
fig.savefig(P/'Hydraulic_force_waveforms.png',dpi=180,facecolor='white');plt.close(fig)

# Selected rows and compact machine-readable report inputs.
selected=[]
for f,d in [(75,8),(75,12),(75,16),(75,20),(180,8),(180,12),(180,16),(180,20)]:
 r=case(f,d);selected.append(r.to_dict())
pd.DataFrame(selected).to_csv(P/'selected_cases.csv',index=False)
stats={'case_count':len(df),'status_counts':df.status.value_counts().to_dict(),
       'max_balance_error_ml':float(df.balance_error_ml.max()),
       'max_cycle_flow_error_ml':float(df.net_cycle_error_ml.max()),
       'max_periodic_residual':float(df.periodic_residual.max()),
       'max_pressure_force_case':df.loc[df.force_absmax_N.idxmax()].to_dict()}
(P/'summary.json').write_text(json.dumps(stats,indent=2))
print(pd.DataFrame(selected)[['f','valve_in_mm','pc_peak_mmhg','pc_min_mmhg','force_peak_N','force_min_N','force_absmax_N','Q_Lmin','fill_deficit_ml']].round(3).to_string(index=False))
print(json.dumps(stats,indent=2))

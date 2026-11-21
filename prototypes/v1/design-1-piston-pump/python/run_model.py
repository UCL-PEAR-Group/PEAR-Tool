"""Local entry point for the existing piston hydraulic model.

Run from any working directory. Output files go to results/python, never archive.
No physical equations or baseline parameters are changed by this entry point.
"""
from dataclasses import asdict, replace
from pathlib import Path
import argparse
import json
import platform
import runpy

import numpy as np
import pandas as pd
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from hydraulic_sweep import Case, OUT, simulate, motion, sweep

ROOT=Path(__file__).resolve().parents[1]

def verify_reference():
    reference=pd.read_csv(ROOT/'archive/pump_hydraulic_sweep/selected_cases.csv')
    records=[]
    for frequency,bore in [(75.,16.),(180.,16.),(180.,8.)]:
        case=Case(f=frequency,valve_in_mm=bore,valve_out_mm=bore)
        result=simulate(case)
        assert result['status']=='periodic', result
        row=reference[(reference.f==frequency)&(reference.valve_in_mm==bore)].iloc[0]
        errors={name:abs(result[name]-row[name])/max(abs(row[name]),1e-12)
                for name in ['force_absmax_N','Q_Lmin','pc_min_mmhg']}
        assert max(errors.values())<1e-6, errors
        assert result['balance_error_ml']<1e-3
        assert result['net_cycle_error_ml']<1e-3
        assert result['min_flow_ml_s']>-1e-6
        records.append({'bpm':frequency,'valve_mm':bore,
                        'relative_errors':errors,'status':'passed'})
    case=Case(); period=60/case.f
    u,q,dq=motion(np.array([0,case.ejection_fraction*period,period]),case)
    np.testing.assert_allclose(u,[0,case.swept_ml,0],atol=1e-10)
    np.testing.assert_allclose(q,0,atol=1e-10)
    np.testing.assert_allclose(dq,0,atol=1e-9)
    stopped=simulate(Case(f=180.,valve_in_mm=8.,valve_out_mm=8.,gas_ref_ml=1.))
    assert stopped['status']=='low_pressure_guard', stopped
    record={'checks':records,'motion_endpoints':'passed','expected_guard':'passed',
            'python':platform.python_version(),'numpy':np.__version__,
            'scipy':scipy.__version__,'physical_validation':False,
            'scope':'Regression and conservation checks; unchanged hydraulic equations.'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'verification_status.json').write_text(json.dumps(record,indent=2)+'\n')
    return record

def baseline(case):
    result=simulate(case,keep_trace=True)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'baseline.json').write_text(json.dumps(result,indent=2)+'\n')
    if result['status']!='periodic':
        print(json.dumps(result,indent=2))
        return result
    trace=result['trace']
    fig,axes=plt.subplots(2,1,figsize=(8,6),sharex=True,layout='constrained')
    axes[0].plot(trace['time_s'],trace['pressure_force_N'],color='#007f85')
    axes[0].set_ylabel('Signed hydraulic force (N)')
    axes[1].plot(trace['time_s'],trace['qin_Lmin'],label='Inlet')
    axes[1].plot(trace['time_s'],trace['qout_Lmin'],label='Outlet')
    axes[1].set(xlabel='Time (s)',ylabel='Instantaneous flow (L/min)')
    axes[1].legend()
    for ax in axes:ax.grid(alpha=.25)
    fig.suptitle('Exploratory piston model — one periodic cycle')
    fig.savefig(OUT/'baseline.png',dpi=180)
    plt.close(fig)
    print(json.dumps({k:result[k] for k in ['status','Q_Lmin','force_absmax_N',
                                          'pc_peak_mmhg','pc_min_mmhg']},indent=2))
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['baseline','check','sweep'],nargs='?',default='baseline')
    parser.add_argument('--config',type=Path,help='JSON overrides of Case fields, baseline only')
    args=parser.parse_args()
    if args.config and args.mode!='baseline':parser.error('--config applies only to baseline')
    if args.mode=='check':
        print(json.dumps(verify_reference(),indent=2))
    elif args.mode=='sweep':
        sweep()
        runpy.run_path(str(Path(__file__).with_name('make_outputs.py')),run_name='__main__')
    else:
        overrides=json.loads(args.config.read_text()) if args.config else {}
        unknown=set(overrides)-set(asdict(Case()))
        if unknown:parser.error('Unknown Case fields: '+', '.join(sorted(unknown)))
        case=replace(Case(),**overrides)
        required_positive=['f','diameter_mm','swept_ml','valve_in_mm','valve_out_mm',
                           'gas_ref_ml','atmosphere_mmhg','n','rho','Cd','tube_d_mm','tube_l_m']
        for key,value in asdict(case).items():
            if not isinstance(value,(float,int)) or isinstance(value,bool) or not np.isfinite(value):
                parser.error(f'{key} must be a finite real number')
        if any(getattr(case,key)<=0 for key in required_positive):
            parser.error('Frequency, dimensions, gas amount and material coefficients must be positive')
        if not 0<case.ejection_fraction<1:parser.error('ejection_fraction must lie between 0 and 1')
        if case.line_loss_K<0 or case.residual_ml<=0:parser.error('Invalid line loss or residual volume')
        if case.pin_mmhg+case.atmosphere_mmhg<=case.pressure_floor_abs_mmhg:
            parser.error('Initial pressure must exceed the low-pressure guard')
        if case.gas_ref_pressure_mmhg+case.atmosphere_mmhg<=0:
            parser.error('Reference gas absolute pressure must be positive')
        baseline(case)

if __name__=='__main__':main()

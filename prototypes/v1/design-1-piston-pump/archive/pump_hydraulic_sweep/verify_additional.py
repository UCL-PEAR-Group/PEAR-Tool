from pathlib import Path
from dataclasses import fields
import json
import pandas as pd
from hydraulic_sweep import Case,simulate
P=Path(__file__).resolve().parent
df=pd.read_csv(P/'case_results.csv')
rows=[df.loc[df.force_absmax_N.idxmax()],df[(df.group=='main')&(df.f==75)&(df.valve_in_mm==16)&(df.gas_ref_ml==10)].iloc[0]]
checks=[]
for row in rows:
    c=Case(**{f.name:float(row[f.name]) for f in fields(Case)})
    fine=simulate(c,rtol=2e-9,max_step_div=360,npoints=7201)
    checks.append({'case':{f.name:float(row[f.name]) for f in fields(Case)},'coarse':row.to_dict(),'refined':fine,
        'relative_change_percent':{k:100*abs(float(row[k])-fine[k])/max(abs(fine[k]),1e-12) for k in ['force_absmax_N','Q_Lmin','pc_min_mmhg']}})
(P/'additional_verification.json').write_text(json.dumps(checks,indent=2))
print([r['relative_change_percent'] for r in checks])

import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
import {addWaveformSheet} from './waveform_sheet.mjs';
import {addPressureCycle} from './pressure_cycle_sheet.mjs';

const design=process.env.PEAR_DESIGN_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const outputDir=process.env.PEAR_OUTPUT_DIR || path.join(design,'results','spreadsheet-review');
await fs.mkdir(outputDir,{recursive:true});
const records=JSON.parse(await fs.readFile(path.join(design,'research/literature_register.json'),'utf8'));
const equations=JSON.parse(await fs.readFile(path.join(design,'research/equation_map.json'),'utf8'));
const wb=Workbook.create();
const navy='#17324D',teal='#176B72',amber='#FFF1CF',muted='#526576';
function base(name,last,cols,widths){
 const s=wb.worksheets.add(name);s.showGridLines=false;
 s.getRange(`A1:${cols}${last}`).format.font={name:'Arial',size:11,color:navy};
 s.getRange(`A1:${cols}${last}`).format.rowHeight=24;
 widths.forEach((w,i)=>s.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${last}`).format.columnWidth=w);
 s.freezePanes.freezeRows(6);return s;
}
function band(s,row,end,vals){s.getRange(`A${row}:${end}${row}`).values=[vals];s.getRange(`A${row}:${end}${row}`).format={fill:navy,font:{color:'#FFFFFF',bold:true},rowHeight:29};}
function textrow(s,row,text,end='F'){s.getRange(`A${row}:${end}${row}`).merge();s.getRange(`A${row}`).values=[[text]];s.getRange(`A${row}:${end}${row}`).format.wrapText=true;}
const s=base('Pressure start',82,'F',[33,12,19,17,56,39]);
textrow(s,2,'PEAR | Piston pump pressure model — first algebraic step');s.getRange('A2:F2').format.font={size:18,bold:true};s.getRange('A2:F2').format.rowHeight=32;
textrow(s,3,'5 L/min • 75 pulses/min per circuit • flat plunger • illustrative full-fill, open-outlet point');
textrow(s,4,'Amber = editable input. Results below are local pressure/force estimates, not maximum force or a solved circulatory cycle.');s.getRange('A4:F4').format.font.color=muted;
band(s,6,'F',['Input','Symbol','Value','Unit','Status / assumption','Provenance']);
const inputs=[
['Mean circuit flow','Qmean',5,'L/min','Prescribed baseline','User, 21 Nov 2026'],
['Circuit pulse rate','h',75,'pulses/min','Prescribed baseline','User, 21 Nov 2026'],
['Piston diameter','Dp',50,'mm','Illustrative; free design variable','Prior exploratory case; not selected'],
['Ejection fraction','gamma',.4,'fraction','Assumed for timing illustration','Prior exploratory motion allocation'],
['Instantaneous flow multiplier','kq',1,'dimensionless','q = kq × ejection-average flow; not necessarily peak','Chosen local test point'],
['External outlet pressure','po',90,'mmHg gauge','Assumed constant at this local point; not a solved mean/peak','Prior nominal load assumption'],
['Rear-face pressure','prear',0,'mmHg gauge','Atmospheric rear face','Assumption'],
['Liquid density','rho',1000,'kg/m³','Water-like example; replace with measured BMF value','Prior illustrative input'],
['Outlet valve bore','dv',16,'mm','Geometric area used as provisional effective area','Prior illustrative input'],
['Valve discharge coefficient','Cd',.7,'dimensionless','Uncalibrated constant','Prior illustrative input'],
['Outlet line bore','Dt',20,'mm','Uniform line approximation','Prior illustrative input'],
['Outlet line length','L',.2,'m','Selected segment only','Prior illustrative input'],
['Quadratic line loss coefficient','K',1,'dimensionless','Lumped assumed loss; no duplicate valve term','Prior illustrative input'],
['Additional linear resistance','Rlin',0,'mmHg/(L/min)','Excluded until applicable/calibrated; not a complete friction law','Unresolved component input'],
['Local flow acceleration','dq/dt',0,'(L/min)/s','Zero at this selected point; does not define a waveform','Assumption']
];s.getRange('A7:F21').values=inputs;s.getRange('C7:C21').format.fill=amber;s.getRange('C7:C21').setNumberFormat('0.00');s.getRange('E7:F21').format.wrapText=true;s.getRange('A7:F21').format.rowHeight=40;
s.getRange('C10').setNumberFormat('0%');s.getRange('C8').setNumberFormat('0');
for(const row of [7,8,9,11,14,15,16,17,18])s.getRange(`C${row}`).dataValidation={rule:{type:'decimal',operator:'greaterThan',formula1:0}};
s.getRange('C10').dataValidation={rule:{type:'decimal',operator:'between',formula1:.01,formula2:.99}};
textrow(s,23,'Open-valve calculation: use a defined outlet pressure and flow at one instant. SI conversion occurs in the formulas.');
band(s,24,'F',['Result','Symbol','Value','Unit','Interpretation','Equation / source']);
const outputs=[
['Required net delivery','Vnet','=1000*C7/C8','mL/pulse','Equals swept volume only in this full-fill limit','E1; conservation'],
['Circuit period','T','=60/C8','s','Per circuit','Time conversion'],
['Piston area','Ap','=PI()*(C9/1000)^2/4','m²','Flat face; no rod subtraction','E2'],
['Required ideal travel','S','=C25*0.000001/C27*1000','mm','No leakage or storage; geometry illustration','E2'],
['Ejection duration','te','=C10*C26','s','One dedicated chamber; 1B timing illustration','gamma × T'],
['Ejection-average flow','qe','=C7/C10','L/min','Not peak flow','Qmean / gamma'],
['Chosen instantaneous flow','q','=C11*C30','L/min','Set by multiplier for local calculation','kq × qe'],
['Chosen instantaneous flow, SI','qSI','=C31/60000','m³/s','Use this in loss/inertia expressions','1 L/min = 1/60000 m³/s'],
['Valve area','Av','=PI()*(C15/1000)^2/4','m²','Provisional effective area','E5'],
['Line area','At','=PI()*(C17/1000)^2/4','m²','Uniform circular line','E6'],
['Line inertance','I','=C14*C18/C34','Pa s²/m³','Only this line segment included','E6; T20'],
['Valve pressure loss','dpv','=C14/2*(C32/(C16*C33))^2/133.322','mmHg','Forward-flow, constant Cd approximation','E5'],
['Quadratic line pressure loss','dpk','=C14*C19/2*(C32/C34)^2/133.322','mmHg','Assumed coefficient; not calibrated','E5'],
['Additional linear loss','dpr','=C20*C31','mmHg','Zero by default; component model unresolved','Rlin × q'],
['Line inertia contribution','dpi','=C35*(C21/60000)/133.322','mmHg','Can be negative when flow decelerates','I × dq/dt'],
['Chamber pressure','pc','=C12+SUM(C36:C39)','mmHg gauge','Includes specified downstream pressure and selected path','E4'],
['Local hydraulic force','Fh','=C27*(C40-C13)*133.322','N','Signed; excludes seal friction and moving-solid inertia','E7; not maximum force'],
];
for(let i=0;i<outputs.length;i++){const row=25+i,a=outputs[i];s.getRange(`A${row}:F${row}`).values=[[a[0],a[1],null,a[3],a[4],a[5]]];s.getRange(`C${row}`).formulas=[[a[2]]];}
s.getRange('C25:C41').setNumberFormat('0.000');for(const row of [27,32,33,34])s.getRange(`C${row}`).setNumberFormat('0.000E+00');
s.getRange('E25:F41').format.wrapText=true;s.getRange('A25:F41').format.rowHeight=36;s.getRange('A40:F41').format.fill='#E4F2F0';
textrow(s,43,'MAXIMUM FORCE NOT COMPUTED: requires a periodic pressure/flow history, valve states, filling and air-pocket dynamics.');s.getRange('A43:F43').format.font={bold:true,color:'#9A4A10'};
s.getRange('A45:F46').values=[['1A: shared physical cycle rate','fA',null,'cycles/min','One right + one left delivery per circuit period','Volume/time accounting'],['1B: rate per dedicated chamber','fB',null,'cycles/min','Each chamber supplies one circuit','Volume/time accounting']];s.getRange('C45').formulas=[['=2*C8']];s.getRange('C46').formulas=[['=C8']];s.getRange('E45:F46').format.wrapText=true;s.getRange('A45:F46').format.rowHeight=40;
textrow(s,48,'Sensitivity at fixed target delivery and the same local hydraulic condition. Independent diameter sweeps; no optimisation.');
band(s,49,'F',['Piston bore (mm)','Travel (mm)','Local force (N)','Valve bore (mm)','Valve loss (mmHg)','Conditions']);
for(let i=0;i<8;i++){const r=50+i;s.getRange(`A${r}:F${r}`).values=[[30+10*i,null,null,6+2*i,null,'Same Q, h, Cd and local q']];s.getRange(`B${r}`).formulas=[[`=$C$25*0.000001/(PI()*(A${r}/1000)^2/4)*1000`]];s.getRange(`C${r}`).formulas=[[`=PI()*(A${r}/1000)^2/4*($C$40-$C$13)*133.322`]];s.getRange(`E${r}`).formulas=[[`=$C$14/2*($C$32/($C$16*PI()*(D${r}/1000)^2/4))^2/133.322`]];}
s.getRange('B50:C57').setNumberFormat('0.00');s.getRange('E50:E57').setNumberFormat('0.00');
const ch1=s.charts.add('line',s.getRange('A49:B57'));ch1.title='Piston diameter vs required travel';ch1.hasLegend=false;ch1.setPosition('A60','C77');ch1.xAxis.title.text='Piston bore (mm)';ch1.yAxis.title.text='Travel (mm)';ch1.yAxis.numberFormatCode='0.0';
const ch2=s.charts.add('line',s.getRange('D49:E57'));ch2.title='Outlet bore vs local valve loss';ch2.hasLegend=false;ch2.setPosition('D60','F77');ch2.xAxis.title.text='Valve bore (mm)';ch2.yAxis.title.text='Pressure loss (mmHg)';ch2.yAxis.numberFormatCode='0.0';
for(const c of [ch1,ch2]){c.titleTextStyle.fontSize=14;c.titleTextStyle.typeface='Arial';c.xAxis.textStyle={typeface:'Arial',fontSize:11};c.yAxis.textStyle={typeface:'Arial',fontSize:11};}
textrow(s,79,'Use Equation map for the unimplemented dynamic coupling; use Literature for primary-source access and limits.');
textrow(s,80,'Workbook calculations verified in the authoring engine. Native Excel / LibreOffice and physical rig validation are not yet performed.');

const lit=base('Literature',24,'I',[9,30,38,41,44,46,42,37,65]);
textrow(lit,2,'PEAR | Cardiovascular piston-pump literature','I');lit.getRange('A2:I2').format.font={size:18,bold:true};
textrow(lit,3,'Targeted review • 12 primary journal papers + 1 thesis + 1 review • searched 21 November 2026','I');
textrow(lit,4,'Filter by purpose and access. Full methods are not available for every paper; related platform papers are not independent validations.','I');
const lh=['ID','Study','Purpose category','Architecture','Role / model takeaway','Reported conditions','Access / reading location','DOI','Title / source URL'];
band(lit,6,'I',lh);
const lr=records.map(r=>[r.id,r.source,r.category,r.architecture,r.purpose+' '+r.takeaway,r.conditions,r.access+' | '+r.locator,r.doi,r.title+'\n'+r.url]);
lit.getRange(`A7:I${6+lr.length}`).values=lr;lit.getRange(`A7:I${6+lr.length}`).format.wrapText=true;lit.getRange(`A7:I${6+lr.length}`).format.verticalAlignment='center';lit.getRange(`A7:I${6+lr.length}`).format.rowHeight=116;
lit.tables.add(`A6:I${6+lr.length}`,true,'LiteratureRegister');
textrow(lit,23,'Screened out: Herwald et al. 2024, DOI 10.1016/j.ohx.2024.e00561 — programmable centrifugal pump, not a piston mechanism.','I');

const eq=base('Equation map',22,'F',[9,26,76,53,75,46]);
textrow(eq,2,'PEAR | Coupling map — equations and assumptions');eq.getRange('A2:F2').format.font={size:18,bold:true};
textrow(eq,3,'Pressure cycle now solves the assumed arterial load. Gas storage and chamber valve transitions remain unresolved.');
textrow(eq,4,'Symbols and units are local to each row. Read the accompanying review before combining equations.');
band(eq,6,'F',['ID','Block','Expression','Variables / units','Assumptions / limits','Status / provenance']);eq.getRange(`A7:F${6+equations.length}`).values=equations;eq.getRange(`A7:F${6+equations.length}`).format.wrapText=true;eq.getRange(`A7:F${6+equations.length}`).format.rowHeight=88;eq.getRange(`A7:F${6+equations.length}`).format.verticalAlignment='center';
eq.tables.add(`A6:F${6+equations.length}`,true,'EquationRegister');

const wave=addWaveformSheet(wb,base,band,textrow);
const pressureCfg=JSON.parse(await fs.readFile(path.join(design,'research/pressure_cycle_inputs.json'),'utf8'));
const heartCoefficients=(await fs.readFile(path.join(design,'research/heart_reference_harmonics.csv'),'utf8')).trim().split('\n').slice(1).map(line=>line.split(',').map(Number));
const cycle=addPressureCycle(wb,base,band,textrow,heartCoefficients,pressureCfg);
wb.recalculate();
const value=a=>s.getRange(a).values[0][0];
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9*Math.max(1,Math.abs(b)),`${a} != ${b}`);
const pi=Math.PI,A=pi*.05**2/4,q=12.5/60000,Av=pi*.016**2/4,At=pi*.02**2/4;
const dpv=1000/2*(q/(.7*Av))**2/133.322,dpk=1000/2*(q/At)**2/133.322;
near(value('C25'),5000/75);near(value('C28'),(5000/75)*1e-6/A*1000);near(value('C36'),dpv);near(value('C41'),A*(90+dpv+dpk)*133.322);
const checks={baseline:{net_mL:value('C25'),travel_mm:value('C28'),ejection_flow_L_min:value('C30'),valve_loss_mmHg:value('C36'),chamber_mmHg:value('C40'),local_force_N:value('C41')},perturbations:[]};
const travel=value('C28'),force=value('C41');s.getRange('C9').values=[[100]];wb.recalculate();near(value('C28'),travel/4);near(value('C41'),force*4);checks.perturbations.push('Doubling piston bore quarters travel and quadruples force at fixed local pressure');s.getRange('C9').values=[[50]];
s.getRange('C15').values=[[8]];wb.recalculate();near(value('C36'),16*dpv);checks.perturbations.push('Halving valve bore multiplies constant-Cd loss by 16');s.getRange('C15').values=[[16]];
s.getRange('C8').values=[[150]];wb.recalculate();near(value('C25'),5000/150);near(value('C30'),12.5);checks.perturbations.push('Doubling bpm at fixed mean flow halves required delivery; ejection-average flow stays constant at fixed fraction');s.getRange('C8').values=[[75]];
wb.recalculate();near(value('C41'),checks.baseline.local_force_N);
const wv=a=>wave.getRange(a).values[0][0];
const refs=JSON.parse(await fs.readFile(path.join(design,'research/waveforms/smooth_waveform_verification.json'),'utf8'));
const wm=refs.metrics.find(m=>m.profile==='published_harmonics'&&m.epsilon===.05);
const relative=(actual,expected,tolerance)=>assert.ok(Math.abs(actual/expected-1)<tolerance,`${actual} != ${expected}`);
relative(wv('C23'),wm.ejection_peak_L_min,1e-4);relative(wv('C24'),wm.filling_peak_L_min,1e-4);relative(wv('C25'),wm.max_abs_acceleration_m_s2,.004);
near(wv('C15'),5000/75);near(wv('C26'),0);near(wv('C30'),0);near(wv('C31'),0);
checks.waveform={peak_ejection_L_min:wv('C23'),peak_filling_L_min:wv('C24'),sampled_max_acceleration_m_s2:wv('C25'),return_position:wv('C26'),eject_fill_jump:wv('C30'),wrap_jump:wv('C31'),independent_python_reference:wm,perturbations:[]};
const peak=wv('C23'),maxacc=wv('C25'),required=wv('C19');
wave.getRange('C8').values=[[0]];wb.recalculate();assert.ok(Math.abs(wv('C30'))>1);checks.waveform.perturbations.push('Zero smoothing restores nonzero harmonic acceleration jumps');
wave.getRange('C7').values=[['Half-sine']];wb.recalculate();relative(wv('C23'),Math.PI/2*12.5,1e-5);checks.waveform.perturbations.push('Half-sine selector reproduces analytic peak');
wave.getRange('C8').values=[[.05]];wave.getRange('C7').values=[['Published harmonics']];
s.getRange('C8').values=[[150]];wb.recalculate();near(wv('C23'),peak);near(wv('C25'),2*maxacc);near(wv('C19'),required/2);checks.waveform.perturbations.push('At fixed mean flow and shape, doubled rate preserves flow peak, doubles acceleration and halves required stroke');s.getRange('C8').values=[[75]];
s.getRange('C10').values=[[.5]];wb.recalculate();near(wv('C23'),peak*.4/.5);near(wv('C30'),0);checks.waveform.perturbations.push('Timing change rescales peak flow and preserves smooth reversal');s.getRange('C10').values=[[.4]];
wb.recalculate();near(wv('C23'),peak);near(wv('C25'),maxacc);near(value('C41'),checks.baseline.local_force_N);
const absMean=(x,y)=>Math.abs(x-y)<0.003; // Trapezoidal pressure-mean tolerance, mmHg.
const pv=a=>cycle.getRange(a).values[0][0];
const pressureRef=JSON.parse(await fs.readFile(path.join(design,'research/pressure_cycle/pressure_cycle_verification.json'),'utf8'));
assert.ok(absMean(pv('C24'),90));relative(pv('C26'),pressureRef.baseline.systemic.arterial_max_mmhg,1e-4);relative(pv('C29'),pressureRef.baseline.systemic.phase_max_abs_hydraulic_force_n,1e-4);near(pv('C30'),0);
checks.pressure_cycle={baseline:{arterial_mean_mmhg:pv('C24'),arterial_min_mmhg:pv('C25'),arterial_max_mmhg:pv('C26'),chamber_min_mmhg:pv('C27'),phase_force_n:pv('C29'),closed_valve_violation_mmhg:pv('C30')},perturbations:[]};
cycle.getRange('C7').values=[['Pulmonary']];wb.recalculate();assert.ok(absMean(pv('C24'),15));relative(pv('C26'),pressureRef.baseline.pulmonary.arterial_max_mmhg,1e-4);relative(pv('C29'),pressureRef.baseline.pulmonary.phase_max_abs_hydraulic_force_n,.004);assert.ok(pv('C30')>19);checks.pressure_cycle.perturbations.push('Pulmonary preset gives 15 mmHg mean and exposes a closed-valve inconsistency');cycle.getRange('C7').values=[['Systemic']];
cycle.getRange('M23').values=[[3]];wb.recalculate();assert.ok(absMean(pv('C24'),90));assert.ok(pv('C26')<102);checks.pressure_cycle.perturbations.push('Doubling load compliance narrows pressure pulse without changing mean');cycle.getRange('M23').values=[[1.5]];
const phaseForce=checks.pressure_cycle.baseline.phase_force_n;s.getRange('C9').values=[[100]];wb.recalculate();near(pv('C29'),4*phaseForce);assert.ok(absMean(pv('C24'),90));checks.pressure_cycle.perturbations.push('Doubling piston bore quadruples hydraulic force at the same flow and load');s.getRange('C9').values=[[50]];
wb.recalculate();near(pv('C29'),phaseForce);near(wv('C23'),peak);near(value('C41'),checks.baseline.local_force_N);
for(const sheet of [s,lit,eq,wave,cycle]){const vals=sheet.getUsedRange().values;for(const row of vals)for(const v of row)assert.ok(!/^#(REF!|DIV\/0!|VALUE!|NAME\?|NUM!|N\/A|SPILL!|CALC!)/.test(String(v)),String(v));}
checks.formula_errors=0;checks.native_excel_tested=false;checks.physical_validation=false;
await fs.writeFile(path.join(outputDir,'spreadsheet_verification.json'),JSON.stringify(checks,null,2)+'\n');
await fs.writeFile(path.join(outputDir,'formula_inspection.txt'),JSON.stringify(await wb.inspect({kind:'table',range:"'Pressure start'!A24:F46",include:'values,formulas',tableMaxRows:23,tableMaxCols:6}),null,2));
await fs.writeFile(path.join(outputDir,'waveform_formula_inspection.txt'),JSON.stringify(await wb.inspect({kind:'table',range:"'Waveform'!A6:F31",include:'values,formulas',tableMaxRows:26,tableMaxCols:6}),null,2));
await fs.writeFile(path.join(outputDir,'pressure_cycle_formula_inspection.txt'),JSON.stringify(await wb.inspect({kind:'table',range:"'Pressure cycle'!A21:F38",include:'values,formulas',tableMaxRows:18,tableMaxCols:6}),null,2));
for(const [sheetName,range,file,scale] of [['Pressure cycle','A1:F41','pressure_cycle_inputs_preview.png',1],['Pressure cycle','A43:F66','pressure_cycle_charts_preview.png',1],['Pressure cycle','H6:P29','pressure_cycle_sources_preview.png',1],['Pressure cycle','A69:U74','pressure_cycle_build_preview.png',.8],['Equation map','A1:F4','equations_heading_preview.png',.7]]){const png=await wb.render({sheetName,range,scale,format:'png'});await fs.writeFile(path.join(outputDir,file),new Uint8Array(await png.arrayBuffer()));}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(outputDir,'Pump_pressure_literature_starter.xlsx'));
console.log(JSON.stringify(checks,null,2));
console.log('Saved '+path.join(outputDir,'Pump_pressure_literature_starter.xlsx'));

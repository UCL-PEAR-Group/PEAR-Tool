// Periodic load solution and conditional full-liquid phase pressures.
export function addPressureCycle(wb,base,band,textrow,coeffs,cfg){
 const p=base('Pressure cycle',871,'U',[34,13,23,19,36,43,16,18,17,17,17,19,18,19,19,20,20,19,21,21,21]);
 p.freezePanes.unfreeze();
 textrow(p,2,'Pressure cycle and physiological reference');p.getRange('A2:F2').format.font={size:17,bold:true};
 textrow(p,3,'Flow command from Waveform. Periodic three-element load. Chamber phases remain conditional on valve feasibility.');
 textrow(p,4,'Published reference: 75/min and 6.6 L/min, retained unscaled. Different operating conditions prevent a validation-error claim.');
 band(p,6,'F',['Control / result','Symbol','Value','Unit','Meaning','Basis']);
 const rows=[
 [7,'Arterial load','side','Systemic','choice','Select systemic or pulmonary trial','Load presets at H22:M24'],
 [8,'Inlet reservoir pressure','pi','=IF(C7="Systemic",I23,I24)','mmHg gauge','Constant inlet reservoir','Illustrative input; distinct from return'],
 [9,'Terminal return pressure','pr','=IF(C7="Systemic",J23,J24)','mmHg gauge','Pressure after distal resistance','Illustrative boundary'],
 [10,'Proximal resistance','R1','=IF(C7="Systemic",K23,K24)','mmHg s/mL','Effective proximal load term','Reference-informed trial'],
 [11,'Distal resistance','R2','=IF(C7="Systemic",L23,L24)','mmHg s/mL','Mean-load setting','Chosen for 90 / 15 mmHg at 5 L/min'],
 [12,'Load compliance','Cw','=IF(C7="Systemic",M23,M24)','mL/mmHg','Free parameter; not fitted','Edit preset to explore pulse pressure'],
 [14,'Inlet valve bore','dvi',cfg.inlet.valve_diameter_mm,'mm','Provisional effective area','Uncalibrated geometry'],
 [15,'Inlet discharge coefficient','Cdi',cfg.inlet.Cd,'dimensionless','Constant orifice approximation','Uncalibrated coefficient'],
 [16,'Inlet tube bore','Dti',cfg.inlet.tube_diameter_mm,'mm','Uniform line','Illustrative'],
 [17,'Inlet line length','Li',cfg.inlet.length_m,'m','Accelerating liquid segment','Illustrative'],
 [18,'Inlet local loss coefficient','Ki',cfg.inlet.K,'dimensionless','Additional local loss','No duplicate valve loss'],
 [19,'Additional inlet resistance','Ri',cfg.inlet.R_mmhg_s_ml,'mmHg s/mL','Zero means omitted','Not proof of negligible viscous loss'],
 [21,'Load decay time constant','tau','=C11*C12','s','Distal resistance × compliance','Exponential decay when outlet flow = 0'],
 [22,'Periodic starting excess pressure','y0','=J871/(1-EXP(-\'Waveform\'!C14/C21))','mmHg','pw(0) − pr','One-cycle map; no circular iteration'],
 [24,'Calculated mean arterial pressure','pa mean','=SUM(Q70:Q871)/\'Waveform\'!C14','mmHg gauge','Numerical cycle average','Mean is set by chosen resistance'],
 [25,'Minimum arterial pressure','pa min','=MIN(L70:L871)','mmHg gauge','Sampled arterial minimum','Load response'],
 [26,'Maximum arterial pressure','pa max','=MAX(L70:L871)','mmHg gauge','Sampled arterial maximum','Load response'],
 [27,'Minimum conditional chamber pressure','pc min','=MIN(N70:N871)','mmHg gauge','Phase calculation','Transitions excluded'],
 [28,'Maximum conditional chamber pressure','pc max','=MAX(N70:N871)','mmHg gauge','Phase calculation','Transitions excluded'],
 [29,'Phase-only maximum absolute force','Fh max','=MAX(MAX(O70:O871),-MIN(O70:O871))','N','NOT a complete-cycle force rating','Excludes seals and solid inertia'],
 [30,'Largest closed-valve inconsistency','violation','=MAX(P70:P871)','mmHg','Positive means assumed valve would open','Zero-cracking passive valves'],
 [31,'Pressure jump: ejection → filling','jump ef','=N471-N470','mmHg','Unresolved pressure transition','Right limit minus left limit'],
 [32,'Pressure jump: cycle wrap','jump fe','=N70-N871','mmHg','Unresolved pressure transition','Right limit minus left limit'],
 [34,'Reference mean arterial pressure','ref mean','=IF(C7="Systemic",K7,O7)','mmHg','Published functional reference','6.6 L/min; 75/min'],
 [35,'Reference arterial minimum','ref min','=MIN(S70:S871)','mmHg','Reconstructed, sampled','Not a population lower limit'],
 [36,'Reference arterial maximum','ref max','=MAX(S70:S871)','mmHg','Reconstructed, sampled','Not a population upper limit'],
 [38,'Within-phase valve result','status','=IF(C30>0.00000001,"INCONSISTENT","No conflict detected")','assessment','Checks assumed CLOSED branch only','Open forward flow may decelerate against gradient']
 ];
 for(const [r,label,symbol,v,unit,meaning,basis]of rows){p.getRange(`A${r}:F${r}`).values=[[label,symbol,null,unit,meaning,basis]];if(typeof v==='string'&&v.startsWith('='))p.getRange(`C${r}`).formulas=[[v]];else p.getRange(`C${r}`).values=[[v]];}
 p.getRange('A7:F38').format.rowHeight=31;p.getRange('A7:F38').format.wrapText=true;
 p.getRange('C8:C36').setNumberFormat('0.000');p.getRange('C7').format.fill='#FFF1CF';p.getRange('C14:C19').format.fill='#FFF1CF';
 p.getRange('C7').dataValidation={rule:{type:'list',values:['Systemic','Pulmonary']}};
 for(const r of [14,15,16,17])p.getRange(`C${r}`).dataValidation={rule:{type:'decimal',operator:'greaterThan',formula1:0}};
 textrow(p,40,'Both pressure transitions remain unresolved, even when the within-phase valve test detects no conflict.');
 textrow(p,41,'Outlet geometry, density and rear pressure link to Pressure start. No gas storage, valve events or distributed wave reflections.');
 p.getRange('H6:P6').values=[['k','Ao Q amp','Ao Q phase','Ao p amp','Ao p phase','PA Q amp','PA Q phase','PA p amp','PA p phase']];
 p.getRange('H6:P6').format={fill:'#17324D',font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:36};p.getRange('H7:P17').values=coeffs;
 p.getRange('H19:P20').merge();p.getRange('H19').values=[['Qureshi et al. (2018), author manuscript Appendix A Table A1, DOI 10.1088/1361-6579/aa9d60; harmonics from Milnor (1989). Amplitudes: mL/s or mmHg; phases: radians. Functional reference, not raw recordings.']];p.getRange('H19:P20').format.wrapText=true;
 p.getRange('H22:M22').values=[['Load','pi (mmHg)','pr (mmHg)','R1 (mmHg s/mL)','R2 (mmHg s/mL)','Cw (mL/mmHg)']];p.getRange('H22:M22').format={fill:'#17324D',font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:40};
 p.getRange('H23:M24').values=Object.entries(cfg.loads).map(([side,l])=>[side,l.inlet_pressure_mmhg,l.return_pressure_mmhg,l.R1_mmhg_s_ml,l.R2_mmhg_s_ml,l.C_ml_mmhg]);p.getRange('I23:M24').format.fill='#FFF1CF';p.getRange('I23:M24').setNumberFormat('0.000');
 p.getRange('K23:M24').dataValidation={rule:{type:'decimal',operator:'greaterThan',formula1:0}};
 p.getRange('H27:L27').values=[['Path','R (mmHg s/mL)','B (mmHg s²/mL²)','I (mmHg s²/mL)','Units use mL/s']];p.getRange('H27:L27').format={fill:'#17324D',font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:42};
 p.getRange('H28:H29').values=[['Outlet'],['Inlet']];
 p.getRange('I28:K29').formulas=[
 ["='Pressure start'!C20*0.06","='Pressure start'!C14/2*(1/('Pressure start'!C16*PI()*('Pressure start'!C15/1000)^2/4)^2+'Pressure start'!C19/(PI()*('Pressure start'!C17/1000)^2/4)^2)*0.000000000001/133.322","='Pressure start'!C14*'Pressure start'!C18/(PI()*('Pressure start'!C17/1000)^2/4)*0.000001/133.322"],
 ['=C19',"='Pressure start'!C14/2*(1/(C15*PI()*(C14/1000)^2/4)^2+C18/(PI()*(C16/1000)^2/4)^2)*0.000000000001/133.322","='Pressure start'!C14*C17/(PI()*(C16/1000)^2/4)*0.000001/133.322"]];
 p.getRange('I28:K29').setNumberFormat('0.000E+00');
 textrow(p,65,'Curves share normalised cycle phase. The reference remains at 75/min and 6.6 L/min when pump inputs change.');
 textrow(p,66,'Chamber pressures and force are available below as conditional phase values; the plotted arterial trace is not ventricular pressure.');
 band(p,69,'U',['Phase','Time (s)','Qo (mL/s)','Qi (mL/s)','dQo/dt (mL/s²)','dQi/dt (mL/s²)','dt (s)','Decay a','Forcing b (mmHg)','Zero-start y (mmHg)','pw (mmHg)','pa (mmHg)','Path dp (mmHg)','pc (mmHg)','Fh (N)','Violation (mmHg)','pa dt (mmHg s)','Cycle phase','Reference pa (mmHg)','Ref Q (L/min)','Pump Q (L/min)']);p.getRange('A69:U69').format.wrapText=true;p.getRange('A69:U69').format.rowHeight=42;
 const forms=[];
 const series=(amp,phase,r)=>`$${amp}$7+`+Array.from({length:10},(_,i)=>`$${amp}$${8+i}*COS(2*PI()*$H$${8+i}*R${r}+$${phase}$${8+i})`).join('+');
 for(let r=70;r<=871;r++){
  const w=r-10,first=r===70;
  forms.push([
   `='Waveform'!A${w}`,`='Waveform'!C${w}`,`='Waveform'!Q${w}/0.06`,`='Waveform'!R${w}/0.06`,
   `=IF(A${r}=0,'Waveform'!M${w},0)`,`=IF(A${r}=1,-'Waveform'!M${w},0)`,first?'=0':`=B${r}-B${r-1}`,
   `=EXP(-G${r}/$C$21)`,first?'=0':`=IF(G${r}=0,0,$C$11*(C${r-1}*(1-H${r})+(C${r}-C${r-1})*(1-$C$21/G${r}*(1-H${r}))))`,
   first?'=0':`=H${r}*J${r-1}+I${r}`,`=$C$9+J${r}+$C$22*EXP(-B${r}/$C$21)`,
   `=K${r}+$C$10*C${r}`,`=IF(A${r}=0,$I$28*C${r}+$J$28*C${r}^2+$K$28*E${r},$I$29*D${r}+$J$29*D${r}^2+$K$29*F${r})`,
   `=IF(A${r}=0,L${r}+M${r},$C$8-M${r})`,`='Waveform'!$C$18*(N${r}-'Pressure start'!$C$13)*133.322`,
   `=IF(A${r}=0,MAX(0,$C$8-N${r}),MAX(0,N${r}-L${r}))`,first?'=0':`=(L${r}+L${r-1})/2*G${r}`,
   `=B${r}/'Waveform'!$C$14`,`=IF($C$7="Systemic",${series('K','L',r)},${series('O','P',r)})`,
   `=IF($C$7="Systemic",${series('I','J',r)},${series('M','N',r)})*0.06`,`=C${r}*0.06`
  ]);
 }
 p.getRange('A70:U871').formulas=forms;p.getRange('B70:U871').setNumberFormat('0.0000');
 p.getRange('P70:P871').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:1e-8,format:{fill:'#FDE7E7',font:{color:'#A00020'}}});
 p.getRange('C30').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:1e-8,format:{fill:'#FDE7E7',font:{color:'#A00020'}}});
 for(const [cols,title,unit,start,end]of [[['L','S'],'Arterial pressure comparison','mmHg gauge','A44','C62'],[['U','T'],'Outlet flow comparison','L/min','D44','F62']]){
  const c=p.charts.add('scatter',[p.getRange('R69:R871'),...cols.map(col=>p.getRange(`${col}69:${col}871`))]);c.title=title;c.setPosition(start,end);c.legend={position:'top',textStyle:{typeface:'Arial',fontSize:11}};
  c.xAxis.title.text='Normalised cycle phase';c.yAxis.title.text=unit;c.titleTextStyle.fontSize=14;c.titleTextStyle.typeface='Arial';c.xAxis.numberFormatCode='0.0';c.yAxis.numberFormatCode='0.0';
  c.series.items[0].line={fill:'#176B72',style:'solid',width:2};c.series.items[1].line={fill:'#757F89',style:'dashed',width:2};
 }
 return p;
}

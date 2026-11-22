// Extend the existing workbook with one transparent, formula-driven kinematic build.
export function addWaveformSheet(wb, base, band, textrow) {
 const w=base('Waveform',861,'R',[33,12,25,18,33,42,16,18,16,16,16,18,20,18,18,20,20,20]);
 w.freezePanes.unfreeze();
 textrow(w,2,'Piston waveform and stroke reversals');w.getRange('A2:F2').format.font={size:17,bold:true};
 textrow(w,3,'One dedicated chamber. Full liquid, no leakage or dwell. Pressure and gas dynamics are not solved here.');
 textrow(w,4,'Amber cells select shape and smoothing. Flow, rate, diameter and timing link to Pressure start.');
 band(w,6,'F',['Control / result','Symbol','Value','Unit','Meaning','Basis']);
 const entries=[
 [7,'Shape pair','shape','Published harmonics','choice','Swanson–Clark / Talukder–Reul or half-sine','Published shapes; coefficients at H6:K8'],
 [8,'Endpoint smoothing width','epsilon',.05,'phase fraction','At EACH end of each phase; zero = raw','Engineering trial, not an optimum'],
 [9,'Mean circuit flow','Qmean',"='Pressure start'!C7",'L/min','Prescribed mean','Linked input'],
 [10,'Delivery rate','h',"='Pressure start'!C8",'/min','Per dedicated chamber','Linked input'],
 [11,'Piston diameter','D',"='Pressure start'!C9",'mm','Illustrative design value','Linked input'],
 [12,'Ejection fraction','gamma',"='Pressure start'!C10",'fraction','0.4 means filling:ejection = 60:40','Linked input'],
 [14,'Cycle period','T','=60/C10','s','No dwell','Time conversion'],
 [15,'Required phase volume','Vs','=1000*C9/C10','mL','Same filling and ejection volume','Mean flow / delivery rate'],
 [16,'Ejection duration','te','=C12*C14','s','Piston advance','gamma × T'],
 [17,'Filling duration','tf','=(1-C12)*C14','s','Piston return','(1 − gamma) × T'],
 [18,'Piston area','Ap','=PI()*(C11/1000)^2/4','m²','Flat face','Circular geometry'],
 [19,'Required ideal travel','S','=C15*0.001/C18','mm','Changes with target flow / rate','Not variable stroke on fixed hardware'],
 [20,'Ejection shape integral','Ge','=SUM(K60:K460)','dimensionless','Trapezoidal integral, 400 intervals','Normalises ejection volume'],
 [21,'Filling shape integral','Gf','=SUM(K461:K861)','dimensionless','Trapezoidal integral, 400 intervals','Normalises filling volume'],
 [23,'Peak ejection flow','Qe,max','=MAX(Q60:Q460)','L/min','Sampled maximum','400 intervals per phase'],
 [24,'Peak filling flow','Qi,max','=MAX(R461:R861)','L/min','Sampled maximum','400 intervals per phase'],
 [25,'Maximum absolute acceleration','a,max','=MAX(MAX(P60:P861),-MIN(P60:P861))','m/s²','Piston kinematics; not force','Sampled maximum'],
 [26,'Return position / stroke','x(T)/S','=N861','dimensionless','Should be near zero','Discrete volume conservation'],
 [28,'Ejection transition duration','epsilon te','=1000*C8*C16','ms','At EACH endpoint','Width × phase duration'],
 [29,'Filling transition duration','epsilon tf','=1000*C8*C17','ms','At EACH endpoint','Width × phase duration'],
 [30,'Acceleration jump: eject → fill','jump ef','=P461-P460','m/s²','Zero for positive smoothing','Right limit − left limit'],
 [31,'Acceleration jump: cycle wrap','jump fe','=P60-P861','m/s²','Zero for positive smoothing','Right limit − left limit']
 ];
 for(const [r,label,symbol,v,unit,meaning,basis] of entries){
   w.getRange(`A${r}:F${r}`).values=[[label,symbol,null,unit,meaning,basis]];
   if(typeof v==='string'&&v.startsWith('='))w.getRange(`C${r}`).formulas=[[v]];else w.getRange(`C${r}`).values=[[v]];
 }
 w.getRange('A7:F31').format.rowHeight=29;
 w.getRange('E7:F31').format.wrapText=true;w.getRange('A7:F8').format.rowHeight=40;
 w.getRange('C7:C8').format.fill='#FFF1CF';w.getRange('C8:C31').setNumberFormat('0.000');
 w.getRange('C8').setNumberFormat('0.0%');w.getRange('C12').setNumberFormat('0%');w.getRange('C18').setNumberFormat('0.000E+00');
 w.getRange('C7').dataValidation={rule:{type:'list',values:['Published harmonics','Half-sine']}};
 w.getRange('C8').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:.5}};
 textrow(w,33,'Use epsilon = 0 or 0.02–0.50 on this grid. Smaller nonzero widths need finer sampling in Python.');
 textrow(w,34,'Smoothing removes acceleration jumps but can raise peak acceleration. Force still requires the hydraulic model.');
 w.getRange('H6:K8').values=[['Phase','c1','c2','c3'],['Ejection',.924,.230,.092],['Filling',.520,.257,.479]];
 w.getRange('H6:K6').format={fill:'#17324D',font:{color:'#FFFFFF',bold:true},rowHeight:29};
 w.getRange('I7:K8').setNumberFormat('0.000');
 w.getRange('H10:R11').merge();w.getRange('H10').values=[['Coefficients: Franzetti et al. 2019, supplied PDF p. 5, Eqs 14–15, DOI 10.1115/1.4044488. Half-sine uses c1 = 1, c2 = c3 = 0. Endpoint window is our engineering extension.']];w.getRange('H10:R11').format.wrapText=true;
 textrow(w,56,'Detailed calculation below: phase 0 = ejection, phase 1 = filling; Qp is signed piston displacement flow.');
 textrow(w,57,'G is integrated numerically. Acceleration uses analytic shape derivatives; volume uses the same quadrature as position.');
 band(w,59,'R',['Phase','u','Cycle t (s)','Raw g','dg/du','Window z','w','dw/du','g w','d(g w)/du','Area increment','Qp (mL/s)','dQp/dt (mL/s²)','x / S','Velocity (mm/s)','Acceleration (m/s²)','Outlet (L/min)','Inlet (L/min)']);
 w.getRange('A59:R59').format.wrapText=true;w.getRange('A59:R59').format.rowHeight=42;
 const forms=[];
 for(let phase=0;phase<2;phase++) for(let j=0;j<=400;j++){
   const r=60+phase*401+j,start=phase?461:60,crow=phase?8:7;
   const dur=phase?'$C$17':'$C$16', norm=phase?'$C$21':'$C$20',sign=phase?-1:1;
   forms.push([
    `=${phase}`,`=${j}/400`,`=${phase?'$C$16+':''}B${r}*${dur}`,
    `=IF($C$7="Half-sine",SIN(PI()*B${r}),$I$${crow}*SIN(PI()*B${r})+$J$${crow}*SIN(2*PI()*B${r})+$K$${crow}*SIN(3*PI()*B${r}))`,
    `=IF($C$7="Half-sine",PI()*COS(PI()*B${r}),PI()*($I$${crow}*COS(PI()*B${r})+2*$J$${crow}*COS(2*PI()*B${r})+3*$K$${crow}*COS(3*PI()*B${r})))`,
    `=IF($C$8=0,1,MIN(1,MIN(B${r},1-B${r})/$C$8))`,
    `=10*F${r}^3-15*F${r}^4+6*F${r}^5`,
    `=IF($C$8=0,0,IF(B${r}<$C$8,1,IF(B${r}>1-$C$8,-1,0))*30*F${r}^2*(1-F${r})^2/$C$8)`,
    `=D${r}*G${r}`,`=E${r}*G${r}+D${r}*H${r}`,
    j===0?'=0':`=(I${r}+I${r-1})/2*(B${r}-B${r-1})`,
    `=${sign}*$C$15/${dur}*I${r}/${norm}`,
    `=${sign}*$C$15/${dur}^2*J${r}/${norm}`,
    `=${phase?'1-':''}SUM(K${start}:K${r})/${norm}`,
    `=L${r}*0.001/$C$18`,`=M${r}*0.000001/$C$18`,
    phase?'=0':`=L${r}*0.06`,phase?`=-L${r}*0.06`:'=0'
   ]);
 }
 w.getRange('A60:R861').formulas=forms;
 w.getRange('B60:R861').setNumberFormat('0.0000');w.getRange('A60:A861').setNumberFormat('0');
 const flow=w.charts.add('scatter',[w.getRange('C59:C861'),w.getRange('Q59:Q861'),w.getRange('R59:R861')]);
 flow.title='Outlet and inlet flow';flow.setPosition('A36','C53');flow.legend={position:'top',textStyle:{typeface:'Arial',fontSize:11}};
 flow.xAxis.title.text='Cycle time (s)';flow.yAxis.title.text='Flow (L/min)';
 flow.series.items[0].line={fill:'#176B72',style:'solid',width:2};flow.series.items[1].line={fill:'#B9622E',style:'solid',width:2};
 const accel=w.charts.add('scatter',[w.getRange('C59:C861'),w.getRange('P59:P861')]);
 accel.title='Piston acceleration';accel.hasLegend=false;accel.setPosition('D36','F53');
 accel.xAxis.title.text='Cycle time (s)';accel.yAxis.title.text='Acceleration (m/s²)';
 accel.series.items[0].line={fill:'#176B72',style:'solid',width:2};
 for(const c of [flow,accel]){c.titleTextStyle.fontSize=14;c.titleTextStyle.typeface='Arial';c.xAxis.numberFormatCode='0.0';c.yAxis.numberFormatCode='0.0';c.xAxis.textStyle={typeface:'Arial',fontSize:11};c.yAxis.textStyle={typeface:'Arial',fontSize:11};}
 return w;
}

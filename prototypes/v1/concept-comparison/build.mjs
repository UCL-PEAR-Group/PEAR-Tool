import fs from 'node:fs/promises';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const [design,outputDir]=process.argv.slice(2);
if(!design||!outputDir)throw Error('Usage: node build.mjs <design-directory> <output-directory>');
const source=await Workbook.fromCSV(await fs.readFile(`${design}/WEIGHTED_DESIGN_MATRIX.csv`,'utf8'),{sheetName:'Input'});
const criteria=source.worksheets.getItem('Input').getRange('A2:D11').values.map(r=>[r[0],r[1],Number(r[2]),r[3]]);
const concepts=['Piston','Diaphragm','Impeller','Peristaltic'];
const wb=Workbook.create();
const main=wb.worksheets.add('Comparison');
const notes=wb.worksheets.add('Criteria and notes');
const palette={ink:'#24394C',muted:'#526477',header:'#314C65',input:'#FFF2CC',line:'#C8D2DC',pale:'#EDF1F5',red:'#FCE4D6'};
function base(sheet,range){sheet.showGridLines=false;sheet.getRange(range).format={font:{name:'Arial',size:11,color:palette.ink},verticalAlignment:'center',rowHeight:23};sheet.getRange('A1:A40').format.columnWidthPx=22;}
function header(sheet,range){sheet.getRange(range).format={fill:palette.header,font:{color:'#FFFFFF',bold:true},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,borders:{insideVertical:{style:'thin',color:'#FFFFFF'}}};}
function title(sheet,cell,text){sheet.getRange(cell).values=[[text]];sheet.getRange(cell).format.font={name:'Arial',size:17,bold:true,color:palette.ink};}
base(main,'A1:I33');base(notes,'A1:H17');
main.tabColor=palette.header;
main.getRange('B1:B33').format.columnWidthPx=55;
main.getRange('C1:C33').format.columnWidthPx=282;
main.getRange('D1:D33').format.columnWidthPx=94;
main.getRange('E1:H33').format.columnWidthPx=151;
title(main,'B2','Pump concept comparison');
main.getRange('B3').values=[['Amber cells are editable. Add scores, concept details and supporting notes.']];
main.getRange('B4').values=[['Score 1–5: poor, constrained, plausible, strong, evidenced. Leave unknown scores blank.']];
main.getRange('B3:H4').format.font={name:'Arial',size:11,color:palette.muted};
main.getRange('B5:H5').format.borders={bottom:{style:'thin',color:palette.line}};
main.getRange('B6:H6').values=[['ID','Attribute','Weight',...concepts]];header(main,'B6:H6');
main.getRange('B7:D16').values=criteria.map(r=>r.slice(0,3));
main.getRange('B7:H16').format.rowHeight=32;
main.getRange('B7:H16').format.borders={insideHorizontal:{style:'thin',color:'#E3E7EB'}};
main.getRange('C7:C16').format.wrapText=true;
main.getRange('D7:H16').format.fill=palette.input;
main.getRange('D7:D16').format.numberFormat='0.00';
main.getRange('E7:H16').format.numberFormat='0';
main.getRange('D7:H16').format.horizontalAlignment='right';
main.dataValidations.add({range:'E7:H16',rule:{type:'whole',operator:'between',formula1:1,formula2:5}});
main.getRange('E7:H16').conditionalFormats.addCustom('=AND(E7<>"",NOT(OR(E7=1,E7=2,E7=3,E7=4,E7=5)))',{fill:palette.red,font:{color:'#9C0006',bold:true}});
main.getRange('D7:D16').conditionalFormats.addCustom('=AND(D7<>"",OR(NOT(ISNUMBER(D7)),D7<0,D7>1))',{fill:palette.red,font:{color:'#9C0006',bold:true}});
main.getRange('C18').values=[['Weighted total / 5']];main.getRange('D18').formulas=[['=SUM(D7:D16)']];
main.getRange('C19').values=[['Valid scores entered']];
main.getRange('C20').values=[['Rank (1 = highest)']];
main.getRange('C21').values=[['Score status']];
main.getRange('D20').formulas=[['=IF(AND(COUNT(D7:D16)=10,MIN(D7:D16)>=0,MAX(D7:D16)<=1,ABS(D18-1)<0.000000001),"Weights OK","Fix weights")']];
for(const col of ['E','F','G','H']){
 main.getRange(`${col}19`).formulas=[['='+Array.from({length:10},(_,i)=>`IF(AND(ISNUMBER(${col}${i+7}),OR(${[1,2,3,4,5].map(v=>`${col}${i+7}=${v}`).join(',')})),1,0)`).join('+')]];
 main.getRange(`${col}18`).formulas=[[`=IF(AND(${col}19=10,$D$20="Weights OK"),ROUND(SUMPRODUCT($D$7:$D$16,${col}7:${col}16),6),"")`]];
 main.getRange(`${col}20`).formulas=[[`=IF(COUNT($E$18:$H$18)=4,1+COUNTIFS($E$18:$H$18,">"&${col}18),"")`]];
 main.getRange(`${col}21`).formulas=[[`=IF(COUNTA(${col}7:${col}16)=0,"Add scores",IF(COUNTA(${col}7:${col}16)<>${col}19,"Use integers 1-5",IF(${col}19<10,"Complete scores",IF($D$20<>"Weights OK","Check weights","Scored"))))`]];
}
main.getRange('C18:H18').format={fill:palette.pale,font:{bold:true},borders:{top:{style:'thin',color:palette.line}},rowHeight:28};
main.getRange('D18:H18').format.numberFormat='0.00';
main.getRange('E19:H19').format.numberFormat='0" / 10"';
main.getRange('D20:H21').format.font={name:'Arial',size:11,color:palette.muted};
main.getRange('D20').conditionalFormats.add('containsText',{text:'Fix',format:{fill:palette.red,font:{color:'#9C0006'}}});
main.getRange('B23').values=[['Totals require ten valid scores and weights summing to 1.00. Ranking requires all four totals; ties share rank.']];
main.getRange('B24').values=[['Total = sum of weight × score. A ranking does not establish compliance with the PDS.']];
main.getRange('B23:H24').format.font={name:'Arial',size:11,color:palette.muted};
main.getRange('C26:H26').values=[['Concept details','',...concepts]];header(main,'C26:C26');header(main,'E26:H26');
main.getRange('C27:C30').values=[['Specific design / variant'],['Actuation and valves'],['Operating conditions / assumptions'],['Key references / sketch links']];
main.getRange('C27:C30').format.wrapText=true;
main.getRange('E27:H30').format={fill:palette.input,wrapText:true,verticalAlignment:'top'};
main.getRange('C27:H30').format.borders={insideHorizontal:{style:'thin',color:'#E3E7EB'}};
main.getRange('B27:H30').format.rowHeight=55;
main.freezePanes.freezeRows(6);

notes.getRange('B1:B17').format.columnWidthPx=55;
notes.getRange('C1:C17').format.columnWidthPx=385;
notes.getRange('D1:G17').format.columnWidthPx=222;
title(notes,'B2','Criteria and supporting notes');
notes.getRange('B3').values=[['Criteria and weights: supplied project matrix, 23 November 2026.']];
notes.getRange('B4').values=[['Record the evidence, score reasoning and unresolved assumptions for each concept in the amber fields.']];
notes.getRange('B3:G4').format.font={name:'Arial',size:11,color:palette.muted};
notes.getRange('B6:G6').values=[['ID','What a high score means',...concepts]];header(notes,'B6:G6');
notes.getRange('B7:C16').values=criteria.map(r=>[r[0],r[3]]);
notes.getRange('B7:G16').format={rowHeight:60,wrapText:true,verticalAlignment:'top',borders:{insideHorizontal:{style:'thin',color:'#E3E7EB'}}};
notes.getRange('D7:G16').format.fill=palette.input;
notes.freezePanes.freezeRows(6);
notes.freezePanes.freezeColumns(3);

const checkLog=[];
function assert(condition,label){if(!condition)throw Error(label);checkLog.push(label);}
function values(addr){return main.getRange(addr).values.flat();}
function setScores(matrix){main.getRange('E7:H16').values=matrix;wb.recalculate();}
wb.recalculate();
assert(values('E18:H18').every(v=>v===''||v===null),'Blank inputs do not yield totals');
assert(values('E20:H20').every(v=>v===''||v===null),'Blank inputs do not yield ranks');
let trial=Array.from({length:10},()=>[3,4,2,5]);setScores(trial);
assert(JSON.stringify(values('E18:H18'))===JSON.stringify([3,4,2,5]),'Known scores produce expected weighted totals');
assert(JSON.stringify(values('E20:H20'))===JSON.stringify([3,2,4,1]),'Ranking follows totals');
trial=Array.from({length:10},()=>[5,4,2,3]);setScores(trial);
assert(JSON.stringify(values('E20:H20'))===JSON.stringify([1,2,4,3]),'Changing inputs changes ranking');
trial[0][0]=null;setScores(trial);
assert(values('E18')[0]===''&&values('F18')[0]===4,'Missing score suppresses only its concept total');
assert(values('E20:H20').every(v=>v===''),'Incomplete comparison has no ranking');
for(const invalid of [0,6,2.5,'unknown','3']){trial[0][0]=invalid;setScores(trial);assert(values('E18')[0]==='',`Invalid score ${JSON.stringify(invalid)} suppresses total`);}
trial=Array.from({length:10},()=>[3,3,3,3]);setScores(trial);
assert(values('E20:H20').every(v=>v===1),'Equal totals share rank');
main.getRange('D7').values=[[0.20]];wb.recalculate();assert(values('E18:H18').every(v=>v===''),'Weights not summing to one suppress totals');
main.getRange('D7').values=[[criteria[0][2]]];
main.getRange('E7:H16').clear({applyTo:'contents'});wb.recalculate();
assert(values('E19:H19').every(v=>v===0),'Final score inputs restored to blank');
assert(Math.abs(values('D18')[0]-1)<1e-12,'Original weights preserved');
const inspection=await wb.inspect({kind:'table',range:'Comparison!C18:H21',include:'values,formulas',tableMaxRows:4,tableMaxCols:6,maxChars:5500});
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},maxChars:2000});
await fs.mkdir(outputDir,{recursive:true});
for(const [sheetName,range,name] of [['Comparison','B2:H30','comparison_preview.png'],['Criteria and notes','B2:G16','notes_preview.png']]){
 const img=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(`${outputDir}/${name}`,new Uint8Array(await img.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(`${outputDir}/Pump_Concept_Comparison.xlsx`);
await fs.writeFile(`${outputDir}/verification.json`,JSON.stringify({checks:checkLog,inspection:inspection.ndjson,error_scan:errors.ndjson,native_excel_or_libreoffice_execution:false},null,2));
console.log(JSON.stringify({output:`${outputDir}/Pump_Concept_Comparison.xlsx`,checks:checkLog.length,inspection:inspection.ndjson,errors:errors.ndjson}));

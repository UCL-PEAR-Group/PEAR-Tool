%[text] # Design 1: Piston Pump — living calculations
%[text] MECH0073 / PEAR, V1 prototype. This plain-text Live Script is the MATLAB calculation entry point. Read ../MODEL.md for assumptions, decisions and the complete model definition. Archived numerical results were generated in Python. The MATLAB dynamic port must pass verify_reference before its results replace that reference.
%%
%[text] ## Prescribed operating point and free geometry
c=pump_parameters();
requestedFlow_Lmin=5;
requestedBPM=75;
diameter_mm=c.diameter_mm;
geometricStroke_mL=c.swept_ml;
pistonArea_mm2=pi*diameter_mm^2/4;
travel_mm=1000*geometricStroke_mL/pistonArea_mm2;
requiredNetDelivery_mL=1000*requestedFlow_Lmin/requestedBPM;
disp(table(requestedFlow_Lmin,requestedBPM,diameter_mm,travel_mm, ...
    geometricStroke_mL,requiredNetDelivery_mL));
%[text] Mean circuit flow [L/min] = net delivered volume [mL/beat] × delivery frequency [beats/min] / 1000. Net delivered volume is measured or calculated; it is not automatically equal to geometric piston displacement when gas, valve transients or a bypass are present.
%%
%[text] ## Fixed stroke: compatible flow and frequency
bpm=[40;60;75;90;120;150;180];
geometricFlow_Lmin=bpm*geometricStroke_mL/1000;
targetDelivery_mL=1000*requestedFlow_Lmin./bpm;
idealDeliveredFraction=targetDelivery_mL/geometricStroke_mL;
idealBypassFraction=1-idealDeliveredFraction;
idealBypassFraction(idealDeliveredFraction>1)=NaN;
disp(table(bpm,geometricFlow_Lmin,targetDelivery_mL, ...
    idealDeliveredFraction,idealBypassFraction));
figure('Name','Fixed-stroke operating constraints');
tiledlayout(1,2);
nexttile;plot(bpm,geometricFlow_Lmin,'o-','LineWidth',1.8);hold on;
yline(requestedFlow_Lmin,'--');grid on;
xlabel('Delivery frequency (beats/min)');ylabel('Mean flow (L/min)');
legend('Ideal full-stroke delivery','Requested flow','Location','best');
nexttile;plot(bpm,targetDelivery_mL,'o-','LineWidth',1.8);hold on;
yline(geometricStroke_mL,'--');grid on;
xlabel('Delivery frequency (beats/min)');ylabel('Volume per beat (mL)');
legend('Required net delivery','Geometric swept volume','Location','best');
%[text] The bypass calculation is an ideal volume budget, not a simulated bypass controller. A fraction above one cannot be obtained merely by diverting part of one ideal full stroke. For two ventricular chambers in series, apply the per-beat relation to each circuit; do not add their flows to claim doubled cardiac output.
%%
%[text] ## Diameter–travel relationship
D=(30:5:70)';
S=4*1000*geometricStroke_mL./(pi*D.^2);
disp(table(D,S,'VariableNames',{'PistonDiameter_mm','Travel_mm'}));
%[text] Geometric swept volume = piston-face area × travel. Cylinder length, piston thickness, port clearance and residual chamber volume must be accounted for separately. No rod area is subtracted from this plunger's wetted face.
%%
%[text] ## Archived hydraulic trends — executed Python reference
here=fileparts(mfilename('fullpath'));
referenceDir=fullfile(here,'..','archive','pump_hydraulic_sweep');
data=readtable(fullfile(referenceDir,'case_results.csv'));
base=data(strcmp(data.group,'main') & strcmp(data.status,'periodic') ...
    & data.gas_ref_ml==10,:);
figure('Name','Archived hydraulic parameter sweep');
tiledlayout(2,2);
nexttile;hold on;
for bore=[8,12,16,20]
    rows=sortrows(base(base.valve_in_mm==bore,:),'f');
    semilogy(rows.f,rows.force_absmax_N,'o-','LineWidth',1.5, ...
        'DisplayName',sprintf('%g mm valves',bore));
end
set(gca,'YScale','log');grid on;legend('Location','best');
xlabel('Frequency (beats/min)');ylabel('Peak hydraulic force (N)');
title('Frequency and valve restriction');
nexttile;hold on;
for f=[75,180]
    rows=sortrows(base(base.f==f,:),'valve_in_mm');
    plot(rows.valve_in_mm,rows.force_absmax_N,'o-','LineWidth',1.5, ...
        'DisplayName',sprintf('%g/min',f));
end
grid on;legend('Location','best');
xlabel('Inlet and outlet bore (mm)');ylabel('Peak hydraulic force (N)');
title('Valve diameter');
nexttile;hold on;
for f=[75,180]
    row=base(base.f==f & base.valve_in_mm==16,:);
    plot(D,row.force_absmax_N*(D/50).^2,'LineWidth',1.5, ...
        'DisplayName',sprintf('%g/min, 16 mm valves',f));
end
grid on;legend('Location','best');
xlabel('Piston diameter (mm)');ylabel('Peak hydraulic force (N)');
title('Fixed swept-volume history; travel changes');
nexttile;hold on;
for bore=[8,12,16,20]
    rows=sortrows(base(base.valve_in_mm==bore,:),'f');
    plot(rows.f,rows.Q_Lmin,'o-','LineWidth',1.5, ...
        'DisplayName',sprintf('%g mm valves',bore));
end
yline(5,'--','5 L/min');grid on;legend('Location','best');
xlabel('Frequency (beats/min)');ylabel('Mean outlet flow (L/min)');
title('Fixed travel; flow remains an output');
%%
%[text] ## Within-cycle force and air sensitivity
waves=jsondecode(fileread(fullfile(referenceDir,'waveforms.json')));
keys={'f75_d16','f180_d16','f180_d8'};
figure('Name','Archived force waveforms and air sensitivity');
tiledlayout(2,2);
for j=1:3
    nexttile;w=waves.(keys{j});
    plot(w.phase,w.pressure_force_N,'LineWidth',1.5);grid on;
    xlabel('Cycle fraction');ylabel('Signed hydraulic force (N)');
    title(strrep(keys{j},'_',' / '));xline(.4,'--','Return starts');
end
nexttile;hold on;
settings=[75,16;180,16;180,8];
for j=1:3
    rows=data(strcmp(data.group,'main') & strcmp(data.status,'periodic') ...
        & data.f==settings(j,1) & data.valve_in_mm==settings(j,2),:);
    rows=sortrows(rows,'gas_ref_ml');
    plot(rows.gas_ref_ml,rows.force_absmax_N,'o-','LineWidth',1.5, ...
        'DisplayName',sprintf('%g/min, %g mm',settings(j,:)));
end
grid on;legend('Location','best');
xlabel('Reference air volume at 10 mmHg gauge (mL)');ylabel('Peak hydraulic force (N)');
%[text] The three waveform panels have different vertical scales. Pressure force uses chamber pressure minus rear pressure, not simply outlet minus inlet pressure. Rear pressure is atmospheric in these tests. The gas changes both filling and ejection dynamics; its reference volume is not its instantaneous volume.
%%
%[text] ## Recalculate the baseline in MATLAB
%[text] Set runDynamic true after running verify_reference. This calls the translated ODE/event model rather than loading archived results. Runtime parity is not yet established in the preparation environment.
runDynamic=false;
if runDynamic
    [baseline,trace]=pump_simulate(c);
    disp(struct2table(baseline));
    if strcmp(baseline.status,'periodic')
        figure('Name','New MATLAB baseline');
        plot(trace.time_s,trace.pressure_force_N,'LineWidth',1.5);grid on;
        xlabel('Time (s)');ylabel('Signed hydraulic force (N)');
    end
end
%[text] Run run_sweep separately to regenerate all 118 cases. New outputs go to results/matlab; the archived reference is preserved. These are uncalibrated hydraulic predictions, with actuator loads, seal friction, solid inertia and whole-loop Windkessel dynamics outside the current model.

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---

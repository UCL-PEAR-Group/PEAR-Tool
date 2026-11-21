function checks=verify_reference()
%VERIFY_REFERENCE Cross-language and conservation checks; not validation.
% Must be executed in MATLAB before using the port to replace reference data.
here=fileparts(mfilename('fullpath'));
ref=readtable(fullfile(here,'..','archive','pump_hydraulic_sweep','selected_cases.csv'));
settings=[75,16;180,16;180,8];
checks=zeros(size(settings,1),5);
for j=1:size(settings,1)
    c=pump_parameters(); c.f=settings(j,1);
    c.valve_in_mm=settings(j,2); c.valve_out_mm=settings(j,2);
    [r,~]=pump_simulate(c);
    assert(strcmp(r.status,'periodic'),'Case did not reach periodic operation.');
    row=ref(ref.f==c.f & ref.valve_in_mm==c.valve_in_mm,:);
    assert(height(row)==1,'Reference row must be unique.');
    forceError=abs(r.force_absmax_N-row.force_absmax_N)/row.force_absmax_N;
    flowError=abs(r.Q_Lmin-row.Q_Lmin)/row.Q_Lmin;
    assert(forceError<1e-3,'Pressure force differs by more than 0.1%%.');
    assert(flowError<1e-3,'Mean flow differs by more than 0.1%%.');
    assert(r.balance_error_ml<1e-3,'Chamber volume balance residual too large.');
    assert(r.net_cycle_error_ml<1e-3,'Inlet/outlet periodic balance failed.');
    assert(r.min_flow_ml_s>-1e-6,'Reverse check-valve flow exceeds tolerance.');
    checks(j,:)=[c.f,c.valve_in_mm,forceError,flowError,r.balance_error_ml];
end
c=pump_parameters(); T=60/c.f;
[u,q,dq]=pump_motion([0,c.ejection_fraction*T,T],c);
assert(max(abs(u-[0,c.swept_ml,0]))<1e-9,'Motion endpoint volume failed.');
assert(max(abs(q))<1e-9 && max(abs(dq))<1e-8,'Motion endpoint smoothness failed.');
c.f=180; c.valve_in_mm=8; c.valve_out_mm=8; c.gas_ref_ml=1;
r=pump_simulate(c);
assert(strcmp(r.status,'low_pressure_guard'),'Expected low-pressure guard did not occur.');
checks=array2table(checks,'VariableNames',{'bpm','Valve_mm', ...
    'ForceRelativeError','FlowRelativeError','BalanceError_mL'});
disp(checks);
fprintf('MATLAB comparison and conservation checks passed. Physical validation remains outstanding.\n');
end

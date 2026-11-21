function [r,trace] = pump_simulate(c,opt)
%PUMP_SIMULATE Retained-gas chamber with ideal check valves and leg inertance.
% MATLAB port of archive/pump_hydraulic_sweep/hydraulic_sweep.py.
% Runtime verification in MATLAB is pending. See verify_reference.m.
% State: [chamber gauge mmHg; inlet mL/s; outlet mL/s; inlet mL; outlet mL].
if nargin<2, opt=struct(); end
if ~isfield(opt,'RelTol'), opt.RelTol=2e-7; end
if ~isfield(opt,'MaxStepDiv'), opt.MaxStepDiv=120; end
if ~isfield(opt,'MaxCycles'), opt.MaxCycles=24; end
if ~isfield(opt,'NPoints'), opt.NPoints=2401; end
validateattributes(c.gas_ref_ml,{'numeric'},{'scalar','positive','finite'});
validateattributes(c.f,{'numeric'},{'scalar','positive','finite'});
validateattributes(c.ejection_fraction,{'numeric'},{'scalar','>',0,'<',1});
validateattributes([c.diameter_mm,c.swept_ml,c.valve_in_mm,c.valve_out_mm, ...
    c.tube_d_mm,c.tube_l_m,c.Cd,c.n,c.rho],{'numeric'},{'positive','finite'});
assert(c.pin_mmhg+c.atmosphere_mmhg>c.pressure_floor_abs_mmhg, ...
    'Initial inlet pressure is below the exploratory guard.');
[Bi,Ii]=pump_coefficients(c,c.valve_in_mm);
[Bo,Io]=pump_coefficients(c,c.valve_out_mm);
T=60/c.f;
y=[c.pin_mmhg;0;0;0;0];
opened=[false,false];
active=opened;
segmentStart=0;
openingTol=1e-6; % mmHg: numerical event regularisation only
r=c; r.status='not_periodic'; r.cycles=0; r.periodic_residual=NaN;
fields={'pc_peak_mmhg','pc_min_mmhg','force_peak_N','force_min_N', ...
    'force_absmax_N','delivered_ml','inlet_ml','Q_Lmin','eta', ...
    'qout_peak_Lmin','qin_peak_Lmin','fill_deficit_ml','liquid_min_ml', ...
    'gas_max_ml','balance_error_ml','net_cycle_error_ml','min_flow_ml_s'};
for j=1:numel(fields), r.(fields{j})=NaN; end
trace=struct();
assert(c.residual_ml+c.swept_ml-gasVolume(c.pin_mmhg)>.1, ...
    'Initial liquid inventory is below the guard.');
for cycle=1:opt.MaxCycles
    startY=y; y(4:5)=0; startY(4:5)=0;
    segments={}; t=(cycle-1)*T; finish=cycle*T; nevents=0;
    while t<finish-1e-12
        active=opened; segmentStart=t;
        options=odeset('RelTol',opt.RelTol, ...
            'AbsTol',[1e-7,1e-7,1e-7,1e-8,1e-8], ...
            'MaxStep',T/opt.MaxStepDiv,'Events',@events);
        sol=ode15s(@rhs,[t,finish],y,options);
        segments{end+1}=sol; %#ok<AGROW>
        previous=t; t=sol.x(end); y=sol.y(:,end);
        if isfield(sol,'ie') && ~isempty(sol.ie)
            % Terminal events are at the endpoint; discard any earlier
            % non-terminal initial events recorded by MATLAB's ODE solver.
            hit=find(abs(sol.xe-t)<=1e-10*max(1,T));
            if ~isempty(hit)
                j=sol.ie(hit(end));
                if j>=3
                    if j==3, r.status='low_pressure_guard';
                    else, r.status='liquid_inventory_guard'; end
                    r.cycles=cycle;
                    return
                end
                opened(j)=~opened(j); y(j+1)=0; nevents=nevents+1;
                if nevents>30 || (t==previous && nevents>2)
                    error('pump:ValveChatter','Repeated valve events at one time.');
                end
            elseif t<finish-1e-12
                error('pump:IncompleteIntegration','Integration stopped without an endpoint event.');
            end
        elseif t<finish-1e-12
            error('pump:IncompleteIntegration','Integration stopped before the cycle ended.');
        end
    end
    scales=[100;max(c.swept_ml/T,1);max(c.swept_ml/T,1)];
    r.periodic_residual=max(abs(y(1:3)-startY(1:3))./scales);
    r.cycles=cycle;
    if cycle>=3 && r.periodic_residual<2e-7
        r.status='periodic'; break
    end
end
if ~strcmp(r.status,'periodic'), return; end
ts=linspace((cycle-1)*T,cycle*T,opt.NPoints);
ys=zeros(5,numel(ts));
for k=1:numel(ts)
    chosen=0;
    for j=1:numel(segments)
        ss=segments{j};
        if ts(k)>=ss.x(1)-1e-12 && ts(k)<=ss.x(end)+1e-12
            chosen=j; break
        end
    end
    assert(chosen>0,'No solution segment for requested sample.');
    ss=segments{chosen};
    ys(:,k)=deval(ss,min(max(ts(k),ss.x(1)),ss.x(end)));
end
[u,~,~]=pump_motion(ts,c);
vg=gasVolume(ys(1,:)); vl=c.residual_ml+c.swept_ml-u-vg;
F=ys(1,:)*133.322387415*pi*(c.diameter_mm*1e-3)^2/4;
residual=vl-vl(1)-(ys(4,:)-ys(5,:));
targetLiquid=c.residual_ml+c.swept_ml-gasVolume(c.pin_mmhg);
r.pc_peak_mmhg=max(ys(1,:)); r.pc_min_mmhg=min(ys(1,:));
r.force_peak_N=max(F); r.force_min_N=min(F); r.force_absmax_N=max(abs(F));
r.delivered_ml=ys(5,end); r.inlet_ml=ys(4,end);
r.Q_Lmin=c.f*r.delivered_ml/1000; r.eta=r.delivered_ml/c.swept_ml;
r.qout_peak_Lmin=max(ys(3,:))*.06; r.qin_peak_Lmin=max(ys(2,:))*.06;
r.fill_deficit_ml=max(0,targetLiquid-vl(end));
r.liquid_min_ml=min(vl); r.gas_max_ml=max(vg);
r.balance_error_ml=max(abs(residual));
r.net_cycle_error_ml=abs(r.inlet_ml-r.delivered_ml);
r.min_flow_ml_s=min(min(ys(2:3,:)));
trace=struct('time_s',ts-(cycle-1)*T,'phase',(ts-(cycle-1)*T)/T, ...
    'pc_gauge_mmhg',ys(1,:),'pressure_force_N',F, ...
    'qin_Lmin',ys(2,:)*.06,'qout_Lmin',ys(3,:)*.06, ...
    'piston_displacement_ml',u,'gas_ml',vg,'liquid_ml',vl);

    function vg=gasVolume(p)
        vg=c.gas_ref_ml*((c.atmosphere_mmhg+c.gas_ref_pressure_mmhg) ...
            ./(c.atmosphere_mmhg+p)).^(1/c.n);
    end
    function dy=rhs(tt,yy)
        p=yy(1); qi=yy(2); qo=yy(3);
        C=gasVolume(p)/(c.n*(c.atmosphere_mmhg+p));
        [~,vp,~]=pump_motion(tt,c);
        dqi=0; dqo=0;
        if active(1), dqi=(c.pin_mmhg-p-Bi*qi*abs(qi))/Ii; end
        if active(2), dqo=(p-c.pout_mmhg-Bo*qo*abs(qo))/Io; end
        dy=[(qi-qo+vp)/C;dqi;dqo;qi;qo];
    end
    function [v,terminal,direction]=events(tt,yy)
        v=zeros(4,1); direction=ones(4,1); terminal=ones(4,1);
        for jj=1:2
            if active(jj)
                v(jj)=yy(jj+1); direction(jj)=-1;
                % A newly opened valve starts with zero flow and positive
                % acceleration. Avoid treating that initial zero as closure.
                if tt==segmentStart && yy(jj+1)==0, v(jj)=1e-12; end
            elseif jj==1, v(jj)=c.pin_mmhg-yy(1)-openingTol;
            else, v(jj)=yy(1)-c.pout_mmhg-openingTol; end
        end
        v(3)=yy(1)+c.atmosphere_mmhg-c.pressure_floor_abs_mmhg;
        [uNow,~,~]=pump_motion(tt,c);
        v(4)=c.residual_ml+c.swept_ml-uNow-gasVolume(yy(1))-.1;
        direction(3:4)=-1;
    end
end

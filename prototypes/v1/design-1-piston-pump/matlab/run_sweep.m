function results=run_sweep()
%RUN_SWEEP Reproduce the 118 dynamic cases without overwriting the archive.
here=fileparts(mfilename('fullpath'));
out=fullfile(here,'..','results','matlab');
if ~exist(out,'dir'), mkdir(out); end
cases={}; groups={};
for gas=[1,10,20]
    for bore=[8,12,16,20]
        for f=[40,60,75,90,120,150,180]
            c=pump_parameters();c.gas_ref_ml=gas;c.f=f;
            c.valve_in_mm=bore;c.valve_out_mm=bore;
            append(c,'main');
        end
    end
end
for pressure=[120,200]
    for f=[75,180]
        for bore=[8,12,16,20]
            c=pump_parameters();c.pout_mmhg=pressure;c.f=f;
            c.valve_in_mm=bore;c.valve_out_mm=bore;
            append(c,'outlet_load');
        end
    end
end
settings=[75,16;180,16;180,8];
for exponent=[1,1.4]
    for j=1:3
        c=specialCase(j);c.n=exponent;append(c,'thermal');
    end
end
for coefficient=[.6,.8]
    for j=1:3
        c=specialCase(j);c.Cd=coefficient;append(c,'discharge_coefficient');
    end
end
for fraction=[.3,.5]
    for j=1:3
        c=specialCase(j);c.ejection_fraction=fraction;append(c,'timing');
    end
end
rows=cell(size(cases));
for j=1:numel(cases)
    r=pump_simulate(cases{j});r.group=groups{j};rows{j}=r;
    fprintf('%d/%d: %s\n',j,numel(cases),r.status);
end
results=struct2table([rows{:}]);
writetable(results,fullfile(out,'case_results.csv'));
full=cell(1,28);k=0;
for bore=[8,12,16,20]
    for f=[40,60,75,90,120,150,180]
        c=pump_parameters();c.f=f;c.valve_in_mm=bore;c.valve_out_mm=bore;
        r=pump_full_fill(c);r.f=f;r.valve_in_mm=bore;k=k+1;full{k}=r;
    end
end
writetable(struct2table([full{:}]),fullfile(out,'full_fill_reference.csv'));
softwareVersion=version; %#ok<NASGU>
save(fullfile(out,'run_record.mat'),'cases','groups','softwareVersion');

    function append(c,group)
        cases{end+1}=c; groups{end+1}=group;
    end
    function c=specialCase(j)
        c=pump_parameters();c.f=settings(j,1);
        c.valve_in_mm=settings(j,2);c.valve_out_mm=settings(j,2);
    end
end

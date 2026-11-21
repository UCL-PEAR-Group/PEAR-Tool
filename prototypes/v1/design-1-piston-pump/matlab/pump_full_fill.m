function r = pump_full_fill(c)
%PUMP_FULL_FILL Separate imposed-full-fill reference with no gas storage.
% Instantaneous valve switching is imposed here. Pressure-screen failure
% means the assumed filled trajectory is not a feasible liquid prediction.
T = 60/c.f;
t = (0:4000)*T/4001;
[~,q,dq] = pump_motion(t,c);
[Bi,Ii] = pump_coefficients(c,c.valve_in_mm);
[Bo,Io] = pump_coefficients(c,c.valve_out_mm);
advance = t < c.ejection_fraction*T;
p = c.pin_mmhg-Bi*q.^2+Ii*dq;
p(advance) = c.pout_mmhg+Bo*q(advance).^2+Io*dq(advance);
F = p*133.322387415*pi*(c.diameter_mm*1e-3)^2/4;
r = struct('pc_peak_mmhg',max(p),'pc_min_mmhg',min(p), ...
    'force_peak_N',max(F),'force_absmax_N',max(abs(F)), ...
    'Q_Lmin',c.f*c.swept_ml/1000,'eta',1, ...
    'pressure_screen_pass',min(p)+c.atmosphere_mmhg>=c.pressure_floor_abs_mmhg);
end

function [B,I] = pump_coefficients(c,valve_mm)
%PUMP_COEFFICIENTS Quadratic loss and inertance in mmHg, mL, seconds.
% B units: mmHg/(mL/s)^2. I units: mmHg/(mL/s^2).
At = pi*(c.tube_d_mm*1e-3)^2/4;
Av = pi*(valve_mm*1e-3)^2/4;
mmHgPa = 133.322387415;
B = c.rho/2*(1/(c.Cd*Av)^2+c.line_loss_K/At^2)*1e-12/mmHgPa;
I = c.rho*c.tube_l_m/At*1e-6/mmHgPa;
end

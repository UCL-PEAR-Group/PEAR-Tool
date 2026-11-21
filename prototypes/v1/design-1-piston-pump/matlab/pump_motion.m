function [u,q,dq] = pump_motion(t,c)
%PUMP_MOTION Smooth full-stroke volume trajectory; no mechanism is assumed.
% u: displacement volume [mL]; q: rate [mL/s]; dq: acceleration [mL/s^2].
T = 60/c.f;
phase = mod(t,T);
te = c.ejection_fraction*T;
advance = phase < te;
dt = te*advance + (T-te)*(~advance);
z = (phase./te).*advance + ((phase-te)./(T-te)).*(~advance);
h = 10*z.^3 - 15*z.^4 + 6*z.^5;
hp = 30*z.^2.*(1-z).^2;
hpp = 60*z.*(1-z).*(1-2*z);
sgn = 2*advance-1;
u = c.swept_ml*(h.*advance + (1-h).*(~advance));
q = c.swept_ml*sgn.*hp./dt;
dq = c.swept_ml*sgn.*hpp./dt.^2;
end

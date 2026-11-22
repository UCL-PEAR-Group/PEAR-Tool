# System variable register

This register covers the current one-chamber pump model, its performance targets, numerical settings and the identified near-term interfaces. It is not a claim that every future actuator, controller or Windkessel variable has already been defined.

**Physical role and Python data type are separate classifications.** A continuous physical quantity can be a prescribed input, a design parameter, a dynamic state or a calculated output. Almost all scalar physical quantities use `float`; their time histories use NumPy floating-point arrays (JSON archives serialise them as lists). Valve states use `bool`; sample/cycle counts use `int`; labels use `str`.

A free design parameter can be varied between candidate designs and still remain fixed throughout a test. A constitutive coefficient is not a control knob simply because the code lets us change it: it must represent a real component or material. Entries marked **not implemented** are a planning inventory, not additional equations already present.

The exploratory gas solver has **three independent continuous physical states**: chamber pressure, inlet flow and outlet flow. The two integrated-volume states are accounting accumulators. Gas volume, liquid inventory and force are dependent quantities. This state count is not a count of mechanical degrees of freedom. The separate full-liquid pressure-cycle study in section 18 has one dynamic load state, pw; prescribed flow drives it, and conditional chamber pressure is algebraic. These are distinct implementations, not a combined four-state solution.

The inlet and outlet of each chamber have their own entries; a future two-ventricle model should suffix them `_R` and `_L`. The current code simulates one chamber, not the four-valve whole-heart system. The operating matrix separately distinguishes per-circuit pulse rate h from physical chamber rate f: f=2h for the shared chamber (1A), and f=h per chamber for two dedicated chambers (1B). Architecture budget entries do not implement the coupled hydraulics.

## Dependencies to preserve

- Piston area A = πD²/4; swept volume Vs = A S. Choose two of D, S and Vs; calculate the third.
- Required net volume per circuit pulse = 1000 × circuit target flow [L/min] / per-circuit pulse rate h [min⁻¹]. This is distinct from geometric displacement.
- Period T = 60/f; advance time = γT; return time = (1−γ)T.
- Gas amount/reference condition is fixed for a closed pocket, while its instantaneous pressure, volume and compliance vary. Gas-law pressure is absolute.
- Actual mean flow, net-delivery ratio and maximum force are responses of the coupled system, not independent inputs to be freely prescribed together.
- The current atmospheric-rear force is chamber gauge pressure × face area. It is not generally outlet pressure minus inlet pressure multiplied by area.

The tables use the units actually present in the code. Internal flow is mL/s; exported trace flow is L/min. `VARIABLES.csv` is the machine-readable version with separate physical-nature and Python-type columns.


## 1. Requirements and operating inputs

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Qtarget / `Q_target_Lmin` | Desired mean circuit flow | Prescribed target | float | L/min | 5 nominal; 2–7 range; Requirement only | A target for comparison; not imposed as outlet flow by the current pressure-driven solution. |
| f / `f` | Physical chamber delivery-cycle frequency | Prescribed / operating input | float | cycles/min per chamber | 75 nominal; sweep 40–180; Implemented | Current one-chamber solver: one fill/eject cycle per event. Concept 1A requires f=2h; concept 1B requires f=h per chamber for per-circuit pulse rate h. |
| pout,target,mean / `p_out_mean_target` | Desired mean outlet pressure | Prescribed target | float | mmHg gauge | 90 nominal; 60–120 PDS; Requirement only | Requirement distinct from the constant outlet test boundary. |
| pout,target,peak / `p_out_peak_target` | Desired / permitted instantaneous outlet pressure | Prescribed target | float | mmHg gauge | PDS references 120 / 160; upper intended 200; Requirement only | Select the required test condition; these are not measured internal-pressure ratings. |
| T / `T` | Physical chamber cycle period | Derived timing | float | s | 0.8 at 75/min; Implemented | T=60/f. For equal R/L allocations 1A T=30/h; 1B T=60/h. Switching/dwell must fit the schedule. |
| γ / `ejection_fraction` | Fraction of cycle assigned to advance | Selectable timing input | float | 1 | 0.4; sensitivity 0.3 / 0.5; Implemented | Motion is prescribed, not yet closed-loop controlled. |
| te / `te` | Advance duration | Derived timing | float | s | 0.32 at baseline; Implemented | te = γT. |
| tf / `T-te` | Return duration | Derived timing | float | s | 0.48 at baseline; Implemented | tf = (1−γ)T; excludes a separate dwell stage. |
| t / `t / time_s` | Time / sampled cycle time | Independent coordinate | float / ndarray[float64] | s | 0 to T in a reported cycle; Implemented |  |
| φ / `phase` | Cycle fraction | Derived coordinate | float / ndarray[float64] | 1 | 0–1; Implemented | phase = cycle time/T. |

## 2. Geometry and displacement

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Dp / `diameter_mm` | Plunger-face diameter | Free design parameter | float | mm | 50 illustrative; Implemented | Chosen before manufacture; fixed during each simulation. |
| Ap / `π(Dp/1000)^2/4` | Plunger-face area | Derived geometry | float | m² | 0.0019635 at Dp = 50 mm; Derived expression | No wetted rod area deduction. |
| S / `stroke_mm` | Piston travel | Dependent geometry / alternative design input | float | mm | 33.95 at baseline; Derived, not a Case field | S = 4000 Vs/(π Dp²), for Vs in mL. Code currently selects Dp and Vs, then infers S. |
| Vs / `swept_ml` | Geometric swept volume | Free design parameter, fixed per run | float | mL | 5000/75 = 66.6667; Implemented | Vs = Ap S; Dp, S and Vs cannot all be varied independently. |
| Vmin / `residual_ml` | Minimum total chamber volume | Free design parameter | float | mL | 40 assumed; Implemented | Contains both residual liquid and retained gas; not the same as swept volume. |
| Vmax / `residual_ml+swept_ml` | Maximum total chamber volume | Derived geometry | float | mL | 106.6667; Derived expression | At full retraction. |
| Vch(t) / `residual_ml+swept_ml-u` | Instantaneous total chamber volume | Derived trajectory | ndarray[float64] | mL | Variable; Derived expression | Vch = Vmin + Vs − u. |
| x(t) / `u/Ap with unit conversion` | Piston position from full retraction | Prescribed trajectory, derived from volume | ndarray[float64] | mm | 0 to S; Derived expression | x_mm = 1000 u_mL / Ap_mm2. |
| dx/dt / `qp/Ap with unit conversion` | Piston velocity | Derived trajectory | ndarray[float64] | mm/s | Variable; Derived expression | Not currently a separately saved trace. |
| d²x/dt² / `dq/Ap with unit conversion` | Piston acceleration | Derived trajectory | ndarray[float64] | mm/s² | Variable; Derived expression | Used indirectly through prescribed volume dynamics; no solid inertia force yet. |
| u(t) / `u / piston_displacement_ml` | Displacement volume, positive on advance | Prescribed trajectory | ndarray[float64] | mL | 0 to Vs; Implemented | Quintic advance/return profile. |
| du/dt / `qp / vp / q from motion` | Piston displacement rate | Derived trajectory | float / ndarray[float64] | mL/s | Variable; Implemented | Not identical to outlet flow when gas storage is changing. |
| d²u/dt² / `dq from motion` | Displacement-volume acceleration | Derived trajectory | float / ndarray[float64] | mL/s² | Variable; Implemented | Used explicitly in the imposed-full-fill reference. |
| Lc / `cylinder_length_mm` | Total cylinder length | Future design parameter | float | mm | Unselected; Not implemented | Must accommodate travel, plunger, ports and clearance. |
| tp / `plunger_thickness_mm` | Plunger thickness | Future design parameter | float | mm | Unselected; Not implemented | Relevant to physical envelope, not current hydraulic balance. |
| cend / `end_clearance_mm` | End clearance / port allowance | Future design parameter | float | mm | Unselected; Not implemented | Cylinder length minus plunger thickness alone does not determine usable travel. |

## 3. Valves and connected hydraulic legs

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| di / `valve_in_mm` | Inlet clear bore | Free design parameter | float | mm | 16 baseline; 8 / 12 / 16 / 20 sweep; Implemented | Inlet and outlet bores can be set independently in Case. |
| do / `valve_out_mm` | Outlet clear bore | Free design parameter | float | mm | 16 baseline; 8 / 12 / 16 / 20 sweep; Implemented | Previous sweep varied both together, not independently. |
| Avi, Avo / `Av in coeff` | Valve flow areas | Derived geometry | float | m² | π dv²/4 after unit conversion; Derived expression | One area per leg. Equivalent bore is not necessarily nominal connector diameter. |
| Cd / `Cd` | Valve discharge coefficient | Constitutive / calibration parameter | float | 1 | 0.7; sensitivity 0.6 / 0.8; Implemented | One shared coefficient in current code; not yet measured. |
| dtube / `tube_d_mm` | Connected line bore | Free design / interface parameter | float | mm | 20 assumed; Implemented | Same value for both legs in current code. |
| At / `At in coeff` | Connected line area | Derived geometry | float | m² | π dtube²/4 after unit conversion; Derived expression | Derived expression |
| ℓ / `tube_l_m` | Effective liquid inertial length | Design / interface parameter | float | m | 0.2 assumed; Implemented | Same value for both legs; not piston travel or cylinder length. |
| K / `line_loss_K` | Lumped quadratic line-loss coefficient | Constitutive / calibration parameter | float | 1 | 1 assumed; Implemented | Not a derived Darcy friction factor and not a calibrated viscosity model. |
| Bi, Bo / `Bi / Bo` | Quadratic hydraulic resistance coefficients | Derived constitutive coefficients | float | mmHg/(mL/s)² internally | Calculated from density, Cd, areas and K; Derived expression | SI equivalent: Pa·s²/m⁶. |
| Ii, Io / `Ii / Io` | Hydraulic inertances | Derived constitutive coefficients | float | mmHg/(mL/s²) internally | Calculated from ρℓ/At; Derived expression | SI equivalent: Pa·s²/m³. |
| si, so / `opened / active` | Inlet/outlet open states | Discrete hybrid states | list[bool] | open/closed | Event-dependent; Implemented | Two booleans per model chamber. Current passive checks are not mechanically linked. |
| Δpcr,i, Δpcr,o / `valve_cracking_pressure` | Physical valve cracking pressures | Future constitutive parameters | float | mmHg | Assumed zero; Implicit zero; finite values not implemented | The 1e-6 mmHg numerical opening tolerance is not a physical cracking pressure. |
| τvalve / `valve_response_time_s` | Valve opening / closure response time | Future constitutive parameter | float | s | Not selected; Not implemented | Leaflet or actuator valve dynamics are currently omitted. |
| Qleak / `leakage_flow` | Leakage flow | Future constitutive response | float | mL/s | Assumed zero; Implicit zero; nonzero law not implemented | Would require a specified pressure-dependent leakage law. |

## 4. Fluid and retained gas

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| ρ / `rho` | Liquid density | Fluid property | float | kg/m³ | 1000 assumed; Implemented | Water-like value; not measured BMF properties. |
| μ / `dynamic_viscosity_Pas` | Liquid dynamic viscosity | Future fluid property | float | Pa·s | Unspecified; Not implemented | Requires viscosity-dependent losses; non-Newtonian BMF may require μ(shear rate, temperature). |
| Tfluid / `fluid_temperature_C` | Liquid temperature | Future condition / measured input | float | °C | Unspecified in this model; Not implemented | Thermal dependence of density and viscosity is not solved. |
| Kbulk / `liquid_bulk_modulus_Pa` | Liquid bulk modulus | Future constitutive parameter | float | Pa | Incompressible-liquid assumption; Implicit incompressible limit | Finite liquid compressibility is not included. |
| Vg0 / `gas_ref_ml` | Reference sealed gas volume | Reference condition / design parameter | float | mL | 10; sensitivity 1 / 20; Implemented | Volume at specified reference pressure, not a constant volume during motion. |
| pg0,gauge / `gas_ref_pressure_mmhg` | Reference gas pressure | Reference condition | float | mmHg gauge | 10 assumed; Implemented | Together with gas amount/volume defines reference state. |
| patm / `atmosphere_mmhg` | Atmospheric pressure | Environmental parameter | float | mmHg absolute | 760 assumed; Implemented | Needed to convert all gas pressures to absolute. |
| pg0,abs / `atmosphere_mmhg+gas_ref_pressure_mmhg` | Absolute reference gas pressure | Derived reference condition | float | mmHg absolute | 770 at baseline; Derived expression | Gas-law pressure must be absolute. |
| n / `n` | Polytropic exponent | Constitutive assumption | float | 1 | 1.2; sensitivity 1 / 1.4; Implemented | Assumed effective exponent; no gas heat-transfer equation. |
| Vg(t) / `vg / gas_ml` | Instantaneous gas volume | Dependent gas state | float / ndarray[float64] | mL | Calculated from pc; Implemented | Vg = Vg0 (pg0,abs/pc,abs)^(1/n). Not an additional independent ODE state. |
| Cg(t) / `C in rhs` | Instantaneous gas compliance | Derived constitutive quantity | float / ndarray[float64] | mL/mmHg internally | Vg/(n pc,abs); Implemented | SI equivalent: m³/Pa. |
| mg / `gas_mass_kg` | Retained gas mass | Future derived reference quantity | float | kg | Unspecified; Not independently used in current model | Closed-gas assumption fixes mass; calculating it needs reference temperature and gas properties. |
| Tg(t) / `gas_temperature_K` | Gas temperature | Future thermodynamic state | float | K | Not solved; Not implemented | A full energy/heat-transfer model would replace or justify the chosen exponent. |

## 5. Boundary pressures and evolving chamber states

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| pi / `pin_mmhg` | Upstream pressure at model leg entrance | Boundary condition | float | mmHg gauge | 10 constant; Implemented | Represents upstream reservoir/load. Time-dependent boundary not yet wired into Case. |
| po / `pout_mmhg` | Downstream pressure at model leg exit | Boundary condition | float | mmHg gauge | 90; sensitivities 120 / 200 constant; Implemented | Distinct from chamber pressure and from a specified pressure waveform. |
| pb / `rear_pressure_gauge` | Pressure on rear face of plunger | Boundary condition | float | mmHg gauge | 0 fixed; Implicit constant | Current force function assumes atmospheric rear; pb is not inlet pressure. |
| pc(t) / `y[0] / pc_gauge_mmhg` | Chamber pressure | Independent continuous ODE state | float / ndarray[float64] | mmHg gauge | Initial pc = pi; Implemented | Varies over the cycle. |
| pc,abs(t) / `atmosphere_mmhg+pc` | Absolute chamber pressure | Derived pressure | float / ndarray[float64] | mmHg absolute | Variable; Derived expression | Used for gas law and pressure guard. |
| Qi(t) / `y[1] / qin_Lmin` | Inlet flow | Independent continuous ODE state | float / ndarray[float64] | mL/s internally; L/min in trace | Initially zero; Implemented | Forward check-valve flow; multiplied by 0.06 for the saved trace. |
| Qo(t) / `y[2] / qout_Lmin` | Outlet flow | Independent continuous ODE state | float / ndarray[float64] | mL/s internally; L/min in trace | Initially zero; Implemented | Outlet flow differs from piston displacement rate during gas storage. |
| Vin,int(t) / `y[3]` | Integrated inlet volume | Integral accumulator state | float / ndarray[float64] | mL | Reset to zero each cycle; Implemented | Used for delivered-volume and conservation accounting. |
| Vout,int(t) / `y[4]` | Integrated outlet volume | Integral accumulator state | float / ndarray[float64] | mL | Reset to zero each cycle; Implemented | Not an extra mechanical degree of freedom. |
| Vl(t) / `vl / liquid_ml` | Liquid inventory inside chamber | Dependent volume state | ndarray[float64] | mL | Vmin + Vs − u − Vg; Implemented | Derived rather than independently integrated. |
| Δpi(t), Δpo(t) / `pin-pc / pc-pout` | Forward pressure differences across each leg | Derived hydraulic quantities | float / ndarray[float64] | mmHg | Variable; Derived expression | Each includes the modelled valve and line segment, not necessarily only the physical valve. |

## 6. Calculated outputs and performance

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Fp(t) / `pressure_force_N` | Signed hydraulic balancing force | Calculated response | ndarray[float64] | N | Calculated per case; Implemented | Ap(pc−pb); excludes seals and solid inertia. |
| Fp,max / `force_absmax_N` | Largest absolute hydraulic force in final cycle | Calculated response | float | N | Calculated per case; Implemented | Maximum over sampled final periodic cycle; not a component rating. |
| Fpush / `force_peak_N` | Largest positive signed pressure force | Calculated response | float | N | Calculated per case; Implemented | May be interpreted as peak advancing-axis balancing demand. |
| Fmin / `force_min_N` | Most negative signed pressure force | Calculated response | float | N | Calculated per case; Implemented | Signed value; retraction-demand magnitude is max(0,−Fmin). |
| pc,max / `pc_peak_mmhg` | Maximum chamber pressure | Calculated response | float | mmHg gauge | Calculated per case; Implemented | Not maximum outlet-boundary pressure. |
| pc,min / `pc_min_mmhg` | Minimum chamber pressure | Calculated response | float | mmHg gauge | Calculated per case; Implemented | Add atmospheric pressure for absolute value. |
| Vnet / `delivered_ml` | Outlet volume delivered in the final cycle | Calculated response | float | mL/beat | Calculated per case; Implemented | Integral of Qo; distinct from geometric swept volume. |
| Vin,cycle / `inlet_ml` | Inlet volume entering in the final cycle | Calculated response | float | mL/beat | Calculated per case; Implemented | Should equal outlet cycle volume at periodic operation. |
| Qmean / `Q_Lmin` | Mean delivered outlet flow | Calculated response | float | L/min | Calculated per case; Implemented | f × Vnet / 1000. |
| rV / `eta` | Net-delivery / swept-volume ratio | Calculated response | float | 1 | Calculated per case; Implemented | A calculated ratio, not a free control input; can exceed 1 in this ideal inertial valve model. |
| Qi,max / `qin_peak_Lmin` | Peak instantaneous inlet flow | Calculated response | float | L/min | Calculated per case; Implemented | Not the cycle mean. |
| Qo,max / `qout_peak_Lmin` | Peak instantaneous outlet flow | Calculated response | float | L/min | Calculated per case; Implemented | Not the cycle mean. |
| ΔVfill / `fill_deficit_ml` | Liquid deficit at full retraction | Calculated response | float | mL | Calculated per case; Implemented | Relative to inventory at reference inlet pressure; distinct from net-delivery shortfall. |
| Vl,min / `liquid_min_ml` | Minimum liquid inventory | Calculated response | float | mL | Calculated per case; Implemented | Must remain above the model inventory guard. |
| Vg,max / `gas_max_ml` | Maximum gas volume | Calculated response | float | mL | Calculated per case; Implemented | Dynamic value, not reference gas volume. |
| Vnet,required / `1000*Qtarget/f` | Required net delivery for target flow and frequency | Derived requirement | float | mL/beat | 66.67 nominal; 27.78 at 180/min for 5 L/min; Derived requirement | This is a requirement, not a guarantee that the selected geometry can supply it. |
| Qgeom / `f*swept_ml/1000` | Ideal geometric displacement flow | Derived ideal reference | float | L/min | 5 at 75/min; 12 at 180/min; Derived reference | Assumes one complete ideal liquid delivery per cycle. |
| Ftotal / `total_actuator_force_N` | Total actuator force | Future calculated response | float | N | Not calculated; Out of current scope | Would add seal friction and moving-solid inertia with consistent signs; mechanism loads remain deferred. |
| Fseal, meff / `seal_force_N / moving_mass_kg` | Seal friction and moving mass | Future constitutive / mechanical parameters | float | N; kg | Not specified; Out of current scope | Not included in current peak hydraulic force. |

## 7. Circuit interfaces, control and measurements

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Rwk / `windkessel_resistance` | Equivalent circuit resistance(s) | External subsystem parameter | float / ndarray[float64] | Pa·s/m³ or mmHg·min/L | See section 18 and pressure_cycle_inputs.json; Separate full-liquid load study implemented; gas-solver coupling pending | Not the valve coefficient B. A selected Windkessel may have several resistances. The earlier gas solver still uses constant pressure boundaries. |
| Cwk / `windkessel_compliance` | Equivalent circuit compliance(s) | External subsystem parameter | float / ndarray[float64] | m³/Pa or mL/mmHg | See section 18 and pressure_cycle_inputs.json; Separate full-liquid load study implemented; gas-solver coupling pending | Distinct from chamber gas compliance Cg. The earlier gas solver still uses constant pressure boundaries. |
| Vres, hres / `reservoir_volume / reservoir_head` | Atrial / lung reservoir inventories and heads | External subsystem state | float / ndarray[float64] | mL; m | Not specified; Not implemented | Constant-boundary tests do not model depletion or recirculation delay. |
| pcirc(t) / `circuit_pressure_history` | Supplied upstream/downstream pressure histories | External boundary signals | float / ndarray[float64] | mmHg gauge | See section 18 and pressure_cycle_inputs.json; Separate full-liquid load study implemented; gas-solver coupling pending | Future coupled Windkessel interface; use one per ventricular loop. The earlier gas solver still uses constant pressure boundaries. |
| β(t) / `bypass_command` | Commanded diversion fraction / valve setting | Candidate manipulated variable | float / ndarray[float64] | 1 | Not specified; Not implemented | Not selected or implemented; an actuator setting need not equal actual diverted fraction. |
| Qbypass(t) / `bypass_flow` | Actual diverted flow | Future hydraulic state / response | float / ndarray[float64] | mL/s | Not specified; Not implemented | Requires bypass geometry, valve law and reservoir boundary. |
| topen, tclose / `active_valve_timing` | Actively commanded valve times | Candidate manipulated inputs | float / ndarray[float64] | s or cycle fraction | Not specified; Not implemented | Current valves are passive pressure-driven events. |
| pm,i, pm,o / `measured_pressure` | Measured pressures at specified sensor taps | Measured signals | float / ndarray[float64] | mmHg gauge | Not specified; Not implemented | A valve pressure drop needs taps on both sides; current model leg also includes a line segment. |
| Qm,i, Qm,o / `measured_flow` | Measured inlet and outlet flow signals | Measured signals | float / ndarray[float64] | L/min | Not specified; Not implemented | Mean flow control needs cycle averaging and specified measurement location. |
| fs, Δts / `sample_rate_Hz / sample_interval_s` | DAQ sampling rate and interval | Instrumentation settings | float / ndarray[float64] | Hz; s | Not specified; Not implemented | Separate from ODE solver time step and plotted sample count. |
| up, uQ, ux / `pressure_uncertainty / flow_uncertainty / position_uncertainty` | Measurement uncertainties | Instrumentation / calibration parameters | float / ndarray[float64] | mmHg; L/min; mm | Not specified; Not implemented | Define standard or expanded uncertainty and propagation method when sensors are selected. |
| eQ / `flow_control_error` | Mean-flow target minus measured mean flow | Future controller variable | float / ndarray[float64] | L/min | Not specified; Not implemented | No controller currently implemented. |
| Kp, Ki, Kd / `controller_gains` | Feedback control gains | Future tuning parameters | float / ndarray[float64] | Depend on the chosen input/output and controller form | Not specified; Not implemented | A gain cannot be assigned units or a value before the control architecture is selected. |

## 8. Numerical controls and diagnostics

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| rtol / `rtol` | ODE relative tolerance | Numerical setting / diagnostic | float | 1 | 2e-7; Implemented | Refinement used 2e-9. |
| atol / `atol` | ODE absolute tolerances | Numerical setting / diagnostic | list[float] | Mixed state units | [1e-7,1e-7,1e-7,1e-8,1e-8]; Implemented | Order: pc, Qi, Qo, integrated inlet and outlet volume. |
| Nstep / `max_step_div` | Maximum-step denominator | Numerical setting / diagnostic | int | 1 | 120; Implemented | Maximum step = T/Nstep; refinement 360. |
| Ncycles / `max_cycles` | Maximum cycles attempted | Numerical setting / diagnostic | int | cycles | 24; Implemented | At least three cycles before periodicity is accepted. |
| Nsamples / `npoints` | Final-cycle sample count | Numerical setting / diagnostic | int | samples | 2401; Implemented | Refinement 7201; separate from adaptive integration steps. |
| Nfull / `npts` | Gas-free reference sample count | Numerical setting / diagnostic | int | samples | 4001; Implemented | Used by full_fill. |
| εperiodic / `periodic threshold` | Scaled periodic endpoint tolerance | Numerical setting / diagnostic | float | 1 | 2e-7; Implemented | Fixed implementation threshold; state scaling described in source. |
| εopen / `opening_tol` | Numerical valve opening offset | Numerical setting / diagnostic | float | mmHg | 1e-6; Implemented | Avoids zero-time event chatter; not physical valve cracking pressure. |
| pguard / `pressure_floor_abs_mmhg` | Minimum absolute pressure guard | Numerical setting / diagnostic | float | mmHg absolute | 50; Implemented | Exploratory validity floor, not measured cavitation threshold. |
| Vguard / `liquid inventory floor` | Minimum retained liquid inventory guard | Numerical setting / diagnostic | float | mL | 0.1; Implemented | Fixed implementation threshold. |
| Nevents / `event chatter limit` | Maximum events in one cycle | Numerical setting / diagnostic | int | events | 30; Implemented | Implementation guard. |
| record_trace / `keep_trace` | Whether full-cycle arrays are returned | Numerical setting / diagnostic | bool | true/false | False by default; Implemented | Baseline/notebook requests True. |
| status / `status` | Run outcome | Numerical setting / diagnostic | str | category | periodic / not_periodic / low_pressure_guard / liquid_inventory_guard; Implemented | Solver errors raise exceptions. |
| Nused / `cycles` | Cycles actually simulated | Numerical setting / diagnostic | int | cycles | Calculated; Implemented | Run diagnostic. |
| εend / `periodic_residual` | Scaled endpoint state change | Numerical setting / diagnostic | float | 1 | Calculated; Implemented | Numerical periodicity measure. |
| εV / `balance_error_ml` | Maximum chamber-volume balance residual | Numerical setting / diagnostic | float | mL | Calculated; Implemented | Conservation check, not measurement uncertainty. |
| εcycle / `net_cycle_error_ml` | Absolute inlet/outlet cycle-volume difference | Numerical setting / diagnostic | float | mL | Calculated; Implemented | Conservation at periodic operation. |
| Qmin,num / `min_flow_ml_s` | Smallest sampled valve flow | Numerical setting / diagnostic | float | mL/s | Calculated; Implemented | Checks numerical violation of forward-only valves. |
| valid_ref / `pressure_screen_pass` | Pressure screen for imposed-full-fill reference | Numerical setting / diagnostic | bool | true/false | Calculated; Implemented | A pass does not guarantee no local cavitation. |
| case_group / `group` | Parameter sweep category | Numerical setting / diagnostic | str | category | main / outlet_load / thermal / discharge_coefficient / timing; Implemented | Metadata, not a physical variable. |
| y / `y` | ODE state vector | Numerical setting / diagnostic | ndarray[float64], shape (5,) | Mixed state units | [pc, Qi, Qo, Vin,int, Vout,int]; Implemented | Three independent physical ODE states plus two integral accumulators. |
| solver / `method` | ODE integration method | Numerical setting / diagnostic | str | category | Radau; Implemented | Numerical choice, not a model property. |
| mmHg→Pa / `MMHG` | Pressure-unit conversion factor | Numerical setting / diagnostic | float | Pa/mmHg | 133.322387415; Implemented | Fixed conversion constant. |

## 9. Architecture budgets and planned routing

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| concept / `concept` | Piston architecture label | Design option | str | category | 1A / 1B; Matrix only | 1A shared chamber with alternating R/L duty; 1B two dedicated chambers. Not a hydraulic solver switch. |
| h / `h_per_limb_per_min` | Pulse rate at each circuit arterial outlet | Prescribed target | float | pulses/min | 75 nominal; 40–180 PDS; Matrix only | Distinct from physical chamber f. Matrix assumes one delivery per circuit per heart period. |
| Nch / `physical_chamber_count` | Number of physical pump chambers | Architecture property | int | chambers | 1 for 1A; 2 for 1B; Matrix only | Not number of mechanical degrees of freedom. |
| fch / `delivery_cycles_per_physical_chamber_per_min` | Required delivery-cycle frequency per physical chamber | Derived timing | float | cycles/min | 2h for 1A; h for 1B; Matrix only | 360/min for 1A at 180 bpm per circuit; no hydraulic simulation at that rate yet. |
| Qpasses / `target_liquid_passes_per_chamber_Lmin` | Target net liquid passes through each physical chamber | Derived volume budget | float | L/min | 2Q for 1A; Q for 1B; Matrix only | Excludes bypass. Does not double the reported circulation flow. |
| sroute / `routing_state` | Shared-chamber connection state | Future discrete state | str / Enum | category | R-fill / R-eject / L-fill / L-eject / transition to define; Not implemented | Physical port map and transition isolation remain unselected; preserve gas and residual liquid state across switches. |
| tswitch / `switching_time_s` | Time reserved for valve routing transitions | Future timing input | float | s | Not selected; Not implemented | Must fit within the heart period; current prescribed motion reserves no separate switching dwell. |
| deltaRL / `ventricular_phase_offset` | Right/left chamber motion offset | Selectable timing input | float | fraction of heart period | Not selected; Not implemented | Concurrent or offset motion possible in 1B; valve openings still depend on pressure loads. |
| pPAmean / `pulmonary_mean_pressure_target` | Mean pulmonary arterial load | Prescribed target | float | mmHg gauge | 15 / 25 / 35; Requirement only | Current PDS p.1; pulmonary peak and right-atrial inlet boundary remain open. |
| Qphantom / `phantom_inlet_flow_target` | Flow target at the declared phantom anatomical plane | Prescribed signal | float / ndarray[float64] | L/min | Trace and branch split not selected; Not implemented | Do not automatically equate local abdominal flow to total pump output. |

## 17. Waveform kinematics

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| shape / `waveform_shape` | Candidate ejection and filling shape pair | Selectable command parameter | str | category | published_harmonics / half_sine; Kinematic comparison only | Not a switch in the hydraulic solver. |
| epsilon / `epsilon` | Transition width at each endpoint as a fraction of phase duration | Free smoothing parameter | float | 1 | 0.05 trial; 0 restores raw; Kinematic comparison only | No optimum selected; smoothing can increase peak acceleration. |
| u / `u` | Normalised phase time | Independent coordinate | float / ndarray[float64] | 1 | 0 to 1; Implemented in waveform study | Each phase is normalised separately. |
| Ge / Gf / `shape_integral` | Integral of the windowed phase shape | Derived normalisation | float | 1 | Calculated per phase; Implemented in waveform study | Quadrature; sets unit-area shape. |
| Qp / `signed_piston_flow` | Signed geometric piston displacement flow | Prescribed command history | ndarray[float64] | mL/s | Positive ejection; negative filling; Implemented in waveform study | Equals signed liquid flow only under full-liquid no-storage assumptions. |
| amax / `max_abs_acceleration_m_s2` | Maximum absolute commanded piston acceleration | Derived output | float | m/s² | 5.026 harmonic trial at D=50 mm; Kinematic comparison only | Fine-grid maximum; does not include solid mass or hydraulic pressure. |

## 18. Periodic load and heart comparison

| Symbol / code | Meaning | Physical role | Python type | Units | Current value / status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| side / `side` | Systemic or pulmonary load selection | Selectable scenario | str | 1 | systemic / pulmonary; Implemented in separate pressure-cycle study | Separate trial cases, not a solved two-loop circulation. |
| R1 / `R1_mmhg_s_ml` | Proximal load resistance | External subsystem parameter | float | mmHg s/mL | 0.040 systemic; 0.015 pulmonary; Implemented in separate pressure-cycle study | Reference-informed illustrative values; uncalibrated. |
| R2 / `R2_mmhg_s_ml` | Distal load resistance | External subsystem parameter | float | mmHg s/mL | 0.980 systemic; 0.045 pulmonary; Implemented in separate pressure-cycle study | Chosen for 90 / 15 mmHg mean at 5 L/min; not independent corroboration. |
| Cw / `C_ml_mmhg` | Arterial-load compliance | External subsystem parameter | float | mL/mmHg | 1.5 systemic; 5.0 pulmonary; Implemented in separate pressure-cycle study | Free trial values; distinct from chamber gas compliance. |
| pr / `return_pressure_mmhg` | Pressure beyond distal load resistance | Boundary input | float | mmHg gauge | 5 systemic; 10 pulmonary; Implemented in separate pressure-cycle study | Constant boundary; distinct from inlet and rear-face pressure. |
| pi / `inlet_pressure_mmhg` | Atrial reservoir pressure | Boundary input | float | mmHg gauge | 10 systemic; 5 pulmonary; Implemented in separate pressure-cycle study | Constant reservoir; no depletion or return-delay model. |
| pw(t) / `compliance_pressure_mmhg` | Pressure at load compliance node | Dynamic load state | ndarray[float64] | mmHg gauge | Periodic history; Implemented in separate pressure-cycle study | One continuous state in this separate prescribed-flow study. |
| pa(t) / `arterial_pressure_mmhg` | Pressure at arterial load inlet | Calculated output | ndarray[float64] | mmHg gauge | pw + R1 Qo; Implemented in separate pressure-cycle study | Compare with arterial reference; not ventricular pressure. |
| pc(t) / `chamber_pressure_mmhg` | Conditional chamber phase pressure | Calculated phase output | ndarray[float64] | mmHg gauge | Derived during each imposed phase; Implemented in separate pressure-cycle study | Pressure transitions unresolved; passive valve assumptions must be checked. |
| Fh,phase / `phase_max_abs_hydraulic_force_n` | Largest absolute phase hydraulic force | Calculated phase diagnostic | float | N | 32.6 systemic; 15.5 pulmonary; Implemented in separate pressure-cycle study | 50 mm illustrative bore; not complete-cycle rating; pulmonary valve schedule inconsistent. |
| vclosed / `closed_valve_violation_mmhg` | Wrong-way pressure across an assumed-closed branch | Feasibility diagnostic | ndarray[float64] | mmHg | 0 systemic; peak 19.2 pulmonary; Implemented in separate pressure-cycle study | Positive means assumed-closed zero-cracking passive valve would open. |
| Δpjoin / `ejection_to_filling_pressure_jump_mmhg / cycle_wrap_pressure_jump_mmhg` | Unresolved one-sided pressure joins | Model limitation diagnostic | float | mmHg | −88.9 / +62.7 systemic; Implemented in separate pressure-cycle study | A smooth piston acceleration does not resolve chamber pressure switching. |
| S_k, φ_k / `heart_reference_harmonics.csv` | Published Fourier amplitudes and phases | Reference data | ndarray[float64] | mL/s or mmHg; radians | 10 harmonics plus mean; Implemented in separate pressure-cycle study | Qureshi 2018 Appendix A Table A1 from Milnor 1989; 75/min and 6.6 L/min; unscaled. |

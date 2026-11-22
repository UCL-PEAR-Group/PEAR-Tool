# Piston pump model checkpoint

22 November 2026. Consolidated assessment of the model and its implementation,
including the user's correction that the rear piston face need not be atmospheric.

**[Read the checkpoint PDF](reports/checkpoint/Pump_Model_Checkpoint.pdf)** ·
[Editable LaTeX source](reports/checkpoint/Pump_Model_Checkpoint.tex)

## Goal and current position

Determine how piston geometry, waveform, valve coordination, retained air and
external circuit loads produce net flow, pressure and hydraulic piston load.
Use the results to compare the shared- and dual-chamber concepts, then build the
interactive MATLAB model after the necessary derivation and numerical checks.

We have analytical blocks and separate executed reference calculations. We do
not yet have one verified simulation of the current enforced-valve design,
right/left routing and potentially sealed rear chamber. Old passive-valve,
atmospheric-rear results remain reference cases, not current-design ratings.

## Confirmed decisions and remaining assumptions

| Topic | Current position |
| --- | --- |
| Baseline target | 5 L/min and 75 pulses/min per arterial outlet; 66.667 mL net delivery required per pulse |
| Concepts | Keep 1A shared sequential duties and 1B two dedicated chambers |
| Piston | Flat wetted face; no wetted-rod deduction; diameter/travel remain design variables |
| Duty timing | Adjustable shared right fraction lambda_R, default 0.5; within-duty advance/return allocation is separate |
| Valves | Enforced states coordinated with piston phase; pressure may participate; transitions idealised for now |
| Front air | Deliberately retained sealed pocket; real reference state and thermal exponent unselected |
| Rear boundary | Atmospheric, sealed-gas or other controlled/vented condition must be explicit; not yet selected |
| Losses and circuit | Valve/line coefficients and reservoir/Windkessel data remain declared inputs, not measured rig properties |
| Software | Executed Python references; MATLAB remains the intended live-model platform, with current numerical execution unverified |

## Rear-pressure correction

Let A_p be the wetted piston area and A_b the effective dry-side pressure area.
With a common gauge reference and an exposed external rod end at that ambient
pressure, hydraulic balancing force is

$$
F_h=A_p p_c-A_b p_b.
$$

Only when A_b = A_p does this reduce to A_p(p_c-p_b). A dry-side rod may make A_b
annular even though the wetted face has no rod. Other pressure exposures need
the actual geometry's force balance.

For a candidate sealed rear gas volume that increases during piston advance,

$$
V_b(x)=V_{b,r}+A_b(x-x_r),\qquad
P_b(x)=P_{b,r}\left[\frac{V_{b,r}}{V_b(x)}\right]^{n_b},\qquad
p_b=P_b-p_{\mathrm{atm}}.
$$

P_b and P_b,r are absolute gas pressures. V_b,r is a separate rear reference
volume, not the front retained-air amount. This assumes fixed gas mass, constant
polytropic exponent n_b and positive volume. It is an analytical candidate,
not a selected boundary or implemented solver feature.

## Next steps and completion gates

| Order | Work | Completion criterion |
| --- | --- | --- |
| 1 | Define one-chamber front/rear and circuit boundaries | Every boundary, effective area and gas reference state is explicit; unknowns have declared trial ranges |
| 2 | Close the ideal-valve equations | A consistent switching/inertance treatment is declared; no unexplained flow reset or fictitious finite surge peak |
| 3 | Solve and verify one chamber with its load | Reproducible motion, flow, pressures, inventory and force; units/conservation/limits/periodicity/time-resolution checks |
| 4 | Add architecture coupling | Shared duty/routing carry-over or dual-chamber linkage; reservoir balances and unequal timing are explicit |
| 5 | Compare feasible geometry and operating cases | Achieved flow, waveform, filling and load trends support a design matrix; no hidden geometry resizing in rate sweeps |
| 6 | Build MATLAB interface | Visualisation reads the same verified model and clearly labels inputs, assumptions and case status |
| 7 | Calibrate and independently validate | Selected hardware and measured uncertainty; revisit finite valve transitions and peak loads where relevant |

The immediate next deliverable is a reviewable closed equation set and a verified
single-chamber/load case. Converter/motor design, FEA, detailed closure dynamics
and hardware control remain deferred. The final hydraulic load must include rear
pressure; bulk load estimates must remain distinct from unresolved switching
surges and from total mechanical drive force.

## Evidence inspected for this checkpoint

- `python/verification_status.json`: stored regression and notebook checks;
  physical validation false.
- `research/pressure_cycle/pressure_cycle_verification.json`: separate prescribed
  flow study; full-cycle force unresolved.
- `spreadsheet/spreadsheet_verification.json`: formula checks; native Excel test
  false; no physical validation.
- `matlab/verification_status.json`: static parser passed; MATLAB runtime execution
  false.
- Current source, derivations, operating matrix and variable register.

No new hydraulic simulation or MATLAB execution was performed for this checkpoint.
The full PDF gives numerical examples with their limitations, external references,
source paths and the scope of the rear-pressure algebra checks.

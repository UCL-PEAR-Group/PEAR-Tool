# Interactive piston model: development target

Recorded 22 November 2026. Goal and proposed implementation plan; no new MATLAB
simulation or application has been executed in this update.

## User's intended outcome

An interactive model of the plunger pump, showing synchronised piston motion,
pressure and flow waveforms at different heart rates. MATLAB is now the preferred
likely platform because the user reports installing it locally on Ubuntu.
The installed release, available toolboxes and local execution are not verified.
The model is still being derived collaboratively; recording this destination does
not select a complete design or authorise assumptions to be hidden inside a UI.

The existing Python calculations, spreadsheet, source data and numerical checks
remain the reproducible reference during development. The older MATLAB port is
unexecuted and does not include all subsequent waveform and load work. It must
be reviewed and checked before it is promoted to a maintained entry point.

## Priority confirmed — 22 November 2026

The user explicitly places the application after completion of the derivation.
The current task is retained-air chamber compliance and enforced valve
opening/closure. [Derivation 04](research/DERIVATION_04_RETAINED_AIR_AND_VALVE_EVENTS.md)
provides the storage balance; [valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md)
supersedes its passive switching assumption. The command/transition law remains
to be derived and the combined model has not been implemented or verified.
Application work must not displace that task.

## What the first interactive version should show

| Element | Inputs or displayed outputs | Interpretation |
| --- | --- | --- |
| Piston view | Position, selected bore/travel, chamber and retained-gas volumes | Schematic driven by the same numerical solution as the plots; no converter design required |
| Timing controls | Per-circuit bpm, ejection/filling allocation, waveform and smoothing | Explicit timing assumptions; distinguish motion allocation from actual valve-open durations |
| Pressure plots | Chamber, inlet reservoir and arterial/load-inlet pressure | Label measurement locations and gauge/absolute reference; compare with corresponding physiology |
| Flow plots | Inlet and outlet instantaneous flow, cycle mean and net delivery | Actual outputs of continuity and valve dynamics in the coupled model |
| Valve indication | Commands, effective opening and routing state; opening/closing times | Enforced sequence and modelled physical response; calculate actual flow from the hydraulics |
| Load summary | Hydraulic force history and peak positive/negative load | Seals, moving-solid inertia and converter distribution remain outside current scope |
| Reference overlay | Published aortic/pulmonary signals, source conditions, optional normalised phase | Preserve reference flow/rate and label any transformation; no automatic claim of validation |
| Case record | Inputs, assumptions, units, initial state, solver settings and outputs | Save reproducible cases; distinguish transient from periodic results |

A single dedicated chamber is the first implementation unit. It can later be
reused for 1B's two dedicated chambers, or placed in 1A's explicit alternating
routing schedule. Neither architecture is selected by this software plan.

## The bpm control must preserve the selected physical assumptions

For one dedicated chamber, mean flow in L/min equals physical delivery frequency
in cycles/min multiplied by net delivery in mL/cycle, divided by 1000.
Net delivery must be integrated from outlet flow in the coupled model.

| Mode | Held fixed | What is solved or changed |
| --- | --- | --- |
| Fixed pump: default rate study | Piston diameter and travel, gas amount, valve/path geometry and load coefficients | Change bpm and calculate flow, pressure, valve events, filling and force |
| Geometry-sizing study | Desired mean flow, bpm and selected diameter | Calculate ideal required travel; clearly label that geometry changes between cases |
| Controlled mean-flow study: future | A declared flow target and bpm | Requires an explicit mechanism such as variable travel or modelled bypass/spill; controller capability is not assumed |

At the ideal 66.667 mL stroke, 75/min gives 5 L/min and 180/min gives 12 L/min.
Retained gas, valve behaviour and restricted filling can change actual net
volume. These ideal figures do not establish that a real rig can reach 12 L/min.

The current spreadsheet derives swept volume from target flow divided by bpm.
Its rate changes therefore represent sizing at fixed target flow, not a fixed
manufactured cylinder. The future app must not silently use that normalisation
in the fixed-pump mode. Changing bore, travel or gas charge creates a new design
case; it does not imply those properties can change physically during a run.

For 1A, distinguish per-circuit pulse rate h from physical chamber rate f. Under
the current one-delivery-per-duty interpretation, f = 2h; for 1B each chamber has
f = h. Timing/routing and carry-over states must be implemented before either
whole architecture is represented as solved.

## Proposed software structure

1. **Numerical model in MATLAB functions.** Keep inputs, waveform generation,
   constitutive laws, valve events, integration and output calculations separate
   from graphics. Retained-gas chamber storage and the arterial load must be
   solved together before claiming a complete chamber pressure/force cycle.
   A stiff solver such as ode15s is a candidate, with event handling and
   convergence checks; it is not a selected/tested solver for this project yet.
   The zero-storage full-liquid limit needs its own algebraic/event treatment,
   rather than dividing by zero chamber compliance.
2. **Interactive display in App Designer.** Read numerical outputs to animate
   the piston, indicate valve states and update linked pressure/flow plots.
   Screen refresh and animation playback speed are separate from integration
   time steps and physical bpm. Base MATLAB functions and App Designer are the
   initial target; Simulink can be assessed later for block-based control work.
3. **Optional later rig connection.** Compare time-stamped sensor readings with
   model outputs once sensors and communication are defined. Animated desktop
   simulation is not evidence of deterministic real-time control or a validated
   digital twin. A hardware connection is outside this first application scope.

For the first interface, changing a parameter starts a clearly labelled new
case, computes its response and displays convergence towards a periodic cycle.
A steady-state replay must be labelled as replay. A later continuously changing
bpm experiment must retain chamber/load states and phase, with a defined rate
ramp; simply resetting the phase or jumping the motion derivative can create
artificial pressure/force spikes. Restart and continuous-transient modes should
therefore remain distinct.

## Work in reviewable increments

1. Resolve chamber storage and commanded valve/routing transitions while
   retaining the current periodic-load assumptions. Reassess negative filling
   pressures; Derivation 03's closed-valve conflicts apply to passive checks and
   are not automatically inconsistencies for enforced closure.
2. Implement a MATLAB numerical baseline and compare like-for-like cases with
   the executed Python reference. Confirm units, event timing, cycle volumes,
   periodicity, energy balance where applicable and tolerance/time-step sensitivity.
   Numerical agreement is verification, not physical validation.
3. Add the one-chamber animation and linked plots. Begin at the 75 bpm nominal
   setting, then compare selected rates such as 40, 120 and 180 bpm with fixed
   geometry. Calculate rather than prescribe the delivered mean flow.
4. Add selectable waveforms and timing, saved-case comparison and physiology
   metrics at matched measurement locations/conditions.
5. Extend the explicit topology for the two chamber concepts. Add measurement
   comparison, calibration and independent validation when physical data exist.

No full-cycle force rating, simulation speed, supported MATLAB release or
physical waveform accuracy is promised by this roadmap. Those are measurable
outcomes of the next implementation and tests.

## Software references checked for this plan

- MathWorks, [App Designer](https://www.mathworks.com/help/matlab/ref/appdesigner.html):
  interactive UI authoring. Supports the proposed application layer; no specific
  installed release was inferred from the documentation's current version.
- MathWorks, [ode15s](https://www.mathworks.com/help/matlab/ref/ode15s.html):
  stiff ODE/DAE solver and event outputs. Supports the proposed solver candidate,
  not a conclusion that this pump formulation has been verified in MATLAB.
- MathWorks, [timer](https://www.mathworks.com/help/matlab/ref/timer.html):
  scheduled callbacks are affected by other work and are not a deterministic
  real-time control guarantee. A display timer must not dictate hydraulic steps.
- MathWorks, [App Designer timer example](https://www.mathworks.com/help/matlab/creating_guis/memory-monitor-gui-in-app-designer.html):
  periodic plot updates with start/stop/cleanup. This is a UI example, not a
  cardiovascular model or hardware-control validation.

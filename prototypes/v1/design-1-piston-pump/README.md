# Design 1: Piston Pump

**[Editable four-concept comparison](../concept-comparison/Pump_Concept_Comparison.xlsx)**: blank score and evidence fields for piston, diaphragm, impeller and peristaltic concepts, with the supplied criteria and automatic weighted totals/ranking.

**[Weighted concept assessment](WEIGHTED_DESIGN_MATRIX.md)** ([CSV](WEIGHTED_DESIGN_MATRIX.csv)): user-supplied C1–C10 weights, applied provisionally on 23 November 2026. Single chamber 2.84/5; dual chambers 3.45/5. Holding scores cover unresolved evidence; neither concept is declared PDS-compliant.

**[Team report: sketches, derivations and roadmap](reports/team_review/Piston_Pump_Team_Report.pdf)** ([source and assets](reports/team_review/README.md)). Consolidated 23 November 2026; qualitative mechanism trade-offs, all three supplied concept images and current modelling limits.

**Start with the [model checkpoint](MODEL_CHECKPOINT.md)**
([PDF](reports/checkpoint/Pump_Model_Checkpoint.pdf), [LaTeX source](reports/checkpoint/Pump_Model_Checkpoint.tex)).
It consolidates the current equations, decisions, implementation limits and next
steps. Rear pressure is now an explicit boundary: atmospheric is only one case.
The force balance must use the actual wetted and rear pressure areas.

Current scope: [adjustable right/left duties and ideal valve transitions](research/DUTY_ALLOCATION_AND_IDEAL_VALVES.md).
The shared-chamber allocation defaults to 50:50 and is adjustable with
`python python/build_operating_matrix.py --right-duty-fraction 0.6`. This changes
timing budgets only. Detailed valve transition dynamics are deferred until valve
selection; no switching-surge force rating is implied.

Waveform options: [published candidates, adjustable timing and comparison plots](research/WAVEFORM_CANDIDATES.md).

Latest analytical step: [Derivation 05: phase and pressure valve sequence](research/DERIVATION_05_PHASE_AND_PRESSURE_VALVE_SEQUENCE.md).
This defines candidate phase windows, optional pressure conditions, latched
commands, a future finite-opening refinement and the position needed for
gas-pressure build-up. Current valve transitions are idealised; a combined
simulation and component-specific switching loads are still pending.

Previous analytical step: [Derivation 04: retained-air storage and valve events](research/DERIVATION_04_RETAINED_AIR_AND_VALVE_EVENTS.md).
The retained-air storage derivation remains applicable. The user has now confirmed
**enforced valve states** coordinated with piston phase for both concepts; pressure
may also enter the command rule. See [valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md).
The passive switch rules are retained as a comparison model, not the selected
design. The combined enforced-valve model has not been implemented or simulated.
Complete and verify its derivation before developing the MATLAB interface.

Latest pressure calculation: [Derivation 03: pressure histories and the heart reference](research/DERIVATION_03_PRESSURE_AND_HEART_REFERENCE.md).
The **Pressure cycle** sheet now calculates a periodic three-element arterial
load, conditional chamber pressures and hydraulic forces, with an unscaled
published aortic/pulmonary reference. The reference is at 6.6 L/min and 75/min;
our trial remains at 5 L/min and 75/min. Its closed-valve diagnostics concern
passive checks only; the enforced-valve transitions remain unresolved, preventing
the phase force extrema from being treated as design ratings.
Run `python research/build_pressure_cycle.py` to reproduce this study.

Previous step: [Derivation 02: volume-preserving waveform joining](research/DERIVATION_02_WAVEFORM_JOINING.md).
The workbook now includes a **Waveform** sheet with selectable shapes, endpoint
smoothing, flow, velocity, acceleration and position. The 5% smoothing trial
removes acceleration jumps but increases peak acceleration; it is not a selected
motor command. Run `python research/build_smooth_waveforms.py` to reproduce the
comparison and width sensitivity.

Continue the analytical development with
[Derivation 01: full-liquid chamber, pressure and force](research/DERIVATION_01_FULL_LIQUID.md).

Supporting sources: [cardiovascular piston-pump literature review](research/PISTON_PUMP_LITERATURE_REVIEW.md)
and [formula-driven pressure starter workbook](spreadsheet/Pump_pressure_literature_starter.xlsx).
The baseline is 5 L/min at 75 pulses/min per circuit. The workbook contains a
local open-valve calculation and a periodic arterial-load study. Neither is a
completed chamber/valve cycle or a verified maximum-force rating.
See [spreadsheet scope and verification](spreadsheet/README.md).

Start with the [goal and concept comparison](GOAL_AND_CONCEPT_MATRIX.md) and
[operating-case matrix](OPERATING_MATRIX.md) ([CSV](OPERATING_MATRIX.csv)).
Both the single chamber with alternating duties (1A) and two dedicated
ventricular chambers (1B) remain under consideration.

MATLAB is now the preferred likely platform for the planned
[interactive piston, pressure and flow model](LIVE_MODEL_TARGET.md), following
the user's local Ubuntu installation. Python remains the executed numerical
reference while the coupled model and MATLAB implementation are developed.
Continue with [MODEL.md](MODEL.md) and the
[variable register](VARIABLES.md) ([CSV](VARIABLES.csv)). Editable calculations
and plots are in [Pump_Model.ipynb](python/Pump_Model.ipynb). The notebook is
optional: every simulation can run through the command line.

## Run locally

From this directory, using Python 3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/run_model.py check
python python/run_model.py baseline
```

The baseline writes `results/python/baseline.json` and `baseline.png`.
Those generated outputs are ignored by Git; the original archive is preserved.
To change an operating case, edit a JSON file containing `Case` fields:

```sh
python python/run_model.py baseline --config python/example_case.json
python python/run_model.py sweep
```

The sweep regenerates all 118 cases and the two trend figures in
`results/python/`. It does not alter the archive. The executed reference used
Python 3.12 and the versions pinned in `requirements.txt`; local installation
on the user's computer has not been performed by this task.

For the optional notebook, install the extra kernel dependencies and open it
in VS Code's Jupyter extension or another Jupyter frontend:

```sh
python -m pip install -r requirements-notebook.txt
```

Select the virtual environment's Python kernel. The notebook locates the model
from either its own directory, this design directory or the repository root.
It performs one new baseline simulation and plots its output; the archived
sweep is identified separately. All notebook code cells were executed sequentially in an in-process IPython
shell during this update. A separate Jupyter kernel could not bind sockets
in this environment, so frontend rendering remains unchecked. The committed
notebook has outputs cleared to keep code review clean.

To regenerate the architecture volume/timing budget (standard library only):

```sh
python python/build_operating_matrix.py
```

This does not run hydraulic simulations or modify the archived results.

## Files and model status

- `research/VALVE_CONTROL_AND_ROUTING.md`: confirmed enforced states, port assignments
  and next command/transition decisions.
- `GOAL_AND_CONCEPT_MATRIX.md`: project goal, concept comparison and evidence gates.
- `OPERATING_MATRIX.md`, `OPERATING_MATRIX.csv`: 11 operating points × two
  architectures, with explicit per-circuit and physical-chamber frequencies.
- `references/`: unaltered user sketch and provenance.
- `python/`: active model, runner, plotting script, notebook and matrix/register generators.
- `VARIABLES.csv`: editable source of the variable register; run
  `python python/render_variables.py` to update `VARIABLES.md`.
- `MODEL.md`: maintained equations, input provenance, interpretation and choices.
- `DECISIONS.md`, `PROGRESS.md`: dated decisions and work status.
- `python/verification_status.json`: executed regression and notebook checks.
- `archive/`: unchanged earlier source, data, figures and LaTeX reports.
- `MANIFEST.sha256`: original archive hashes.
- `LIVE_MODEL_TARGET.md`: interactive-model goal, fixed-geometry bpm behaviour
  and staged MATLAB/App Designer development plan.
- `matlab/`: earlier unexecuted port; review and numerical comparison are needed
  before it becomes the maintained implementation for the new interactive goal.

The Python hydraulic equations and baseline parameters are unchanged from the
executed reference. Regression checks cover three representative cases,
conservation, motion endpoints and the expected low-pressure guard. These are
numerical checks, not calibration or independent physical validation. Actuator
loads, feedback control, bypass paths and the whole circulation remain outside
the present solver.

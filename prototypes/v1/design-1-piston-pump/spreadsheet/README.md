# Pressure and literature starter workbook

Open `Pump_pressure_literature_starter.xlsx` in a spreadsheet application.
It needs no Python or special spreadsheet add-in to use. Amber cells are editable
inputs; calculations and chart source ranges are ordinary cell formulas.

- **Pressure start:** 5 L/min at 75 pulses/min, full-fill geometry, an illustrative
  forward-flow pressure/force point and two diameter sensitivities.
- **Literature:** purpose, architecture, model contribution, numerical conditions,
  access limits, reading locations and URLs for fourteen records.
- **Equation map:** proposed coupled model blocks, units, assumptions and status.
- **Waveform:** choose the published harmonic pair or half-sine, adjust endpoint
  smoothing, and inspect full-liquid flow, displacement, velocity and acceleration.
  Shared operating inputs link to Pressure start; its local force remains separate.
- **Pressure cycle:** selectable systemic/pulmonary three-element load, periodic
  arterial pressure, conditional phase chamber pressure/force, closed-valve checks
  and published arterial pressure/flow references. Two native charts compare
  curves against normalised cycle phase. The reference retains 75/min and 6.6 L/min.

On Pressure cycle, change C7 to select the load; edit the amber I23:M24 preset
cells to vary reservoir pressures, resistance and compliance. C14:C19 define
inlet geometry/losses. Outlet geometry, density and rear pressure link to Pressure
start; waveform settings link to Waveform. Columns N:P below row 69 contain
conditional chamber pressure, force and valve conflicts. C31:C32 expose unresolved
pressure jumps. A zero within-phase conflict does not resolve those transitions.

The Waveform sheet starts at a trial smoothing width of 5% at each endpoint.
Use zero for the raw reference or 0.02–0.50 with the current 400-interval phase
grid. A smaller nonzero width needs finer sampling in Python. Positive width
removes acceleration jumps but can increase peak acceleration. See
`../research/DERIVATION_02_WAVEFORM_JOINING.md` for the derivation and comparison.

Read `../research/PISTON_PUMP_LITERATURE_REVIEW.md` first. The local force is not
the maximum. The arterial-load time history and full-liquid filling phase are
now calculated, but chamber gas dynamics, actual valve events and pressure
transitions are not solved in this workbook. The illustrative loss coefficients are not
calibrated; zero additional linear resistance does not establish negligible
wall friction. Existing Python simulations have not been replaced.

## Reproducibility and checks

`../research/build_review.py` regenerates the source register, equation map and
independent tapered-passage check using Python's standard library.

`build_workbook.mjs` authors and checks the workbook using `@oai/artifact-tool`
from the Codex primary runtime. That authoring dependency is not required for
editing the delivered XLSX. To rebuild in an environment that supplies it,
run the builder with that environment's Node executable. `PEAR_DESIGN_DIR`
overrides this design directory and `PEAR_OUTPUT_DIR` selects the output folder.
Without overrides, the script writes to `../results/spreadsheet-review/`.

`spreadsheet_verification.json` records independent baseline calculations,
pressure and waveform input perturbations and zero detected formula errors.
The updated workbook contains five sheets and six linked native charts.
Pressure-cycle checks include comparison with Python, load selection, compliance
and diameter changes, then restoration of the baseline. The 400-interval phase
grid gives systemic chamber minimum −34.40 mmHg versus −34.54 mmHg on the Python
fine grid; force maxima agree to better than 0.01% for that case. The pulmonary
force check permits 0.4% relative sampling error. Do not infer physical accuracy
from numerical agreement. `export_verification.json` checks preservation of
existing cells, linked charts and the exported formula caches.
Waveform results were compared to an independent Python quadrature and fine grid;
the default sampled acceleration peak is 0.15% below the fine-grid result.
Changed views were rendered and visually inspected; the earlier views retain
their previous checks. Desktop Excel/LibreOffice execution,
component calibration and independent physical validation remain unperformed.

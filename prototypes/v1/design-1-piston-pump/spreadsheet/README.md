# Pressure and literature starter workbook

Open `Pump_pressure_literature_starter.xlsx` in a spreadsheet application.
It needs no Python or special spreadsheet add-in to use. Amber cells are editable
inputs; calculations and chart source ranges are ordinary cell formulas.

- **Pressure start:** 5 L/min at 75 pulses/min, full-fill geometry, an illustrative
  forward-flow pressure/force point and two diameter sensitivities.
- **Literature:** purpose, architecture, model contribution, numerical conditions,
  access limits, reading locations and URLs for fourteen records.
- **Equation map:** proposed coupled model blocks, units, assumptions and status.

Read `../research/PISTON_PUMP_LITERATURE_REVIEW.md` first. The local force is not
the maximum. Gas dynamics, valve events, filling and the Windkessel time history
are not solved in this workbook. The illustrative loss coefficients are not
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
three input perturbations and zero detected formula errors. Exported XML was
checked for 43 formulas and two linked charts. Every worksheet and chart area
was rendered and visually inspected. Desktop Excel/LibreOffice execution,
component calibration and independent physical validation remain unperformed.

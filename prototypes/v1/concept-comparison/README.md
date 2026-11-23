# Four-concept pump comparison

[Open the editable workbook](Pump_Concept_Comparison.xlsx).

The workbook compares **piston, diaphragm, impeller and peristaltic** concepts using the user's C1–C10 criteria and weights. All 40 scores, supporting-note fields and concept details start blank. Previous single/dual-piston scores are not applied to an unspecified piston variant.

## Use

- **Comparison:** enter whole-number scores from 1 to 5 in E7:H16. Weights in D7:D16 are editable and must sum to 1.00. Add the specific variant, actuation/valves, operating assumptions and reference links in E27:H30.
- **Criteria and notes:** the supplied high-score meanings accompany fields for each concept's evidence, reasoning and open assumptions.
- Totals calculate as the sum of weight × score only when all ten scores for that concept are valid and the weights are valid. Ranking appears when all four totals exist. Equal totals share a rank.
- Blank scores mean unassessed, not zero or an assumed average. The weighted ranking does not establish PDS compliance.

## Reproduction and checks

The criteria/weights are read from `../design-1-piston-pump/WEIGHTED_DESIGN_MATRIX.csv`, columns A–D, preserving the user-supplied matrix. Existing scores in that file are ignored.

`build.mjs` uses `@oai/artifact-tool`. Run in a temporary working directory with the installed Codex primary runtime dependencies available, supplying the design directory and output directory:

```bash
"$CODEX_PRIMARY_RUNTIME_NODE" build.mjs /path/to/design-1-piston-pump /path/to/output
```

The builder verifies known weighted totals, ranking changes, tied scores, incomplete input, invalid scores and invalid weight sums, then restores all scores to blank. `verification.json` records the checks. Both sheets were rendered and visually reviewed; the exported XLSX was inspected for formulas, blank scores and whole-number validation. Native Excel/LibreOffice execution was not available in this environment.

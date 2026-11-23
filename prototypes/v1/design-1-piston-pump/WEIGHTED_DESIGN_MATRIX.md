# Weighted piston concept assessment

23 November 2026. User-supplied C1–C10 criteria and weights. Provisional engineering judgements, not measured performance. Both concepts remain under consideration.

**Result: 1A shared chamber = 2.84/5; 1B dual chambers = 3.45/5.** The 0.61-point lead favours developing the dual-chamber concept first. It does not establish PDS compliance, a final architecture selection or a statistical confidence level.

## Concepts and common comparison basis

- **1A — single piston, alternating duties:** one flat-face plunger chamber alternates right/pulmonary and left/systemic assignments using enforced valves and selectors. This is not the early opposed-space separating-piston sketch.
- **1B — dual pistons:** two dedicated flat-face ventricular chambers, each with an inlet and outlet. Proposed inlet/outlet command pairing and adjustable timing remain subject to a feasible actuation schedule.
- Compare at **5 L/min and 75 pulses/min per circuit**: 66.67 mL net delivery per outlet pulse. The required net delivery is not automatically the geometric sweep.
- 1A must perform **150 fill–eject duties/min**; 1B performs **75 duties/min per piston**. A circuit period is 0.8 s. Equal 1A allocation gives 0.4 s per duty before charging switching/dwell against this budget. Unequal allocation remains adjustable. 1B gives each chamber the full 0.8 s period and permits overlap.
- At 180 pulses/min per circuit, the counts become 360 duties/min for 1A and 180/min per piston for 1B. This is cycle accounting, not a demonstrated capability.
- Both retain the known sealed front-air assumption, negligible-leakage starting model, explicit but unresolved rear boundary, and coupled reservoir/Windkessel loads. A fixed stroke alone does not independently prescribe mean flow and pulse rate.
- No motor, converter, materials, valve hardware or controller has been selected. The waveform scores assess architecture potential conditional on suitable motion control; a fixed-speed crank does not automatically supply an arbitrary waveform.

## Scoring convention

The user supplied the criteria and weights but no numerical scale. This assessment adopts 1–5: **1** major mismatch; **2** substantial constraints; **3** plausible fit with material work remaining; **4** strong architectural fit, verification pending; **5** strong fit supported by relevant verified performance and component evidence. No score of 5 is assigned.

An asterisk marks an **equal holding score of 3** where the present evidence does not justify a comparative score. It is an arithmetic placeholder, not proof of satisfactory performance. These rows account for **55% of the total weight**. No pass threshold has been assumed.

Weighted total = sum of (criterion weight × criterion score). The maximum is 5 because the supplied weights sum to 1.00. Totals are weighted ordinal preferences, not efficiencies, probabilities or percentages of requirements met.

## Applied matrix

| ID | Attribute | Weight | 1A single | 1B dual | 1A weighted | 1B weighted |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| C1 | Hydraulic operating capability | 0.16 | 3 | 4 | 0.48 | 0.64 |
| C2 | Waveform accuracy | 0.16 | 2 | 4 | 0.32 | 0.64 |
| C3 | Consistency | 0.16 | 3* | 3* | 0.48 | 0.48 |
| C4 | Prototype cost | 0.06 | 3* | 3* | 0.18 | 0.18 |
| C5 | Manufacturability | 0.10 | 3* | 3* | 0.30 | 0.30 |
| C6 | Blood-mimicking fluid compatibility | 0.05 | 3* | 3* | 0.15 | 0.15 |
| C7 | Cleaning and serviceability | 0.08 | 3* | 3* | 0.24 | 0.24 |
| C8 | System integration and modularity | 0.13 | 3 | 4 | 0.39 | 0.52 |
| C9 | Durability | 0.07 | 3* | 3* | 0.21 | 0.21 |
| C10 | Measurement interference | 0.03 | 3* | 3* | 0.09 | 0.09 |
| **Total** | | **1.00** | | | **2.84/5** | **3.45/5** |

## Reasons for the scores

**C1 — Hydraulic operating capability**

High score means: Can plausibly achieve required flow, pressure and pulsatile behaviour.

Both have a plausible displacement-based route to the target. 1A must complete two sequential duties per circuit period; 1B gives each chamber a full period and a dedicated load. Neither complete architecture has demonstrated the operating envelope.

**C2 — Waveform accuracy**

High score means: Can reproduce desired flow and pressure-waveform features under operating conditions

1A has shorter duty windows, state carry-over between loads and no overlap of direct chamber ejections. 1B permits overlapping cycles and separate chamber states. Its advantage remains conditional on suitable actuation, valve timing and circuit loads; linked commands do not provide arbitrary independent control.

**C3 — Consistency**

High score means: Stable, measurable and capable of repeatable profiles

Both can be instrumented, but neither has repeated-run evidence or a verified complete model. Retained-gas state, reservoir inventory, seals and valve switching must be controlled. Separate chambers alone do not prove better repeatability.

**C4 — Prototype cost**

High score means: Within our budget

1A saves one piston/chamber assembly but adds circuit selection hardware and its control. 1B duplicates chambers and seals but retains dedicated paths. No comparable BOM or quotations support a cost difference.

**C5 — Manufacturability**

High score means: Achievable with university equipment, accessible parts and manageable development effort

1A concentrates development in routing and sealing. 1B requires two chamber assemblies and coordinated motion. Drawings, tolerances, candidate parts and workshop availability have not established either as easier.

**C6 — Blood-mimicking fluid compatibility**

High score means: Suitable with BMF and does not degrade and limits unwanted effects on fluid properties

Architecture alone cannot establish compatibility. Both require checks of wetted materials, seals, temperature, gas retention and changes in fluid properties against the selected BMF.

**C7 — Cleaning and serviceability**

High score means: Disassembly possible, draining, cleaning and replacement of worn parts

1A has fewer chambers but a selector manifold may create difficult-to-drain passages. 1B has more wetted parts but dedicated circuits. Access, dead spaces, drainage and seal replacement need a layout assessment.

**C8 — System integration and modularity**

High score means: Can accommodate both systemic and pulmonary circulation interfaces

Both can connect the two circulations. 1B has dedicated right/left interfaces and chamber states, with no reassignment of a shared chamber. 1A requires coordinated selectors and pressure-state carry-over. Reservoir balance remains necessary in both.

**C9 — Durability**

High score means: Low expected wear and good prospect of maintaining performance over the required duty

The shared piston performs twice as many fill-eject duties per unit time as each dedicated piston at the same outlet pulse rate. This is an exposure difference, not a lifetime prediction: 1B has more seals/components and no wear data exist for either.

**C10 — Measurement interference**

High score means: Low vibration, noise and disturbance to sensors or future optical measurements

1A has faster shared-chamber duty scheduling; 1B has additional moving parts and possible coupled forces. Mounting, balance, transmission, valve actuation and sensor installation remain unspecified. No measured vibration or noise comparison exists.

## Interpretation and sensitivity

The lead comes entirely from C1 (+0.16), C2 (+0.32) and C8 (+0.13). C1 concerns attaining the required operating points, C2 concerns the accuracy of the resulting traces and C8 concerns circuit interfaces/modularity. These criteria are related; their contributions are not independent experimental evidence. The user’s weights are retained unchanged.

If both provisional dual scores for C1 and C2 fall from 4 to 3, its total becomes 3.13/5 and its lead falls to 0.29. A single one-point score change moves the total by that criterion’s weight.

As a stress test, moving all seven holding scores to 4 for 1A and 2 for 1B gives totals 3.39 and 2.90 and reverses the order. This deliberately correlated scenario is not a forecast or uncertainty interval; it shows why evidence covering 55% of the weight must be obtained before final selection.

The lower single-chamber waveform score assumes the goal remains realistic behaviour in both circuits, with right/left timing and waveform flexibility valued. If only sequential outlet pulses are required, C2 must be revisited. If simultaneous direct ventricular ejection becomes mandatory, unbuffered 1A fails that requirement regardless of its weighted total; outlet storage would be an additional design needing evaluation.

## Evidence needed before a final decision

1. Complete the current one-chamber equations and a verified periodic case, then add shared routing or dual coupling. Compare achieved flow, pressure/flow waveforms, inventory drift and front/rear hydraulic load at matched circuit conditions.
2. Specify waveform tolerances and measurement planes. Check whether proposed linked valve commands and motion profiles can meet right/left requirements simultaneously.
3. Prepare like-for-like layouts and BOMs including selectors, valve actuators, chambers, seals, sensors, structure and drive transmission. Review tolerances and university manufacturing access.
4. Select candidate wetted materials and seals; assess BMF compatibility, draining, dismantling and seal replacement.
5. Measure repeated-run profiles, leakage, wear, vibration and noise. Distinguish numerical verification, calibration and independent hardware validation.

PDS requirements remain feasibility gates. Neither concept has passed them by receiving a weighted score. The present result sets a provisional development priority and keeps the single-chamber option open.

## Provenance and reproducibility

- Criteria, weights and high-score definitions: user’s matrix supplied in this conversation on 23 November 2026, reproduced in the CSV. Scores and holding-value treatment: this provisional engineering assessment.
- Architecture and targets: [GOAL_AND_CONCEPT_MATRIX.md](GOAL_AND_CONCEPT_MATRIX.md) and the preserved [concept sketch](references/concept_sketch_2026-11-21.jpeg).
- Current model limits and rear boundary: [MODEL_CHECKPOINT.md](MODEL_CHECKPOINT.md).
- Consolidated derivations and interpretation: [team report](reports/team_review/Piston_Pump_Team_Report.pdf).
- Baseline repository commit: `0206ebcac92c50893c0f82035491ff6baa998138`.
- [WEIGHTED_DESIGN_MATRIX.csv](WEIGHTED_DESIGN_MATRIX.csv) contains the weights, meanings, scores, weighted contributions and rationale. Recalculate the weighted contributions if editing its scores; this CSV contains values, not live spreadsheet formulas.
- Arithmetic checked with exact decimal weights. No new hydraulic simulation, component quotation, MATLAB execution or physical test was performed for this assessment.
- The project handbook is not present in the available workspace; this assessment uses the user-provided essential project instructions and the inspected project records.

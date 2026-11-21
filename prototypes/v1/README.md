# V1 prototype

This branch tracks the first benchtop prototype for MECH0073 / PEAR.

| Workstream | Working branch | Entry point | Status |
| --- | --- | --- | --- |
| Design 1: Piston Pump | `v1-prototype-design-1-piston-pump` | [Living model document](https://github.com/UCL-PEAR-Group/PEAR-Tool/blob/v1-prototype-design-1-piston-pump/prototypes/v1/design-1-piston-pump/MODEL.md) | Exploratory hydraulic model; MATLAB migration awaiting runtime verification |

## Branch workflow

`v1-prototype` was created from `main`. The Design 1 branch is created from
this prototype branch and is intended to merge back into it when reviewed.
Git branches are independent references rather than nested folders. The names
avoid the conflicting pair `v1-prototype` and `v1-prototype/design-1`.
Future design branches should start from `v1-prototype` and use a distinct
name such as `v1-prototype-design-2-<concept>`.

Keep prototype-wide decisions here and design-specific work within its own
directory. Record assumptions and model status alongside results. Numerical
verification, calibration and independent experimental validation are separate
stages. No model result here establishes clinical predictive validity.

## Current scope

The piston-pump work estimates hydraulic pressure force, displacement and
delivered flow. Actuator/converter design is deferred. Windkessel loads are
interfaces to the wider circuit; the current sweep uses constant boundary
pressure tests. The legacy repository content is historical context, not a
validated baseline for this prototype.

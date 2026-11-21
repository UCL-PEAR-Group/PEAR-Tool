# Decision record

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D001 | 2026-11-21 | Use a flat-face plunger with no wetted rod area deduction | User concept | Accepted |
| D002 | 2026-11-21 | Use 5 L/min and 75 deliveries/min as the nominal reference | User-prescribed targets | Accepted |
| D003 | 2026-11-21 | Retain fixed mechanical travel within each running configuration | User design assumption | Accepted for current model |
| D004 | 2026-11-21 | Model deliberately retained sealed air using a reference gas state | User clarification; actual gas volume varies | Accepted; quantity/thermal model provisional |
| D005 | 2026-11-21 | Keep flow-rising-with-frequency and independent-flow strategies open | User instruction | Open comparison |
| D006 | 2026-11-21 | Estimate hydraulic pressure load before selecting actuation | User scope | Accepted |
| D007 | 2026-11-21 | Use MATLAB as the primary development language going forward | User preference | Port prepared; execution verification pending |
| D008 | 2026-11-21 | Preserve executed Python results and previous reports as a reference archive | Reproducibility during migration | Complete |
| D009 | 2026-11-21 | Track V1 on `v1-prototype`; develop Design 1 on `v1-prototype-design-1-piston-pump` | User's prototype/design branch organisation | Implemented |
| D010 | 2026-11-21 | Maintain `MODEL.md` plus a plain-text MATLAB Live Script | Readable explanation, executable calculations and reviewable Git diffs | Implemented; live rendering pending MATLAB |

No valve bore, cylinder size, net-delivery controller or force rating has been
selected. A bypass and active spill timing are candidates, not accepted designs.
The 50 mm face, 33.95 mm travel and 66.7 mL geometric stroke remain illustrative.

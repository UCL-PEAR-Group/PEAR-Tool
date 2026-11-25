# Restart 02 — valve continuity and pressure-control interpretation

25 November 2026. The user confirms that one valve will always be open while the piston moves and asks how pressure and flow can be controlled. This note proves the ideal continuity constraint and introduces a deliberately simple load model to explain control choices. It does not select a controller or implement a dynamic simulation.

## 1. Ideal moving-chamber balance

Retain the air-free, rigid, completely liquid-filled, incompressible and leak-free baseline from [Restart 01](01_CHAMBER_AND_VARIABLE_STROKE.md). Positive piston advance reduces wet volume. Define \(Q_i>0\) into the chamber and \(Q_o>0\) out:

$$
\frac{dV_c}{dt}=Q_i-Q_o=-A_p\dot x,
\qquad
\boxed{Q_o-Q_i=A_p\dot x.}
$$

If both valves are closed and have no leakage, \(Q_i=Q_o=0\), so \(A_p\dot x=0\). Since \(A_p>0\),

$$
\boxed{\text{both valves closed}\ \Longrightarrow\ \dot x=0.}
$$

The contrapositive requires at least one available flow path whenever the piston moves. It does not itself prohibit both valves being open: exactly-one-open and direction-matched routing are additional design rules.

Let effective ideal states \(u_i,u_o\) be 0 closed and 1 open. Commands and effective states coincide only in this ideal instantaneous-transition model:

$$
\begin{array}{c|c|c|c|c}
\text{phase} & \dot x & u_i & u_o & \text{flow}\\ \hline
\text{advance} & >0 & 0 & 1 & Q_o=A_p\dot x,\ Q_i=0\\
\text{return} & <0 & 1 & 0 & Q_i=-A_p\dot x,\ Q_o=0
\end{array}
$$

Thus \(\dot x\ne0\Rightarrow u_i+u_o=1\). The intended mutual-exclusion policy is \(u_i u_o=0\). Both may be closed during a stationary switching dwell. Finite valve travel would require the effective flow path to be established before motion resumes.

Equivalently, during the correctly routed ideal phases,

$$
Q_o=\max(A_p\dot x,0),\qquad Q_i=\max(-A_p\dot x,0).
$$

These are conditional conservation results, not assurances that arbitrary motion is attainable. Required pressure, inlet supply and actuator force must still be feasible. An open valve can have substantial resistance. Finite liquid/wall compliance would modify the balance during transitions; it is not included by silently changing the ideal constraints.

For one advance and one return per chamber cycle, integration yields \(SV=A_pS\) in this loss-free limit. The retained bookkeeping relation \(SV=\eta_v A_pS\) applies when net delivery losses are introduced. Do not simultaneously impose the leak-free instantaneous equations and a reduced efficiency without modelling or explicitly allocating the missing volume.

## 2. Define the pressure location

Use a common gauge datum:

- \(p_c\): pressure inside the wet piston chamber.
- \(p_a\): pressure immediately downstream of the outlet valve/path, at the arterial-load inlet.
- \(p_v\): downstream return/reservoir pressure for that load.
- \(p_b\): dry-side pressure, a separate later force-model boundary.

For this discussion, the controlled outlet quantity means \(p_a\). A phantom measurement plane farther downstream may require another pressure node.

An illustrative open-outlet relation, at specified stations with elevation/reversible area effects neglected or handled separately, is

$$
p_c-p_a=R_oQ_o+B_oQ_o|Q_o|+I_o\frac{dQ_o}{dt}.
$$

Here \(R_o\) is linear resistance (Pa s/m³), \(B_o\) is quadratic loss coefficient (Pa s²/m⁶), and \(I_o\) is fluid inertance (Pa s²/m³). This is a later model block, not calibrated hardware data. The inertial term can change sign; chamber pressure is not always higher than outlet pressure during deceleration.

A position controller supplies the force required to track the requested motion, within capability. Pressure is then a response of that motion and load. Force limitation can prevent tracking. Force-controlled pressure operation is another possible mode, but force and exact motion are not independently prescribed through the same mechanical input.

Throttling the pump outlet at unchanged delivered flow and unchanged downstream load mainly increases the pressure drop upstream of that restriction and the chamber force demand. It does not independently set the downstream arterial pressure.

## 3. Simplest explanatory pressure model

To expose the coupling, use a two-element external Windkessel with constant resistance \(R>0\), compliance \(C>0\) and return pressure \(p_v\):

$$
\boxed{C\frac{dp_a}{dt}=Q_o-\frac{p_a-p_v}{R}.}
$$

\(C\) has units m³/Pa and represents external volume storage per pressure change. It need not imply air in the piston chamber. This simplified illustration does not replace the previously considered three-element circuit or select Windkessel hardware.

Pressure rises when incoming flow exceeds drainage to the return boundary, and falls when drainage exceeds incoming flow. During outlet isolation/filling, \(Q_o=0\), and for constant \(p_v\):

$$
p_a(t)-p_v=[p_a(t_1)-p_v]\exp[-(t-t_1)/(RC)].
$$

Thus arterial pressure can remain elevated while the pump chamber refills. The external storage and outlet isolation separate the chamber and arterial states.

At periodic operation with constant \(R,C,p_v\), averaging gives

$$
\boxed{\overline p_a-p_v=R\overline Q_o.}
$$

Changing pulse shape at fixed mean flow can change pressure peaks and timing but does not change this model's mean pressure drop at fixed \(R\). A three-element Windkessel adds a proximal resistance; its mean total pressure drop uses the sum of its two resistances.

## 4. What can be controlled?

| Strategy | Adjustable quantity | Consequence |
| --- | --- | --- |
| Flow/motion priority | Piston amplitude, timing and trajectory | Flow is targeted; pressure follows the supplied circuit load |
| Pressure priority through piston motion | Feedback changes piston speed/trajectory using measured pressure | Pressure is targeted; the resulting flow and net delivery must be checked |
| Joint pump-and-load tuning/control | Motion plus a separate adjustable load element and appropriate compliance | Compatible pressure/flow targets can be pursued together, within hardware and model constraints |

With a fixed passive load, the two waveforms cannot be arbitrary independent targets. Inverting the illustrative load equation shows the required compatible flow:

$$
Q_{\rm required}(t)=C\frac{dp_{\rm target}}{dt}
+\frac{p_{\rm target}(t)-p_v}{R}.
$$

During ejection, this would require \(\dot x=Q_{\rm required}/A_p\). Its sign, integral, stroke bound and valve phase must be feasible. During filling with the outlet closed, \(Q_o=0\), so the pressure target must follow the load's free decay. Piston feedback cannot impose an arbitrary arterial trace while the outlet is isolated.

One actuator can still influence several summary features by shaping its waveform. The limitation concerns arbitrary independent pressure/flow histories and, for the stated constant-resistance model, incompatible mean targets. Sensors improve observability but do not add independent hydraulic actuation.

The present position-waveform model is therefore retained as the initial forward model: prescribe \(x(t)\), derive the routed flow, and calculate the resulting pressures from the external-load equations. Pressure targets are comparison objectives. A later controller can alter the waveform; a controller architecture is not selected by this explanation.

## 5. Illustrative mean-value calculation

Assume, solely for illustration, \(\overline Q_o=5\) L/min, \(\overline p_a=90\) mmHg and \(p_v=10\) mmHg. These pressure values are not newly selected requirements.

$$
R=\frac{90-10}{5}=16\ \mathrm{mmHg\,min/L}.
$$

If resistance rises to 20 mmHg min/L:

- Holding 5 L/min gives mean pressure \(10+20\times5=110\) mmHg.
- Holding mean pressure at 90 mmHg gives mean flow \((90-10)/20=4\) L/min.
- To retain both original mean targets in this model, restore the compatible total resistance (or change another independent boundary condition).

These are calculations from the simple periodic model, not simulated or measured rig results.

## 6. Literature support and scope

1. Kung EO, Taylor CA. Development of A Physical Windkessel Module to Re-Create In-Vivo Vascular Flow Impedance for In-Vitro Experiments. Cardiovasc Eng Technol. 2011;2(1):2–14. [DOI](https://doi.org/10.1007/s13239-010-0030-6). [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4548962/). Methods §2.1 relates pressure and flow through impedance and adjusts resistance/compliance to match target pressure given flow. The continuity argument and two-element illustration above are our stated derivations.
2. Meskin M, et al. Investigating the importance of left atrial compliance on fluid dynamics in a novel mock circulatory loop. Sci Rep. 2024;14:1864. [DOI](https://doi.org/10.1038/s41598-024-52327-6). [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10803730/). Methods, fluid-dynamic in-vitro test setup: piston stroke sets cardiac output, resistance clamps tune mean pressure, and the compliance chamber tunes pulse pressure. This is a precedent, not validation of our proposed pump.
3. Franzetti G, Díaz-Zuccarini V, Balabani S. Design of an In Vitro Mock Circulatory Loop to Reproduce Patient-Specific Vascular Conditions: Toward Precision Medicine. J Eng Sci Med Diagn Ther. 2019;2(4):041004. [DOI](https://doi.org/10.1115/1.4044488). [Author manuscript and record](https://discovery.ucl.ac.uk/id/eprint/10109598/). Supports coordinated waveform and afterload tuning.

Sources accessed 25 November 2026. The Nature page redirected to an inaccessible identity endpoint; the complete Meskin article was read through PMC instead. No new hydraulic simulation, controller tuning, hardware selection or experiment was performed.

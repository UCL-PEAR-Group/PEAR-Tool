"""Volume-preserving endpoint smoothing of candidate flow commands.

This is a kinematic study, not a pressure solver or a motor controller.
Published coefficients: supplied Franzetti et al. (2019), PDF p. 5, Eqs 14–15.
The endpoint window and its width are our engineering extension.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COEFFICIENTS = {
    'half_sine': ([1.0], [1.0]),
    'published_harmonics': ([.924, .230, .092], [.520, .257, .479]),
}
TRAP = getattr(np, 'trapezoid', None) or np.trapz


def raw_shape(u, coefficients):
    k = np.arange(1, len(coefficients) + 1)
    c = np.asarray(coefficients)
    phase = np.asarray(u)[..., None] * k * np.pi
    return (np.sum(c * np.sin(phase), axis=-1),
            np.sum(c * k * np.pi * np.cos(phase), axis=-1))


def window(u, epsilon):
    if not 0 <= epsilon <= .5:
        raise ValueError('epsilon must lie in [0, 0.5]')
    u = np.asarray(u)
    if epsilon == 0:
        return np.ones_like(u), np.zeros_like(u)
    z = np.minimum(1., np.minimum(u, 1-u)/epsilon)
    h = 10*z**3 - 15*z**4 + 6*z**5
    dh = 30*z**2*(1-z)**2
    sign = np.where(u < epsilon, 1., np.where(u > 1-epsilon, -1., 0.))
    return h, sign*dh/epsilon


def integral(coefficients, epsilon):
    """Independent high-order integration, split at the window boundaries."""
    nodes, weights = np.polynomial.legendre.leggauss(80)
    bounds = sorted(set([0., epsilon, 1-epsilon, 1.]))
    area = 0.
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        u = lo + (nodes+1)*(hi-lo)/2
        g, _ = raw_shape(u, coefficients)
        w, _ = window(u, epsilon)
        area += np.dot(weights, g*w)*(hi-lo)/2
    return float(area)


def phase_profile(u, coefficients, epsilon):
    g, dg = raw_shape(u, coefficients)
    w, dw = window(u, epsilon)
    area = integral(coefficients, epsilon)
    return g*w/area, (dg*w+g*dw)/area


def calculate(name, epsilon, qmean, bpm, gamma, diameter, n=40000):
    if min(qmean, bpm, diameter) <= 0 or not 0 < gamma < 1:
        raise ValueError('Positive flow, rate, diameter and 0 < gamma < 1 required')
    t = 60/bpm
    sv = 1000*qmean/bpm
    area = np.pi*(diameter/1000)**2/4
    u = np.linspace(0, 1, n+1)
    phases = []
    for i, (c, duration) in enumerate(zip(COEFFICIENTS[name], [gamma*t, (1-gamma)*t])):
        shape, slope = phase_profile(u, c, epsilon)
        sign = 1 if i == 0 else -1
        q = sign*sv/duration*shape
        dq = sign*sv/duration**2*slope
        cumulative = np.r_[0., np.cumsum((shape[1:]+shape[:-1])/2*np.diff(u))]
        x = cumulative if i == 0 else 1-cumulative
        phases.append({'u': u, 'time': u*duration + (0 if i == 0 else gamma*t),
                       'q': q, 'dq': dq, 'accel': dq*1e-6/area,
                       'x': x, 'duration': duration,
                       'volume': float(TRAP(abs(q), u*duration))})
        assert shape.min() > -1e-12
        assert abs(phases[-1]['volume']-sv) < 2e-6
    e, f = phases
    metric = {'profile': name, 'epsilon': epsilon,
              'ejection_peak_L_min': float(e['q'].max()*.06),
              'filling_peak_L_min': float(-f['q'].min()*.06),
              'max_abs_acceleration_m_s2': float(max(abs(e['accel']).max(), abs(f['accel']).max())),
              'ejection_volume_mL': e['volume'], 'filling_volume_mL': f['volume'],
              'eject_fill_acceleration_jump_m_s2': float(f['accel'][0]-e['accel'][-1]),
              'wrap_acceleration_jump_m_s2': float(e['accel'][0]-f['accel'][-1]),
              'return_position_over_stroke': float(f['x'][-1])}
    if epsilon > 0:
        assert max(abs(metric[k]) for k in ['eject_fill_acceleration_jump_m_s2', 'wrap_acceleration_jump_m_s2']) < 1e-12
    return metric, phases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epsilon', type=float, default=.05)
    parser.add_argument('--flow', type=float, default=5.)
    parser.add_argument('--bpm', type=float, default=75.)
    parser.add_argument('--ejection-fraction', type=float, default=.4)
    parser.add_argument('--diameter-mm', type=float, default=50.)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'waveforms')
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    params = (args.flow, args.bpm, args.ejection_fraction, args.diameter_mm)
    metrics, rows, convergence = [], [], []
    fig, axes = plt.subplots(3, 2, figsize=(11.5, 8.2), sharex=True)
    for col, name in enumerate(COEFFICIENTS):
        for eps, style, colour, label in [(0., '--', '#87919B', 'Original phase shapes'),
                                         (args.epsilon, '-', '#176B72', f'Smoothed: ε = {args.epsilon:g}')]:
            m, phases = calculate(name, eps, *params)
            metrics.append(m)
            for i, p in enumerate(phases):
                axes[0, col].plot(p['time'], p['q']*.06, style, color=colour, label=label if i == 0 else None)
                axes[1, col].plot(p['time'], p['x'], style, color=colour)
                axes[2, col].plot(p['time'], p['accel'], style, color=colour)
                if eps == args.epsilon:
                    for j in range(0, len(p['u']), 100):
                        rows.append([name, 'ejection' if i == 0 else 'filling', p['time'][j], p['u'][j],
                                     p['q'][j], p['dq'][j], p['x'][j], p['accel'][j]])
        axes[0, col].set_title('Half-sine pair' if col == 0 else 'Swanson–Clark / Talukder–Reul')
        for ax in axes[:, col]:
            ax.axvline(60/args.bpm*args.ejection_fraction, color='#CDD3D8', linewidth=.8)
            ax.grid(alpha=.18)
            ax.spines[['top', 'right']].set_visible(False)
        axes[0, col].legend(loc='lower left', fontsize=8)
        axes[2, col].set_xlabel('Cycle time (s)')
    axes[0, 0].set_ylabel('Signed piston flow (L/min)')
    axes[1, 0].set_ylabel('Position / stroke')
    axes[2, 0].set_ylabel('Acceleration (m/s²)')
    for row in range(3):
        low = min(ax.get_ylim()[0] for ax in axes[row])
        high = max(ax.get_ylim()[1] for ax in axes[row])
        for ax in axes[row]: ax.set_ylim(low, high)
    fig.suptitle(f'{args.flow:g} L/min · {args.bpm:g}/min · filling:ejection = {1-args.ejection_fraction:.0%}:{args.ejection_fraction:.0%}', fontsize=14)
    fig.text(.5, .015, f'D = {args.diameter_mm:g} mm illustrative. Negative flow denotes filling. Kinematics only; no gas or pressure dynamics.', ha='center', fontsize=9)
    fig.tight_layout(rect=[0, .04, 1, .96])
    fig.savefig(out/'smooth_waveform_comparison.png', dpi=160)
    plt.close(fig)
    # Boundary-window sensitivity and spreadsheet quadrature resolution.
    sensitivity = []
    for name in COEFFICIENTS:
        for eps in sorted(set([0., .02, .05, .1, .15, args.epsilon])):
            sensitivity.append(calculate(name, eps, *params)[0])
            for i, c in enumerate(COEFFICIENTS[name]):
                exact = integral(c, eps)
                for n in [200, 400, 800]:
                    u = np.linspace(0, 1, n+1)
                    g, _ = raw_shape(u, c)
                    w, _ = window(u, eps)
                    err = abs(TRAP(g*w, u)/exact-1)
                    convergence.append({'profile': name, 'phase': i, 'epsilon': eps,
                                        'intervals': n, 'relative_integral_error': float(err)})
                    if n >= 400: assert err < 5e-5
    # A centred finite difference checks analytic derivatives independently.
    derivative_errors = []
    for name in COEFFICIENTS:
        for c in COEFFICIENTS[name]:
            u = np.linspace(.001, .999, 999)
            delta = 1e-6
            shape, ds = phase_profile(u, c, args.epsilon)
            numerical = (phase_profile(u+delta, c, args.epsilon)[0]-phase_profile(u-delta, c, args.epsilon)[0])/(2*delta)
            error = float(max(abs(numerical-ds)))
            assert error < 2e-6
            derivative_errors.append(error)
    with (out/'smooth_waveform_samples.csv').open('w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['profile', 'phase', 'cycle_time_s', 'u', 'signed_flow_mL_s',
                         'signed_flow_slope_mL_s2', 'position_over_stroke', 'acceleration_m_s2'])
        writer.writerows(rows)
    result = {'status': 'Numerically checked kinematic commands; no hydraulic or physical validation',
              'inputs': vars(args) | {'output': str(out)},
              'source': 'Franzetti 2019, supplied PDF p. 5 Eqs 14–15; endpoint window is our extension',
              'metrics': metrics, 'epsilon_sensitivity': sensitivity,
              'quadrature_convergence': convergence, 'derivative_max_errors': derivative_errors,
              'scope': 'One dedicated chamber, full liquid, no leakage, no dwell, feasible ideal valves assumed'}
    (out/'smooth_waveform_verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()

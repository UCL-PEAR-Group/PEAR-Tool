# MATLAB development status

The user now identifies MATLAB as the preferred likely platform for the future
interactive piston, pressure and flow model, following local installation on
Ubuntu. See [the development target](../LIVE_MODEL_TARGET.md).

The files currently in this directory are an earlier, unexecuted port. Source
parsing passed in the earlier work, but no MATLAB runtime verification was
performed. They do not incorporate all later waveform/pressure-cycle work and
are not yet the maintained calculation entry point.

Use `../python/`, the spreadsheet and recorded numerical outputs as the executed
reference while we complete the coupled derivation and review the MATLAB
implementation. Numerical MATLAB comparisons must be executed and recorded
before the port is promoted. No application or physical rig connection has been
implemented by the roadmap update.

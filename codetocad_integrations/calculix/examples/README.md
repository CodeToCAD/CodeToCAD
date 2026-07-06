# CalculiX FEA examples

- `beam_fea.py` — a steel cantilever beam modeled with Build123D, clamped
  on one face and end-loaded; solves a static analysis with CalculiX and
  renders the deformed shape colored by von Mises stress and displacement.
  The results match the Euler-Bernoulli analytic solution to ~1%.

Requirements: `uv sync --extra calculix --extra build123d` plus the
CalculiX solver. Install `ccx` any of these ways:

- `micromamba create -p ~/.codetocad/ccx -c conda-forge calculix`
  (auto-discovered by the integration)
- any `ccx` on your PATH
- set `CODETOCAD_CCX=/path/to/ccx`

# Contributing

Use Python 3.12+, create a virtual environment and install `.[dev]`. Work on a
feature branch and open a PR; do not push unreviewed implementation to main.
Keep commits focused and run pytest, Ruff, mypy and a package build before review.
Add synthetic-signal tests for DSP changes and injectable-backend tests for I/O
logic. Document hardware-dependent checks separately, including skipped checks.
Do not add prerecorded personal microphone audio or fabricate measurements.

Describe user-visible behavior, architecture decisions, test commands/results
and remaining hardware limitations. Use only code/assets with verified licenses;
retain required attribution. Discuss native dependencies or licensing changes
before introducing them. The original project is MIT; dependencies are not
relicensed by that choice.

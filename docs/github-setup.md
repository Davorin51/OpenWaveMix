# GitHub development checkout

The project is published at https://github.com/Davorin51/OpenWaveMix.
The current default development branch is `development`; main has not been created
or modified. The initial milestone is published for review and continued work.

```shell
git clone --branch development https://github.com/Davorin51/OpenWaveMix.git
cd OpenWaveMix
python -m venv .venv
# Activate the environment, then:
python -m pip install -e ".[dev]"
pytest
```

Create a focused feature branch for subsequent changes and open a PR into
`development`. Establishing main and merging a reviewed release into it remain
separate actions requiring explicit approval.

The original downloadable source snapshot used the local branch
`feat/device-monitoring`. Its optional history bundle preserves those local
commits. The GitHub import preserves the same milestone content in focused
commits following an initial repository bootstrap commit. Commit IDs differ
because the parent history differs.

Do not force-push over unseen remote changes or commit the optional history
bundle to the repository. See validation.md for the recorded local checks and
hardware limitations.

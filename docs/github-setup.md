# Import this milestone to GitHub

The prepared project is on `feat/device-monitoring`. No change was pushed to
main. The connected GitHub interface could inspect repositories but could not
create the missing target repository.

Create an **empty** `Davorin51/OpenWaveMix` repository in GitHub, choosing the
visibility you want, without adding README/license files. If working from the
provided source ZIP, initialize a local feature branch:

```shell
git init -b feat/device-monitoring
git add .
git commit -m "Add researched audio discovery and metering foundation"
git remote add origin https://github.com/Davorin51/OpenWaveMix.git
git push -u origin feat/device-monitoring
```

If using the original committed checkout or restoring the included history
bundle, skip init/add/commit and add only the remote and feature-branch push.
The optional `OpenWaveMix-history.bundle` in the download preserves the focused
local commits; extract it elsewhere and run `git clone OpenWaveMix-history.bundle
OpenWaveMix-with-history` to reconstruct that checkout. Do not commit the bundle.

If the target already has a main branch, fetch and review it first, preserve its
working files and prepare a compatible feature branch/PR. Do not force-push over
unseen content or merge to main without explicit approval. For a brand-new empty
remote, the first pushed branch may become its default; establishing main and
merging this milestone is a separate reviewed action.

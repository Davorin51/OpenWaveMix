# Third-party licensing

OpenWaveMix's LICENSE applies only to original project code and documentation.
No external application source, assets or drivers are vendored.

Runtime dependencies retain their own licensing:

| Component | Primary license | Source |
| --- | --- | --- |
| python-sounddevice | MIT | https://github.com/spatialaudio/python-sounddevice/blob/master/LICENSE |
| PortAudio (native library) | MIT-style | https://portaudio.com/docs/v19-doxydocs/License.html |
| NumPy | BSD-3-Clause; binary artifacts contain additional components | https://github.com/numpy/numpy/blob/main/LICENSE.txt |
| CFFI | MIT | https://foss.heptapod.net/pypy/cffi |

Installation resolves these separately. When distributing a Windows executable,
include the actual resolved dependencies' full license texts and bundled native
library notices. This summary is not a substitute for those texts. Inspect the
installed wheels' licenses and create an exact binary dependency inventory before
publishing a release. No Windows binary is shipped by this milestone.

Future PySide6/Qt and SciPy dependencies are evaluated in the technology decision;
they are not runtime dependencies yet. Do not describe an entire bundled Qt
application as exclusively MIT. VB-CABLE/Voicemeeter/Elgato products are not
included, and their separate redistribution rights must not be assumed.

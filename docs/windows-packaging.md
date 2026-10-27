# Windows executable build (CLI milestone)

Build on Windows with the desired Python architecture. PyInstaller is not a
cross-compiler. This recipe is provided but has not been executed on Windows here.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev,packaging]"
.\.venv\Scripts\python -m PyInstaller --clean --noconfirm --onedir --console --name OpenWaveMix --collect-all sounddevice --collect-all _sounddevice_data scripts/launcher.py
.\dist\OpenWaveMix\OpenWaveMix.exe devices
```

Prefer `--onedir` for inspectable native DLLs and future replaceable Qt libraries.
The Windows sounddevice wheel includes `_sounddevice_data`; inspect PyInstaller
warnings and DLL collection rather than assuming the command is sufficient.
Test on a clean Windows 11 machine without Python, enumerate endpoints, capture
explicitly and test device loss. Preserve native package licenses in the output
folder with their exact versions. Do not publish until notices and DLL inventory
are verified. This release does not contain a compiled EXE or virtual driver.

The future GUI needs additional PySide6/Qt plugin and license handling; this CLI
recipe does not validate that later product.

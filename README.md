# PokeGBA

Cartridge-style Pokemon launcher for Linux. It launches locally supplied
Game Boy, Game Boy Color, and Game Boy Advance games through mGBA.
Infinite Fusion via Wine is optional and experimental. Raspberry Pi/ARM
gameplay has not been validated; use native ARM dependencies on ARM devices.

## Run locally

Install Python with Tkinter and a trusted mGBA executable. Supply your own
legally obtained ROMs in `roms/`, using the filenames in
`launcher/pokemon-gba-menu.py`.

```sh
bash launcher/pokemon-gba-menu.sh
```

The checkout is the default project directory. mGBA is found on `PATH` or at
`emulators/mgba-qt`. Local environment overrides are available:

| Variable | Purpose |
| --- | --- |
| `POKEMON_GBA_HOME` | Project directory for local games and emulators |
| `POKEMON_GBA_ROM_DIR` | Your ROM directory |
| `POKEMON_GBA_MGBA` | Path to the mGBA executable |
| `POKEMON_GBA_PYTHON` | Python executable for the shell wrapper |
| `POKEMON_GBA_FUSION_DIR` | Optional Infinite Fusion directory |
| `POKEMON_GBA_WINE` | Wine executable |
| `POKEMON_GBA_WINEPREFIX` | Isolated local Wine prefix |

The desktop entry in `packaging/` is an installation template. Set its paths
locally before installing it. Keep the personalized entry out of Git.

## Security and private files

This repository supplies launcher code and artwork. ROMs, save data,
savestates, emulators, game executables, and personal configuration are not
included. The launcher starts the emulator or game with your user privileges;
use trusted executables. Wine is not a malware sandbox. Keep personal files
and local paths out of public issues and commits. See [SECURITY.md](SECURITY.md).

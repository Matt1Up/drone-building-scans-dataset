# Drone Building Scans

Two commercial buildings in the Minneapolis suburbs, flown August 2026. Full image sets with
GPS intact, plus the finished 3D models so you can compare your reconstruction against mine.

CC BY 4.0.

| scan | images | size | subject |
|---|---:|---|---|
| `rec-center` | 393 | 4.1 GB | recreation center |
| `border-foods` | 951 | 12 GB | Border Foods (Taco Bell franchise) — flat roof, rooftop HVAC, parking, drive-through |

There is almost no free drone photogrammetry test data for buildings. Everything published is
either a city block or a turntable object. If you are building roof inspection, insurance, or
solar tooling and need real data to test against, this is meant for you.

## Capture

Both scans were flown low and slow, under 16 m, with the gimbal sweeping from straight down to
slightly upward.

| | rec center | border foods |
|---|---|---|
| captured | 2026-08-16, 17:31–18:11 | 2026-08-22, 18:17–19:13 |
| relative altitude | 2.7 – 15.6 m | 1.1 – 15.2 m |
| nadir (≤ −80°) | 144 | 416 |
| oblique (−80° to −30°) | 22 | 231 |
| low / level (> −30°) | 227 | 304 |

Nadir frames cover the roof, oblique catch the roof edge and parapet, low and level frames get
the walls. That's why walls resolve — most aerial capture is nadir-only and building sides come
out as smeared vertical texture.

| | |
|---|---|
| **Camera** | DJI FC9313, 8.7 mm, f/1.8 |
| **Resolution** | 4096 × 3072 — native sensor readout, not an interpolated mode |
| **ISO** | 100 throughout |
| **Geotagging** | GPS lat/lon/altitude in EXIF on every frame |

Native resolution matters. These drones offer a higher-megapixel mode that interpolates from
the same sensor well — it invents texture, and a photogrammetry solver treats invented texture
as real observations. Everything here is the native readout.

## Reference models

Each scan ships with the finished model, so you can check your result against a known one
without needing my camera poses.

| | |
|---|---|
| `rec-center/model/rec-center.glb` | 19.7 MB |
| `border-foods/model/border-foods.glb` | 21.8 MB |
| `border-foods/model/border-foods.obj` + `.mtl` | 456 MB |

GLB opens in a browser, Blender, or any glTF viewer. OBJ is there for the bigger one if you
want the untextured geometry at full density.

## Gaussian splatting

No camera poses here — run COLMAP or GLOMAP first. Both scans are small enough that ordinary
3DGS handles them without the large-scale variants, unlike a city block. Downsample to
~1600 px before training.

The reference `.glb` gives you something to compare a splat or a mesh against.

## Download

Images are hosted off GitHub. See [docs/download.md](docs/download.md).

```bash
./scripts/download.sh --scan rec-center      # 4.1 GB, start here
./scripts/download.sh --scan border-foods    # 12 GB
./scripts/download.sh --all
./scripts/verify.sh
```

## Notes

- **Both are commercial buildings.** No residential property, no occupants.
- The licence covers the imagery. Any trademarks visible in it belong to their owners.
- Shot in evening light — long shadows on the parking lot in both sets.

## Licence

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

[Creative Commons Attribution 4.0](LICENSE). Commercial use and ML training are fine. Credit required.

```
Drone Building Scans — Matthew Guertin, 2026. CC BY 4.0.
https://github.com/Matt1Up/drone-building-scans-dataset
```

## Related

- **[Tree photogrammetry dataset](https://github.com/Matt1Up/tree-photogrammetry-dataset)** — 812 images of one tree, with camera poses.
- **[Chicago / Grant Park](https://github.com/Matt1Up/chicago-photogrammetry-dataset)** — 2,751 aerial images over downtown Chicago.
- **[mattguertin.com](https://mattguertin.com)**

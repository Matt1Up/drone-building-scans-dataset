# Downloading

Images, models and tie points are hosted on Hugging Face, not GitHub — this repo holds
documentation, manifests, checksums and the small pose files.

```
flat-roof/       951 images   10.61 GiB
shingle-roof/    395 images    4.08 GiB
                              15.51 GiB total
```

## Hugging Face

```bash
pip install -U huggingface_hub

./scripts/download.sh --scan shingle-roof   # 4.08 GiB, start here
./scripts/download.sh --scan flat-roof      # 10.61 GiB
./scripts/download.sh --all                 # both
./scripts/download.sh --models              # reference models only, ~475 MB
```

Browse: **https://huggingface.co/datasets/Matt1up/drone-building-scans**

Raw CLI, without the wrapper. Run it again if it stops — finished files are skipped.

```bash
hf download Matt1up/drone-building-scans --repo-type dataset --local-dir ./data
```

## What's in each scan

```
<scan>/images/               source JPEGs, original aircraft filenames, EXIF intact
<scan>/poses/xmp/            RealityScan XMP sidecars, one per aligned image
<scan>/poses/colmap/         cameras.txt, images.txt, points3D.txt
<scan>/model/                textured .glb (and .obj + .mtl for flat-roof)
<scan>/sfm/tiepoints.ply     sparse point cloud
flat-roof/controlpoints.txt  AprilTag control points — the scale reference
```

`cameras.txt` and `images.txt` are also committed to this repo under `poses/`, so you can read
the camera parameters without downloading anything. `points3D.txt` is on Hugging Face because
of its size.

## Why individual files, not archives

- download one scan without taking both
- downloads resume — a dropped connection doesn't restart from zero
- each file is checksummed on its own
- no scratch space needed to unpack an archive

Nothing is gzipped. JPEG is already compressed; measured on this content it reclaims well under
1% while destroying random access.

## Verifying

```bash
./scripts/verify.sh
```

Checks SHA-256 for every image you actually have and ignores the rest, so partial downloads
verify cleanly. The lists are `manifest/<scan>/checksums.sha256`.

Per-scan manifests live at `manifest/<scan>/images.csv` and carry filename, size, SHA-256,
dimensions, capture time and GPS for every image.

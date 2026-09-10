# Reproducing the reconstructions

The images are ordinary geotagged JPEGs, so any structure-from-motion tool reads them. Below
are suggested settings and the things specific to *these* captures worth knowing before you
spend hours on them.

Both scans ship solved poses in [`../poses/`](../poses/), so you can skip alignment entirely
and go straight to meshing or splatting. Reproduce it only if you want to compare.

---

## What to expect

| | flat-roof | shingle-roof |
|---|---|---|
| images | 951 | 395 |
| solved | **951 / 951** | 384 / 395 |
| components | 1 | **3** |

**The shingle-roof alignment splits.** RealityScan produced three components — 384 cameras,
4 and 3 — and the two small ones are solved in their own arbitrary coordinate frames. Only the
384-camera component is published; the other 7 cameras are listed in
[`../poses/shingle-roof/unaligned.txt`](../poses/shingle-roof/unaligned.txt) alongside the 4
that never aligned.

If your solve splits the same way, that is the dataset behaving normally, not your settings
failing. Adding control points across the structure is the usual fix.

**flat-roof solves cleanly at 951/951** in one component. It is the easier of the two.

---

## RealityCapture / RealityScan

Suggested starting settings. These are recommendations, not a record of the original runs.

| setting | value | why |
|---|---|---|
| Image overlap | `High` | dense low-altitude orbits |
| Detector sensitivity | `Medium` | buildings have plenty of texture |
| Max features per image | `40000` | default is fine at this image count |
| Image downscale factor | `1` | do not downscale; fine detail is the point |

Reconstruction in `Normal` detail is enough for a building. Set a reconstruction region first —
the unclipped extent pulls in a lot of thinly-observed parking lot and neighbouring lawn.

---

## COLMAP / GLOMAP

```bash
colmap feature_extractor \
  --database_path db.db --image_path images/ \
  --ImageReader.camera_model SIMPLE_RADIAL \
  --ImageReader.single_camera 1

colmap exhaustive_matcher --database_path db.db

# either COLMAP's mapper, or GLOMAP for a much faster global solve
colmap mapper --database_path db.db --image_path images/ --output_path sparse/
```

`--ImageReader.single_camera 1` **is** correct here — unlike the Chicago dataset, every frame in
each scan is 4096 × 3072 from the same lens, so one camera model is right.

Exhaustive matching is tractable at 395 and 951 images.

---

## Scale

Only **flat-roof** is metrically scaled, from a 1.997 m AprilTag bar used as control points.
See the *Scale* section in the [README](../README.md), including the tag-numbering trap —
RealityScan's labels are not the official 36h11 IDs a detector will report.

A fresh solve of your own will come out at arbitrary scale unless you detect the tags and apply
the 1.997 m constraint yourself.

**shingle-roof has no scale reference at all.** Geometry only.

---

## Gaussian splatting

`poses/<scan>/colmap/` is a drop-in sparse reconstruction — `cameras.txt`, `images.txt` and
`points3D.txt` (the last hosted with the images). Point a 3DGS pipeline at it and train.

Both scans are small enough for ordinary 3DGS; the large-scale variants a city block needs do
not apply. Downsample to ~1600 px wide first — nothing trains at 4096 px, and the originals are
here so you can choose.

# Downloading

Images are hosted on Hugging Face, not GitHub — this repo holds documentation, manifests and
checksums.

```
rec-center/     393 images    4.1 GB
border-foods/   951 images     12 GB
```

## Hugging Face

```bash
pip install -U 'huggingface_hub[cli]'

./scripts/download.sh --scan rec-center     # start here, 4.1 GB
./scripts/download.sh --scan border-foods   # 12 GB
./scripts/download.sh --all                 # both
./scripts/download.sh --models              # just the reference models, ~500 MB
```

Or browse: **https://huggingface.co/datasets/Matt1up/drone-building-scans**

## Why individual files, not archives

The images are published as individual files rather than one archive:

- download one scan without taking both
- downloads resume — a dropped connection doesn't restart from zero
- each file is checksummed on its own
- no scratch space needed to unpack

Nothing is gzipped. JPEG is already compressed; measured on these sets it reclaims well under
1% while destroying random access.

## Verifying

```bash
./scripts/verify.sh
```

Checks SHA-256 for every file present and ignores the rest, so partial downloads verify fine.
`manifest/images.csv` also carries dimensions, capture time, GPS and gimbal angle per image.

#!/usr/bin/env bash
# Download building scan image sets.
#   ./scripts/download.sh --scan rec-center      4.1 GB, 393 images
#   ./scripts/download.sh --scan border-foods    12 GB, 951 images
#   ./scripts/download.sh --all
#   ./scripts/download.sh --models               reference .glb/.obj only (~500 MB)
set -euo pipefail
HF_REPO="${HF_REPO:-Matt1up/drone-building-scans}"
DEST="${DEST:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/data}"

scans=(); mode=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scan)   scans+=("$2"); mode=scan; shift 2 ;;
    --all)    mode=all; shift ;;
    --models) mode=models; shift ;;
    --dest)   DEST="$2"; shift 2 ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
[[ -z "$mode" ]] && { sed -n '2,6p' "$0"; exit 2; }

if ! command -v hf >/dev/null 2>&1 && ! command -v huggingface-cli >/dev/null 2>&1; then
  echo "Needs the Hugging Face CLI:  pip install -U 'huggingface_hub[cli]'"
  echo "Other mirrors are listed in docs/download.md"
  exit 1
fi
HF=$(command -v hf || command -v huggingface-cli)

mkdir -p "$DEST"
args=(download "$HF_REPO" --repo-type dataset --local-dir "$DEST")
case "$mode" in
  all)    : ;;
  models) args+=(--include "*/model/*") ;;
  scan)   for s in "${scans[@]}"; do args+=(--include "${s}/*"); done ;;
esac

echo "→ $HF_REPO ($mode) → $DEST"
"$HF" "${args[@]}"
echo
echo "Done. Verify with:  ./scripts/verify.sh"

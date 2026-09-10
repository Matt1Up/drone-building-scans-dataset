#!/usr/bin/env python3
"""Copy the XMP poses of the LARGEST aligned component, renamed to image basenames.

Usage: scripts/pick-component.py <run_dir> <dest_scan_dir>

RealityScan splits alignment into components when it cannot tie everything together. Each
component is solved in its OWN arbitrary coordinate frame, so poses from different components
must never be merged -- doing so silently scatters cameras into unrelated frames. The report
lists every image once per component, so a naive parse also miscounts what is unaligned.
"""
import re, html, sys, os, shutil

run, dst = sys.argv[1], sys.argv[2]
s = html.unescape(open(f"{run}/report-cameras.html", encoding="utf-8", errors="replace").read())
blocks = re.split(r'### COMPONENT ', s)[1:]

comps = []
for b in blocks:
    h = re.match(r'"([^"]*)" guid=(\S+) cameras=(\d+)', b)
    rows = re.findall(r'img=(\S+) idx=(\d+) wh=(\d+)x(\d+) aligned=(\w+) cam=(-?\d+)', b)
    comps.append((h.group(1), [r for r in rows if r[4] == "True"], rows))
comps.sort(key=lambda c: -len(c[1]))
name, aligned, allrows = comps[0]
print(f"  components: {[(c[0], len(c[1])) for c in comps]}")
print(f"  using largest: {name} with {len(aligned)} cameras")
if len(comps) > 1:
    orphan = sum(len(c[1]) for c in comps[1:])
    print(f"  ignoring {len(comps)-1} orphan component(s), {orphan} cameras -- different frames")

out = f"{dst}/poses/xmp"
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    os.remove(os.path.join(out, f))
made = miss = 0
for img, idx, w, h, a, cam in aligned:
    p = os.path.join(run, "xmp", f"{int(cam):05d}.xmp")
    if not os.path.exists(p):
        miss += 1; continue
    shutil.copy2(p, os.path.join(out, os.path.splitext(img)[0] + ".xmp")); made += 1

total = {r[0] for r in allrows}
inmain = {r[0] for r in aligned}
notin = sorted(total - inmain)
with open(f"{dst}/poses/unaligned.txt", "w") as fh:
    fh.write("# Images not in the main aligned component.\n")
    fh.write("# Some failed to align; some solved into small orphan components in their own\n")
    fh.write("# coordinate frames, which cannot be merged with the main one.\n")
    fh.write("\n".join(notin) + "\n")
print(f"  wrote {made} poses (missing {miss}), {len(notin)} images not in main component")

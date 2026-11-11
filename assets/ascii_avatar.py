#!/usr/bin/env python3
"""
Builds assets/avatar3d.svg: a spinning 3D ASCII version of your GitHub avatar,
drawn with the letters of your handle.

Default: uses the built-in 5x5 grid (reconstructed from a screenshot of the avatar).
Exact:   python ascii_avatar.py --fetch ard12115
         (downloads your real avatar, reads it as a 5x5 identicon grid, needs: pip install pillow)
Options: --word ARD12115  --frames 48  --out ../assets/avatar3d.svg
"""
import argparse, io, math, urllib.request

# 1 = coloured cube, 0 = empty (5x5 identicon, mirrored left/right)
DEFAULT_GRID = [
    "00100",
    "00100",
    "01110",
    "10101",
    "01010",
]

def grid_from_avatar(user):
    from PIL import Image
    url = f"https://github.com/{user}.png?size=250"
    img = Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=20).read())).convert("RGB")
    w, h = img.size
    bg = img.getpixel((2, 2))                       # identicon background (corner)
    cell = w / 7.0                                  # identicons have a 1-cell margin
    rows = []
    for r in range(5):
        row = ""
        for c in range(5):
            px = img.getpixel((int((c + 1.5) * cell), int((r + 1.5) * cell)))
            diff = sum(abs(a - b) for a, b in zip(px, bg))
            row += "1" if diff > 60 else "0"
        rows.append(row)
    return rows

# ---------- tiny 3D engine: ray-cast boxes, orthographic, ASCII output ----------
def boxes_from_grid(grid):
    cubes = []
    for r, line in enumerate(grid):
        for c, v in enumerate(line):
            if v == "1":
                cubes.append(((c - 2.5, 1.5 - r, -1.15 + 0.475), (c - 1.5, 2.5 - r, -0.15 + 0.475)))
    plate = ((-2.7, -2.7, -0.15 + 0.475), (2.7, 2.7, 0.2 + 0.475))
    return plate, cubes

def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def rot_y(t):
    c, s = math.cos(t), math.sin(t); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
def rot_x(t):
    c, s = math.cos(t), math.sin(t); return [[1, 0, 0], [0, c, -s], [0, s, c]]
def transpose(m): return [[m[j][i] for j in range(3)] for i in range(3)]
def apply(m, v): return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))

def hit_box(o, d, bmin, bmax):
    tmin, tmax, axis, sgn = -1e9, 1e9, -1, 1
    for a in range(3):
        if abs(d[a]) < 1e-9:
            if o[a] < bmin[a] or o[a] > bmax[a]: return None
            continue
        t1 = (bmin[a] - o[a]) / d[a]; t2 = (bmax[a] - o[a]) / d[a]
        lo, hi = (t1, t2) if t1 < t2 else (t2, t1)
        if lo > tmin: tmin, axis, sgn = lo, a, (-1 if d[a] > 0 else 1)
        tmax = min(tmax, hi)
        if tmin > tmax: return None
    if tmax <= 0: return None
    return tmin, axis, sgn

def render_frame(plate, cubes, theta, cols, rows, word):
    R = mat_mul(rot_x(-0.38), rot_y(theta))          # object -> world
    Rt = transpose(R)
    d = apply(Rt, (0, 0, 1))
    L = (-0.5, 0.7, -0.6); n = math.sqrt(sum(x * x for x in L)); L = tuple(x / n for x in L)
    sx = 6.4 / cols; sy = 2 * sx
    layers = {k: [[" "] * cols for _ in range(rows)] for k in ("plate", "dark", "mid", "bright")}
    for rr in range(rows):
        for cc in range(cols):
            px = (cc + 0.5 - cols / 2) * sx
            py = (rows / 2 - (rr + 0.5)) * sy
            o = apply(Rt, (px, py, -30))
            best = None
            for box, kind in [(plate, "plate")] + [(b, "cube") for b in cubes]:
                h = hit_box(o, d, *box)
                if h and (best is None or h[0] < best[0]):
                    best = (h[0], h[1], h[2], kind)
            if not best: continue
            t, axis, sgn, kind = best
            nrm = [0, 0, 0]; nrm[axis] = sgn
            nw = apply(R, nrm)
            b = max(0.0, sum(a * c for a, c in zip(nw, L))) * 0.85 + 0.15
            if kind == "plate":
                layers["plate"][rr][cc] = "." if b < 0.6 else ","
                continue
            hit = tuple(o[i] + d[i] * t for i in range(3))
            idx = (int(math.floor((hit[0] + 3) * 5)) + 3 * int(math.floor((hit[1] + 3) * 2)) +
                   int(math.floor((hit[2] + 2) * 4))) % len(word)
            layer = "dark" if b < 0.4 else ("mid" if b < 0.7 else "bright")
            layers[layer][rr][cc] = word[idx]
    return layers

def build_svg(grid, word, frames, cols=56, rows=28):
    plate, cubes = boxes_from_grid(grid)
    fs = 13; cw = fs * 0.6; lh = cw * 2
    W = cols * cw + 40; H = rows * lh + 70
    colors = {"plate": "#334155", "dark": "#0f766e", "mid": "#2dd4bf", "bright": "#d1fae5"}
    dur = 8.0
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Spinning 3D ASCII avatar of {word}">',
           f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#0d2236"/></linearGradient></defs>',
           f'<rect width="{W:.0f}" height="{H:.0f}" rx="18" fill="url(#bg)"/>',
           f'<rect x=".5" y=".5" width="{W-1:.0f}" height="{H-1:.0f}" rx="18" fill="none" stroke="#38bdf8" stroke-opacity=".35"/>',
           f'<g font-family="\'SFMono-Regular\',Consolas,Menlo,\'Liberation Mono\',monospace" font-size="{fs}" style="white-space:pre">']
    for f in range(frames):
        theta = 2 * math.pi * f / frames
        layers = render_frame(plate, cubes, theta, cols, rows, word)
        if f == 0:
            out.append("<!-- frame 0 preview -->")
        if f == 0 or True:
            pass
        if f == 0:
            kt, vals = "0;" + f"{1/frames:.5f}", "visible;hidden"
        elif f == frames - 1:
            kt, vals = "0;" + f"{f/frames:.5f}", "hidden;visible"
        else:
            kt, vals = f"0;{f/frames:.5f};{(f+1)/frames:.5f}", "hidden;visible;hidden"
        out.append(f'<g visibility="hidden"><animate attributeName="visibility" dur="{dur}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>')
        for name in ("plate", "dark", "mid", "bright"):
            lines = ["".join(r).rstrip() for r in layers[name]]
            if not any(lines): continue
            ts = "".join(f'<tspan x="20" y="{44 + i * lh:.1f}">{ln}</tspan>' for i, ln in enumerate(lines) if ln)
            out.append(f'<text xml:space="preserve" fill="{colors[name]}">{ts}</text>')
        out.append("</g>")
    out.append("</g>")
    cap_y = H - 22
    out.append(f'<text x="{W/2:.0f}" y="{H-34:.0f}" text-anchor="middle" font-family="monospace" font-size="12" fill="#64748b">rendering @{word.lower()}</text>')
    out.append(f'<text x="{W/2:.0f}" y="{cap_y:.0f}" text-anchor="middle" font-family="monospace" font-size="13" fill="#7dd3fc">&gt; spin --axis y --ascii<tspan>_<animate attributeName="opacity" values="1;1;0;0;1" dur="0.9s" repeatCount="indefinite"/></tspan></text>')
    out.append("</svg>")
    return "\n".join(out), render_frame(plate, cubes, math.radians(20), cols, rows, word)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch"); ap.add_argument("--word", default="ARD12115")
    ap.add_argument("--frames", type=int, default=48); ap.add_argument("--out", default="../assets/avatar3d.svg")
    a = ap.parse_args()
    grid = grid_from_avatar(a.fetch) if a.fetch else DEFAULT_GRID
    print("grid:", grid)
    svg, prev = build_svg(grid, a.word, a.frames)
    open(a.out, "w", encoding="utf-8").write(svg)
    print("wrote", a.out, f"{len(svg)/1024:.0f} KB")
    # terminal preview of one frame
    h = len(prev["plate"])
    for r in range(h):
        print("".join(next((prev[k][r][c] for k in ("bright", "mid", "dark", "plate") if prev[k][r][c] != " "), " ") for c in range(len(prev["plate"][0]))))

#!/usr/bin/env python3
"""Cybercore asset generator for the ard12115 profile README.

Regenerates assets/header.svg, divider.svg, languages.svg and footer.svg
with a cybercore palette (near-black void, neon cyan / magenta / violet /
lime, scanlines, glitch text, perspective grid).

Usage:  python3 tools/build_assets.py
"""
import os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ---------------------------------------------------------------- palette
VOID = "#04040a"        # deep background
PANEL = "#0a0a16"       # panel fill
CYAN = "#00f0ff"
MAGENTA = "#ff2bd6"
VIOLET = "#8b5cf6"
LIME = "#39ff14"
AMBER = "#ffb000"
INK = "#e6faff"         # near-white text
DIM = "#5b6b8c"         # muted labels

MONO = "'SFMono-Regular',Consolas,Menlo,'Liberation Mono',monospace"

# GitHub linguist colors (fallback to cyber accents)
LANG_COLORS = {
    "HTML": CYAN, "Python": LIME, "GDScript": VIOLET, "JavaScript": AMBER,
    "TypeScript": MAGENTA, "C++": "#61caff", "CSS": "#7dd3fc",
}

# Repository-weighted bytes, fetched live from the GitHub API on 2026-11-15
# (public, non-fork repos of ARD12115).
LANG_BYTES = {
    "HTML": 890636, "Python": 702345, "GDScript": 615461, "JavaScript": 319130,
    "TypeScript": 251841, "C++": 78051, "CSS": 77625, "Other": 53291,
}


def pct_str(name):
    total = sum(LANG_BYTES.values())
    return round(100 * LANG_BYTES[name] / total)


def defs_shell(w, h, extra=""):
    """Shared background: void gradient + neon glows + scanlines."""
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VOID}"><animate attributeName="stop-color" values="{VOID};#0a0418;#04101a;{VOID}" dur="14s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="#0b0616"><animate attributeName="stop-color" values="#0b0616;#04101a;#12041c;#0b0616" dur="14s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <radialGradient id="glowC" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowM" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".22"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></radialGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{CYAN}" opacity=".05"/></pattern>
  <filter id="neon" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  {extra}
</defs>"""


def frame(w, h):
    """Neon border with animated corner brackets."""
    c = 16
    corners = [
        f'<path d="M2,{c+2} L2,6 Q2,2 6,2 L{c+2},2" stroke="{CYAN}"/>',
        f'<path d="M{w-c-2},2 L{w-6},2 Q{w-2},2 {w-2},6 L{w-2},{c+2}" stroke="{MAGENTA}"/>',
        f'<path d="M2,{h-c-2} L2,{h-6} Q2,{h-2} 6,{h-2} L{c+2},{h-2}" stroke="{MAGENTA}"/>',
        f'<path d="M{w-c-2},{h-2} L{w-6},{h-2} Q{w-2},{h-2} {w-2},{h-6} L{w-2},{h-c-2}" stroke="{CYAN}"/>',
    ]
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" '
            f'stroke="{VIOLET}" stroke-opacity=".4"/>'
            + '<g fill="none" stroke-width="2">' + "".join(corners) + "</g>")


def svg_doc(w, h, label, body):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + body + "</svg>")
    ET.fromstring(doc)  # fail fast if malformed
    return doc


# ---------------------------------------------------------------- header
def build_header():
    w, h = 960, 260
    taglines = ["full-stack · ai · game dev",
                "build useful things, learn in public",
                "python · typescript · c++ · cuda"]
    anims, texts = [], []
    for i, t in enumerate(taglines):
        anims.append(
            f'<clipPath id="c{i}"><rect x="58" y="140" width="0" height="34">'
            f'<animate attributeName="width" values="0;{len(t)*13};{len(t)*13};0" keyTimes="0;0.12;0.9;1" dur="18s" begin="{i*6}s" repeatCount="indefinite"/></rect></clipPath>')
        texts.append(f'<text x="60" y="168" font-family="{MONO}" font-size="22" fill="{CYAN}" clip-path="url(#c{i})">{t}<tspan fill="{INK}">_</tspan></text>')
    body = f"""
{defs_shell(w, h)}
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <ellipse cx="790" cy="60" rx="260" ry="140" fill="url(#glowM)"/>
  <ellipse cx="120" cy="230" rx="300" ry="120" fill="url(#glowC)"/>
  <g stroke="{CYAN}" stroke-opacity=".08"><line x1="0" y1="200" x2="960" y2="180"/><line x1="0" y1="220" x2="960" y2="196"/><line x1="0" y1="240" x2="960" y2="212"/><line x1="0" y1="260" x2="960" y2="228"/><line x1="80" y1="260" x2="240" y2="176"/><line x1="240" y1="260" x2="360" y2="176"/><line x1="400" y1="260" x2="480" y2="176"/><line x1="560" y1="260" x2="600" y2="176"/><line x1="720" y1="260" x2="720" y2="176"/><line x1="880" y1="260" x2="840" y2="176"/></g>
  <text x="60" y="86" font-family="{MONO}" font-size="13" fill="{DIM}">// SYSTEM.ONLINE — USER.PROFILE</text>
  <text x="60" y="118" font-family="'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif" font-size="52" font-weight="700" fill="{INK}" filter="url(#neon)">Abhinav Ravindra<tspan fill="{CYAN}">_</tspan></text>
  <text x="62" y="120" font-family="'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif" font-size="52" font-weight="700" fill="{MAGENTA}" opacity="0">Abhinav Ravindra<animate attributeName="opacity" values="0;0;.5;0;0;.35;0" keyTimes="0;.55;.56;.58;.9;.92;1" dur="7s" repeatCount="indefinite"/></text>
  {''.join(texts)}
  <text x="60" y="210" font-family="{MONO}" font-size="12" fill="{LIME}">&gt; boot_sequence: ok   &gt; gpu: linked   &gt; net: synced</text>
  <rect width="{w}" height="{h}" fill="url(#scan)"/>
</g>
{frame(w, h)}
<defs>{''.join(anims)}</defs>"""
    return svg_doc(w, h, "Abhinav Ravindra - Full-stack, AI, Game dev (cybercore header)", body)


# ---------------------------------------------------------------- divider
def build_divider():
    w, h = 960, 24
    body = f"""
<defs>
  <linearGradient id="l" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".35" stop-color="{CYAN}"/><stop offset=".65" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-.5 0;.5 0;-.5 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="g" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect x="40" y="11" width="880" height="2" rx="1" fill="url(#l)" opacity=".8"/>
<circle r="5" cy="12" fill="{CYAN}" filter="url(#g)"><animate attributeName="cx" values="40;920;40" dur="6s" repeatCount="indefinite"/></circle>
<circle r="2.5" cy="12" fill="#ffffff"><animate attributeName="cx" values="40;920;40" dur="6s" repeatCount="indefinite"/></circle>
<circle r="3" cy="12" fill="{MAGENTA}" filter="url(#g)"><animate attributeName="cx" values="920;40;920" dur="6s" repeatCount="indefinite"/></circle>
<rect x="450" y="8" width="60" height="8" rx="2" fill="{VOID}" stroke="{VIOLET}" stroke-opacity=".5"/>
<text x="480" y="15" text-anchor="middle" font-family="{MONO}" font-size="7" fill="{DIM}">SYS.OK</text>"""
    return svg_doc(w, h, "cybercore section divider", body)


# ---------------------------------------------------------------- languages
def build_languages():
    w, h = 960, 270
    rows = []
    max_pct = pct_str("HTML")
    names = [k for k in LANG_BYTES if k != "Other"] + ["Other"]
    y = 78
    for name in names:
        p = pct_str(name)
        bw = int(560 * p / max_pct)
        color = LANG_COLORS.get(name, DIM)
        rows.append(f"""  <text x="40" y="{y+13}" font-family="{MONO}" font-size="14" fill="{INK}">{name}</text>
  <rect x="150" y="{y}" width="560" height="16" rx="8" fill="{PANEL}" stroke="{color}" stroke-opacity=".25"/>
  <rect x="150" y="{y}" width="0" height="16" rx="8" fill="{color}" filter="url(#neon)">
    <animate attributeName="width" values="0;{bw};{bw};0" keyTimes="0;0.18;0.92;1" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1;.4 0 1 1"/>
  </rect>
  <text x="726" y="{y+13}" font-family="{MONO}" font-size="14" fill="{color}">{p}%</text>""")
        y += 36
    label = "Language mix across my repositories: " + ", ".join(
        f"{n} {pct_str(n)}%" for n in names)
    body = f"""
{defs_shell(w, h)}
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <ellipse cx="880" cy="240" rx="240" ry="120" fill="url(#glowC)"/>
  <text x="40" y="44" font-family="{MONO}" font-size="16" font-weight="700" fill="{LIME}">&gt; stack.scan --all-repos</text>
  <text x="290" y="44" font-family="{MONO}" font-size="16" fill="{LIME}">_<animate attributeName="opacity" values="1;1;0;0;1" dur="0.9s" repeatCount="indefinite"/></text>
  <text x="40" y="62" font-family="{MONO}" font-size="11" fill="{DIM}">repository-weighted languages · byte totals from GitHub API</text>
{''.join(rows)}
  <rect width="{w}" height="{h}" fill="url(#scan)"/>
</g>
{frame(w, h)}"""
    return svg_doc(w, h, label, body)


# ---------------------------------------------------------------- footer
def build_footer():
    w, h = 960, 140
    bars = []
    heights = [18, 34, 26, 44, 30, 52, 38, 24, 46, 32, 20, 40, 28, 50, 36, 22, 42, 30, 18, 34]
    for i, bh in enumerate(heights):
        x = 60 + i * 44
        color = [CYAN, MAGENTA, VIOLET, LIME][i % 4]
        nbh = max(10, bh // 2)
        dur = f"{1 + (i % 5) * 0.2:.1f}s"
        bars.append(
            f'<rect x="{x}" y="{110-bh}" width="8" height="{bh}" rx="2" fill="{color}" opacity=".7">'
            f'<animate attributeName="height" values="{bh};{nbh};{bh}" dur="{dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{110-bh};{110-nbh};{110-bh}" dur="{dur}" repeatCount="indefinite"/></rect>')
    body = f"""
{defs_shell(w, h)}
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <g stroke="{VIOLET}" stroke-opacity=".12"><line x1="0" y1="112" x2="960" y2="112"/><line x1="0" y1="124" x2="960" y2="124"/><line x1="0" y1="140" x2="960" y2="136"/></g>
  {''.join(bars)}
  <text x="480" y="40" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{CYAN}" filter="url(#neon)">[ connection maintained · signal strong · keep building ]</text>
  <text x="480" y="64" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}">ard12115@cybercore:~$ exit --to=next-build</text>
  <rect width="{w}" height="{h}" fill="url(#scan)"/>
</g>
{frame(w, h)}"""
    return svg_doc(w, h, "cybercore footer with equalizer", body)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    jobs = {"header.svg": build_header(), "divider.svg": build_divider(),
            "languages.svg": build_languages(), "footer.svg": build_footer()}
    for fname, content in jobs.items():
        path = os.path.join(ASSETS, fname)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"wrote {path} ({len(content)} bytes)")


if __name__ == "__main__":
    main()

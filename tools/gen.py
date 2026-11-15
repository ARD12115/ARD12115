import textwrap
from xml.sax.saxutils import escape as X
W=900
BG,SURF,LINE,TXT,DIM,CY,IN,EM='#080a0f','#0f172a','#1e293b','#e8ecf4','#8e95a5','#4cd7f6','#6366f1','#10b981'
M="Consolas,'JetBrains Mono',Menlo,monospace"; S="'Segoe UI',Inter,Arial,sans-serif"
def head(h,extra='',W=W):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<defs><pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#131a28" stroke-width=".6"/></pattern>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{IN}"/></linearGradient>{extra}</defs>
<rect width="{W}" height="{h}" fill="{BG}"/><rect width="{W}" height="{h}" fill="url(#g)"/>
'''
def t(x,y,s,fill=TXT,size=11,font=M,w='400',ls=0,anchor='start',extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-family="{font}" font-weight="{w}" letter-spacing="{ls}" text-anchor="{anchor}" {extra}>{X(s)}</text>\n'
def box(x,y,w,h,fill=SURF,stroke='#334155',op=.55):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-opacity="{op}"/>\n'
def led(x,y,c=EM,dur=2):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{c}"><animate attributeName="opacity" values="1;.25;1" dur="{dur}s" repeatCount="indefinite"/></circle>\n'
def section(y,n,title,right=''):
    s=t(30,y,f'SECTION {n}',CY,10,ls=1.5)+t(120,y,title.upper(),TXT,13,S,'700',.5)
    if right: s+=t(870,y,right,DIM,9,ls=1,anchor='end')
    return s+f'<line x1="30" y1="{y+12}" x2="870" y2="{y+12}" stroke="{LINE}"/>\n'

# ---------- HEADER ----------
def header():
    h=430; o=head(h)
    o+=box(0,0,W,40,'#0a0d14',LINE,1)
    o+=led(30,20)+t(42,24,'REF: SPEC-2026.04',TXT,10,w='600')+t(150,24,'| SYS_CORE // ARD12115',DIM,10)
    for i,(n,a) in enumerate([('00. OVERVIEW',1),('01. VECTORS',0),('02. REPOSITORIES',0),('03. RUNTIME',0),('04. DISPATCH',0)]):
        x=395+[0,92,172,282,362][i]
        o+=t(x,24,n,TXT if a else DIM,9)
    o+=f'<rect x="395" y="37" width="82" height="2" fill="{CY}"/>'
    o+=t(870,24,'STATUS: ONLINE (NOMINAL)',EM,9,anchor='end')
    o+=t(30,66,'SPEC DOC: ENG-SYS-PROFILE-26',DIM,9)+t(290,66,'ID: ard12115',CY,9)+t(470,66,'STANDARD: DIN / ISO-9241 TECHNICAL',DIM,9)+t(870,66,'REVISION: v4.0.8 [LOCKED]',EM,9,anchor='end')
    o+=f'<line x1="30" y1="76" x2="870" y2="76" stroke="{LINE}"/>'
    o+=f'<rect x="30" y="102" width="6" height="6" fill="{EM}"/>'+t(44,109,'ENGINEERING DOSSIER & SPECIFICATION SHEET',EM,9,ls=1.5)
    o+=t(30,166,'ABHINAV',TXT,58,S,'300',-2)+t(30,224,'RAVINDRA',TXT,58,S,'800',-2)
    o+=t(30,252,'//',IN,12)+t(52,252,'SYSTEMS ARCHITECT & FULL-STACK ENGINEER',CY,11,w='600',ls=1.5)
    for i,l in enumerate(['Specialized in low-overhead distributed systems, hardware-adjacent graphics runtimes,','deep learning computer vision architectures, and resilient event-driven data streaming.']):
        o+=t(30,278+i*17,l,DIM,12,S)
    o+=t(30,322,'"Build useful things, learn in public." — Core Principle [SPEC 0x01]',DIM,10,extra='font-style="italic"')
    # buttons
    o+=box(30,340,150,30,'#fff','#fff',1)+t(105,359,'INSPECT SPECIFICATIONS ↓',BG,9,w='700',anchor='middle')
    o+=box(190,340,110,30,BG,'#334155')+t(245,359,'DIRECT DISPATCH',TXT,9,anchor='middle')
    o+=box(310,340,120,30,BG,'#334155',.3)+t(370,359,'EXPORT RAW MARKDOWN',DIM,8,anchor='middle')
    # viewport panel
    px,py,pw,ph=500,96,370,250
    o+=box(px,py,pw,ph,'#05070b','#334155')
    o+=t(px+10,py+16,'FIG 1.0: VOLUMETRIC SCENE MATRIX',CY,8,ls=1)+t(px+pw-10,py+16,'60.0 FPS LOCKED',EM,8,anchor='end')
    o+=t(px+10,py+34,'ORIGIN: [0.00, 0.00, 0.00]',DIM,7)+t(px+10,py+44,'FOV: 45°  //  RAD: 1.60m',DIM,7)
    cx,cy=px+pw/2,py+ph/2+6
    # grid lines
    o+=f'<g stroke="{LINE}" stroke-dasharray="2 4"><line x1="{px}" y1="{cy}" x2="{px+pw}" y2="{cy}"/><line x1="{cx}" y1="{py}" x2="{cx}" y2="{py+ph}"/></g>'
    o+=f'<g transform="translate({cx},{cy})" fill="none" stroke-width="1.1">'
    o+=f'<circle r="92" stroke="{EM}" stroke-opacity=".6" stroke-dasharray="3 8"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="30s" repeatCount="indefinite"/></circle>'
    o+=f'<ellipse rx="86" ry="26" stroke="{CY}" stroke-opacity=".7"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></ellipse>'
    o+=f'<ellipse rx="26" ry="86" stroke="{EM}" stroke-opacity=".6"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/></ellipse>'
    o+=f'<polygon points="0,-70 61,-35 61,35 0,70 -61,35 -61,-35" stroke="{IN}" stroke-opacity=".75"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/></polygon>'
    o+=f'<polygon points="0,-44 38,-22 38,22 0,44 -38,22 -38,-22" stroke="{CY}"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="14s" repeatCount="indefinite"/></polygon>'
    import math,random; random.seed(7)
    for i in range(34):
        a=random.random()*6.28; r=60+random.random()*40; d=random.choice([10,14,18,24]); c=random.choice([CY,IN,EM])
        o+=f'<circle r="1.6" fill="{c}" stroke="none" cx="{r:.0f}" cy="0"><animateTransform attributeName="transform" type="rotate" from="{a*57:.0f}" to="{a*57+360:.0f}" dur="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.3;1" dur="{2+i%3}s" repeatCount="indefinite"/></circle>'
    o+='</g>'
    o+=t(cx,cy-2,'ARD12115',CY,15,w='700',anchor='middle')+t(cx,cy+13,'~/runtime: OK',EM,9,anchor='middle')
    o+=t(px+10,py+ph-8,'INTERACTION: AUTO ORBIT',CY,7)+t(px+pw-10,py+ph-8,'BUFFER: SHADER_PASS_04',DIM,7,anchor='end')
    o+=f'<rect x="{px+1}" y="{py+20}" width="{pw-2}" height="1.5" fill="{CY}" opacity=".25"><animate attributeName="y" values="{py+20};{py+ph-6};{py+20}" dur="5s" repeatCount="indefinite"/></rect>'
    # stat strip
    stats=[('SYSTEM ROLE','Full-Stack Core',TXT),('PRIMARY DOMAIN','AI · Cloud · Graphics',TXT),('LATENCY AVERAGE','12.0 ms',EM),('SYSTEM AVAILABILITY','99.98% SLA',EM),('CORE LANGUAGE ENGINE','Py · TS · C++ · GD',CY),('AUDITED REPOSITORIES','9 AUDITED SPECS',CY)]
    cw=840/6
    for i,(a,b,c) in enumerate(stats):
        x=30+i*cw
        o+=box(x,388,cw,38,BG,LINE,1)+t(x+8,402,a,DIM,6.5,ls=.8)+t(x+8,418,b,c,10.5,w='600')
    return o+'</svg>'

# ---------- VECTORS ----------
def vectors():
    h=250; o=head(h)+section(30,'01.0','Architectural Vectors & Engineering Disciplines','[ISO DOMAIN TAXONOMY // 3 VECTORS]')
    cards=[('VEC_VISION.AI','STABLE',EM,'AI & COMPUTER VISION',['Medical imaging reconstruction, anatomical ROI','segmentation, deep residual transfer models','(ResNet18), and persistent multi-agent LLM','orchestrators with state graphs.'],'FRAMEWORKS','PyTorch · TorchVision · OpenCV','TARGETS','ResNet · UNet · Autoencoders'),
    ('VEC_DIST.FLOW','STABLE',EM,'DISTRIBUTED SYSTEMS & CLOUD',['Strict Postgres atomic transactional outboxes,','high-throughput Apache Kafka streaming,','OpenSearch fuzzy indexing layers, and low-','overhead WebSocket pipelines.'],'INFRASTRUCTURE','Kafka · PostgreSQL · Redis','CONCURRENCY','ACID Isolation, 0% Outbox Loss'),
    ('VEC_LOW.GRAPH','ACTIVE',IN,'GAME TECH & LOW-LEVEL GRAPHICS',['Custom GLSL/GDShader graphics pipelines,','algorithmic terrain generation, CUDA GPU','hashing memory caches, and emulator','microsecond translation pacing.'],'PIPELINE','Godot 4 · C++ · GLSL · CUDA','FRAME LATENCY','16.1ms Fixed (60Hz Locked)')]
    cw=280
    for i,(id_,st,sc,ti,ds,l1,v1,l2,v2) in enumerate(cards):
        x=30+i*(cw+0)
        o+=box(x,56,cw-4,176,SURF,'#334155',.4)+f'<rect x="{x}" y="56" width="{cw-4}" height="2" fill="{[CY,CY,IN][i]}"><animate attributeName="opacity" values=".4;1;.4" dur="3s" begin="{i*.6}s" repeatCount="indefinite"/></rect>'
        o+=t(x+12,76,f'VECTOR 0{i+1} // {id_}',DIM,7.5,ls=.8)+t(x+cw-16,76,st,sc,8,w='600',anchor='end')
        o+=t(x+12,100,ti,TXT,12.5,S,'700')
        for j,l in enumerate(ds): o+=t(x+12,120+j*13,l,DIM,10,S)
        o+=f'<line x1="{x+12}" y1="180" x2="{x+cw-16}" y2="180" stroke="{LINE}"/>'
        o+=t(x+12,196,l1,DIM,7.5,ls=1)+t(x+12,208,v1,TXT,9)+t(x+12,222,l2,DIM,7.5,ls=1)
        o+=t(x+100 if False else x+12+len(l2)*5.6,222,'',TXT)  # spacer
        o+=t(x+cw-16,222,v2,CY if i<2 else EM,8,anchor='end')
    return o+'</svg>'

# ---------- REPOS ----------
R=[('SPEC_01','PulseCart','DISTRIBUTED STOREFRONT','Postgres strict inventory locks, Transactional Outbox publishing state events to Apache Kafka, and OpenSearch for fuzzy querying with race-condition checkout mitigation.','TS · Kafka · Postgres · Next.js','OUTBOX LOSS','0.00%',1.0),
('SPEC_02','ReliefNet','DISASTER LOGISTICS','Dynamic resource allocation calculating optimal relief dispatch routes via Open Source Routing Machine (OSRM) with bi-directional socket telemetry.','React · Node.js · Mongo · Socket.IO','DISPATCH SPEED','< 18.0 ms',.82),
('SPEC_03','MedhaDrishti','MRI NEURAL ENHANCE','Brain and spine MRI reconstruction with deep convolutional autoencoders and ResNet18 transfer learning; automated ROI segmentation for lesion & edema demarcation.','Python · PyTorch · OpenCV','DICE SCORE','0.932 DSC',.93),
('SPEC_04',"Anuvada","AWARD WINNER '26",'Kannada ↔ English multimodal pipeline for text, voice, and real-world signboards via optical character recognition and acoustic synthesis.','Python · Tesseract · Streamlit','OCR ACCURACY','96.4%',.96),
('SPEC_05','SkillMatch','SEMANTIC RESUME PARSER','Automated engineering resume matching engine with multidimensional vector embeddings, cosine distance scoring, and missing qualification attribution.','Python · NLP · Embeddings','COSINE ACCURACY','0.910 SIM',.91),
('SPEC_06','JARVIS-Assistant','MULTI-LLM DAEMON','Autonomous desktop assistant coordinating multiple local and remote LLM models, duplex audio stream synthesis, and shell tool routing.','Python · Rust · React · TS','ROUTER DIVERSITY','4 MODELS',.7),
('SPEC_07','Recircle','EDGE CV / DIGITAL TWIN','Edge-device real-time recyclable waste classifier linked to an interactive spatial 3D campus digital twin and grounded material-handling AI.','Python · Vision · GenAI','EDGE INFERENCE','42.0 FPS',.75),
('SPEC_08','GR-racer','ARCADE PHYSICS ENGINE','2000s arcade vehicular simulator in Godot 4: algorithmic road generation, custom rigid-body collision math, and GLSL shading pipelines for low-power hardware.','Godot 4 · GDScript · GLSL','FRAME PACING','16.1 ms (60Hz)',.9),
('SPEC_09','XeniaShaderOpt','CUDA ACCELERATION CORE','Xenia Canary emulator subsystem: pre-compiled shader caching, CUDA-assisted pipeline hashing, microsecond frame pacing, and low-drift audio sync loops.','C++ · CUDA · Python','STUTTER REDUCTION','-74.2%',.74)]
def repos():
    rh=62; h=96+len(R)*rh+10; o=head(h)+section(30,'02.0','Production Repositories & Engineering Specifications','[9 VERIFIED SYSTEMS]')
    o+=t(30,56,'Standardized itemized catalog of verified operational software systems.',DIM,10,S)
    o+=box(30,66,840,22,'#0a0d14',LINE,1)
    for x,l in [(40,'SPEC ID'),(110,'SYSTEM NAME'),(250,'TECHNICAL SUMMARY & ARCHITECTURE'),(640,'STACK'),(760,'BENCHMARK')]: o+=t(x,81,l,DIM,7.5,ls=1)
    for i,(sid,n,tag,sm,stk,ml,mv,pct) in enumerate(R):
        y=96+i*rh
        o+=f'<line x1="30" y1="{y+rh-1}" x2="870" y2="{y+rh-1}" stroke="{LINE}"/>'
        o+=t(40,y+22,sid,CY,10,w='700')+t(110,y+22,n,TXT,12,S,'700')+t(110,y+36,tag,DIM,6.5,ls=.8)
        for j,l in enumerate(textwrap.wrap(sm,66)[:3]): o+=t(250,y+17+j*12,l,DIM,9,S)
        for j,l in enumerate(stk.replace(' · ',' · ').split(' · ')): pass
        w=textwrap.wrap(stk,18)
        for j,l in enumerate(w[:3]): o+=t(640,y+20+j*12,l,TXT,8.5)
        o+=t(760,y+17,ml,DIM,6.5,ls=.8)+t(868,y+17,mv,EM,9,w='700',anchor='end')
        o+=box(760,y+26,108,5,'#05070b',LINE,1)+f'<rect x="760" y="{y+26}" height="5" fill="url(#bar)"><animate attributeName="width" from="0" to="{108*pct:.0f}" dur="1.4s" begin="{i*.15}s" fill="freeze"/></rect>'
    return o+'</svg>'

# ---------- LANGUAGES ----------
def langs():
    h=250; o=head(h)+section(30,'03.0','System Runtime & Language Composition','[AUDITED REPOSITORY COMMIT VOLUME]')
    o+=t(30,62,'STATIC CODE VOLUME ALLOCATION',DIM,8,ls=1)+t(870,62,'100.0% AGGREGATE',TXT,9,w='700',anchor='end')
    L=[('HTML / UI',30,'Semantic Web Core','#a5b4fc'),('PYTHON',24,'PyTorch · ML Pipelines',EM),('GDSCRIPT',21,'Godot 4 Mechanics',CY),('JAVASCRIPT',11,'Client Runtime',IN),('TYPESCRIPT',8,'Type-safe Services','#38bdf8'),('C++ / CUDA',3,'Hardware Kernels','#94a3b8')]
    x=30
    for i,(n,p,d,c) in enumerate(L):
        w=8.4*p
        o+=f'<rect x="{x}" y="72" height="14" fill="{c}"><animate attributeName="width" from="0" to="{w-2:.0f}" dur="1.2s" begin="{i*.12}s" fill="freeze"/></rect>'
        o+=t(x,108,n,DIM,7,ls=.6)+t(x,124,f'{p:.1f}%',c,15,w='700')+t(x,138,d,c,7.5)
        x+=w
    eco=[('FRONTEND ECOSYSTEM','React, Next.js, Vite, Tailwind CSS,','shadcn/ui'),('AI / VISION ECOSYSTEM','PyTorch, OpenCV, ResNet18,','LLM Tooling'),('DATA & INFRASTRUCTURE','PostgreSQL, Apache Kafka,','OpenSearch, Docker'),('GRAPHICS & ENGINE','Godot 4, GLSL / GDShader,','CUDA, Linux')]
    for i,(a,b,c) in enumerate(eco):
        x=30+i*210
        o+=f'<line x1="{x}" y1="168" x2="{x+196}" y2="168" stroke="{LINE}"/>'+t(x,186,a,DIM,7,ls=.8)+t(x,204,b,TXT,9.5)+t(x,217,c,TXT,9.5)
    return o+'</svg>'

# ---------- TERMINAL ----------
def terminal():
    h=300; o=head(h)+section(30,'04.0','Protocol & Dispatch Terminal','[COMMUNICATION CHANNEL READY]')
    o+=box(30,50,840,120,'#05070b','#334155')+led(46,66)+t(58,70,'SHELL: ard12115@syscore.net',EM,9,w='600')
    lines=[('ard12115@syscore:~$ ./dispatch --collaborate --target="abhinav"',CY),('[HANDSHAKE] Handshake established with Abhinav Ravindra.',DIM),('[OK] Active vectors: AI & Vision, Distributed Kafka Pipelines, Godot 4 Physics.',EM),('> Selected communication protocols available below:',TXT)]
    for i,(l,c) in enumerate(lines):
        o+=t(46,96+i*19,l,c,10,extra=f'opacity="0"')[:-1].replace('opacity="0"','opacity="0"')
        o=o.rstrip('\n'); o=o[:o.rfind('opacity="0">')]+f'opacity="0">{X(l)}<animate attributeName="opacity" from="0" to="1" dur="0.01s" begin="{.8+i*1.0}s" fill="freeze"/></text>\n'
    o+=f'<rect x="46" y="158" width="7" height="2" fill="{CY}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
    P=[('PROTOCOL 01','GitHub Registry','Browse 9 public production','repositories and commit history.','@ard12115',CY),('PROTOCOL 02','Direct Dispatch','Send engineering inquiries or','collaboration proposals.','contact@yourmail.dev',IN),('PROTOCOL 03','Export Profile Spec','Raw Markdown technical spec','sheet of this profile.','PROFILE_SPECS.md',EM)]
    for i,(a,b,c,d,e,col) in enumerate(P):
        x=30+i*282
        o+=box(x,186,276,96,SURF,'#334155',.4)+f'<rect x="{x}" y="186" width="2" height="96" fill="{col}"/>'
        o+=t(x+14,204,a,DIM,7.5,ls=1)+t(x+14,224,b,TXT,13,S,'700')+t(x+14,243,c,DIM,10,S)+t(x+14,256,d,DIM,10,S)+t(x+14,273,e,col,9)
    return o+'</svg>'

# ---------- FOOTER ----------
def footer():
    h=70; o=head(h)+t(30,26,'ABHINAV RAVINDRA // TECHNICAL PORTFOLIO',TXT,11,w='700')+t(30,42,'International typographic spec sheet layout. No telemetry tracking cookies deployed.',DIM,9,S)
    o+=t(870,26,'CORE CLOCKS: 4.8 GHz   BANDWIDTH: 2.4 GB/s   FAILURES: 0 DETECTED',DIM,8,anchor='end')+t(870,56,'DIN 1451 // SWISS SPEC FORMAT // 2026 EDITION',DIM,7.5,anchor='end')
    return o+'</svg>'
for n,f in [('header',header),('vectors',vectors),('repos',repos),('languages',langs),('terminal',terminal),('footer',footer)]:
    open(f'{n}.svg','w').write(f())


def _hdr_all():
    return header()
def topbar():
    o=head(86)
    full=header()
    import re
    body=full.split('<rect width="900" height="430" fill="url(#g)"/>\n',1)[1]
    # keep only the first lines up to the divider at y=76
    cut=body.split('<line x1="30" y1="76"',1)[0]+'<line x1="30" y1="76" x2="870" y2="76" stroke="#1e293b"/>'
    return o+cut+'</svg>'
def heroleft():
    H=307; o=head(H,W=490).replace('width="900"','width="490"').replace('viewBox="0 0 900','viewBox="0 0 490')
    o=o.replace('<rect width="900"','<rect width="490"')
    full=header().split('<rect width="900" height="430" fill="url(#g)"/>\n',1)[1]
    a=full.index('<rect x="30" y="102"'); b=full.index('<rect x="500"') if '<rect x="500"' in full else full.index(t(500,0,'')[:0]+'<rect x="500"')
    # panel starts with box(px,py..) -> find via 'FIG 1.0' backtrack
    b=full.rfind('<rect x="500"',0,full.index('FIG 1.0'))
    return o+'<g transform="translate(0,-92)">'+full[a:b]+'</g></svg>'
def stats():
    o=head(52)
    full=header()
    a=full.rfind('<rect',0,full.index('y="388"')); body=full[a:full.rindex('</svg>')]
    return o+'<g transform="translate(0,-380)">'+body+'</g></svg>'
for n,f in [('topbar',topbar),('heroleft',heroleft),('stats',stats)]:
    open(f'{n}.svg','w').write(f())

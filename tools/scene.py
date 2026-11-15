import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFont, ImageChops
Wp,Hp=360,263; SS=2; N=300
w,h=Wp*SS,Hp*SS
BG=(5,7,11)
f=(h/2)/math.tan(math.radians(22.5)); CAMZ=28
random.seed(12115); np.random.seed(12115)
def hexc(s): return tuple(int(s[i:i+2],16) for i in (1,3,5))
cyan,indigo,emer=hexc('#38bdf8'),hexc('#6366f1'),hexc('#10b981')
# particles
P=[];C=[]
for _ in range(750):
    th=random.uniform(-180,180); ph=random.uniform(-180,180); r=6.8+random.random()*2.2
    P.append((r*math.sin(th)*math.cos(ph),r*math.sin(th)*math.sin(ph),r*math.cos(th)))
    if random.random()>.5:
        k=random.random(); a=[cyan[i]*(1-k)+indigo[i]*k for i in range(3)]
    else: a=emer
    C.append(a)
P=np.array(P);C=np.array(C)
# icosahedron detail=1 edges
g=(1+5**.5)/2
V=[(-1,g,0),(1,g,0),(-1,-g,0),(1,-g,0),(0,-1,g),(0,1,g),(0,-1,-g),(0,1,-g),(g,0,-1),(g,0,1),(-g,0,-1),(-g,0,1)]
F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
V=[np.array(v,float)/np.linalg.norm(v) for v in V]
verts=list(V);cache={}
def mid(a,b):
    k=(min(a,b),max(a,b))
    if k not in cache:
        m=verts[a]+verts[b]; verts.append(m/np.linalg.norm(m)); cache[k]=len(verts)-1
    return cache[k]
edges=set()
for a,b,c in F:
    ab,bc,ca=mid(a,b),mid(b,c),mid(c,a)
    for tri in [(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)]:
        for i in range(3):
            p,q=tri[i],tri[(i+1)%3]; edges.add((min(p,q),max(p,q)))
verts=np.array(verts)*7.5; edges=list(edges)
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def proj(X):
    d=CAMZ-X[:,2]; return np.stack([w/2+f*X[:,0]/d, h/2-f*X[:,1]/d],1), d
phi=np.linspace(0,2*math.pi,101)
ring=np.stack([8.8*np.cos(phi),8.8*np.sin(phi),0*phi],1)
try: fb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',1); FP='/usr/share/fonts/truetype/dejavu/DejaVuSansMono'
except: FP=None
def font(sz,bold=False):
    return ImageFont.truetype(FP+('-Bold' if bold else '')+'.ttf',int(sz))
# text billboard
tex=Image.new('RGBA',(512,512),(0,0,0,0)); d=ImageDraw.Draw(tex)
def ctext(y,s,fnt,col): d.text((256,y),s,font=fnt,fill=col+(255,),anchor='mm')
ctext(210,'ARD12115',font(58,True),cyan);ctext(275,'~/runtime: OK',font(24),emer);ctext(320,'01000001 01010010',font(24),hexc('#a5b4fc'))
side=int(8*f/CAMZ); tex=tex.resize((side,side),Image.LANCZOS)
def frame(k):
    t=k/N
    gm=Rx(2*math.pi*t)@Ry(4*math.pi*t)
    lay_l=Image.new('RGB',(w,h),(0,0,0)); dl=ImageDraw.Draw(lay_l)
    # wireframe
    X=verts@gm.T; S,_=proj(X)
    col=tuple(int(c*.45) for c in indigo)
    for a,b in edges: dl.line([tuple(S[a]),tuple(S[b])],fill=col,width=SS)
    # rings
    for rm,cc in [(Rx(math.pi/3)@Rz(2*math.pi*t),(56,189,248)),(Ry(math.pi/3)@Rz(-2*math.pi*t),emer)]:
        X=(ring@rm.T)@gm.T; S,_=proj(X); dl.line([tuple(p) for p in S],fill=tuple(int(c*.65) for c in cc),width=SS*2)
    # particles (additive squares)
    lay_p=Image.new('RGB',(w,h),(0,0,0)); dp=ImageDraw.Draw(lay_p)
    X=P@gm.T; S,dep=proj(X); order=np.argsort(-dep)
    for i in order:
        sz=0.38*(h/2)/dep[i]; x,y=S[i]
        dp.rectangle([x-sz/2,y-sz/2,x+sz/2,y+sz/2],fill=tuple(int(c*.88) for c in C[i]))
    img=ImageChops.add(ImageChops.add(Image.new('RGB',(w,h),BG),lay_l),lay_p)
    img.paste(tex,(w//2-side//2,h//2-side//2),tex)
    return img.resize((Wp,Hp),Image.LANCZOS)
frames=[frame(k) for k in range(N)]

def fnt(sz,b=False):
    return ImageFont.truetype(FP+('-Bold' if b else '')+'.ttf',sz)
def compose(im):
    TH=22; out=Image.new('RGB',(Wp,Hp+2*TH),(8,10,15)); out.paste(im,(0,TH)); d=ImageDraw.Draw(out)
    d.rectangle([0,0,Wp-1,Hp+2*TH-1],outline=(40,50,68))
    d.line([(0,TH),(Wp,TH)],fill=(30,37,51)); d.line([(0,TH+Hp),(Wp,TH+Hp)],fill=(30,37,51))
    d.rectangle([8,8,13,13],fill=(76,215,246)); d.text((20,11),'FIG 1.0: VOLUMETRIC SCENE MATRIX',font=fnt(9),fill=(232,236,244),anchor='lm')
    d.text((Wp-8,11),'60.0 FPS LOCKED',font=fnt(9),fill=(76,215,246),anchor='rm')
    d.text((8,TH+10),'ORIGIN: [0.00, 0.00, 0.00]',font=fnt(8),fill=(144,143,160),anchor='lm'); d.text((8,TH+21),'FOV: 45° // RAD: 1.62m',font=fnt(8),fill=(144,143,160),anchor='lm')
    d.text((Wp-8,TH+Hp-20),'BUFFER: SHADER_PASS_OK',font=fnt(8),fill=(78,222,163),anchor='rm'); d.text((Wp-8,TH+Hp-9),'GEO_SEED: 0x415244',font=fnt(8),fill=(78,222,163),anchor='rm')
    d.text((8,TH+Hp+11),'INTERACTION: AUTO ORBIT',font=fnt(9),fill=(232,236,244),anchor='lm'); d.text((Wp-8,TH+Hp+11),'[PROJECTION: ORTHO-SYM]',font=fnt(9),fill=(30,37,51),anchor='rm')
    for x,y,dx,dy,c in [(0,0,1,1,(76,215,246)),(Wp-1,0,-1,1,(76,215,246)),(0,Hp+2*TH-1,1,-1,(78,222,163)),(Wp-1,Hp+2*TH-1,-1,-1,(78,222,163))]:
        d.line([(x,y),(x+8*dx,y)],fill=c,width=2); d.line([(x,y),(x,y+8*dy)],fill=c,width=2)
    return out
frames=[compose(f) for f in frames]
pal=frames[0].quantize(colors=32,method=Image.MEDIANCUT)
q=[im.quantize(palette=pal,dither=Image.NONE) for im in frames]
q[0].save('scene.gif',save_all=True,append_images=q[1:],duration=40,loop=0,optimize=True,disposal=1)
frames[60].save('preview.png')

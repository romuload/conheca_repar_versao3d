# Gera a maquete 3D detalhada da REPAR (fluxograma "Conheça a REPAR") no Blender 5.x
# Executar no Blender:  exec(open(r"C:\Users\romul\Documents\REPAR_maquete_3D\gerar_maquete_repar.py", encoding="utf-8").read())
import bpy, bmesh, math, random, json, os
from mathutils import Matrix, Vector

PASTA = r"C:\Users\romul\Documents\REPAR_maquete_3D"
pi = math.pi

# ------------------------------------------------------------------ limpar
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    for d in list(coll): coll.remove(d)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
scene = bpy.context.scene
root = bpy.data.collections.new("REPAR"); scene.collection.children.link(root)
def newcol(n):
    c = bpy.data.collections.new(n); root.children.link(c); return c
C_ENV = newcol("Ambiente"); C_UNITS = newcol("Unidades"); C_PIPES = newcol("Tubulacoes"); C_LIGHTS = newcol("Luzes")

# ------------------------------------------------------------------ materiais
def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    return tuple(((x+0.055)/1.055)**2.4 if x > 0.04045 else x/12.92 for x in c)
MATS = {}
def M(name, hexc, metal=0.0, rough=0.6, emit=0.0, alpha=1.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hexc), 1)
    b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if emit > 0:
        b.inputs["Emission Color"].default_value = (*lin(hexc), 1); b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    m.diffuse_color = (*lin(hexc), 1); MATS[name] = m; return m

steel  = M("aco_claro", "#dfe3e8", 0.65, 0.32)
steel2 = M("aco_escuro", "#7b8794", 0.7, 0.4)
steel3 = M("aco_estrutura", "#5c6773", 0.6, 0.5)
galv   = M("galvanizado", "#a9b2bc", 0.8, 0.35)
white  = M("tanque_branco", "#f1f3f5", 0.1, 0.4)
concrete = M("concreto", "#a3abb4", 0, 0.9)
slab   = M("piso_unidade", "#59636d", 0, 0.85)
grat   = M("grade_piso", "#3f4750", 0.5, 0.6)
ground = M("gramado", "#2f5a2f", 0, 1)
sand   = M("areia", "#b9a77f", 0, 1)
water  = M("agua", "#174669", 0.1, 0.05)
road   = M("asfalto_via", "#24292f", 0, 0.9)
walk   = M("calcada", "#7d858d", 0, 0.9)
paint_w = M("faixa_branca", "#e8e8e8", 0, 0.6)
glow   = M("brilho_forno", "#ff8a2a", 0, 0.5, 12)
red    = M("vermelho", "#c8352e", 0, 0.55)
yellow = M("amarelo_seg", "#f2b705", 0, 0.5)
green  = M("verde_seg", "#1f8a4c", 0, 0.5)
treem  = M("conifera", "#2b5f31", 0, 0.9)
treem2 = M("folhosa", "#3c7a37", 0, 0.9)
treem3 = M("arbusto", "#4d8a3a", 0, 0.9)
trunk  = M("tronco", "#5a3d2b", 0, 0.9)
dark   = M("grafite", "#353b42", 0.3, 0.6)
hullm  = M("casco", "#8a2420", 0.2, 0.55)
deckm  = M("convés", "#4f6b4f", 0.1, 0.7)
refr   = M("refratario", "#8a5a44", 0, 0.8)
darktank = M("tanque_escuro", "#4a4f57", 0.3, 0.5)
brick  = M("tijolo", "#7a4032", 0, 0.85)
glass  = M("vidro", "#3d6b8c", 0.3, 0.08)
winlit = M("janela_acesa", "#ffd9a0", 0, 0.4, 6)
lamp_w = M("luz_quente", "#ffc978", 0, 0.3, 40)
lamp_c = M("luz_fria", "#d8ecff", 0, 0.3, 30)
lamp_r = M("luz_aviso", "#ff2a1a", 0, 0.3, 40)
rubber = M("pneu", "#1b1d20", 0, 0.9)
pilem  = M("material_granel", "#1e1f22", 0, 1)
car_cols = [M("carro_"+h, "#"+h, 0.5, 0.3) for h in ("c0392b", "2e86de", "dfe6e9", "2d3436", "f39c12")]

STREAMS = {"petroleo":"#ff5a1f","rat":"#a16207","gasoleo":"#f59e0b","residuo_vac":"#7c3a12","odes":"#fda4af",
 "craqueado":"#cbd5e1","glp":"#22c55e","nafta_leve":"#fde047","nafta_pesada":"#14b8a6","querosene":"#a855f7",
 "diesel":"#3b82f6","gasolina":"#facc15","qav":"#c084fc","solvente":"#22d3ee","oleo_comb":"#ef4444","rasf":"#94a3b8"}
PIPE_M = {k: M("fluxo_"+k, v, 0.2, 0.35, 3.0) for k, v in STREAMS.items()}
BAND_M = {k: M("faixa_"+k, v, 0.1, 0.4, 0.6) for k, v in STREAMS.items()}

# ------------------------------------------------------------------ construtor de malhas
class B:
    def __init__(s): s.bm = bmesh.new(); s.mats = []
    def _mi(s, m):
        if m not in s.mats: s.mats.append(m)
        return s.mats.index(m)
    def _set(s, verts, m, smooth=False):
        mi = s._mi(m); fs = set()
        for v in verts:
            for f in v.link_faces: fs.add(f)
        for f in fs: f.material_index = mi; f.smooth = smooth and len(f.verts) <= 4
    def cyl(s, x, y, z0, h, r, m, seg=24, r2=None, smooth=True):
        r2 = r if r2 is None else r2
        ret = bmesh.ops.create_cone(s.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r2, depth=h,
                                    matrix=Matrix.Translation((x, y, z0+h/2)))
        s._set(ret['verts'], m, smooth)
    def box(s, x, y, z0, sx, sy, sz, m, rot=0):
        mat = Matrix.Translation((x, y, z0+sz/2)) @ Matrix.Rotation(rot, 4, 'Z') @ Matrix.Diagonal((sx, sy, sz, 1))
        ret = bmesh.ops.create_cube(s.bm, size=1, matrix=mat); s._set(ret['verts'], m)
    def sph(s, x, y, z, r, m, seg=24):
        ret = bmesh.ops.create_uvsphere(s.bm, u_segments=seg, v_segments=max(4, seg//2), radius=r,
                                        matrix=Matrix.Translation((x, y, z)))
        s._set(ret['verts'], m, True)
    def seg(s, p0, p1, r, m, n=8, smooth=True):
        p0 = Vector(p0); p1 = Vector(p1); d = p1-p0; L = d.length
        if L < 1e-4: return
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        mat = Matrix.Translation((p0+p1)/2) @ q.to_matrix().to_4x4()
        ret = bmesh.ops.create_cone(s.bm, cap_ends=True, cap_tris=False, segments=n, radius1=r, radius2=r, depth=L, matrix=mat)
        s._set(ret['verts'], m, smooth)
    def bar(s, p0, p1, w, m):          # barra de seção quadrada entre dois pontos
        s.seg(p0, p1, w*0.7, m, n=4, smooth=False)
    def poly(s, pts, r, m, n=8, joints=True):
        for i in range(len(pts)-1): s.seg(pts[i], pts[i+1], r, m, n)
        if joints:
            for p in pts[1:-1]: s.sph(p[0], p[1], p[2], r*1.02, m, seg=8)
    def hcyl(s, x, y, z, L, r, m, seg=20, axis='X'):
        if axis == 'X': s.seg((x-L/2, y, z), (x+L/2, y, z), r, m, seg)
        else: s.seg((x, y-L/2, z), (x, y+L/2, z), r, m, seg)
    def torus(s, x, y, z, R, r, m, seg=32, tseg=5, smooth=True):
        vs = []
        for i in range(seg):
            a = 2*pi*i/seg; ca, sa = math.cos(a), math.sin(a)
            for j in range(tseg):
                b = 2*pi*j/tseg; rr = R+r*math.cos(b)
                vs.append(s.bm.verts.new((x+rr*ca, y+rr*sa, z+r*math.sin(b))))
        for i in range(seg):
            for j in range(tseg):
                a = vs[i*tseg+j]; b = vs[((i+1) % seg)*tseg+j]; c = vs[((i+1) % seg)*tseg+(j+1) % tseg]; d = vs[i*tseg+(j+1) % tseg]
                s.bm.faces.new((a, b, c, d))
        s._set(vs, m, smooth)
    def prism(s, outline, z0, z1, m):  # contorno 2D extrudado
        bot = [s.bm.verts.new((x, y, z0)) for x, y in outline]
        top = [s.bm.verts.new((x, y, z1)) for x, y in outline]
        s.bm.faces.new(list(reversed(bot))); s.bm.faces.new(top)
        n = len(outline)
        for i in range(n): s.bm.faces.new((bot[i], bot[(i+1) % n], top[(i+1) % n], top[i]))
        s._set(bot+top, m)
    def build(s, name, coll, loc=(0, 0, 0), rot=0, parent=None, props=None):
        me = bpy.data.meshes.new(name); s.bm.to_mesh(me); s.bm.free()
        for m in s.mats: me.materials.append(m)
        o = bpy.data.objects.new(name, me); coll.objects.link(o)
        if parent: o.parent = parent
        o.location = loc; o.rotation_euler = (0, 0, rot)
        for k, v in (props or {}).items(): o[k] = v
        return o

# ------------------------------------------------------------------ detalhes reutilizáveis
def railing_ring(b, x, y, z, R, posts=True):
    b.torus(x, y, z+1.0, R, 0.045, galv, seg=40, tseg=4)
    b.torus(x, y, z+0.5, R, 0.035, galv, seg=40, tseg=4)
    if posts:
        n = max(8, int(2*pi*R/1.2))
        for i in range(n):
            a = 2*pi*i/n; b.box(x+R*math.cos(a), y+R*math.sin(a), z, 0.06, 0.06, 1.0, galv)

def platform_ring(b, x, y, z, r, w=1.1, lights=3):
    b.cyl(x, y, z, 0.14, r+w, grat, seg=40, smooth=False)
    railing_ring(b, x, y, z+0.14, r+w-0.05)
    for i in range(lights):
        a = 2*pi*i/lights+0.4
        b.sph(x+(r+w-0.15)*math.cos(a), y+(r+w-0.15)*math.sin(a), z+1.25, 0.09, lamp_w, seg=6)

def ladder_cage(b, x, y, z0, z1, ang, r):
    ux, uy = math.cos(ang), math.sin(ang); tx, ty = -uy, ux
    cx, cy = x+ux*(r+0.35), y+uy*(r+0.35)
    for sgn in (-1, 1): b.seg((cx+tx*0.25*sgn, cy+ty*0.25*sgn, z0), (cx+tx*0.25*sgn, cy+ty*0.25*sgn, z1), 0.035, galv, n=4)
    z = z0+2.4
    while z < z1:
        b.torus(cx+ux*0.35, cy+uy*0.35, z, 0.38, 0.025, galv, seg=10, tseg=3); z += 1.0
    for k in range(4):
        a = k*pi/2+pi/4
        b.seg((cx+ux*0.35+0.38*math.cos(a), cy+uy*0.35+0.38*math.sin(a), z0+2.4),
              (cx+ux*0.35+0.38*math.cos(a), cy+uy*0.35+0.38*math.sin(a), z1), 0.02, galv, n=3)

def nozzle(b, x, y, z, ang, r_shell, L=0.9, rn=0.18):
    ux, uy = math.cos(ang), math.sin(ang)
    p0 = (x+ux*r_shell*0.9, y+uy*r_shell*0.9, z); p1 = (x+ux*(r_shell+L), y+uy*(r_shell+L), z)
    b.seg(p0, p1, rn, steel2, n=10)
    b.seg((p1[0]-ux*0.06, p1[1]-uy*0.06, z), (p1[0]+ux*0.06, p1[1]+uy*0.06, z), rn*1.6, steel3, n=12)

def ext_pipe(b, x, y, r, z_top, ang, z_bot=1.2, rp=0.2, m=None):
    m = m or steel2; ux, uy = math.cos(ang), math.sin(ang); off = r+0.55
    pts = [(x, y, z_top+r*0.6), (x+ux*off, y+uy*off, z_top+r*0.6), (x+ux*off, y+uy*off, z_bot), (x+ux*(off+2.2), y+uy*(off+2.2), z_bot)]
    b.poly(pts, rp, m)

def tower(h, r, rings=4, ladder_ang=2.4, pipe_angs=(0.6, -2.0), band=None):
    b = B(); top = 0.8+h
    b.cyl(0, 0, 0, 0.8, r+0.35, concrete, seg=32)
    b.cyl(0, 0, 0.8, h, r, steel, seg=32); b.sph(0, 0, top, r*0.98, steel, seg=32)
    z = 2.0
    while z < top-0.5:                                # cintas de isolamento
        b.cyl(0, 0, z, 0.06, r+0.02, steel2, seg=32, smooth=False); z += 1.6
    for i in range(1, rings+1):
        platform_ring(b, 0, 0, 0.8+h*i/(rings+0.4), r)
    ladder_cage(b, 0, 0, 0.8, top-0.3, ladder_ang, r)
    for k, a in enumerate(pipe_angs): ext_pipe(b, 0, 0, r, top-1.0-k*1.5, a)
    for i in range(6): nozzle(b, 0, 0, 2.0+i*(h-2)/6, 0.3+i*1.1, r)
    b.seg((0, 0, top+r*0.9), (0, 0, top+r*0.9+1.4), 0.12, steel2, n=8)     # respiro
    b.sph(0, 0, top+r*0.9+1.5, 0.14, lamp_r, seg=6)                         # luz de balizamento
    b.seg((r*0.5, 0, top+r*0.6), (r*0.5, 0, top+r*0.6+2.2), 0.06, galv, n=4) # turco
    b.seg((r*0.5, 0, top+r*0.6+2.2), (r*0.5+1.4, 0, top+r*0.6+2.2), 0.05, galv, n=4)
    if band: b.cyl(0, 0, 1.2, 0.5, r+0.03, BAND_M[band], seg=32, smooth=False)
    return b

def vac_tower(h, r1, r2):
    b = B(); b.cyl(0, 0, 0, 0.8, r1+0.35, concrete, seg=32); hb = h*0.4; ht = h*0.45
    b.cyl(0, 0, 0.8, hb, r1, steel, seg=32); b.cyl(0, 0, 0.8+hb, 1.4, r1, steel, seg=32, r2=r2)
    b.cyl(0, 0, 2.2+hb, ht, r2, steel, seg=32); top = 2.2+hb+ht; b.sph(0, 0, top, r2*0.98, steel, seg=32)
    for z, rr in ((0.8+hb*0.55, r1), (2.2+hb+ht*0.35, r2), (2.2+hb+ht*0.75, r2)): platform_ring(b, 0, 0, z, rr)
    ladder_cage(b, 0, 0, 0.8, top-0.3, 2.6, r2)
    ext_pipe(b, 0, 0, r2, top-0.6, 0.0, rp=0.45)        # linha de topo larga para os ejetores
    for i in range(5): nozzle(b, 0, 0, 2.0+i*2.6, 0.8+i*1.2, r1 if i < 2 else r2)
    b.sph(0, 0, top+r2*0.95, 0.14, lamp_r, seg=6)
    return b

def furnace(w, d, hh, sh):
    b = B(); b.box(0, 0, 0, w+0.8, d+0.8, 0.4, concrete)
    b.box(0, 0, 0.4, w, d, hh, refr)
    n = int(w/0.9)
    for i in range(n+1):                             # nervuras
        x = -w/2+i*w/n
        for yy in (-d/2-0.05, d/2+0.05): b.box(x, yy, 0.4, 0.12, 0.12, hh, steel3)
    for yy in (-d/2-0.07, d/2+0.07):
        for i in range(n):                           # janelas dos queimadores
            b.box(-w/2+(i+0.5)*w/n, yy, 0.8, w/n*0.55, 0.06, 0.45, glow)
    b.box(0, 0, 0.4+hh, w*0.7, d*0.75, 1.6, steel2)
    b.box(0, 0, 2.0+hh, w*0.4, d*0.5, 0.8, steel3)
    b.cyl(0, 0, 2.8+hh, sh, 0.5, steel2, seg=20)
    b.cyl(0, 0, 2.8+hh+sh-1.4, 1.4, 0.53, red, seg=20); b.cyl(0, 0, 2.8+hh+sh-2.6, 0.6, 0.53, white, seg=20)
    platform_ring(b, 0, 0, 2.8+hh+sh*0.65, 0.5, w=0.9, lights=2)
    ladder_cage(b, 0, 0, 2.8+hh, 2.8+hh+sh*0.65, pi/2, 0.5)
    b.sph(0, 0, 2.8+hh+sh+0.2, 0.15, lamp_r, seg=6)
    for sgn in (-1, 1): b.box(sgn*(w/2+0.4), 0, 0.4, 0.5, d*0.6, hh+1.6, steel3)     # escadas laterais
    return b

def tank(r, h, band=None, m=None, bund=True):
    b = B(); m = m or white
    b.cyl(0, 0, 0, 0.35, r+0.4, concrete, seg=40)
    b.cyl(0, 0, 0.35, h, r, m, seg=40)
    b.cyl(0, 0, 0.35+h, 0.8, r+0.05, m, seg=40, r2=r*0.12)
    for z in (0.35+h*0.33, 0.35+h*0.66): b.cyl(0, 0, z, 0.08, r+0.04, steel2, seg=40, smooth=False)
    if band: b.cyl(0, 0, 0.35+h*0.78, 0.55, r+0.05, BAND_M[band], seg=40, smooth=False)
    railing_ring(b, 0, 0, 0.35+h+0.1, r-0.2)
    steps = 26; a0 = -0.6; a1 = a0+1.9               # escada helicoidal
    for i in range(steps):
        t = i/(steps-1); a = a0+(a1-a0)*t; z = 0.35+h*t
        b.box((r+0.45)*math.cos(a), (r+0.45)*math.sin(a), z, 0.9, 0.35, 0.08, grat, rot=a+pi/2)
        if i % 2 == 0: b.seg(((r+0.85)*math.cos(a), (r+0.85)*math.sin(a), z), ((r+0.85)*math.cos(a), (r+0.85)*math.sin(a), z+1.0), 0.03, galv, n=4)
    pts = [((r+0.85)*math.cos(a0+(a1-a0)*t), (r+0.85)*math.sin(a0+(a1-a0)*t), 1.35+h*t) for t in [i/8 for i in range(9)]]
    b.poly(pts, 0.035, galv, n=4, joints=False)
    for a in (pi*0.9, pi*1.3): nozzle(b, 0, 0, 0.9, a, r, L=1.4, rn=0.22)
    b.seg((r*0.7, 0, 0.35+h+0.4), (r*0.7, 0, 0.35+h+1.3), 0.15, steel2, n=8)
    if bund:
        R = r+3.0
        for sx, sy, ww, dd in ((0, R, 2*R+0.4, 0.4), (0, -R, 2*R+0.4, 0.4), (R, 0, 0.4, 2*R), (-R, 0, 0.4, 2*R)):
            b.box(sx, sy, 0, ww, dd, 0.9, concrete)
    return b

def gsphere(r):
    b = B(); zc = r+2.2; nl = 8
    for i in range(nl):
        a = i*2*pi/nl; px, py = math.cos(a)*r*0.92, math.sin(a)*r*0.92
        b.cyl(px, py, 0, 0.5, 0.45, concrete, seg=8, smooth=False)
        b.cyl(px, py, 0.5, zc-0.5, 0.22, steel3, seg=10)
        a2 = (i+1)*2*pi/nl; qx, qy = math.cos(a2)*r*0.92, math.sin(a2)*r*0.92
        b.seg((px, py, 0.8), (qx, qy, zc-0.4), 0.06, steel3, n=4); b.seg((qx, qy, 0.8), (px, py, zc-0.4), 0.06, steel3, n=4)
    b.sph(0, 0, zc, r, white, 40)
    b.torus(0, 0, zc, r+0.05, 0.12, steel2, seg=48, tseg=5)
    b.cyl(0, 0, zc+r-0.15, 0.15, 1.5, grat, seg=20, smooth=False); railing_ring(b, 0, 0, zc+r, 1.45)
    sx = r+2.5                                         # escada de acesso ao topo
    b.seg((sx, -0.5, 0), (0.9, -0.5, zc+r-0.1), 0.06, galv, n=4); b.seg((sx, 0.5, 0), (0.9, 0.5, zc+r-0.1), 0.06, galv, n=4)
    for t in [i/14 for i in range(15)]:
        x = sx+(0.9-sx)*t; z = (zc+r-0.1)*t; b.box(x, 0, z, 0.25, 1.0, 0.06, grat)
    b.seg((sx, -0.55, 1.0), (0.9, -0.55, zc+r+0.9), 0.03, galv, n=4); b.seg((sx, 0.55, 1.0), (0.9, 0.55, zc+r+0.9), 0.03, galv, n=4)
    b.seg((0, -r*0.5, zc-r*0.85), (0, -r*0.5-1.5, 1.0), 0.18, steel2)
    b.sph(0, 0, zc+r+1.2, 0.12, lamp_r, seg=6)
    return b

def steel_structure(b, x, y, sx, sy, levels, h, coolers=True, lights=True):
    lv = [h*(i+1)/levels for i in range(levels)]
    cols = [(x-sx/2, y-sy/2), (x+sx/2, y-sy/2), (x+sx/2, y+sy/2), (x-sx/2, y+sy/2)]
    for cx, cy in cols:
        b.box(cx, cy, 0, 0.5, 0.5, 0.25, concrete); b.box(cx, cy, 0.25, 0.28, 0.28, h, steel3)
    for z in lv:
        for i in range(4):
            p, q = cols[i], cols[(i+1) % 4]; b.bar((p[0], p[1], z), (q[0], q[1], z), 0.22, steel3)
        b.box(x, y, z-0.08, sx, sy, 0.08, grat)
        for i in range(4):
            p, q = cols[i], cols[(i+1) % 4]
            b.seg((p[0], p[1], z+1.0), (q[0], q[1], z+1.0), 0.035, yellow, n=4)
        if lights: b.sph(x+sx/2-0.2, y-sy/2+0.2, z+2.2, 0.1, lamp_w, seg=6)
    zz = [0]+lv
    for k in range(len(zz)-1):                        # contraventamento
        p, q = cols[0], cols[1]
        b.seg((p[0], p[1], zz[k]+0.3), (q[0], q[1], zz[k+1]-0.2), 0.05, steel3, n=4)
        p, q = cols[1], cols[2]
        b.seg((p[0], p[1], zz[k+1]-0.2), (q[0], q[1], zz[k]+0.3), 0.05, steel3, n=4)
        # escada em zigue-zague
        sxs = x-sx/2-0.7; y0 = y-sy/2+0.3 if k % 2 == 0 else y+sy/2-0.3; y1 = y+sy/2-0.3 if k % 2 == 0 else y-sy/2+0.3
        b.seg((sxs, y0, zz[k]), (sxs, y1, zz[k+1]), 0.08, yellow, n=4)
    if coolers: air_cooler(b, x, y, h, sx*0.95, sy*0.95)
    # vasos e trocadores nos andares
    if levels >= 2:
        b.hcyl(x, y, lv[0]+0.7, sx*0.7, 0.55, steel, axis='X')
        b.hcyl(x, y+sy*0.25, lv[1]+0.5, sx*0.5, 0.35, steel2, axis='X')

def air_cooler(b, x, y, z, sx, sy):
    b.box(x, y, z, sx, sy, 0.9, steel2)
    nf = max(2, int(sx/2.2))
    for i in range(nf):
        fx = x-sx/2+(i+0.5)*sx/nf
        for j in (-1, 1) if sy > 3.2 else (0,):
            fy = y+j*sy/4
            b.cyl(fx, fy, z+0.9, 0.35, min(sx/nf, sy/2)*0.42, steel3, seg=20, smooth=False)
            b.cyl(fx, fy, z+1.2, 0.05, 0.25, dark, seg=8, smooth=False)

def exchangers(b, x, y, n=3, L=4.0, r=0.45, rot_y=False):
    for i in range(n):
        yy = y+(i-(n-1)/2)*1.4
        for sxo in (-L*0.3, L*0.3): b.box(x+sxo, yy, 0, 0.4, 1.0, 0.8, concrete)
        b.hcyl(x, yy, 0.8+r, L, r, steel, axis='X')
        b.hcyl(x-L/2-0.25, yy, 0.8+r, 0.5, r*1.1, steel2, axis='X')
        b.cyl(x+L*0.2, yy, 0.8+r*1.8, 0.5, 0.12, steel2, seg=8)

def pump(b, x, y, rot=0):
    b.box(x, y, 0, 1.6, 0.7, 0.3, concrete)
    b.hcyl(x-0.25, y, 0.75, 0.8, 0.28, M("motor_azul", "#2f5d8a", 0.3, 0.5), axis='X')
    b.cyl(x+0.45, y, 0.3, 0.6, 0.25, steel2, seg=12)
    b.seg((x+0.45, y, 0.9), (x+0.45, y, 1.6), 0.1, steel2, n=8)

def street_light(b, x, y, ang):
    b.seg((x, y, 0), (x, y, 6), 0.08, steel3, n=6)
    ex, ey = x+math.cos(ang)*1.4, y+math.sin(ang)*1.4
    b.seg((x, y, 6), (ex, ey, 6.2), 0.05, steel3, n=4)
    b.box(ex, ey, 5.95, 0.6, 0.3, 0.15, dark); b.box(ex, ey, 5.88, 0.45, 0.2, 0.08, lamp_w)

def converter():
    b = B(); b.box(0, 0, 0, 11, 6.5, 0.6, concrete)
    # riser e vaso separador (reator)
    b.cyl(-3, 0, 0.6, 16, 0.75, steel, seg=24)
    b.cyl(-3, 0, 16.6, 5, 2.2, steel, seg=32); b.sph(-3, 0, 21.6, 2.2, steel, 32); b.sph(-3, 0, 16.6, 2.2, steel, 32)
    platform_ring(b, -3, 0, 16.0, 2.2); platform_ring(b, -3, 0, 21.0, 2.2, lights=2)
    # regenerador
    b.cyl(2.8, 0, 0.6, 2.6, 2.3, steel2, seg=32); b.sph(2.8, 0, 5.8, 3.0, steel, 32)
    b.cyl(2.8, 0, 5.8, 7.5, 3.0, steel, seg=32); b.sph(2.8, 0, 13.3, 3.0, steel, 32)
    platform_ring(b, 2.8, 0, 8.5, 3.0); platform_ring(b, 2.8, 0, 13.0, 3.0, lights=2)
    # standpipes de catalisador
    b.poly([(2.0, -1.2, 4.0), (-1.5, -1.0, 2.0), (-2.6, -0.6, 1.4)], 0.42, steel2)
    b.poly([(-2.4, 0.9, 17.5), (0.6, 1.0, 14.0), (1.8, 1.2, 11.5)], 0.42, steel2)
    b.poly([(2.8, 0, 16.2), (2.8, 0, 18.5), (6.5, 0, 18.5), (6.5, 0, 3.0)], 0.5, steel2)   # gases de combustão
    b.poly([(-3, 2.4, 22.5), (-3, 4.5, 22.5), (-3, 4.5, 2.0)], 0.6, steel2)               # linha de topo do reator
    ladder_cage(b, 2.8, 0, 0.6, 13.0, -pi/2, 3.0); ladder_cage(b, -3, 0, 0.6, 21.0, pi/2+0.4, 2.2)
    steel_structure(b, -3, -0.2, 4.5, 4.2, 3, 15.6, coolers=False)
    b.sph(-3, 0, 24.0, 0.15, lamp_r, seg=6); b.sph(2.8, 0, 16.4, 0.15, lamp_r, seg=6)
    return b

def building(sx, sy, sz, wall=None, rows=2, logo=False):
    b = B(); wall = wall or white
    b.box(0, 0, 0, sx, sy, sz, wall); b.box(0, 0, sz, sx+0.3, sy+0.3, 0.4, dark)
    for k in range(rows):
        z = 0.9+k*(sz-0.6)/rows
        for yy in (-sy/2-0.03, sy/2+0.03): b.box(0, yy, z, sx*0.86, 0.06, 0.6, winlit)
        for xx in (-sx/2-0.03, sx/2+0.03): b.box(xx, 0, z, 0.06, sy*0.8, 0.6, winlit)
    for i in range(int(sx/3)):
        b.box(-sx/2+1.5+i*3, 0, sz+0.4, 1.2, 1.0, 0.7, steel2)
    return b

def distrib(sx, sy, sz):
    b = building(sx, sy, sz, rows=1)
    for i in range(3): b.box(-sx/2+1.3+i*2.2, -sy/2-0.04, 0, 1.6, 0.08, 2.4, dark)    # docas
    b.box(0, -sy/2-1.2, 2.6, sx, 2.4, 0.12, steel2)
    b.box(-sx/2+0.9, -sy/2-0.06, sz-1.4, 1.2, 0.08, 1.0, green)
    return b

def posto(sx, sy, h=4.2):
    b = B(); b.box(0, 0, 0, sx, sy, 0.15, concrete)
    for px in (-sx/4, sx/4):
        b.box(px, 0, 0.15, 0.45, 0.45, h, steel2)
        b.box(px, 0, 0.15, 3.2, 0.9, 0.25, concrete)
        for k in (-1, 1): b.box(px+k*0.9, 0, 0.4, 0.55, 0.45, 1.4, white); b.box(px+k*0.9, -0.24, 1.2, 0.4, 0.03, 0.4, glass)
    b.box(0, 0, 0.15+h, sx, sy, 0.6, white)
    b.box(0, -sy/2-0.01, 0.15+h, sx, 0.08, 0.6, green); b.box(0, sy/2+0.01, 0.15+h, sx, 0.08, 0.6, green)
    b.box(0, -sy/2-0.02, 0.15+h+0.45, sx, 0.1, 0.15, yellow)
    for px in (-sx/3, 0, sx/3):
        for py in (-sy/4, sy/4): b.box(px, py, 0.15+h-0.05, 0.9, 0.5, 0.05, lamp_c)
    b.box(sx/2+3.0, 1.5, 0, 4.5, 3.5, 3.2, white); b.box(sx/2+3.0, -0.27, 0.4, 3.8, 0.06, 1.8, winlit)   # loja
    b.box(sx/2+3.0, 1.5, 3.2, 4.8, 3.8, 0.3, green)
    b.seg((-sx/2-1.5, -sy/2-1.5, 0), (-sx/2-1.5, -sy/2-1.5, 6.5), 0.15, steel2)       # totem
    b.box(-sx/2-1.5, -sy/2-1.5, 5.0, 1.8, 0.35, 2.0, green); b.box(-sx/2-1.5, -sy/2-1.7, 5.2, 1.4, 0.05, 1.5, lamp_c)
    return b

def wheels(b, xs, y_half, r=0.45, z=0.45):
    for x in xs:
        for sy in (-y_half, y_half): b.seg((x, sy-0.18, z), (x, sy+0.18, z), r, rubber, n=12)

def truck(cargo='tank'):
    b = B(); b.box(-0.6, 0, 0.55, 7.0, 1.4, 0.35, dark)
    b.box(3.0, 0, 0.55, 1.6, 2.2, 2.0, white); b.box(3.81, 0, 1.6, 0.04, 1.9, 0.8, glass)
    b.box(3.0, 0, 2.55, 1.4, 2.0, 0.3, white)
    for yy in (-1.05, 1.05): b.box(3.82, yy, 1.0, 0.05, 0.12, 0.12, lamp_c)
    wheels(b, (3.0, -1.6, -2.8), 0.95)
    if cargo == 'tank':
        b.hcyl(-1.0, 0, 2.0, 5.6, 1.05, white, axis='X')
        for xx in (-3.0, -1.0, 1.0): b.cyl(xx, 0, 2.95, 0.3, 0.3, steel2, seg=10)
    else:
        b.box(-1.0, 0, 0.9, 5.6, 2.2, 0.15, steel2)
        for i in range(7):
            for j in range(3): b.cyl(-3.5+i*0.8, -0.7+j*0.7, 1.05, 0.75, 0.27, M("botijao", "#5b8bd0", 0.3, 0.4), seg=10)
    return b

def car(col):
    b = B(); b.box(0, 0, 0.35, 4.2, 1.8, 0.75, col); b.box(-0.2, 0, 1.1, 2.3, 1.6, 0.6, glass)
    b.box(-0.2, 0, 1.68, 2.1, 1.5, 0.06, col)
    wheels(b, (1.35, -1.35), 0.82, r=0.36, z=0.36)
    for yy in (-0.6, 0.6): b.box(2.11, yy, 0.75, 0.04, 0.35, 0.15, lamp_c)
    return b

def ship():
    b = B(); L = 34; Wd = 5.8
    hull = [(-L/2, -Wd/2), (L/2-6, -Wd/2), (L/2, 0), (L/2-6, Wd/2), (-L/2, Wd/2)]
    b.prism(hull, -1.6, 0.4, hullm)
    inner = [(x*0.98, y*0.96) for x, y in hull]
    b.prism(inner, 0.4, 1.9, M("casco_preto", "#1f2328", 0.2, 0.6))
    b.prism([(x*0.97, y*0.93) for x, y in hull], 1.9, 2.0, deckm)
    b.box(-14, 0, 2.0, 4.0, 5.0, 5.0, white)                     # superestrutura
    for z in (2.8, 4.0, 5.2): b.box(-11.98, 0, z, 0.05, 4.4, 0.5, winlit)
    b.box(-14.5, 0, 7.0, 2.6, 5.6, 0.25, white)
    b.cyl(-15.5, 0, 7.0, 3.0, 0.8, M("chamine_navio", "#22313f", 0.2, 0.5), seg=16)
    b.cyl(-15.5, 0, 9.6, 0.4, 0.82, red, seg=16)
    b.seg((-14, 0, 7.2), (-14, 0, 10.5), 0.06, steel2, n=4); b.sph(-14, 0, 10.6, 0.12, lamp_w, seg=6)
    for yy in (-1.0, 0, 1.0): b.seg((-11, yy, 2.4), (12, yy, 2.4), 0.16, M("tubo_convés", "#7a8b5a", 0.3, 0.5), n=8)
    for xx in range(-9, 13, 4): b.box(xx, 0, 2.0, 0.2, 4.0, 0.4, steel2)
    b.box(0, 0, 2.0, 1.8, 5.0, 1.0, steel3)                       # manifold
    for sgn in (-1, 1):
        b.seg((0, sgn*1.5, 2.0), (0, sgn*1.5, 6.0), 0.12, yellow, n=6); b.seg((0, sgn*1.5, 6.0), (2.8, sgn*2.6, 5.0), 0.08, yellow, n=6)
    b.box(13.5, 0, 2.0, 2.5, 3.0, 1.0, white); b.seg((14, 0, 3.0), (14, 0, 7.0), 0.08, steel2, n=4)
    b.sph(14, 0, 7.1, 0.12, lamp_w, seg=6)
    return b

def buoy():
    b = B(); b.cyl(0, 0, -0.8, 1.3, 2.0, yellow, seg=24); b.cyl(0, 0, 0.5, 0.6, 1.2, red, seg=20)
    b.cyl(0, 0, 1.1, 1.5, 0.15, steel2, seg=8); b.sph(0, 0, 2.7, 0.18, lamp_w, seg=6)
    return b

def plane():
    """Avião comercial de corredor único (~23 m), asa baixa enflechada, motores sob as asas."""
    b = B(); Z = 3.2; R = 1.25
    faixa = M("faixa_aviao", "#1f4e8c", 0.2, 0.4)
    jan = M("janela_aviao", "#1b2a3a", 0.3, 0.15)
    vidro_cab = M("parabrisa", "#0f1b28", 0.6, 0.05)
    porta = M("porta_aviao", "#c9d1d8", 0.2, 0.4)
    def cyl_patch(x0, x1, p0, p1, m, k=1.006, nx=1, nph=2):
        vs = []
        for i in range(nx+1):
            x = x0+(x1-x0)*i/nx; row = []
            for j in range(nph+1):
                ph = math.radians(p0+(p1-p0)*j/nph)
                row.append(b.bm.verts.new((x, R*k*math.cos(ph), Z+R*k*math.sin(ph))))
            vs.append(row)
        for i in range(nx):
            for j in range(nph): b.bm.faces.new((vs[i][j], vs[i][j+1], vs[i+1][j+1], vs[i+1][j]))
        b._set([v for r in vs for v in r], m, True)
    def nose_patch(t0, t1, p0, p1, m, k=1.012, nt=4, nph=4):
        vs = []
        for i in range(nt+1):
            t = t0+(t1-t0)*i/nt; row = []
            for j in range(nph+1):
                ph = math.radians(p0+(p1-p0)*j/nph); rr = R*math.sin(t)*k
                row.append(b.bm.verts.new((6.5+2.6*math.cos(t)*k, rr*math.cos(ph), Z+rr*math.sin(ph))))
            vs.append(row)
        for i in range(nt):
            for j in range(nph): b.bm.faces.new((vs[i][j], vs[i][j+1], vs[i+1][j+1], vs[i+1][j]))
        b._set([v for r in vs for v in r], m, True)
    def loft(stations, m):
        # stations: lista de seções [(x_le, x_max, x_te, y, z, espessura)] -> perfil em losango
        rings = []
        for xl, xm, xt, y, z, th in stations:
            rings.append([b.bm.verts.new(p) for p in ((xl, y, z), (xm, y, z+th*0.6), (xt, y, z+th*0.05), (xm, y, z-th*0.4))])
        for r0, r1 in zip(rings, rings[1:]):
            for k in range(4): b.bm.faces.new((r0[k], r0[(k+1) % 4], r1[(k+1) % 4], r1[k]))
        b.bm.faces.new(rings[0]); b.bm.faces.new(list(reversed(rings[-1])))
        b._set([v for r in rings for v in r], m)
    def fin_shape(outline, thick, mat, m):
        bot = [b.bm.verts.new(mat @ Vector((x, h, -thick/2))) for x, h in outline]
        top = [b.bm.verts.new(mat @ Vector((x, h, thick/2))) for x, h in outline]
        b.bm.faces.new(list(reversed(bot))); b.bm.faces.new(top)
        n = len(outline)
        for i in range(n): b.bm.faces.new((bot[i], bot[(i+1) % n], top[(i+1) % n], top[i]))
        b._set(bot+top, m)
    ROT_X = Matrix.Rotation(pi/2, 4, 'X')
    # fuselagem, nariz e cone de cauda
    b.seg((-7.5, 0, Z), (6.5, 0, Z), R, white, n=40)
    ret = bmesh.ops.create_uvsphere(b.bm, u_segments=40, v_segments=20, radius=1.0, matrix=Matrix.Translation((6.5, 0, Z)) @ Matrix.Diagonal((2.6, R, R, 1)))
    b._set(ret['verts'], white, True)
    p0 = Vector((-7.5, 0, Z)); p1 = Vector((-13.4, 0, Z+0.6)); d = p1-p0
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    ret = bmesh.ops.create_cone(b.bm, cap_ends=True, cap_tris=False, segments=40, radius1=R, radius2=0.32, depth=d.length,
                                matrix=Matrix.Translation((p0+p1)/2) @ q.to_matrix().to_4x4())
    b._set(ret['verts'], white, True); b.sph(p1.x, 0, p1.z, 0.32, steel2, 12)
    # para-brisa: 4 painéis na curvatura do nariz, com colunas entre eles
    for a0, a1 in ((47, 66), (69, 88), (92, 111), (114, 133)):
        nose_patch(0.98, 1.2, a0, a1, vidro_cab, nt=3, nph=4)
    for a0, a1 in ((38, 46), (134, 142)): nose_patch(1.24, 1.4, a0, a1, vidro_cab, nt=2, nph=2)   # janelas laterais da cabine
    # faixa da pintura e janelas de passageiros
    for p0_, p1_ in ((-8, -2), (182, 188)): cyl_patch(-7.4, 6.45, p0_, p1_, faixa, nx=6)
    for i in range(19):
        x = 4.6-i*0.62
        cyl_patch(x-0.13, x+0.13, 14, 24, jan); cyl_patch(x-0.13, x+0.13, 156, 166, jan)
    for x0 in (5.25, -6.9):
        cyl_patch(x0, x0+0.75, -14, 34, porta, k=1.004, nph=4); cyl_patch(x0, x0+0.75, 146, 194, porta, k=1.004, nph=4)
    # carenagem da asa (barriga)
    ret = bmesh.ops.create_uvsphere(b.bm, u_segments=24, v_segments=12, radius=1.0, matrix=Matrix.Translation((-0.4, 0, Z-0.8)) @ Matrix.Diagonal((4.6, 1.25, 0.6, 1)))
    b._set(ret['verts'], white, True)
    # asas com enflechamento, afilamento e diedro + winglets
    for s in (1, -1):
        loft([(2.4, 0.9, -2.6, s*0.9, Z-0.85, 0.42), (0.1, -1.0, -3.6, s*4.6, Z-0.6, 0.3), (-4.2, -4.8, -5.8, s*11.5, Z-0.05, 0.12)], white)
        fin_shape([(-4.3, 0), (-5.8, 0), (-6.5, 1.5), (-5.9, 1.5)], 0.1, Matrix.Translation((0, s*11.5, Z-0.05)) @ ROT_X, white)
        b.sph(-4.4, s*11.55, Z, 0.1, M("luz_verde", "#30ff70", 0, 0.3, 40) if s > 0 else lamp_r, seg=6)
        # motor: nacele, entrada, fan, cone de exaustão e pilone
        y = s*4.6; zc = Z-1.65
        b.seg((-1.3, y, zc), (2.3, y, zc), 0.8, white, n=28)
        b.seg((2.25, y, zc), (2.45, y, zc), 0.84, steel, n=28)
        b.seg((2.38, y, zc), (2.47, y, zc), 0.66, dark, n=28); b.sph(2.42, y, zc, 0.2, steel2, 10)
        ret = bmesh.ops.create_cone(b.bm, cap_ends=True, cap_tris=False, segments=24, radius1=0.62, radius2=0.3, depth=1.0,
                                    matrix=Matrix.Translation((-1.8, y, zc)) @ Matrix.Rotation(-pi/2, 4, 'Y'))
        b._set(ret['verts'], steel2, True)
        b.box(0.2, y, zc+0.5, 2.4, 0.22, 0.45, white)
        # trem de pouso principal (2 rodas)
        b.seg((-1.0, s*2.7, Z-0.9), (-1.0, s*2.7, 0.55), 0.12, steel3, n=8)
        for dy in (-0.32, 0.32): b.seg((-1.0, s*2.7+dy-0.14, 0.5), (-1.0, s*2.7+dy+0.14, 0.5), 0.5, rubber, n=16)
    # estabilizadores horizontais e deriva
    for s in (1, -1):
        loft([(-10.4, -11.2, -12.8, s*0.5, Z+0.35, 0.22), (-12.7, -13.1, -13.9, s*4.7, Z+0.55, 0.08)], white)
    fin_shape([(-9.2, 0), (-12.7, 0), (-13.8, 5.0), (-12.3, 5.0)], 0.26, Matrix.Translation((0, 0, Z+0.75)) @ ROT_X, white)
    fin_shape([(-11.6, 3.2), (-13.4, 3.2), (-13.8, 5.0), (-12.3, 5.0)], 0.28, Matrix.Translation((0, 0, Z+0.75)) @ ROT_X, faixa)
    # trem do nariz
    b.seg((7.2, 0, Z-R+0.1), (7.2, 0, 0.5), 0.1, steel3, n=8)
    for dy in (-0.22, 0.22): b.seg((7.2, dy-0.12, 0.4), (7.2, dy+0.12, 0.4), 0.38, rubber, n=14)
    # luzes: farol anticolisão e luz de cauda
    b.sph(-1.0, 0, Z+R+0.08, 0.12, lamp_r, seg=6); b.sph(-1.0, 0, Z-R-0.08, 0.12, lamp_r, seg=6)
    b.sph(-13.75, 0, Z+0.62, 0.1, lamp_c, seg=6)
    bmesh.ops.scale(b.bm, vec=(0.8, 0.8, 0.8), verts=b.bm.verts)   # escala da maquete
    return b

def fert_plant():
    b = building(14, 6, 4, wall=brick, rows=1)
    for x in (-4.5, 0, 4.5):
        n = 8; h = 18; sg = h/n
        b.box(x, 1.0, 4.4, 2.4, 2.4, 0.4, concrete)
        for k in range(n):
            ra = 0.9*(1-0.28*k/n); rb = 0.9*(1-0.28*(k+1)/n)
            b.cyl(x, 1.0, 4.8+k*sg, sg, ra, red if (n-1-k) % 2 == 0 else white, seg=24, r2=rb)
        platform_ring(b, x, 1.0, 4.8+h*0.7, 0.75, w=0.6, lights=2)
        b.sph(x, 1.0, 4.8+h+0.25, 0.15, lamp_r, seg=6)
    for x in (-6, 6): b.cyl(x, -4.5, 0, 7, 1.4, white, seg=24); b.sph(x, -4.5, 7, 1.4, white, 20)   # silos
    return b

def shed_pile(sx, sy, sz):
    b = B(); b.box(0, 0, 0, sx, sy, 0.25, concrete)
    for i in range(5):
        x = -sx/2+0.3+i*(sx-0.6)/4
        for yy in (-sy/2+0.3, sy/2-0.3): b.box(x, yy, 0.25, 0.35, 0.35, sz, steel3)
        b.prism([(x-0.15, -sy/2-0.4), (x+0.15, -sy/2-0.4), (x+0.15, sy/2+0.4), (x-0.15, sy/2+0.4)], sz+0.25, sz+0.45, steel3)
    roof_l = [(-sx/2-0.3, -sy/2-0.5), (sx/2+0.3, -sy/2-0.5), (sx/2+0.3, 0), (-sx/2-0.3, 0)]
    b.prism(roof_l, sz+0.45, sz+0.6, M("telha", "#7f8c8d", 0.6, 0.4))
    b.prism([(-sx/2-0.3, 0), (sx/2+0.3, 0), (sx/2+0.3, sy/2+0.5), (-sx/2-0.3, sy/2+0.5)], sz+0.45, sz+0.6, M("telha", "#7f8c8d", 0.6, 0.4))
    b.cyl(0, 0, 0.25, sz*0.8, min(sx, sy)*0.42, pilem, seg=28, r2=0.3, smooth=False)
    b.seg((sx/2, 0, 1.0), (sx/2+6, 0, sz+1.5), 0.35, steel3, n=4)                  # correia transportadora
    return b

# ------------------------------------------------------------------ unidades
UNITS = [
 ("U01",1,"São Francisco","O petroleiro descarrega na monoboia. O petróleo vai ao tanque em São Francisco e segue pelo oleoduto OSPAR até a refinaria.",(-60,25),((-42,23),(14,22))),
 ("U02",2,"Destilação","O petróleo é aquecido na fornalha e separado na torre em GLP, nafta leve, nafta pesada, querosene, diesel e resíduo atmosférico (RAT).",(-19,22),((-19,22),(20,16))),
 ("U03",3,"Unidade a Vácuo","O RAT é reaquecido na fornalha e destilado a vácuo: sai gasóleo para o craqueamento e resíduo de vácuo para a desasfaltação.",(3,23),((3,23),(16,14))),
 ("U04",4,"Unidade de Craqueamento","O gasóleo e o óleo desasfaltado são quebrados no conversor catalítico. A fracionadora separa GLP e resíduo para óleo combustível.",(32,25),((32,25),(24,18))),
 ("U05",5,"GLP (gás de cozinha)","Recebe GLP da destilação e do craqueamento, armazena na esfera e envia à distribuidora.",(-33,1),((-33,1),(20,14))),
 ("U06",6,"Gasolina","Mistura nafta leve e nafta pesada para formar a gasolina A, enviada à distribuidora.",(-29,-21),((-29,-21),(20,16))),
 ("U07",7,"Diesel","O diesel pesado passa pela hidrodessulfurização. O diesel leve recebe nafta pesada e querosene e vira diesel para uso em motores.",(-13,-41),((-13,-41),(24,14))),
 ("U08",8,"Querosene","O querosene da destilação passa pela hidrodessulfurização e vira QAV-1 para uso em aeronaves.",(17,-42),((17,-42),(20,14))),
 ("U09",9,"Unidade de Desasfaltação","Separa o resíduo de vácuo em óleo desasfaltado (ODES), que volta ao craqueamento, e resíduo asfáltico.",(11,1),((11,1),(14,12))),
 ("U10",10,"Unidade de Solvente","Fraciona a nafta leve da destilação em nafta peróxida e solvente de borracha.",(38,-21),((38,-21),(16,14))),
 ("U11",11,"Fosfértil","Recebe resíduo para óleo combustível e resíduo asfáltico como matéria-prima para fertilizantes. Parte é armazenada em tanque.",(58,3),((58,3),(20,16))),
]
UOBJ = {}
for uid, num, nome, desc, c, pad in UNITS:
    e = bpy.data.objects.new(uid, None); C_UNITS.objects.link(e); e.location = (c[0], c[1], 0)
    e.empty_display_type = 'PLAIN_AXES'; e.empty_display_size = 3
    e["tipo"] = "unidade"; e["num"] = num; e["nome"] = nome; e["descricao"] = desc; UOBJ[uid] = e
    (px, py), (sx, sy) = pad; b = B(); b.box(0, 0, 0, sx, sy, 0.18, slab)
    b.box(0, -sy/2+0.15, 0.18, sx, 0.3, 0.04, yellow); b.box(0, sy/2-0.15, 0.18, sx, 0.3, 0.04, yellow)
    b.box(-sx/2+0.15, 0, 0.18, 0.3, sy, 0.04, yellow); b.box(sx/2-0.15, 0, 0.18, 0.3, sy, 0.04, yellow)
    for cx in (-sx/2-0.4, sx/2+0.4):                       # postes de iluminação nos cantos
        for cy in (-sy/2-0.4, sy/2+0.4): street_light(b, cx, cy, math.atan2(-cy, -cx))
    b.build(uid+"_piso", C_UNITS, loc=(px-c[0], py-c[1], 0), parent=e, props={"tipo": "piso", "unidade": uid})

def EQ(uid, slug, bld, x, y, rot, cat, nome, funcao, ent, sai):
    c = UOBJ[uid].location
    return bld.build(f"{uid}_{slug}", C_UNITS, loc=(x-c.x, y-c.y, 0.18), rot=rot, parent=UOBJ[uid],
        props={"tipo": "equipamento", "unidade": uid, "categoria": cat, "nome": nome, "funcao": funcao, "entradas": ent, "saidas": sai})

DET = {}
def det(uid):
    if uid not in DET: DET[uid] = B()
    return DET[uid]
def D(uid, x, y):            # coordenadas locais da unidade para detalhes
    c = UOBJ[uid].location; return x-c.x, y-c.y

EQ("U01","petroleiro",ship(),-70,42,1.2,"Navio","Petroleiro","Transporta o petróleo até o litoral de São Francisco do Sul.","Petróleo","Petróleo para a monoboia")
EQ("U01","monoboia",buoy(),-60,31,0,"Monoboia","Monoboia","Boia de amarração no mar. O petroleiro descarrega por mangote sem precisar atracar.","Petróleo do petroleiro","Petróleo para o tanque de São Francisco")
EQ("U01","tanque",tank(4.5,6,band="petroleo"),-42,23,0,"Tanque","Tanque de petróleo (São Francisco)","Armazena o petróleo recebido antes do envio pelo oleoduto.","Petróleo da monoboia","Petróleo para o oleoduto OSPAR")
EQ("U02","tanque",tank(3.5,5,band="petroleo"),-25,26.5,0,"Tanque","Tanque de petróleo REPAR","Recebe o petróleo do oleoduto OSPAR e alimenta a destilação.","Petróleo do oleoduto OSPAR","Petróleo para a fornalha")
EQ("U02","fornalha",furnace(5,3.5,3,11),-24.5,17.5,0,"Fornalha","Fornalha da destilação","Aquece o petróleo antes da torre atmosférica.","Petróleo","Petróleo aquecido")
EQ("U02","torre",tower(20,1.7,rings=5,ladder_ang=2.2,pipe_angs=(0.9,-2.3,2.9)),-15,23,0,"Torre","Torre de destilação atmosférica","Separa o petróleo por faixa de ebulição.","Petróleo aquecido","GLP, nafta leve, nafta pesada, querosene, diesel e RAT (resíduo atmosférico)")
EQ("U03","fornalha",furnace(4,3,3,10),-1,18.5,0,"Fornalha","Fornalha da unidade a vácuo","Reaquece o resíduo atmosférico antes da torre de vácuo.","RAT da destilação","RAT aquecido")
EQ("U03","torre",vac_tower(17,1.3,2.3),5,25.5,0,"Torre","Torre de vácuo","Destila o RAT sob pressão reduzida.","RAT aquecido","Gasóleo e resíduo de vácuo")
EQ("U04","conversor",converter(),26,30.5,0,"Conversor","Conversor catalítico (reator e regenerador)","Quebra as moléculas pesadas em contato com o catalisador quente.","Gasóleo e ODES","Efluente craqueado para a fracionadora")
EQ("U04","fracionadora",tower(19,1.9,rings=4,ladder_ang=-0.4,pipe_angs=(2.4,1.2)),36,23.5,0,"Torre","Fracionadora do craqueamento","Separa o efluente craqueado.","Efluente do conversor","GLP e resíduo para óleo combustível")
EQ("U05","esfera",gsphere(4.0),-37.5,4,0,"Esfera","Esfera de GLP","Armazena GLP sob pressão em estado líquido.","GLP da destilação e do craqueamento","GLP para a distribuidora")
EQ("U05","distribuidora",distrib(7,5,5),-27.5,4,0,"Distribuidora","Distribuidora de GLP","Envasa e expede o gás de cozinha.","GLP da esfera","Botijões para o consumidor")
EQ("U05","caminhao",truck('botijoes'),-28,-3,0,"Veículo","Caminhão de botijões","Leva o GLP envasado ao consumidor.","Botijões de GLP","Distribuição")
EQ("U06","torre",tower(10,1.0,rings=2,ladder_ang=2.8,pipe_angs=(0.5,)),-35,-17,0,"Torre","Torre de gasolina","Combina nafta leve e nafta pesada na gasolina A.","Nafta leve e nafta pesada","Gasolina A")
EQ("U06","distribuidora",distrib(7,5,5),-27,-17,0,"Distribuidora","Distribuidora de gasolina","Recebe a gasolina A e prepara a gasolina comercial.","Gasolina A","Gasolina para os postos")
EQ("U06","posto",posto(10,5),-31,-26,0,"Posto","Posto de combustível","Ponto de venda da gasolina ao consumidor.","Gasolina","Abastecimento de veículos")
EQ("U07","hdt",tower(10,1.2,rings=2,ladder_ang=2.6,pipe_angs=(0.3,)),-20,-37.5,0,"Torre","Hidrodessulfurização de diesel","Remove enxofre do diesel pesado.","Diesel pesado","Diesel leve")
EQ("U07","distribuidora",distrib(7,5,5),-11,-37.5,0,"Distribuidora","Distribuidora de diesel","Recebe o diesel leve misturado com nafta pesada e querosene.","Diesel leve, nafta pesada e querosene","Diesel para uso em motores")
EQ("U07","posto",posto(10,5),-8,-45,0,"Posto","Posto de combustível","Ponto de venda do diesel.","Diesel","Abastecimento de caminhões e ônibus")
EQ("U07","caminhao",truck(),-19,-45.5,0,"Veículo","Caminhão","Uso final do diesel em motores.","Diesel","—")
EQ("U08","hdt",tower(10,1.1,rings=2,ladder_ang=2.4,pipe_angs=(-0.5,)),11,-39,0,"Torre","Hidrodessulfurização de querosene","Remove enxofre do querosene da destilação.","Querosene da destilação","QAV-1")
EQ("U08","caminhao",truck(),44.5,-55.6,0,"Veículo","Caminhão abastecedor","Leva o QAV-1 até as aeronaves.","QAV-1","Abastecimento")
EQ("U08","aeronave",plane(),39,-49,0,"Aeronave","Aeronave","Uso final do QAV-1.","QAV-1","—")
EQ("U09","torre",tower(14,1.5,rings=3,ladder_ang=2.5,pipe_angs=(0.9,)),8.5,3,0,"Torre","Torre de desasfaltação","Separa o resíduo de vácuo com solvente.","Resíduo de vácuo","ODES (óleo desasfaltado) e resíduo asfáltico")
EQ("U10","torre",tower(12,1.1,rings=3,ladder_ang=2.6,pipe_angs=(0.5,)),34,-19,0,"Torre","Torre de solvente","Fraciona a nafta leve.","Nafta leve da destilação","Nafta peróxida e solvente de borracha")
EQ("U10","tanque",tank(3,5,band="solvente"),42,-19,0,"Tanque","Tanque de solvente de borracha","Armazena o solvente de borracha.","Solvente de borracha","Solvente para expedição")
EQ("U11","fabrica",fert_plant(),55,5.5,0,"Fábrica","Planta de fertilizantes","Usa os resíduos da refinaria como matéria-prima.","Resíduo para óleo combustível e resíduo asfáltico","Fertilizantes")
EQ("U11","tanque",tank(3,4,band="oleo_comb",m=darktank),64.5,-2,0,"Tanque","Tanque de matéria-prima","Armazena parte da matéria-prima recebida.","Matéria-prima da refinaria","Estoque")

# detalhes por unidade (estruturas, trocadores, bombas, veículos)
b = det("U01"); x, y = D("U01", -45, 14.5); b.box(x, y, 0.18, 5, 3, 3, white); b.box(x, y-1.53, 1.0, 4.2, 0.06, 0.8, winlit)
for yy in (19.5, 21): px, py = D("U01", -36.5, yy); pump(b, px, py)
b = det("U02"); sx_, sy_ = D("U02", -11.5, 26.8); steel_structure(b, sx_, sy_, 4, 4, 3, 12)
px, py = D("U02", -20.2, 20.6); exchangers(b, px, py, n=2, L=3.0, r=0.4)
for yy in (25.5, 27.5): px, py = D("U02", -18.6, yy); pump(b, px, py)
px, py = D("U02", -26.5, 15.2); b.box(px, py, 0.18, 4, 1.2, 2.6, concrete)
b = det("U03"); sx_, sy_ = D("U03", 9.2, 20.2); steel_structure(b, sx_, sy_, 3.5, 3.5, 2, 9)
px, py = D("U03", 1.5, 27.5); exchangers(b, px, py, n=2, L=3.0, r=0.4)
for xx in (2.5, 4.0): px, py = D("U03", xx, 21.6); pump(b, px, py)
b = det("U04"); sx_, sy_ = D("U04", 31, 19.5); steel_structure(b, sx_, sy_, 5, 4, 3, 12)
px, py = D("U04", 40.8, 30.0); exchangers(b, px, py, n=3, L=4.0, r=0.45)
px, py = D("U04", 23.5, 19.5); b.box(px, py, 0.18, 6, 4, 4, white); b.box(px, py-2.03, 1.2, 5, 0.06, 0.7, winlit); b.box(px, py, 4.18, 6.3, 4.3, 0.35, dark)
for xx in (38.5, 40): px, py = D("U04", xx, 20.0); pump(b, px, py)
b = det("U05")
for xx in (-33, -31.5): px, py = D("U05", xx, -0.5); pump(b, px, py)
b = det("U06")
b = det("U07"); sx_, sy_ = D("U07", -23, -42.5); steel_structure(b, sx_, sy_, 3, 3, 2, 7, coolers=True)
px, py = D("U07", -15.5, -40.5); exchangers(b, px, py, n=1, L=3.0, r=0.4)
b = det("U08"); sx_, sy_ = D("U08", 15, -38); steel_structure(b, sx_, sy_, 3.5, 3, 2, 8)
px, py = D("U08", 20.5, -40.5); exchangers(b, px, py, n=2, L=3.0, r=0.4)
b = det("U09"); sx_, sy_ = D("U09", 13.5, -1.8); steel_structure(b, sx_, sy_, 3, 2.8, 2, 8)
for xx in (6, 7.5): px, py = D("U09", xx, -2.5); pump(b, px, py)
b = det("U10"); px, py = D("U10", 38, -25); b.hcyl(px, py, 1.4, 4.5, 0.8, steel, axis='X'); b.box(px-1.5, py, 0.18, 0.4, 1.2, 0.8, concrete); b.box(px+1.5, py, 0.18, 0.4, 1.2, 0.8, concrete)
sx_, sy_ = D("U10", 37.5, -16.5); air_cooler(b, sx_, sy_, 4.0, 4.0, 2.4)
for cx in (-1.8, 1.8):
    for cy in (-1.0, 1.0): b.box(sx_+cx, sy_+cy, 0.18, 0.25, 0.25, 3.9, steel3)
for uid, bb in DET.items():
    bb.build(uid+"_detalhes", C_UNITS, parent=UOBJ[uid], props={"tipo": "detalhe", "unidade": uid})
# objetos avulsos (veículos e galpão) como detalhes
def ADD(uid, name, bld, x, y, rot=0):
    c = UOBJ[uid].location
    bld.build(f"{uid}_{name}", C_UNITS, loc=(x-c.x, y-c.y, 0.18), rot=rot, parent=UOBJ[uid], props={"tipo": "detalhe", "unidade": uid})
ADD("U05", "carro", car(car_cols[1]), -36, -3.5)
ADD("U06", "carro_a", car(car_cols[0]), -33.5, -27.2); ADD("U06", "carro_b", car(car_cols[2]), -28.5, -24.8, pi)
ADD("U06", "caminhao_tanque", truck(), -22.5, -27.5, pi/2)
ADD("U07", "carro", car(car_cols[3]), -10.5, -46.2)
ADD("U11", "galpao", shed_pile(10, 6, 5), 54, -1.5)
ADD("U08", "terminal", building(10, 4, 4, wall=white, rows=1), 40, -34.5)

# ------------------------------------------------------------------ tubulações de processo
PIPES = [
 ("P01","petroleo","U01","U01",[(-60,31),(-50.5,24),(-46.5,24)],0.9),
 ("P02","petroleo","U01","U02",[(-37.5,22),(-32,22),(-32,26.5),(-28.5,26.5)],1.0),
 ("P03","petroleo","U02","U02",[(-25,23),(-25,19.7)],1.0),
 ("P04","petroleo","U02","U02",[(-22,17.5),(-17.5,17.5),(-17.5,21.5)],1.0),
 ("P05","rat","U02","U03",[(-13.3,21),(-8,21),(-8,18.5),(-3,18.5)],1.3),
 ("P06","rat","U03","U03",[(1,18.5),(5,18.5),(5,23)],1.0),
 ("P07","gasoleo","U03","U04",[(7,27),(14,27),(14,29.5),(21.5,29.5)],1.3),
 ("P08","residuo_vac","U03","U09",[(6.5,24),(6.5,12),(8.5,12),(8.5,4.5)],1.0),
 ("P09","odes","U09","U04",[(10,3.5),(16.5,3.5),(16.5,31),(21.5,31)],1.7),
 ("P10","craqueado","U04","U04",[(28.5,27),(36,27),(36,25.5)],2.2),
 ("P11","glp","U02","U05",[(-16.4,22.5),(-16.4,10),(-36,10),(-36,7)],1.0),
 ("P12","glp","U04","U05",[(35,22),(35,12.5),(-39,12.5),(-39,7)],1.6),
 ("P13","nafta_leve","U02","U06",[(-15.6,22.5),(-15.6,-10),(-36,-10),(-36,-15.5)],1.2),
 ("P14","nafta_pesada","U02","U06",[(-14.8,22.5),(-14.8,-11.5),(-34,-11.5),(-34,-15.5)],1.5),
 ("P15","diesel","U02","U07",[(-14,22.5),(-14,-30),(-20,-30),(-20,-35.8)],1.0),
 ("P16","querosene","U02","U08",[(-13.2,22.5),(-13.2,-31.5),(11,-31.5),(11,-37.5)],1.3),
 ("P17","querosene","U02","U07",[(-12.4,22.5),(-12.4,-34.8)],1.6),
 ("P18","nafta_pesada","U02","U07",[(-13.4,22),(-10.8,22),(-10.8,-34.8)],1.9),
 ("P19","nafta_leve","U02","U10",[(-13.4,24),(-9.8,24),(-9.8,-8),(34,-8),(34,-17.5)],1.0),
 ("P20","oleo_comb","U04","U11",[(37.5,22.5),(46,22.5),(46,6.5),(48.5,6.5)],1.3),
 ("P21","rasf","U09","U11",[(10,2.5),(47,2.5),(47,5),(48.5,5)],1.0),
 ("P22","glp","U05","U05",[(-33.5,4),(-31,4)],1.0),
 ("P23","gasolina","U06","U06",[(-34,-17),(-30.5,-17)],1.0),
 ("P24","diesel","U07","U07",[(-18.8,-37.5),(-14.5,-37.5)],1.0),
 ("P25","qav","U08","U08",[(12,-40.5),(12,-44),(28,-44),(28,-55.6),(40,-55.6)],1.0),
 ("P26","solvente","U10","U10",[(35.1,-19),(39,-19)],1.0),
 ("P27","oleo_comb","U11","U11",[(61.5,4),(64.5,4),(64.5,1)],1.0),
]
sup = B()
for pid, stream, a, b_, pts, z in PIPES:
    cu = bpy.data.curves.new(pid, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.3; cu.bevel_resolution = 3; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i, (x, y) in enumerate(pts): sp.points[i].co = (x, y, z, 1)
    tmp = bpy.data.objects.new(pid+"_tmp", cu); C_PIPES.objects.link(tmp); bpy.context.view_layer.update()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(bpy.context.evaluated_depsgraph_get())); me.name = pid
    bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.curves.remove(cu)
    me.materials.clear(); me.materials.append(PIPE_M[stream])
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(pid, me); C_PIPES.objects.link(o)
    o["tipo"] = "tubulacao"; o["fluxo"] = stream; o["de"] = a; o["para"] = b_; o["path"] = json.dumps([[x, y, z] for x, y in pts])
    for i in range(len(pts)-1):
        p0, p1 = Vector(pts[i]), Vector(pts[i+1]); d = p1-p0; L = d.length; n = int(L//4.5)
        if L < 0.1: continue
        nx, ny = -d.y/L, d.x/L
        for k in range(1, n+1):
            q = p0+d*(k/(n+1))
            if q.x > -49:
                sup.box(q.x, q.y, 0, 0.5, 0.5, 0.15, concrete)
                sup.box(q.x, q.y, 0.15, 0.2, 0.2, z-0.45, steel3)
                sup.bar((q.x-nx*0.45, q.y-ny*0.45, z-0.32), (q.x+nx*0.45, q.y+ny*0.45, z-0.32), 0.18, steel3)
            else:
                sup.box(q.x, q.y, -0.1, 0.25, 0.25, z-0.2, steel3)        # flutuadores do duto submarino
    # flanges a cada 9 m
    for i in range(len(pts)-1):
        p0, p1 = Vector((*pts[i], z)), Vector((*pts[i+1], z)); d = p1-p0; L = d.length
        if L < 0.1: continue
        u = d/L
        for k in range(1, int(L//9)+1):
            q = p0+u*(k*9)
            sup.seg(q-u*0.07, q+u*0.07, 0.42, steel2, n=12)
sup.build("Suportes_tubulacao", C_ENV, props={"tipo": "ambiente"})

# ------------------------------------------------------------------ racks de utilidades (tubulação cinza elevada)
rack = B()
def pipe_rack(b, p0, p1, w=3.0, zb=3.2, n_pipes=6, spacing=6.0):
    p0 = Vector(p0); p1 = Vector(p1); d = p1-p0; L = d.length; u = d/L; nrm = Vector((-u.y, u.x))
    nb = int(L//spacing)+1
    for k in range(nb+1):
        q = p0+u*min(L, k*spacing)
        a = q+nrm*w/2; c = q-nrm*w/2
        for pp in (a, c): b.box(pp.x, pp.y, 0, 0.45, 0.45, 0.2, concrete); b.box(pp.x, pp.y, 0.2, 0.25, 0.25, zb+1.4, steel3)
        b.bar((a.x, a.y, zb), (c.x, c.y, zb), 0.22, steel3); b.bar((a.x, a.y, zb+1.4), (c.x, c.y, zb+1.4), 0.22, steel3)
    for side in (-1, 1):
        a = p0+nrm*side*w/2; c = p1+nrm*side*w/2
        b.bar((a.x, a.y, zb), (c.x, c.y, zb), 0.18, steel3); b.bar((a.x, a.y, zb+1.4), (c.x, c.y, zb+1.4), 0.18, steel3)
    cols = [galv, steel2, M("utilidade_verde", "#4f7f5a", 0.4, 0.5), galv, M("utilidade_azul", "#4a6f93", 0.4, 0.5), steel2]
    for i in range(n_pipes):
        off = -w/2+0.35+i*(w-0.7)/(n_pipes-1); rr = 0.16+0.06*(i % 3)
        a = p0+nrm*off; c = p1+nrm*off
        b.seg((a.x, a.y, zb+0.12+rr), (c.x, c.y, zb+0.12+rr), rr, cols[i % len(cols)], n=10)
        if i % 2 == 0: b.seg((a.x, a.y, zb+1.52+rr*0.7), (c.x, c.y, zb+1.52+rr*0.7), rr*0.7, cols[(i+2) % len(cols)], n=8)
    for k in range(0, nb, 2):
        q = p0+u*k*spacing+nrm*w/2; b.sph(q.x, q.y, zb+2.4, 0.09, lamp_w, seg=6)
pipe_rack(rack, (-40, 12.2), (34, 12.2), w=2.8)
pipe_rack(rack, (-13.3, 11), (-13.3, -29), w=8.2, zb=3.4, n_pipes=8)
pipe_rack(rack, (-8, -6.5), (33, -6.5), w=2.6, zb=3.2, n_pipes=5)
rack.build("Racks_utilidades", C_ENV, props={"tipo": "ambiente"})

# ------------------------------------------------------------------ terreno, vias, orla, cerca
env = B()
env.box(12, -6, -0.6, 126, 112, 0.6, ground)
sand = M("areia_umida", "#8f8467", 0, 1)
envs = B(); envs.box(-52, -6, -0.75, 3.2, 112, 0.6, sand); envs.box(12, -63, -0.75, 126, 2.6, 0.6, sand)
envs.build("Orla", C_ENV, props={"tipo": "ambiente"})
envw = B(); envw.box(0, 0, -1.6, 1200, 1200, 1.2, water); envw.build("Agua", C_ENV, props={"tipo": "ambiente"})
ROADS = [(12, -13.5, 126, 3.4), (12, 15.4, 120, 3.0), (-46.5, -6, 3.4, 108), (48.6, -6, 3.0, 108), (2.5, -33, 3.2, 38), (12, 40, 120, 3.4)]
for x, y, sx, sy in ROADS:
    env.box(x, y, 0, sx, sy, 0.06, road)
    horiz = sx > sy; L = sx if horiz else sy
    for k in range(int(L//4)):
        t = -L/2+2+k*4
        if horiz: env.box(x+t, y, 0.06, 1.8, 0.14, 0.01, paint_w)
        else: env.box(x, y+t, 0.06, 0.14, 1.8, 0.01, paint_w)
    for k in range(int(L//16)):                       # postes ao longo das vias
        t = -L/2+8+k*16
        if horiz: street_light(env, x+t, y+sy/2+0.6, -pi/2)
        else: street_light(env, x+sx/2+0.6, y+t, pi)
env.box(36, -49, 0, 28, 20, 0.08, road)                       # pátio de aeronaves
for i in range(6): env.box(23.5+i*4.5, -49, 0.08, 2.4, 0.15, 0.02, yellow)   # linha de táxi
env.box(36, -39.3, 0.08, 28, 0.12, 0.02, yellow); env.box(36, -58.7, 0.08, 28, 0.12, 0.02, yellow)
for k in range(4): street_light(env, 24+k*8, -38.4, -pi/2)
# cerca do perímetro
for (x0, y0, x1, y1) in ((-49.5, -61, -49.5, 49), (-49.5, 49, 74.5, 49), (74.5, 49, 74.5, -61), (74.5, -61, -49.5, -61)):
    L = math.hypot(x1-x0, y1-y0); n = int(L//3)
    for k in range(n+1):
        t = k/n; env.box(x0+(x1-x0)*t, y0+(y1-y0)*t, 0, 0.1, 0.1, 1.8, steel3)
    env.seg((x0, y0, 1.75), (x1, y1, 1.75), 0.04, galv, n=4); env.seg((x0, y0, 0.9), (x1, y1, 0.9), 0.03, galv, n=4)
env.build("Terreno_vias", C_ENV, props={"tipo": "ambiente"})

# mangote flutuante monoboia -> navio
hose = B(); hose.poly([(-60, 31, 0.0), (-63, 32.5, -0.2), (-66, 33.6, -0.1), (-69.5, 34.6, 1.4)], 0.25, M("mangote", "#1c1c1c", 0, 0.7))
for t in range(5): hose.cyl(-60.8-t*1.9, 31.4+t*0.75, -0.45, 0.5, 0.45, red, seg=10)
hose.build("U01_mangote", C_UNITS, loc=(60, -25, 0.0), parent=UOBJ["U01"], props={"tipo": "detalhe", "unidade": "U01"})

# ------------------------------------------------------------------ vegetação
random.seed(11); trees = B(); blocked = []
for uid, num, nome, desc, c, ((px, py), (sx, sy)) in UNITS: blocked.append((px-sx/2-2.5, px+sx/2+2.5, py-sy/2-2.5, py+sy/2+2.5))
for x, y, sx, sy in ROADS: blocked.append((x-sx/2-1.8, x+sx/2+1.8, y-sy/2-1.8, y+sy/2+1.8))
blocked += [(20, 52, -61, -31), (-42, 36, 10, 14.5), (-18.5, -8, -29, 11), (-9, 35, -9.5, -3.5), (48, 62, -6, 2)]
for pid, stream, a, b_, pts, z in PIPES:
    for i in range(len(pts)-1):
        (x0, y0), (x1, y1) = pts[i], pts[i+1]; blocked.append((min(x0, x1)-1.8, max(x0, x1)+1.8, min(y0, y1)-1.8, max(y0, y1)+1.8))
def free(x, y): return all(not (a <= x <= b and c <= y <= d) for a, b, c, d in blocked)
n = 0
for _ in range(9000):
    x = random.uniform(-48.5, 73.5); y = random.uniform(-60, 48)
    if not free(x, y): continue
    kind = random.random()
    if kind < 0.45:
        h = random.uniform(2.6, 4.2); r = random.uniform(0.9, 1.4)
        trees.cyl(x, y, 0, 0.9, 0.16, trunk, seg=5, smooth=False)
        trees.cyl(x, y, 0.8, h*0.6, r, treem, seg=7, r2=r*0.35, smooth=False)
        trees.cyl(x, y, 0.8+h*0.45, h*0.55, r*0.75, treem, seg=7, r2=0.05, smooth=False)
    elif kind < 0.85:
        r = random.uniform(1.0, 1.7)
        trees.cyl(x, y, 0, 1.4, 0.18, trunk, seg=5, smooth=False)
        ret = bmesh.ops.create_icosphere(trees.bm, subdivisions=1, radius=r, matrix=Matrix.Translation((x, y, 1.3+r*0.8)) @ Matrix.Diagonal((1, 1, 0.85, 1)))
        trees._set(ret['verts'], treem2)
    else:
        r = random.uniform(0.5, 0.8)
        ret = bmesh.ops.create_icosphere(trees.bm, subdivisions=1, radius=r, matrix=Matrix.Translation((x, y, r*0.6)))
        trees._set(ret['verts'], treem3)
    n += 1
    if n >= 1100: break
trees.build("Vegetacao", C_ENV, props={"tipo": "ambiente"})

# ------------------------------------------------------------------ iluminação, câmera e render (Eevee)
def add_light(name, kind, loc, energy, color, size=0.5):
    L = bpy.data.lights.new(name, kind); L.energy = energy; L.color = color
    if kind in ('POINT', 'SPOT'): L.shadow_soft_size = size
    o = bpy.data.objects.new(name, L); C_LIGHTS.objects.link(o); o.location = loc; return o
sun = add_light("Sol_crepusculo", 'SUN', (0, 0, 50), 4.5, (1.0, 0.74, 0.52))
sun.rotation_euler = (math.radians(62), 0, math.radians(-50)); sun.data.angle = math.radians(3)
moon = add_light("Luz_ceu", 'SUN', (0, 0, 50), 1.6, (0.6, 0.75, 1.0)); moon.rotation_euler = (math.radians(30), 0, math.radians(140))
for uid, num, nome, desc, c, ((px, py), (sx, sy)) in UNITS:
    add_light(f"Luz_{uid}", 'POINT', (px, py, 9), 4500, (1.0, 0.78, 0.5), size=2.0)
add_light("Luz_patio", 'POINT', (37, -47, 8), 2500, (0.85, 0.92, 1.0), 2.0)

world = scene.world or bpy.data.worlds.new("World"); scene.world = world; world.use_nodes = True
nt = world.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground")
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
ramp.color_ramp.elements[0].position = 0.48; ramp.color_ramp.elements[0].color = (*lin("#0a1a2c"), 1)
ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (*lin("#1d3f66"), 1)
el = ramp.color_ramp.elements.new(0.53); el.color = (*lin("#e08a52"), 1)
nt.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.6
nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

cam = bpy.data.cameras.new("Camera_aerea"); cam.lens = 30; cam.clip_end = 2000
co = bpy.data.objects.new("Camera_aerea", cam); C_ENV.objects.link(co)
co.location = (-86, -90, 80)
look = Vector((-7, -3, 0)) - co.location; co.rotation_euler = look.to_track_quat('-Z', 'Y').to_euler()
scene.camera = co

scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920; scene.render.resolution_y = 1080; scene.render.resolution_percentage = 100
ee = scene.eevee
for attr, val in (("taa_render_samples", 64), ("use_raytracing", True), ("use_shadows", True), ("shadow_ray_count", 2), ("use_gtao", True)):
    try: setattr(ee, attr, val)
    except Exception: pass
try: scene.view_settings.view_transform = 'AgX'; scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass

# brilho (bloom) no compositor
try:
    ng = bpy.data.node_groups.new("Brilho_REPAR", 'CompositorNodeTree')
    rl = ng.nodes.new("CompositorNodeRLayers"); gl = ng.nodes.new("CompositorNodeGlare")
    try: gl.inputs["Type"].default_value = 'Bloom'
    except Exception: gl.glare_type = 'BLOOM'
    for nm, v in (("Threshold", 0.9), ("Strength", 0.8), ("Size", 0.6)):
        if nm in gl.inputs: gl.inputs[nm].default_value = v
    go = ng.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    gout = ng.nodes.new("NodeGroupOutput")
    ng.links.new(rl.outputs["Image"], gl.inputs["Image"]); ng.links.new(gl.outputs["Image"], gout.inputs[0])
    scene.compositing_node_group = ng
    BLOOM = "ok"
except Exception as ex:
    BLOOM = "falhou: %s" % ex

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PASTA, "REPAR_maquete.blend"))
RESUMO = {"objetos": len(bpy.data.objects), "vertices": sum(len(o.data.vertices) for o in bpy.data.objects if o.type == 'MESH'), "arvores": n, "bloom": BLOOM}

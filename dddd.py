import math
import pyray as rl

# ─── Vector3 class (from your code) ──────────────────────────────────────────
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, v): return Vector3(self.x+v.x, self.y+v.y, self.z+v.z)
    def __sub__(self, v): return Vector3(self.x-v.x, self.y-v.y, self.z-v.z)
    def __mul__(self, v): return Vector3(self.x*v,   self.y*v,   self.z*v)

def dot(v1, v2):       return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
def length(v):         return math.sqrt(dot(v, v))
def normalize(v):
    m = length(v)
    return v * (1.0/m) if m != 0 else v

# ─── Ray vs infinite plane ────────────────────────────────────────────────────
def hit_plane_dist(plane_center, plane_normal, ray_origin, ray_dir):
    denom = dot(plane_normal, ray_dir)
    if abs(denom) > 1e-6:
        t = dot(plane_center - ray_origin, plane_normal) / denom
        if t > 0:
            return t
    return None

# ─── Ray vs sphere ────────────────────────────────────────────────────────────
def hit_sphere_dist(center, radius, ray_origin, ray_dir):
    oc = ray_origin - center
    a  = dot(ray_dir, ray_dir)
    b  = 2.0 * dot(oc, ray_dir)
    c  = dot(oc, oc) - radius * radius
    disc = b*b - 4*a*c
    if disc < 0:
        return None
    t = (-b - math.sqrt(disc)) / (2.0 * a)
    return t if t > 0 else None

# ─── Ray vs cylinder (finite, axis-aligned Y) ─────────────────────────────────
def hit_cylinder_dist(base, radius, height, ray_origin, ray_dir):
    # Infinite cylinder around Y axis shifted to base.x, base.z
    ox = ray_origin.x - base.x
    oz = ray_origin.z - base.z
    dx = ray_dir.x
    dz = ray_dir.z
    a  = dx*dx + dz*dz
    if abs(a) < 1e-6:
        return None
    b    = 2*(ox*dx + oz*dz)
    c    = ox*ox + oz*oz - radius*radius
    disc = b*b - 4*a*c
    if disc < 0:
        return None
    t = (-b - math.sqrt(disc)) / (2*a)
    if t < 0:
        t = (-b + math.sqrt(disc)) / (2*a)
    if t < 0:
        return None
    # Check Y bounds
    hy = ray_origin.y + t * ray_dir.y
    if hy < base.y or hy > base.y + height:
        return None
    return t

# ─── Ray vs cone (finite, axis-aligned Y, tip at top) ─────────────────────────
def hit_cone_dist(base, radius, height, ray_origin, ray_dir):
    # Cone: at y=base.y radius=radius, at y=base.y+height radius=0
    tip_y = base.y + height
    k  = radius / height   # slope
    ox = ray_origin.x - base.x
    oy = ray_origin.y - tip_y   # relative to tip
    oz = ray_origin.z - base.z
    dx, dy, dz = ray_dir.x, ray_dir.y, ray_dir.z
    a  = dx*dx + dz*dz - k*k*dy*dy
    b  = 2*(ox*dx + oz*dz - k*k*oy*dy)
    c  = ox*ox + oz*oz - k*k*oy*oy
    if abs(a) < 1e-6:
        return None
    disc = b*b - 4*a*c
    if disc < 0:
        return None
    t = (-b - math.sqrt(disc)) / (2*a)
    if t < 0:
        t = (-b + math.sqrt(disc)) / (2*a)
    if t < 0:
        return None
    hy = ray_origin.y + t * ray_dir.y
    if hy < base.y or hy > tip_y:
        return None
    return t

# ─── Simple diffuse shading ───────────────────────────────────────────────────
LIGHT = normalize(Vector3(1, 2, 0.5))

def shade(normal, base_col, ambient=0.25):
    d = max(0.0, dot(normalize(normal), LIGHT))
    intensity = ambient + (1.0 - ambient) * d
    r = int(min(255, base_col[0] * intensity))
    g = int(min(255, base_col[1] * intensity))
    b = int(min(255, base_col[2] * intensity))
    return rl.Color(r, g, b, 255)

def flat(r, g, b): return rl.Color(r, g, b, 255)

# ─── Scene definition ─────────────────────────────────────────────────────────
WIDTH, HEIGHT = 800, 600
camera_pos = Vector3(0, 0.2, 0)

# Planes: (center, normal, base_rgb)
planes_scene = [
    (Vector3(0, -1.0,  0), Vector3( 0,  1,  0), (241, 156, 187)),  # floor
    (Vector3(0,  0,   -5), Vector3( 0,  0,  1), ( 50,  80, 160)),  # front
    (Vector3(-3, 0,    0), Vector3( 1,  0,  0), (200,  102, 204)),  # left
    (Vector3( 3, 0,    0), Vector3(-1,  0,  0), ( 251, 206,  177)),  # right
    (Vector3(0,  2.0,  0), Vector3( 0, -1,  0), ( 255, 153, 102)),  # ceiling
]

# Figures: (type, params...)
# sphere:   ("sphere",   center_V3, radius, rgb)
# cone:     ("cone",     base_V3,   radius, height, rgb)
# cylinder: ("cylinder", base_V3,   radius, height, rgb)
figures = [
    ("sphere",   Vector3(-1.5, -0.4, -3.5), 0.55,      (180,  50, 220)),
    ("cone",     Vector3( 0.0, -1.0, -4.0), 0.45, 1.5, (220, 100,  40)),
    ("cylinder", Vector3( 1.5, -1.0, -3.5), 0.35, 1.1, (123, 45,123)),
]
print("Rendering... please wait...")
canvas = rl.gen_image_color(WIDTH, HEIGHT, rl.BLACK)

for y in range(HEIGHT):
    for x in range(WIDTH):
        aspect = WIDTH / HEIGHT
        px = (2.0 * x / WIDTH  - 1.0) * aspect
        py =  1.0 - 2.0 * y / HEIGHT
        ray_dir = normalize(Vector3(px, py, -1.5))

        closest_t   = float('inf')
        pixel_color = rl.BLACK

        # ── Test planes ──────────────────────────────────────────────────────
        for (pcenter, pnormal, prgb) in planes_scene:
            t = hit_plane_dist(pcenter, pnormal, camera_pos, ray_dir)
            if t and t < closest_t:
                closest_t   = t
                hit_pt      = camera_pos + ray_dir * t
                pixel_color = shade(pnormal, prgb)

        # ── Test figures ─────────────────────────────────────────────────────
        for fig in figures:
            kind = fig[0]

            if kind == "sphere":
                _, center, radius, rgb = fig
                t = hit_sphere_dist(center, radius, camera_pos, ray_dir)
                if t and t < closest_t:
                    closest_t   = t
                    hit_pt      = camera_pos + ray_dir * t
                    normal      = hit_pt - center
                    pixel_color = shade(normal, rgb)

            elif kind == "cone":
                _, base, radius, height, rgb = fig
                t = hit_cone_dist(base, radius, height, camera_pos, ray_dir)
                if t and t < closest_t:
                    closest_t   = t
                    hit_pt      = camera_pos + ray_dir * t
                    # Approximate outward normal (radial in XZ)
                    nx = hit_pt.x - base.x
                    nz = hit_pt.z - base.z
                    normal = normalize(Vector3(nx, radius/height, nz))
                    pixel_color = shade(normal, rgb)

            elif kind == "cylinder":
                _, base, radius, height, rgb = fig
                t = hit_cylinder_dist(base, radius, height, camera_pos, ray_dir)
                if t and t < closest_t:
                    closest_t   = t
                    hit_pt      = camera_pos + ray_dir * t
                    normal      = normalize(Vector3(hit_pt.x - base.x, 0, hit_pt.z - base.z))
                    pixel_color = shade(normal, rgb)

        if closest_t != float('inf'):
            rl.image_draw_pixel(canvas, x, y, pixel_color)

# ─── Window & display loop ────────────────────────────────────────────────────
rl.init_window(WIDTH, HEIGHT, "Static 3D Figures — CPU Raytracer")
rl.set_target_fps(60)

screen_texture = rl.load_texture_from_image(canvas)

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.draw_texture(screen_texture, 0, 0, rl.WHITE)
    rl.draw_text("Sphere  |  Cone  |  Cylinder  — CPU Raytracing", 10, 10, 18, rl.RAYWHITE)
    rl.draw_fps(WIDTH - 80, 10)
    rl.end_drawing()

rl.unload_texture(screen_texture)
rl.unload_image(canvas)
rl.close_window()
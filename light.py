import math
class Vector3:
    def __init__(self, x, y, z):
        self.x = x  
        self.y = y
        self.z = z
    def __add__ (self,v):
            x = self.x + v.x
            y = self.y + v.y
            z = self.z + v.z
            return Vector3 (x,y,z)
    def __str__ (self):
                return f"Vector3 ({self.x}, {self.y}, {self.z})"
    def __mul__ (self,v):
                return Vector3(self.x * v, self.y * v, self.z * v)
    def __sub__ (self,v):
                return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)
v1 = Vector3(3,2,5)
v2 = Vector3(8,5,4)
print(v1+v2)

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
print(dot(v1, v2))
def length(v):
    return math.sqrt(dot(v, v))
def normalize (v):
    m = length(v)
    return v*(1.0/m) if m != 0 else v
print(normalize (v1))

def hit_sphere(center, radius, ray_origin, ray_dir):
    oc = ray_origin - center
    a = dot(ray_dir, ray_dir)
    b = 2.0 * dot(oc, ray_dir)
    c = dot(oc, oc) - radius * radius
    
    discriminant = b*b - 4*a*c
    
    if discriminant < 0:
        return -1.0 
    
    return (-b - math.sqrt(discriminant)) / (2.0 * a)
    oc = ray_origin - center
    
    # at^2 + bt + c = 0
    a = dot(ray_dir, ray_dir)
    b = 2.0 * dot(oc, ray_dir)
    c = dot(oc, oc) - radius * radius
    
    discriminant = b*b - 4*a*c
    
    return discriminant > 0
import pyray as rl
WIDTH = 800
HEIGHT = 600
TITLE = "Моє коло"

# --- 1. SETTINGS ---

canvas = rl.gen_image_color(WIDTH, HEIGHT, rl.BLACK)

# --- 4. MAIN LOOP ---
rl.init_window(WIDTH, HEIGHT, TITLE)
rl.set_target_fps(60)

# Create a texture on the GPU that we will update with our CPU canvas
screen_texture = rl.load_texture_from_image(canvas)

camera_pos = Vector3(0, 0, 0)
sphere_pos = Vector3(0, 0, -5)
sphere_radius = 1.0

while not rl.window_should_close():    
    ########################################
    for y in range(HEIGHT):
        for x in range(WIDTH):

            aspect_ratio = WIDTH / HEIGHT
            px = (2.0 * x / WIDTH - 1.0) * aspect_ratio
            py = (1.0 - 2.0 * y / HEIGHT)
            
            ray_dir = normalize(Vector3(px, py, -1.0))
            
            t = hit_sphere(sphere_pos, sphere_radius, camera_pos, ray_dir)
            
            if t > 0.0:
                hit_point = camera_pos + (ray_dir * t)
                normal = normalize(hit_point - sphere_pos)
                light_dir = normalize(Vector3(0.0, 0.0, 1.0))
                
                diffuse = max(0.0, dot(normal, light_dir))
                
                ambient = 0.2
                intensity = min(1.0, diffuse + ambient) 
                
                r = int(100 * intensity) 
                g = int(20 * intensity)   
                b = int(130 * intensity)
                
                rl.image_draw_pixel(canvas, x, y, rl.Color(r, g, b, 255))
            else:
                rl.image_draw_pixel(canvas, x, y, rl.BLACK)

    ########################################

    # To see changes in real-time, we must re-upload the RAM image to the GPU texture
    rl.update_texture(screen_texture, canvas.data)

    # --- DRAW (Visuals) ---
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)

    # Draw our custom pixel buffer
    rl.draw_texture(screen_texture, 0, 0, rl.WHITE)



    # UI / Overlays
    rl.draw_text("CPU Pixel Buffer (Raytrace)", 10, 10, 20, rl.RAYWHITE)
    rl.draw_fps(WIDTH - 80, 10)

    rl.end_drawing()




# --- 5. CLEANUP ---
rl.unload_texture(screen_texture)
rl.unload_image(canvas)
rl.close_window()

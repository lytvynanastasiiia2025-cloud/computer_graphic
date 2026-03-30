import pyray as rl
from features.vector3 import normalize, Vector3
from features.sphere import hit_sphere
from features.utils import WIDTH, HEIGHT, TITLE

# --- 1. SETTINGS ---

canvas = rl.gen_image_color(WIDTH, HEIGHT, rl.BLACK)

# --- 4. MAIN LOOP ---
rl.init_window(WIDTH, HEIGHT, TITLE)
rl.set_target_fps(60)

# Create a texture on the GPU that we will update with our CPU canvas
screen_texture = rl.load_texture_from_image(canvas)

camera_pos = Vector3(8, 9, 10)
sphere_pos = Vector3(7, 6, 5 )
sphere_radius = 1.0
sphere_pos2 = Vector3( 10, 9, 8)
sphere_radius2 = 1.0

while not rl.window_should_close():    
    ########################################
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Перетворюємо координати пікселів (0..800) у простір (-1..1)
            # Враховуємо співвідношення сторін (aspect ratio)
            aspect_ratio = WIDTH / HEIGHT
            px = (2.0 * x / WIDTH - 1.0) * aspect_ratio
            py = (1.0 - 2.0 * y / HEIGHT)
            
            # Напрямок променя від ока через поточний піксель
            ray_dir = normalize(Vector3(px, py, -1.0))
            
            if hit_sphere(sphere_pos, sphere_radius, camera_pos, ray_dir):
                rl.image_draw_pixel(canvas, x, y, rl.PINK)
            elif hit_sphere(sphere_pos2, sphere_radius2, camera_pos, ray_dir):
                rl.image_draw_pixel(canvas, x, y, rl.BLUE)

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

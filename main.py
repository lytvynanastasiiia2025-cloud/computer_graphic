import pyray as rl 
from features.utils import WIDTH, HEIGHT, TITLE, draw_line 

rl.init_window(WIDTH, HEIGHT, TITLE) 
rl.set_target_fps(60) 

canvas = rl.gen_image_color(WIDTH, HEIGHT, rl.BLACK) 
screen_texture = rl.load_texture_from_image(canvas) 
while not rl.window_should_close(): 
    draw_line(canvas, 100, 100, 700, 350, rl.GOLD) 
    rl.update_texture(screen_texture, canvas.data) 
    rl.begin_drawing() 
    rl.clear_background(rl.BLACK) 
    rl.draw_texture(screen_texture, 0, 0, rl.WHITE) 
    rl.draw_text("Press ESC to exit", 10, 10, 20, rl.RAYWHITE) 
    rl.end_drawing() 

rl.unload_texture(screen_texture) 
rl.unload_image(canvas) 
rl.close_window()
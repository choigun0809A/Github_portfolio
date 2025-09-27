from pyray import *


init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()
    key = get_key_pressed()
    if chr(key) == "W" and is_key_pressed(key):
        print("W")
    vec = Vector2(0, 0)
    rect = Rectangle(0, 0, 0, 0)
    rect.height
close_window()


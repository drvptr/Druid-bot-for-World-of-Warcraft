from Xlib import X, display
import struct
import time

def decode_rgb_to_float(r, g, b):
    int_val = (r << 16) + (g << 8) + b  
    return int_val / 1000 

d = display.Display()
root = d.screen().root

while True:
    raw = root.get_image(0, 0, 90, 30, X.ZPixmap, 0xFFFFFF) 
    pixels = struct.unpack(f"{90 * 30 * 4}B", raw.data)  

    coords = []
    for i in range(3):  # Три кубика: X, Y, Z
        x_offset = i * 30 + 15  # Берём середину кубика
        y_offset = 15  # Тоже середина по высоте

        pixel_index = (y_offset * 90 + x_offset) * 4  
        b, g, r = pixels[pixel_index:pixel_index+3] 

        coords.append(decode_rgb_to_float(r, g, b))

    print(f"Player coordinates: X={coords[0]}, Y={coords[1]}, Z={coords[2]}")
    time.sleep(0.1) 

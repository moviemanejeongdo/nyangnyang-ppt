import re
import os

file_path = r'e:\unity 26.04.28\냥냥ppt260606\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update totalSlides
content = content.replace('const totalSlides = 9;', 'const totalSlides = 10;')

# 2. Update CSS Selectors (Reverse order)
content = content.replace('#slide-8', '#slide-9')
content = content.replace('#slide-7', '#slide-8')
content = content.replace('#slide-6', '#slide-7')
content = content.replace('#slide-5', '#slide-6')
content = content.replace('slide-8', 'slide-9')  # For classes or IDs like id="slide-8"
content = content.replace('slide-7', 'slide-8')
content = content.replace('slide-6', 'slide-7')
content = content.replace('slide-5', 'slide-6')

# But wait, slide5SubIndex, slide5Sub2State, slide7State, slide8State might be renamed?
# It's safer to not rename JS variables (slide7State etc) unless necessary. The user only cares about the visual output.
# But replacing 'slide-5' -> 'slide-6' globally will change `slide5SubIndex` to `slide6SubIndex` if we are not careful!
# So we MUST NOT globally replace 'slide-5'. We only replace specific ID strings.

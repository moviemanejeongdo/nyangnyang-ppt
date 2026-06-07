import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_slide_7 = """        <div class="slide" id="slide-7">
            <div class="glass-panel" style="width: 85%; height: 85%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px;">"""

new_slide_7 = """        <div class="slide" id="slide-7" style="justify-content: center; align-items: center;">
            <div class="glass-panel" style="width: 85%; max-width: 1500px; height: 85%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px; margin: 0 auto;">"""

if old_slide_7 in text:
    text = text.replace(old_slide_7, new_slide_7)
    with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed slide 7 alignment!")
else:
    print("Could not find slide 7 HTML block.")

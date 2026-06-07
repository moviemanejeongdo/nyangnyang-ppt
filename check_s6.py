import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s6_idx = text.find('id="slide-6"')
if s6_idx != -1:
    end_s6 = text.find('    </div>\n\n    <div class="nav-hint"', s6_idx)
    print(text[end_s6-100:end_s6+100])

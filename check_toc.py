import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="slide-2"')
if start != -1:
    end = text.find('</ul>', start)
    print(text[start:end+5])

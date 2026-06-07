import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="slide-7"')
if start != -1:
    end = text.find('<!-- ===== 7페이지 끝 ===== -->', start)
    print(text[start-30:end+35])

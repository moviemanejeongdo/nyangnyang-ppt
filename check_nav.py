import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('.nav-hint {')
if start != -1:
    end = text.find('}', start) + 1
    print('CSS:', text[start:end])

html_start = text.find('<div class="nav-hint" id="nav-hint">')
if html_start != -1:
    html_end = text.find('</div>', html_start) + 6
    print('HTML:', text[html_start:html_end])

js_start = text.find("document.getElementById('nav-hint').innerText =")
if js_start != -1:
    js_end = text.find(';', js_start) + 1
    print('JS:', text[js_start:js_end])

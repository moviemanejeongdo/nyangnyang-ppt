import re
with open(r'e:\unity 26.04.28\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
matches = re.findall(r'<div class="slide" id="slide-(\d+)"', html)
for m in matches:
    print('Slide', m)

# Also let's extract the actual headers inside each slide to be 100% sure.
for m in matches:
    # find the next h2 or title after this slide
    idx = html.find(f'<div class="slide" id="slide-{m}"')
    if idx != -1:
        snippet = html[idx:idx+1000]
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', snippet, re.DOTALL)
        title = h2.group(1).strip() if h2 else "No H2 found"
        # strip inner tags
        title = re.sub(r'<[^>]+>', '', title)
        print(f'Slide {m}: {title}')

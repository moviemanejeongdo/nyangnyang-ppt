import re

html_path = 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# font-size가 정의된 모든 패턴 찾기
matches = re.findall(r'font-size\s*:\s*([^;}\s]+)', content)
print("Found font-size patterns:")
for m in sorted(list(set(matches))):
    print(m)

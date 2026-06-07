import re

html_path = 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# font-size: \d+px 패턴을 찾아서 수치에 2를 더해주는 함수
def replace_font_px(match):
    val = int(match.group(1))
    return f"font-size: {val + 2}px"

# 정규식을 사용하여 font-size: XXpx 패턴을 매칭하고 변환
new_content = re.sub(r'font-size\s*:\s*(\d+)px', replace_font_px, content)

# 변경 사항이 있을 경우 파일에 기록
if content != new_content:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Font sizes successfully increased by 2px.")
else:
    print("No font-size: XXpx patterns found to change.")

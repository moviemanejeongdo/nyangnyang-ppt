import os
from PIL import Image

folder = os.path.dirname(os.path.abspath(__file__))
imgs = sorted([f for f in os.listdir(folder) if f.upper().endswith('.PNG')])
print(f"{len(imgs)}개 이미지 발견")

pages = []
for f in imgs:
    img = Image.open(os.path.join(folder, f)).convert('RGB')
    pages.append(img)

output = os.path.join(folder, '냥냥카페_PPT.pdf')
pages[0].save(output, save_all=True, append_images=pages[1:], resolution=150)
print(f"PDF 생성 완료: {output}")

import os

file_path = r'e:\unity 26.04.28\냥냥ppt260606\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make a backup
with open(file_path + '.bak', 'w', encoding='utf-8') as f:
    f.write(content)

# Adjust glass panel overflow
content = content.replace(
    'justify-content: flex-start; padding: 40px; margin: 0 auto; overflow-y: auto;">',
    'justify-content: center; padding: 40px; margin: 0 auto; overflow-y: hidden;">'
)

# Adjust grid to 4 columns, smaller gap
content = content.replace(
    'display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; width: 100%;',
    'display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; width: 100%;'
)

# Adjust SVG size
content = content.replace('width="60" height="60"', 'width="48" height="48"')
content = content.replace('style="margin-bottom: 15px;"><rect x="2"', 'style="margin-bottom: 10px;"><rect x="2"')
content = content.replace('style="margin-bottom: 15px;"><path d="M12"', 'style="margin-bottom: 10px;"><path d="M12"')
content = content.replace('style="margin-bottom: 15px;"><path d="M14.7"', 'style="margin-bottom: 10px;"><path d="M14.7"')
content = content.replace('style="margin-bottom: 15px;"><polyline points="16"', 'style="margin-bottom: 10px;"><polyline points="16"')
content = content.replace('style="margin-bottom: 15px;"><circle cx="12"', 'style="margin-bottom: 10px;"><circle cx="12"')

# Adjust title margin
content = content.replace('style="margin-bottom: 40px; font-size: 56px; color: #333;">개발 환경</h2>', 'style="margin-bottom: 30px; font-size: 50px; color: #333;">개발 환경</h2>')

# Adjust cards padding
content = content.replace('padding: 25px; border-radius: 20px;', 'padding: 20px; border-radius: 20px;')

# Adjust h3
content = content.replace('style="font-size: 24px; color: #2c3e50; margin-bottom: 15px;">', 'style="font-size: 20px; color: #2c3e50; margin-bottom: 8px;">')

# Adjust p
content = content.replace('style="font-size: 18px; color: #555; line-height: 1.6;">', 'style="font-size: 15px; color: #555; line-height: 1.4;">')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Styles adjusted for Slide 5")

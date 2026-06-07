import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
old_css = """        .nav-hint {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.1em;
            color: var(--text-muted);
            letter-spacing: 0.1em;
            opacity: 0.5;
            font-family: 'Outfit', sans-serif;
            pointer-events: none;
        }"""
new_css = """        .nav-hint {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.1em;
            color: var(--text-muted);
            letter-spacing: 0.1em;
            opacity: 0.5;
            font-family: 'Outfit', sans-serif;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1000;
        }

        .nav-hint .nav-btn {
            cursor: pointer;
            transition: color 0.3s, transform 0.2s, opacity 0.3s;
            padding: 5px 10px;
            opacity: 0.7;
        }

        .nav-hint .nav-btn:hover {
            color: var(--accent-primary);
            transform: scale(1.3);
            font-weight: 800;
            opacity: 1;
        }"""
text = text.replace(old_css, new_css)

# 2. Update HTML
old_html = '<div class="nav-hint" id="nav-hint">&lt; 1 / 6 &gt;</div>'
new_html = """<div class="nav-hint" id="nav-hint">
        <span class="nav-btn" id="nav-prev">&lt;</span>
        <span id="nav-current">1 / 6</span>
        <span class="nav-btn" id="nav-next">&gt;</span>
    </div>"""
text = text.replace(old_html, new_html)

# 3. Update JS goToSlide
old_js = "document.getElementById('nav-hint').innerText = `< ${index} / ${totalSlides} >`;"
new_js = "document.getElementById('nav-current').innerText = `${index} / ${totalSlides}`;"
text = text.replace(old_js, new_js)

# 4. Add Event Listeners
# Before the closing </script> tag
event_listeners = """
        // 하단 네비게이션 버튼 클릭 이벤트
        document.getElementById('nav-prev').addEventListener('click', () => {
            if (currentSlideIndex > 1) {
                goToSlide(currentSlideIndex - 1);
            } else {
                goToSlide(1);
            }
        });

        document.getElementById('nav-next').addEventListener('click', () => {
            if (currentSlideIndex < totalSlides) {
                goToSlide(currentSlideIndex + 1);
            }
        });
"""
if "document.getElementById('nav-prev').addEventListener('click'" not in text:
    script_end = text.rfind('</script>')
    if script_end != -1:
        text = text[:script_end] + event_listeners + '    ' + text[script_end:]

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated nav-hint successfully!")

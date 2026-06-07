import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\codex.html', 'r', encoding='utf-8') as f:
    codex = f.read()

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# CSS extraction
css_start = codex.find('/* ===== 6페이지 시작: 개발 이슈 회고 CSS ===== */')
css_end = codex.find('/* ===== 6페이지 끝: 개발 이슈 회고 CSS ===== */') + len('/* ===== 6페이지 끝: 개발 이슈 회고 CSS ===== */')
if css_start != -1 and css_end != -1:
    css_block = codex[css_start:css_end]
    insert_pos_css = index.find('@keyframes blinkCursor')
    if insert_pos_css != -1 and '/* ===== 6페이지 시작: 개발 이슈 회고 CSS ===== */' not in index:
        index = index[:insert_pos_css] + css_block + '\n\n        ' + index[insert_pos_css:]
        print("CSS injected")
else:
    print("Could not find CSS block in codex.html")

# HTML extraction
html_start = codex.find('<!-- ===== 5-3 시작: 음료 제조 알고리즘 서브 페이지 ===== -->')
html_end = codex.find('<!-- ===== 6페이지 끝 ===== -->') + len('<!-- ===== 6페이지 끝 ===== -->')
if html_start != -1 and html_end != -1:
    html_block = codex[html_start:html_end]
    
    index_html_start = index.find('<!-- 5-3: 음료 제조 알고리즘 서브 페이지 -->')
    # look for the end of the presentation container in index.html
    # which is right before <div class="nav-hint" id="nav-hint">&lt; 1 / 5 &gt;</div>
    nav_hint_idx = index.find('<div class="nav-hint" id="nav-hint">')
    if nav_hint_idx != -1 and index_html_start != -1:
        # the end of the html to replace should be exactly the div ending before nav-hint
        # let's just find the last </div> before nav-hint_idx
        # actually, just replace from index_html_start to nav_hint_idx (with some padding)
        index_html_end = index.rfind('</div>', 0, nav_hint_idx)
        # we need to remove the 3 closing divs from index.html (for slide5-sub-page, slide, presentation)
        # wait, let's just do a simpler replacement
        index_html_end = index.find('    <div class="nav-hint" id="nav-hint">')
        if index_html_end != -1:
            # We want to replace from index_html_start up to right before `    </div>\n\n    <div class="nav-hint`
            # Let's find exactly `    </div>\n\n    <div class="nav-hint`
            end_match = index.find('    </div>\n\n    <div class="nav-hint"')
            if end_match != -1:
                index = index[:index_html_start] + html_block + '\n' + index[end_match:]
                print("HTML injected")
            else:
                print("Could not find end match in index.html")
        else:
            print("Could not find nav-hint in index.html")
else:
    print("Could not find HTML block in codex.html")

# Update Slide Count
if 'const totalSlides = 5;' in index:
    index = index.replace('const totalSlides = 5;', 'const totalSlides = 6;')
    print("Slide count updated to 6")
elif 'const totalSlides = 6;' in index:
    print("Slide count is already 6")

# Update nav-hint text
index = index.replace('&lt; 1 / 5 &gt;', '&lt; 1 / 6 &gt;')

# Update TOC js mapping
old_toc_js = '''                } else if (index === 2) {
                    goToSlide(5); // 3. 주요 기능 구현 -> 5페이지
                }
            });
        });'''
new_toc_js = '''                } else if (index === 2) {
                    goToSlide(5); // 3. 주요 기능 구현 -> 5페이지
                } else if (index === 3) {
                    goToSlide(6); // 4. 개발 중 이슈사항 -> 6페이지
                }
            });
        });'''
if old_toc_js in index:
    index = index.replace(old_toc_js, new_toc_js)
    print("TOC JS updated")

# Extract JS from codex.html
slide6_js_start = codex.find('// 5페이지 비디오 클릭 시 재생/일시정지 토글 기능 및 오버레이 애니메이션')
slide6_js_end = codex.find('</script>', slide6_js_start)
if slide6_js_start != -1 and slide6_js_end != -1:
    slide6_js = codex[slide6_js_start:slide6_js_end]
    end_script_idx = index.rfind('</script>')
    if end_script_idx != -1 and 'document.querySelectorAll(\'#slide-6 .issue-dot\')' not in index:
        index = index[:end_script_idx] + '        ' + slide6_js + '\n    ' + index[end_script_idx:]
        print("JS injected")

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Replacement complete")

import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update totalSlides
if 'const totalSlides = 6;' in text:
    text = text.replace('const totalSlides = 6;', 'const totalSlides = 7;')
    
# 2. Insert Slide 7 HTML
slide7_html = """        <!-- Slide 7: 시연 영상 -->
        <div class="slide" id="slide-7">
            <div class="glass-panel" style="width: 85%; height: 85%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px;">
                <h2 class="title" style="margin-bottom: 20px;">시연 영상</h2>
                <div style="flex: 1; width: 100%; border-radius: 20px; overflow: hidden; background: #000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); position: relative;" id="slide7-video-container">
                    <video id="demo-video-7" src="유니티images/7페이지/시연연상.mp4" style="width: 100%; height: 100%; object-fit: contain;" preload="metadata"></video>
                </div>
            </div>
        </div>
        <!-- ===== 7페이지 끝 ===== -->"""

insert_target = '        <!-- ===== 6페이지 끝 ===== -->\n    </div>'
if insert_target in text and 'id="slide-7"' not in text:
    text = text.replace(insert_target, '        <!-- ===== 6페이지 끝 ===== -->\n' + slide7_html + '\n    </div>')

# 3. Add JS state variable
state_target = 'let slide5Sub2State = 0;'
if state_target in text and 'let slide7State' not in text:
    text = text.replace(state_target, state_target + '\n        let slide7State = 0; // 0: paused, 1: playing')

# 4. Update Spacebar logic
old_space = """                } else if (currentSlideIndex === 6) {
                    if (!nextIssueCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex < totalSlides) {"""

new_space = """                } else if (currentSlideIndex === 6) {
                    if (!nextIssueCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 7) {
                    const video7 = document.getElementById('demo-video-7');
                    if (slide7State === 0) {
                        if (video7) video7.play();
                        slide7State = 1;
                    } else if (slide7State === 1) {
                        if (video7) {
                            video7.pause();
                        }
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    }
                } else if (currentSlideIndex < totalSlides) {"""

if old_space in text and 'currentSlideIndex === 7' not in text:
    text = text.replace(old_space, new_space)

# 5. Update Backspace logic
old_back = """                } else if (currentSlideIndex === 6) {
                    if (!previousIssueCard()) {
                        goToSlide(5);
                    }
                } else if (currentSlideIndex === 2) {"""

new_back = """                } else if (currentSlideIndex === 6) {
                    if (!previousIssueCard()) {
                        goToSlide(5);
                    }
                } else if (currentSlideIndex === 7) {
                    if (slide7State === 1) {
                        const video7 = document.getElementById('demo-video-7');
                        if (video7) {
                            video7.pause();
                            video7.currentTime = 0;
                        }
                        slide7State = 0;
                    } else {
                        goToSlide(6);
                    }
                } else if (currentSlideIndex === 2) {"""

if old_back in text:
    text = text.replace(old_back, new_back)

# 6. Update goToSlide to pause/reset video7
old_goto = """            if (index === 6) {
                startIssueCarousel();
                startIssuePhotoRotator();
            } else {
                stopIssueCarousel();
                stopIssuePhotoRotator();
            }"""

new_goto = """            if (index === 6) {
                startIssueCarousel();
                startIssuePhotoRotator();
            } else {
                stopIssueCarousel();
                stopIssuePhotoRotator();
            }

            if (index === 7) {
                slide7State = 0;
                const video7 = document.getElementById('demo-video-7');
                if (video7) {
                    video7.pause();
                    video7.currentTime = 0;
                }
            } else {
                const video7 = document.getElementById('demo-video-7');
                if (video7) video7.pause();
            }"""

if old_goto in text and 'index === 7' not in text:
    text = text.replace(old_goto, new_goto)

# 7. Update TOC Click Event
old_toc_click = """                } else if (index === 3) {
                    goToSlide(6); // 4. 개발 중 이슈사항 -> 6페이지
                }
            });"""

new_toc_click = """                } else if (index === 3) {
                    goToSlide(6); // 4. 개발 중 이슈사항 -> 6페이지
                } else if (index === 4) {
                    goToSlide(7); // 5. 시연영상 -> 7페이지
                }
            });"""

if old_toc_click in text:
    text = text.replace(old_toc_click, new_toc_click)

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Slide 7 added successfully.')

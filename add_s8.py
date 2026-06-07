import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update totalSlides
text = re.sub(r'const totalSlides = \d+;', 'const totalSlides = 9;', text)

# 2. Add CSS
css_to_add = """
        /* 8페이지 3D 캐러셀 스타일 */
        .carousel-3d-container {
            perspective: 1500px;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .carousel-3d-card {
            position: absolute;
            width: 500px;
            height: 650px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            padding: 50px 40px;
            transition: all 0.7s cubic-bezier(0.25, 0.8, 0.25, 1);
            transform-style: preserve-3d;
            display: flex;
            flex-direction: column;
            gap: 30px;
        }

        .carousel-3d-card.active {
            transform: translateX(0) scale(1) translateZ(0);
            opacity: 1;
            z-index: 10;
        }

        .carousel-3d-card.prev {
            transform: translateX(-450px) scale(0.85) translateZ(-300px) rotateY(25deg);
            opacity: 0.5;
            z-index: 5;
        }

        .carousel-3d-card.next {
            transform: translateX(450px) scale(0.85) translateZ(-300px) rotateY(-25deg);
            opacity: 0.5;
            z-index: 5;
        }

        .carousel-3d-card.hidden-left {
            transform: translateX(-800px) scale(0.6) translateZ(-600px) rotateY(40deg);
            opacity: 0;
            z-index: 1;
        }

        .carousel-3d-card.hidden-right {
            transform: translateX(800px) scale(0.6) translateZ(-600px) rotateY(-40deg);
            opacity: 0;
            z-index: 1;
        }

        .card-member-name {
            font-size: 2.5em;
            font-weight: 800;
            color: var(--accent-primary);
            border-bottom: 4px solid var(--accent-secondary);
            padding-bottom: 15px;
            text-align: center;
            margin-bottom: 10px;
            letter-spacing: 0.1em;
        }
        
        .card-section h3 {
            font-size: 1.4em;
            color: var(--text-main);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-section ul {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .card-section li {
            font-size: 1.15em;
            line-height: 1.6;
            color: var(--text-muted);
            position: relative;
            padding-left: 25px;
            word-break: keep-all;
        }

        .card-section li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent-secondary);
            font-weight: bold;
            font-size: 1.2em;
        }
"""
if "carousel-3d-container" not in text:
    style_end = text.find('</style>')
    if style_end != -1:
        text = text[:style_end] + css_to_add + '    ' + text[style_end:]

# 3. Add HTML for Slide 8 and 9
html_to_add = """
        <!-- Slide 8: 팀원별 소감 -->
        <div class="slide" id="slide-8" style="justify-content: center; align-items: center; padding: 0;">
            <h2 class="title" style="position: absolute; top: 80px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 20; text-shadow: 0 4px 20px rgba(255,255,255,0.8);">
                팀원별 소감<br><span style="font-size: 0.4em; color: var(--text-muted); letter-spacing: 0.2em; font-weight: normal;">TEAM RETROSPECTIVE</span>
            </h2>
            
            <div class="carousel-3d-container" id="carousel-8">
                <!-- Card 1: 조예은 -->
                <div class="carousel-3d-card active">
                    <div class="card-member-name">조예은</div>
                    <div class="card-section">
                        <h3>💡 소감</h3>
                        <ul>
                            <li>XR Interactable Toolkit 사전 학습 및 적용 과정에서 깊은 배움을 얻음</li>
                            <li>Git 활용 능력이 크게 향상되었으며, 기획과 파트 분배의 중요성을 체감함</li>
                        </ul>
                    </div>
                    <div class="card-section">
                        <h3>🚀 발전 방향</h3>
                        <ul>
                            <li>액체가 담긴 컵의 출렁임과 같은 <strong>정밀한 물리 상호작용</strong> 구현 희망</li>
                            <li>멀티플레이어 기반의 본격적인 <strong>타이쿤 장르</strong>로의 게임 확장</li>
                        </ul>
                    </div>
                </div>

                <!-- Card 2: 황인용 -->
                <div class="carousel-3d-card next">
                    <div class="card-member-name">황인용</div>
                    <div class="card-section">
                        <h3>💡 소감</h3>
                        <ul>
                            <li>시뮬레이터 장르 특유의 디테일 구현 난이도와 중요성 체감</li>
                            <li>명확한 명세서 작성이 팀 프로젝트 소통에 필수적임을 인식</li>
                            <li>초기 기획 방향을 모두 담아내지 못한 점에 대한 아쉬움</li>
                        </ul>
                    </div>
                    <div class="card-section">
                        <h3>🚀 발전 방향</h3>
                        <ul>
                            <li>단순 시뮬레이터를 넘어, 복합적인 <strong>카페 운영(타이쿤) 시스템</strong> 도입 및 고도화</li>
                        </ul>
                    </div>
                </div>

                <!-- Card 3: 정해륜 -->
                <div class="carousel-3d-card hidden-right">
                    <div class="card-member-name">정해륜</div>
                    <div class="card-section">
                        <h3>💡 소감</h3>
                        <ul>
                            <li>VR 환경 내 물리 기반 상호작용 및 시스템 통합 경험 축적</li>
                            <li>단순 기능 구현을 넘어, <strong>현실감 있는 인터랙션 설계</strong>와 구조적 접근의 중요성 학습</li>
                        </ul>
                    </div>
                    <div class="card-section">
                        <h3>🚀 발전 방향</h3>
                        <ul>
                            <li>결과 중심 평가를 탈피하여, XR 장비(HMD/컨트롤러) 데이터를 활용한 <strong>사용자 동선 및 효율성 정량 분석</strong></li>
                            <li>맞춤형 피드백을 제공하는 <strong>XR 직무 훈련 전문 콘텐츠</strong>로의 확장 도약</li>
                        </ul>
                    </div>
                </div>

                <!-- Card 4: 최재빈 -->
                <div class="carousel-3d-card hidden-right">
                    <div class="card-member-name">최재빈</div>
                    <div class="card-section">
                        <h3>💡 소감</h3>
                        <ul>
                            <li>소비자 눈높이에 맞춘 <strong>대화형 AI 에이전트 개발</strong>의 실무적 어려움과 보람 체감</li>
                            <li>안정적인 프레임 확보와 저지연(Low-Latency)을 위해 Half-Duplex 최적화 선택</li>
                        </ul>
                    </div>
                    <div class="card-section">
                        <h3>🚀 발전 방향</h3>
                        <ul>
                            <li>대화형 AI 기술을 응용한 <strong>아바타 면접, 영어 회화, AI 스트리머</strong> 등 다목적 비즈니스 모델(BM) 창출</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <!-- ===== 8페이지 끝 ===== -->

        <!-- Slide 9: Q&A -->
        <div class="slide" id="slide-9" style="justify-content: center; align-items: center;">
            <div class="glass-panel" style="width: 80%; height: 60%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h2 style="font-size: 5em; color: var(--accent-primary); margin-bottom: 20px; font-weight: 900; letter-spacing: 0.1em;">Q & A</h2>
                <p style="font-size: 1.8em; color: var(--text-muted);">경청해 주셔서 감사합니다. 자유롭게 질문해 주세요!</p>
            </div>
        </div>
        <!-- ===== 9페이지 끝 ===== -->
"""

insert_target = '        <!-- ===== 7페이지 끝 ===== -->\n    </div>'
if insert_target in text and 'id="slide-8"' not in text:
    text = text.replace(insert_target, '        <!-- ===== 7페이지 끝 ===== -->\n' + html_to_add + '\n    </div>')


# 4. Add slide8State JS variable
state_target = 'let slide7State = 0; // 0: paused, 1: playing'
if state_target in text and 'let slide8State' not in text:
    text = text.replace(state_target, state_target + '\n        let slide8State = 0; // 0 to 3 for members')

# 5. Add updateSlide8Cards JS function
func_to_add = """
        function updateSlide8Cards() {
            const cards = document.querySelectorAll('#carousel-8 .carousel-3d-card');
            cards.forEach((card, index) => {
                card.className = 'carousel-3d-card'; // reset classes
                if (index === slide8State) {
                    card.classList.add('active');
                } else if (index === slide8State - 1) {
                    card.classList.add('prev');
                } else if (index === slide8State + 1) {
                    card.classList.add('next');
                } else if (index < slide8State - 1) {
                    card.classList.add('hidden-left');
                } else if (index > slide8State + 1) {
                    card.classList.add('hidden-right');
                }
            });
        }
"""
if "function updateSlide8Cards" not in text:
    script_start = text.find('<script>')
    if script_start != -1:
        text = text[:script_start+8] + func_to_add + text[script_start+8:]

# 6. Update Spacebar logic
old_space = """                } else if (currentSlideIndex === 7) {
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

new_space = """                } else if (currentSlideIndex === 7) {
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
                } else if (currentSlideIndex === 8) {
                    if (slide8State < 3) {
                        if (typeof playPopSound === 'function') playPopSound();
                        slide8State++;
                        updateSlide8Cards();
                    } else {
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    }
                } else if (currentSlideIndex < totalSlides) {"""

if old_space in text and 'currentSlideIndex === 8' not in text:
    text = text.replace(old_space, new_space)

# 7. Update Backspace logic
old_back = """                } else if (currentSlideIndex === 7) {
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

new_back = """                } else if (currentSlideIndex === 7) {
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
                } else if (currentSlideIndex === 8) {
                    if (slide8State > 0) {
                        if (typeof playPopSound === 'function') playPopSound();
                        slide8State--;
                        updateSlide8Cards();
                    } else {
                        goToSlide(7);
                    }
                } else if (currentSlideIndex === 2) {"""

if old_back in text:
    text = text.replace(old_back, new_back)

# 8. Reset slide8State in goToSlide
old_goto = """            if (index === 7) {
                slide7State = 0;"""

new_goto = """            if (index === 8) {
                slide8State = 0;
                updateSlide8Cards();
            }

            if (index === 7) {
                slide7State = 0;"""

if old_goto in text and 'index === 8' not in text:
    text = text.replace(old_goto, new_goto)

# 9. Update TOC Clicks
old_toc_click = """                } else if (index === 4) {
                    goToSlide(7); // 5. 시연영상 -> 7페이지
                }
            });"""

new_toc_click = """                } else if (index === 4) {
                    goToSlide(7); // 5. 시연영상 -> 7페이지
                } else if (index === 5) {
                    goToSlide(8); // 6. 팀원별 소감 -> 8페이지
                } else if (index === 6) {
                    goToSlide(9); // 7. Q&A -> 9페이지
                }
            });"""

if old_toc_click in text:
    text = text.replace(old_toc_click, new_toc_click)

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Slide 8 (3D Carousel) and 9 added successfully.")

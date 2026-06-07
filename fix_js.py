import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# 1. Add missing JS global variables and functions for Slide 6 from codex.html
slide6_funcs = """
        let issueCardIndex = 0;
        let issueAutoTimer = null;
        let issuePhotoTimer = null;
        let issuePhotoCursor = 0;

        function sortIssuePhotoSource(a, b) {
            const fileA = a.split('/').pop() || a;
            const fileB = b.split('/').pop() || b;
            const numberA = fileA.match(/^\d+(?=\.)/);
            const numberB = fileB.match(/^\d+(?=\.)/);
            if (numberA && numberB) {
                return Number(numberA[0]) - Number(numberB[0]) || fileA.localeCompare(fileB, 'ko-KR');
            }
            if (numberA) return -1;
            if (numberB) return 1;
            return fileA.localeCompare(fileB, 'ko-KR', { numeric: true, sensitivity: 'base' });
        }

        const issuePhotoSources = [
            "유니티images/6페이지/01.png",
            "유니티images/6페이지/02.png",
            "유니티images/6페이지/03.png",
            "유니티images/6페이지/04.png",
            "유니티images/6페이지/05.png",
            "유니티images/6페이지/2d 느낌 ChatGPT Image 2026년 5월 30일 오전 02_32_42.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오전 02_30_13.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오전 02_51_45.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오전 03_39_15.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오후 01_41_11.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오후 04_33_09.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 30일 오후 05_13_52.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 31일 오후 05_18_36.png",
            "유니티images/6페이지/ChatGPT Image 2026년 5월 31일 오후 06_02_11.png",
            "유니티images/6페이지/스크린샷 2026-05-30 023105.png",
            "유니티images/6페이지/스크린샷 2026-05-30 140805.png",
            "유니티images/6페이지/스크린샷 2026-05-30 140824.png",
            "유니티images/6페이지/스크린샷 2026-05-30 140841.png",
            "유니티images/6페이지/스크린샷 2026-05-30 140858.png",
            "유니티images/6페이지/스크린샷 2026-05-30 155537.png",
            "유니티images/6페이지/스크린샷 2026-05-30 155613.png",
            "유니티images/6페이지/스크린샷 2026-05-30 170714.png",
            "유니티images/6페이지/스크린샷 2026-05-30 170754.png",
            "유니티images/6페이지/스크린샷 2026-05-30 203102.png",
            "유니티images/6페이지/스크린샷 2026-05-31 175422.png",
            "유니티images/6페이지/스크린샷 2026-05-31 215430.png",
            "유니티images/6페이지/스크린샷 2026-06-03 141614.png",
            "유니티images/6페이지/스크린샷 2026-06-03 144944.png",
            "유니티images/6페이지/스크린샷 2026-06-07 130007.png",
            "유니티images/6페이지/스크린샷 2026-06-07 130016.png",
            "유니티images/6페이지/스크린샷 2026-06-07 130042.png",
            "유니티images/6페이지/일반손님.png",
            "유니티images/6페이지/진상손님.png",
            "유니티images/6페이지/틱톡커.png",
            "유니티images/6페이지/플레이어.png"
        ].sort(sortIssuePhotoSource);

        function showIssueCard(index, playSound = true) {
            const cards = Array.from(document.querySelectorAll('#slide-6 .issue-card'));
            const track = document.getElementById('issue-carousel-track');
            const dots = Array.from(document.querySelectorAll('#slide-6 .issue-dot'));
            const progressFill = document.getElementById('issue-progress-fill');
            if (!track || cards.length === 0) return false;

            const nextIndex = Math.max(0, Math.min(index, cards.length - 1));
            if (playSound && issueCardIndex !== nextIndex) {
                playPopSound();
            }

            issueCardIndex = nextIndex;
            track.style.transform = `translateX(-${issueCardIndex * 100}%)`;

            dots.forEach((dot, dotIndex) => {
                dot.classList.toggle('active', dotIndex === issueCardIndex);
            });

            if (progressFill) {
                progressFill.style.width = `${((issueCardIndex + 1) / cards.length) * 100}%`;
            }

            return true;
        }

        function nextIssueCard() {
            const cards = Array.from(document.querySelectorAll('#slide-6 .issue-card'));
            if (issueCardIndex < cards.length - 1) {
                showIssueCard(issueCardIndex + 1);
                return true;
            }
            return false;
        }

        function previousIssueCard() {
            if (issueCardIndex > 0) {
                showIssueCard(issueCardIndex - 1);
                return true;
            }
            return false;
        }

        function startIssueCarousel() {
            stopIssueCarousel();
            showIssueCard(0, false);
        }

        function stopIssueCarousel() {
            if (issueAutoTimer !== null) {
                clearInterval(issueAutoTimer);
                issueAutoTimer = null;
            }
        }

        function restartIssueCarousel() {
        }

        function setIssuePhoto(polaroid, src) {
            const img = polaroid.querySelector('img');
            if (!img || !src || img.getAttribute('src') === src) return;
            const nextImage = new Image();
            nextImage.onload = () => {
                polaroid.classList.add('is-switching');
                setTimeout(() => {
                    img.src = src;
                    requestAnimationFrame(() => {
                        polaroid.classList.remove('is-switching');
                    });
                }, 240);
            };
            nextImage.onerror = () => {
                const failedIndex = issuePhotoSources.indexOf(src);
                if (failedIndex >= 0) {
                    issuePhotoSources.splice(failedIndex, 1);
                    issuePhotoCursor = issuePhotoCursor % Math.max(issuePhotoSources.length, 1);
                }
            };
            nextImage.src = src;
        }

        function primeIssuePhotos() {
            document.querySelectorAll('#slide-6 .issue-polaroid img').forEach((img) => {
                img.onerror = () => {
                    const fallback = issuePhotoSources.find((src) => src !== img.getAttribute('src'));
                    if (fallback) {
                        const nextImage = new Image();
                        nextImage.onload = () => { img.src = fallback; };
                        nextImage.src = fallback;
                    }
                };
            });
        }

        function rotateIssuePhotos() {
            const slots = Array.from(document.querySelectorAll('#slide-6 .issue-polaroid'));
            if (slots.length === 0 || issuePhotoSources.length === 0) return;
            slots.forEach((slot, slotIndex) => {
                const sourceIndex = (issuePhotoCursor + slotIndex) % issuePhotoSources.length;
                setIssuePhoto(slot, issuePhotoSources[sourceIndex]);
            });
            issuePhotoCursor = (issuePhotoCursor + 1) % issuePhotoSources.length;
        }

        function startIssuePhotoRotator() {
            stopIssuePhotoRotator();
            primeIssuePhotos();
            rotateIssuePhotos();
            issuePhotoTimer = setInterval(rotateIssuePhotos, 2600);
        }

        function stopIssuePhotoRotator() {
            if (issuePhotoTimer !== null) {
                clearInterval(issuePhotoTimer);
                issuePhotoTimer = null;
            }
        }
"""
if "let issueCardIndex =" not in index:
    insert_pos = index.find('let memberCardIndex = 0;')
    if insert_pos != -1:
        insert_pos += len('let memberCardIndex = 0;')
        index = index[:insert_pos] + '\n' + slide6_funcs + index[insert_pos:]

# 2. Update goToSlide to call slide 6 logic
goto_search = "            if (index === 6) {\n                startIssueCarousel();\n                startIssuePhotoRotator();\n            } else {\n                stopIssueCarousel();\n                stopIssuePhotoRotator();\n            }"
if goto_search not in index:
    goto_insert = index.find('            // 5페이지 플로우 차트 타이핑 및 서브페이지 세팅')
    if goto_insert != -1:
        index = index[:goto_insert] + goto_search + '\n\n' + index[goto_insert:]

# 3. Update keydown - Spacebar for Slide 5 and Slide 6
old_space_slide5 = """                    } else if (slide5SubIndex === 3) {
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    } else if (currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex < totalSlides) {"""

new_space_slide5 = """                    } else if (slide5SubIndex >= 3 && slide5SubIndex < 6) {
                        showSlide5SubPage(slide5SubIndex + 1, 'next');
                    } else if (slide5SubIndex === 6) {
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    } else if (currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 6) {
                    if (!nextIssueCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex < totalSlides) {"""
if old_space_slide5 in index:
    index = index.replace(old_space_slide5, new_space_slide5)

# 4. Update keydown - Backspace for Slide 5 and Slide 6
old_back_slide5 = """                } else if (currentSlideIndex === 5) {
                    if (slide5SubIndex === 3) {
                        showSlide5SubPage(2, 'prev');
                    } else if (slide5SubIndex === 2) {"""
new_back_slide5 = """                } else if (currentSlideIndex === 5) {
                    if (slide5SubIndex > 3) {
                        showSlide5SubPage(slide5SubIndex - 1, 'prev');
                    } else if (slide5SubIndex === 3) {
                        showSlide5SubPage(2, 'prev');
                    } else if (slide5SubIndex === 2) {"""
if old_back_slide5 in index:
    index = index.replace(old_back_slide5, new_back_slide5)

old_back_slide6 = """                } else if (currentSlideIndex === 2) {"""
new_back_slide6 = """                } else if (currentSlideIndex === 6) {
                    if (!previousIssueCard()) {
                        goToSlide(5);
                    }
                } else if (currentSlideIndex === 2) {"""
if "currentSlideIndex === 6) {\n                    if (!previousIssueCard()) {" not in index:
    index = index.replace(old_back_slide6, new_back_slide6)

# Write updated content
with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Javascript fixed!")

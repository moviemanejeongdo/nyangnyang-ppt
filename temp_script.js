
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

        // 16:9 비율 반응형 자동 맞춤 스크립트
        function resizePresentation() {
            const presentation = document.getElementById('presentation');
            const windowRatio = window.innerWidth / window.innerHeight;
            const targetRatio = 1920 / 1080;
            let scale;

            if (windowRatio < targetRatio) {
                // 창이 16:9보다 좁은 경우 (가로 기준 맞춤)
                scale = window.innerWidth / 1920;
            } else {
                // 창이 16:9보다 넓은 경우 (세로 기준 맞춤)
                scale = window.innerHeight / 1080;
            }
            presentation.style.transform = `scale(${scale})`;
        }

        window.addEventListener('resize', resizePresentation);
        resizePresentation(); // 초기 로드 시 실행

        // 귀여운 '뿅' 사운드를 재생하는 Web Audio API 함수
        function playPopSound() {
            // 사용자의 요청에 따라 뿅뿅 효과음을 재생하지 않도록 비워둡니다.
        }

        // 문 열리는 사운드 재생 (합성음)
        function playDoorOpenSound() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                // 슬라이딩 도어(드르륵 스르륵) 사운드 생성
                const bufferSize = audioCtx.sampleRate * 1.5; // 1.5초
                const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                const data = buffer.getChannelData(0);

                for (let i = 0; i < bufferSize; i++) {
                    // 갈리는 듯한 화이트 노이즈
                    data[i] = Math.random() * 2 - 1;
                }

                const noiseSource = audioCtx.createBufferSource();
                noiseSource.buffer = buffer;

                // 문이 밀리는 듯한 주파수 변화를 위한 필터
                const filter = audioCtx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(100, audioCtx.currentTime);
                filter.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.8);
                filter.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 1.5);

                // 볼륨 페이드
                const gainNode = audioCtx.createGain();
                gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
                gainNode.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + 0.2);
                gainNode.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.8);
                gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 1.5);

                noiseSource.connect(filter);
                filter.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                noiseSource.start();
            } catch (e) {
                console.log('Door audio failed', e);
            }
        }

        const bgmJazz = new Audio('sound/BGM재즈_sergequadrado-luxury-jazz-loop-312713.mp3');
        bgmJazz.loop = true;

        let bgmFadeInterval = null;

        function fadeAudio(audio, targetVolume, duration = 1000) {
            if (bgmFadeInterval) {
                clearInterval(bgmFadeInterval);
                bgmFadeInterval = null;
            }

            // 재생 시작 시 볼륨이 아직 0인 경우 play() 호출 필수
            if (targetVolume > 0 && audio.paused) {
                audio.volume = 0;
                audio.play().catch(e => console.log('BGM play failed:', e));
            }

            const stepTime = 50;
            const steps = duration / stepTime;
            const volumeStep = (targetVolume - audio.volume) / steps;

            bgmFadeInterval = setInterval(() => {
                let nextVolume = audio.volume + volumeStep;

                if ((volumeStep > 0 && nextVolume >= targetVolume) ||
                    (volumeStep < 0 && nextVolume <= targetVolume)) {
                    audio.volume = targetVolume;
                    clearInterval(bgmFadeInterval);
                    bgmFadeInterval = null;
                    if (targetVolume === 0) {
                        audio.pause();
                        audio.currentTime = 0;
                    }
                } else {
                    audio.volume = Math.max(0, Math.min(1, nextVolume));
                }
            }, stepTime);
        }

        let currentSlideIndex = 1;
let slide5State = 0;
        const totalSlides = 10;

        let introState = 0; // 0: 초기(숨김), 1: 텍스트&메이드 등장, 2: 이후 슬라이드 이동
        let tocAutoTimer = null;
        let tocAutoIndex = 0;
        const memberBgIntervalSeconds = 2;
        let memberBgTimer = null;
        let memberBgIndex = 0;
        let memberCardIndex = 0;

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
            "유니티images/7페이지/01.png",
            "유니티images/7페이지/02.png",
            "유니티images/7페이지/03.png",
            "유니티images/7페이지/04.png",
            "유니티images/7페이지/05.png",
            "유니티images/7페이지/06.png",
            "유니티images/7페이지/07.png",
            "유니티images/7페이지/08.png",
            "유니티images/7페이지/11.png",
            "유니티images/7페이지/12.png",
            "유니티images/7페이지/13.png",
            "유니티images/7페이지/14.png",
            "유니티images/7페이지/15.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오전 02_30_13.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오전 02_51_45.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오전 03_39_15.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오후 01_41_11.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오후 04_33_09.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 30일 오후 05_13_52.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 31일 오후 05_18_36.png",
            "유니티images/7페이지/ChatGPT Image 2026년 5월 31일 오후 06_02_11.png",
            "유니티images/7페이지/스크린샷 2026-05-30 023105.png",
            "유니티images/7페이지/스크린샷 2026-05-30 140805.png",
            "유니티images/7페이지/스크린샷 2026-05-30 140824.png",
            "유니티images/7페이지/스크린샷 2026-05-30 140841.png",
            "유니티images/7페이지/스크린샷 2026-05-30 140858.png",
            "유니티images/7페이지/스크린샷 2026-05-30 155537.png",
            "유니티images/7페이지/스크린샷 2026-05-30 155613.png",
            "유니티images/7페이지/스크린샷 2026-05-30 170714.png",
            "유니티images/7페이지/스크린샷 2026-05-30 203102.png",
            "유니티images/7페이지/스크린샷 2026-05-31 175422.png",
            "유니티images/7페이지/스크린샷 2026-05-31 215430.png",
            "유니티images/7페이지/스크린샷 2026-06-03 141614.png",
            "유니티images/7페이지/스크린샷 2026-06-03 144944.png",
            "유니티images/7페이지/스크린샷 2026-06-07 130007.png",
            "유니티images/7페이지/스크린샷 2026-06-07 130016.png",
            "유니티images/7페이지/스크린샷 2026-06-07 130042.png",
            "유니티images/7페이지/스크린샷 2026-06-07 152341.png",
            "유니티images/7페이지/스크린샷 2026-06-07 152358.png",
            "유니티images/7페이지/일반손님.png",
            "유니티images/7페이지/진상손님.png"
        ];

        function showIssueCard(index, playSound = true) {
            const cards = Array.from(document.querySelectorAll('#slide-8 .issue-card'));
            const track = document.getElementById('issue-carousel-track');
            const dots = Array.from(document.querySelectorAll('#slide-8 .issue-dot'));
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

            if (issueCardIndex === 1) {
                stopIssuePhotoRotator();
                const field = document.querySelector('#slide-8 .issue-photo-field');
                if (field) field.classList.add('steam-mode');
                const slots = Array.from(document.querySelectorAll('#slide-8 .issue-polaroid'));
                if (slots.length >= 2) {
                    setIssuePhoto(slots[0], "유니티images/7페이지/steam1.gif");
                    setIssuePhoto(slots[1], "유니티images/7페이지/steam2.gif");
                }
            } else {
                const field = document.querySelector('#slide-8 .issue-photo-field');
                if (field) field.classList.remove('steam-mode');
                if (issuePhotoTimer === null) {
                    startIssuePhotoRotator();
                }
            }

            return true;
        }

        function nextIssueCard() {
            const cards = Array.from(document.querySelectorAll('#slide-8 .issue-card'));
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
            document.querySelectorAll('#slide-8 .issue-polaroid img').forEach((img) => {
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
            const slots = Array.from(document.querySelectorAll('#slide-8 .issue-polaroid'));
            if (slots.length === 0 || issuePhotoSources.length === 0) return;
            slots.forEach((slot, slotIndex) => {
                const sourceIndex = (issuePhotoCursor + slotIndex) % issuePhotoSources.length;
                setIssuePhoto(slot, issuePhotoSources[sourceIndex]);
            });
            issuePhotoCursor = (issuePhotoCursor + 1) % issuePhotoSources.length;
        }

        function startIssuePhotoRotator() {
            stopIssuePhotoRotator();
            issuePhotoCursor = 0;
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


        function showMemberCard(index) {
            const cards = Array.from(document.querySelectorAll('#slide-3 .member-card'));
            const dots = Array.from(document.querySelectorAll('#slide-3 .member-dot'));
            const progress = document.getElementById('member-progress');
            if (cards.length === 0) return;

            const nextIndex = Math.max(0, Math.min(index, cards.length - 1));

            // 카드가 실제로 변경될 때만 뿅 효과음 재생
            if (memberCardIndex !== nextIndex) {
                playPopSound();
            }

            cards.forEach((card, cardIndex) => {
                const wasActive = card.classList.contains('is-active');
                card.classList.toggle('is-active', cardIndex === nextIndex);
                card.classList.toggle('is-exiting', wasActive && cardIndex !== nextIndex);

                if (wasActive && cardIndex !== nextIndex) {
                    setTimeout(() => {
                        card.classList.remove('is-exiting');
                    }, 650);
                }
            });

            dots.forEach((dot, dotIndex) => {
                dot.classList.toggle('is-active', dotIndex === nextIndex);
            });

            if (progress) {
                progress.textContent = `${String(nextIndex + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
            }

            memberCardIndex = nextIndex;
        }

        function nextMemberCard() {
            const cards = Array.from(document.querySelectorAll('#slide-3 .member-card'));
            if (memberCardIndex < cards.length - 1) {
                showMemberCard(memberCardIndex + 1);
                return true;
            }

            return false;
        }

        function previousMemberCard() {
            if (memberCardIndex > 0) {
                showMemberCard(memberCardIndex - 1);
                return true;
            }

            return false;
        }

        function rotateMemberBackground() {
            const rotator = document.querySelector('.members-bg-rotator');
            const imageList = Array.isArray(window.SLIDE3_BACKGROUND_IMAGES) ? window.SLIDE3_BACKGROUND_IMAGES : [];
            if (!rotator || imageList.length === 0) return;

            // 1. 기존 클래스별 카드들 선택
            const cardTL = rotator.querySelector('.polaroid-card.pos-tl');
            const cardTR = rotator.querySelector('.polaroid-card.pos-tr');
            const cardBR = rotator.querySelector('.polaroid-card.pos-br');
            const cardBL = rotator.querySelector('.polaroid-card.pos-bl');
            const cardEnter = rotator.querySelector('.polaroid-card.pos-enter');

            // 2. BL -> Exit (빠져나감)
            if (cardBL) {
                cardBL.className = 'polaroid-card pos-exit';
                setTimeout(() => {
                    cardBL.remove();
                }, 850); // 트랜지션 완료 후 제거
            }

            // 3. BR -> BL
            if (cardBR) {
                cardBR.className = 'polaroid-card pos-bl';
            }

            // 4. TR -> BR
            if (cardTR) {
                cardTR.className = 'polaroid-card pos-br';
            }

            // 5. TL -> TR
            if (cardTL) {
                cardTL.className = 'polaroid-card pos-tr';
            }

            // 6. Enter -> TL (새로 들어옴)
            if (cardEnter) {
                cardEnter.className = 'polaroid-card pos-tl';
            }

            // 7. 다음 번 유입을 위한 신규 카드를 pos-enter 상태로 추가
            const nextSrc = imageList[memberBgIndex];
            memberBgIndex = (memberBgIndex + 1) % imageList.length;

            const newCard = document.createElement('div');
            newCard.className = 'polaroid-card pos-enter';

            const newImg = document.createElement('img');
            newImg.src = nextSrc;
            newImg.alt = '';
            newImg.loading = 'lazy';
            newCard.appendChild(newImg);

            rotator.appendChild(newCard);
        }

        function startMemberBackgroundRotator() {
            stopMemberBackgroundRotator();

            const imageList = Array.isArray(window.SLIDE3_BACKGROUND_IMAGES) ? window.SLIDE3_BACKGROUND_IMAGES : [];
            if (imageList.length <= 4 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

            memberBgTimer = setInterval(() => {
                rotateMemberBackground();
            }, memberBgIntervalSeconds * 1000);
        }

        function stopMemberBackgroundRotator() {
            if (memberBgTimer !== null) {
                clearInterval(memberBgTimer);
                memberBgTimer = null;
            }
        }

        function setupMemberBackgroundRotator() {
            const rotator = document.querySelector('.members-bg-rotator');
            const imageList = Array.isArray(window.SLIDE3_BACKGROUND_IMAGES) ? window.SLIDE3_BACKGROUND_IMAGES : [];

            if (!rotator || imageList.length === 0) return;

            rotator.innerHTML = '';

            // 초기 4개 카드를 각각 알맞은 위치에 생성
            const initialPositions = ['pos-tl', 'pos-tr', 'pos-br', 'pos-bl'];
            for (let i = 0; i < 4; i++) {
                const src = imageList[i % imageList.length];
                const card = document.createElement('div');
                card.className = `polaroid-card ${initialPositions[i]}`;

                const img = document.createElement('img');
                img.src = src;
                img.alt = '';
                img.loading = 'eager';

                card.appendChild(img);
                rotator.appendChild(card);
            }

            // 다음에 들어올 이미지의 인덱스는 4
            memberBgIndex = 4 % imageList.length;

            // 다음을 위해 미리 enter 위치에 카드를 하나 만들어 둔다.
            const nextSrc = imageList[memberBgIndex];
            memberBgIndex = (memberBgIndex + 1) % imageList.length;

            const enterCard = document.createElement('div');
            enterCard.className = 'polaroid-card pos-enter';

            const enterImg = document.createElement('img');
            enterImg.src = nextSrc;
            enterImg.alt = '';
            enterImg.loading = 'lazy';

            enterCard.appendChild(enterImg);
            rotator.appendChild(enterCard);

            startMemberBackgroundRotator();
        }

        function clearTocAutoHighlight() {
            document.querySelectorAll('#slide-2 .toc-item').forEach(item => item.classList.remove('auto-active'));
        }

        function startTocAutoHighlight() {
            stopTocAutoHighlight();

            const items = Array.from(document.querySelectorAll('#slide-2 .toc-item'));
            if (items.length === 0) return;

            tocAutoIndex = 0;
            items[tocAutoIndex].classList.add('auto-active');

            tocAutoTimer = setInterval(() => {
                items[tocAutoIndex].classList.remove('auto-active');
                tocAutoIndex = (tocAutoIndex + 1) % items.length;
                items[tocAutoIndex].classList.add('auto-active');
            }, 1000);
        }

        function stopTocAutoHighlight() {
            if (tocAutoTimer !== null) {
                clearInterval(tocAutoTimer);
                tocAutoTimer = null;
            }

            clearTocAutoHighlight();
        }

        let slide5SubIndex = 1;
        let slide5Sub2State = 0;
        let slide7State = 0; // 0: paused, 1: playing
        let slide8State = 0; // 0 to 3 for members // 0: clear, 1~3: cards, 4: video playing, 5: end

        function showSlide5SubPage(targetIndex, direction = 'next') {
            const subPages = Array.from(document.querySelectorAll('#slide-6 .slide5-sub-page'));
            const sub1 = document.getElementById('slide5-sub-1');
            const sub2 = document.getElementById('slide5-sub-2');
            const activeSub = subPages[targetIndex - 1];
            if (!sub1 || !sub2 || !activeSub) return;

            // 5-2 서브페이지 진입/이탈 시 초기화 로직
            const headerExtras = document.getElementById('slide5-sub2-header-extras');
            if (targetIndex === 2) {
                if (headerExtras) headerExtras.style.opacity = '1';
                slide5Sub2State = 0;
                const cards = sub2.querySelectorAll('.server-card-v2');
                cards.forEach(card => {
                    card.classList.remove('active');
                });
                const track = document.getElementById('carousel-track-v2');
                if (track) track.style.transform = `translateY(0px)`;
                const thumbVideo = sub2.querySelector('.card-video-container video');
                if (thumbVideo) thumbVideo.play();
            } else if (targetIndex === 1) {
                if (headerExtras) headerExtras.style.opacity = '0';
                const thumbVideo = sub2.querySelector('.card-video-container video');
                if (thumbVideo) thumbVideo.pause();
                const popupVideo = document.getElementById('server-popup-video');
                if (popupVideo) popupVideo.pause();
            } else if (targetIndex >= 3) {
                if (headerExtras) headerExtras.style.opacity = '0';
                const thumbVideo = sub2.querySelector('.floating-video-thumbnail video');
                if (thumbVideo) thumbVideo.pause();
                const popupVideo = document.getElementById('server-popup-video');
                if (popupVideo) popupVideo.pause();
            }

            // 효과음 재생 (슬라이드가 바뀔 때만)
            if (slide5SubIndex !== targetIndex) {
                playPopSound();
            }

            // duplicate removed
            const inactiveSubs = subPages.filter(page => page !== activeSub);

            if (direction === 'next') {
                // 뒤로 물러남 (exit-left)
                inactiveSubs.forEach(page => {
                    page.classList.remove('active', 'exit-right');
                    page.classList.add('exit-left');
                });

                // 오른쪽에서 진입
                activeSub.classList.remove('exit-left');
                activeSub.classList.add('exit-right');
                activeSub.offsetHeight; // force reflow
                activeSub.classList.remove('exit-right');
                activeSub.classList.add('active');
            } else {
                // 앞으로 물러남 (exit-right)
                inactiveSubs.forEach(page => {
                    page.classList.remove('active', 'exit-left');
                    page.classList.add('exit-right');
                });

                // 왼쪽에서 진입
                activeSub.classList.remove('exit-right');
                activeSub.classList.add('exit-left');
                activeSub.offsetHeight; // force reflow
                activeSub.classList.remove('exit-left');
                activeSub.classList.add('active');
            }

            slide5SubIndex = targetIndex;

            // 5-1 플로우차트면 타이핑 애니메이션 실행 및 비디오 정지
            if (targetIndex === 1) {
                startFlowchartTyping();
                const video = sub2.querySelector('video');
                if (video) video.pause();
            } else if (targetIndex === 2) {
                // 5-2면 타이핑 애니메이션 정지 (비디오는 스페이스바 순차 제어로만 재생)
                if (typingTimer) {
                    clearInterval(typingTimer);
                    typingTimer = null;
                }
                const container = document.getElementById('flowchart-typing-text');
                if (container) container.textContent = '';

                // 비디오는 재생하지 않음 — slide5Sub2State 순차 로직에서만 재생
                const video = sub2.querySelector('video');
                if (video) {
                    video.muted = false;
                    video.volume = 0.5;
                    video.currentTime = 0;
                    video.pause();
                }
            } else {
                if (typingTimer) {
                    clearInterval(typingTimer);
                    typingTimer = null;
                }
                const container = document.getElementById('flowchart-typing-text');
                if (container) container.textContent = '';
            }
        }

        // 6페이지 타이핑 애니메이션 데이터 및 헬퍼
        const typingText = `로그인 -> 손님 입장 -> 응대 점수 달성 -> 음료 제작 -> 음료 전달`;

        let typingIndex = 0;
        let typingTimer = null;

        function startFlowchartTyping() {
            const container = document.getElementById('flowchart-typing-text');
            if (!container) return;

            if (typingTimer) {
                clearInterval(typingTimer);
                typingTimer = null;
            }
            container.textContent = '';
            typingIndex = 0;

            typingTimer = setInterval(() => {
                if (typingIndex < typingText.length) {
                    container.textContent += typingText.charAt(typingIndex);
                    typingIndex++;
                } else {
                    clearInterval(typingTimer);
                    typingTimer = null;
                }
            }, 30); // 30ms 간격으로 출력
        }

        // 페이지 이동 함수
        
        // 통합 페이지 번호 계산
        function updateStepCounter() {
            let currentStep = 0;
            let totalSteps = 0;

            // Wait, cardsLen was from #slide-6 (Key Features). But Key Features will become #slide-7.
            const cardsLen = document.querySelectorAll('#slide-7 .server-card-v2').length || 3;
            // issueCardsLen was from #slide-8. But Issues will become #slide-9.
            const issueCardsLen = document.querySelectorAll('#slide-9 .issue-card').length || 5;

            const stepsPerSlide = {
                1: 3, 
                2: 1,
                3: 4, 
                4: 1,
                5: 2, // Dev Env cascade
                6: 1 + (cardsLen + 2) + 1, // Key Features
                7: 2, // demo video
                8: issueCardsLen, // issues
                9: 4, 
                10: 1
            };

            for (let i = 1; i <= 10; i++) {
                totalSteps += stepsPerSlide[i] || 1;
            }

            for (let i = 1; i < currentSlideIndex; i++) {
                currentStep += stepsPerSlide[i] || 1;
            }

            if (currentSlideIndex === 1) {
                currentStep += (typeof introState !== 'undefined' ? introState + 1 : 1);
            } else if (currentSlideIndex === 3) {
                currentStep += (typeof memberCardIndex !== 'undefined' ? memberCardIndex + 1 : 1);
            } else if (currentSlideIndex === 5) {
                currentStep += (typeof slide5State !== 'undefined' ? slide5State + 1 : 1);
            } else if (currentSlideIndex === 7) {
                if (typeof slide5SubIndex !== 'undefined') { // the variable name is still slide5SubIndex!
                    if (slide5SubIndex === 1) {
                        currentStep += 1;
                    } else if (slide5SubIndex === 2) {
                        currentStep += 1 + (typeof slide5Sub2State !== 'undefined' ? slide5Sub2State + 1 : 1);
                    } else if (slide5SubIndex === 3) {
                        currentStep += 1 + (cardsLen + 2) + 1;
                    }
                } else {
                    currentStep += 1;
                }
            } else if (currentSlideIndex === 8) {
                currentStep += (typeof slide7State !== 'undefined' ? slide7State + 1 : 1);
            } else if (currentSlideIndex === 9) {
                currentStep += (typeof issueCardIndex !== 'undefined' ? issueCardIndex + 1 : 1);
            } else if (currentSlideIndex === 10) {
                currentStep += (typeof slide8State !== 'undefined' ? slide8State + 1 : 1);
            } else {
                currentStep += 1;
            }

            const navElement = document.getElementById('nav-current');
            if (navElement) {
                navElement.innerText = `${currentStep} / ${totalSteps}`;
            }
        }

        function goToSlide(index) {
            // 1페이지에서 2페이지로 넘어갈 때는 문 소리가 나므로 뿅 소리 생략, 그 외 슬라이드 전환 시 뿅 효과음 재생
            if (!(currentSlideIndex === 1 && index === 2)) {
                playPopSound();
            }
            stopTocAutoHighlight();
            document.querySelectorAll('.slide').forEach(slide => slide.classList.remove('active'));
            document.getElementById(`slide-${index}`).classList.add('active');
            currentSlideIndex = index;
            updateStepCounter();

            if (index === 2) {
                startTocAutoHighlight();
                // fadeAudio(bgmJazz, 1.0, 1500); // 1.5초 동안 서서히 페이드인 (배경음악 제거)
            } else {
                // fadeAudio(bgmJazz, 0, 1000);   // 1초 동안 서서히 페이드아웃 후 pause (배경음악 제거)
            }

            if (index === 3) {
                showMemberCard(0);
                startMemberBackgroundRotator();
            } else {
                stopMemberBackgroundRotator();
            }

            if (index === 6) {
                startIssueCarousel();
                startIssuePhotoRotator();
            } else {
                stopIssueCarousel();
                stopIssuePhotoRotator();
            }

            if (index === 8) {
                slide8State = 0;
                updateSlide8Cards();
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
            }

            // 6페이지 플로우 차트 타이핑 및 서브페이지 세팅
            if (index === 5) {
                showSlide5SubPage(1, 'next');
            } else {
                if (typingTimer) {
                    clearInterval(typingTimer);
                    typingTimer = null;
                }
                const container = document.getElementById('flowchart-typing-text');
                if (container) container.textContent = '';

                // 6페이지 이탈 시 비디오 정지 처리
                const sub2 = document.getElementById('slide5-sub-2');
                if (sub2) {
                    const video = sub2.querySelector('video');
                    if (video) video.pause();
                }
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault(); // 스페이스바 스크롤 방지

                if (currentSlideIndex === 1) {
                    if (introState === 0) {
                        // 1. 벽 뒤에서 메이드가 45도로 갸우뚱하며 나오고, 텍스트 페이드 인
                        playPopSound(); // 뿅! 사운드 재생
                        document.getElementById('maid-image').classList.remove('hide');
                        document.getElementById('maid-image').classList.add('show');
                        document.getElementById('intro-title').classList.add('show');
                        document.getElementById('intro-subtitle').classList.add('show');
                        document.getElementById('intro-team').classList.add('show');
                        introState = 1;
                    } else if (introState === 1) {
                        // 2. Spline 느낌의 부드러운 블러 & 무빙 오빗 트랜지션
                        const transition = document.getElementById('spline-transition');
                        transition.classList.add('active'); // 서서히 블러가 깔리고 빛이 퍼짐

                        playDoorOpenSound(); // 사운드 재생

                        setTimeout(() => {
                            goToSlide(2); // 화면이 완전히 몽환적으로 블러 처리됐을 때 슬라이드 2로 교체

                            setTimeout(() => {
                                transition.classList.remove('active'); // 서서히 블러가 걷히며 2페이지 등장
                            }, 300);
                        }, 1500); // 1.5초 대기 (블러와 빛이 최대로 찼을 때)

                        introState = 2; // 이후 슬라이드 이동 상태
                    }
                } else if (currentSlideIndex === 3) {
                    if (!nextMemberCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 5) {
                    if (slide5State === 0) {
                        slide5State = 1;
                        document.querySelectorAll('#slide-5 .env-card').forEach((card, i) => {
                            setTimeout(() => {
                                card.style.opacity = '1';
                                card.style.transform = 'translateY(0)';
                            }, i * 100);
                        });
                        updateStepCounter();
                    } else {
                        if (currentSlideIndex < totalSlides) goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 6) {
                    if (slide5SubIndex === 1) {
                        showSlide5SubPage(2, 'next');
                    } else if (slide5SubIndex === 2) {
                        const modal = document.getElementById('server-video-modal');

                        const cards = document.querySelectorAll('#slide5-sub-2 .server-card-v2');

                        if (slide5Sub2State < cards.length) {
                            playPopSound();

                            cards.forEach(c => c.classList.remove('active'));
                            const activeCard = cards[slide5Sub2State];
                            activeCard.classList.add('active');

                            const viewport = document.getElementById('carousel-viewport-v2');
                            const track = document.getElementById('carousel-track-v2');

                            if (viewport && track) {
                                const cardTop = activeCard.offsetTop;
                                const targetY = 280 - cardTop; // 수직 중앙으로 더 내려오도록 100 -> 280으로 변경

                                track.style.transform = `translateY(${targetY}px)`;
                            }

                            slide5Sub2State++;
                        } else if (slide5Sub2State === cards.length) {
                            // 한 번에 모달 열기 및 비디오 재생
                            const modal = document.getElementById('server-video-modal');
                            const popupVideo = document.getElementById('server-popup-video');
                            if (modal) {
                                if (typeof playPopSound === 'function') playPopSound();
                                modal.classList.add('open');
                            }
                            if (popupVideo) {
                                popupVideo.play();
                            }
                            slide5Sub2State++;
                        } else if (slide5Sub2State >= cards.length + 1) {
                            // 다시 스페이스바 누르면 모달 닫고 다음 페이즈로 이동
                            const modal = document.getElementById('server-video-modal');
                            const popupVideo = document.getElementById('server-popup-video');
                            if (modal && modal.classList.contains('open')) {
                                modal.classList.remove('open');
                                if (popupVideo) popupVideo.pause();
                            }
                            showSlide5SubPage(3, 'next');
                        }
                    } else if (slide5SubIndex >= 3 && slide5SubIndex < 6) {
                        showSlide5SubPage(slide5SubIndex + 1, 'next');
                    } else if (slide5SubIndex === 6) {
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    } else if (currentSlideIndex < totalSlides) {
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
                } else if (currentSlideIndex === 8) {
                    if (!nextIssueCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 9) {
                    if (slide8State < 3) {
                        if (typeof playPopSound === 'function') playPopSound();
                        slide8State++;
                        updateSlide8Cards();
                    } else {
                        if (currentSlideIndex < totalSlides) {
                            goToSlide(currentSlideIndex + 1);
                        }
                    }
                } else if (currentSlideIndex < totalSlides) {
                    // 1번 슬라이드 이후 일반적인 다음 슬라이드 전환
                    goToSlide(currentSlideIndex + 1);
                }
            } else if (e.code === 'Backspace') {
                e.preventDefault(); // 백스페이스 뒤로가기 기본 동작 방지

                if (currentSlideIndex === 3) {
                    if (!previousMemberCard()) {
                        goToSlide(2);
                    }
                } else if (currentSlideIndex === 6) {
                    if (slide5SubIndex > 3) {
                        showSlide5SubPage(slide5SubIndex - 1, 'prev');
                    } else if (slide5SubIndex === 3) {
                        showSlide5SubPage(2, 'prev');
                    } else if (slide5SubIndex === 2) {
                        if (slide5Sub2State > 0) {
                            const cards = document.querySelectorAll('#slide5-sub-2 .server-card-v2');
                            const modal = document.getElementById('server-video-modal');
                            const popupVideo = document.getElementById('server-popup-video');

                            if (slide5Sub2State === cards.length + 1) {
                                // 비디오 재생 취소 및 모달 닫기
                                if (popupVideo) {
                                    popupVideo.pause();
                                    popupVideo.currentTime = 0;
                                }
                                if (modal) {
                                    modal.classList.remove('open');
                                }
                                slide5Sub2State--;
                            } else {
                                // 캐러셀 이전 상태로
                                slide5Sub2State--;
                                cards.forEach(c => c.classList.remove('active'));
                                
                                if (slide5Sub2State > 0) {
                                    const activeCard = cards[slide5Sub2State - 1];
                                    activeCard.classList.add('active');
                                    
                                    const track = document.getElementById('carousel-track-v2');
                                    if (track) {
                                        const cardTop = activeCard.offsetTop;
                                        const targetY = 280 - cardTop; // 수직 중앙으로 더 내려오도록 100 -> 280으로 변경
                                        track.style.transform = `translateY(${targetY}px)`;
                                    }
                                } else {
                                    const track = document.getElementById('carousel-track-v2');
                                    if (track) track.style.transform = `translateY(0px)`;
                                }
                            }
                        } else {
                            showSlide5SubPage(1, 'prev');
                        }
                    } else {
                        goToSlide(4);
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
                } else if (currentSlideIndex === 8) {
                    if (!previousIssueCard()) {
                        goToSlide(7);
                    }
                } else if (currentSlideIndex === 9) {
                    if (slide8State > 0) {
                        if (typeof playPopSound === 'function') playPopSound();
                        slide8State--;
                        updateSlide8Cards();
                    } else {
                        goToSlide(8);
                    }
                } else if (currentSlideIndex === 2) {
                    // 2페이지에서 백스페이스 누르면 1페이지로 돌아감
                    goToSlide(1);
                    // 1페이지로 돌아오면 텍스트가 띄워진 상태로 유지
                    introState = 1;
                } else if (currentSlideIndex > 2) {
                    // 그 외 페이지는 이전 페이지로
                    goToSlide(currentSlideIndex - 1);
                } else if (currentSlideIndex === 1 && introState > 0) {
                    // 1페이지에서 텍스트가 떠있는 상태면 다시 벽 뒤로 숨김
                    document.getElementById('maid-image').classList.remove('show');
                    document.getElementById('maid-image').classList.add('hide');
                    document.getElementById('intro-title').classList.remove('show');
                    document.getElementById('intro-subtitle').classList.remove('show');
                    document.getElementById('intro-team').classList.remove('show');
                    introState = 0;
                }
            }
        });
    updateStepCounter();

        setupMemberBackgroundRotator();

        // 목차 클릭 시 해당 슬라이드로 즉시 이동하도록 바인딩
        document.querySelectorAll('#slide-2 .toc-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                if (index === 0) {
                    goToSlide(3); // 1. 멤버 소개 -> 3페이지
                } else if (index === 1) {
                    goToSlide(4); // 2. 프로젝트 개요 -> 4페이지
                } else if (index === 2) {
                    goToSlide(5); // 3. 개발 환경 -> 5페이지
                } else if (index === 3) {
                    goToSlide(6); // 4. 주요 기능 구현 -> 6페이지
                } else if (index === 4) {
                    goToSlide(7); // 5. 시연영상 -> 7페이지
                } else if (index === 5) {
                    goToSlide(8); // 6. 개발 중 이슈사항 -> 8페이지
                } else if (index === 6) {
                    goToSlide(9); // 7. 팀원별 소감 -> 9페이지
                } else if (index === 7) {
                    goToSlide(10); // 8. Q&A -> 10페이지
                }
            });
        });

        // 6페이지 비디오 클릭 시 재생/일시정지 토글 기능 및 오버레이 애니메이션
        document.addEventListener('DOMContentLoaded', () => {
            const videoFrames = document.querySelectorAll('.video-frame-wrapper');
            videoFrames.forEach(wrapper => {
                const video = wrapper.querySelector('video');
                const overlay = wrapper.querySelector('.play-pause-overlay');
                let overlayTimer = null;

                if (!video || !overlay) return;

                const showOverlay = (state) => {
                    overlay.classList.remove('playing', 'paused');
                    overlay.classList.add(state);
                    overlay.classList.add('show');

                    if (overlayTimer) clearTimeout(overlayTimer);
                    overlayTimer = setTimeout(() => {
                        overlay.classList.remove('show');
                    }, 800);
                };

                video.addEventListener('click', () => {
                    if (video.paused) {
                        video.play();
                        showOverlay('playing');
                    } else {
                        video.pause();
                        showOverlay('paused');
                    }
                });
            });
        });

        // 비디오 모달 제어
        document.addEventListener('DOMContentLoaded', () => {
            const openBtn = document.getElementById('open-video-modal-btn');
            const closeBtn = document.getElementById('close-video-modal-btn');
            const modal = document.getElementById('server-video-modal');
            const popupVideo = document.getElementById('server-popup-video');

            if (openBtn && closeBtn && modal && popupVideo) {
                openBtn.addEventListener('click', () => {
                    if (typeof playPopSound === 'function') playPopSound();
                    modal.classList.add('open');
                    popupVideo.currentTime = 0;
                    popupVideo.play();
                });

                const closeModal = () => {
                    if (typeof playPopSound === 'function') playPopSound();
                    modal.classList.remove('open');
                    popupVideo.pause();
                };

                closeBtn.addEventListener('click', closeModal);
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) closeModal();
                });
            }
        });
            // 6페이지 비디오 클릭 시 재생/일시정지 토글 기능 및 오버레이 애니메이션
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('#slide-8 .issue-dot').forEach(dot => {
                dot.addEventListener('click', () => {
                    const nextIndex = Number(dot.dataset.issueIndex || 0);
                    showIssueCard(nextIndex);
                    restartIssueCarousel();
                });
            });

            const videoFrames = document.querySelectorAll('.video-frame-wrapper');
            videoFrames.forEach(wrapper => {
                const video = wrapper.querySelector('video');
                const overlay = wrapper.querySelector('.play-pause-overlay');
                let overlayTimer = null;

                if (!video || !overlay) return;

                const showOverlay = (state) => {
                    overlay.classList.remove('playing', 'paused');
                    overlay.classList.add(state);
                    overlay.classList.add('show');

                    if (overlayTimer) clearTimeout(overlayTimer);
                    overlayTimer = setTimeout(() => {
                        overlay.classList.remove('show');
                    }, 800);
                };

                video.addEventListener('click', () => {
                    if (video.paused) {
                        video.play();
                        showOverlay('playing');
                    } else {
                        video.pause();
                        showOverlay('paused');
                    }
                });
            });
        });
    
    
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
    
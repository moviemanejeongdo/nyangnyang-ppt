const totalSlides = 9;
let currentSlideIndex = 1;

// 현재 파일명(00X.html)에서 슬라이드 번호 감지
const pathMatch = window.location.pathname.match(/00(\d)\.html/);
if (pathMatch) {
    currentSlideIndex = parseInt(pathMatch[1], 10);
}

// 16:9 비율 반응형 자동 맞춤 스크립트
function resizePresentation() {
    const presentation = document.getElementById('presentation');
    if (!presentation) return;
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
    requestAnimationFrame(() => {
        presentation.classList.add('scaled');
    });
}

window.addEventListener('resize', resizePresentation);
document.addEventListener('DOMContentLoaded', resizePresentation);

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

// 특정 슬라이드로 이동하는 제어 로직 (?step=last 형태로 마지막 단계 로드 지원)
function goToSlide(index, step = null) {
    if (index < 1 || index > totalSlides) return;
    if (!(currentSlideIndex === 1 && index === 2)) {
        playPopSound();
    }
    
    let targetURL = `00${index}.html`;
    if (step) {
        targetURL += `?step=${step}`;
    }
    window.location.href = targetURL;
}

function goToNextPage() {
    if (currentSlideIndex < totalSlides) {
        goToSlide(currentSlideIndex + 1);
    }
}

function goToPrevPage(step = null) {
    if (currentSlideIndex > 1) {
        goToSlide(currentSlideIndex - 1, step);
    }
}

// DOM 로드 완료 시 바인딩 및 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 하단 네비게이션 힌트 설정
    const navHint = document.getElementById('nav-hint');
    if (navHint) {
        const navCurrent = document.getElementById('nav-current');
        if (navCurrent) {
            navCurrent.innerText = `${currentSlideIndex} / ${totalSlides}`;
        }

        const navPrev = document.getElementById('nav-prev');
        if (navPrev) {
            navPrev.addEventListener('click', (e) => {
                e.preventDefault();
                goToPrevPage();
            });
        }

        const navNext = document.getElementById('nav-next');
        if (navNext) {
            navNext.addEventListener('click', (e) => {
                e.preventDefault();
                goToNextPage();
            });
        }
    }
});

# -*- coding: utf-8 -*-
"""
DaVinci Resolve용 영상 변환 스크립트 (CFR H.264 변환)
- 스마트폰 가변 프레임레이트(VFR), HEVC, HDR 10-bit 등의 영상을
  DaVinci Resolve Free/Studio 버전에서 미디어 오프라인(Media Offline) 없이
  안정적으로 편집할 수 있는 H.264 CFR(고정 프레임레이트) MP4 포맷으로 일괄 변환합니다.
"""

import os
import sys
import shutil
import subprocess
import re

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
CONVERTED_DIR = os.path.join(BASE_DIR, "converted")

def clean_filename(filename):
    """
    파일명에서 영문, 숫자, 언더스코어(_), 대시(-), 점(.)만 남기고 정제합니다.
    한글이나 공백 등 DaVinci Resolve에서 경로 인식이 꼬일 수 있는 문자를 안전한 문자로 변경합니다.
    """
    name, ext = os.path.splitext(filename)
    
    # 1. 영문, 숫자, 언더스코어, 대시를 제외한 모든 문자를 언더스코어로 치환
    cleaned = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    # 2. 연속된 언더스코어를 하나로 축소
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    # 3. 양 끝의 언더스코어 제거
    cleaned = cleaned.strip('_')
    
    # 만약 정제 후 파일명이 비어버리거나 안전하지 않다면 기본값 사용
    if not cleaned:
        cleaned = "converted_video"
        
    return f"{cleaned}{ext.lower()}"

def check_ffmpeg():
    """시스템에 FFmpeg가 설치되어 있는지 확인합니다."""
    try:
        # FFmpeg 버전 확인 명령 실행
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def move_existing_videos_to_input():
    """현재 디렉토리에 있는 test1.mp4, test2.mp4 등의 원본 영상을 input 폴더로 이동시킵니다."""
    moved_files = []
    for file in os.listdir(BASE_DIR):
        # 스크립트 자체는 제외하고, 확장자가 mp4인 파일 중 input/converted 디렉토리가 아닌 것
        if file.lower().endswith(".mp4") and file not in ["convert_for_resolve.py"]:
            src_path = os.path.join(BASE_DIR, file)
            dest_path = os.path.join(INPUT_DIR, file)
            
            # 이미 input 폴더에 동일한 파일이 있는지 확인
            if not os.path.exists(dest_path):
                print(f"[*] 원본 파일 발견: {file} -> input/ 폴더로 이동합니다.")
                shutil.move(src_path, dest_path)
                moved_files.append(file)
            else:
                # 이미 존재하면 원본 삭제 혹은 그냥 둠 (안전을 위해 덮어쓰지 않고 안내만)
                print(f"[*] {file} 파일이 이미 input/ 폴더에 존재하므로 이동을 건너뜁니다.")
    return moved_files

def convert_videos():
    # 폴더 생성
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(CONVERTED_DIR, exist_ok=True)
    
    # FFmpeg 설치 여부 확인
    if not check_ffmpeg():
        print("=" * 80)
        print("[오류] FFmpeg가 시스템에 설치되어 있지 않거나 환경 변수(Path)에 등록되어 있지 않습니다.")
        print("=" * 80)
        print("설치 방법:")
        print("1. Windows용 FFmpeg 다운로드:")
        print("   - https://www.gyan.dev/ffmpeg/builds/ 에서 'ffmpeg-git-essentials.7z' 또는 'ffmpeg-release-essentials.zip' 다운로드")
        print("2. 압축 해제 후 bin 폴더(예: C:\\ffmpeg\\bin)를 시스템 환경 변수의 'Path'에 추가합니다.")
        print("3. 새 터미널/명령 프롬프트를 열고 본 스크립트를 다시 실행해주세요.")
        print("=" * 80)
        return

    # 현재 디렉토리의 mp4 파일들을 input/ 폴더로 이동
    move_existing_videos_to_input()
    
    # input/ 폴더 내 mp4 파일 목록 가져오기
    input_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".mp4")]
    
    if not input_files:
        print("[!] input/ 폴더에 변환할 MP4 파일이 없습니다.")
        print("    원본 mp4 파일들을 input/ 폴더에 넣고 스크립트를 다시 실행해주세요.")
        return

    print(f"[*] 총 {len(input_files)}개의 파일을 변환합니다.")
    print("=" * 60)

    for idx, filename in enumerate(input_files, 1):
        input_path = os.path.join(INPUT_DIR, filename)
        
        # 안전한 출력 파일명 생성
        safe_filename = clean_filename(filename)
        # 만약 원본 파일명과 안전한 파일명이 같고 충돌 위험이 있다면 '_resolved' 접미사 추가
        name, ext = os.path.splitext(safe_filename)
        safe_filename = f"{name}_resolved{ext}"
        
        output_path = os.path.join(CONVERTED_DIR, safe_filename)
        
        print(f"[{idx}/{len(input_files)}] 변환 시작: {filename}")
        print(f"  -> 출력 파일명: {safe_filename}")
        
        # FFmpeg 변환 명령어 구성
        # -y: 덮어쓰기 허용
        # -c:v libx264: H.264 비디오 코덱 사용 (Resolve 호환성 극대화)
        # -preset medium: 인코딩 속도/압축률 밸런스 (slow도 좋으나 대용량 시 medium이 무난)
        # -crf 18: 고화질 기준 시각적 손실 없는 수준 (18~20 권장, 수치가 낮을수록 고화질/대용량)
        # -pix_fmt yuv420p: 픽셀 포맷 8-bit YUV 4:2:0 (Resolve Free 버전은 10-bit H.264/H.265를 읽지 못함)
        # -r 30: 30fps 고정 프레임레이트(CFR) 변환 (VFR 싱크 밀림 방지)
        # -c:a aac: AAC 오디오 코덱 (Resolve 호환성 우수)
        # -ar 48000: 오디오 샘플레이트 48kHz (Resolve 프로젝트 기본값과 매칭)
        # -ac 2: 스테레오 2채널 설정
        # -movflags +faststart: MP4 메타데이터(moov atom)를 파일 앞으로 당겨 Resolve 및 웹 재생 로딩 최적화
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-ar", "48000",
            "-ac", "2",
            "-movflags", "+faststart",
            output_path,
            "-y"
        ]
        
        try:
            # 변환 프로세스 실행
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
            
            if process.returncode == 0:
                print(f"[+] 성공: {safe_filename} 변환이 완료되었습니다.")
                print(f"    저장 위치: {output_path}\n")
            else:
                print(f"[-] 실패: {filename} 변환 중 오류가 발생했습니다.")
                print("FFmpeg 오류 로그:")
                print(process.stderr)
                print("\n")
                
        except Exception as e:
            print(f"[-] 시스템 오류: {str(e)}\n")

    print("=" * 60)
    print("[*] 모든 파일의 변환 작업이 종료되었습니다.")
    print(f"    - 원본 파일 위치: {INPUT_DIR}")
    print(f"    - 변환 완료 파일 위치: {CONVERTED_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    convert_videos()

import re

with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_show_sub = """        function showSlide5SubPage(targetIndex, direction = 'next') {
            const sub1 = document.getElementById('slide5-sub-1');
            const sub2 = document.getElementById('slide5-sub-2');
            const sub3 = document.getElementById('slide5-sub-3');
            const subPages = [sub1, sub2, sub3].filter(Boolean);
            if (!sub1 || !sub2 || !sub3) return;"""

new_show_sub = """        function showSlide5SubPage(targetIndex, direction = 'next') {
            const subPages = Array.from(document.querySelectorAll('#slide-5 .slide5-sub-page'));
            const sub1 = document.getElementById('slide5-sub-1');
            const sub2 = document.getElementById('slide5-sub-2');
            const activeSub = subPages[targetIndex - 1];
            if (!sub1 || !sub2 || !activeSub) return;"""

if old_show_sub in text:
    text = text.replace(old_show_sub, new_show_sub)
else:
    print("Failed to replace showSlide5SubPage top part")

# Check if there are other hardcoded things like `else if (targetIndex === 3)`.
# In index.html:
#            } else if (targetIndex === 3) {
#                if (headerExtras) headerExtras.style.opacity = '0';
#                const thumbVideo = sub2.querySelector('.floating-video-thumbnail video');
#                if (thumbVideo) thumbVideo.pause();
#                const popupVideo = document.getElementById('server-popup-video');
#                if (popupVideo) popupVideo.pause();
#            }
# We should change this to `} else if (targetIndex >= 3) {` so that for 4, 5, 6 it also stops the videos and hides headerExtras!
old_target_3 = """            } else if (targetIndex === 3) {
                if (headerExtras) headerExtras.style.opacity = '0';
                const thumbVideo = sub2.querySelector('.floating-video-thumbnail video');
                if (thumbVideo) thumbVideo.pause();
                const popupVideo = document.getElementById('server-popup-video');
                if (popupVideo) popupVideo.pause();
            }"""

new_target_3 = """            } else if (targetIndex >= 3) {
                if (headerExtras) headerExtras.style.opacity = '0';
                const thumbVideo = sub2.querySelector('.floating-video-thumbnail video');
                if (thumbVideo) thumbVideo.pause();
                const popupVideo = document.getElementById('server-popup-video');
                if (popupVideo) popupVideo.pause();
            }"""

if old_target_3 in text:
    text = text.replace(old_target_3, new_target_3)
else:
    print("Failed to replace targetIndex === 3")


with open(r'e:\unity 26.04.28\260521 냥냥카페\냥냥ppt260606\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated subPages logic successfully!")

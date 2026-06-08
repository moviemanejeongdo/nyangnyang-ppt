import re
import os

file_path = r'e:\unity 26.04.28\냥냥ppt260606\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove blue background
content = content.replace(
    '<div class="slide" id="slide-5" style="justify-content: center; align-items: center; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">',
    '<div class="slide" id="slide-5" style="justify-content: center; align-items: center;">'
)

# 2. Add inline initial CSS for cards to be hidden
content = content.replace(
    'class="env-card" style="background',
    'class="env-card" style="opacity: 0; transform: translateY(30px); transition: opacity 0.5s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); background'
)

# 3. Add slide5State variable
if 'let slide5State = 0;' not in content:
    content = content.replace(
        'let currentSlideIndex = 1;',
        'let currentSlideIndex = 1;\nlet slide5State = 0;'
    )

# 4. Update stepsPerSlide for slide 5
content = content.replace(
    '5: 1, // Dev Env (new)',
    '5: 2, // Dev Env cascade'
)

# 5. Update step logic for slide 5
old_step_logic = '''            if (currentSlideIndex === 1) {
                currentStep += (typeof introState !== 'undefined' ? introState + 1 : 1);
            } else if (currentSlideIndex === 3) {'''

new_step_logic = '''            if (currentSlideIndex === 1) {
                currentStep += (typeof introState !== 'undefined' ? introState + 1 : 1);
            } else if (currentSlideIndex === 3) {
                currentStep += (typeof memberCardIndex !== 'undefined' ? memberCardIndex + 1 : 1);
            } else if (currentSlideIndex === 5) {
                currentStep += (typeof slide5State !== 'undefined' ? slide5State + 1 : 1);'''
content = content.replace(old_step_logic, new_step_logic.split('} else if (currentSlideIndex === 3) {')[0] + '} else if (currentSlideIndex === 3) {')

if '} else if (currentSlideIndex === 5) {' not in content:
    content = content.replace(
        '} else if (currentSlideIndex === 3) {\n                currentStep += (typeof memberCardIndex !== \'undefined\' ? memberCardIndex + 1 : 1);',
        '} else if (currentSlideIndex === 3) {\n                currentStep += (typeof memberCardIndex !== \'undefined\' ? memberCardIndex + 1 : 1);\n            } else if (currentSlideIndex === 5) {\n                currentStep += (typeof slide5State !== \'undefined\' ? slide5State + 1 : 1);'
    )

# 6. Reset logic in goToSlide
old_goto = '''    function goToSlide(index) {
        if (index < 1 || index > totalSlides) return;
        currentSlideIndex = index;'''

new_goto = '''    function goToSlide(index) {
        if (index < 1 || index > totalSlides) return;
        currentSlideIndex = index;
        
        // Reset Slide 5
        if (index === 5) {
            slide5State = 0;
            document.querySelectorAll('#slide-5 .env-card').forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
            });
        }
'''
content = content.replace(old_goto, new_goto)

# 7. Add keydown space handler logic
# I need to insert it inside the `if (e.code === 'Space' || e.key === ' ' || e.code === 'ArrowRight')` block
# Let's find: `} else if (currentSlideIndex === 3) {` inside keydown listener
old_keydown = '''                } else if (currentSlideIndex === 3) {
                    if (!nextMemberCard() && currentSlideIndex < totalSlides) {
                        goToSlide(currentSlideIndex + 1);
                    }
                } else if (currentSlideIndex === 6) {'''

new_keydown = '''                } else if (currentSlideIndex === 3) {
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
                } else if (currentSlideIndex === 6) {'''

content = content.replace(old_keydown, new_keydown)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Slide 5 animations applied.")

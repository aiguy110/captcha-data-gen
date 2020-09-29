from captcha.image import ImageCaptcha
import random
import string
import json
import sys
import os


def gen_training_data(output_dir, num_samples):
    min_chars = 4
    max_chars = 5
    char_set = string.ascii_letters + string.digits

    image_gen = ImageCaptcha()
    for n in range(num_samples):
        captcha_length = random.choice(range(min_chars, max_chars+1))
        captcha_text = ''
        for c in range(captcha_length):
            captcha_text += random.choice(char_set)
        
        gen_result = image_gen.generate_image(captcha_text, for_training=True)
        target = gen_result["final"]
        target.save( os.path.join(output_dir, f'{captcha_text}.png') )

        label = []

        for c, char_img in enumerate(gen_result["char_onlys"]):
            left = -1
            right = -1
            top = -1
            bottom = -1
            
            for x in range(char_img.width):
                for y in range(char_img.height):
                    if char_img.getpixel((x,y)) != (255,255,255):
                        if left == -1:
                            left = x
                        if x > right:
                            right = x
                        if top == -1 or top > y:
                            top = y
                        if y > bottom:
                            bottom = y
        
            label.append({'left':left, 'right': right, 'top': top, 'bottom':bottom})
        
        with open(os.path.join(output_dir, f'{captcha_text}.json'), 'w') as f:
            json.dump(label, f)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:')
        print('python3 main.py <number_of_samples>')
        
    num_samples = int(sys.argv[1])
    gen_training_data('data', num_samples)
import os

from PIL import Image

input_dir = '../assets/employee_images'
output_dir = '../assets/employee_images_resized_256'
os.makedirs(output_dir, exist_ok=True)

target_size = (256, 256)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', 'jpeg')):
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img.save(os.path.join(output_dir, filename))
        print(f'✅ Resized {filename}')

print('🎉 All done!')
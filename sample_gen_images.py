import requests
import os

# Target folder
output_dir = 'assets/employee_images'
os.makedirs(output_dir, exist_ok=True)

# Starting ID
start_id = 4001
total_images = 50

# Download loop
for i in range(total_images):
    user_id = start_id + i
    filename = f'{user_id}.png'
    file_path = os.path.join(output_dir, filename)

    try:
        response = requests.get('https://thispersondoesnotexist.com/',
                                timeout=5)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f'✅ Downloaded {filename}')
    except Exception as e:
        print(f'❌ Failed to download {filename}: {e}')

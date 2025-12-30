"""Create a simple icon for the Human Simulator app"""
from PIL import Image, ImageDraw

# Create a 512x512 image with a blue gradient background
size = 512
image = Image.new('RGB', (size, size), color='#1E88E5')
draw = ImageDraw.Draw(image)

# Draw a circle (representing human/activity)
circle_color = '#FFFFFF'
margin = 40
draw.ellipse([margin, margin, size-margin, size-margin], fill=circle_color, outline=circle_color)

# Draw a smaller inner circle (representing movement/activity)
inner_margin = 120
inner_color = '#1E88E5'
draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], fill=inner_color)

# Save as PNG first
image.save('/Users/tahiru/Desktop/bots/icon.png')
print("✅ Icon created: icon.png")

# For macOS ICNS format, we need to use iconutil
# Create a temporary png file and convert it
import subprocess
import os

png_path = '/Users/tahiru/Desktop/bots/icon.png'
iconset_path = '/Users/tahiru/Desktop/bots/icon.iconset'
icns_path = '/Users/tahiru/Desktop/bots/icon.icns'

# Create iconset directory
os.makedirs(iconset_path, exist_ok=True)

# Generate different sizes required for ICNS
sizes = [16, 32, 64, 128, 256, 512]
for size in sizes:
    img = Image.open(png_path).resize((size, size), Image.Resampling.LANCZOS)
    img.save(f'{iconset_path}/icon_{size}x{size}.png')
    # Also create @2x versions for some sizes
    if size < 512:
        img2x = Image.open(png_path).resize((size*2, size*2), Image.Resampling.LANCZOS)
        img2x.save(f'{iconset_path}/icon_{size}x{size}@2x.png')

# Convert iconset to icns using macOS iconutil
try:
    subprocess.run(['iconutil', '-c', 'icns', iconset_path, '-o', icns_path], check=True)
    print(f"✅ ICNS icon created: icon.icns")
except Exception as e:
    print(f"⚠️  Could not create ICNS: {e}")
    print("You can use 'icon.png' instead with: pyinstaller --onefile --windowed --name 'HumanSimulator' ./ai.py")

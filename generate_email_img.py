import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os

text = "rt20bg@gmail.com"
# Try to load a standard font, fallback to default if not found
try:
    font = PIL.ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = PIL.ImageFont.load_default()

# Get the bounding box of the text
left, top, right, bottom = font.getbbox(text)
width = right - left
height = bottom - top

# Add some padding
padding_x = 10
padding_y = 5

image_width = width + 2 * padding_x
image_height = height + 2 * padding_y

# Create an image with an explicitly solid RGB background (no alpha channel)
img = PIL.Image.new('RGB', (image_width, image_height), color=(246, 248, 250))
d = PIL.ImageDraw.Draw(img)

# Draw the text in a vibrant GitHub link blue
d.text((padding_x, padding_y - top), text, fill=(9, 105, 218), font=font)

# Save the image
output_path = r"e:\Antigravity projects\email_contact.png"
img.save(output_path)
print(f"Saved {output_path}")

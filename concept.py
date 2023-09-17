from PIL import Image, ImageDraw, ImageFont

game = 'cyberpunk2077'

# crop_box = (1710, 490, 2050, 870) # dobre, cyber
# crop_box = (1050, 580, 1470, 890) # chata
# crop_box = (2080, 500, 2480, 930) # czacha
# crop_box = (1340, 180, 1780, 460) # lampa
crop_box = (600, 400, 1300, 1300) # flara
image_filenames = ['base3', 'dlss-jakosc3', 'dlss-balans3', 'dlss-wydajnosc3', 'fsr-jakosc3', 'fsr-balans3', 'fsr-wydajnosc3']
# image_filenames = ['base','dlss-jakosc', 'dlss-balans', 'dlss-wydajnosc', 'fsr-jakosc', 'fsr-balans', 'fsr-wydajnosc']
# image_labels = ['Bazowy', 'DLSS jakosc', 'DLSS balans', 'DLSS wydajnosc', 'FSR jakosc', 'FSR balans', 'FSR wydajnosc']
image_labels = ['Base', 'DLSS Quality', 'DLSS Balance', 'DLSS Performance', 'FSR Quality', 'FSR Balance', 'FSR Performance']

cropped_images = []

for filename in image_filenames:
    image = Image.open(f'images/{game}/{filename}.png')
    cropped_image = image.crop(crop_box)
    cropped_images.append(cropped_image)


text_height = 40
stitched_image = Image.new('RGB', (sum([img.width for img in cropped_images]), cropped_images[0].height + text_height), (255,255,255))

font = ImageFont.truetype('US101.TTF', 40)

draw = ImageDraw.Draw(stitched_image)

offset = 0
for idx, img in enumerate(cropped_images):
    stitched_image.paste(img, (offset, 0))

    text = image_labels[idx]
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = offset + (img.width - text_width) // 2
    text_y = img.height
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    offset += img.width

stitched_image.save(f'croppedImages/{game}_3_flara.png')

stitched_image.show()

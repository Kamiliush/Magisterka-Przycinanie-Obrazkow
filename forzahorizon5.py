from PIL import Image, ImageDraw, ImageFont

def create_comparison_image(game, crop_box, image_names, image_labels, image_number='1', image_suffix=''):
    cropped_images = []

    for filename in image_names:
        image = Image.open(f'images/{game}/{filename+image_number}.png')
        cropped_image = image.crop(crop_box)
        cropped_images.append(cropped_image)

    text_height = 40
    total_width = cropped_image.width * 4
    total_height = (cropped_image.height + text_height) * 2
    stitched_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    font = ImageFont.truetype('DejaVuSansCondensed-Bold.ttf', 30)
    draw = ImageDraw.Draw(stitched_image)

    for idx, (img, label) in enumerate(zip(cropped_images, image_labels)):
        row = idx // 4
        col = idx % 4
        x_offset = col * cropped_image.width
        y_offset = row * (cropped_image.height + text_height)
        if idx == 0:
            y_offset += (cropped_image.height + text_height) // 2
        if idx >= 4:
            x_offset += cropped_image.width

        # Wklejanie obrazu
        stitched_image.paste(img, (x_offset, y_offset))

        # Dodawanie tekstu
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x_offset + (cropped_image.width - text_width) // 2
        text_y = y_offset + cropped_image.height
        draw.text((text_x, text_y), label, font=font, fill=(0, 0, 0))

    stitched_image.save(f'output_images/{game}_grid_scene_{image_number}_box_{image_suffix}.png')

    stitched_image.show()


game = 'forzahorizon5'
suffix = 'test'

crop_boxes = {'1': [(355, 215, 730, 530)],
              '2': [(1950, 420, 2280, 700)],
              }
#crop_box = (left, top, right, bottom) # flara
image_names = ['base', 'dlss-jakosc', 'dlss-balans', 'dlss-wydajnosc', 'fsr-jakosc', 'fsr-balans', 'fsr-wydajnosc']
image_labels = ['BAZOWY', 'DLSS JAKOŚĆ', 'DLSS BALANS', 'DLSS WYDAJNOŚĆ', 'FSR JAKOŚĆ', 'FSR BALANS', 'FSR WYDAJNOŚĆ']
# image_labels_english = ['Base', 'DLSS Quality', 'DLSS Balance', 'DLSS Performance', 'FSR Quality', 'FSR Balance', 'FSR Performance']

for key, crop_box_list in crop_boxes.items():
    for i, crop_box in enumerate(crop_box_list):
        create_comparison_image(game, crop_box, image_names, image_labels, key, f'{i+1}')

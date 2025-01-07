import os
import random
from PIL import Image
from utils import apply_fog, reduce_lighting, apply_weather_overlay


def overlay_images(landmine_dir, landscape_dir,
                   output_dir,
                   output_size: tuple[int, int] = (1024, 768),
                   transparency=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    landmine_images = [f for f in os.listdir(landmine_dir)
                       if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    landscape_images = [f for f in os.listdir(landscape_dir)
                        if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    for landmine_image in landmine_images:
        landmine_path = os.path.join(landmine_dir, landmine_image)
        landmine = Image.open(landmine_path).convert("RGBA")

        for landscape_image in landscape_images:
            landscape_path = os.path.join(landscape_dir, landscape_image)
            landscape = Image.open(landscape_path).convert("RGBA")
            landscape = landscape.resize(output_size)
            scale_factor = 0.09
            landmine_resized = landmine.resize((
                int(landscape.width * scale_factor),
                int(landscape.height * scale_factor)
            ))

            x_offset = random.randint(0, landscape.width - landmine_resized.width)
            y_offset = random.randint(int(landscape.height * 2 / 3),
                                      landscape.height - landmine_resized.height)

            if transparency > 0:
                alpha = landmine_resized.getchannel('A')
                alpha = alpha.point(lambda p: p * (1 - transparency / 255))
                landmine_resized.putalpha(alpha)

            landscape.paste(landmine_resized, (x_offset, y_offset), landmine_resized)

            output_filename = f"overlay_{landmine_image.split('.')[0]}_{landscape_image.split('.')[0]}.png"
            output_path = os.path.join(output_dir, output_filename)
            landscape.save(output_path, "PNG")
            print(f"Saved overlay image to {output_path}")
            apply_fog(output_path)
            reduce_lighting(output_path)
            apply_weather_overlay(output_path, "rain")
            apply_weather_overlay(output_path, "snow")


landmine_dir = "./landmines"
landscape_dir = "./landscapes"
output_dir = "./output"
overlay_images(landmine_dir, landscape_dir, output_dir)
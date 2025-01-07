from PIL import Image, ImageEnhance
import numpy as np
from transformers import pipeline
import os


def apply_fog(image_path):
    img = Image.open(image_path).convert("RGBA")
    pipe = pipeline(task="depth-estimation",
                    model="depth-anything/Depth-Anything-V2-Base-hf")
    depth = pipe(img)["depth"]
    white_layer = Image.new('RGBA', img.size, (216, 216, 216, 0))

    grayscale_array = np.array(depth)
    white_array = np.array(white_layer)

    alpha = 255 - grayscale_array
    alpha = np.clip(alpha * 1.3, 0, 255).astype(np.uint8)  # Intensify fog by scaling alpha values

    white_array[:, :, 3] = alpha

    white_layer_transparent = Image.fromarray(white_array, 'RGBA')

    result = Image.alpha_composite(img.convert('RGBA'), white_layer_transparent)

    result.save(f"{image_path.split('.png')[0]}_foggy.png")
    print(f"Fog applied to {image_path.split('.png')[0]}_foggy.png")


def reduce_lighting(image_path, brightness_factor=0.3):
    img = Image.open(image_path)

    enhancer = ImageEnhance.Brightness(img)
    darker_image = enhancer.enhance(brightness_factor)

    darker_image.save(f"{image_path.split('.png')[0]}_darkened.png")
    print(f"Lighting reduced in {image_path.split('.png')[0]}_darkened.png")


def apply_weather_overlay(image_path, weather_type="rain", transparency=1):
    base_image = Image.open(image_path).convert("RGBA")

    texture_folder = f"./{weather_type}"
    texture_path = f"{texture_folder}/{np.random.choice(os.listdir(texture_folder))}"

    texture = Image.open(texture_path).convert("RGBA")
    texture = texture.resize(base_image.size)

    if transparency < 1:
        alpha = texture.getchannel('A')
        alpha = alpha.point(lambda p: int(p * transparency))
        texture.putalpha(alpha)

    combined_image = Image.alpha_composite(base_image, texture)

    output_filename = f"{image_path.split('.png')[0]}_{weather_type}.png"
    combined_image.save(output_filename)
    print(f"{weather_type.capitalize()} effect applied to {image_path.split('.png')[0]}_{weather_type}.png")

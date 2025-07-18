import numpy as np
from pathlib import Path
from modules.image_process import png_to_array, crop_image, save_array_to_png

folder = Path("C:/Code/Stress-Imaging/SAMPLE_DATA/XMED_3_point_bending")

# Get all PNG files in the folder
png_files = list(folder.glob('*.png'))

# Print each PNG file
for file in png_files:
    img_array = png_to_array(file)
    crop_range_x = [115, 507]
    crop_range_y = [190, 264]
    cropped_img_array = crop_image(img_array, crop_range_x, crop_range_y)
    new_filename = file.name.replace(".png", "_cropped.png")
    save_array_to_png(cropped_img_array, new_filename, save_dir=folder)
    print(file.name)

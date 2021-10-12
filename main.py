import sys
from PIL import Image
import os
import glob
import math
from itertools import product
import glob


def should_resize(img, max_width):
    img_size = img.size
    width = img_size[0]
    if width <= max_width:
        return False
    else:
        return True

def resize_width(image, max_width):
    img = image.copy()
    img_size = img.size
        
    new_height = int(math.ceil((max_width / img_size[0]) * img_size[1]))
    img.thumbnail(size=(max_width, new_height))
    return img

def generate_glob_paths(images_directories, images_formats):
    # Generate all the possible convinations for directories and formats
    product_result = list(product(images_directories, images_formats))
    # Create the actual list of strings for glob
    get_glob_paths = lambda p : f"{p[0]}/*.{p[1]}"
    return [get_glob_paths(p) for p in product_result]

# Naive validation
def to_int(value):
    try:
        return int(value)
    except ValueError:
        print(f"{value} is not a number")
        sys.exit(1)

def to_arr(value):
    return [x.strip() for x in value.split(',')]

def debug():
    return os.environ["DEBUG"] == "True"

def print_debug(msg):
    if debug():
        print(msg)

def main():

    # Arguments
    images_max_width = to_int(os.environ["IMAGES_MAX_WIDTH"])
    images_quality = to_int(os.environ["IMAGES_QUALITY"])

    images_formats = to_arr(os.environ["IMAGES_FORMATS"])
    images_directories = to_arr(os.environ["IMAGES_DIRECTORIES"])

    # If these are empty it would replace the original image
    images_prefix = os.environ["IMAGES_PREFIX"]
    images_suffix = os.environ["IMAGES_SUFFIX"]

    paths = generate_glob_paths(images_directories, images_formats)

    print_debug(f"images_max_width= {images_max_width}")
    print_debug(f"images_quality= {images_quality}")
    print_debug(f"images_formats= {images_formats}")
    print_debug(f"images_directories= {images_directories}")
    print_debug(f"images_prefix= {images_prefix}")
    print_debug(f"images_suffix= {images_suffix}")
    print_debug(f"paths= {paths}")


    result = []
    for path in paths:
        print_debug(f"Opening images: {path}")
        # Find all the matching files ...
        for image_src in glob.glob(path):
            print_debug(f"Image src= {image_src}")
            image = Image.open(image_src)
            if should_resize(image, images_max_width):
                print_debug(f"Going to resize {image_src} ...")
                img = resize_width(image, images_max_width)

                image_raw_name = image.filename.rsplit('.', 1)[0]
                image_path = image_raw_name.rsplit('/', 1)[0]
                image_name = image_raw_name.rsplit('/', 1)[1]
                image_format = image.filename.rsplit('.', 1)[1]

                new_name = f"{image_path}/{images_prefix}{image_name}{images_suffix}.{image_format}"
                img.save(new_name, optimize=True, quality=images_quality)
                result.append(new_name)
    
    print(f"::set-output name=result::{result}")
    sys.exit(0)

if __name__ == "__main__":
    main()

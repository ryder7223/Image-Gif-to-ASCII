from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ASCII characters ordered from dark to light
ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:\",^`'.,"

def resize_image(image, new_width=100, scale=1.0):
    """
    Resizes image to maintain aspect ratio with adjustable scale for resolution.
    Higher scale gives higher resolution ASCII art.
    """
    if more_info == True:
        print("Resizing image...")
    width, height = image.size
    aspect_ratio = height / width
    new_width = int(new_width * scale)
    new_height = int(new_width * aspect_ratio * 0.5)  # Adjust height for ASCII aspect ratio
    return image.resize((new_width, new_height))
def grayscale(image):
    """Converts image to grayscale."""
    if more_info == True:
        print("Converting image to grayscale...")
    return image.convert("L")

def pixels_to_ascii(image):
    """Maps pixels in grayscale image to ASCII characters."""
    if more_info == True:
        print("Mapping pixels to characers...")
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 4]  # Maps pixel (0-255) to index in ASCII_CHARS (0-64)
    return ascii_str

def convert_image_to_ascii(image_path, new_width=100, scale=1.0):
    """
    Converts an image to ASCII art, with adjustable resolution via `scale`.
    Higher scale increases detail (resolution), lower scale decreases it.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}. {e}")
        return

    # Resize and convert to grayscale
    image = resize_image(image, new_width, scale)
    image = grayscale(image)

    # Convert pixels to ASCII
    ascii_str = pixels_to_ascii(image)

    # Format ASCII string into image dimensions
    if more_info == True:
        print("Finishing up...")
    ascii_img = ""
    ascii_width = image.width
    for i in range(0, len(ascii_str), ascii_width):
        ascii_img += ascii_str[i:i+ascii_width] + "\n"
    if more_info == True:
        print("Generation complete.")
    return ascii_img

# Test the function with different scales
image_path = "shark.png"
outscale = 1
more_info = False
ascii_art = convert_image_to_ascii(image_path, new_width=100, scale=outscale)  # Increase scale for higher resolution
if ascii_art:
    with open(f'{image_path}.txt', 'w') as file:
        file.write(ascii_art)
        print(f"\n{image_path}.txt generated.")
else:
    print("\nFailed to generate ASCII art.")
from PIL import Image, ImageFile, GifImagePlugin
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

# ASCII characters ordered from dark to light
ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:\",^`'.,"

def resize_image(image, new_width=100, scale=1.0):
    """
    Resizes image to maintain aspect ratio with an additional adjustment for ASCII character height.
    This ensures the ASCII art matches the original proportions.
    """
    width, height = image.size
    aspect_ratio = height / width
    new_width = int(new_width * scale)
    new_height = int(new_width * aspect_ratio * 0.5)  # Adjust height for ASCII's 2:1 aspect ratio
    return image.resize((new_width, new_height))

def grayscale(image):
    """Converts image to grayscale."""
    return image.convert("L")

def pixels_to_ascii(image):
    """Maps pixels in grayscale image to ASCII characters."""
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 4]  # Maps pixel (0-255) to index in ASCII_CHARS (0-64)
    return ascii_str

def ascii_frame(image, new_width=100, scale=1.0):
    """Converts a single frame to ASCII art with correct aspect ratio matching."""
    image = resize_image(image, new_width, scale)
    image = grayscale(image)
    ascii_str = pixels_to_ascii(image)
    
    # Format ASCII string into image dimensions
    ascii_img = ""
    ascii_width = image.width
    for i in range(0, len(ascii_str), ascii_width):
        ascii_img += ascii_str[i:i+ascii_width] + "\n"
        
    return ascii_img

def convert_gif_to_ascii(gif_path, new_width=100, scale=1.0, output_path="ascii_gif.gif"):
    """
    Converts a GIF to ASCII art for each frame and saves as an animated ASCII GIF,
    matching the frame durations of the original GIF.
    """
    try:
        with Image.open(gif_path) as gif:
            frames = []
            durations = []
            try:
                while True:
                    # Capture frame duration
                    durations.append(gif.info.get('duration', 100))  # Default to 100ms if duration is missing
                    frame_ascii = ascii_frame(gif.copy(), new_width, scale)
                    frame_image = ascii_to_image(frame_ascii, new_width, scale=image_scale)
                    frames.append(frame_image)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass  # End of frames
        
            # Save as animated ASCII GIF with frame durations
            if frames:
                frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames[1:],
                    loop=0,
                    duration=durations
                )
                print(f"ASCII GIF saved as {output_path}")
            else:
                print("Failed to generate ASCII frames.")
    except Exception as e:
        print(f"Unable to open GIF file {gif_path}. {e}")
        return
    
    

def ascii_to_image(ascii_str, width, scale=1.0, font_size=1, bg_color="white", fg_color="black"):
    """
    Converts ASCII string into an image for GIF frame, with specified background and font colors.
    """
    from PIL import ImageDraw, ImageFont
    
    lines = ascii_str.splitlines()
    font = ImageFont.load_default()
    char_width, char_height = font.getsize("A")
    
    # Remove the * 2 multiplier on img_width to avoid adding extra horizontal space
    img_width = int(char_width * width * scale)  # Adjust for scale, not extra width
    img_height = int(char_height * len(lines))

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    y_offset = 0
    for line in lines:
        draw.text((0, y_offset), line, fill=fg_color, font=font)
        y_offset += char_height

    return img


# Example usage:
gif_path = "input2.gif"
image_scale = 0.5
convert_gif_to_ascii(gif_path, new_width=80, scale=image_scale, output_path=f"ascii_{gif_path}")
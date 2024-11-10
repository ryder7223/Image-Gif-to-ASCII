from PIL import Image, ImageFile, ImageDraw, ImageFont
import time
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

# ASCII characters ordered from dark to light
ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:\",^`'.,"

def resize_image(image, new_width=100, scale=1.0):
    width, height = image.size
    aspect_ratio = height / width
    new_width = int(new_width * scale)
    new_height = int(new_width * aspect_ratio * 0.5)  # Adjust height for ASCII's 2:1 aspect ratio
    return image.resize((new_width, new_height))

def grayscale(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 4] for pixel in pixels)
    return ascii_str

def ascii_frame(image, new_width=100, scale=1.0):
    image = resize_image(image, new_width, scale)
    image = grayscale(image)
    ascii_str = pixels_to_ascii(image)

    # Format ASCII string into image dimensions
    ascii_img = ""
    ascii_width = image.width
    for i in range(0, len(ascii_str), ascii_width):
        ascii_img += ascii_str[i:i + ascii_width] + "\n"

    return ascii_img

def convert_gif_to_ascii(gif_path, new_width=100, scale=1.0, chunk_size=0.1):
    try:
        with Image.open(gif_path) as gif:
            total_frames = 0
            durations = []
            
                # Count total frames
            try:
                while True:
                    durations.append(gif.info.get('duration', 100))
                    total_frames += 1
                    gif.seek(gif.tell() + 1)
            except EOFError:
                gif.seek(0)  # Reset to the first frame
            
            print(f"Total frames to process: {total_frames}")
            
            chunk_frame_count = max(1, int(total_frames * chunk_size))  # Calculate frames per chunk
            processed_frames = 0
            chunk_paths = []
            
                # Loop through the GIF in chunks
            while processed_frames < total_frames:
                frames_in_chunk = min(chunk_frame_count, total_frames - processed_frames)
                chunk_frames = []
                chunk_durations = []
            
                for _ in range(frames_in_chunk):
                    try:
                            # Capture frame duration
                        duration = gif.info.get('duration', 100)  # Default to 100ms if duration is missing
                        chunk_durations.append(duration)
                        frame_ascii = ascii_frame(gif.copy(), new_width, scale)
                        frame_image = ascii_to_image(frame_ascii, new_width, scale=image_scale)
                        chunk_frames.append(frame_image)
                        processed_frames += 1
            
                        gif.seek(gif.tell() + 1)
                    except EOFError:
                        break  # End of frames
            
                    # Save the current chunk to a temporary GIF file
                if chunk_frames:
                    temp_output_path = f"chunk_{len(chunk_paths)}.gif"
                    chunk_frames[0].save(
                        temp_output_path,
                        save_all=True,
                        append_images=chunk_frames[1:],
                        loop=0,
                        duration=chunk_durations
                        )
                    print(f"Saved chunk to {temp_output_path}")
                    chunk_paths.append(temp_output_path)
            
                # Print the FFmpeg command to combine chunks
            print_ffmpeg_command(chunk_paths)
    except Exception as e:
        print(f"Unable to open GIF file {gif_path}. {e}")
        return



def print_ffmpeg_command(chunk_paths):
    # Create the FFmpeg command string directly
    command = "ffmpeg "
    
    # Add each chunk file path to the command
    inputs = " ".join(f"-i '{os.path.abspath(chunk)}'" for chunk in chunk_paths)
    command += f"{inputs} -filter_complex \"concat=n={len(chunk_paths)}:v=1:a=0[out]\" -map \"[out]\" output.gif && "

    # Add cleanup commands to remove chunk files
    cleanup_commands = " && ".join(f"rm '{os.path.abspath(chunk)}'" for chunk in chunk_paths)
    command += cleanup_commands

    # Save the command to a shell script file
    script_file_path = "combine_chunks.sh"
    with open(script_file_path, "w") as script_file:
        script_file.write("#!/bin/bash\n")
        script_file.write(command + "\n")

    # Make the script executable
    os.chmod(script_file_path, 0o755)

    # Print command to run the script
    print(f"\nRun the following command to execute the script that combines the chunks and cleans up:\n")
    print(f"bash {script_file_path}")

def ascii_to_image(ascii_str, width, scale=1.0, bg_color="white", fg_color="black"):
    lines = ascii_str.splitlines()
    font = ImageFont.load_default()
    char_width, char_height = font.getsize("A")

    img_width = int(char_width * width * scale)
    img_height = int(char_height * len(lines))

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    y_offset = 0
    for line in lines:
        draw.text((0, y_offset), line, fill=fg_color, font=font)
        y_offset += char_height

    return img

# Example usage:
gif_path = "f.gif"
image_scale = 5
chunk_size = 0.08  # Set chunk size between 0 and 1 (e.g., 0.1 for 10%)
convert_gif_to_ascii(gif_path, new_width=80, scale=image_scale, chunk_size=chunk_size)
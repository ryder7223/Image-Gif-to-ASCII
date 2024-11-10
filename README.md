---

# ASCII Conversion Scripts

This repository contains Python scripts for converting images and GIFs into ASCII art. Each script has unique features suited for different purposes, including image resizing, grayscale conversion, frame-by-frame processing, and memory-efficient handling of GIFs.

## Scripts

### 1. `ascii.py`

This script converts a single image into ASCII art.

- **Features**:
  - Resizes images with an adjustable scale for resolution control.
  - Converts images to grayscale and maps pixel brightness to ASCII characters.
  - Outputs ASCII art in text format.

- **Usage**:
  Update the `image_path`, `new_width`, and `scale` parameters in the script to your preferred values. Run the script, and the ASCII art will be saved as a `.txt` file.

  ```python
  image_path = "example.png"  # Path to the image
  outscale = 1                # Scaling factor (1 for original size)
  ascii_art = convert_image_to_ascii(image_path, new_width=100, scale=outscale)
  ```

### 2. `asciiGif.py`

This script converts each frame of a GIF into ASCII art, saving the frames as an animated ASCII GIF.

- **Features**:
  - Resizes and converts each GIF frame to ASCII.
  - Preserves frame durations, allowing smooth animated ASCII GIF output.
  - Saves ASCII GIF output as `ascii_gif.gif`.

- **Usage**:
  Set the `gif_path`, `new_width`, `scale`, and `output_path` parameters to process a GIF.

  ```python
  gif_path = "input.gif"            # Path to the input GIF
  image_scale = 0.5                 # Scale to control ASCII resolution
  convert_gif_to_ascii(gif_path, new_width=80, scale=image_scale, output_path="ascii_output.gif")
  ```

### 3. `asciiGifLimitMem.py`

This script is optimized for large GIFs, processing them in memory-efficient chunks to avoid high memory usage. This is particularly useful for longer GIFs.

- **Features**:
  - Processes GIF frames in chunks to reduce memory load.
  - Outputs ASCII frames in individual temporary GIF chunks, which can later be combined.
  - Includes an option to generate a shell script to merge the chunks using FFmpeg.

- **Usage**:
  Define `gif_path`, `new_width`, `scale`, and `chunk_size` (a float between 0 and 1 representing the portion of frames to process per chunk). After running, execute the generated `combine_chunks.sh` to combine chunks.

  ```python
  gif_path = "large_input.gif"      # Path to the large GIF
  image_scale = 1.0                 # Scale for ASCII resolution
  chunk_size = 0.1                  # Process 10% of frames per chunk
  convert_gif_to_ascii(gif_path, new_width=80, scale=image_scale, chunk_size=chunk_size)
  ```

  **Note**: The `combine_chunks.sh` script requires [FFmpeg](https://ffmpeg.org/) to merge the chunked GIFs.

---

## Requirements

- **Python 3.x**
- **Pillow** (`pip install pillow`)
- **FFmpeg** (for combining chunks in `asciiGifLimitMem.py`)

## License

This project is open-source and available under the [MIT License](LICENSE).

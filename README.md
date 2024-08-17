# Dlsys v2.1.0

Dlsys is a powerful and versatile Python package for downloading and processing various types of content from the internet, including YouTube videos, websites, images, and audio files.

## Features

- Download audio and video from YouTube and other supported platforms
- Split audio files into customizable segments
- Download images from URLs with error handling
- Download and save webpages
- Support for multiprocessing to speed up downloads
- Improved error handling and logging
- Customizable output formats for audio and video

## Installation

You can install Dlsys using pip:

```
pip install dlsys
```

## Usage

Here are some examples of how to use Dlsys v2.1.0:

```python
from dlsys import Dlsys

# Download audio from a YouTube video and split it into 60-minute segments
Dlsys().set_url("https://youtu.be/Y3whytmX51w").split(60).audio()

# Download video from a YouTube URL in MP4 format
Dlsys().set_url("https://youtu.be/Y3whytmX51w").set_format("mp4").video()

# Download multiple audio files using multiprocessing
urls = ["https://youtu.be/video1", "https://youtu.be/video2", "https://youtu.be/video3"]
Dlsys().set_url(urls).output_dir("downloads").multi().audio()

# Download images
image_urls = ["https://example.com/image1.jpg", "https://example.com/image2.png"]
Dlsys().set_url(image_urls).output_dir("images").download_images()

# Download webpages
webpage_urls = ["https://example.com", "https://example.org"]
Dlsys().set_url(webpage_urls).output_dir("webpages").download_webpages()
```

## New in v2.1.0

- Added `set_format()` method to specify output format for audio and video
- Improved error handling with more informative error messages
- Enhanced logging capabilities for better debugging
- Performance optimizations for faster downloads
- Updated dependencies to their latest versions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/yourusername/dlsys/issues).

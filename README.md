# Dlsys v2.0.0

Dlsys is a powerful and versatile Python package for downloading and processing various types of content from the internet, including YouTube videos, websites, images, and audio files.

## Features

- Download audio and video from YouTube and other supported platforms
- Split audio files into customizable segments
- Download images from URLs with error handling
- Download and save webpages
- Support for multiprocessing to speed up downloads
- Improved error handling and logging

## Installation

You can install Dlsys using pip:

```
pip install dlsys
```

## Usage

Here are some examples of how to use Dlsys v2.0.0:

```python
from dlsys import Dlsys

# Download audio from a YouTube video and split it into 60-minute segments
Dlsys().set_url("https://youtu.be/Y3whytmX51w").split(60).audio()

# Download video from a YouTube URL
Dlsys().set_url("https://youtu.be/Y3whytmX51w").video()

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

## New in v2.0.0

- Improved error handling and logging
- Added support for video downloads
- Enhanced multiprocessing capabilities
- Updated to support Python 3.7+
- Improved documentation and type hints

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

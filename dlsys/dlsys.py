import yt_dlp
import multiprocessing
import os
import requests
from pathlib import Path
from pydub import AudioSegment
import math

class Dlsys:
    """
    A class for downloading and processing various types of content from the internet.
    This includes YouTube videos, websites, images, and audio files.

    The class provides methods for setting URLs, specifying output directories,
    enabling multiprocessing, splitting audio files, and downloading different types of content.

    Attributes:
        urls (list): A list of URLs to process.
        output_path (str): The output path template for downloaded content.
        output_dir (str): The directory where downloaded content will be saved.
        use_multiprocessing (bool): Whether to use multiprocessing for downloads.
        split_minutes (int): The number of minutes to split audio files into, if specified.

    Example usage:
        # Download audio from a YouTube video and split it into 60-minute segments
        from ytdl import Dlsys
        Dlsys().set_url("https://youtu.be/Y3whytmX51w").split(60).audio()

        # Download multiple audio files using multiprocessing
        urls = ["https://youtu.be/video1", "https://youtu.be/video2", "https://youtu.be/video3"]
        Dlsys().set_url(urls).output_dir("downloads").multi().audio()

        # Download images
        image_urls = ["https://example.com/image1.jpg", "https://example.com/image2.png"]
        Dlsys().set_url(image_urls).output_dir("images").download_images(image_urls)

        # Download webpages
        webpage_urls = ["https://example.com", "https://example.org"]
        Dlsys().set_url(webpage_urls).output_dir("webpages").download_webpages(webpage_urls)
    """
    
    def __init__(self):
        self.urls = []
        self.output_path = '%(title)s.%(ext)s'
        self.output_dir = '.'
        self.use_multiprocessing = False
        self.split_minutes = None

    def set_url(self, urls):
        """Set the URL(s) for download."""
        if isinstance(urls, str):
            self.urls = [urls]
        elif isinstance(urls, list):
            self.urls = urls
        else:
            raise ValueError("URLs must be a string or a list of strings.")
        return self

    def set_output_path(self, output_path):
        """Set the output path for the downloaded content."""
        self.output_path = output_path
        return self

    def output_dir(self, output_dir):
        """Set the output directory for downloaded content."""
        self.output_dir = output_dir
        return self

    def multi(self):
        """Enable multiprocessing for downloads."""
        self.use_multiprocessing = True
        return self

    def split(self, minutes):
        """Set the number of minutes for splitting audio files."""
        self.split_minutes = minutes
        return self

    def audio(self):
        """Download audio from the set URL(s) and optionally split it."""
        if not self.urls:
            raise ValueError("URL(s) not set. Use set_url() method first.")
        
        if len(self.urls) == 1:
            output_file = self._download_audio(self.urls[0])
            if self.split_minutes:
                self.split_audio(output_file, self.split_minutes)
        else:
            output_files = self.download_audios(self.urls)
            if self.split_minutes:
                for file in output_files:
                    self.split_audio(file, self.split_minutes)
        
        return self

    def download_audios(self, audio_urls):
        """
        Download a list of audio files and save them to the output directory using multiprocessing.
        
        :param audio_urls: A list of audio URLs to download.
        :return: A list of output file paths.
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        output_files = []
        if self.use_multiprocessing:
            with multiprocessing.Pool() as pool:
                output_files = pool.map(self._download_audio, audio_urls)
        else:
            for url in audio_urls:
                output_files.append(self._download_audio(url))

        print("All audio files downloaded!")
        return output_files

    def _download_audio(self, url):
        """Helper method to download a single audio file."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.output_dir, self.output_path),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            output_path = os.path.splitext(filename)[0] + '.mp3'
        print(f"Audio downloaded for: {url}")
        return output_path

    def download_image(self, url, output_path):
        """Download a single image and save it to the specified output path."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded and saved to: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image from {url}: {e}")

    def download_images(self, image_urls):
        """
        Download a list of images and save them to the output directory using multiprocessing.
        
        :param image_urls: A list of image URLs to download.
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        if self.use_multiprocessing:
            with multiprocessing.Pool() as pool:
                tasks = []
                for url in image_urls:
                    filename = os.path.basename(url)
                    output_path = os.path.join(self.output_dir, filename)
                    tasks.append(pool.apply_async(self.download_image, args=(url, output_path)))
                
                for task in tasks:
                    task.get()  # Wait for all tasks to complete
        else:
            for url in image_urls:
                filename = os.path.basename(url)
                output_path = os.path.join(self.output_dir, filename)
                self.download_image(url, output_path)

        print("All images downloaded!")
        return self

    def download_webpage(self, url, output_path):
        """Download a single webpage and save it to the specified output path."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            print(f"Webpage downloaded and saved to: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading webpage {url}: {e}")

    def download_webpages(self, webpage_urls):
        """
        Download a list of webpages and save them to the output directory using multiprocessing.
        
        :param webpage_urls: A list of webpage URLs to download.
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        if self.use_multiprocessing:
            with multiprocessing.Pool() as pool:
                tasks = []
                for url in webpage_urls:
                    filename = f"{url.split('://')[-1].replace('/', '_')}.html"
                    output_path = os.path.join(self.output_dir, filename)
                    tasks.append(pool.apply_async(self.download_webpage, args=(url, output_path)))
                
                for task in tasks:
                    task.get()  # Wait for all tasks to complete
        else:
            for url in webpage_urls:
                filename = f"{url.split('://')[-1].replace('/', '_')}.html"
                output_path = os.path.join(self.output_dir, filename)
                self.download_webpage(url, output_path)

        print("All webpages downloaded!")
        return self

    def download_video(self):
        """Download the video from the set URL and save it to the output path."""
        if not self.url:
            raise ValueError("URL not set. Use set_url() method first.")

        ydl_opts = {
            'outtmpl': self.output_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        
        print(f"Video downloaded and saved to: {self.output_path}")
        return self

    @staticmethod
    def download_image(url, output_path):
        """
        Download a single image and save it to the specified output path.
        
        :param url: The URL of the image to download.
        :param output_path: The path to save the downloaded image.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(output_path, 'wb') as file:
                file.write(response.content)

            print(f"Image downloaded and saved to: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image {url}: {e}")

    def download_images(self, image_urls):
        """
        Download a list of images and save them to the output directory using multiprocessing.
        
        :param image_urls: A list of image URLs to download.
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        with multiprocessing.Pool() as pool:
            tasks = []
            for url in image_urls:
                filename = os.path.basename(url)
                output_path = os.path.join(self.output_dir, filename)
                tasks.append(pool.apply_async(self.download_image, args=(url, output_path)))
            
            for task in tasks:
                task.get()  # Wait for all tasks to complete

        print("All images downloaded!")
        return self

    def split_audio(self, input_file, minutes):
        """
        Split an audio file into segments of specified minutes.
        
        :param input_file: Path to the input audio file.
        :param minutes: Number of minutes for each segment.
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist.")
        
        # Load the audio file
        audio = AudioSegment.from_mp3(input_file)
        
        # Calculate the number of segments
        segment_length_ms = minutes * 60 * 1000  # Convert minutes to milliseconds
        num_segments = math.ceil(len(audio) / segment_length_ms)
        
        # Split the audio file
        for i in range(num_segments):
            start_time = i * segment_length_ms
            end_time = (i + 1) * segment_length_ms
            segment = audio[start_time:end_time]
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = f"{base_name}_part{i+1}.mp3"
            output_path = os.path.join(os.path.dirname(input_file), output_filename)
            
            # Export the segment
            segment.export(output_path, format="mp3")
            print(f"Exported: {output_path}")
        
        print(f"Split {input_file} into {num_segments} parts of {minutes} minutes each.")
        return self


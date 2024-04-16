import subprocess
import threading
import time
import os

def download_stream(stream_url, output_path):
    while True:
        try:
            streamlink_command = ["streamlink", "--stream-url", stream_url]
            result = subprocess.run(streamlink_command, capture_output=True, text=True)
            if "error: No streams found on this URL" not in result.stdout:
                print(f"Stream is online. Downloading {stream_url}...")
                download_path = find_available_filename(output_path)
                streamlink_download_command = ["streamlink", stream_url, "best", "-o", download_path]
                subprocess.run(streamlink_download_command)
            else:
                print(f"Stream is offline. Retrying in 30 seconds...")
            time.sleep(30)
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Retrying in 30 seconds...")
            time.sleep(30)

def find_available_filename(output_path):
    if not os.path.exists(output_path):
        return output_path
    
    base_filename, extension = os.path.splitext(output_path)
    counter = 1
    while True:
        numbered_filename = f"{base_filename}_{counter}{extension}"
        if not os.path.exists(numbered_filename):
            return numbered_filename
        counter += 1

if __name__ == "__main__":
    stream_url = input("Enter the stream URL: ").strip()
    filename = input("Enter the filename (excluding extension): ").strip()
    output_path = f"F:/streamlink/{filename}.mp4"  # Default output path
    
    downloader_thread = threading.Thread(target=download_stream, args=(stream_url, output_path))
    downloader_thread.start()
    downloader_thread.join()

# Licensed under the WTFPL License

import os
import time
import aiohttp
import asyncio
from urllib.parse import urlparse

url = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'

async def delay(ms):
    await asyncio.sleep(ms / 1000)

async def download_image(session, image_url, file_path):
    try:
        async with session.get(image_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download image: {response.status}")
            content = await response.read()
            with open(file_path, 'wb') as f:
                f.write(content)
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"⛔ Failed to fetch JSON file: {response.status}")
                json_data = await response.json()
                data = json_data.get('data')
                
                if not data:
                    raise Exception('⛔ JSON does not have a "data" property at its root.')

                download_dir = os.path.join(os.getcwd(), 'downloads')
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                    print(f"📁 Created directory: {download_dir}")

                for file_index, (key, subproperty) in enumerate(data.items(), start=1):
                    if subproperty and subproperty.get('dhd'):
                        image_url = subproperty['dhd']
                        print(f"🔍 Found image URL!")
                        parsed_url = urlparse(image_url)
                        
                        # Extrahiere den Dateinamen ohne .jpg
                        filename = os.path.basename(parsed_url.path).replace('.jpg', '') or f'image_{file_index}'
                        file_path = os.path.join(download_dir, f"{filename}.jpg")

                        await download_image(session, image_url, file_path)
                        print(f"🖼️ Saved image to {file_path}")

                        await delay(250)

    except Exception as e:
        print(f"Error: {str(e)}")

def ascii_art():
    print("""
 /$$      /$$ /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$
| $$$    /$$$| $$  /$$/| $$__  $$ /$$__  $$| $$__  $$
| $$$$  /$$$$| $$ /$$/ | $$  \\ $$| $$  \\__/| $$  \\ $$
| $$ $$/$$ $$| $$$$$/  | $$$$$$$ |  $$$$$$ | $$  | $$
| $$  $$$| $$| $$  $$  | $$__  $$ \\____  $$| $$  | $$
| $$\\  $ | $$| $$\\  $$ | $$  \\ $$ /$$  \\ $$| $$  | $$
| $$ \\/  | $$| $$ \\  $$| $$$$$$$/|  $$$$$$/| $$$$$$$/
|__/     |__/|__/  \\__/|_______/  \\______/ |_______/""")
    print("")
    print("🤑 Starting downloads from your favorite sellout grifter's wallpaper app...")

if __name__ == "__main__":
    ascii_art()
    time.sleep(5)
    asyncio.run(main())

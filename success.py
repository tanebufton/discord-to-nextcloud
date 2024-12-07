from discord.ext.commands import Bot
import json
import datetime
import requests
import time
from nc_py_api import Nextcloud
from io import BytesIO

"""
Load Bot Config
"""
with open('config.json') as file:
    data = json.load(file)
BOT_TOKEN = data['DiscordToken']
BOT_PREFIX = data['prefix']
SUCCESS_CHANNEL_NAME = data['SuccessChannelName']
NEXTCLOUD_SITE = data['nextcloud_url']
NEXTCLOUD_USERNAME = data['nc_username']
NEXTCLOUD_PASSWORD = data['nc_password']

client = Bot(command_prefix = BOT_PREFIX)

"""
Main Bot Code
"""
# Function to ensure folder existence
def ensure_folder_exists(nc, folder_path):
    # Check if the folder exists by listing its parent directory
    parent_path = '/'.join(folder_path.split('/')[:-1])
    folder_name = folder_path.split('/')[-1]
    try:
        # List the parent directory
        nodes = nc.files.listdir(parent_path)
        # Check if the folder exists among the listed nodes
        if not any(node.name == folder_name and node.is_dir for node in nodes):
            # Create the folder if it doesn't exist
            nc.files.mkdir(folder_path)
            print(f"Created folder: {folder_path}")
    except Exception as e:
        print(f"Error checking or creating folder {folder_path}: {e}")

@client.event
async def on_ready():
    print('Success Downloader is Online.')

@client.event
async def on_message(message):
    if message.author.bot:
        pass

    elif (len(message.attachments) != 0 and SUCCESS_CHANNEL_NAME in str(message.channel)):
        for items in message.attachments:
            # Accepted picture extension types
            pic_ext = ['.jpg', '.png', '.jpeg']
            for ext in pic_ext:
                if items.filename.find(ext) != -1:
                    try:
                        # Get the image URL
                        img_url = items.url
                        # Split out Filename - Add's timestamp because images may have same names (e.g. Untitled.png)
                        filename_parts = items.filename.split(".")
                        timestamp = str(int(time.time()))
                        filename = f"{filename_parts[0]}_{timestamp}.{filename_parts[1]}"

                        # Download the image
                        request = requests.get(img_url, stream=True)
                        if request.status_code == 200:
                            buf = BytesIO()
                            for chunk in request.iter_content(1024):
                                buf.write(chunk)
                            buf.seek(0)

                            # Connect to NextCloud Instance
                            nc = Nextcloud(nextcloud_url=NEXTCLOUD_SITE, nc_auth_user=NEXTCLOUD_USERNAME, nc_auth_pass=NEXTCLOUD_PASSWORD)

                            # Move to Local Folder
                            now = datetime.datetime.now()
                            year_folder = f"/Success Images/{now.year}"
                            month_folder = f"{year_folder}/{now.strftime('%B')}"

                            # Ensure year and month folders exist
                            ensure_folder_exists(nc, year_folder)
                            ensure_folder_exists(nc, month_folder)

                            # Construct the remote path
                            remote_path = f"{month_folder}/{filename}"

                            # Upload to Nextcloud
                            nc.files.upload_stream(remote_path, buf)
                            print(f"Uploaded {filename} to Nextcloud at {remote_path}")
                            buf.close() 
                    except:
                        print("Unable to upload")


    await client.process_commands(message)


client.run(BOT_TOKEN)
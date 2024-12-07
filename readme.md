
## Discord to Nextcloud Downloader

Takes images from a Discord channel and uploads them to Nextcloud. Primarily used for [Synergy](https://www.instagram.com/synergy) to save Success posts to be used for our monthly success collages. 

The script will monitor a specific discord channel and save any posted photos to a "Success Images" folder split by Year and Month. 

You can configure  a different base folder by editing the ``year_folder`` string on Line 78. 



### Features
- Uses Discord.py library for Discord bot integration.
- Uses [nc_py_api](https://pypi.org/project/nc-py-api/) for uploading files directly to Nextcloud via API without having to have the folder/software mounted locally.



### Prerequisites

- Python 3.6 or higher
- Discord account
- Bot token (obtained from the Discord Developer Portal)
- Nextcloud (Versions 27, 28, 29 and 30 currently supposed)

### Installation

* Clone this repository to your local machine:

```
git clone https://github.com/tanebufton/discord-to-nextcloud.git
```

* Navigate to the project directory:

```
cd discord-to-nextcloud
```
* Install the required Python packages using pip:
```
pip install -r requirements.txt
```

### Configuration
*  Edit the `config.json` file in the project directory

```
{
    "DiscordToken":"",
    "prefix":"!!!",
    "SuccessChannelName":"",
    "nextcloud_url": "",
    "nc_username": "",
    "nc_password": ""
}
```
* Replace "DiscordToken" with your actual bot token obtained from the Discord Developer Portal.

* Customize the "prefix" - "SuccessChannelName" - "nextcloud_url" - "nc_username" and "nc_password) values as needed.

### Running the bot

Run the bot by executing the main `success.py` file - I would recommend using [PM2](https://pm2.keymetrics.io/) or something similar to have the bot continuously running 24/7 on a server. 



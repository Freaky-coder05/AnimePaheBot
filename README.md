# AnimePaheBot

![AnimePaheBot](https://vault.pictures/p/73f05b1874e841efb87d107779bd4d2d.jpg)

A fully customizable Telegram bot for anime lovers. You can use it to search, download, and manage your favorite anime shows. Built with Python and Pyrogram, it's simple to deploy and easy to modify.

## Features
- **Anime Search**: Find your favorite anime using the `/anime` command.
- **Thumbnail Management**: Set, view, or delete custom thumbnails.
- **Caption Management**: Save, view, or delete custom captions.
- **Upload Options**: Choose between document or video formats for uploads.
- **User Management**: Track all users of the bot.
- **Broadcast Messages**: Send updates to all users.
- **Queue Tracking**: View active downloads.
- **Latest Anime**: Fetch the latest airing anime from AnimePahe.

## Owner Credit
This bot was made by [RAHAT](https://t.me/r4h4t_69). Anyone can modify this bot as they like, but please do not remove the credit.

## How to Deploy
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/TG_AnimePahe_BOT.git
   cd TG_AnimePahe_BOT
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
     API_ID="your_api_id"
     API_HASH="your_api_hash"
     BOT_TOKEN="your_bot_token"
     LOG_CHANNEL="your_log_channel_id"
     MONGO_URL="your_mongo_db_url"
     DB_NAME="your_database_name"
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Bot Commands

### General Commands
| Command             | Description                                   |
|---------------------|-----------------------------------------------|
| `/start`            | Welcome message and menu buttons.            |
| `/help`             | Get assistance with bot commands.            |
| `/latest`           | Fetch the latest airing anime.               |
| `/anime <name>`     | Search for an anime by name.                 |
| `/queue`            | View active downloads in the queue.          |

### Thumbnail Commands
| Command             | Description                                   |
|---------------------|-----------------------------------------------|
| `/set_thumb`        | Set a custom thumbnail (reply to a photo).   |
| `/see_thumb`        | View your current thumbnail.                 |
| `/del_thumb`        | Delete your custom thumbnail.                |

### Caption Commands
| Command             | Description                                   |
|---------------------|-----------------------------------------------|
| `/set_caption`      | Save a custom caption (reply to a text).     |
| `/see_caption`      | View your current caption.                   |
| `/del_caption`      | Delete your custom caption.                  |

### Admin Commands
| Command             | Description                                   |
|---------------------|-----------------------------------------------|
| `/users`            | Get the total number of bot users.           |
| `/broadcast`        | Send a message to all bot users (reply).     |

## Contributing
This bot is open-source, and contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. Let's make this bot even better together!

---
### Disclaimer
This bot is not affiliated with AnimePahe or any other anime platform. Use it responsibly.

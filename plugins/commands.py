#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one requests do not remove my credit..........#

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pyrogram.errors
from bs4 import BeautifulSoup
from plugins.headers import*
from helper.database import*
from plugins.queue import*
from config import START_PIC, ADMIN
import random
import asyncio

user_queries = {}


@Client.on_message(filters.command("start") & filters.private)
def start(client, message):
    # Choose a random image from the list
    
    id = message.from_user.id
    if id not in ADMIN:
        return message.reply_text("❌ Sorry Only Admin can use me")
        
    if not present_user(id):
        try:
            add_user(id)
        except Exception as e:
            client.send_message(-100245790578, f"{e}")
            pass
    start_pic = random.choice(START_PIC)
    
    # Create inline buttons
    buttons = [
        [
            InlineKeyboardButton("Owner", url="https://t.me/Awt_botz"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [
            InlineKeyboardButton("Close", callback_data="close")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Send the welcome message with the random image and inline buttons
    client.send_photo(
        chat_id=message.chat.id,
        photo=start_pic,
        caption="👋 Welcome to the Anime PaheBot! \n\nUse the buttons below for assistance or to contact the owner",
        reply_markup=reply_markup
    )

@Client.on_message(filters.command("set_thumb") & filters.private)
def set_thumbnail(client, message):
    # Check if the message is a reply
    if not message.reply_to_message:
        message.reply_text("Please reply to a photo with this command.")
        return
    
    # Check if the reply is to a photo
    if not message.reply_to_message.photo:
        message.reply_text("Please reply to a photo with this command.")
        return

    # Save the thumbnail
    file_id = message.reply_to_message.photo.file_id
    save_thumbnail(message.from_user.id, file_id)
    message.reply_text("Thumbnail saved successfully!")

# Command: See thumbnail
@Client.on_message(filters.command("see_thumb") & filters.private)
def see_thumbnail(client, message):
    thumbnail = get_thumbnail(message.from_user.id)
    if thumbnail:
        client.send_photo(message.chat.id, thumbnail, caption="Your custom thumbnail.")
    else:
        message.reply_text("No custom thumbnail found in the database.")

# Command: Delete thumbnail
@Client.on_message(filters.command("del_thumb") & filters.private)
def del_thumbnail(client, message):
    if get_thumbnail(message.from_user.id):
        delete_thumbnail(message.from_user.id)
        message.reply_text("Custom thumbnail deleted successfully!")
    else:
        message.reply_text("No custom thumbnail found in the database.")
        
@Client.on_message(filters.command("set_caption") & filters.private)
def save_caption_command(client, message):
    # Check if the message is a reply and if the replied message contains text
    if message.reply_to_message and message.reply_to_message.text:
        caption = message.reply_to_message.text    
        save_caption(message.from_user.id, caption)
        message.reply_text(f"<b>Caption saved:</b> \n\n <code>{caption}</code>")
    else:
        # If the message is not a reply or doesn't contain text, send an error message
        message.reply_text("Please reply to a text message to save it as a caption.")
    
    
 # Command: See caption
@Client.on_message(filters.command("see_caption") & filters.private)
def see_caption_command(client, message):
    caption = get_caption(message.from_user.id)
    if caption:
        message.reply_text(f"<b>Your current caption:</b> \n\n <code>{caption}</code>")
    else:
        message.reply_text("No custom caption found in the database.")   
# Command: Delete caption
@Client.on_message(filters.command("del_caption") & filters.private)
def delete_caption_command(client, message):
    if get_caption(message.from_user.id):
        delete_caption(message.from_user.id)
        message.reply_text("Custom caption deleted successfully!")
    else:
        message.reply_text("No custom caption found in the database.")
        
        
@Client.on_message(filters.command("options") & filters.private)
def set_upload_options(client, message):
    user_id = message.from_user.id
    current_method = get_upload_method(user_id)
    
    # Set checkmarks based on current selection
    document_status = "✅" if current_method == "document" else "❌"
    video_status = "✅" if current_method == "video" else "❌"
    
    # Inline buttons for options
    buttons = [
        [
            InlineKeyboardButton(f"Document ({document_status})", callback_data="set_method_document"),
            InlineKeyboardButton(f"Video ({video_status})", callback_data="set_method_video")
        ],[
            InlineKeyboardButton("Close❌", callback_data="close")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    message.reply_text(f"Your Current Upload Method: {current_method.capitalize()}", reply_markup=reply_markup)


# Command: Search anime
@Client.on_message(filters.command("anime") & filters.private)
def search_anime(client, message):
    id = message.from_user.id
    if id not in ADMIN:
        return message.reply_text("❌ You Can't able to Use this bot")
    if not present_user(id):
        try:
            add_user(id)
        except Exception as e:
            client.send_message(-1002457905787, f"{e}")
            pass
    try:
        query = message.text.split("/anime ", maxsplit=1)[1]
    except IndexError:
        message.reply_text(f"Usage: <code> /anime anime_name</code>")
        return

    search_url = f"https://animepahe.si/api?m=search&q={query.replace(' ', '+')}"
    response = session.get(search_url).json()

    if response['total'] == 0:
        message.reply_text("Anime not found.")
        return

    user_queries[message.chat.id] = query
    anime_buttons = [
        [InlineKeyboardButton(anime['title'], callback_data=f"anime_{anime['session']}")]
        for anime in response['data']
    ]
    anime_buttons.append([InlineKeyboardButton("Close❌", callback_data="close")])
    
    reply_markup = InlineKeyboardMarkup(anime_buttons)
    # Reply to the same message with anime title buttons
    #message.reply_text("Select an anime:", reply_markup=reply_markup, quote=True)
    gif_url = "https://files.catbox.moe/1shkm0.jpg"
    message.reply_video(
        #chat_id=message.chat.id,
        video=gif_url,
        caption=f"Search Reasult For <code>{query}</code>",
        reply_markup=reply_markup,
        quote=True
    )
    
    
WAIT_MSG = """"<b>Processing ...</b>"""
REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""    
@Client.on_message(filters.command('users') & filters.private & filters.user(ADMIN))
def get_users(client, message):
  	msg = client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
  	users = full_userbase()
  	msg.edit(f"{len(users)} users are using this bot")
    
    
@Client.on_message(filters.private & filters.command('broadcast') & filters.user(ADMIN))
async def send_text(client, message):
    if message.reply_to_message:
        query = full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except pyrogram.errors.FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except pyrogram.errors.UserIsBlocked:
                del_user(chat_id)
                blocked += 1
            except pyrogram.errors.InputUserDeactivated:
                del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
    
@Client.on_message(filters.command("queue") & filters.private)
def view_queue(client, message):
    with download_lock:
        if not global_queue:
            message.reply_text("No active downloads.")
            return

        # Count active tasks for each user
        user_task_counts = {}
        for username, link in global_queue:
            user_task_counts[username] = user_task_counts.get(username, 0) + 1

        # Prepare the queue display
        queue_text = "Active Downloads:\n"
        for i, (username, task_count) in enumerate(user_task_counts.items(), start=1):
            # Create a clickable profile link for the user           
            user_profile_link = f"[{username}](https://t.me/{username})"
            queue_text += f"{i}. {user_profile_link} (Active Task = {task_count})\n"

        message.reply_text(queue_text, disable_web_page_preview=True)
@Client.on_message(filters.command("latest") & filters.private)
def send_latest_anime(client, message):
    try:
        # Fetch the latest airing anime from AnimePahe
        API_URL = "https://animepahe.ru/api?m=airing&page=1"
        response = session.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            anime_list = data.get('data', [])

            # Check if any anime is available
            if not anime_list:
                message.reply_text("No latest anime available at the moment.")
                return

            # Prepare the message content with titles and links
            latest_anime_text = "<b>📺 Latest Airing Anime:</b>\n\n"
            for idx, anime in enumerate(anime_list, start=1):
                title = anime.get('anime_title')
                anime_session = anime.get('anime_session')
                episode = anime.get('episode')
                link = f"https://animepahe.ru/anime/{anime_session }"
                latest_anime_text += f"<b>{idx}) <a href='{link}'>{title}</a> [E{episode}]</b>\n"

            # Send the formatted anime list with clickable links
            message.reply_text(latest_anime_text, disable_web_page_preview=True)
        else:
            message.reply_text(f"Failed to fetch data from the API. Status code: {response.status_code}")
    
    except Exception as e:
        client.send_message(-100245790578, f"Error: {e}")
        message.reply_text("Something went wrong. Please try again later.")


@Client.on_message(filters.command("airing") & filters.private)
def send_latest_anime(client, message):
    try:
        # Fetch the latest airing anime from AnimePahe
        API_URL = "https://animepahe.ru/anime/airing"
        response = session.get(API_URL)
        if response.status_code == 200:          
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all anime links
            anime_list = soup.select(".index-wrapper .index a")

            # Check if any anime is available
            if not anime_list:
                message.reply_text("No airing anime available at the moment.")
                return

            # Prepare the message content with titles and links
            airing_anime_text = "<b>🎬 Currently Airing Anime:</b>\n\n"
            for idx, anime in enumerate(anime_list, start=1):
                title = anime.get("title", "Unknown Title")
                link = "https://animepahe.ru" + anime["href"]
                #airing_anime_text += f"<b>{idx}) <a href='{link}'>{title}</a></b>\n"
                airing_anime_text += f"<b>{idx}){title}</b>\n"

            # Send the formatted anime list with clickable links
            message.reply_text(airing_anime_text, disable_web_page_preview=True)
        else:
            message.reply_text(f"Failed to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        # Log the error and notify the user
        #client.send_message(-1002457905787, f"Error: {e}")
        message.reply_text("Something went wrong. Please try again later.")

        

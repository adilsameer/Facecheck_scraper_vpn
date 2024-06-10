import os
import telebot
from telebot import types
import logging
from scraper import Scraper  # Ensure this is your Scraper class

# Configure logging
logging.basicConfig(level=logging.INFO)

# Recommended: Use an environment variable to store your bot key securely
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

if bot_token is None:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

bot = telebot.TeleBot(bot_token)

# Create a directory to save uploaded images
os.makedirs('uploaded_images', exist_ok=True)

scraper = Scraper()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a custom keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🔍 Find Person from Image')
    btn3 = types.KeyboardButton('🔗 APIs')
    btn4 = types.KeyboardButton('ℹ️ Learn More')
    markup.add(btn1, btn3, btn4)

    # Send a welcome message with the custom keyboard
    welcome_message = (
        "🤖 Hello! This bot can do the following:\n"
        "1. 🔍 Find Person from Image\n"
        "2. 🔗 APIs\n"
        "3. ℹ️ Learn More\n\n"
        "Please choose an option from the menu below."
    )
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🔍 Find Person from Image")
def find_image(message):
    bot.send_message(message.chat.id, "📤 Please upload Person image to proceed.")


@bot.message_handler(func=lambda message: message.text == "🔗 APIs")
def apis(message):
    api_info = (
        "🔗 You selected 'APIs'. Here are some useful APIs:\n"
        "- API 1: /upload takes post request and image file to scan and return unique image_id\n"
        "- API 2: /results/<image_id> get results of uploaded search\n"
    )
    bot.send_message(message.chat.id, api_info)


@bot.message_handler(func=lambda message: message.text == "ℹ️ Learn More")
def learn_more(message):
    learn_more_info = (
        "ℹ️Here's more information about this bot:\n"
        "This bot helps you with image processing, uploading images, and accessing various APIs. "
        "Feel free to explore the options from the menu."
    )
    bot.send_message(message.chat.id, learn_more_info)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image_path = os.path.join('uploaded_images', file_info.file_path.split('/')[-1])
        logging.info(f"Saving image to: {image_path}")

        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        logging.info("Image saved successfully.")

        bot.send_message(message.chat.id, "📤 Image uploaded successfully. Processing...")

        # Process the uploaded image with Scraper
        scraper.main(fr"absolute path{image_path}")

        # Check the scraper's logs and send them to the user
        if scraper.extracted_urls:
            bot.send_message(message.chat.id, "🔍 Search Completed. Extracted URLs:")
            for url in scraper.extracted_urls:
                bot.send_message(message.chat.id, f"🔗 Found URL: {url}")
        else:
            bot.send_message(message.chat.id, "❌ Captcha Solved failed or No URLs found in the image.\nTry again after "
                                              "sometime.")

        # Delete the processed image
        if os.path.exists(image_path):
            os.remove(image_path)
            logging.info("Processed image deleted.")
        else:
            logging.error("Failed to delete processed image. File does not exist.")

    except Exception as e:
        logging.error(f"Error handling image: {e}")
        bot.send_message(message.chat.id, "❌ An error occurred while processing the image.")


# Start polling to keep the bot running and listening for incoming messages
bot.polling()

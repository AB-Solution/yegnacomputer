import telebot
import os

# Get the Telegram Bot Token from Render's environment variables
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Dictionary to store user details
user_data = {}

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to የኛ - Yegna Computer Bot! 🤖\nUse the web form to register and upload a PDF document.")

# Save user data and send confirmation
@bot.message_handler(commands=['save_data'])
def save_data(message):
    try:
        # Extract data sent via the webpage
        data = message.text.split('|')
        if len(data) != 3:
            bot.reply_to(message, "Invalid format. Please try again.")
            return

        _, name, id_number = data

        # Validate ID number format
        if not id_number or len(id_number) != 14 or '-' not in id_number:
            bot.reply_to(message, "Invalid ID number format. It must be in the format 1234-5678-9101.")
            return

        username = message.chat.username if message.chat.username else "No username available"

        # Save data to user_data dictionary
        user_data[message.chat.id] = {'name': name, 'id_number': id_number, 'username': username}

        # Send confirmation message
        confirmation_message = (
            f"✅ Your data has been saved successfully!\n\n"
            f"**Name:** {name}\n"
            f"**ID Number:** {id_number}\n"
            f"**Telegram Username:** @{username}\n\n"
            f"Now, you can upload your PDF file."
        )
        bot.send_message(message.chat.id, confirmation_message, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Handle PDF uploads and send confirmation
@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    try:
        # Save the uploaded PDF
        if message.document.mime_type == 'application/pdf':
            bot.reply_to(
                message,
                f"✅ Thank you! Your PDF file **{message.document.file_name}** has been uploaded successfully.",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(message, "⚠️ Only PDF files are allowed. Please try again.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Run the bot
if __name__ == "__main__":
    print("Yegna Computer Bot is running...")
    bot.infinity_polling()

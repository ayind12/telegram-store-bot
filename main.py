import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://prodseller.com/v1'
HEADERS = {'X-Api-Key': API_KEY}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to the Reseller Bot! Use /buy <product_id> to purchase."
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Usage: /buy <product_id>'
        )
        return

    product_id = args[0]

    # Simulate API call to create an order
    try:
        response = requests.post(
            f"{BASE_URL}/orders",
            headers=HEADERS,
            json={"productId": product_id, "quantity": 1}
        )
        order = response.json()

        if 'error' in order:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Error: {order['error']}"
            )
        else:
            delivery_key = order.get('deliveredKey', 'Pending delivery')
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Key: {delivery_key}"
            )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while processing your order."
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    buy_handler = CommandHandler('buy', buy)

    application.add_handler(start_handler)
    application.add_handler(buy_handler)

    application.run_polling()

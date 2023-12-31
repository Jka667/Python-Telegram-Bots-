import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from collections import Counter

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store referral links and track activities
referral_links = {}
referral_activities = Counter()

# Admin user ID - replace with the actual admin's user ID
admin_user_id = 1005068235

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    referral_links[user_id] = f'https://t.me/hopopo667?start={user_id}'
    update.message.reply_text(f'Your referral link: {referral_links[user_id]}')

# Define the stats command to track referral activities
def stats(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    referrer_count = referral_activities[user_id]
    update.message.reply_text(f'You have referred {referrer_count} users.')

# Define the top command to display top referrers to the admin
def top(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != admin_user_id:
        update.message.reply_text("You are not authorized to use this command.")
        return

    top_referrers = referral_activities.most_common(3)  # Adjust the number as needed
    message = "Top Referrers:\n"
    
    for rank, (referrer_id, count) in enumerate(top_referrers, start=1):
        message += f"{rank}. User {referrer_id}: {count} referrals\n"
    
    update.message.reply_text(message)

# Define a handler to track new users and referral activities
def track_referral(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the user was referred by someone
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        referral_activities[referrer_id] += 1
        logger.info(f"User {user_id} referred by {referrer_id}")

    # Other processing logic can go here

# Set up the bot
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("6006582026:AAGx71HPzA43UJ-lmJglw-_cFgM_UDCffyQ")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("top", top))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()

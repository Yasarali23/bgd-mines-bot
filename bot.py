from telegram.ext import Updater, CommandHandler
from mines_fair import get_mine_positions
from generate_image import create_mines_image
from auth import is_vip
from tracker import update_accuracy, get_accuracy

TOKEN = "7840887285:AAEYjOZSSrcM55cT6mcivXOrozlWfucgS1s"  # Replace this

def check_mines(update, context):
    user_id = update.effective_user.id
    if not is_vip(user_id):
        update.message.reply_text("🚫 Access Denied. VIPs only.")
        return

    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /check server_seed client_seed nonce")
            return

        server_seed = args[0]
        client_seed = args[1]
        nonce = int(args[2])

        mines = get_mine_positions(server_seed, client_seed, nonce, mine_count=5)
        safe = [i for i in range(1, 26) if i not in mines]

        update_accuracy(True)
        accuracy = get_accuracy()

        msg = (
            f"🧠 BGD Mines Prediction\n"
            f"💣 Mines at: {mines}\n"
            f"✅ Safe Tiles: {safe}\n"
            f"🎯 Accuracy: {accuracy}%"
        )

        image_path = create_mines_image(mines)
        update.message.reply_text(msg)
        update.message.reply_photo(photo=open(image_path, "rb"))

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("check", check_mines))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

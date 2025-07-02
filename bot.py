import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from mines_fair import get_mine_positions
from generate_image import create_mines_image
from auth import is_vip
from tracker import update_accuracy, get_accuracy

TOKEN = os.getenv("7840887285:AAEYjOZSSrcM55cT6mcivXOrozlWfucgS1s") or "7840887285:AAEYjOZSSrcM55cT6mcivXOrozlWfucgS1s"  # Replace with your token if not using env var

async def check_mines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_vip(user_id):
        await update.message.reply_text("🚫 Access Denied. VIPs only.")
        return

    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Usage: /check server_seed client_seed nonce")
        return

    try:
        server_seed = args[0]
        #client_seed = args[1]
        #nonce = int(args[2])

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
        await update.message.reply_text(msg)
        await update.message.reply_photo(photo=InputFile(image_path))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("check", check_mines))
    app.run_polling()

if __name__ == "__main__":
    main()

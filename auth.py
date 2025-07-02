# Add your own Telegram user ID
VIP_USERS = {
    5720602195  # Replace this with your ID
}

def is_vip(user_id):
    return user_id in VIP_USERS

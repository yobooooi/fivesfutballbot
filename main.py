import logging
import telebot

from telebot import types

API_TOKEN = "5222376568:AAEgdxQHZjH8pvUr7NBx-CaYUzIJtp0sbgI"

bot = telebot.TeleBot(API_TOKEN)
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

player_dict = {}
available_slots = [
    "Wed, 6 April @ 20h00, Fives Futbol, Pinehurst ",
    "Wed, 13 April @ 20h00, Pinehurst",
]


class Player:
    def __init__(self, name):
        self.name = name
        self.payment_method = None
        self.slot = None


# Handle '/register' and '/help'
@bot.message_handler(commands=["register"])
def send_welcome(message):
    msg = bot.reply_to(
        message,
        """\
Hi there, I am the FivesFutball bot.
What's your name?
""",
    )
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        player = Player(name)
        player_dict[chat_id] = player

        # adding markup for payment option
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Card", "Cash")
        msg = bot.reply_to(message, "What is your payment method?", reply_markup=markup)

        bot.register_next_step_handler(msg, process_payment_method)
    except Exception as e:
        bot.reply_to(message, "oooops")


def process_payment_method(message):
    try:
        chat_id = message.chat.id
        payment_method = message.text
        player = player_dict[chat_id]
        player.payment_method = payment_method

        # adding markup for selection of booking slot
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(available_slots[0], available_slots[1])
        msg = bot.reply_to(
            message, "Select the time slot you're playing?", reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_time_slot)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "oooops")


def process_time_slot(message):
    try:
        chat_id = message.chat.id
        time_slot = message.text
        player = player_dict[chat_id]
        player.slot = time_slot

        # respondinng with confirmation of booking
        bot.send_message(
            chat_id,
            "Thank you {0}\n Your booking referece is {1} \n Payment Method is {2} \n The slot you selected {3}".format(
              player.name,
              chat_id,
              player.payment_method,
              player.slot
            )
        )
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "oooops")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()

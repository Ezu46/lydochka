import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '6839626610:AAFLkqTWyc_6zXN_PKrlgHaRxAMDnndWRDY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_button = KeyboardButton("🎰 Запустить лудку 🎰")
coin_button = KeyboardButton("🪙 Подбросить монетку 🪙")
markup = ReplyKeyboardMarkup(resize_keyboard=True).row(start_button, coin_button)

coin_tossing_users = {} 

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    url = "https://topdevka.com/uploads/posts/2023-01/1673922609_1-topdevka-com-p-erotika-bolshie-siski-libbi-smit-1.jpg"
    await message.reply_photo(photo=url, caption="здарова бандиты")

@dp.message_handler(lambda message: message.text == "🪙 Подбросить монетку 🪙")
async def initiate_coin_toss(message: types.Message):
    coin_tossing_users[message.from_user.id] = None
    await message.answer("Выберите сторону монеты:", reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True
    ).add(KeyboardButton("Орёл")).add(KeyboardButton("Решка")))

@dp.message_handler(lambda message: message.text.lower() in ["орёл", "решка"] and message.from_user.id in coin_tossing_users)
async def coin_guess(message: types.Message):
    user_guess = message.text.lower()
    coin_tossing_users[message.from_user.id] = user_guess
    await message.answer(f"Вы выбрали: {user_guess}\nОжидаем результат подбрасывания монеты...", reply_markup=ReplyKeyboardRemove())

    if None not in coin_tossing_users.values():
        await process_coin_toss(message.chat.id, message.from_user.id)
        coin_tossing_users.pop(message.from_user.id)

@dp.message_handler(lambda message: message.text == "🎰 Запустить лудку 🎰")
async def play_casino(message: types.Message):
    await message.answer("🎰 Крутим барабаны... 🎰")
    result = "Поздравляем, вы выиграли!"
    await message.answer(result)

async def process_coin_toss(chat_id: int, user_id: int):
    user_guess = coin_tossing_users[user_id]
    coin_result = random.choice(["орёл", "решка"])

    result = f"Результат подбрасывания монеты: {coin_result}\n"
    if user_guess == coin_result:
        result += "Поздравляем, вы угадали!"
    else:
        result += "Увы, попробуйте еще раз!"

    await bot.send_message(chat_id, result, reply_markup=markup)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

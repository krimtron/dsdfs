import aiogram
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.state import State, StatesGroup
import random
import asyncio
from aiogram.filters import Command

bot = Bot(token=' ')
dp = Dispatcher()

correct_answers = 0
incorrect_answers = 0

class Test(StatesGroup):
    first_question = State()

@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    global correct_answers, incorrect_answers
    correct_answers = 0
    incorrect_answers = 0
    await message.reply("Привіт! Я готовий перевіряти твої знання математики. Готовий до першого питання? (введіть 'я готовий')")

@dp.message(lambda message: message.text.startswith("Я готов"))
async def generate_question(message: types.Message):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])

    correct_result = eval(f"{num1} {operator} {num2}")
    question_text = f"{correct_result}\nДалі 4е кнопки з варіантами примерів:\n"

    answer_options = [f"{random.randint(1, 10)} {random.choice(['+', '-', '*'])} {random.randint(1, 10)}" for _ in range(3)]
    answer_options.append(f"{num1} {operator} {num2}")
    random.shuffle(answer_options)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in answer_options:
        markup.add(KeyboardButton(option))

    await message.reply(question_text, reply_markup=markup)

@dp.message()
async def check_answer(message: types.Message):
    global correct_answers, incorrect_answers
    expression = message.text
    correct_result = eval(expression)
    
    if expression == f"{correct_result}":
        correct_answers += 1
        await message.reply("Правильно!")
    else:
        incorrect_answers += 1
        await message.reply(f"Невірно. Правильна відповідь {correct_result}.")

async def main():
    print("Starting bot...")
    print("Bot username: @{}".format((await bot.me())))
    await dp.start_polling(bot)

asyncio.run(main())

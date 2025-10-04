
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.utils import executor

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "8389408896:AAFVlqYmx_NDhF_EmejgepbF5cRhkmKg9og"  # вставьте сюда токен от BotFather
ADMIN_ID = 8053866861           # вставьте сюда ваш Telegram ID
# ========================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Клавиатура с кнопкой "Предложить новость"
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Предложить новость"))

# ====== Хэндлеры ======

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    text = (
        "Приветствуем тебя! Ты попал в Наш информационный портал проекта Rozetked!\n\n"
        "Чтобы предложить новость — нажми кнопку «Предложить новость»."
    )
    await message.answer(text, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Предложить новость")
async def propose_news(message: types.Message):
    text = "Введите вашу новость (можно прикрепить фото или файл):"
    await message.answer(text)

# Получаем текст от пользователя
@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: types.Message):
    if message.text == "/start" or message.text == "Предложить новость":
        return
    forward_text = f"Новость от @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}):\n\n{message.text}"
    await bot.send_message(ADMIN_ID, forward_text)
    await message.answer("Ваше сообщение было отправлено! Ожидайте ответа от администратора.")

# Получаем фото или документ
@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def handle_file(message: types.Message):
    caption = message.caption or ""
    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        await bot.send_photo(ADMIN_ID, photo=file_id, caption=f"Новость от @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}):\n\n{caption}")
    else:
        file_id = message.document.file_id
        await bot.send_document(ADMIN_ID, document=file_id, caption=f"Новость от @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}):\n\n{caption}")
    await message.answer("Ваше сообщение было отправлено! Ожидайте ответа от администратора.")

# ====== ЗАПУСК БОТА ======
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import logging
import aiosqlite
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router
import asyncio
logging.basicConfig(level=logging.INFO)

SUPPORT_CHAT_ID = -100  # Замените на ID вашего чата поддержки

bot = Bot(token='token') # Укажите токен бота с botfather
dp = Dispatcher()
router = Router()
dp.include_router(router)

DATABASE = 'topics.db'

class QuestionState(StatesGroup):
    waiting_for_question = State()

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_topics (
                user_id INTEGER PRIMARY KEY,
                message_thread_id INTEGER NOT NULL
            )
        """)
        await db.commit()

async def get_topic_id(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT message_thread_id FROM user_topics WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def get_user_id_by_topic(message_thread_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT user_id FROM user_topics WHERE message_thread_id = ?", (message_thread_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def save_topic_id(user_id: int, message_thread_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT OR REPLACE INTO user_topics (user_id, message_thread_id) VALUES (?, ?)",
                         (user_id, message_thread_id))
        await db.commit()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Задать вопрос", callback_data="ask_question")
    keyboard.adjust(1)
   
    await message.answer("Привет! Нажми на кнопку, чтобы задать вопрос.", reply_markup=keyboard.as_markup())

@router.callback_query(F.data == "ask_question")
async def process_callback_ask_question(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        # Проверяем, есть ли топик для пользователя в базе данных
        topic_id = await get_topic_id(callback_query.from_user.id)
       
        if topic_id is None:
            # Если топика нет, создаем новый
            topic = await bot.create_forum_topic(chat_id=SUPPORT_CHAT_ID,
                                                 name=callback_query.from_user.full_name)
            topic_id = topic.message_thread_id
            # Сохраняем ID топика в базу данных
            await save_topic_id(callback_query.from_user.id, topic_id)
       
        await callback_query.message.answer("Пожалуйста, введите ваш вопрос:")
        await state.set_state(QuestionState.waiting_for_question)
       
    except Exception as e:
        logging.error(f"Ошибка при создании топика: {e}")
        await callback_query.message.answer("Произошла ошибка при создании топика.")

@router.message(StateFilter(QuestionState.waiting_for_question))
async def handle_question(message: types.Message, state: FSMContext):
    try:
        # Получаем ID топика из базы данных
        topic_id = await get_topic_id(message.from_user.id)
       
        if topic_id:
            await bot.send_message(chat_id=SUPPORT_CHAT_ID,
                                   text=f"Вопрос от {message.from_user.full_name}: {message.text}",
                                   message_thread_id=topic_id)
            await message.answer("Ваш вопрос отправлен в поддержку, скоро с вами свяжутся.")
            await state.clear()
        else:
            await message.answer("Ошибка: бот не может отправить сообщение в этом чате.")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в топик: {e}")
        await message.answer("Произошла ошибка при отправке сообщения в топик.")

@router.message(F.reply_to_message)
async def handle_reply(message: types.Message):
    try:
        # Проверяем, есть ли сообщение, на которое отвечает администратор
        if message.reply_to_message:
            # Получаем ID топика из сообщения, на которое отвечает администратор
            topic_id = message.reply_to_message.message_thread_id
            # Получаем ID пользователя, которому принадлежит этот топик
            user_id = await get_user_id_by_topic(topic_id)
           
            if user_id:
                # Отправляем ответ пользователю
                await bot.send_message(chat_id=user_id,
                                       text=f"Ответ от поддержки: {message.text}")
            else:
                await message.answer("Ошибка: не удалось найти пользователя для этого топика.")
    except Exception as e:
        logging.error(f"Ошибка при отправке ответа пользователю: {e}")
        await message.answer("Произошла ошибка при отправке ответа пользователю.")

if __name__ == "__main__":
    asyncio.run(init_db())
    dp.run_polling(bot)
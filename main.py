from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram import Bot, Dispatcher, executor
from config import group_id, bot_token, get_psql_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
import db_utils
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

user_status = {}

@dp.message_handler(commands=['start', 'admin'])
async def handle_command(message) -> None:
    if message.text == '/start':
            
        db_utils.save_user(
            session=session,
            user_id=message.from_user.id,
            language=message.from_user.locale.language,
            count_offers=0,
            created=date.today()
        )
        # Button to suggest
        km = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton(text="Suggest post", callback_data="suggest")
        km.add(button1)
        await bot.send_message(text="Hello there!",
                                chat_id=message.from_user.id,
                                reply_markup=km)
    
    elif message.text == '/admin':
        # Button to stats
        km = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton(text="Stats 📊", callback_data="stats")
        km.add(button1)
        
        await bot.send_message(
                text="Admin menu",
                chat_id=message.from_user.id,
                reply_markup=km)

@dp.message_handler(content_types=ContentType.ANY)
async def forward_to_channel(message) -> None:
    # Forwards the suggestion to the chat
    if message.from_user.id in user_status:

        if user_status[message.from_user.id]["status"] == "suggest":

            del user_status[message.from_user.id]
            await message.forward(chat_id=group_id)
            db_utils.update_count_offers(session=session, id=message.from_user.id)



@dp.callback_query_handler()
async def handle_callbacks(callback):
    # reveals sum of suggestions
    if callback.data == "stats":

        return await bot.send_message(
            text=db_utils.get_sum_of_all_count_offers(session=session),
            chat_id=callback.from_user.id)
    # inits the suggestion 
    elif callback.data == "suggest":

        user_status[callback.from_user.id] = {
            "status": ""
        }

        user_status[callback.from_user.id]["status"] = "suggest"
        return await bot.send_message(text="Now send your idea", chat_id=callback.from_user.id)


if __name__ == "__main__":
    # Database engine (Example data provided)
    engine = create_engine(
                get_psql_url(
                            "w", "214214", "localhost",
                            5432, "tg_database"),
                echo=False, encoding='utf-8')
    # Database session
    db_utils.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Bot's polling
    executor.start_polling(dp, skip_updates=True)
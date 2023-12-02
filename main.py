import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '6644783891:AAHo2pRq-tMYZtur_oc1j77hiH3MgQ-xGxY'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

censure = []
with open('censure.txt', 'r', encoding='utf8') as file:
    for word in file:
        censure.append(''.join(word.split()))


async def delete_message(chat_id, message_id):
    await asyncio.sleep(600)  # 3600 - 1 ЧАС
    await bot.delete_message(chat_id, message_id)


@dp.message_handler(content_types=['new_chat_members'])
async def welcome(message: types.Message):
    for new_member in message.new_chat_members:
        welcome_text = (
            f'Добро пожаловать в чат, <b>{new_member.first_name}!</b>👋\n\n'

            f'<i><a href="https://t.me/c/1922812627/1">#general</a></i>'
            f'Общение и обмен информацией.\n'

            f'<i><a href="https://t.me/c/1922812627/102">#useful_things</a></i>'
            f'Обмен полезными ресурсами.\n'

            f'<i><a href="https://t.me/c/1922812627/18">#study</a></i>'
            f'Информация связанные с учебой.'
        )

        sent_message = await message.reply(welcome_text, parse_mode='html')
        await message.delete()
        asyncio.create_task(
            delete_message(message.chat.id, sent_message.message_id)
        )


@dp.message_handler(content_types=['left_chat_member'])
async def user_left(message: types.Message):
    await message.delete()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f'Привет, <b>{message.from_user.first_name}!!</b>👋', parse_mode='html'
    )


@dp.message_handler(commands=['info'])
async def user_info(message: types.Message):
    user = message.from_user
    chat_member = await bot.get_chat_member(message.chat.id, user.id)
    status = 'Unknown'
    if chat_member.status == 'member':
        status = 'Участник'
    elif chat_member.status == 'administrator':
        status = 'Администратор'
    elif chat_member.status == 'creator':
        status = 'Создатель'

    await message.answer(
        f'🆔 ID: {user.id}\n'
        f'👱 Имя: {user.first_name}\n'
        f'🌐 Имя пользователя: @{user.username}\n'
        f'👮 Статус: {status}\n'

    )


@dp.message_handler()
async def delete(message: types.Message):
    message_list = message.text.lower().split()
    for user_message in message_list:
        if user_message in censure:
            await message.delete()
            await message.answer('😡 Ай-яй-яй :)')
            censure_info = (
                f'От: {message.from_user.first_name}\n'
                f'@{message.from_user.username}\n\n'
                f'{message.text}'
            )

            await bot.send_message(chat_id=5108798186, text=censure_info)
            await bot.send_message(chat_id=375711858, text=censure_info)
            return

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)

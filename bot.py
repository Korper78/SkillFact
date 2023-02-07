from aiogram.filters import Command
from aiogram.types import Message
from loader import dp, bot


@dp.message(Command('start'))
async def command_start(message: Message):
    await message.delete()
    await message.answer('Вас приветствует бот - генератор паролей. нажмите кнопку для создания пароля')


if __name__ == '__main__':
    dp.run_polling(bot)

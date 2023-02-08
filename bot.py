from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from loader import dp, bot
from passgen import pass_gen


class EnterLength(StatesGroup):
    message = State()
    pass_length = State()
    choice = State()
    chars = State()
    digits = State()
    symbols = State()


class MenuCbData(CallbackData, prefix='menu'):
    choice: str = ''


menu_kb = [
    [InlineKeyboardButton(text='Пароль из букв', callback_data=MenuCbData(choice='chars').pack())],
    [InlineKeyboardButton(text='Пароль из букв и цифр', callback_data=MenuCbData(choice='digits').pack())],
    [InlineKeyboardButton(text='Пароль из букв, цифр и символов', callback_data=MenuCbData(choice='symbols').pack())],
    [InlineKeyboardButton(text='Ввести заново длину пароля', callback_data=MenuCbData(choice='back').pack())]
]


async def delete_prev_message(message: Message, message_id: int) -> None:
    if message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    return


@dp.message(Command(commands=['start', 'cancel']))
async def command_start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await delete_prev_message(message, data.get('message'))
    m = await message.answer(
        'Вас приветствует бот - генератор паролей. Введите желаемую длину пароля (от 5 до 15 символов):')
    await state.update_data(message=m.message_id)
    await state.set_state(EnterLength.pass_length)


@dp.message(Command('help'))
async def command_help(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    # await data['message'].delete()
    await delete_prev_message(message, data.get('message'))
    m = await message.answer("""Этот бот генерирует пароли из латинских букв, цифр и спецсимволов.
                                Вводите необходимые данные, используя цировую клавиатуру.
                                Введите '/cancel', чтобы отменить ввод.
                                Введите '/start', чтобы начать.""")
    await state.update_data(message=m.message_id)


@dp.message(EnterLength.pass_length, F.text.regexp(r'\d+'))
async def enter_password_length(message: Message, state: FSMContext):
    pass_length = int(message.text)
    data = await state.get_data()
    await delete_prev_message(message, data.get('message'))
    await message.delete()
    if 4 < pass_length < 16:
        await state.update_data(pass_length=pass_length)
        m = await message.answer(text='Отлично! Теперь выберите вариант пароля:',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=menu_kb))
        await state.update_data(message=m.message_id)
    else:
        m = await message.answer('Введите желаемую длину пароля (от 5 до 15 символов):')
        await state.update_data(message=m.message_id)


@dp.callback_query(MenuCbData.filter(F.choice == 'chars'))
async def select_chars(callback: CallbackQuery, callback_data: MenuCbData, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await state.update_data(chars=data['pass_length'])
    await state.update_data(digits=0)
    await state.update_data(symbols=0)
    await print_password(callback.message, state)


@dp.callback_query(MenuCbData.filter(F.choice == 'digits'))
async def select_digits(callback: CallbackQuery, callback_data: MenuCbData, state: FSMContext):
    # await callback.message.delete()
    # data = await state.get_data()
    # await state.update_data(chars=data['pass_length'])
    await state.update_data(digits=1)
    await state.update_data(symbols=0)
    await callback.message.edit_text('Введите количество латинских букв:', reply_markup=None)
    await state.set_state(EnterLength.chars)


@dp.callback_query(MenuCbData.filter(F.choice == 'symbols'))
async def select_symbols(callback: CallbackQuery, callback_data: MenuCbData, state: FSMContext):
    await state.update_data(digits=1)
    await state.update_data(symbols=1)
    await callback.message.edit_text('Введите количество латинских букв:', reply_markup=None)
    await state.set_state(EnterLength.chars)


@dp.callback_query(MenuCbData.filter(F.choice == 'back'))
async def select_back(callback: CallbackQuery, callback_data: MenuCbData, state: FSMContext):
    await state.update_data(message=0)
    await command_start(callback.message, state)


@dp.message(EnterLength.chars, F.text.regexp(r'\d+'))
async def enter_chars_length(message: Message, state: FSMContext):
    chars = int(message.text)
    data = await state.get_data()
    await delete_prev_message(message, data.get('message'))
    await message.delete()
    if chars and (chars + data['digits'] + data['symbols']) <= data['pass_length']:
        await state.update_data(chars=chars)
        if data['symbols']:
            m = await message.answer(text='Принято! Теперь введите количество цифр:')
            await state.update_data(message=m.message_id)
            await state.set_state(EnterLength.digits)
        else:
            await state.update_data(digits=(data['pass_length'] - chars))
            await print_password(message, state)
    else:
        m = await message.answer('Неверный ввод. Введите количество латинских букв:')
        await state.update_data(message=m.message_id)


@dp.message(EnterLength.digits, F.text.regexp(r'\d+'))
async def enter_digits_length(message: Message, state: FSMContext):
    digits = int(message.text)
    data = await state.get_data()
    await delete_prev_message(message, data.get('message'))
    await message.delete()
    if digits and (digits + data['chars'] + data['symbols']) <= data['pass_length']:
        await state.update_data(digits=digits)
        await state.update_data(symbols=(data['pass_length'] - data['chars'] - digits))
        await print_password(message, state)
    else:
        m = await message.answer('Неверный ввод. Введите количество цифр:')
        await state.update_data(message=m.message_id)


async def print_password(message: Message, state: FSMContext):
    data = await state.get_data()
    password = await pass_gen(data['chars'], data['digits'], data['symbols'])
    m = await message.answer(f'Принято! Ваш пароль <code>{password}</code>.\n Введите для /start продолжения',
                             reply_markup=None)
    await state.update_data(message=m.message_id)


@dp.message()
async def enter_wrong_text(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await delete_prev_message(message, data.get('message'))
    m = await message.answer(text='Что-то не то! Повторите ввод')
    await state.update_data(message=m.message_id)


if __name__ == '__main__':
    dp.run_polling(bot)

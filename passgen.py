from string import ascii_letters, digits
from random import sample, shuffle
from time import sleep

symbols = '[]{}()*/,.!?+-_#@%&'
template = ascii_letters + digits + '[]{}()*/,.!?+-_#@%&'


def passgen() -> None:
    pass_length = 0
    while pass_length < 5 or pass_length > 16:
        try:
            pass_length = int(input('Введите желаемую длину пароля:') or 0)
            if pass_length < 5:
                print('Пароль слишком короткий' if pass_length > 0 else 'Введите значение больше 0')
            elif pass_length > 16:
                print('Пароль слишком длинный')
            else:
                print('Отлично! Ща сгенерим!')
        except ValueError:
            print('Введите положительное целое число!')
            # pass_length = 0
    password = ''.join(sample(template, pass_length))
    sleep(3)
    print('Ваш пароль: ', password)
    return


async def pass_gen(chars, digs, symbs) -> str:
    _chars = sample(ascii_letters, chars)
    _digs = sample(digits, digs)
    _symbs = sample(symbols, symbs)
    password = _chars + _digs + _symbs
    shuffle(password)
    return ''.join(password)


if __name__ == '__main__':
    passgen()

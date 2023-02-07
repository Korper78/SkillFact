from string import ascii_letters, digits
from random import sample
from time import sleep

template = ascii_letters + digits + '[]{}()*,!?-_'


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


async def pass_gen() -> None:
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
    return password


if __name__ == '__main__':
    passgen()

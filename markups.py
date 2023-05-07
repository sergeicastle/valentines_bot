from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

# Инлайн клавиатура главное меню
mainMenu = InlineKeyboardMarkup(row_width=1)
btn1m = InlineKeyboardButton(text='Открыть сердце', callback_data='btnOpenHeart')
btn2m = InlineKeyboardButton(text='Создать сердце', callback_data='btnCreateHeart123')
mainMenu.add(btn1m, btn2m)

# Инлайн клавиатура для оплаты
mainPayment = InlineKeyboardMarkup(row_width=1)
btn1p = InlineKeyboardButton(text='Оплата - 100 руб.', callback_data='btnPayment')
mainPayment.add(btn1p)

# Реплай клавиатура выбора ответов на вопрос
answer1 = KeyboardButton('1')
answer2 = KeyboardButton('2')
answer3 = KeyboardButton('3')
answer4 = KeyboardButton('4')

mainAnswer = ReplyKeyboardMarkup(resize_keyboard=True).row(answer1, answer2, answer3, answer4)


def buy_meny(isURL=True, url='', bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isURL:
        btnUrlQIWI = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.add(btnUrlQIWI)

    btnCheckQIWI = InlineKeyboardButton(text='Проверить оплату', callback_data='check_' + bill)
    qiwiMenu.add(btnCheckQIWI)
    return qiwiMenu

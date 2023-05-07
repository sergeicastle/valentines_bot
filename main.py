import random
import markups as nav
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from pyqiwip2p import QiwiP2P

from create_bot import dp, bot, QIWI_TOKEN
from db import Database

db = Database('database.db')
p2p = QiwiP2P(auth_key=QIWI_TOKEN)


# создаем класс для машины состояний: фото, текст вопроса, 4 варианта ответа, правильный ответ
class FSMAdmin(StatesGroup):
    photo = State()
    text = State()
    answer1 = State()
    answer2 = State()
    answer3 = State()
    answer4 = State()
    correct_answer = State()


# обрабатываем команду создания новой валентинки
@dp.message_handler(commands='create', state=None)
async def create_heart(message: types.Message):
    # проверяем чтобы пользователь создал не больше 5 вопросов викторины
    if db.get_count(message.from_user.id) < 6 and db.get_status(message.from_user.id) == 'create':
        # переводим машину состояний в ожидание отправки фотографии
        await FSMAdmin.photo.set()
        x = db.get_count(message.from_user.id)
        await message.reply(f'Загрузи картинку для {x} вопроса (обязательно поставь галочку ✅ сжать изображение)')
    else:
        await message.reply('Ты уже загрузил 5 вопросов, выбирай что сделать дальше')


# обрабатываем машину состояний, сохраняем фотографию в словарь
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = db.get_count(message.from_user.id)
        data['secretword'] = db.get_secret_word(message.from_user.id)
        data['cong'] = db.get_cong(message.from_user.id)
        data['photo'] = message.photo[0].file_id
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    x = db.get_count(message.from_user.id)
    await message.reply(f'Теперь введи текст {x} вопроса на который нужно ответить\n\n(например: ты помнишь город в '
                        f'котором мы познакомились?)')


# обрабатываем машину состояний, сохраняем текст вопроса в словарь
@dp.message_handler(state=FSMAdmin.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    await message.reply(f'Теперь введи ответ 1')


# обрабатываем машину состояний, сохраняем 1-ый вариант ответа в словарь
@dp.message_handler(state=FSMAdmin.answer1)
async def load_answer1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer1'] = message.text
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    await message.reply('Теперь введи ответ 2')


# обрабатываем машину состояний, сохраняем 2-ой вариант ответа в словарь
@dp.message_handler(state=FSMAdmin.answer2)
async def load_answer2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer2'] = message.text
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    await message.reply('Теперь введи ответ 3')


# обрабатываем машину состояний, сохраняем 3-ий вариант ответа в словарь
@dp.message_handler(state=FSMAdmin.answer3)
async def load_answer3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer3'] = message.text
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    await message.reply('Теперь введи ответ 4')


# обрабатываем машину состояний, сохраняем 4-ый вариант ответа в словарь
@dp.message_handler(state=FSMAdmin.answer4)
async def load_answer4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer4'] = message.text
    # переводим машину состояний в ожидание следующего ответа
    await FSMAdmin.next()
    await message.reply('Теперь введи номер правильного ответа\n\n✅ напиши цифру правильного ответа от 1 до 4, '
                        'без кавычек, точек и запятых')


# обрабатываем машину состояний, сохраняем правильный вариант ответа в словарь
@dp.message_handler(state=FSMAdmin.correct_answer)
async def load_correct_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['correct_answer'] = message.text
    # записываем вопрос в базу данных
    await db.sql_add_command(state)
    y = db.get_count(message.from_user.id)
    x = db.get_count(message.from_user.id) + 1
    db.set_count(message.from_user.id, x)
    # проверяем чтобы пользователь создал не больше 5 вопросов викторины
    if db.get_count(message.from_user.id) < 6:
        await message.reply(f'Отлично, ты создал {y}/5 вопросов.\n\n➡ Создай следующий вопрос, нажимай /create')
    else:
        # если пользователь создал 5 вопросов, присылаем клавиатуру с оплатой
        await message.reply('Все 5 вопросов готовы, после оплаты ты '
                            'сможешь поделиться валентинокой', reply_markup=nav.mainPayment)
    # выходим из машины состояний и очищаем словарь
    await state.finish()


# выход из машины состояний
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# обрабатываем команду бота старт
@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    db.set_countsearch(message.from_user.id, 1)
    db.set_count(message.from_user.id, 1)
    db.set_status(message.from_user.id, 'no')
    # проверяем есть ли пользователь в базе
    if not db.user_exists(message.from_user.id):
        # если пользователя нет, записываем его в базу данных
        db.add_user(message.from_user.id)
    await message.answer_sticker(r'CAACAgEAAxkBAAEHahxjz_8WaZJspdpgqCSdh4aKzoq0BwACyQcAAuN4BAABhEkOibFTmlstBA')
    await bot.send_message(message.from_user.id, f'Мы подарили уже: {db.get_people_count(1)} сердец\nЧто ты хочешь '
                                                 f'сделать?', reply_markup=nav.mainMenu)


# обрабатываем оплату
@dp.callback_query_handler(text='btnPayment')
async def payment(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    comment = str(call.from_user.id) + '_' + str(random.randint(1000, 9999))
    bill = p2p.bill(amount=100, lifetime=15, comment=comment)

    db.add_check(call.from_user.id, bill.bill_id)
    await bot.send_message(call.from_user.id, f'Вам нужно отправить {100} руб. на наш счет QIWI\nСсылку: {bill.pay_url}'
                                              f'\n указав комментарий к оплате {comment}',
                           reply_markup=nav.buy_meny(url=bill.pay_url, bill=bill.bill_id))


# обрабатываем оплату и чек
@dp.callback_query_handler(text_contains='check_')
async def check(call: types.CallbackQuery):
    bill = str(call.data[6:])
    info = db.get_check(bill)
    if info:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            db.set_status(call.from_user.id, 'no')
            x = db.get_secret_word(call.from_user.id)
            db.set_pay('yes', x)
            await bot.send_message(call.from_user.id, f'Оплата прошла успешно! Твоя валентинка создана, отправь '
                                                      f'получателю ссылку на этого бота и секретное слово: "{x}", чтобы '
                                                      f'он смог открыть валентинку.\n\nМожешь создать еще одну '
                                                      f'валентинку, перезапусти бота /start')
            await bot.send_photo(call.from_user.id,
                                 r'AgACAgIAAxkBAAO3Y9UDbt4xvfq9i4l1vYu6H_riRUMAAtTBMRvh7alKmUASnoVkoScBAAMCAANzAAMtBA',
                                 f'Тебе прислали цифровую валентинку, чтобы открыть:\n➡перейди '
                                 f'https://t.me/LFLove_bot\n➡ '
                                 f'твоё секретное слово: {x}')
            db.delete_check(bill)
        else:
            await bot.send_message(call.from_user.id, 'Вы не оплатили счет',
                                   reply_markup=nav.buy_meny(False, bill=bill))
    else:
        await bot.send_message(call.from_user.id, 'Счет не найден')


# обрабатываем успешную оплату
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.message):
    if message.successful_payment.invoice_payload == 'love':
        db.set_status(message.from_user.id, 'no')
        x = db.get_secret_word(message.from_user.id)
        db.set_pay('yes', x)
        y = db.get_people_count(1) + 1
        db.set_people_count(y)
        await bot.send_message(message.from_user.id, f'Оплата прошла успешно! Твоя валентинка создана, отправь '
                                                     f'получателю ссылку на этого бота и секретное слово: {x}, чтобы '
                                                     f'он смог открыть валентинку.\n\nМожешь создать еще одну '
                                                     f'валентинку, перезапусти бота /start')


# обрабатываем открытие валентинки
@dp.callback_query_handler(text='btnOpenHeart')
async def sql_data(call: types.Message):
    db.set_status(call.from_user.id, 'open')
    await bot.send_message(call.from_user.id, 'Напиши секретное слово')


# обрабатываем текст с секретным словом, для открытия валентинки
@dp.callback_query_handler(text='btnCreateHeart123')
async def create_heart(call: types.CallbackQuery):
    db.set_status(call.from_user.id, 'secretword')
    await bot.send_message(call.from_user.id, 'Напиши секретное слово, по которому твое сердце смогут найти.'
                                              ' Не пиши распространенные слова и слова длиннее 10 символов.'
                                              ' (пример слова: LOVE123XYZ)')


# обрабатываем начало диалога с пользователем и секретное слово
@dp.message_handler()
async def echo_send(message: types.Message):
    if message.chat.type == 'private':
        if db.get_status(message.from_user.id) == 'secretword':
            # проверяем чтобы секретное слово было не больше 10 символов
            if len(message.text) > 10:
                await bot.send_message(message.from_user.id, "Секретное слово не должно превышать 10 символов")
            if db.secret_word_exists(message.text):
                await bot.send_message(message.from_user.id, "Упс, что-то пошло не так, попробуйте другое слово 🤔")
            else:
                # записываем секретное слово в базу данных
                db.set_secret_word(message.from_user.id, message.text)
                db.set_secret_word_pay(message.text)
                db.set_status(message.from_user.id, 'setcong')
                await bot.send_message(message.from_user.id, 'Отлично, теперь пришли поздравление, которое увидит '
                                                             'получатель после ответа на вопросы')
        # записываем поздравление пользователя в базу данных
        elif db.get_status(message.from_user.id) == 'setcong':
            db.set_cong(message.from_user.id, message.text)
            db.set_status(message.from_user.id, 'create')
            await bot.send_message(message.from_user.id, 'Можешь вернуться назад, нажать "открыть сердце" и отправить '
                                                         'тестовое слово "LOVE123" чтобы посмотреть пример того, '
                                                         'что может получиться\n\nТеперь, давай создадим '
                                                         'твое сердце, которым ты сможешь '
                                                         'поделиться с любимым человеком!\n\n Если запутаешься, можешь '
                                                         'перезапустить бота /start\n\nВсего создание сердца '
                                                         'состоит из нескольких простых этапов:\n\n1. Выбери '
                                                         'кодовое слово, по которому твое сердце смогут найти и '
                                                         'напиши поздравление, которое получатель прочитает в '
                                                         'конце\n2. Добавь пять вопросов на которые следует ответить'
                                                         '\n   2.1 Добавь картинку\n   2.2 По очереди добавь 4-ре '
                                                         'вырианта ответа\n   2.3 Напиши правильный ответ\n3. '
                                                         'Cохрани и отправь получателю\n\nСледуй подсказкам бота и '
                                                         'у тебя все получится\n\n ➡ Нажимай /create чтобы начать')
        # обрабатываем открытие валентинки по секретному слову
        elif db.get_status(message.from_user.id) == 'open':
            # проверяем чтобы валентинка была оплачена
            if not db.secret_word_exists_pay(message.text, 'yes'):
                await bot.send_message(message.from_user.id, 'Вы ввели неверное слово, попробуйте еще раз 🙃')
            else:
                db.set_secret_word_search(message.from_user.id, message.text)
                db.set_status(message.from_user.id, 'answer')
                await db.get_question(message.from_user.id, message)
                await bot.send_message(message.from_user.id, 'Выбирай свой ответ', reply_markup=nav.mainAnswer)
        # обрабатываем правильный ответ на вопрос
        elif db.get_status(message.from_user.id) == 'answer':
            if message.text == '1' or message.text == '2' or message.text == '3' or message.text == '4':
                if message.text == db.get_correctanswer(message.from_user.id):
                    await bot.send_message(message.from_user.id, 'Правильно!')
                    x = db.get_countsearch(message.from_user.id) + 1
                    db.set_countsearch(message.from_user.id, x)
                    await db.get_question(message.from_user.id, message)
                    if db.get_countsearch(message.from_user.id) > 5:
                        db.set_countsearch(message.from_user.id, 1)
                        db.set_status(message.from_user.id, 'no')
                        x = db.get_cong_f(message.from_user.id)
                        await bot.send_message(message.from_user.id, x, reply_markup=types.ReplyKeyboardRemove())
                # обрабатываем неправильный ответ на вопрос
                else:
                    y = random.randint(1, 3)
                    if y == 1:
                        await bot.send_message(message.from_user.id, 'Не-а 😛, попробуй еще раз')
                    if y == 2:
                        await bot.send_message(message.from_user.id, 'Нууу нет 🙄, попробуй еще раз')
                    if y == 3:
                        await bot.send_message(message.from_user.id, 'Почти правильно 🤭, попробуй еще раз')


executor.start_polling(dp, skip_updates=True)

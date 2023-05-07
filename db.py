import sqlite3

from create_bot import bot


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # сохраняем машину состояний
    async def sql_add_command(self, state):
        async with state.proxy() as data:
            self.cursor.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
            self.connection.commit()

    # узнаем вопрос
    async def get_question(self, user_id, message):
        for ret in self.cursor.execute('SELECT data.photo, data.text, data.answer1, data.answer2, data.answer3, '
                                       'data.answer4 FROM data, users WHERE users.user_id = ? AND data.secretword = '
                                       'users.secretword_search AND data.id = users.count_search', (user_id,
                                                                                                    )).fetchall():
            await bot.send_photo(message.from_user.id, ret[0],
                                 f'\n{ret[1]}\n\n1) {ret[2]}\n2) {ret[3]}\n3) {ret[4]}\n4) {ret[5]}')

    # узнаем статус пользователя
    def get_cong_f(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT data.cong FROM data, users WHERE users.user_id = ? AND '
                                         'data.secretword = users.secretword_search AND data.id = '
                                         'users.count_search', (user_id,)).fetchall()
            for row in result:
                text = str(row[0])
                return text

    # добавление нового пользователя
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))

    # проверяем существует ли пользователь в базе
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
            return bool(len(result))

    # узнаем статус пользователя
    def get_status(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT status FROM users WHERE user_id = ?', (user_id,)).fetchall()
            for row in result:
                status = str(row[0])
                return status

    # добавляем статус пользователя
    def set_status(self, user_id, status):
        with self.connection:
            return self.cursor.execute('UPDATE users SET status = ? WHERE user_id = ?', (status, user_id,))

    # узнаем секретное слово
    def get_secret_word(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT secretword FROM users WHERE user_id = ?', (user_id,)).fetchall()
            for row in result:
                secretword = str(row[0])
                return secretword

    # добавляем секретное слово пользователя
    def set_secret_word_search(self, user_id, word):
        with self.connection:
            return self.cursor.execute('UPDATE users SET secretword_search = ? WHERE user_id = ?', (word, user_id,))

    # добавляем секретное слово пользователя
    def set_secret_word(self, user_id, word):
        with self.connection:
            return self.cursor.execute('UPDATE users SET secretword = ? WHERE user_id = ?', (word, user_id,))

    # добавляем секретное слово пользователя (для оплаты)
    def set_secret_word_pay(self, word):
        with self.connection:
            return self.cursor.execute('INSERT INTO secretword (word) VALUES (?)', (word,))

    # узнаем счетчик вопроса пользователя
    def get_count(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT count FROM users WHERE user_id = ?', (user_id,)).fetchall()
            for row in result:
                count = int(row[0])
                return count

    # добавляем счетчик вопроса
    def set_count(self, user_id, status):
        with self.connection:
            return self.cursor.execute('UPDATE users SET count = ? WHERE user_id = ?', (status, user_id,))

    # добавляем оплату секретного слова
    def set_pay(self, status, word):
        with self.connection:
            return self.cursor.execute('UPDATE secretword SET status = ? WHERE word = ?', (status, word,))

    # проверяем существуетли секретное слово в базе
    def secret_word_exists(self, word):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM secretword WHERE word = ?', (word,)).fetchall()
            return bool(len(result))

    # проверяем существуетли секретное слово в базе (оплаченное)
    def secret_word_exists_pay(self, word, status):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM secretword WHERE word = ? AND status = ?',
                                         (word, status,)).fetchall()
            return bool(len(result))

    # узнаем правильный ответ
    def get_correctanswer(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT data.correctanswer FROM data, users WHERE users.user_id = ? AND '
                                         'data.secretword = users.secretword_search AND data.id = '
                                         'users.count_search', (user_id,)).fetchall()
            for row in result:
                correctanswer = str(row[0])
                return correctanswer

    # добавляем счетчик вопроса пользователя (при ответе)
    def set_countsearch(self, user_id, word):
        with self.connection:
            return self.cursor.execute('UPDATE users SET count_search = ? WHERE user_id = ?', (word, user_id,))

    # узнаем счетчик вопроса пользователя (при ответе)
    def get_countsearch(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT count_search FROM users WHERE user_id = ?', (user_id,)).fetchall()
            for row in result:
                count = int(row[0])
                return count

    # добавляем поздравление
    def set_cong(self, user_id, word):
        with self.connection:
            return self.cursor.execute('UPDATE users SET cong = ? WHERE user_id = ?', (word, user_id,))

    # узнаем поздравление
    def get_cong(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT cong FROM users WHERE user_id = ?', (user_id,)).fetchall()
            for row in result:
                cong = str(row[0])
                return cong

    # добавление счета
    def add_check(self, user_id, bill_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO checkk (user_id, bill_id) VALUES (?, ?)', (user_id, bill_id,))

    # узнаем счет
    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM checkk WHERE bill_id = ?', (bill_id,)).fetchall()
            if not bool(len(result)):
                return False
            return int(result[0][0])

    # удаление записи после оплаты
    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM checkk WHERE bill_id = ? ', (bill_id,))

    # добавляем кол-во пользователей
    def set_people_count(self, count):
        with self.connection:
            return self.cursor.execute('INSERT INTO metrick (count) VALUES (?)', (count,))

    # узнаем кол-во пользователей
    def get_people_count(self, met):
        with self.connection:
            result = self.cursor.execute('SELECT count FROM metrick WHERE id = ?', (met,)).fetchall()
            for row in result:
                count = int(row[0])
                return count

<img src="https://img.shields.io/badge/Engine-Python%203.11%20-blue" alt="Python Version"> <img src="https://img.shields.io/badge/Engine-Aiogram%202.24-blue" alt="Aiogram Version"> <img src="https://img.shields.io/badge/Engine-pyQiwiP2P%202.0.6-orange" alt="pyQiwiP2P Version"> <img src="https://img.shields.io/badge/License-MIT%20-brightgreen" alt="License">

## About

Телеграм-бот для поздравлений. Создайте викторину из 5 вопросов (изображение, текст вопроса, четыре варианта ответа). После оплаты, отправьте секретное слово любому пользователю. После прохождения викторины, пользователь получит ваше поздравление.

## Documentation

Для работы бота, создайте в корневой папке файл create_bot.py
```
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '' # вставьте ваш токен телеграм
QIWI_TOKEN = '' # вставьте ваш токен Qiwi

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
```

## Developers

- [Sergei Korobov](https://github.com/sergeicastle)

## License

Project valentines_bot is distributed under the MIT license.

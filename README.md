<h1 align="center">🤖 Telegram Бот для Форумов</h1>
В новом обновлении тг была добавлена нативная реализация подобного чата для групп/каналов/ботов.

В новом обновлении тг была добавлена нативная реализация подобного чата для групп/каналов/ботов.

В новом обновлении тг была добавлена нативная реализация подобного чата для групп/каналов/ботов.


<p align="center">Удобное решение для общения с клиентами через топики в Telegram супергруппах</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white">
  <img alt="Aiogram" src="https://img.shields.io/badge/Aiogram-3.x-blue.svg?style=flat">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-3-green.svg?style=flat&logo=sqlite&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/Лицензия-MIT-yellow.svg?style=flat">
</p>

---

## 📝 Описание

Этот бот создан для организации общения с клиентами через форумы Telegram. Основная идея - каждому пользователю создается отдельный топик (тред) в супергруппе администраторов, что позволяет удобно отслеживать и отвечать на запросы пользователей.

### ✨ Основные возможности:
- Автоматическое создание тем в форуме для каждого пользователя
- Удобный интерфейс для задания вопросов 
- Хранение соответствия пользователей и тем в базе данных
- Простая обратная связь для администраторов

## 📷 Демонстрация работы:

<table align="center">
  <tr>
    <td align="center"><b>Пользователь</b></td>
    <td align="center"><b>Администратор</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/ForeverWinterNight/Telegram-threads-bot/blob/main/img/img1.png" alt="Интерфейс пользователя" width="100%"></td>
    <td><img src="https://github.com/ForeverWinterNight/Telegram-threads-bot/blob/main/img/img2.png" alt="Интерфейс администратора" width="100%"></td>
  </tr>
</table>

## 🚀 Установка и запуск

### Требования
- Python 3.11+
- Aiogram 3.x
- Aiosqlite

### Установка (Linux)

```bash
# Обновление системы
sudo apt update
sudo apt upgrade

# Установка Python
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python3.11-venv python3.11-dev

# Настройка окружения
python3.11 -m ensurepip --upgrade
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### Установка (Windows)

```bash
# Создание виртуального окружения
python -m venv venv
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

## ⚙️ Настройка

1. Получите токен бота у [@BotFather](https://t.me/BotFather)
2. Создайте супергруппу с включенными форумами
3. Добавьте бота в супергруппу и назначьте его администратором
4. Узнайте ID супергруппы (можно использовать @userinfobot)
5. Обновите файл `main.py`:
   ```python
   SUPPORT_CHAT_ID = -100... # ID вашей супергруппы с форумами
   bot = Bot(token='ваш_токен') # Токен от BotFather
   ```

## 🏁 Запуск бота

```bash
# Активация виртуального окружения (если еще не активировано)
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows

# Запуск бота
python main.py
```

## 🤝 Вклад в проект

Вклады приветствуются! Если у вас есть идеи или предложения по улучшению бота:
1. Форкните репозиторий
2. Создайте ветку с вашими изменениями
3. Отправьте Pull Request

## 📄 Лицензия

Распространяется под лицензией MIT. Подробности в файле LICENSE.

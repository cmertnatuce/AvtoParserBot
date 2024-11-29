# -*- coding: cp1251 -*- 

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup
import asyncio

# Хранилище данных
data_store = {
    "site": None,
    "parsing": False,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

# Функция для старта
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я бот для парсинга сайтов. Используйте команды для настройки и парсинга.\n"
        "Для списка всех команд введите /help."
    )

# Команда помощи
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "/start - Приветствие\n"
        "/info - Инструкция к боту\n"
        "/help - Список доступных команд\n"
        "/set_site - Установка сайта для парсинга\n"
        "/start_parse - Запуск процесса парсинга\n"
        "/pause_parse - Остановка процесса парсинга\n"
        "/get_filters - Просмотр текущих фильтров (пока не реализовано)\n"
        "/export_data - Экспорт собранных данных (пока не реализовано)"
    )

# Команда информации
async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Инструкция:\n"
        "1. Установите сайт для парсинга с помощью команды /set_site.\n"
        "2. При желании установите фильтр командой /set_filter.\n"
        "3. Запустите парсинг командой /start_parse.\n"
        "4. Остановите парсинг в любой момент командой /pause_parse.\n"
    )

# Установка URL сайта
async def set_site(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Выбрать cars.av.by", callback_data="site_cars_av")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выберите сайт из списка или введите URL вручную после команды /set_site:",
        reply_markup=reply_markup,
    )

# Обработчик выбора сайта через кнопку
async def site_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "site_cars_av":
        data_store["site"] = "https://cars.av.by/filter?sort=4"
        await query.edit_message_text("Сайт установлен: https://cars.av.by/filter?sort=4")

# Парсинг сайта
async def start_parse(update: Update, context: CallbackContext):
    if not data_store["site"]:
        await update.message.reply_text("Сначала укажите сайт командой /set_site.")
        return

    if data_store["parsing"]:
        await update.message.reply_text("Парсинг уже запущен!")
        return

    data_store["parsing"] = True
    await update.message.reply_text(f"Запуск парсинга сайта: {data_store['site']}")

    try:
        while data_store["parsing"]:
            # Выполняем запрос к сайту
            response = requests.get(data_store["site"], headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # Извлечение данных
            car_elements = soup.find_all("div", class_="listing-item")
            if not car_elements:
                await update.message.reply_text("Не удалось найти данные на сайте. Проверьте URL.")
                data_store["parsing"] = False
                return

            # Сбор информации
            results = []
            for car in car_elements:
                title_element = car.find("h3", class_="listing-item__title")
                title = title_element.get_text(strip=True) if title_element else "Марка и модель не указаны"

                params_element = car.find("div", class_="listing-item__params")
                if params_element:
                    params_text = params_element.get_text(strip=True).split(',')
                    car_details = ', '.join(param.strip() for param in params_text)
                else:
                    car_details = "Данные о машине не указаны"

                price_element = car.find("div", class_="listing-item__priceusd")
                price = price_element.get_text(strip=True) if price_element else "Цена не указана"

                results.append(f"Марка и модель: {title}\nХарактеристики: {car_details}\nЦена: {price}")

            # Отправляем результаты в чат
            if results:
                for result in results:
                    await update.message.reply_text(result)
                    await asyncio.sleep(1)  # Пауза между сообщениями

            # Пауза перед следующим циклом
            await asyncio.sleep(10)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")
    finally:
        data_store["parsing"] = False
        await update.message.reply_text("Парсинг завершён.")

# Приостановка парсинга
async def pause_parse(update: Update, context: CallbackContext):
    if not data_store["parsing"]:
        await update.message.reply_text("Парсинг не запущен.")
        return

    data_store["parsing"] = False
    await update.message.reply_text("Парсинг приостановлен.")

# Основная функция, создающая приложение
def main():
    application = Application.builder().token("7566953382:AAEPW9VJgRrWnje3QXEvBdOA9KelDYTjZmM").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("set_site", set_site))
    application.add_handler(CommandHandler("start_parse", start_parse))
    application.add_handler(CommandHandler("pause_parse", pause_parse))
    application.add_handler(CallbackQueryHandler(site_selection))  # Для кнопок

    print("Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()

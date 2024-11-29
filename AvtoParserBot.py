# -*- coding: cp1251 -*- 

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup
import asyncio

# ��������� ������
data_store = {
    "site": None,
    "parsing": False,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

# ������� ��� ������
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������! � ��� ��� �������� ������. ����������� ������� ��� ��������� � ��������.\n"
        "��� ������ ���� ������ ������� /help."
    )

# ������� ������
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "/start - �����������\n"
        "/info - ���������� � ����\n"
        "/help - ������ ��������� ������\n"
        "/set_site - ��������� ����� ��� ��������\n"
        "/start_parse - ������ �������� ��������\n"
        "/pause_parse - ��������� �������� ��������\n"
        "/get_filters - �������� ������� �������� (���� �� �����������)\n"
        "/export_data - ������� ��������� ������ (���� �� �����������)"
    )

# ������� ����������
async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "����������:\n"
        "1. ���������� ���� ��� �������� � ������� ������� /set_site.\n"
        "2. ��� ������� ���������� ������ �������� /set_filter.\n"
        "3. ��������� ������� �������� /start_parse.\n"
        "4. ���������� ������� � ����� ������ �������� /pause_parse.\n"
    )

# ��������� URL �����
async def set_site(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("������� cars.av.by", callback_data="site_cars_av")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "�������� ���� �� ������ ��� ������� URL ������� ����� ������� /set_site:",
        reply_markup=reply_markup,
    )

# ���������� ������ ����� ����� ������
async def site_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "site_cars_av":
        data_store["site"] = "https://cars.av.by/filter?sort=4"
        await query.edit_message_text("���� ����������: https://cars.av.by/filter?sort=4")

# ������� �����
async def start_parse(update: Update, context: CallbackContext):
    if not data_store["site"]:
        await update.message.reply_text("������� ������� ���� �������� /set_site.")
        return

    if data_store["parsing"]:
        await update.message.reply_text("������� ��� �������!")
        return

    data_store["parsing"] = True
    await update.message.reply_text(f"������ �������� �����: {data_store['site']}")

    try:
        while data_store["parsing"]:
            # ��������� ������ � �����
            response = requests.get(data_store["site"], headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # ���������� ������
            car_elements = soup.find_all("div", class_="listing-item")
            if not car_elements:
                await update.message.reply_text("�� ������� ����� ������ �� �����. ��������� URL.")
                data_store["parsing"] = False
                return

            # ���� ����������
            results = []
            for car in car_elements:
                title_element = car.find("h3", class_="listing-item__title")
                title = title_element.get_text(strip=True) if title_element else "����� � ������ �� �������"

                params_element = car.find("div", class_="listing-item__params")
                if params_element:
                    params_text = params_element.get_text(strip=True).split(',')
                    car_details = ', '.join(param.strip() for param in params_text)
                else:
                    car_details = "������ � ������ �� �������"

                price_element = car.find("div", class_="listing-item__priceusd")
                price = price_element.get_text(strip=True) if price_element else "���� �� �������"

                results.append(f"����� � ������: {title}\n��������������: {car_details}\n����: {price}")

            # ���������� ���������� � ���
            if results:
                for result in results:
                    await update.message.reply_text(result)
                    await asyncio.sleep(1)  # ����� ����� �����������

            # ����� ����� ��������� ������
            await asyncio.sleep(10)
    except Exception as e:
        await update.message.reply_text(f"��������� ������: {e}")
    finally:
        data_store["parsing"] = False
        await update.message.reply_text("������� ��������.")

# ������������ ��������
async def pause_parse(update: Update, context: CallbackContext):
    if not data_store["parsing"]:
        await update.message.reply_text("������� �� �������.")
        return

    data_store["parsing"] = False
    await update.message.reply_text("������� �������������.")

# �������� �������, ��������� ����������
def main():
    application = Application.builder().token("7566953382:AAEPW9VJgRrWnje3QXEvBdOA9KelDYTjZmM").build()

    # ������������ ����������� ������
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("set_site", set_site))
    application.add_handler(CommandHandler("start_parse", start_parse))
    application.add_handler(CommandHandler("pause_parse", pause_parse))
    application.add_handler(CallbackQueryHandler(site_selection))  # ��� ������

    print("��� �������!")
    application.run_polling()

if __name__ == '__main__':
    main()

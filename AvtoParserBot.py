# -*- coding: cp1251 -*-

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ������� ��� ������
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������! � ��� ��� �������� ������. ����������� �������, ����� ��������� �������, ������ ������� � ������ ������."
    )

# ������� ��� ������
async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "/start - ����������� � ������� ���������� � �����������.\n"
        "/help - ������ ��������� ������.\n"
        "/set_filter - ��������� �������� ��� ��������.\n"
        "/start_parse - ������ ��������.\n"
        "/pause_parse - ��������� �������� �������� ��������.\n"
        "/get_filters - �������� ������� ������������� ��������.\n"
        "/set_site - ��������� URL �����.\n"
        "/export_data - ������� ��������� ������ � ����.\n"
        "/info - �������� ���������� �������������."
    )

# ������� ��� ������ ���������� � ��������
async def set_filter(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /set_filter ��������� ��������� ������� ��� �������� �����. ��������, �� ������ ������� �������� �����, ��������� � ������ ��������� ��� ���������� ������."
    )

# ������� ��� ������ ���������� � ������� ��������
async def start_parse(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /start_parse ��������� ������� �������� ����� � �������������� ���������. ����� ������� ��� ����� �������� ������ � ���������� �����."
    )

# ������� ��� ������ ���������� �� ��������� ��������
async def pause_parse(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /pause_parse ��������� ������������� ������� ������� ��������, ���� �� ��� �������."
    )

# ������� ��� ������ ���������� � ������� ��������
async def get_filters(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /get_filters ���������� ������� ��������� �������� ��� ��������. �� ������ �������, ����� ������� ����������� �� ������ ������."
    )

# ������� ��� ������ ���������� �� ��������� �����
async def set_site(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /set_site ��������� ���������� URL �����, � �������� ����� ����������� �������. ������� ����� ����� ����� �������."
    )

# ������� ��� ������ ���������� �� �������� ������
async def export_data(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "������� /export_data ��������� �������������� ��������� ������ � ���� (��������, � ������ CSV ��� TXT)."
    )

# ������� ��� ����������� ����������
async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "���������� �� �������������:\n"
        "1. ����������� ������� /set_site ��� ��������� URL �����, ������� ����� ���������.\n"
        "2. ��������� ������� � ������� ������� /set_filter.\n"
        "3. ��������� ������� �������� /start_parse.\n"
        "4. ��� ������������� ������������� ������� �������� /pause_parse.\n"
        "5. �������� ������� ������� � ������� ������� /get_filters.\n"
        "6. ������������� ��������� ������ � ������� ������� /export_data.\n"
        "��� �������������� ������ ����������� ������� /help."
    )

# �������� �������, ��������� ����������
def main():
    application = Application.builder().token("7566953382:AAEPW9VJgRrWnje3QXEvBdOA9KelDYTjZmM   ").build()

    # ������������ ����������� ������
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("set_filter", set_filter))
    application.add_handler(CommandHandler("start_parse", start_parse))
    application.add_handler(CommandHandler("pause_parse", pause_parse))
    application.add_handler(CommandHandler("get_filters", get_filters))
    application.add_handler(CommandHandler("set_site", set_site))
    application.add_handler(CommandHandler("export_data", export_data))
    application.add_handler(CommandHandler("info", info))
    print("��� �������!")

    # ������ ����
    application.run_polling()

if __name__ == '__main__':
    main()

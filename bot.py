import asyncio
import logging
import time

import requests
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5939145853:AAE_D-XEl2ELKjm7sd-vpCBPe9CHvLJHAgE")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Оплатить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer("Добро пожаловать в платежный сервис нашей компании!"
                         " Чтобы воспользоваться услугой, нажмите Оплатить",
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Оплатить")
async def pay(message: types.Message):
    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization": "Token "
                         "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
                         "eyJpZCI6Mzk0MCwiZXhwIjo4ODA3MzI1ODkwMH0."
                         "ROhghbCgljGD_8r1dWC9ScUnmIsEEYwRrLCSG012zLU"
    }
    data = {
        "amount": 49,
        "shop_id": "hWzIOXLWZMTXoAiz"
    }

    response_json = requests.post(url=url, headers=headers, data=data).json()
    print(response_json)
    await bot.send_message(message.chat.id, "Оплатите данный счет в криптовалюте: " +
                           response_json["pay_url"])
    while True:
        time.sleep(5)
        a = requests.get(url=f"https://api.cryptocloud.plus/v1/invoice/info?uuid=INV-{response_json['invoice_id']}",
                         headers=headers).json()
        if a["status_invoice"] == "paid":
            await bot.send_message("Вы успешно оплатили услугу")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from config import CONFIG
from telethon import TelegramClient
import asyncio


api_id = CONFIG["api_id"]
api_hash = CONFIG["api_hash"]
bot = "@Arman_own_bot"


async def test_start(client: TelegramClient):
    async with client.conversation(bot, timeout=10) as conv:
        await conv.send_message("/start")
        resp = await conv.get_response()

        text = 'Привет, я личный бот Армана.' \
               '\nЕсли не знаешь что делать напиши /help.'

        assert text == resp.raw_text


async def test_help(client: TelegramClient):
    async with client.conversation(bot, timeout=10) as conv:
        await conv.send_message("/help")
        resp = await conv.get_response()

        text = 'Это бот который может выдавать последние новости про Реал Мадрид' \
               ' и про МФТИ.\nНапиши "Real Madrid" и получишь новость' \
               ' про Реал Мадрид.\nНапиши "MIPT" и получишь новость про МФТИ.\n' \
               'А если написать сообщение он повторно отправит его' \
               ' и предложить две кнопки: "Real Madrid" и "Mipt".'

        assert text == resp.raw_text


async def test_rm(client: TelegramClient):
    try:
        async with client.conversation(bot, timeout=30) as conv:
            await conv.send_message("Real Madrid")
            resp = await conv.get_response()
    except asyncio.exceptions.TimeoutError:
        raise Exception("request is being processed for a long time")


async def test_mipt(client: TelegramClient):
    try:
        async with client.conversation(bot, timeout=30) as conv:
            await conv.send_message("MIPT")
            resp = await conv.get_response()
    except asyncio.exceptions.TimeoutError:
        raise Exception("request is being processed for a long time")


def main():
    with TelegramClient('session', api_id, api_hash) as client:
        client.loop.run_until_complete(test_start(client))
        client.loop.run_until_complete(test_help(client))
        client.loop.run_until_complete(test_rm(client))
        client.loop.run_until_complete(test_mipt(client))


if __name__ == "__main__":
    main()

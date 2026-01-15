import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

# Загружаем данные
with open("builds.json", "r", encoding="utf-8") as f:
    BUILDS = json.load(f)

TELEGRAM_TOKEN = os.getenv("8467489965:AAHMDzpinSgNl0t0m1sa2PeW0ji72KtqvHk")
bot = Bot(token="8467489965:AAHMDzpinSgNl0t0m1sa2PeW0ji72KtqvHk")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎮 Привет! Я — бот-помощник по билдам в Genshin Impact.\n\n"
        "Напиши: /билд имя_персонажа\n"
        "Пример: /билд zhongli, /билд ayaka\n\n"
        "Список доступных: zhongli, ayaka"
    )

@dp.message(Command("билд"))
async def send_build(message: types.Message):
    args = message.text.replace("/билд", "").strip().lower()
    if not args:
        await message.answer("Укажите имя персонажа на английском (например: /билд zhongli)")
        return

    char = BUILDS.get(args)
    if not char:
        await message.answer("Персонаж не найден. Доступные: zhongli, ayaka")
        return

    # Формируем сообщение
    text = f"🌟 <b>{char['name']}</b>\n"
    text += f"Элемент: {char['element']} | Оружие: {char['weapon']} | {'⭐' * char['rarity']}\n\n"
    text += f"<b>Роль:</b> {char['role']}\n\n"
    text += "<b>Сеты артефактов:</b>\n• " + "\n• ".join(char["artifact_sets"]) + "\n\n"
    text += "<b>Статы:</b>\n"
    for slot, stat in char["stats"].items():
        text += f"  • {slot.capitalize()}: {stat}\n"
    text += "\n<b>Оружие:</b>\n• " + "\n• ".join(char["weapons"]) + "\n\n"
    text += f"<b>Совет по команде:</b> {char['team_tips']}"

    await message.answer(text, parse_mode="HTML")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))

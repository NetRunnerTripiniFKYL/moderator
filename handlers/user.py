from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я — бот-модератор чата.\n"
        "Я слежу за порядком, фильтрую токсичность, угрозы и спам.\n"
        "Если кто-то нарушает правила — пиши /report или просто веди себя хорошо 🙂"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🤖 Доступные команды:\n"
        "/start — приветствие и инфо о боте\n"
        "/help — список команд\n"
        "/rules — правила поведения\n"
        "/report — пожаловаться на сообщение\n"
        "/status — статус бота"
    )


@router.message(Command("rules"))
async def cmd_rules(message: Message):
    await message.answer(
        "📜 Правила чата:\n"
        "- Без оскорблений и агрессии\n"
        "- Без политики, экстремизма и токсичных тем\n"
        "- Спам и флуд запрещены\n"
        "- Соблюдайте уважение к участникам"
    )


@router.message(Command("report"))
async def cmd_report(message: Message):
    await message.answer(
        "🚨 Пожалоба зарегистрирована.\n"
        "Если сообщение действительно нарушает правила — модератор примет меры."
    )
    # TODO: можно сохранять жалобы в лог или пересылать админу


@router.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer("✅ Бот активен. Модерация включена.")
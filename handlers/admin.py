import os
import json
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter

router = Router()


LOG_PATH = "data/logs.json"

# Простой фильтр по правам (в бою можно усложнить)
async def is_admin(message: Message) -> bool:
    member = await message.chat.get_member(message.from_user.id)
    return member.status in ("administrator", "creator")


@router.message(Command("log"))
async def cmd_log(message: Message):
    if not await is_admin(message):
        return await message.answer("❌ Только для админов.")
    
    if not os.path.exists(LOG_PATH):
        return await message.answer("Логов пока нет.")

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        return await message.answer("⚠️ Логи повреждены.")

    last_logs = logs[-5:] if len(logs) >= 5 else logs

    text = "\n\n".join(
        f"🕒 {log.get('timestamp')}\n"
        f"👤 {log.get('username')} (ID: {log.get('user_id')})\n"
        f"🚨 Действие: {log.get('action')}\n"
        f"📌 Причина: {log.get('reason')}\n"
        f"💬 Сообщение:\n{log.get('message')}"
        for log in last_logs
    )

    await message.answer(f"📝 Последние записи логов:\n\n{text}")


@router.message(Command("logall"))
async def cmd_logall(message: Message):
    if not await is_admin(message):
        return await message.answer("❌ Только для админов.")
    
    if not os.path.exists(LOG_PATH):
        return await message.answer("Логов пока нет.")

    await message.answer_document(FSInputFile(LOG_PATH), caption="📂 Полный лог")

@router.message(Command("cleanlog"))
async def cmd_cleanlog(message: Message):
    if not await is_admin(message):
        return await message.answer("❌ Только для админов.")
    
    if not os.path.exists(LOG_PATH):
        return await message.answer("📂 Лог уже пуст.")

    try:
        os.remove(LOG_PATH)
        await message.answer("🧹 Лог очищен.")
    except Exception as e:
        await message.answer(f"⚠️ Не удалось удалить лог: {e}")
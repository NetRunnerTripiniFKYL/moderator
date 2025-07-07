from aiogram import Router, F
from aiogram.types import Message
from gpt import moderate_message
from services.logger import log_action

router = Router()
@router.message(F.text | F.caption)
async def moderate_incoming_message(message: Message):
    # Не модерируем свои сообщения
    if message.from_user.is_bot:
        return

    # Берём либо text, либо caption
    text = message.text or message.caption
    if not text:
        return  # например, стикер или просто фото без подписи

    result = moderate_message(text)
    punishment = result.get("наказание", "никакое")
    reason = result.get("описание", "никакое")

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    # логируем всё
    log_action(
        user_id=user_id,
        username=username,
        action=punishment,
        reason=reason,
        message=text
    )

    # реагируем
    if punishment == "никакое":
        return

    if punishment == "бан":
        try:
            await message.answer(
                f"⚠️ Бан @{username}\nПричина: {reason}",
                reply_to_message_id=message.message_id
            )
            await message.chat.ban(user_id=user_id)
            await message.delete()
        except Exception:
            await message.answer("❗ Не удалось забанить пользователя.")
import os
import json
from datetime import datetime

LOG_PATH = "data/logs.json"

def log_action(user_id: int, username: str, action: str, reason: str, message: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "username": username,
        "action": action,
        "reason": reason,
        "message": message
    }

    # Убедимся, что директория существует
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # Загружаем старые логи
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
    except Exception:
        logs = []

    # Добавляем запись
    logs.append(log_entry)

    # Сохраняем обратно
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
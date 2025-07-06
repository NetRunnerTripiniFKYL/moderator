import openai
import os
from dotenv import load_dotenv
load_dotenv()
import json
from config import promt

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def moderate_message(user_ansver : str):
    user_ansver_for_search = user_ansver
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "developer", "content": f"{promt}."
            },
            {
                "role": "user", "content": f"{user_ansver}"
            }
          ]
    )

    response = response.model_dump()
    print(response["choices"][0]["message"]["content"])
    return(parse_gpt_response(response["choices"][0]["message"]["content"]))

def parse_gpt_response(response_text: str) -> dict:
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        return {
            "наказание": "никакое",
            "описание": f"Ошибка парсинга: {e}. Ответ: {response_text}"
        }
import g4f
import os
from bot.toloka_bot import TolokaBot

ENV_USERNAME = os.environ.get('ENV_USERNAME') # Значение из переменной среды
ENV_PASSWORD = os.environ.get('ENV_PASSWORD') # Значение из переменной среды
POST_TYPE = ['auto', 'manual'] # Тип подтверждения результата (вручную или автоматически)
GPT_MODELS = {0: g4f.models.gpt_35_long, 1: g4f.models.gpt_4}

if __name__ == '__main__':
    user_model_id = int(input('какую модель ИНС использовать(0 - Recommended):\n' +
                         '\n'.join([f'{i[0]} - {i[1]}' for i in GPT_MODELS.items()]) + '\n'))
    user_count_records = int(input('Сколько записей нужно разметить: '))

    bot = TolokaBot(model=GPT_MODELS[user_model_id], username=ENV_USERNAME,
                    password=ENV_PASSWORD, session_template_uri='./session_template.txt')
    bot.main(user_count_records, post_type=POST_TYPE[0])


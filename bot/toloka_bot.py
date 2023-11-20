import requests
import keyboard
from bot.answer_generator import AnswerGenerator
from bot.authenticator import Authenticator
from bot.toloka_model import TolokaModel
from bot.toloka_output_editor import TolokaEditor
from bot.toloka_parser import TolokaParser


class TolokaBot:
    def __init__(self, model, username, password, session_template_uri, ):
        self.toloka_editor = TolokaEditor()
        self.session = requests.Session()
        self.session_template_uri = session_template_uri
        self.login_payload = {'username': username, 'password': password}
        self.work_url = 'http://tomeo.pythonanywhere.com/'
        self.parser = TolokaParser(self.session, self.work_url)
        self.authenticator = Authenticator(self.session, self.login_payload)
        self.answer_generator = AnswerGenerator(model)

    def load_session_template(self):
        with open(self.session_template_uri, 'r', encoding='utf-8') as f:
            return f.read()

    def submit_post_request(self, post_payload):
        response = self.session.post(self.work_url, data=post_payload)
        return response.ok

    def send_result(self, toloka_mdl: TolokaModel):
        post_payload = {
            'csrfmiddlewaretoken': self.parser.csrf,
            'id': toloka_mdl.post_id,
            'Garbage': toloka_mdl.generated_result['Garbage'],
            'selected_field': toloka_mdl.generated_result['selected_field'],
            'selected_emotion': toloka_mdl.generated_result['selected_emotion']
        }

        if self.submit_post_request(post_payload):
            return f'Запись размечена успешно!'
        else:
            return 'Ошибка отправки POST-запроса.'

    def main(self, count, post_type):
        self.login_payload.update({'csrfmiddlewaretoken': self.parser.csrf})

        if self.authenticator.login():
            print("Successfully logged in.")
        else:
            print("Failed to log in.")
            return
        for record_counter in range(count):
            toloka_mdl = self.parser.get_toloka_model()

            if not toloka_mdl:
                print("Unable to fetch data from the website.")
                return

            for i in range(3):
                generated_text = self.answer_generator.generate_sentence(self.load_session_template(), toloka_mdl.get_prompt())
                toloka_mdl.set_generated_json(generated_text)

                edited_result = self.toloka_editor.check_categories_in_result(toloka_mdl.generated_result)
                toloka_mdl.generated_result = edited_result

                if toloka_mdl.generated_result:
                    break
                print(f'Попыток генерации: {i + 1}')

            if not toloka_mdl.generated_result:
                continue

            print(f'\n=============RECORD №{record_counter + 1}=============\n' + toloka_mdl.get_prompt())
            print('\n=============RESULT=============\n' + str(toloka_mdl.generated_result) + '\n')

            if post_type == 'manual':
                print('Если Вы согласны на отправку результата, нажмите Enter, если хотите пропустить - Esc')
                key = keyboard.read_event(suppress=True).name
                if key == 'enter':
                    print(self.send_result(toloka_mdl))
                elif key == 'esc':
                    print('Запись пропущена.')
            elif post_type == 'auto':
                print(self.send_result(toloka_mdl))

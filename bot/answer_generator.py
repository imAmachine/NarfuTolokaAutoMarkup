from g4f import ChatCompletion

from bot.gtranslator import GTranslator


class AnswerGenerator:
    def __init__(self, model):
        self.model = model
        self.translator = GTranslator()

    def generate_sentence(self, session_template, prompt):
        en_text = self.translator.transl(prompt)
        response = ChatCompletion.create(
            model=self.model,
            messages=[{
                          'role': 'Markup the data; the input data consists of "Comment to the post" or "post" from the Internet on the topic of "assessment of various spheres of life in the city or region.',
                          'content': session_template + en_text}]
        )

        return response

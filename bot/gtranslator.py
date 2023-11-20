from googletrans import Translator


class GTranslator:
    def __init__(self):
        self.translator = Translator()

    def transl(self, input_text):
        translated_text = self.translator.translate(input_text, dest='en')
        return translated_text.text


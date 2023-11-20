import json


def parse_result_json(text):
    try:
        return json.loads(text)
    except Exception as e:
        print(text)
        return None


class TolokaModel:
    def __init__(self, post_id, post_text=None, comment=None):
        self.post_id = post_id
        self.post_text = post_text
        self.comment = comment
        self.generated_result = None

    def get_prompt(self):
        result_str = f'###POST: {self.post_text}\n###COMMENT: {self.comment}'
        return result_str

    def get_post_id(self):
        return self.post_id

    def set_generated_json(self, generated_text):
        json_start_ind = generated_text.find('{')
        json_end_ind = generated_text.find('}', json_start_ind) + 1
        json_text = generated_text[json_start_ind:json_end_ind]
        self.generated_result = parse_result_json(json_text)


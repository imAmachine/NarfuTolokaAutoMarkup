from bs4 import BeautifulSoup

from bot.toloka_model import TolokaModel


class TolokaParser:
    def __init__(self, session, form_url):
        self.session = session
        self.form_url = form_url
        self.csrf = self.get_csrf_token()

    def get_csrf_token(self):
        response = self.session.get(self.form_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        return csrf_token

    def get_toloka_model(self):
        response = self.__fetch_data_from_website()
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            post_element = soup.select_one('.descr > .descr__about > .about__text > p')
            post = post_element.get_text(strip=True) if post_element else None

            comment_element = soup.select_one('.descr > .descr__section, .flex > .descr__text > p')
            comment = comment_element.get_text(strip=True) if comment_element else None

            post_id_element = soup.select_one('.form input[name="id"]')
            post_id = post_id_element.get('value') if post_id_element else None
            model = TolokaModel(post_id, post, comment)
            return model
        else:
            return None

    def __fetch_data_from_website(self):
        response = self.session.get(self.form_url)
        self.csrf = self.get_csrf_token()
        if response.ok:
            return response.text
        else:
            return None

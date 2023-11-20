class Authenticator:
    def __init__(self, session, login_payload):
        self.session = session
        self.login_payload = login_payload

    def login(self):
        response = self.session.post('http://tomeo.pythonanywhere.com/login/', data=self.login_payload)

        if 'NArFU TOLOKA - Login' in response.text.lower():
            return False
        return response.ok

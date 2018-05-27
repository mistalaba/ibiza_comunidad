from anymail.backends.mailgun import EmailBackend
from core.tasks import async_send_messages

class CustomEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        async_send_messages.delay(email_messages)

"""Google reCAPTCHA verification used for login form"""


from typing import Optional
import requests
from flask import current_app


def verify(token: Optional[str]) -> bool:
    secret_key = current_app.config['CAPTCHA_SECRET_KEY']

    res = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': secret_key,
            'response': token
            }
        )

    verified = False
    if res.status_code == 200 and res.json()['success']:
        verified = True

    return verified

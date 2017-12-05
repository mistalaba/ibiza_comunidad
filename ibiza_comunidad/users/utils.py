import hashlib
import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def get_avatar(source, email=None):
    """
    Method for retrieving an avatar from different sources.
    """

    if source == 'gravatar':
        """
        Gravatar needs the email address

        """
        if email:
            base_url = 'https://secure.gravatar.com/avatar/'
            size = '?s=1024'
            user_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
            url = '{}{}{}'.format(base_url, user_hash, size)

    return url

def save_avatar(user, url):
    """
    Takes an url and saves the avatar to connected account
    """
    img_temp = NamedTemporaryFile(delete=True)
    request = requests.get(url, stream=True)
    if request.status_code == requests.codes.ok:
        filename = 'gravatar.jpg'
        for block in request.iter_content(1024 * 8):
            if not block:
                break
            # Write image block to temporary file
            img_temp.write(block)
    else:
        return None

    user.user_profile.avatar.save(
        filename,
        File(img_temp)
    )


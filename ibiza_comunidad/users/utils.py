import hashlib
import requests
import random
import os

from django.core.files import File

from core.utils import material_color_palette, create_tempfile

def get_avatar(source, user, social_account=None):
    """
    Method for retrieving an avatar from different sources.
    Provide social_account if fb or twitter
    """
    url = None
    filext = '.jpg'
    prefix = '{}_'.format(source)

    # Check if it's Facebook
    if social_account:
        url = social_account.get_avatar_url()
    # Check if it's Twitter
    elif source == 'gravatar':
        """
        Gravatar needs the email address
        """
        if user.email:
            email = user.email
            base_url = 'https://secure.gravatar.com/avatar/'
            size = '1024'
            user_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
            url = '{0}{1}{3}?s={2}&d=404'.format(base_url, user_hash, size, filext)

    if url:
        create_tempfile(url, prefix, filext)
    return None


def save_avatar(user, image_object):
    if image_object:
        user.profile.avatar.save(
            os.path.basename(image_object.name),
            File(image_object)
        )


def assign_random_user_color(user=None):
    color = random.choice(material_color_palette)
    if user is None:
        return color[1]
    else:
        if user.profile.color == '#000000':
            # Assign a color
            user.profile.color = color[1]
            user.profile.save()
        return user


def get_initials(user):
    if not user.first_name and not user.last_name:
        # Get initials from username
        initials = user.username[:2]
    else:
        initials = '{}{}'.format(user.first_name[:1], user.last_name[:1])
    return initials.upper()

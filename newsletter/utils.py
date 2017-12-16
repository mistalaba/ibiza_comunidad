from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

import logging
logger = logging.getLogger(__name__)


def send_newsletter_signup(request, extra_context):
    """
    Necessary context:
    'subject',
    'recipient_email',
    'category' category object

    Optional:
    'button_link'
    'button_text'
    """
    # text_content = 'Welcome to the newsletter.\nPlease activate your subscription by this link: {}\n\nKind regards,\n/Comunidad Ibiza\n\nUnsubscribe here: %tag_unsubscribe_url%'.format(url)
    # html_content = '<p>Welcome to the newsletter.<br>Please activate your subscription <a href="{}">here</a></p><p>Kind regards,<br>/Comunidad Ibiza</p><p><a href="%tag_unsubscribe_url%">Unsubscribe</a></p>'.format(url)
    context = {
        'logo': request.build_absolute_uri("static/newsletter/logo-192x192.png")
    }
    context.update(extra_context)
    category = context['category']

    c = Context(context)
    text_content = render_to_string('email_templates/confirm.txt', c)
    html_content = render_to_string('email_templates/beefree-confirm.html', c)
    import ipdb; ipdb.set_trace()
    msg = EmailMultiAlternatives(
        extra_context['subject'],
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [extra_context['recipient_email']],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.tags = [category.tag]
    msg.send()
    logger.info("Confirmation email sent to {}".format(extra_context['recipient_email']))

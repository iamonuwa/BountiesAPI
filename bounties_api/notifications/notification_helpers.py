from django.template.loader import render_to_string
from notifications.models import Notification, DashboardNotification
from bounties.ses_client import send_email
from bounties.utils import bounty_url_for, profile_url_for
from django.db import transaction


def create_bounty_notification(**kwargs):
    bounty = kwargs.pop('bounty')
    bounty_url = bounty_url_for(bounty.bounty_id, bounty.platform) + kwargs.get('url_query', '')
    kwargs.update({'url': bounty_url, 'notification_created': bounty.bounty_created})
    create_notification(**kwargs)


def create_profile_updated_notification(*args, **kwargs):
    profile_url = profile_url_for(kwargs.get('user').public_address)
    kwargs.update({'url': profile_url})
    create_notification(**kwargs)


@transaction.atomic
def create_notification(
        uid,
        notification_name,
        user,
        notification_created,
        data,
        subject,
        is_activity=True,
        string_data_email=None,
        email_button_string='View in App',
        url=''):

    notification, created = Notification.objects.get_or_create(
        uid=str(uid),
        defaults={
            'notification_name': notification_name,
            'user': user,
            'notification_created': notification_created,
            'dashboard': True,
        },
    )
    # this is atomic, so this is a good indicator
    if not created:
        return
    DashboardNotification.objects.create(
        notification=notification,
        string_data=data,
        is_activity=is_activity,
        data={'link': url},
    )

    username = 'bounty hunter'
    if user and user.name:
        username = user.name
    email_html = render_to_string(
        'base_notification.html',
        context={
            'link': url,
            'username': username,
            'message_string': string_data_email or data,
            'button_text': email_button_string})
    email_txt = 'Hello {}! \n {}'.format(
        username, string_data_email or data, )
    email_settings = user.settings.emails
    activity_emails = email_settings['activity']
    if is_activity and not activity_emails:
        return

    if not is_activity and notification_name not in user.settings.accepted_email_settings():
        return

    if not notification.email_sent:
        send_email(user.email, subject, email_txt, email_html)
        notification.email_sent = True
        notification.save()

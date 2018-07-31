from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.models import Bounty
from std_bounties.client_helpers import map_user_data
from user.models import User

bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackMessageClient()


def profile_updated(**kwargs):
    data = map_user_data(
        kwargs.get('inputs').get('profile'),
        kwargs.get(
            'transaction_from',
            None))
    user = User.objects.get_or_create(
        public_address=kwargs.get(
            'transaction_from', '').lower())[0]

    for (key, value) in data.items():
        if key != 'languages' and key != 'skills':
            setattr(user, key, value)

    user.save_and_clear_languages(data.get('languages'))
    user.save_and_clear_skills(data.get('skills', []))

    user.save()

    notification_client.profile_updated(
        kwargs.get(
            'transaction_from',
            '').lower(),
        **kwargs)


def bounty_issued(bounty_id, **kwargs):
    bounty = Bounty.objects.filter(bounty_id=bounty_id)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('value', None)

    if bounty.exists():
        return

    created_bounty = bounty_client.issue_bounty(bounty_id, **kwargs)
    if not is_issue_and_activate:
        notification_client.bounty_issued(bounty_id, **kwargs)
        slack_client.bounty_issued(created_bounty)


def bounty_activated(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('issuer', None)
    bounty_client.activate_bounty(bounty, **kwargs)
    if is_issue_and_activate:
        slack_client.bounty_issued_and_activated(bounty)
        notification_client.bounty_issued_and_activated(bounty_id, **kwargs)
    else:
        notification_client.bounty_activated(bounty_id, **kwargs)
        slack_client.bounty_activated(bounty)


def bounty_fulfilled(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.fulfill_bounty(bounty, **kwargs)
    notification_client.bounty_fulfilled(bounty_id, **kwargs)
    slack_client.bounty_fulfilled(bounty, fulfillment_id)


def fullfillment_updated(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.update_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_updated(bounty_id, **kwargs)
    slack_client.fulfillment_updated(bounty, fulfillment_id)


def fulfillment_accepted(bounty_id, **kwargs):
    fulfillment_id = kwargs.get('fulfillment_id')
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.accept_fulfillment(bounty, **kwargs)
    notification_client.fulfillment_accepted(bounty_id, **kwargs)
    slack_client.fulfillment_accepted(bounty, fulfillment_id)


def bounty_killed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.kill_bounty(bounty, **kwargs)
    notification_client.bounty_killed(bounty_id, **kwargs)
    slack_client.bounty_killed(bounty)


def contribution_added(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    inputs = kwargs.get('inputs', {})
    is_issue_and_activate = inputs.get('issuer', None)
    bounty_client.add_contribution(bounty, **kwargs)
    if not is_issue_and_activate:
        notification_client.contribution_added(bounty_id, **kwargs)
        slack_client.contribution_added(bounty)


def deadline_extended(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.extend_deadline(bounty, **kwargs)
    notification_client.deadline_extended(bounty_id, **kwargs)
    slack_client.deadline_extended(bounty)


def bounty_changed(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.change_bounty(bounty, **kwargs)
    notification_client.bounty_changed(bounty_id, **kwargs)
    slack_client.bounty_changed(bounty)


def issuer_transferred(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.transfer_issuer(bounty, **kwargs)
    notification_client.issuer_transferred(bounty_id, **kwargs)
    slack_client.issuer_transferred(bounty)


def payout_increased(bounty_id, **kwargs):
    bounty = Bounty.objects.get(bounty_id=bounty_id)
    bounty_client.increase_payout(bounty, **kwargs)
    notification_client.payout_increased(bounty_id, **kwargs)
    slack_client.payout_increased(bounty)

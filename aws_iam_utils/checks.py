import sys

from policyuniverse.expander_minimizer import expand_policy
from policy_sentry.querying.actions import get_action_data

from aws_iam_utils.constants import READ, LIST, WRITE
from aws_iam_utils.util import extract_policy_permission_items

def policies_are_equal(p1, p2):
    """
    Checks whether two policies give the same permissions. This will expand all wildcards and Resource constraints and then compare the result.

    @param p1  The first policy. Should be a dict that contains a Statement key, which should be a list of dicts conforming to the AWS IAM Policy schema.
    @param p2  The second policy, same format as p1.

    @returns True if p1 and p2 represent exactly the same permissions, or False otherwise.
    """
    return extract_policy_permission_items(expand_policy(p1)) == extract_policy_permission_items(expand_policy(p2))

def policy_has_only_these_access_levels(p, access_levels):
    """
    Returns True if all actions granted under the given policy are Read or List actions.
    """
    p_items = extract_policy_permission_items(expand_policy(p))
    for item in p_items:
        action_service, action_name = item["action"].split(":")

        action_output = get_action_data(action_service, action_name)

        if action_output is False:
            raise ValueError(f'invalid action: {item["action"]}')

        for action_output_action in action_output[action_service]:
            if action_output_action["action"].lower() != item["action"].lower():
                continue

            if action_output_action["access_level"] not in access_levels:
                return False

    return True


def is_read_only_policy(p):
    """
    Returns True if all actions granted under the given policy are Read or List actions.
    """
    return policy_has_only_these_access_levels(p, [ READ, LIST ])


def is_list_only_policy(p):
    """
    Returns True if all actions granted under the given policy are List actions.
    """
    return policy_has_only_these_access_levels(p, [ LIST ])


def is_read_write_policy(p):
    """
    Returns True if all actions granted under the given policy are Read, List or Write actions.
    """
    return policy_has_only_these_access_levels(p, [ READ, LIST, WRITE ])

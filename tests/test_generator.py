import pytest
import copy

from .context import aws_iam_utils
from aws_iam_utils.constants import READ, LIST, WRITE

def test_generate_read_only_policy():
    p = aws_iam_utils.generator.generate_read_only_policy_for_service('s3')

    for statement in p['Statement']:
        for action in statement['Action']:
            assert action.startswith('s3:')

    assert aws_iam_utils.checks.is_read_only_policy(p)

def test_generate_write_only_policy():
    p = aws_iam_utils.generator.generate_write_only_policy_for_service('s3')

    for statement in p['Statement']:
        for action in statement['Action']:
            assert action.startswith('s3:')

    assert aws_iam_utils.checks.is_write_only_policy(p)

def test_generate_list_only_policy():
    p = aws_iam_utils.generator.generate_list_only_policy_for_service('s3')

    for statement in p['Statement']:
        for action in statement['Action']:
            assert action.startswith('s3:')

    assert aws_iam_utils.checks.is_list_only_policy(p)

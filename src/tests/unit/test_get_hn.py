from unittest.mock import MagicMock

from pytest import fixture

from newsbot.app import GetHN


SLACK_TEXT = "Top 3 from HackerNews:\n>*<https://news.ycombinator.com/item?id=1|1>* - <abc|bcd>"


@fixture()
def obj():
    obj = GetHN.__new__(GetHN)
    obj.logger = MagicMock()
    return obj


def test_should_create_hn_text(obj):
    obj.get_top_stories = MagicMock(
        return_value=[{
            "id": 1,
            "score": 1,
            "url": "abc",
            "title": "bcd"
        }]
    )
    assert obj.create_hn_text() == SLACK_TEXT

# TODO: Add more tests

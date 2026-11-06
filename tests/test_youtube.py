from tizen_tv_homecore.youtube import parse_video


def test_plain_id():
    assert parse_video("abc123") == ("abc123", None, 0)


def test_url_with_list_and_time():
    url = "https://www.youtube.com/watch?v=abc123&list=PL1&t=90s"
    assert parse_video(url) == ("abc123", "PL1", 90)

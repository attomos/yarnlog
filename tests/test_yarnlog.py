from pathlib import Path

import requests_mock
from freezegun import freeze_time

from yarnlog.main import download_and_extract, extract, pipeline, save_file


def test_extract():
    text = """\
<pre>2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
</pre>"""
    expected = """\
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
"""
    actual = extract(text)
    assert actual == expected


def test_extract_witout_pre_tag():
    text = """\
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
"""
    expected = ""
    actual = extract(text)
    assert actual == expected


def test_download_and_extract():
    with requests_mock.Mocker() as m:
        mock_response_text = """\
<pre>2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
</pre>"""
        expected = """\
EXTRACTED FROM http://test.com/application_1234
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
"""
        yarn_url = "http://test.com/application_1234"
        m.get(yarn_url, text=mock_response_text)
        actual = download_and_extract(yarn_url)
        assert actual == expected


def test_download_and_extract_without_pre_tag():
    with requests_mock.Mocker() as m:
        mock_response_text = """\
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null"""
        expected = """\
EXTRACTED FROM http://test.com/application_1234
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null"""
        yarn_url = "http://test.com/application_1234"
        m.get(yarn_url, text=mock_response_text)
        actual = download_and_extract(yarn_url)
        assert actual == expected


def test_save_file():
    save_file(output="some text", output_file="yarnlog_2020")
    output_path = Path("yarnlog_2020")
    actual = output_path.read_text()
    expected = "some text"
    assert actual == expected
    output_path.unlink()


@freeze_time("2020-11-28 05:34:36.112233", tz_offset=0)
def test_pipeline():
    with requests_mock.Mocker() as m:
        mock_response_text = """\
<pre>2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
</pre>"""
        expected = """\
EXTRACTED FROM http://test.com/application_0534
2020-11-22 22:50:27.490 [main] DEBUG org.apache.hadoop.util.Shell - setsid exited with exit code 0
2020-11-22 22:50:27.514 [main] DEBUG org.apache.hadoop.security.Groups - Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping; cacheTimeout=300000; warningDeltaMs=5000
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from system property: null
2020-11-22 22:50:27.542 [main] DEBUG org.apache.hadoop.metrics2.impl.MetricsSystemImpl - from environment variable: null
"""
        yarn_url = "http://test.com/application_0534"
        m.get(yarn_url, text=mock_response_text)
        pipeline(yarn_url)
        output_path = Path("yarnlog_2020_11_28_053436__112233")
        actual = output_path.read_text()
        assert actual == expected
        output_path.unlink()

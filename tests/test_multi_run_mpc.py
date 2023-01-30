import pathlib
from unittest.mock import call

import pytest

from mpc import multi_run_mpc as mpc


def test_time_class_ok():
    # Given
    dummy_time = "12:34:56"
    dummy_hour = 12
    dummy_minute = 34
    dummy_second = 56
    dummy_list = [12, 34, 56]
    # When
    actual = mpc.Time(dummy_time)
    # Then
    assert actual.hour == dummy_hour
    assert actual.minute == dummy_minute
    assert actual.seconds == dummy_second
    assert actual.list == dummy_list


@pytest.mark.parametrize(
    # Given
    "dummy_time",
    [
        "00:70:00",
        "-05:00:00",
        "00:01:70",
        "00:-15:00",
        "00:05:-08"
    ]
)
def test_time_class_raises(dummy_time):
    # Then
    with pytest.raises(ValueError):
        # When
        mpc.Time(dummy_time)


@pytest.mark.parametrize(
    # Given
    "time_diff, initial_time, expected",
    [
        (10, "00:00:00", "00:00:10"),
        (600, "00:50:25", "01:00:25"),
        (3, "03:59:57", "04:00:00"),
        (-5, "00:05:04", "00:04:59"),
        (-75, "00:01:30", "00:00:15"),
        (1, "11:24:35", "11:24:36")
    ]
)
def test_calculate_time_span_ok(time_diff, initial_time, expected):
    # When
    actual = mpc.Time(initial_time).calculate_time_span(time_diff)
    # Then
    assert actual == expected


def test_calculate_time_span_raises():
    # Given
    time_diff = -10
    initial_time = "00:00:09"
    # Then
    with pytest.raises(ValueError):
        # When
        mpc.Time(initial_time).calculate_time_span(time_diff)


def test_instantiate_movies(capsys):
    # Given
    file1 = 'path/to/file1.mp4'
    file2 = 'path/to/file2.mp4'
    time1 = '00:00:30'
    time2 = '00:10:30'
    # When
    a = mpc.Movie(file_path=file1, start_time=time1)
    b = mpc.Movie(file_path=file2, start_time=time2)
    print(a)
    captured = capsys.readouterr()
    expected = [a, b]
    # Then
    assert a.start_time == time1
    assert a.file_path == file1
    assert b.start_time == time2
    assert b.file_path == file2
    assert mpc.Movie.all_movies == expected
    assert a.file_path in captured.out
    assert a.start_time in captured.out


def test_load_configuration():
    # Given
    config_path = './config.json'
    # When
    mpc.load_configuration(config_path)
    # Then
    assert mpc.CONFIGURATION.get('base_command') == "MPC"
    assert mpc.CONFIGURATION.get('first_argument') == " arg1 "
    assert mpc.CONFIGURATION.get('second_argument') == " arg2"
    assert mpc.CONFIGURATION.get('path_to_movies_json') == "movies.json"
    assert mpc.CONFIGURATION.get('time_offset') == "60"
    assert mpc.CONFIGURATION.get('quiet') is True
    assert mpc.CONFIGURATION.get('dry_run') is False


def test_load_movies():
    # Given
    mpc.Movie.all_movies = []
    json_path = pathlib.Path('./movies.json')
    file1 = 'file/path/movie1.mp4'
    file2 = 'file/path/movie2.mp4'
    file3 = 'file/path/movie3.mp4'
    time = "00:00:00"
    # When
    mpc.load_movies(json_path)
    # Then
    assert len(mpc.Movie.all_movies) == 3
    assert mpc.Movie.all_movies[0].file_path == file1
    assert mpc.Movie.all_movies[1].file_path == file2
    assert mpc.Movie.all_movies[2].file_path == file3
    assert mpc.Movie.all_movies[0].start_time == time
    assert mpc.Movie.all_movies[1].start_time == time
    assert mpc.Movie.all_movies[2].start_time == time


def test_build_commands():
    # Given
    mpc.Movie.all_movies = []
    file1 = 'path/to/file1.mp4'
    file2 = 'path/to/file2.mp4'
    time1 = '00:00:30'
    time2 = '00:10:30'
    time1_exp = '00:01:30'
    time2_exp = '00:11:30'
    mpc.CONFIGURATION['time_offset'] = 60
    mpc.CONFIGURATION['quiet'] = True
    mpc.CONFIGURATION['base_command'] = 'base'
    mpc.CONFIGURATION['first_argument'] = ' first '
    mpc.CONFIGURATION['second_argument'] = ' second'
    expected = [f'base \"{file1}\" first {time1_exp} second',
                f'base \"{file2}\" first {time2_exp} second']
    a = mpc.Movie(file_path=file1, start_time=time1)
    b = mpc.Movie(file_path=file2, start_time=time2)
    # When
    actual = mpc.build_commands()
    # Then
    assert a.new_start_time == time1_exp
    assert b.new_start_time == time2_exp
    assert actual == expected


def test_start_execution(mocker):
    # Given
    mpc.CONFIGURATION['dry_run'] = False
    patched_os = mocker.patch('os.system')
    cmd_list = ['cmd1', 'cmd2', 'cmd3']
    calls = [call('cmd /c "cmd1"'), call('cmd /c "cmd2"'), call('cmd /c "cmd3"')]
    # When
    mpc.start_execution(cmd_list)
    # Then
    patched_os.assert_has_calls(calls)

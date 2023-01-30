import pytest

import Multi_Run_MPC as mpc


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
        (-75, "00:01:30", "00:00:15")
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

"""Lab 6 line-coverage test cases for the supplied recycling rewards module."""
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_paper_below_minimum():
    assert reward_points("paper", 3, False) == 0


def test_paper_exact_minimum():
    assert reward_points("paper", 5, False) == 0


def test_paper_with_bonus():
    assert reward_points("paper", 7, True) == 18


def test_metal_base_rate():
    assert reward_points("metal", 5, False) == 36


def test_paper_large_extra():
    assert reward_points("paper", 26, False) == 210


def test_metal_large_extra():
    assert reward_points("metal", 23, False) == 378


def test_hazardous_small_collection():
    assert collection_accepted(5, 5, True) is True


def test_nonhazardous_too_heavy():
    assert collection_accepted(51, 2, False) is False


def test_nonhazardous_accepted():
    assert collection_accepted(20, 2, False) is True


def test_nonhazardous_too_many_bags():
    assert collection_accepted(20, 4, False) is False


def test_morning_open():
    assert slot_status(20, True, False) == "open"


def test_evening_late():
    assert slot_status(5, False, False) == "late"


def test_holiday_missed():
    assert slot_status(0, True, True) == "missed"


def test_holiday_open():
    assert slot_status(35, True, True) == "open"

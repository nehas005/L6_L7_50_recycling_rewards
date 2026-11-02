"""Lab 6 branch-coverage tests, including boundary decisions and alternate outcomes."""
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


@pytest.mark.parametrize("material,weight,bonus,expected", [
    ("paper", 3, False, 0),      # no bonus, below threshold
    ("paper", 5, False, 0),      # equality: extra == 0
    ("paper", 5, True, 6),       # bonus reduces the paper minimum to 4
    ("plastic", 3, True, 6),     # plastic bonus
    ("plastic", 4, False, 6),    # nonmetal, regular rate
    ("metal", 2, True, 0),       # metal bonus does not reduce minimum
    ("metal", 3, False, 12),     # metal standard rate
    ("paper", 25, False, 120),   # extra == 20: no increased rate
    ("paper", 26, False, 210),   # extra > 20: increased nonmetal rate
    ("metal", 22, False, 240),   # extra == 20: no increased rate
    ("metal", 23, False, 378),   # extra > 20: additional metal rate
])
def test_reward_branches(material, weight, bonus, expected):
    assert reward_points(material, weight, bonus) == expected


@pytest.mark.parametrize("material,weight,message", [
    ("glass", 10, "unknown material"),
    ("paper", -0.1, "invalid weight"),
])
def test_reward_invalid_inputs(material, weight, message):
    with pytest.raises(ValueError, match=message):
        reward_points(material, weight, False)


@pytest.mark.parametrize("weight,bags,hazardous,expected", [
    (5, 100, True, True),    # hazardous is accepted at its weight boundary
    (5.1, 1, True, False),  # hazardous over its weight boundary
    (50, 3, False, True),   # nonhazardous boundary
    (50.1, 3, False, False),
    (20, 4, False, False),  # too many bags
    (20, 3, False, True),
])
def test_collection_branches(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize("minutes,morning,holiday,expected", [
    (20, True, False, "open"),    # morning open boundary
    (19, True, False, "late"),
    (5, True, False, "late"),     # morning late boundary
    (4, True, False, "missed"),
    (10, False, False, "open"),   # evening cutoff
    (-5, False, False, "late"),  # evening late boundary
    (-6, False, False, "missed"),
    (35, True, True, "open"),    # holiday adjusts morning cutoff
    (20, True, True, "late"),
    (19, True, True, "missed"),
    (25, False, True, "open"),   # holiday adjusts evening cutoff
    (10, False, True, "late"),
    (9, False, True, "missed"),
])
def test_slot_branches(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected

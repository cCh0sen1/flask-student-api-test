import pytest
@pytest.mark.parametrize(
    "age,result",
    [
        (10,"未成年"),
        (18,"成年"),
        (32,"成年")
    ]
)
def test_age(age,result):
    if age>=18:
        actual="成年"
    else:
        actual="未成年"

    assert actual==result

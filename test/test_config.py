import pytest

class NotInRange(Exception):
    def __init__(self,message="Value not valid"):
        self.message=message
        super().__init__(self.message)


def test_generic():
    a=42
    b=42
    assert a==b


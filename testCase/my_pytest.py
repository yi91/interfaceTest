import pytest
from ddt import ddt, data, unpack
from XTestRunner import HTMLTestRunner


@ddt
class TestClass:
    lia = [['一组', 1, 1], ['二组', 1, 2], ['三组', 2, 2]]

    @data(lia)
    @unpack
    def test_one(self, name, a, b):
        assert a == b


if __name__ == '__main__':
    pytest.main(['-s', '--html=./report.html', 'my_pytest.py'])

import add


class TestPlugin:

    def test_add_function(self):
        assert 6 == add.add(3, 3)
        assert 6 != add.add(3, 4)

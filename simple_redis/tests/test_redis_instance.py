from simple_redis import RedisInstance


class Foo:
    def __repr__(self):
        return self.a

    def __init__(self, a):
        self.a = a


def test_ri():
    ri = RedisInstance()

    ri['a'] = {'b': 1, 'c': 10}
    # print("ri['a']['b']:", ri['a']['b'])
    assert ri['a']['b'] == 1

    f = Foo('correct')
    k = ri.set_obj(f)
    # print("ri[k].a:", ri[k].a)
    assert ri[k].a == 'correct'

    # print("ri.keys()", ri.keys())

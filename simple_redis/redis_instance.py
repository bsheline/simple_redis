# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:24:47 2018

@author: robert.sheline
"""

import os
import re
import subprocess
from pickle import loads, dumps

import redis


class RedisInstance:
    """ Wraps a redis instance, creates server if it doesn't already exist,
    or if force=True
        Will tear down the server at cleanup iff it created it.
        Can handle arbitrary objects as keys and values.
        Internal convention for keys is obj.__class__.__name + "__" + repr(obj)

        use with e.g.: RedisInstance[key] = value
    """

    def __getitem__(self, key):
        return loads(self._store[dumps(key)])

    def __setitem__(self, key, value):
        self._store[dumps(key)] = dumps(value)

    def __delitem__(self, key):
        del self._store[dumps(key)]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._store.keys())

    def keys(self):
        return [loads(x) for x in self._store.keys()]

    def clear(self):
        self._store.flushdb()

    def __init__(self, url='localhost', port=6379, flush=True):
        self.owns_redis = False
        self.address = url
        self.port = port

        # attempt to check for REDIS_HOME enviornment variable,
        # alternatively check for
        # redis binaries in folder below this file. This doesn't matter if
        # redis instance
        # is assumed to be already running.
        path = os.environ.get('REDIS_HOME',
                              os.path.join(os.path.dirname(__file__), 'redis'))
        path = re.compile(r"[\/]").split(
            path)  # fix windows backslash confusion
        self.redis_home = os.path.join(*path)

        if not self.check_server():
            self.create_server()
            assert self.check_server()

        if flush:
            self.clear()

    def __del__(self):
        if self.owns_redis:
            print('tearing down temporary redis server')
            subprocess.call([os.path.join(self.redis_home, 'redis-cli'), '-p',
                             str(self.port), 'shutdown'])

    def check_server(self):
        self._store = redis.StrictRedis(host=self.address, port=self.port,
                                        db=0)
        try:
            self.__setitem__("foo", "bar")
            self.__delitem__("foo")
        except Exception as e:
            print(e)
            return False
        return True

    def create_server(self):
        self.owns_redis = True

        print("creating temporary redis server")
        self.process = subprocess.Popen(
            [os.path.join(self.redis_home, 'redis-server'), '--port',
             str(self.port)],
            stdout=open(os.devnull, 'wb'),
            stderr=subprocess.STDOUT)

        # blocking call to verify server is up
        subprocess.call(
            [os.path.join(self.redis_home, 'redis-cli'), '-p', str(self.port),
             'ping'])

    def set_obj(self, obj):
        """ Store object and return key, using convention
            redis[obj.__class__.__name + "__" + repr(obj)] = obj
        """
        try:
            key = obj.__class__.__name__ + "__" + repr(obj)
            self.__setitem__(key, obj)
            return key
        except Exception as e:
            print(e)
            return None

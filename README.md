# Requirements

* python 3
* redis server (unless connecting remotely):
    - on windows, redis binaries made available at "REDIS_HOME" 
    - on linux, install redis with `sudo apt install redis-server` 

# Installation

* `pip install --upgrade git+https://hq-git.soartech.com/robert.sheline/simple_redis.git`

# Usage

url/port could be an existing server, or a new one: 

`from simple_redis import RedisInstance`\
`ri = RedisInstance(url='localhost', port=6379)`\
`ri['a'] = {'b': 'c'}`\
`print(ri['a']['b'])`

arbitrary object keys/values:

`ri[[True]] = [False]`\
`print(ri[[True]])`

built-in naming convention:

`k = ri.set_obj([True])`\
`print(k)`\
`print(ri[k])`

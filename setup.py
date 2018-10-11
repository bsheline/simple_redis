import setuptools

setuptools.setup(
    name='simple_redis',
    version='0.1',
    description='Wrapper for stupid-easy redis usage',
    url='https://hq-git.soartech.com/git/RaCHeM.git',

    packages=setuptools.find_packages(),

    install_requires=[
        'redis'
    ],

    test_suite='nose.collector',
    tests_require=['nose'],

    zip_safe=True,
)

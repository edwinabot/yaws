from setuptools import setup

setup(
    name='yaws',
    version='0.1',
    py_modules=['yaws'],
    setup_requires=["setuptools-pipfile"],
    use_pipfile=True,
    entry_points='''
        [console_scripts]
        yaws=yaws:create_new_crawl
    ''',
)
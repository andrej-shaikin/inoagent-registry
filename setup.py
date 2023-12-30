from distutils.core import setup

setup(
    name='inoagent-registry',
    version='1.0.2',
    packages=[
        'inoagent'
    ],
    python_requires='>=3.10',
    url='https://github.com/andrej-shaikin/inoagent-registry',
    license='MIT',
    author='Andrey Shaikin',
    author_email='kiwibon@yandex.ru',
    description='Функционал получения актуального списка иноагентов с сайта МинЮста РФ',
    requires=[
        "httpx",
        "pydash",
        "beautifulsoup4",
        "lxml",
    ],
)

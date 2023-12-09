from distutils.core import setup

setup(
    name='inoagent-control',
    version='1.0.0',
    packages=[
        'inoagent'
    ],
    python_requires='>=3.10',
    url='https://gitlab.com/kiwib/inoagent-control',
    license='MIT',
    author='Andrey Shaikin',
    author_email='kiwibon@yandex.ru',
    description='Функционал получения актуального списка иноагентов с сайта МинЮста РФ',
    requires=[
        "httpx",
        "pydash",
    ],
)

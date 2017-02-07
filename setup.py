from distutils.core import setup

setup(
    name = 'cphelper',
    packages = ['cphelper'],
    version = '1.4',
    description = 'A API which will return Course of specific Dept. and also Course which you can enroll at that time.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/cphelper',
    download_url = 'https://github.com/Stufinite/cphelper/archive/v1.4.tar.gz',
    keywords = ['coursepickinghelper', 'timetable', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec',
        'pymongo==3.4.0',
    ],
    zip_safe=True
)

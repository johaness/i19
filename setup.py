from distutils.core import setup

VERSION = '0.0.1'
NAME = 'i19'

setup(
        name = NAME,
        version = VERSION,
        description = "i18n for Angular",
        long_description = "",
        license = 'BSD',
        author = "Johannes Steger",
        author_email = 'jss@coders.de',
        url = 'https://github.com/johaness/%s' % (NAME,),
        zip_safe = False,
        packages = ['i19',],
        package_dir = {'i19': '.',},
        package_data = {'i19': 
            ['i19.js', 'README.rst', 'common.mk',],
            },
        entry_points = {
            'console_scripts': [
                'i19dict=i19.i19dict:main',
                'i19extract=i19.i19extract:main',
                'i19json=i19.i19json:main',
                'i19conf=i19.i19conf:main',
                ],
            },
        install_requires = ['babel',],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: BSD License',
            ],
        )


from setuptools import setup

VERSION = '0.0.4'
NAME = 'i19'

try:
    readme = file('README.rst').read()
except:
    readme = ''

setup(
        name = NAME,
        version = VERSION,
        description = "Support module for i18n in AngularJS",
        long_description = readme,
        license = 'BSD',
        author = "Johannes Steger",
        author_email = 'jss@coders.de',
        url = 'https://github.com/johaness/%s' % (NAME,),
        zip_safe = False,
        packages = ['i19',],
        package_data = {
            'i19': ['i19.js',],
        },
        entry_points = {
            'distutils.commands': [
                'json_catalog=i19.json_catalog:json_catalog',
                'json_angular=i19.json_angular:json_angular',
            ],
            'babel.extractors': [
                'i19_xml = i19.extract:extract',
            ],
        },
        install_requires = ['babel',],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: BSD License',
        ],
)


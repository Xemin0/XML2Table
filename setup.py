from setuptools import setup, find_packages

setup(
    name = 'xml2table',
    version = '0.2.2',
    packages = find_packages(),
    url = 'https://github.com/Xemin0/XML2Table',

    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license = 'BSD',
    author = 'Xemin0',
    author_email = 'loser.qqfang@gmail.com',
    description = 'A simple python GUI to facilate parameter settings (Contact Energies) in XML file generated by CompuCell3D, by converting between XML and a colored table. ',
    install_requires = [
        'numpy>=1.8.0',
    ],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'xml2table=xml2table.xml2table:main',
        ],
    }
)

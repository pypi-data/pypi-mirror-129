#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


# previous approach used to ignored badges in PyPI long description
# long_description = '{}\n{}'.format(
#     re.compile(
#         '^.. start-badges.*^.. end-badges',
#         re.M | re.S,
#         ).sub(
#             '',
#             read('README.rst'),
#             ),
#     re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read(join('docs', 'CHANGELOG.rst')))
#     )

long_description = '{}\n{}'.format(
    read('README.rst'),
    read(join('docs', 'CHANGELOG.rst')),
    )

setup(
    name='py30303_disc',
    version='0.3.0',
    description='UDP 30303 Network discovery library.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='Apache 2.0',
    author='Tim Rightnour',
    author_email='the@garbled.one',
    url='https://github.com/garbled1/py30303_disc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    project_urls={
        'webpage': 'https://github.com/garbled1/py30303_disc',
        'Documentation': 'https://py30303_disc.readthedocs.io/en/latest/',
        'Changelog': 'https://github.com/garbled1/py30303_disc/blob/master/docs/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/garbled1/py30303_disc/issues',
        'Discussion Forum': 'https://github.com/garbled1/py30303_disc/discussions',
        },
    keywords=[
        'udp', 'discovery', '30303',
        ],
    python_requires='>=3.6, <3.10',
    install_requires=[
        # 'click',
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
        },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
        ],
    entry_points={
        'console_scripts': [
            'discover_30303= py30303_disc.cli_int1:main',
            ]
        #
        },
    # cmdclass={'build_ext': optional_build_ext},
    # ext_modules=[
    #    Extension(
    #        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
    #        sources=[path],
    #        include_dirs=[dirname(path)]
    #    )
    #    for root, _, _ in os.walk('src')
    #    for path in glob(join(root, '*.c'))
    # ],
    )

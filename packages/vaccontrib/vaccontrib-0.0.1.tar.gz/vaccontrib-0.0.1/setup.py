from setuptools import setup, Extension
import setuptools
import os
import sys

# get __version__, __author__, and __email__
exec(open("./vaccontrib/metadata.py").read())

setup(
    name='vaccontrib',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url='https://github.com/benmaier/vaccontrib',
    license=__license__,
    description="Quantifying the contributions vaccinated individuals make towards the effective reproduction number.",
    long_description='',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
                'numpy>=1.17',
                'matplotlib>=3.3',
                'bfmplot>=0.0.11',
    ],
    tests_require=['pytest', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    project_urls={
        'Documentation': 'http://vaccontrib.readthedocs.io',
        'Contributing Statement': 'https://github.com/benmaier/vaccontrib/blob/master/CONTRIBUTING.md',
        'Bug Reports': 'https://github.com/benmaier/vaccontrib/issues',
        'Source': 'https://github.com/benmaier/vaccontrib/',
        'PyPI': 'https://pypi.org/project/vaccontrib/',
    },
    include_package_data=True,
    zip_safe=False,
)

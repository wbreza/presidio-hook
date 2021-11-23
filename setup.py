from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def get_version():
    """Parse package __version__.py to get version."""
    versionpy = (Path('pre_commit_hooks') / '__version__.py').read_text()
    return versionpy.split("'")[1]


VERSION = get_version()


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='presidio-hook',
    packages=find_packages(exclude=(['test*', 'tmp*'])),
    version=VERSION,
    description='Tool for detecting sensitive data in the codebase',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Copyright Wallace Breza, Inc. 2021',
    author='Wallace Breza',
    author_email='wallace.breza@microsoft.com',
    url='https://github.com/wbreza/presidio-hook',
    download_url='https://github.com/wbreza/presidio-hook/archive/{}.tar.gz'.format(VERSION),
    keywords=['secret-management', 'pre-commit', 'security', 'entropy-checks'],
    install_requires=[
        'pyyaml',
        'requests',
        'presidio_analyzer',
        'presidio_anonymizer',
        'en_core_web_lg'
    ],
    include_package_data=True,
    extras_require={
        'word_list': [
            'pyahocorasick',
        ],
        'gibberish': [
            'gibberish-detector',
        ],
    },
    entry_points={
        'console_scripts': [
            'presidio-hook = pre_commit_hooks.presidio:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
    ],
)
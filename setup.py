from setuptools import setup, find_packages
import codecs
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
META_PATH = os.path.join('noora', '__init__.py')


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


setup(
    name=find_meta('title'),
    version=find_meta('version'),
    description=find_meta('description'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license=find_meta('license'),
    author=find_meta('author'),
    author_email=find_meta('email'),
    maintainer=find_meta('author'),
    maintainer_email=find_meta('email'),
    url=find_meta('uri'),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='development database',
    packages=find_packages(exclude=['doc', 'docs', 'examples', 'releases', 'snippets', 'src', 'test', 'tests']),
    package_data={'noora': ['*.json',
                            'plugins/mysql/generate/templates/*.json',
                            'plugins/mysql/generate/templates/fct/*.sql',
                            'plugins/mysql/generate/templates/idx/*.sql',
                            'plugins/mysql/generate/templates/tab/*.sql',
                            'plugins/mysql/generate/templates/trg/*.sql',
                            'plugins/mysql/drop/fct/*.sql',
                            'plugins/mysql/drop/prc/*.sql',
                            'plugins/mysql/drop/tab/*.sql',
                            'plugins/mysql/drop/vw/*.sql',
                            'plugins/mysql/update/*.sql',
                            'plugins/mssql/generate/templates/*.json',
                            'plugins/mssql/generate/templates/fct/*.sql',
                            'plugins/mssql/generate/templates/idx/*.sql',
                            'plugins/mssql/generate/templates/seq/*.sql',
                            'plugins/mssql/generate/templates/tab/*.sql',
                            'plugins/mssql/generate/templates/trg/*.sql',
                            'plugins/mssql/drop/cst/*.sql',
                            'plugins/mssql/drop/fct/*.sql',
                            'plugins/mssql/drop/prc/*.sql',
                            'plugins/mssql/drop/seq/*.sql',
                            'plugins/mssql/drop/syn/*.sql',
                            'plugins/mssql/drop/tab/*.sql',
                            'plugins/mssql/drop/typ/*.sql',
                            'plugins/mssql/drop/vw/*.sql',
                            'plugins/mssql/update/*.sql',
                            'plugins/postgresql/generate/templates/*.json',
                            'plugins/postgresql/generate/templates/cst/*.sql',
                            'plugins/postgresql/generate/templates/fct/*.sql',
                            'plugins/postgresql/generate/templates/idx/*.sql',
                            'plugins/postgresql/generate/templates/seq/*.sql',
                            'plugins/postgresql/generate/templates/tab/*.sql',
                            'plugins/postgresql/generate/templates/trg/*.sql',
                            'plugins/postgresql/drop/cst/*.sql',
                            'plugins/postgresql/drop/fct/*.sql',
                            'plugins/postgresql/drop/idx/*.sql',
                            'plugins/postgresql/drop/seq/*.sql',
                            'plugins/postgresql/drop/tab/*.sql',
                            'plugins/postgresql/drop/trg/*.sql',
                            'plugins/postgresql/drop/vw/*.sql',
                            'plugins/postgresql/update/*.sql']},
    install_requires=['six', 'click', 'fire'],
    entry_points={
        'console_scripts': [
            'mynoora=noora.mynoora_cli:main',
        ],
    },
)

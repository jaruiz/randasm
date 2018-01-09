from setuptools import setup

setup(name=                 'randasm',
      version=              '0.1',
      description=          'Builds random, retargettable snippets of assembler source',
      url=                  'http://github.com/jaruiz/randasm',
      author=               'Jose A. Ruiz',
      author_email=         'jose.a.ruiz.dominguez.eu@gmail.com',
      license=              'GPLv3.0',
      packages=             ['randasm'],
      package_dir=          {'randasm': 'randasm'},
      package_data=         {'randasm': ['targets/*.yaml']},
      entry_points=         {
                                'console_scripts': [
                                    'randasm=randasm.cli:main'
                                ],
                            },
      scripts=              ['scripts/randasm-quickcheck'],
      install_requires=     ['pyyaml'],
      zip_safe=             True
      )

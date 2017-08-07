from setuptools import setup

setup(name='salmiak',
      version='0.3',
      description='The easiest movie file renamer this side of github',
      long_description="Look, it's not very powerful, but it's simple. And sometimes that's enough",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
      ],
      keywords='movie rename file scene',
      url='https://github.com/arkalon76/salmiak',
      author='Kenth Fagerlund',
      author_email='salmiak_code@gmail.com',
      license='MIT',
      packages=['salmiak'],
      install_requires=[
        'guessit',
      ],
      test_suite='tests',
      tests_require=['pytest',
                     'pytest',
                     'pytest-pep8',
                     'pytest-cov'],
      entry_points={'console_scripts': [
                        'salmiak = salmiak:main',
                        ],
                    },
      zip_safe=False)

# -*- coding: utf-8 -*-
__author__ = 'Mathieu COUTANT FLEURY'
from setuptools import setup, find_packages

version = '0.0.1'

setup(name='similarDbCnx',
      version=version,
      description="API to access to Database",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python',
      ],
      keywords='similar dbcnx',
      author='Mathieu COUTANT FLEURY',
      author_email='mathieu.coutantfleury@gmail.com',
      maintainer="Mathieu COUTANT FLEURY",
      maintainer_email='mathieu.coutantfleury@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['tests']),
      package_data={'similardbcnx': ['db/conf/*.conf']},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'SQLAlchemy>=1.2',
          'WTForms-Alchemy',
          'SQLAlchemy-Utils==0.33.11'
      ],
      extras_require={
          'mysql': ['mysqlclient~=1.3', ],
      },

      entry_points="""
# -*- Entry points: -*-
[console_scripts]
dbCnx = dbCnx:main
""",
      )

from setuptools import setup, find_packages

desc = """Deferred objects without Twisted."""
summ = """This is the Twisted implementation of Deferred objects with no requirements on the rest of Twisted for use a general purpose callback API."""

PACKAGE_NAME = "deferred"
PACKAGE_VERSION = "0.1"

setup(name=PACKAGE_NAME,
      version=PACKAGE_VERSION,
      description=desc,
      long_description=summ,
      author='Mikeal Rogers, Mozilla',
      author_email='mikeal.rogers@gmail.com',
      url='http://github.com/mikeal/deferred',
      license="MIT",
      packages=find_packages(),
      platforms =['Any'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT',
                   'Operating System :: OS Independent',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ]
     )

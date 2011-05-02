from setuptools import setup, find_packages

readme_file = 'README.rst'

setup(
    name='forms_extras',
    version='0.1.0',
    packages=find_packages('.'),

    # Metadata
    author='Nikolay Zakharov',
    author_email='nikolay@desh.su',
    url = 'https://github.com/freevoid/django-forms-extras',
    description='Extra features, fields and widgets for Django forms',
    long_description=open(readme_file).read(),
    keywords='django forms widgets',
    license = 'MIT',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Framework :: Django',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
    ],
)

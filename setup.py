from setuptools import find_packages, setup


install_requires = [
    'django>=1.8,<2.0',
    'wagtail>=1.2,<2.0'
]

test_require = [
    'flake8',
    'isort',
    'pytest',
    'pytest-cov',
    'pytest-django',
    'wagtail',
]

setup(
    name='wagtail-themes',
    version='0.2.0',
    description='Site specific theme loader for Django Wagtail.',
    author='Rob Moorman',
    author_email='rob@moori.nl',
    url='https://github.com/moorinteractive/wagtail-themes',
    license='MIT',
    install_requires=install_requires,
    extras_require={
        'test': test_require,
    },
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ]
)

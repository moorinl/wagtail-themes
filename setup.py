from setuptools import find_packages, setup


install_requires = [
    'django>=3.1',
    'wagtail>=2.12'
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
    version='0.4.1',
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
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Framework :: Wagtail :: 3',
        'Framework :: Wagtail :: 4',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)

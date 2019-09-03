import setuptools

install_requirements = [
    'requests>=2.21.0,<2.22.0',
    'clabe',
    'lxml',
]

# dataclasses is currently only builtin for 3.7. There is a backport on PyPi.
# There may be an official backport in the future, which is why we don't just
# check the python version.
try:
    import dataclasses
except ModuleNotFoundError:
    install_requirements.append('dataclasses')

test_requires = ['pytest', 'pytest-vcr', 'pycodestyle', 'pytest-cov',
                 'black', 'isort[pipfile]']

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='cepmex',
    version='0.1.3',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='CEP client library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/cep-python',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=install_requirements,
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)

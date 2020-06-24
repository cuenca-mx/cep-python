import setuptools

install_requirements = [
    'requests==2.24.0',
    'clabe==1.2.0',
    'lxml==4.5.1',
    'dataclasses>=0.6;python_version<"3.7"',
]

test_requires = (
    [
        'pytest==5.4.3',
        'pytest-vcr==1.0.2',
        'pytest-cov==2.10.0',
        'black==19.10b0',
        'flake8==3.8.3',
        'isort[pipfile]==4.3.21',
    ],
)

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
    ],
)

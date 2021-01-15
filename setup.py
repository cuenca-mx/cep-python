from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'cep/version.py').load_module()

install_requirements = [
    'requests==2.24.0',
    'clabe==1.2.0',
    'lxml==4.5.1',
    'dataclasses>=0.6;python_version<"3.7"',
]


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='cepmex',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='CEP client library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/cep-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cep=['py.typed']),
    python_requires='>=3.7',
    install_requires=install_requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

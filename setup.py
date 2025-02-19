from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'cep/version.py').load_module()


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
    python_requires='>=3.10',
    install_requires=[
        'requests>=2.32.0,<3.0.0',
        'clabe>=2.0.0,<3.0.0',
        'lxml>=5.3.0,<6.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

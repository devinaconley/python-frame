import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='framelib',
    version='0.0.5',
    author='Devin A. Conley',
    author_email='devinaconley@gmail.com',
    description='lightweight library for building farcaster frames using python and flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devinaconley/python-frames',
    packages=setuptools.find_packages(),
    package_data={
        'framelib': ['templates/*.html']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'eth-abi>=5,<6',
        'eth-hash[pysha3]',
        'eth-utils',
        'flask>=3,<4',
        'pydantic>=2,<3',
        'requests>=2,<3'
    ]
)

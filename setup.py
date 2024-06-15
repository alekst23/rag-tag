from setuptools import setup, find_packages

with open('req-light.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ragtag',
    version='0.1.0',
    author='ALeksandr Titarenko',
    author_email='alekst23@gmail.com',
    description='A RAG architecture with semantic tagging',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alekst23/rag-tag',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements
)

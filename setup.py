import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

requirements = [
        "numpy>=1.19.0",
        "pandas>=1.1.0"
    ]

setuptools.setup(
    name="piflib",
    version="0.1.1",
    author="CSIRO's DATA61",
    author_email="confidential.computing@data61.csiro.au",
    description="A library for computing the personal information factor (PIF)",
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/PIFtools/piflib',
    license='Apache',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    project_urls={
        'Documentation': 'http://piflib.readthedocs.io/',
        'Source': 'https://github.com/PIFtools/piflib',
        'Tracker': 'https://github.com/PIFtools/piflib/issues',
        'Discussion': 'https://github.com/PIFtools/piflib/discussions'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    tests_require=[
        "pytest>=5.0",
    ]
)

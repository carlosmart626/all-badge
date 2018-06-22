from setuptools import setup

from all_badge.__main__ import __version__

readme = open("README.rst").read()

tests_require = [
    "pytest==2.8.2",
    "pytest-cache==1.0",
    "pytest-cov==2.2.0",
    "pytest-pep8==1.0.6",
    "flake8==3.5.0",
]

setup(
    name="all_badge",
    version=__version__,
    description="Generate badges for Coverage.py, Git tags and custom.",
    author="Carlos Martinez",
    author_email="me@carlosmart.co",
    url="https://github.com/CarlosMart626/all-badge",
    packages=["all_badge"],
    zip_safe=True,
    include_package_data=True,
    license="MIT",
    keywords="coverage badge shield git custom badge styles",
    long_description=readme,
    entry_points={"console_scripts": ["all_badge = all_badge.__main__:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
    ],
    tests_require=tests_require,
)

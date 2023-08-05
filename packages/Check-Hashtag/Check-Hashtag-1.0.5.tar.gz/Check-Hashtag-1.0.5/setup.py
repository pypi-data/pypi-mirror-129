import os
import setuptools


def requirements(file="requirements.txt"):
    if os.path.isfile(file):
        with open(file, encoding="utf-8") as r:
            return [i.strip() for i in r]
    else:
        return []


def readme(file="README.md"):
    if os.path.isfile(file):
        with open(file, encoding="utf8") as r:
            return r.read()
    else:
        return ""


setuptools.setup(
    name="Check-Hashtag",
    version="1.0.5",
    description="Hashtag checker",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="Fayas Noushad",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    project_urls={
        "Tracker": "https://github.com/FayasNoushad/Check-Hashtag/issues",
        "Source": "https://github.com/FayasNoushad/Check-Hashtag"
    },
    python_requires=">=3.6",
    py_modules=['check_hashtag'],
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=requirements()
)

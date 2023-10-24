from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scramjet-framework-py",
    version='0.1.1',
    author="Scramjet.org",
    author_email="<info@scramjet.org>",
    description='Scramjet is a simple reactive stream programming framework.',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(exclude=["test"]),
    install_requires=[],
    keywords=['python', 'streams'],
    classifiers=[
    ]
)

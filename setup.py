from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="All_in_One_Secretary",
    version="0.1",
    description="Console bot for contacts and notes",
    long_description=open("README.md").read(),
    url="https://github.com/SergiiGoncharov13/project-All-in-One-Secretary",
    author="Sergii Goncharov, Vladislav Dzyadevich, Krystyna Kuzmenko, Olena Bogoliubova",
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "secretary = All_in_One_Secretary.main:main",
        ],
    },
)

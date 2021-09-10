import io

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="tui10s",
    version="1.0.0",
    license="BSD",
    maintainer="Dad",
    maintainer_email="johnrhutchinson@gmail.com",
    url='',
    description="Eat to tens",
    long_description=readme,
    package_dir={'': 'src'},
    packages=[''],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "black",
        "flake8",
        "pygame",
    ],
    extras_require={"test": ["pytest", "coverage"]},
)

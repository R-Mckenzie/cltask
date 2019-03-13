from setuptools import setup

setup(
    name='cltask',
    version='0.1',
    description='Simple command line task manager',
    author='Ross Mckenzie',
    author_email='rossmckenzie11@gmail.com',
    packages=["cltask"],
    entry_points={
        "console_scripts": ["task=cltask.task:main"]},
    install_requires=[],
)

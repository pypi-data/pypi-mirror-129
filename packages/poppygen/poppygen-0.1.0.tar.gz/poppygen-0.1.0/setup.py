import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='poppygen',
    version='0.1.0',
    url='',
    license='BSD-4',
    author='Timothy L.J. Stewart',
    author_email='me@tljstewart.ai',
    description='PopPyGen: Synthetic Human Population Generator for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",

    keywords='synthetic population, , human population, demographic',
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
        ],

    python_requires=">=3.9",
    packages=setuptools.find_packages(),
    install_requires=requirements
)

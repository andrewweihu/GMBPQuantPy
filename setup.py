import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmbp-quant",
    version="0.0.7",
    author="GMBP",
    author_email="admin@gmbpclub.com",
    license='MIT',
    description="GMBP Python Quant Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GMBPClub/GMBPQuantPy",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="."),
    package_data={'gmbp_quant': ['env_config.cfg']},
    python_requires=">=3.6",
    install_requires=[
        "gmbp-common",
        "bs4",
        "lxml",
        "requests",
        "requests-ntlm",
        "tqdm",
    ]
)

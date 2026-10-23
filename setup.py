from setuptools import setup, find_packages

setup(
    name="discord-chan-custom",
    version="2.5.0",
    description="Minimalist Pink Anime Theme & Studio Control Center for Discord",
    author="Discord-Chan Custom Team",
    packages=find_packages(),
    py_modules=["discord-chan-studio"],
    install_requires=[
        "pillow>=9.0.0"
    ],
    entry_points={
        "console_scripts": [
            "discord-chan-custom=studio:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)

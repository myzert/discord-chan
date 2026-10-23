from setuptools import setup, find_packages

setup(
    name="discord-chan-custom",
    version="2.6.0",
    description="Pixel Retro Anime Theme & Studio Control Center for Discord",
    author="Discord-Chan Custom Team",
    packages=find_packages(),
    py_modules=["discord-chan-studio"],
    install_requires=[
        "pillow>=9.0.0",
        "cairosvg>=2.7.0"
    ],
    entry_points={
        "console_scripts": [
            "discord-chan-custom=studio:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
)

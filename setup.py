from setuptools import setup, find_packages

setup(
    name="discord-chan-custom",
    version="2.6.0",
    description="Universal Anime Theme Customizer & Studio Dashboard for Discord",
    author="myzert",
    author_email="zerttcihuy@gmail.com",
    url="https://github.com/myzert/discord-chan",
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

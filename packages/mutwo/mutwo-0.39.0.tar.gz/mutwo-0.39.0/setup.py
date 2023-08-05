import setuptools  # type: ignore


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extras_require = {
    "midi": ["mido>=1.2.9, <2"],
    "reaper": ["rpp>=0.4, <0.5"],
    "abjad": [
        "abjad-ext-nauert>=3.4.0, <4",
        "abjad>=3.4.0, <4",
        "abjad-ext-rmakers>=3.4.0, <4",
    ],
}

extras_require.update({"all": list(extras_require.values())})  # type: ignore
extras_require.update(
    {"testing": ["nose", "pillow>=8.2.0, <9.0.0"] + extras_require["all"]}
)

setuptools.setup(
    name="mutwo",
    version="0.39.0",
    license="GPL",
    description="event based framework for generative art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Pauli,  Levin Eric Zimmermann",
    author_email="tim.pauli@folkwang-uni.de, levin.eric.zimmermann@posteo.eu",
    url="https://github.com/mutwo-org/mutwo",
    project_urls={"Documentation": "https://mutwo.readthedocs.io/en/latest/"},
    packages=[
        package for package in setuptools.find_packages() if package[:5] != "tests"
    ],
    setup_requires=[],
    install_requires=[
        "expenvelope>=0.6.5, <1.0.0",
        "primesieve>=2.0.0, <3.0.0",
        "numpy>=1.18, <2.00",
        "scipy>=1.4.1, <2.0.0",
        "natsort>=5.3.3, <6.0.0",
        "python-ranges>=0.2.0, <1.0.0",
    ],
    extras_require=extras_require,
    python_requires=">=3.9, <4",
)

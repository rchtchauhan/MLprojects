from setuptools import find_packages, setup

HYPEN_E_DOT = "-e ."

def get_requirements(path: str):
    requirements = []

    with open(path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name="mlproject",
    version="0.0.1",
    author="Rachit Chauhan",
    author_email="rchtchauhan@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="",
    version="1.0.0",
    author="Manish Dange",
    author_email="dangemanish35@gmail.com",
    description="⚡ One command Django project setup with DRF, CORS, dotenv & more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manish780386/djangoforge.git",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "djangoforge=djangoforge.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Topic :: Software Development :: Code Generators",
    ],
    keywords=["django", "setup", "boilerplate", "drf", "cors", "djangoforge"],
)
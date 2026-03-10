import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description=f.read()

_version="0.0.0"

Repo_NAME="TextSummarization-Project"
AUTHOR_USER_NAME="Harsha21261"
SRC_REPO="textsummarizer"
AUTHOR_EMAIL="entbappy73@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=_version,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Text Summarization APP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{Repo_NAME}",
    project_urls={
        "Bug Trackers":f"https://github.com/{AUTHOR_USER_NAME}/{Repo_NAME}/issues",
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src")
)
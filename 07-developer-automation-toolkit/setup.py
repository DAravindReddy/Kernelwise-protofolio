from setuptools import setup, find_packages

setup(
    name="kw-tools",
    version="1.0.0",
    description="Kernelwise Labs Developer Automation & Engineering Productivity Toolkit",
    author="Kernelwise Labs Engineering",
    author_email="engineering@kernelwiselabs.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kw-tools=kw_tools.cli:main",
        ],
    },
    python_requires=">=3.8",
)

import os
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


with open(os.path.join("peakrdl/regblock", "__about__.py"), encoding='utf-8') as f:
    v_dict = {}
    exec(f.read(), v_dict)
    version = v_dict['__version__']

setuptools.setup(
    name="peakrdl-regblock",
    version=version,
    author="Alex Mykyta",
    author_email="amykyta3@github.com",
    description="Generate SystemVerilog RTL that implements a register block from compiled SystemRDL input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SystemRDL/PeakRDL-regblock",
    packages=['peakrdl.regblock'],
    include_package_data=True,
    install_requires=[
        "systemrdl-compiler>=1.21.0",
        "Jinja2>=2.11",
    ],
    classifiers=(
        #"Development Status :: 5 - Production/Stable",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ),
    project_urls={
        "Documentation": "http://peakrdl-regblock.readthedocs.io",
        "Source": "https://github.com/SystemRDL/PeakRDL-regblock",
        "Tracker": "https://github.com/SystemRDL/PeakRDL-regblock/issues",
    },
)

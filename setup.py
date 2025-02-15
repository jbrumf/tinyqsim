from setuptools import setup, find_packages

from tinyqsim import __version__

setup(
    name='tinyqsim',
    version=__version__,
    packages=find_packages(),
    url='',
    license='MIT License',
    author='Jon Brumfitt',
    author_email='',
    description='Simulation of Quantum Computation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'url="https://github.com/jbrumf/tinyqsim"',
        'License :: OSI Approved :: MIT License'
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research'
    ],
    python_requires='>=3.12',
    install_requires=[
        'more-itertools',
        'numpy>=2',
        'matplotlib',
        'ipython',
        'ipympl',
        'scipy',
        'notebook',
        'pytest',
        'pdoc',
        'nb-clean'
    ]
)

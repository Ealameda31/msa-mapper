from setuptools import find_packages, setup

with open('requirements.txt') as r:
    requirements = r.read().splitlines()

with open('version.txt') as v:
    version = v.read()

setup(
    name='msa_mapper',
    install_requires=requirements,
    packages=find_packages(),
    version=version,
    author='Enrique M. Alameda-Basora',
    author_email='emalameda96@gmail.com',
    maintainer='Enrique M. Alameda-Basora',
    maintainer_email='emalameda96@gmail.com',
    url='https://ealameda31.github.io/msa-mapper/',
    description='Geocode locations and map coordinates to Metropolitan Areas',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Text Processing'
        ],
    platforms=['any'],
    keywords=['Geocoding', 'Map', 'Metropolitan Statistical Areas'],
    license='MIT'
)

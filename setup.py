from setuptools import setup, find_packages

setup(
    name='NekUpload',
    version='0.1.0',
    packages=find_packages(include=["NekUpload", "NekUpload.*"]),
    install_requires=[
        'iniconfig==2.0.0',
        'packaging==24.2',
        'pluggy==1.5.0',
        'pytest==8.3.4',
        'numpy',  # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            # Add your command line scripts here
            # Example: 'nek_upload=nek_upload.cli:main',
        ],
    },
    author='Stephen Liu',
    author_email='stephen.liu21@imperial.ac.uk',
    description='Upload pipeline for Nektar++ datasets into online database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shl211/NekUpload',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
)
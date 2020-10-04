from setuptools import setup, find_packages

setup(
        name='ArchiTop',
        version='0.1.4',
        author='Julian Brendel',
        author_email='julian.brendel@t-online.de',
        packages=find_packages(),
        url='http://pypi.python.org/pypi/PackageName/',
        license='LICENSE',
        description='Archidekt to TableTop export cli',
        long_description=open('README.md').read(),
        python_requires='>=3.8',
        install_requires=[
                "requests >= 2.24"
        ],
        entry_points={
                'console_scripts': ['archiTop=archiTop.__main__:main']
        },
        include_package_data=True
)

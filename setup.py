from setuptools import setup, find_packages

setup(
        name='ArchiTop',
        version='0.2.5',
        author='Julian Brendel',
        author_email='julian.brendel@t-online.de',
        packages=find_packages(),
        url='https://github.com/Julian-Brendel/archiTop',
        license='LICENSE',
        description='Archidekt to TableTop export cli',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        python_requires='>=3.8',
        install_requires=[
                "requests >= 2.24",
                "logging-spinner >= 0.2.2"
        ],
        entry_points={
                'console_scripts': ['archiTop=archiTop.__main__:main',
                                    'architop=archiTop.__main__:main']
        },
        include_package_data=True
)

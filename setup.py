from setuptools import setup, find_packages

setup(
        name='project0',
        version='1.0',
        url='https://github.com/siddhardha-maguluri/cs5293sp22-project0',
        project_urls={
            'Bug Reports': 'https://github.com/siddhardha-maguluri/cs5293sp22-project0/issues'
        },
        author='Siddhardha Maguluri',
        author_email='Siddhardha.Maguluri@ou.edu',
        packages=find_packages(exclude=('tests', 'docs')),
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
)

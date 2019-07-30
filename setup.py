from setuptools import setup, find_packages

setup(
    name='worldnews',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tldextract',
        'isoweek',
        'surt',
        'tqdm',
    ],
    author_email='lsingh@college.harvard.edu',
    description='Support for Wayback web, crawl collections analysis',
    keywords='Wayback, analysis, web collections',
)

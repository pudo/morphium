from setuptools import setup, find_packages

setup(
    name='morphium',
    version='0.1.3',
    description="Tools for scrapers on morph.io",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3'
    ],
    keywords='data scrapers',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/morphium',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
        'normality >= 0.2.2',
        'six >= 1.7.3',
        'boto3'
    ],
    tests_require=[],
    test_suite='tests',
    entry_points={}
)

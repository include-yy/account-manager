from setuptools import setup, find_packages


setup(
    name='yyam',
    version='0.1',
    packages=find_packages(),

    description="include-yy's account manager",
    author='include-yy',
    author_email='969041171@qq.com',
    url='https://github.com/include-yy/account-manager',
    license='MIT',
    install_requires=[
        'toml'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3',

    entry_points={
            'console_scripts': [
                'yyam = yyam:main'
            ]
    }
)

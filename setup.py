from setuptools import setup, find_packages


setup(
    name='windy',
    version='0.8.8',
    packages = find_packages(),
    entry_points={
        "console_scripts": ['windy = windy.gui.application:main'],
        'gui_scripts': ['windy = windy.gui.application:main', ]
        },
    description='windy is an application for managing Windows user/system environment variables.',
    url='http://github.com/zeljko.m.gavrilovic/windy',
    author='BigNumbers',
    author_email='zeljko.m.gavrilovic@gmail.com',
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft :: Windows",
      ],
    keywords=["windows", "environment", "variables", "path", "developer", "java"],
    zip_safe=False
    )

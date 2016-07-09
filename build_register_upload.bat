# build: zip, installer using python setup.
# build: stanalone exe using pythonintsaller.
# register the user
# upload zip and installer to pypi package repository
pyinstaller.exe --onefile --windowed --icon=windy.ico windy.spec
python setup.py sdist bdist_wininst register upload
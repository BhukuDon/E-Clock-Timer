import PyInstaller.__main__
import os,shutil
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    "--clean",
    "--name=E Clock",
    "--icon=assets\image\icon.ico",
    "--distpath=",

])

os.remove("E Clock.spec")
shutil.rmtree("build")
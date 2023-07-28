import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["pygame", "os", "random", "re", "sys"],
    "excludes": ["tkinter"],
}
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Tavern 21",
    version="2.0",
    description="Card-Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
    targetName="tavern-21.exe"
)
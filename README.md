# LoloSnake

You will see a quickly programmed variant of the classic Snake. There are heaps of better implementations, but this first experience with Pygames was great fun ;)

I deliberately left out the restrictions by walls.

 ![Preview](preview.png)
# How to play (on Windows)
Simply open the main.exe

# How to install

1. Install Python3
2. Install all Packages
                    
        pip install pygames
        pip install tkinter
        pip install numpy

# How to build excecutable
        pyinstaller main.oy --onefile --noconsole

Copy the executable file to the root directory. Alternatively you can include the used files (sounds) when calling pyinstaller.
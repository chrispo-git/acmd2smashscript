import os
import sys
import time

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
if len(sys.argv) > 1:
  folder = str(sys.argv[1])
else:
  folder = filedialog.askdirectory()

command = 'py acmd2smashscript.py'

for root, dirs, files in os.walk(folder, topdown=False):
   for name in files:
    next_file = os.path.join(root, name)
    if next_file[-1] == "s" and next_file[-2] == "r" and next_file[-3] == ".":
      if folder[0] == folder[-1] and folder[0] == '"':
        stream = os.popen(f'{command} {next_file} {next_file}')
      else:
        stream = os.popen(f'{command} "{next_file}" "{next_file}"')
      output = stream.read()
      output
      print(f"{next_file} converted")
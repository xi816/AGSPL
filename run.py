import os
import sys
import platform

if platform.name == "Linux":
  os.system("python cparse.py")
elif platform.name == "Windows":
  os.system("python3 cparse.py")
else:
  try: os.system("python3 cparse.py")
  except: os.system("python cparse.py")

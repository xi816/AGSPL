import os
import sys
import platform

if platform.uname == "Linux":
  os.system(f"python3 cparse.py -a {sys.argv[1]}")
elif platform.uname == "Windows":
  os.system(f"python cparse.py -a {sys.argv[1]}")
else:
  try: os.system(f"python3 cparse.py -a {sys.argv[1]}")
  except: os.system(f"python cparse.py -a {sys.argv[1]}")


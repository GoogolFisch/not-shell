import json
import sys
import color

color.init()
if sys.platform.startswith("linux") or sys.platform == "darwin":
    Men = __import__("Lin")
elif sys.platform in ("win32", "cygwin"):
    Men = __import__("Win")
else:
    print("Error");exit(1)

shortcuts = None
with open(sys.argv[0][:-7]+"shortcuts.json") as f:
    shortcuts = json.load(f)

a = Men.Main(sys.argv[1:],shortcuts)
a.run()
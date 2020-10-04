#import subprocess
#subprocess.Popen(r"F:\Program Files (x86)\Steam\Steam.exe -applaunch 322170")
#print("Hello lol")
import re

string = "steam://504230"
regex = re.compile(r"steam:\/\/([0-z]+)")
m = regex.search(string)
print(m.group(1))  # 504230

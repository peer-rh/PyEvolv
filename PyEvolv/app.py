from PyEvolv.main import PyEvolv
import json
from pathlib import Path

def main():
    
    constants = json.loads(open(str(Path.home()) + "/.pyevolv/constants.json").read())
    
    pe = PyEvolv(800, 650, constants)
    pe.run()

if __name__=="__main__":
    main()
from db import *
from localSettings import *

'''roboczy plik do różnych testów'''

def main():
	d = DBInterface()
	print("Hello World!")
	print(CSVpath)
	d.CSVparseMeasurements()
  
if __name__== "__main__":
  main()

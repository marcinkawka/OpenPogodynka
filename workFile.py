from db import *
from localSettings import *

def main():
	d = DBInterface()
	print("Hello World!")
	print(CSVpath)
	d.CSVlistHydroGauges()
  
if __name__== "__main__":
  main()

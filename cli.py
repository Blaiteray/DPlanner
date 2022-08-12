#pyinstaller --onefile -w --hiddenimport=babel.numbers cli.py
from src.main import main

if __name__ == '__main__':
	main()
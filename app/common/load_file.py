import os
import json


def load_file():
	with open('app/assets/files.json', 'r') as files:
		file = json.load(files)
		return file
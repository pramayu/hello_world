import os
from selenium import webdriver
from dotenv import load_dotenv
from app.common.user_input import user_input
from app.common.load_file import load_file
from app import SetupCreateFile
load_dotenv()


rs = user_input()
if rs['status'] == True:
	files = load_file()
	if files:
		path = 'app/assets/geckodriver'
		# path = 'app/assets/chromedriver'
		driver = webdriver.Firefox(executable_path=path)
		# driver = webdriver.Chrome(path)
		driver.maximize_window()
		setup = SetupCreateFile(rs['username'], rs['password'], files, driver, rs['panel'])
		login_rs = setup.user_login()
		if login_rs == True:
			setup.process_file()
		else:
			print("Somethings wrong")
	else:
		print("Something wrong")
else:
	print("Something wrong")
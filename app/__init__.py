import os
import csv
import time
from tqdm import tqdm
from datetime import datetime
from selenium.webdriver.common.keys import Keys


class SetupCreateFile():
	def __init__(self, username, password, files, driver, panel=None):
		self.username 	= username
		self.password 	= password
		self.driver 	= driver
		self.files 		= files
		self.panel 		= panel

	def user_login(self):
		try:
			self.driver.get(os.getenv('LOGIN_LINK'))
			self.driver.find_element_by_name("email").send_keys(self.username)
			self.driver.find_element_by_name("password").send_keys(self.password)
			self.driver.find_element_by_class_name("btn-primary").click()
			return True
		except Exception as e:
			return False

	def choose_service(self, lt_service):
		time.sleep(2)
		fr_service = self.driver.find_element_by_id("tdserviceinfo1").text
		fl_service = fr_service.split()[0]
		if len(lt_service) == 2:
			sd_service = self.driver.find_element_by_id("tdserviceinfo2").text
			fl_service = f"{fl_service},{sd_service.split()[0]}"
		return fl_service

	def choose_odppanel(self):
		kap = self.driver.find_elements_by_css_selector("td.column_number a")[0].text
		self.driver.find_element_by_link_text(f"{kap}").click()
		time.sleep(1)
		if self.panel == '1':
			fl_panel = self.driver.find_elements_by_css_selector("tr.odd td")[0].text
			rn_panel = "-".join(fl_panel.split("-")[:-1])
			return rn_panel
		if self.panel == '2':
			fl_panel = self.driver.find_elements_by_css_selector("tr.even td")[0].text
			rn_panel = "-".join(fl_panel.split("-")[:-1])
			return rn_panel

	def collect_odpport(self, odp_name):
		self.driver.get(os.getenv('ODP_LINK'))
		time.sleep(2)
		self.driver.find_elements_by_id("filter")[5].click()
		self.driver.find_elements_by_id("deviceLocation")[0].send_keys(odp_name)
		self.driver.find_elements_by_id("deviceLocation")[0].send_keys(Keys.ENTER)
		time.sleep(1)
		rn_panel = self.choose_odppanel()
		return rn_panel

	def create_file(self, fl_service, rn_panel, port, service):
		sfx_name = datetime.now().strftime("%Y%m%d%H%M%S")
		filename = f"UPDATE_STP_IMMEDIATE_{sfx_name}.csv"
		pathfile = os.getcwd()+'/app/output/'+filename
		with open(pathfile, 'w', newline='') as file:
			thewriter = csv.writer(file, delimiter='|')
			thewriter.writerow(['SERVICE_NAME','SERVICE_NUMBER','ODP_PANEL','PORT_NAME'])
			chk_service = f'0{service}' if service[0] == '3' else service
			thewriter.writerow([f'{fl_service}',f'{chk_service}',f'{rn_panel}',f'{rn_panel}-{port}'])
		time.sleep(6)
		pathfile = os.getcwd()+'/app/output/'+filename
		self.driver.get(os.getenv('UPLOAD_LINK'))
		self.driver.find_elements_by_class_name("select2-selection")[0].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		time.sleep(5)
		self.driver.find_elements_by_class_name("select2-selection")[1].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		time.sleep(2)
		file_input = self.driver.find_element_by_name("file")
		file_input.send_keys(pathfile)
		time.sleep(2)
		self.driver.find_elements_by_class_name("btn-warning")[1].click()
		time.sleep(2)

	def collect_service(self, service, odp_name, port):
		time.sleep(3)
		self.driver.get(os.getenv('SERVICE_LINK'))
		self.driver.find_element_by_id('servid').clear()
		if service[0] == '3':
			self.driver.find_element_by_id('servid').send_keys(f"0{service}")
		else:
			self.driver.find_element_by_id('servid').send_keys(service)
		self.driver.find_element_by_id('servid').send_keys(Keys.ENTER)
		time.sleep(3)
		lt_service = self.driver.find_elements_by_name("selecteds")
		fl_service = self.choose_service(lt_service)
		time.sleep(1)
		rn_panel = self.collect_odpport(odp_name)
		if len(rn_panel) != 0:
			self.create_file(fl_service, rn_panel, port, service)

	

	def process_file(self):
		loop = tqdm(total = len(self.files))
		for file in self.files:
			try:
				self.collect_service(file['SERVICE'], file['ODP'], file['PORT'])
				loop.set_description(f"Latest Service {file['SERVICE']}".format(file))
				loop.update(1)
			except Exception as e:
				print(e)
				pass
				

	
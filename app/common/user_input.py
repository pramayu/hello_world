def user_input():
	rs 			= {'status': False}
	username 	= input("Username: ")
	password 	= input("Password: ")
	print("--Select option--")
	print("Input 1 for update service")
	print("-or-")
	print("Input 2 for check bulk status")
	print("--------------------------------")
	option 		= input("Option: ")
	if option == '1':
		print("--Select panel--")
		panel = input("Input panel 1 or 2: ")
	if option == '2':
		date_bulk = input("Input bulk date, exp: 18-Feb-2020: ")
		push_resl = open("app/assets/result.json", "a+")
	if username and password and option:
		rs = {
			'status'	: True,
			'username'	: username,
			'password'	: password,
			'option'	: option,
			'panel'		: panel if option == '1' else '',
			'date_bulk'	: date_bulk if option == '2' else '',
			'push_resl'	: push_resl if option == '2' else ''
		}
		return rs
	else:
		return rs
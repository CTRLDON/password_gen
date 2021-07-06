import random
import string
import sqlite3
import time
import pandas as pn


def save_pass(account , pass_detaill):
	cr.execute(f"INSERT INTO PASSWORD values('{account}' , '{pass_detaill}')")
	cr.execute("SELECT password FROM PASSWORD")
	all_passwords = cr.fetchall()
	if pass_detaill in all_passwords:
		print("\nyour password saved succefully")
	db.commit()
	print(pass_detaill)

def gen_pass():

	password = ""
	for num in range(int(pass_len)):
		password += str(random.choice(chars_list))

	return password

def delete_pass():
	cr.execute("SELECT account FROM PASSWORD")
	accounts_res = cr.fetchall()
	names_nums = {}
	for num , name in enumerate(accounts_res):
			names_nums[num] = name
			print(f"{num} for {name}")
	select_input = input("what do you want to delete : ")
	for key in names_nums.keys():
		if int(select_input) == key:
			selected = names_nums.get(key)
			cr.execute(f"DELETE FROM PASSWORD where account = '{selected}'")
			db.commit()
			cr.execute(f"SELECT password FROM PASSWORD")
			refreshed_res = cr.fetchall()
			if selected not in refreshed_res :
				print("\nThe Password Deleted Succefully")
				time.sleep(2)
				break

def select_pass():
	cr.execute("SELECT account FROM PASSWORD")
	accounts_res = cr.fetchall()
	names_nums = {}
	for num , name in enumerate(accounts_res):
			names_nums[num] = name
			print(f"{num} for {name}")
	select_input = input("what do you want to select : ")
	for key in names_nums.keys():
		if int(select_input) == key:
			selected = names_nums.get(key)
			cr.execute(f"SELECT password FROM PASSWORD where account = '{selected}'")
			print(cr.fetchone())
			input("Press any key to exit : ")
			break

def select_all():
	cr.execute("SELECT password FROM PASSWORD")
	all_passwords = cr.fetchall()
	cr.execute("SELECT account FROM PASSWORD")
	all_accounts = cr.fetchall()

	table_data = {"accounts" : all_accounts,
	"passwords" : all_passwords}

	passwords_table = pn.DataFrame(table_data)
	print(passwords_table)
	input("Press any key to exit : ")

def own_password():
	password_input = input("Enter here your password : ")
	account_input = input("this password for which account? : ")
	cr.execute("SELECT account FROM PASSWORD")
	all_accounts = cr.fetchall()
	cr.execute("SELECT password FROM PASSWORD")
	all_passwords = cr.fetchall()
	for account in all_accounts:
		for password in all_passwords:
			if account == account_input or password == password_input:
				print("account name or password is already exists , try again")
				time.sleep(2)
				break
			else:
				cr.execute(f"INSERT INTO PASSWORD values('{account_input}' , '{password_input}')")
				db.commit()
				cr.execute("SELECT account FROM PASSWORD")
				refreshed_accounts = cr.fetchall()
				cr.execute("SELECT password FROM PASSWORD")
				refreshed_passwords = cr.fetchall()
				if account_input in refreshed_accounts or password_input in refreshed_passwords:
					print("Password Succefully saved")
					time.sleep(3)
					break
				else:
					print("oh , there is a problem try again")
					time.sleep(2)
					break
		break


db = sqlite3.connect("passwords.db")
db.row_factory = lambda cursor, row: row[0]

cr = db.cursor()
cr.execute("CREATE TABLE IF NOT EXISTS PASSWORD(account text , password text)")

chars_list = [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9]

for char in string.ascii_letters:
	chars_list.append(char)
		
try:
	while True:
		print("\nwelcome to my password generator \n here you can create or even save your passwords \n a for add \n d for delete \n s for showing password \n sa for showing all passwords \n c for creating your own password \n e for exit")
		user_input = input("\nwhat do you want to do : ")

		if user_input.lower() == "a":
			pass_len = input("\nThe lengh of the password : ")

			account_name = input("\nWhat is this password for : ")
			cr.execute("SELECT account FROM PASSWORD")
			accounts = cr.fetchall()
			if account_name.lower() in accounts :
				print("\nEnter another Account name")
				time.sleep(3)
				continue

			while True:
				pass_nums = []
				pass_letters = []
				res = gen_pass()
				for char in str(res):
					if char.isnumeric():
						pass_nums.append(char)
					else:
						pass_letters.append(char)
				if len(pass_nums) == int(pass_len)/2 :
					save_pass(account_name.lower() , str(res))
					time.sleep(4)
					break

		if user_input.lower() == "d":
			delete_pass()

		if user_input.lower() == "e":
			db.close()
			break
		if user_input.lower() == "s":
			select_pass()

		if user_input.lower() == "sa":
			select_all()

		if user_input.lower() == "c":
			own_password()
except sqlite3.DatabaseError as e:
	print("\nthere is an error")
	time.sleep(1)
	print(e)

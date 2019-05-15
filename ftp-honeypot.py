#!/usr/bin/python3

import socket
from threading import Thread
from datetime import datetime

users = {}
HOST = ''
PORT = 42069

def init_user_conf():
	f = open('users.conf', 'r')
	user_conf_lines = f.read().split('\n')
	for user_conf_line in user_conf_lines:
		split_line = user_conf_line.split(':')
		if len(split_line) >= 2:
			username = split_line[0]
			password = split_line[1]
			users[username] = password



def init_server_conf():
	f = open('server.conf', 'r')
	server_conf_lines = f.read().split('\n')
	for server_conf_line in server_conf_lines:
		split_line = server_conf_line.split('=')
		if len(split_line) >= 2:
			conf_variable = split_line[0]
			conf_variable_value = split_line[1]
			if conf_variable == 'PORT':
				PORT = int(conf_variable_value)
			elif conf_variable == 'HOST':
				if conf_variable_value == 'DEFAULT':
					pass
				else:
					HOST = str(conf_variable_value)

def clientThread(conn, connip):
	currentDir = "/"
	isLoggedIn = False
	isRecivingPassword = False
	user_to_login = ""
	log_msg = ""
	while True:
		conn_data = conn.recv(1024).decode()
		if isLoggedIn == False and conn_data.startswith('USER'):
			user_to_login = conn_data[5:]
			conn.sendall('331 Please specify the password.\n'.encode())
			isRecivingPassword = True
		elif isRecivingPassword == True:
			if conn_data.startswith('PASS'):
				user_to_login = user_to_login.replace('\n', '').replace('\r', '')
				password = conn_data[5:].replace('\n', '').replace('\r', '')
				if user_to_login in users.keys() and not(user_to_login == '*'):
					if users[user_to_login] == password:
						conn.sendall('230 Login successful.\n'.encode())
						log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + " and password:" + password + " SUCCESSFUL."
					elif users[user_to_login] == '*':
						conn.sendall('230 Login successful.\n'.encode())
						log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + " and password:" + password + " SUCCESSFUL."
					else:
						conn.sendall('530 Incorrect Login.\n'.encode())
						log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + ' and password:' + password + ' FAILED.'
				elif '*' in users.keys():
					if users['*'] == password:
						conn.sendall('230 Login successful.\n'.encode())
						log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + " and password:" + password + " SUCCESSFUL."
					else:
						conn.sendall('530 Incorrect Login.\n'.encode())
						log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + ' and password:' + password + ' FAILED.'
				else:
					log_msg = 'Login from IP: ' + connip + ' with username:' + user_to_login + ' and password:' + password + ' FAILED.'
					conn.sendall('530 Incorrect Login.\n'.encode())

			if not(log_msg == ''):
				print(log_msg)
			log_msg = ''
			isRecivingPassword = False



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def init_ftp_server():
	s.bind((HOST, PORT))

	s.listen(50)
	print("FTP Honeypot running.")
	while 1:
		conn, addr = s.accept()
		print("client logged in from IP:" + str(addr[0]) + ":" + str(addr[1]))
		conn.sendall("220 (vsFTPd 3.0.3)\n")
		Thread(target=clientThread, args=(conn, str(addr[0]),).start())


def getDateTime():
	now = datetime.now()
	currentDateTime = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
	return currentDateTime


if __name__ == '__main__':
	print('Starting logging, Date (DD/MM/YY): ' + getDateTime() + "\n")
	print("configuring server settings...")
	try:
		init_server_conf()
	except Exception as e:
		print("FAILED: " + str(e))
	print("configuring FTP users...")
	try:
		init_user_conf()
	except Exception as e:
		print("FAILED: " + str(e))
	REAL_HOST = HOST
	if REAL_HOST == '':
		REAL_HOST = '*'
	print("Starting FTP Honeypot on: " + REAL_HOST + ":" + str(PORT) + "...")
	try:
		init_ftp_server()
	except Exception as e:
		print("FAILED: " + str(e))

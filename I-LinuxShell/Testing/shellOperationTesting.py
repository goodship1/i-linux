
import os
import cmd
import time
import datetime
import subprocess
from ErrorHandling import Errors
from  subprocess import check_output

class ShellOperations(cmd.Cmd ,object):
	
	def __init__(self):
		self._e = Errors()#instance of errors
			
	
	def do_cur(self,line):
		"""current returns current working directory"""
		return os.getcwd()#prints the current working directory 
		
	def do_tod(self):
		""" tod return current time and date"""
		unix_time = time.time()#gets unix time stamp
		date_conversion = '%Y-%m-%d %H:%M:%S'#converting unix time stamp
		return datetime.datetime.fromtimestamp(unix_time).strftime(date_conversion)#printing date and time in format of '%Y-%m-%d %H:%M:%S'
	
	def checkiflineisEmpty(self,line):
		empty = ['']
		return line == empty[0]
	
	def formattingCurrentWorkingDirectory(self):
		files = self.current_return()
		files = files.split('/')
		files.remove(files[0])
		return files
		
	def do_cdir(self,line):
		""" cdir changes the file directory"""
		files = os.getcwd()
		files = files.split('/')
		files = files.remove(files[0])
		if(self.checkiflineisEmpty(line)):#if line is empty line 
			try:
				raise Exception(self.e.empty_line())
			except Exception as err:
				return (self.e.empty_line(),True)
				
		elif(line in files)and(os.getcwd()!=line):
				while(True):
					self.do_bdir(line)#call to do_bdir(line)
					if(line==line):
						return line
						break
		
		elif(line not in files):
			try:
				os.chdir(line)#change file directory
			except Exception as err:
				print self.e.no_directory_found()#print exception
	
			
	def get_home(self):
		""" funcution to check if in home directory"""
		return os.getcwd()=="home"	
	
	def checkIfFile(self,line):
		return os.path.isfile(line)
		
	def current_return(self):
		""" returns current directory
		function used to get back to home"""
		return os.getcwd()
	
	
	def do_h(self,line):
		""" h gets to home directory"""
		files = os.getcwd()
		files  =  files.split('/')
		files.remove(files[0])
		find  = files.index('home')#find the index value of home
		counter = len(files)
		while(True):#while true
			self.do_bdir(line)#calls the bdir method 
			counter-=1#decerement count by one each time
			if(counter==find):
				break
		os.chdir('home')#changes the directory
		return True
	
	def do_get(self,line):
		""" get packages"""
		if(self.checkiflineisEmpty(line)):#if line is empty 
			try:
				raise Exception(self._e.empty_line())
			except Exception as err:
				return self._e.empty_line()
		if(self.checkiflineisEmpty(line)==False):#if true
			try:
				connection = check_output("ping -c 1 www.google.com",shell=True)
				if(line=="update"):#checks if line is update then update
					os.system("sudo apt-get update")
					return True
				else:# else try install line 
					os.system("sudo apt-get install %s"%line)
					return True
			except subprocess.CalledProcessError as  err:
				return err
		
	def do_cw(self,line,lineTwo):
		if(self.checkIfFile(line)):#checks if line is a file
			File = open(line).read()#opens file for read
			File = File.splitlines()#splits files at new lines
			count  = len(File)#counts len of file
			return count
		else:
			#error handling if line is not a file
			try:
				raise Exception(self.e.not_file())
			except Exception as Err:
				return Err
			
	
	def do_cl(self): 
		""" cl clears the terminal screen"""
		os.system('clear')#clears the terminal screen 
		
	def do_bl(self,line):
		"""bl lists files which are in the current working directory"""
		files = os.listdir(os.getcwd())#stores current directory and list of files in working direcotry 
		return(files)#lists the directory
			
	def do_bll(self):
		"""bll lists access of files and files of the current working directory"""
		files = os.listdir(os.getcwd())#gets the list of directorys in current
		for x in range(len(files)):
			#refactor
			if(os.access(files[x],os.R_OK == True)and(os.access(files[x],os.W_OK)==True) and(os.access(files[x],os.X_OK)==True)):
				print files[x] +"R_W_X"
			elif(os.access(files[x],os.R_OK)==False)and(os.access(files[x],os.W_OK)==False)and(os.access(files[x],os.X_OK)==True):
				print files[x]+"no access"
			elif(os.access(files[x],os.R_OK)==True)and(os.access(files[x],os.W_OK)==False)and(os.access(files[x],os.X_OK)==False):
				print files[x]+"R"
			elif(os.access(files[x],os.R_OK)==False)and(os.access(files[x],os.W_OK)==True)and(os.access(files[x],os.X_OK)==True):
				print files[x]+"R"
			elif(os.access(files[x],os.R_OK)==False)and(os.access(files[x],os.W_OK)==False)and(os.access(files[x],os.X_OK)==True):
				print files[x] + "X"
			elif(os.access(files[x],os.R_OK)==True)and(os.access(files[x],os.W_OK)==True)and(os.access(files[x],os.X_OK)==False):
				print files[x]+" " + "R_W"
			elif(os.access(files[x],os.R_OK)==False)and(os.access(files[x],os.W_OK)==True)and(os.access(files[x],os.X_OK)==True):
				print files[x]+ +" "+"X_W"
			elif(os.access(files[x],os.R_OK)==True)and(os.access(files[x],os.W_OK)==True)and(os.access(files[x],os.X_OK)==False):
				print files[x]+"R_W"
			elif(os.access(files[x],os.R_OK)==False)and(os.access(files[x],os.W_OK)==True)and(os.access(files[x],os.X_Ok)==False):
				print files[x]+"W"
				
	def do_show(self,line):
		""" show files to user press Q to leave"""
		if(self.checkIfFile(line)):#checks if line is a file
			File = open(line).read()#opens and reads files 
			os.system('less %s'%line)#calls the less linux command
			return True
		else:#else throw error 
			try:
				raise Exception(self._e.not_file())
			except Exception as err:
				return self._e.not_file() 
				
	def do_cw(self,line):
		""" cw counts words of a file"""
		count = 0#count variable
		if(self.checkIfFile(line)):#checks if line is a file
			files = open(line).read()#opens line file for read
			for x in files.split():#splits at whitespaces
				count+=1#increments count by each iteration
			return count #prints count
		else:
			try:
				raise Exception(self._e.not_file())#raise not file exception 
			except Exception as err:#catch error
				return self._e.not_file()#prints error in terminal
	
	
	def do_cat(self,line):
                self.cats = {}
                self.arguments = []
                if(line == ""):
                        while(True):
                                user_cat = raw_input(">>")
                                if(user_cat == 'b'):
										return True
										break
                if(line != "")and(">" in line):
                        while(True):
                                user_cat = raw_input(">>")
                                self.arguments.append(user_cat)
                                if(user_cat == 'b'):
                                        break
                        self.arguments.remove('b')
                        return "%s = %s"%(line[2],self.arguments)
	
	
	
	def do_bdir(self,line):
		"""bdir moves back one directory"""
		os.chdir(os.path.pardir)#moves back one directory in linux system 




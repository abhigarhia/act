import os
import sys
import re

class ParseCommentClass: # Class for parsing.  

	def __init__(self):
		
		self.Icomments = []
		self.Ecomments = []

	def parseComment(self,comment_class, r_comment_class): # definition for parsing
		
		self.parseIncludeClass(comment_class)
		self.parseExcludeClass(r_comment_class)

		return self.Icomments,self.Ecomments
	
	def parseIncludeClass(self,cc): # definition for parsing including classes.

		if cc == '*':
			self.Icomments.append('all')

		elif cc.find('-') != -1:

			start_CC,end_CC = cc.split('-')[0],cc.split('-')[1]
			
			for com in range(ord(start_CC),ord(end_CC)+1):
				self.Icomments.extend(chr(com))

		
		elif cc.find(',') != -1:
			self.Icomments.extend(cc.split(','))

		
		else:
			self.Icomments.extend(cc)


	def parseExcludeClass(self,rcc):	# definition for excluding classes
		
		if rcc.find('-') != -1:

			start_CC,end_CC = rcc.split('-')[0],rcc.split('-')[1]
			
			for com in range(ord(start_CC),ord(end_CC)+1):
				self.Ecomments.extend(chr(com))

		
		elif rcc.find(',') != -1:
			self.Ecomments.extend(rcc.split(','))

		
		else:
			self.Ecomments.extend(rcc)
				

class act(ParseCommentClass): # acting class.
	
	def __init__(self):
		self.file_name = ''
		self.comment_class = ''
		self.rcomment_class = ''

	def getArg(self): # definition for getting arguments.

		self.file_name = sys.argv[1]

		try:
			self.comment_class = sys.argv[2]
			self.rcomment_class = sys.argv[3]

		except IndexError:
			pass	

	def removeClass(self,curr_directory): #definition for removing comments.

		icc,rcc = ParseCommentClass().parseComment(self.comment_class,self.rcomment_class)

		file = open(curr_directory+"\\"+self.file_name,'r')
		data = file.read()

		if icc[0] == 'all':
			lrcc = ''.join(rcc)
			try:
				data = self.removeMLC(data,'A1',xp = rcc)
				data = self.removeSLC(data,'A1',xp = lrcc)

			except:

				data = self.removeMLC(data,'A0')
				data = self.removeSLC(data,'A0')

		else:	
			
			for comm in icc:
				if not(comm in rcc):
					
					try:
						data = self.removeMLC(data,'I0',xp = comm)
						data = data.replace('#'+comm+' ','')
					
					except:
						pass	
		file.close()
 		
		file = open(curr_directory+'\~'+self.file_name,'w')
		file.write(data)
		file.close()
		self.file_name = '~'+self.file_name
		self.execScript(curr_directory)	
		os.remove(curr_directory+"\\"+self.file_name)	

	def removeSLC(self,data,status,xp = None): # removing single comments class.

		if status == 'A0':
			data = re.sub(r'#[a-zA-Z0-9]\s','',data)

		elif status == 'A1':
			data = re.sub(r'#[^'+xp+']\s','',data)

		else:
			pass	

		return data

	def removeMLC(self,data,status,xp = None): # removing multiline comments class.

		if status == 'A0':
			data = re.sub(r"[\''']+[a-zA-Z0-9]\s",'',data)
			data = data.replace("\'\'\'",'')

		elif status == 'A1':
			s = ''.join(xp)
			rpos = 0
			rdata = data[::-1]
			
			while True: # removing second part of the comment.
				
				pos = rdata.find("\'\'\'",rpos)
				if pos == -1:
					break
				rpos = rdata.find("\'\'\'",pos+1)
				
				if not(rdata[rpos-1] in xp):
					rdata = rdata[:pos]+rdata[pos+3:]
						
				else:
					rpos +=1		
			
			data = rdata[::-1]		
			data = re.sub(r"\'\'\'[^"+s+"]\s",'',data) # removing first part of comments.
			
			spos = 0
			while True: # This loop remove starting of non-class comments.
				
				pos = data.find("\'\'\'",spos)
				
				if pos == -1:
					break

				if data[pos+3] !=' ' and data[pos+4] == ' ':
					spos += 1
					pass
				
				else:
					while True:
						if data[pos+3] == ' ':
							data = data[:pos+3]+data[pos+4:]
						else:
							break	
					data = data[:pos]+data[pos+3:]
			
		else:
			pos = data.find("\'\'\'"+xp+' ')
			if pos != -1:
				data = data.replace("\'\'\'"+xp+' ','')
				pos = data.find("\'\'\'",pos+1)
				data = data[:pos]+data[pos+3:]

		return data

	def getStatus(self): # checking status for the passed parameters.

		self.getArg()
		
		if self.comment_class:
			return True

		return False

	def execScript(self,curr_directory):
		os.system('python '+curr_directory+"\\"+self.file_name)
	

curr_directory = os.getcwd()

if __name__ == '__main__':
	obj = act()
	
	if obj.getStatus():
		obj.removeClass(curr_directory)	

	else:
		obj.execScript(curr_directory)		
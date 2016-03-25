#coding:utf8

import requests
from PIL import Image
from StringIO import StringIO
import re

class Download(object):

	def __init__(self, year, user, passwd):
		self.year = year
		self.user = user
		self.passwd = passwd
		self.queue = []
		self.filename = []
		self.header = {
			'Host' : 'inter.jingningsms.com',
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
			'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding' : 'gzip, deflate',
			'Cookie' : '浏览器去查找',
			'Connection' : 'keep-alive',
		}
		self.cookies = self.login()

	def get_code(self):
		code = r'http://inter.jingningsms.com/Account/VerificationCode'
		response = requests.get(code, headers = self.header)
		i = Image.open(StringIO(response.content))
		i.save(open('code.png', 'wb'))
		i.show()

	def login(self):
		self.get_code()
		code = raw_input('code:')
		url = r'http://inter.jingningsms.com/Account/LogOn/'
		data = {
			'year_Value' : str(self.year),
			'year' : str(self.year),
			'year_SelIndex' : '0',
			'UserName' : self.user,
			'Password' : self.passwd,
			'VerificationCode' : code,
			'ReturnUrl' : '/',
			'year_Value' : str(self.year),
			'year' : str(self.year),
			'year_SelIndex' : str(2015-self.year),
			'UserName' : self.user,
			'Password' : self.passwd,
			'VerificationCode' : code
		}
		try:
			r = requests.post(url, data = data, headers = self.header)
			print 'successful'
			print r.text
		except:
			print 'error'
		return r.cookies

	def get_head(self):
		url = r'http://inter.jingningsms.com/?year=%d&_dc=1458829224850&submitDirectEventConfig=%%7B%%22config%%22%%3A%%7B%%22__EVENTTARGET%%22%%3A%%22ctl00%%24ctl00%%22%%2C%%22__EVENTARGUMENT%%22%%3A%%22Scorelist%%7Cpostback%%7Cnodeload%%22%%2C%%22extraParams%%22%%3A%%7B%%22node%%22%%3A%%22root%%22%%7D%%7D%%7D' % self.year

		header={
			'Host' : 'inter.jingningsms.com',
			'Proxy-Connection' : 'keep-alive',
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
			'X-Requested-With' : 'XMLHttpRequest',
			'X-Ext.Net' : 'delta=true',
			'Accept': '*/*',
			'Referer' : 'http://inter.jingningsms.com/?year=2015',
			'Accept-Encoding' : 'gzip, deflate, sdch',
			'Accept-Language' : 'zh-CN,zh;q=0.8}'
		}		
		try:
			response = requests.get(url, cookies = self.cookies, headers = header)
		except:
			self.cookies = self.login()
			try:
				response = requests.get(url, cookies = self.cookies, headers = header)
			except:
				return False
		text = response.text
		pattern = r'&grade_id=(\w+)&class_id=(\w+)&exam_id=(\w+)'

		s = text.split(',')
		for i in s:
			sp = i.split(':')
			if(sp[0] == 'href'):
				href = sp[1][1:-1]
				f = re.findall(pattern, href)[0]
				filename = "%02d_%02d_%d_%d.json" % (int(f[0])/10, int(f[1]), self.year, int(f[2]))
				self.queue.append(href)
				self.filename.append(filename)

	def get_all(self):
		self.get_head()
		for i in range(len(self.queue)):
			url = r'http://inter.jingningsms.com/ScoreList/ScoreListByClass/?year=%d' % (self.year) + self.queue[i]
			filename = self.filename[i]
			print filename,
			print '%03d/%03d' % (i+1, len(self.queue)),
			try:
				response = requests.get(url, cookies = self.cookies)
			except:
				self.cookies = self.login()
				try:
					response = requests.get(url, cookies = self.cookies)
				except:
					return False
			text = response.text
			pattern = r'.*PagingMemoryProxy\((.*), false.*'
			fi = re.findall(pattern, text)[0]
			with open(filename, 'wb') as f:
				f.write(fi.encode('utf8'))
			print "Successful!"

if __name__ == '__main__':
	year = raw_input(u'请输入年份:')
	user = raw_input(u'请输入用户名:')
	passwd = raw_input(u'请输入密码:')
	yz = Download(year, user, passwd)
	yz.get_all()

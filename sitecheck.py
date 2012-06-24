#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import urllib2
import smtplib
import datetime 
import locale 
import time
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

def check(url):
	timeout = 5
	socket.setdefaulttimeout(timeout)
	msg = ''
	for n in range(1, 4):
		try:
			r = urllib2.urlopen(url)
			code = r.code
			if(code == 200):
				msg = ''
				break
		except urllib2.HTTPError, e:
			code = e.code
			msg += '\n  ' + datetime.datetime.today().strftime('%Y-%m-%d(%a) %H:%M:%S') + u': '+ e.msg
		except urllib2.URLError, e:
			code = -1
			msg += '\n  ' + datetime.datetime.today().strftime('%Y-%m-%d(%a) %H:%M:%S') + u': '+ u'URLError Timeout? No reply in ' + str(timeout) + u'sec'
		if(n == 3):
			mailsend(url, code, msg)
		time.sleep(5)

def mailsend(url, code, msg):
	subject = u'ERROR ON ' + url
	body = u'サイトチェックがエラーを発見しました' + '\n' + '\n'
	body += u'time:' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '\n'
	body += u'url :' + url + '\n'
	body += u'code:' + str(code) + '\n'
	body += u'msg :' + msg
	for to_addr in to_addrs:
		msg = create_message2(from_addr, to_addr, subject, body, 'ISO-2022-JP')
		send(from_addr, to_addr, msg)

def send(from_addr, to_addr, msg):
	s = smtplib.SMTP('127.0.0.1')
	s.sendmail(from_addr, [to_addr], msg.as_string())
	s.close()

def create_message2(from_addr, to_addr, subject, body, encoding):
	msg = MIMEText(body.encode(encoding), 'plain', encoding)
	msg['Subject'] = Header(subject, encoding)
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Date'] = formatdate()
	return msg

if __name__ == '__main__':
	from_addr = 'sitecheck@****.co.jp'
	to_addrs = ('xxx1@****.co.jp',
				'xxx2@****.co.jp',)
	map(check, ('http://www.****.co.jp',
				'http://www.****.com/****.jsp',
				'http://www.******.jp/****.html'))
	print 'Checked ' + datetime.datetime.today().strftime('%Y-%m-%d(%a) %H:%M:%S')
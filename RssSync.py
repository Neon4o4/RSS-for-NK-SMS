#encoding=utf8
import httplib
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

def getURLs(content):
	result_re=re.compile('<a.+href="(/html/.+html)">')
	result=result_re.findall(content)
	return result
	
def getPages(context, pageURL):
	context.request('GET',pageURL)
	content=context.getresponse()
	if content.status!=200:
		print 'http error:',content.status
		exit(-1)
	return content.read()
	
def getTitles(content):
	title=re.findall('<a.+href="/html/.+html">(.+)</a>',content)
	return title

def check_updated(url, latest_url):
	return (url==latest_url)

def do_update(urls, titles, latest_url, xml_file):
	tree=ET.parse(xml_file)
	root=tree.getroot()
	channel=root.find('channel')
	latest_update=latest_url
	#item_first=root.find('channel').findall('item')[0]
	for new_item in getNewItems(urls,titles,latest_url):
		channel.insert(3,create_item(new_item[0],unicode(new_item[1],'utf8')))
		latest_update=new_item[0]
		#print new_item[0],new_item[1]#create item and insert
	tree.write(xml_file)
	return latest_update

def create_item(url, title):
	#channel=root.find('channel')
	element_item = Element('item')
	element_title = Element('title')
	element_link = Element('link')
	element_description=Element('description')
	element_title.text=title
	element_link.text=url
	element_description.text=title
	element_item.insert(0,element_description)
	element_item.insert(0,element_link)
	element_item.insert(0,element_title)
	#channel.insert(3,element_item)
	return element_item

def getNewItems(urls, titles, latest_url):
	newItems=[]
	#urls=urls.reverse()
	for i in range(len(urls)):
		if urls[i] == latest_url:
			break
		else:
			newItems.append((urls[i],titles[i]))
	print newItems[0][1]
	newItems.reverse()
	return newItems
	
if __name__ == '__main__':
	page_set=[
		'/html/kydt/all/page1',
		'/html/xwzx/xyxw/page1',
		'/html/bksjx/all/page1',
		'/html/yjsjx/all/page1',
		'/html/xsgz/all/page1',
		'/html/zsxx/all/page1'
	]#科研动态，学院新闻，本科生教育，研究生教育，学生工作，公共数学
	xml_set=[
		'kydt.xml',
		'xwzx.xml',
		'bksjx.xml',
		'yjsjx.xml',
		'xsgz.xml',
		'zsxx.xml'
	]

	file=open('latest','r')
	latest=file.readlines()
	file.close()
	for i in range(len(latest)):
		latest[i]=latest[i].strip('\n')
	print latest
	conn=httplib.HTTPConnection('sms.nankai.edu.cn')
	for i in range(len(page_set)):
		page=getPages(conn, page_set[i])
		urls=getURLs(page)
		titles=getTitles(page)
		if not check_updated(urls[0], latest[i]):
			latest_update=do_update(urls, titles, latest[i], xml_set[i])
			latest[i]=latest_update
	conn.close()
	
	file=open('latest','w')
	file.truncate()
	for line in latest:
		file.writelines(line+'\n')
	file.close()

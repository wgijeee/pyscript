#-*- coding: UTF-8 -*-
#!/usr/bin/python
#====================================================
#每天晚上23点，对数据库进行一次完整备份。第二天0-22点，每小时进行一次增量备份。
#每次备份前把上次的完整备份和23次增量备份移动到指定目录里，保留7天的数据。
#====================================================
import datetime
import subprocess
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tarold.log',
                filemode='a')
stores = ''
def tarrem():
	date = datetime.datetime.now().strftime("%y%m%d")
	oldate=int(date)-1
	suffix = str(oldate)
	storedir = "%s/%s-bak" %(stores,suffix)
	if  os.path.exists(storedir):
		commandtar = "tar -zcvf %s/%s.tar.gz %s --remove-files" %(stores,suffix,storedir)
		subprocess.call(commandtar,shell=True)
		logging.info(commandtar)
		logging.info('success!')
	else:
		logging.info('The directory does not exist')
if __name__ == '__main__':
	tarrem()

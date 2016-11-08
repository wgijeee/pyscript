#-*- coding: UTF-8 -*-
#!/usr/bin/python
#====================================================
# at 23 every night, a full backup of the database. Second days 0-22 point, an incremental backup per hour.
#The last full backup and 23 incremental backup moves to the specified directory 
# each backup before 7 days of retention data.
#
#Who is the original, I do not know. In network collection.
#Application system Centos6.5+
#Python2.6
#Script based software: xtrabackup1.5+ 
#====================================================
import datetime
import subprocess
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='backup.log',
# Log path and log name .日志路径和日志名称
                filemode='a')
backuser = 'datyour name'
#Database user name 
backpass = 'your passow'
#Database user password 
basedir = 'your backup path'
#Backup path  备份路径
databases = '\"you databases\"'
tomorrowdate = datetime.date.fromordinal(datetime.date.today().toordinal()+1).strftime("%y%m%d")
todaydate = datetime.datetime.now().strftime("%y%m%d")
fullback_dir = "%s/%s" %(basedir,tomorrowdate)
cuhour = datetime.datetime.now().strftime("%H")
#Get the current hour  获取当前小时间
ct = str(int(cuhour) - 0)
#Please forgive me for my boredom 偷懒不想做00与0的转换
increment_dir = '%s/%s' %(basedir,ct)
increbase_dir=''
stores = ''
# More than one day backup path 转储超过一天的备份数据

def storebefore():
    suffix = datetime.datetime.now().strftime("%y%m%d")
    storedir = "%s/%s-bak" %(stores,suffix)
    if not os.path.exists(storedir):
        subprocess.call("mkdir -p %s" %(storedir),shell=True)
    command = "cd %s && mv * %s" %(basedir,storedir)
    subprocess.call(command,shell=True)

def cleanstore():
    command = "find %s -type d -mtime +7 |xargs rm -fr" % stores
#Delete the backup data for more than 7 days in the dump directory, and modify it according to the actual data.删除转储目录中超过7天的备份数据，自己按实际修改.
    subprocess.call(command,shell=True)
#tar old day database.
def tarrem():
    date = datetime.datetime.now().strftime("%y%m%d")
    oldate=int(date)-1
    suffix = str(oldate)
    storedir = "%s/%s-bak" %(stores,suffix)
    commandtar = "tar -zcvf %s/%s.tar.gz %s --remove-files" %(stores,suffix,storedir)
    subprocess.call(commandtar,shell=True)
    logging.info(commandtar)

def backup():
    if not os.path.exists(basedir):
        subprocess.call("mkdir -p %s"%basedir,shell=True)
    commandfull = "innobackupex --user=%s --password=%s  --no-timestamp %s" %(backuser,backpass,fullback_dir)
    if cuhour == '23':
#  Backup method, 23 point full backup every day, second days 0-22 point incremental backup 备份方法，每天23点完整备份，第二天0-22点增量备份
        storebefore()
        subprocess.call("rm -fr %s/*"%basedir,shell=True)
        subprocess.call(commandfull,shell=True)
        logging.info(commandfull)
    else:
        if int(cuhour) - 1 >= 0:
            increbase_dir = '%s/%s' %(basedir,str(int(cuhour) - 1))
        else:
            increbase_dir = "%s/%s" %(basedir,todaydate)
        if not os.path.exists(increbase_dir):
            logging.info(' Incremental text backup does not exist (%s) to stop running. '%increbase_dir)
            exit(0)
        commandincre = "innobackupex --user=%s --password=%s  --no-timestamp --incremental %s --incremental-basedir=%s" %(backuser,backpass,increment_dir,increbase_dir)
        subprocess.call(commandincre,shell=True)
        logging.info(commandincre)
         
if __name__ == '__main__':
	tarrem()
    backup()
    cleanstore()

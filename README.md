# pyscript
##mysql.py##
====================================================
at 23 every night, a full backup of the database. Second days 0-22 point, an incremental backup per hour.
The last full backup and 23 incremental backup moves to the specified directory 
 each backup before 7 days of retention data.

Who is the original, I do not know. In network collection.
Application system Centos6.5+
Python2.6
Script based software: xtrabackup1.5+ 

每天晚上23点，对数据库进行一次完整备份。第二天0-22点，每小时进行一次增量备份。
每次备份前把上次的完整备份和23次增量备份移动到指定目录里，保留7天的数据。    
#添加定时任务方法.
```
shell>sudo service crond start
shell>sudo crontab -e
* */1 * * * /usr/bin/python mysql.py
shell>sudo chkconfig crond on
```
2016-11-08
添加使用tar压缩旧的数据。。。。好烦呢
:(
# pyscript
##mysql ##
====================================================
at 23 every night, a full backup of the database. Second days 0-22 point, an incremental backup per hour.
The last full backup and 23 incremental backup moves to the specified directory 
 each backup before 7 days of retention data.

Who is the original, I do not know. In network collection.
Application system Centos6.5+
Python2.6
Script based software: xtrabackup1.5+ 
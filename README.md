# Simple Swiss Tournaments System
Simple Swiss Tournaments System built with Python 2.7 and PostgresSQL

## Reference
http://www.wikiwand.com/en/Swiss-system_tournament

## Requirements
- Python 2.7
- PostgresSQL
- VirtualBox
- Vagrant

## To Run
Start VM  
```
cd vagrant/
vagrant up
```
SSH VM
```
vagrant ssh
```
Set up Database
```
cd /vagrant/tournament/
psql
\i tournament.sql
\q
```
Run Test
```
cd /vagrant/tournament/
python Tournament_test.py
```
Exit VM
```
exit
```
Suspend VM
```
vagrant suspend
```

## Useful Links
How do I destroy a VM when I deleted the .vagrant file?
http://stackoverflow.com/questions/15408969/how-do-i-destroy-a-vm-when-i-deleted-the-vagrant-file  

How to drop a PostgreSQL database if there are active connections to it?
http://stackoverflow.com/questions/5408156/how-to-drop-a-postgresql-database-if-there-are-active-connections-to-it

'''
Created on Jun 07, 2014

@author: Harvey
'''

import datetime
import numpy
import mysql.connector
import csv
import os.path
import misc

dbconfig = {'user': 'harvey', 
          'password':'9619252y', 
          'host':'localhost',
          'database': 'blueshale',
          }

def insert_tick_data(dbtable, tick):
	cnx = mysql.connector.connect(**dbconfig)
	cursor = cnx.cursor()
	col_list = tick.__dict__.keys()
	if 'timestamp' in col_list:
		col_list.remove('timestamp')
		
	stmt = "INSERT IGNORE INTO {table} ({variables}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table=dbtable,variables=','.join(col_list))
	args = tuple([getattr(tick,col) for col in col_list])
	cursor.execute(stmt, args)
	cnx.commit()
	cnx.close()
	pass
    
def bulkinsert_tick_data(dbtable, ticks):
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()
    col_list = ticks[0].__dict__.keys()
    if 'timestamp' in col_list:
        col_list.remove('timestamp')

    stmt = "INSERT IGNORE INTO {table} ({variables}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table=dbtable,variables=','.join(col_list))
    args = [tuple([getattr(tick,col) for col in col_list]) for tick in ticks]    
    cursor.executemany(stmt, args)
    cnx.commit()
    cnx.close()
    pass

def insert_min_data(dbtable, inst, min_data):
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()
    col_list = min_data.keys()
    exch = misc.inst2exch(inst)    
    stmt = "INSERT IGNORE INTO {table} (instID,exch,{variables}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table=dbtable,variables=','.join(col_list))
    args = tuple([inst, exch]+[min_data[col] for col in col_list])
    cursor.execute(stmt, args)
    cnx.commit()
    cnx.close()
    pass

def insert_daily_data(dbtable, inst, daily_data):
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()
    col_list = daily_data.keys()
    exch = misc.inst2exch(inst)    
    stmt = "INSERT IGNORE INTO {table} (instID,exch,{variables}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table=dbtable,variables=','.join(col_list))
    args = tuple([inst, exch]+[daily_data[col] for col in col_list])
    cursor.execute(stmt, args)
    cnx.commit()
    cnx.close()
    pass

def import_tick_from_file(dbtable):
	inst_list = ['IF1406', 'IO1406-C-2300','IO1406-P-2300','IO1406-C-2250',
				'IO1406-P-2250','IO1406-C-2200','IO1406-P-2200','IO1406-C-2150',
				'IO1406-P-2150','IO1406-C-2100','IO1406-P-2100','IO1406-C-2050',
				'IO1406-P-2050','IO1406-C-2000','IO1406-P-2000','IO1407-C-2300',
				'IO1407-P-2300','IO1407-C-2250','IO1407-P-2250','IO1407-C-2200',
				'IO1407-P-2200','IO1407-C-2150','IO1407-P-2150','IO1407-C-2100',
				'IO1407-P-2100','IO1407-C-2050','IO1407-P-2050','IO1407-C-2000',
				'IO1407-P-2000','IF1406']
	date_list = ['20140603','20140604','20140605','20140606']
	main_path = 'C:/dev/src/ktlib/pythonctp/data/'
	cnx = mysql.connector.connect(**dbconfig)
	cursor = cnx.cursor()
	for inst in inst_list:
		for date in date_list:
			path = main_path + inst + '/' + date + '_tick.txt'
			if os.path.isfile(path):
				stmt= "load data infile '{path}' replace into table {table} fields terminated by ',' lines terminated by '\n' (instID, date, @var1, sec, msec, openInterest, volume, price, high, low, bidPrice1, bidVol1, askPrice1, askVol1) set hour=(@var1 div 100), min=(@var1 % 100)".format(path=path, table=dbtable)
				cursor.execute(stmt)
				cnx.commit()
	cnx.close()
	pass
    
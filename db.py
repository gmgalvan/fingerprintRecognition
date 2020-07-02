import pymysql
import paramiko
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
import IPython.core.magics.osm
import os
from os.path import expanduser

'''
DBCLIENT es la clase para poder obtener un cliente que realice una conexion 
tcp ip sobre ssh hacia una base de datos mysql 
TODO: Utilizar patron with para conexion ejemplo: https://effbot.org/zone/python-with-statement.html
'''
class DBCLIENT:
    def __init__(self):
        # TODO: agregar variables de entorno
        pkeyfilepath = os.path.abspath("")
        self.mypkey = paramiko.RSAKey.from_private_key_file(pkeyfilepath)
        self.sql_hostname = ''
        self.sql_username = ''
        self.sql_password = '.'
        self.sql_main_database = ''
        self.sql_port = 
        self.ssh_host = ''
        self.ssh_user = ''
        self.ssh_port = 

        self.tunnel = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_user,
                ssh_pkey=self.mypkey,
                remote_bind_address=(self.sql_hostname, self.sql_port))            
        self.tunnel.start()
        
        self.conn = pymysql.connect(host='', user=self.sql_username,
            passwd=self.sql_password, db=self.sql_main_database,
            port=self.tunnel.local_bind_port)

    def db_connection(self):
        return self.conn
    
    def close(self):
        self.conn.close()
        self.tunnel.close()

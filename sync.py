import configparser
from LdapService import *

config = configparser.ConfigParser()
config.read('config.ini')

ad      =  connection(config['LDAP']['url' ],
                      config['LDAP']['user'],
                      config['LDAP']['pass']);

users   = members(ad, config['LDAP']['base_dn'],
                      config['LDAP']['group_dn']);

print(users)

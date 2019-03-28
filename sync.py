import configparser
import LdapService

config = configparser.ConfigParser()
config.read('config.ini')

ad      =  LdapService.connection(config['LDAP']['url' ],
                      config['LDAP']['user'],
                      config['LDAP']['pass']);


users   = LdapService.members(ad, config['LDAP']['base_dn'],
                      config['LDAP']['group_dn']);

print(users)

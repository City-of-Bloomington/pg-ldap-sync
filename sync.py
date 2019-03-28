"""Sync user accounts from LDAP to postgres
"""
__copyight__ = '2019 City of Bloomington, Indiana'
__license__  = 'GPL-3.0-or-later'

import configparser
import psycopg2
import LdapService
from PostgresService import PostgresService

config = configparser.ConfigParser()
config.read('config.ini')

ad      =  LdapService.connection(config['LDAP']['url' ],
                                  config['LDAP']['user'],
                                  config['LDAP']['pass']);


ad_users = LdapService.members(ad, config['LDAP']['base_dn'],
                                   config['LDAP']['group_dn'])

pg       = PostgresService(config['POSTGRES']['uri' ],
                           config['POSTGRES']['role'])

for u in ad_users:
    p = pg.user(u)
    if not p or not p.member:
        pg.add_user(u)

for u in pg.get_users():
    if u not in ad_users and u.member and not u.superuser:
        pg.del_user(u)

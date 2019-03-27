import ldap

def connection(url, username, password):
    connection = ldap.initialize(url, 0);
    connection.set_option(ldap.OPT_DEBUG_LEVEL,      0);
    connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3);
    connection.set_option(ldap.OPT_REFERRALS,        0);
    connection.set_option(ldap.OPT_TIMELIMIT,       10);
    connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 10);
    connection.simple_bind_s(username, password)
    return connection

def members(connection, base_dn, group):
    usernames = [];
    filter    = '(&(objectClass=user)(memberOf:1.2.840.113556.1.4.1941:=%s))' % group
    attrs     = ['sAMAccountName']
    result    = connection.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs);

    for entry in result:
        if (entry[0] != None):
            usernames.append(entry[1].get('sAMAccountName')[0].decode('utf-8'))
    return usernames;

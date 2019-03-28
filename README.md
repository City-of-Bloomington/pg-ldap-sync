# Sync user accounts from LDAP to Postgres

This python script creates and deletes postgres user accounts by comparing members of an LDAP group.  LDAP group members will have accounts created.  Postgres users not in the LDAP group, who are not SuperUsers, will be deleted.

This is currently written to support ActiveDirectory nested groups. This uses [Microsoft's matching rule OIDs](https://www.google.com/url?q=https://docs.microsoft.com/en-us/windows/desktop/ADSI/search-filter-syntax&sa=D&source=hangouts&ust=1553863746337000&usg=AFQjCNEIX1Uv1p7guD3TqPIqZwbfazYSrw) in the LDAP search filter.

## Requirements
* Python >= 3.6

Python libraries
* configparser
* ldap
* psycopg2

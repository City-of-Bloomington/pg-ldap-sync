"""Handles communication with the postgres server
"""
__copyight__ = '2019 City of Bloomington, Indiana'
__license__  = 'GPL-3.0-or-later'

import psycopg2
import psycopg2.extras
from psycopg2 import sql

from typing import List, Tuple, Optional

class UserResult:
    username:  str
    superuser: bool
    member:    bool

    def __init__(self, data: dict):
        self.username  = data['rolname' ]
        self.superuser = data['rolsuper']
        self.member    = data['member'  ]

class PostgresService:
    group: str
    cursor: psycopg2.extensions.cursor
    users: List[UserResult] = []

    def __init__(self, uri: str, group: str):
        """
        Args:
            uri   (str): The libpq connection uri
                         https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
            group (str): The postgres group to populate with all the LDAP users
        """
        pg            = psycopg2.connect(uri)
        pg.autocommit = True
        self.cursor   = pg.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.group    = group

    def get_users(self) -> List[UserResult]:
        if not self.users:
            sql = """
                select u.rolname,
                    u.rolsuper,
                    case when members.member is not null then True
                            when members.member is null     then False
                        end as member
                from pg_roles        u
                left join (
                    select m.member
                    from pg_roles r
                    join pg_auth_members m on r.oid=m.roleid
                    where r.rolname=%s
                ) members on u.oid=members.member;
                """
            self.cursor.execute(sql, [self.group])
            for row in self.cursor.fetchall():
                self.users.append(UserResult(row))
        return self.users


    def user(self, username: str) -> Optional[UserResult]:
        """Return user info if the user exists on the postgres server
        """
        users = self.get_users()
        for u in users:
            if u.username == username: return u

    def add_user(self, username: str):
        u = self.user(username)
        if not u:
            qq    = 'create role {} with LOGIN'
            query = sql.SQL(qq).format(sql.Identifier(username))

            print(query.as_string(self.cursor))
            self.cursor.execute(query)

            qq    = 'grant {} to {}'
            query = sql.SQL(qq).format(sql.Identifier(self.group),
                                       sql.Identifier(username))
            print(query.as_string(self.cursor))
            self.cursor.execute(query)
        else:
            if not u.member:
                qq    = 'grant {} to {}'
                query = sql.SQL(qq).format(sql.Identifier(self.group),
                                           sql.Identifier(username))
                print(query.as_string(self.cursor))
                self.cursor.execute(query)

    def del_user(self, user: UserResult):
        if user.member and not user.superuser:
            qq    = 'drop role {}'
            query = sql.SQL(qq).format(sql.Identifier(user.username))
            print(query.as_string(self.cursor))
            self.cursor.execute(query)
        else:
            print('Preserving user %s' % user.username)

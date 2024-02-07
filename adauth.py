from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from decouple import config


class ADAuth:
    def __init__(self, server_address=None, domain_name=None, search_base=None, groupname=None):
        if server_address is None:
            self.server_address = config('SERVER_ADDRESS')
        else:
            self.server_address = server_address

        if domain_name is None:
            self.domain_name = config('DOMAIN_NAME')
        else:
            self.domain_name = domain_name

        if search_base is None:
            self.search_base = config('SEARCH_BASE')
        else:
            self.search_base = search_base

        if groupname is None:
            self.group_name = config('GROUP_NAME')
        else:
            self.group_name = groupname

        # Establish a connection to the server
        self.server = Server(self.server_address, get_info=ALL)

    def authenticate_user(self, username, password) -> bool:
        auth = False
        group = False
        auth_and_group = False
        try:
            # Formulate the user's DN (Distinguished Name)
            user_dn = f"{self.domain_name}\\{username}"
            # Establish a connection using the user's credentials
            with Connection(self.server, user=user_dn, password=password, authentication=NTLM, auto_bind=True) as conn:
                # If connection is established, authentication is successful
                auth = True
                # Retrieve user's group memberships
                conn.search(search_base=self.search_base, # Adjust this to your AD's base DN
                            search_filter=f'(sAMAccountName={username})',
                            search_scope=SUBTREE,
                            attributes=['memberOf'])
                # Extract and return the groups from the search result
                if conn.entries:
                    mygroup = self.group_name.lower()
                    groups = []
                    for entry in conn.entries[0].memberOf.values:
                        oneGroup = entry.split(',')[0].split('=')[1].lower()
                        if oneGroup == mygroup:
                            group = True
                            break

                if auth and group:
                    auth_and_group = True
        except Exception as e:
            return False
        return auth_and_group


# # Example usage:
# ## ad_auth = ActiveDirectoryAuth(server_address='192.168.2.27', domain_name='wwd', search_base='DC=wwd,DC=local')
# ad_auth = ActiveDirectoryAuth()
# result = ad_auth.authenticate_user('jcarter', 'Zebras are b and w')
# print(f"Authenticated {result}")
#
#

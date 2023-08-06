"""
The most basic usage automatically saves and loads tokens, and provides
a local server for logging in users.
"""
from globus_sdk import AuthClient
from fair_research_login import NativeClient

# Register a Native App for a client_id at https://developers.globus.org
client = NativeClient(client_id='7414f0b4-7d05-4bb6-bb00-076fa3f17cf5')

# Automatically saves tokens in ~/.globus-native-apps.cfg
tokens = client.login(
    # Request any scopes you want to use here.
    requested_scopes=['openid', 'profile'],
    # You can turn off the local server if it cannot be used for some reason
    no_local_server=False,
    # You can also turn off automatically opening the Auth URL
    no_browser=False,
    # refresh tokens are fully supported, but optional
    refresh_tokens=True,
)

# Calling login() twice will load tokens instead of initiating an oauth flow,
# as long as the requested scopes match and the tokens have not expired.
assert tokens == client.login(requested_scopes=['openid', 'profile'])

# You can also load tokens explicitly. This will also load tokens if you have
# done other logins
assert tokens == client.load_tokens()
# If you want to disregard other saved tokens
assert tokens == client.load_tokens(requested_scopes=['openid', 'profile'])

# Loading by scope is also supported
tokens_by_scope = client.load_tokens_by_scope()
assert set(tokens_by_scope.keys()) == {'openid', 'profile'}

# Authorizers automatically choose a refresh token authorizer if possible,
# and will automatically save new refreshed tokens when they expire.
ac_authorizer = client.get_authorizers()['auth.globus.org']
# Also supported
ac_authorizer = client.get_authorizers_by_scope()['openid']

# Example client usage:
auth_cli = AuthClient(authorizer=ac_authorizer)
user_info = auth_cli.oauth2_userinfo()
print('Hello {}! How are you today?'.format(user_info['name']))

# Revoke tokens now that we're done
client.logout()

# okta-token-fetcher

Provides a commandline script and package for getting an OKTA id_token by interacting with your browser via the commandline.

This script builds off of the dirty quick way to get a token from your browser stated here:
https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/#get-an-access-token-and-make-a-request .

This is done by opening a browser window that navigates to the auth server with localhost as the redirect_uri. There
is an http server that is spun up for just long enough to handle the redirect request and get the id_token from the
query parameters that are sent via window.hash (I suppose OKTA does this so that it can't be sent to the server itself).

Note that when using this tool your OKTA JWT will:

  * Be stored in ~/.okta_token (700 file permissions) unless --no-cache is specified
  * Be visible in the url bar of your browser for a few seconds
  * Be visible on the page after all of the redirects for 3 seconds before being redirected to a final page in your browser

Your OKTA application MUST have "http://localhost:8888" configured as one of the allowed redirect uri's for this tool to work.

## As a terminal script:

```
usage: okta-fetch [-h] -u URL -c CLIENT_ID [-s SCOPES] [-t TOKEN_TYPE] [--no-cache]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The auth server url. This should be only the domain and protocol. eg: https://mydomain.okta.com
  -c CLIENT_ID, --client-id CLIENT_ID
                        The client id to get a token for
  -s SCOPES, --scopes SCOPES
                        Comma delimited list of scopes to request
  -t TOKEN_TYPE, --token-type TOKEN_TYPE
                        The type of token to request
  --no-cache            Don't cache the token
```

# Implemented in another script:

```
fetcher = OktaToken(
    url="https://youraccount.okta.com",
    client_id="abcdefg12345",
    scopes=["groups", "profile"],
    token_type="id_token",
    cache=True
)

print(fetcher.token)
```
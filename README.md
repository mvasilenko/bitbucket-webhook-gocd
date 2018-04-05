# bitbucket-webhook-gocd

based on https://bitbucket.org/atlassianlabs/webhook-listener

this flask app will try extract tag from bitbucket web hook commit info,
and trigger specific pipeline according repo name

bitbucket hooks allowed ip in nginx format:

```
    allow 34.198.203.127;
    allow 34.198.178.64;
    allow 34.198.32.85;
    allow 104.192.136.0/21;
    allow 127.0.0.1;
    deny all;
```

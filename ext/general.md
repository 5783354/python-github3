<!-- https://gist.github.com/raw/71c2878f53e886dc921a/general.md -->

## GitHub API v3

**Note:** This API is in a beta state.  Breaking changes may occur.

### Schema

All API access is over HTTPS, and accessed from the `api.github.com`
domain.  All data is sent and received as JSON.

Blank fields are included as `null` instead of being omitted.

All timestamps are returned in ISO 8601 format:

    YYYY-MM-DDTHH:MM:SSZ

### Authentication

There are two ways to authenticate through GitHub API v3:

Basic Authentication:

    $ curl -u "username:PASSWORD" https://api.github.com

OAuth2 Token (sent in a header):

    $ curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com

OAuth2 Token (sent as a parameter):

    $ curl https://api.github.com?access_token=OAUTH-TOKEN

Read [more about OAuth2](http://develop.github.com).

### Pagination

Requests that return multiple items will be paginated to 30 items by
default.  You can specify further pages with the `?page` parameter.  You
can also set a custom page size up to 100 with the `?per_page` parameter.

    $ curl https://api.github.com/repos.json?page=2&per_page=100

### Rate Limiting

We limit requests to API v3 to 5000 per day.  This is keyed off either your login, or your request IP.  You can check the returned HTTP headers to see your current status:

    $ curl -i https://api.github.com
    HTTP/1.1 200 OK
    Status: 200 OK
    X-RateLimit-Limit: 5000
    X-RateLimit-Remaining: 4966

You can file a [support issue](http://support.github.com/dashboard/queues/2386-api) to request white listed access for your application.  We prefer sites that setup OAuth applications for their users.

### JSON-P Callbacks

You can send a `?callback` parameter to any GET call to have the results
wrapped in a JSON function.  This is typically used when browsers want
to embed GitHub content in web pages by getting around cross domain
issues.  The responses always return 200, and are wrapped in meta
objects containing the actual meta information:

    $ curl https://api.github.com?callback=foo

    foo({
      "data": {},
      "meta": {
        "status": 200,
        "pagination": {"page": 1, "per_page": 30},
        "rate": {"key": "IP ADDRESS", "remaining": 4999, "limit": 5000}
      }
    })

### Versions

Api V3 uses content negotiation to specify the expected output format.
V3 is specified with this mime type:

    application/vnd.github.v3+json

This allows us to upgrade the API if needed, and support multiple versions of the API in transition period.  If you want to ensure your API usage works uninterrupted, you will want to specify this mime type in an Accept header:

    curl -H "Accept: application/vnd.github.v3+json" https://api.github.com

Specifying `application/json` will assume the latest version of the API.  Specifying an unknown version will result in a `406 Not Acceptable` error.

We don't plan to bump the API version unless absolutely necessary.  Things like removing end points, renaming or removing object attributes, or removing resources completely will result in a new version.  This should be extremely rare, however.

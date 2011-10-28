"""
github3.models
~~~~~~~~~~~~~~

This module provides the Github3 object model.
"""

import json

from .helpers import to_python, to_api, key_diff


class BaseResource(object):
    """A BaseResource object."""

    _strs = []
    _ints = []
    _dates = []
    _bools = []
    _map = {}
    _writeable = []
    _cache = {}


    def __init__(self):
        self._bootstrap()
        super(BaseResource, self).__init__()


    def __dir__(self):
        return self.keys()

    def _bootstrap(self):
        """Bootstraps the model object based on configured values."""

        for attr in self.keys():
            setattr(self, attr, None)

    def keys(self):
        return self._strs + self._ints + self._dates + self._bools + self._map.keys()

    def dict(self):
        d = dict()
        for k in self.keys():
            d[k] = self.__dict__.get(k)

        return d

    @classmethod
    def new_from_dict(cls, d, gh=None):

        return to_python(
            obj=cls(), in_dict=d,
            str_keys = cls._strs,
            int_keys = cls._ints,
            date_keys = cls._dates,
            bool_keys = cls._bools,
            object_map = cls._map,
            _gh = gh
        )


    def update(self):
        deploy = key_diff(self._cache, self.dict(), pack=True)

        deploy = to_api(deploy, int_keys=self._ints, date_keys=self._dates, bool_keys=self._bools)
        deploy = json.dumps(deploy)

        r = self._gh._patch_resource(self.ri, deploy)
        return r


class Plan(BaseResource):
    """Github Plan object model."""

    _strs = ['name']
    _ints = ['space', 'collaborators', 'private_repos']

    def __repr__(self):
        return '<plan {0}>'.format(str(self.name))



class User(BaseResource):
    """Github User object model."""

    _strs = [
        'login','avatar_url', 'url', 'name', 'company', 'blog', 'location',
        'email', 'bio', 'html_url']

    _ints = ['id', 'public_repos', 'public_gists', 'followers', 'following']
    _dates = ['created_at',]
    _bools = ['hireable', ]
    # _map = {}
    # _writeable = []

    @property
    def ri(self):
        return ('users', self.login)

    def __repr__(self):
        return '<user {0}>'.format(self.login)

    def repos(self, limit=None):
        return self._gh._get_resources(('users', self.login, 'repos'), Repo, limit=limit)

    def repo(self, reponame):
         return self._gh._get_resource(('repos', self.login, reponame), Repo)

    def orgs(self):
        return self._gh._get_resources(('users', self.login, 'orgs'), Org)



class CurrentUser(User):
    """Github Current User object model."""

    _ints = [
        'id', 'public_repos', 'public_gists', 'followers', 'following',
        'total_private_repos', 'owned_private_repos', 'private_gists',
        'disk_usage', 'collaborators']
    _map = {'plan': Plan}
    _writeable = ['name', 'email', 'blog', 'company', 'location', 'hireable', 'bio']

    @property
    def ri(self):
        return ('user',)

    def __repr__(self):
        return '<current-user {0}>'.format(self.login)

    def repos(self, limit=None):
         return self._gh._get_resources(('user', 'repos'), Repo, limit=limit)

    def repo(self, reponame):
         return self._gh._get_resource(('repos', self.login, reponame), Repo)

    def orgs(self, limit=None):
        return self._gh._get_resources(('user', 'orgs'), Org,  limit=limit)

    def org(self, orgname):
        return self._gh._get_resource(('orgs', orgname), Org)



class Org(BaseResource):
    """Github Organization object model."""

    _strs = [
        'login', 'url', 'avatar_url', 'name', 'company', 'blog', 'location', 'email'
        'html_url', 'type', 'billing_email']
    _ints = [
        'id', 'public_repos', 'public_gists', 'followers', 'following',
        'total_private_repos', 'owned_private_repos', 'private_gists', 'disk_usage',
        'collaborators']
    _dates = ['created_at']
    _map = {'plan': Plan}
    _writable = ['billing_email', 'blog', 'company', 'email', 'location', 'name']

    @property
    def ri(self):
        return ('orgs', self.login)

    def __repr__(self):
        return '<org {0}>'.format(self.login)

    def repos(self, limit=None):
         return self._gh._get_resources(('orgs', self.login, 'repos'), Repo, limit=limit)

    def members(self, limit=None):
        return self._gh._get_resources(('orgs', self.login, 'members'), User, limit=limit)

    def is_member(self, username):
        if isinstance(username, User):
            username = username.login

        r = self._gh._http_resource('GET', ('orgs', self.login, 'members', username), check_status=False)
        return (r.status_code == 204)

    def publicize_member(self, username):
        if isinstance(username, User):
            username = username.login

        r = self._gh._http_resource('PUT', ('orgs', self.login, 'public_members', username), check_status=False, data='')
        return (r.status_code == 204)

    def conceal_member(self, username):
        if isinstance(username, User):
            username = username.login

        r = self._gh._http_resource('DELETE', ('orgs', self.login, 'public_members', username), check_status=False)
        return (r.status_code == 204)

    def remove_member(self, username):
        if isinstance(username, User):
            username = username.login

        r = self._gh._http_resource('DELETE', ('orgs', self.login, 'members', username), check_status=False)
        return (r.status_code == 204)

    def public_members(self, limit=None):
        return self._gh._get_resources(('orgs', self.login, 'public_members'), User, limit=limit)

    def is_public_member(self, username):
        if isinstance(username, User):
            username = username.login

        r = self._gh._http_resource('GET', ('orgs', self.login, 'public_members', username), check_status=False)
        return (r.status_code == 204)




class Repo(BaseResource):
    _strs = [
        'url', 'html_url', 'clone_url', 'git_url', 'ssh_url', 'svn_url',
        'name', 'description', 'homepage', 'language', 'master_branch']
    _bools = ['private', 'fork']
    _ints = ['forks', 'watchers', 'size',]
    _dates = ['pushed_at', 'created_at']
    _map = {'owner': User}


    @property
    def ri(self):
        return ('repos', self.owner.login, self.name)

    def __repr__(self):
        return '<repo {0}/{1}>'.format(self.owner.login, self.name)
    # owner

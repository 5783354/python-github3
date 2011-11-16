#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author: David Medina

from .base import Handler
import github3.models as models
from github3.converters import Rawlizer
from github3.exceptions import UserIsAnonymous


class User(Handler):
    """ User handler with public access """

    prefix = 'users'

    def __repr__(self):
        return '<User handler> %s>' % getattr(self, 'username', 'without user')

    def _parse_user(self, user):
        """ Parse user, and if it fails then try with username in handler

        :param user: It can be a `models.User` or alphanumeric user string

        """
        username = getattr(user, 'login', user)
        if not username or not str(username).isalpha():
            username = getattr(self, 'username', False)
        if not username:
            raise UserIsAnonymous('%s user is not valid' % username)
        return str(username)

    def set_username(self, user):
        """ Set username to query public handler
        Helper to less writing

        :param user: It can be a `models.User` or alphanumeric user string

        """
        self.username = self._parse_user(user)
        return self

    def get(self, user=None):
        """ Return user

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resource(user, model=models.User)

    def get_followers(self, user=None, limit=None):
        """ Return user's followers

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/followers' % user, model=models.User,
                                   limit=limit)

    def get_following(self, user=None, limit=None):
        """ Return users that follow

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/following' % user, model=models.User,
                                   limit=limit)

    def get_repos(self, user=None, limit=None):
        """ Return user's public repositories

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/repos' % user, model=models.Repo,
                                   limit=limit)

    def get_watched(self, user=None, limit=None):
        """ Return repositories that user whatch

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/watched' % user, model=models.Repo,
                                   limit=limit)

    def get_orgs(self, user=None, limit=None):
        """ Return user's public organizations

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/orgs' % user, model=models.Org,
                                   limit=limit)

    def get_gists(self, user=None, limit=None):
        """ Return user's gists

        :param `user`: User model or username string

        """
        user = self._parse_user(user)
        return self._get_resources('%s/gists' % user, model=models.Gist,
                                   limit=limit)


class AuthUser(User):
    """ User handler with public and private access """

    prefix = 'user'

    def __repr__(self):
        return '<AuthUser handler> %s>' % self._gh.session.auth[0]

    def get(self):
        return self._get_resource('', model=models.AuthUser)

    def get_emails(self):
        """ Return list of emails """

        # Ignore converter, it must be Rawlizer
        emails = self._get_resource('emails', converter=Rawlizer)
        return emails

    def create_emails(self, *args):
        """
        Add emails

        :param args: Collection of emails
            create_emails(*('test1@example.com', 'test2@example.cm'))
        """
        parsed_emails = map(str, args)
        all_mails = self._post_resource(
            'emails', data=parsed_emails, converter=Rawlizer)
        return all_mails

    def delete_emails(self, *args):
        """
        Delete emails

        :param args: Collection of emails
            create_emails(*('test1@example.com', 'test2@example.cm'))
        """
        parsed_emails = map(str, args)
        return self._delete('emails', data=parsed_emails)

    def is_following(self, user):
        """
        Return true if you are following the user

        :param `user`: User model or username string
        """

        parse_user = str(getattr(user, 'login', user))
        return self._bool('following/%s' % parse_user)

    def follow(self, user):
        """
        Follow user

        :param `user`: User model or username string

        """

        parse_user = getattr(user, 'login', user)
        return self._put('following/%s' % parse_user)

    def unfollow(self, user):
        """
        Unfollow user

        :param `user`: User model or username string
        """

        parse_user = getattr(user, 'login', user)
        return self._delete('following/%s' % parse_user)

    def get_keys(self):
        """ Get public keys """

        return self._get_resources('keys', model=models.Key,
                                   limit=limit)

    def get_key(self, key_id):
        """ Get public key by id """

        return self._get_resource('keys/%s' % key_id, model=models.Key)

    def create_key(self, **kwargs):
        """
        Create public key

        :param title
        :param key: Key string
        """

        #TODO: render key.pub file
        key = {
            'title': kwargs.get('title', ''),
            'key': kwargs.get('key', '')
        }
        return self._post_resource('keys', data=key, model=models.Key)

    def delete_key(self, key_id):
        """ Delete public key """

        return self._delete('keys/%s' % key_id)

    def get_repos(self, filter='all'):
        """
        Return user's public repositories

        param: filter: 'all', 'public', 'private' or 'member'
        """

        return self._get_resources('repos', model=models.Repo,
                                   limit=limit, type=str(filter))

    def is_watching_repo(self, owner, repo):
        """
        Return true if you are watching the user repository

        :param owner: username
        :param repo: repository name
            is_watching_repo('copitux', 'python-github3')
        """

        owner = getattr(owner, 'login', owner)
        repo = getattr(repo, 'name', repo)
        return self._bool('watched/%s/%s' % (owner, repo))

    def watch_repo(self, owner, repo):
        """
        Watch the repository

        :param owner: username
        :param repo: repository name
        """

        return self._put('watched/%s/%s' % (owner, repo))

    def unwatch_repo(self, owner, repo):
        """
        Unwatch the repository

        :param owner: username
        :param repo: repository name
        """

        return self._delete('watched/%s/%s' % (owner, repo))

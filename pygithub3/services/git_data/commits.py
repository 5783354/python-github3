#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pygithub3.services.base import Service


class Commits(Service):
    """Consume `Commits API <http://developer.github.com/v3/git/commits/>`_"""

    def get(self, sha, user=None, repo=None):
        """get a commit from the current repo"""
        request = self.make_request('git_data.commits.get', sha=sha,
                                       user=user, repo=repo)
        return self._get(request)

    def create(self, data, user=None, repo=None):
        """create a commit on a repo

        :param dict data: Input. See `github commits doc`_
        :param str user: username
        :param str repo: repository name

        """
        return self._post(
            self.make_request('git_data.commits.create', user=user, repo=repo,
                              body=data)
        )



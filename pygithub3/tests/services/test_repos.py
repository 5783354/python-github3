#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase

import requests
from mock import patch, Mock

from pygithub3.services.repos import Repo, Collaborator
from pygithub3.resources.base import json
from pygithub3.tests.utils.base import mock_response, mock_response_result
from pygithub3.tests.utils.services import _, mock_json

json.dumps = Mock(side_effect=mock_json)
json.loads = Mock(side_effect=mock_json)


@patch.object(requests.sessions.Session, 'request')
class TestRepoService(TestCase):

    def setUp(self):
        self.rs = Repo()
        self.rs.set_user('octocat')
        self.rs.set_repo('octocat_repo')

    def test_LIST_without_user(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.set_user('')
        self.rs.list().all()
        self.assertEqual(request_method.call_args[0], ('get', _('user/repos')))

    def test_LIST_with_user_in_args(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list('octoc').all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('users/octoc/repos')))

    def test_LIST_with_user_in_service(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('users/octocat/repos')))

    def test_LIST_filters(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list('octoc', type='public').all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('users/octoc/repos')))
        self.assertEqual(request_method.call_args[1]['params']['type'],
                         'public')

    def test_LIST_BY_ORG(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_by_org('org_name').all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('orgs/org_name/repos')))

    def test_LIST_BY_ORG_filters(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_by_org('org_name', type='public').all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('orgs/org_name/repos')))
        self.assertEqual(request_method.call_args[1]['params']['type'],
                         'public')

    def test_CREATE(self, request_method):
        request_method.return_value = mock_response('post')
        self.rs.create({'name': 'test'})
        self.assertEqual(request_method.call_args[0],
                         ('post', _('user/repos')))

    def test_CREATE_in_org(self, request_method):
        request_method.return_value = mock_response('post')
        self.rs.create({'name': 'test'}, in_org='org_name')
        self.assertEqual(request_method.call_args[0],
                         ('post', _('orgs/org_name/repos')))

    def test_GET_with_repo_in_args(self, request_method):
        request_method.return_value = mock_response()
        self.rs.get(user='user', repo='repo')
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/user/repo')))

    def test_GET_with_repo_in_service(self, request_method):
        request_method.return_value = mock_response()
        self.rs.get()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo')))

    def test_UPDATE_with_repo_in_args(self, request_method):
        request_method.return_value = mock_response('patch')
        self.rs.update({'name': 'test'}, user='user', repo='repo')
        self.assertEqual(request_method.call_args[0],
                         ('patch', _('repos/user/repo')))

    def test_UPDATE_with_repo_in_service(self, request_method):
        request_method.return_value = mock_response('patch')
        self.rs.update({'name': 'test'})
        self.assertEqual(request_method.call_args[0],
                         ('patch', _('repos/octocat/octocat_repo')))

    """ From here I stop to do '*in_args' and '*filter' tests, I consider
    that I tested it enough... """

    def test_LIST_contributors(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_contributors().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/contributors')))

    def test_LIST_contributors_with_anonymous(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_contributors_with_anonymous().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/contributors')))
        self.assertEqual(request_method.call_args[1]['params']['anom'], True)

    def test_LIST_languages(self, request_method):
        request_method.return_value = mock_response()
        self.rs.list_languages()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/languages')))

    def test_LIST_teams(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_teams().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/teams')))

    def test_LIST_tags(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_tags().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/tags')))

    def test_LIST_branches(self, request_method):
        request_method.return_value = mock_response_result()
        self.rs.list_branches().all()
        self.assertEqual(request_method.call_args[0],
                         ('get', _('repos/octocat/octocat_repo/branches')))


@patch.object(requests.sessions.Session, 'request')
class TestCollaboratorsService(TestCase):

    def setUp(self):
        self.cs = Collaborator()
        self.cs.set_user('octocat')
        self.cs.set_repo('oc_repo')

    def test_LIST(self, request_method):
        request_method.return_value = mock_response_result()
        self.cs.list().all()
        self.assertEqual(request_method.call_args[0],
            ('get', _('repos/octocat/oc_repo/collaborators')))

    def test_IS_colaborator(self, request_method):
        request_method.return_value = mock_response()
        self.cs.is_collaborator('user')
        self.assertEqual(request_method.call_args[0],
            ('head', _('repos/octocat/oc_repo/collaborators/user')))

    def test_ADD(self, request_method):
        self.cs.add('user')
        self.assertEqual(request_method.call_args[0],
            ('put', _('repos/octocat/oc_repo/collaborators/user')))

    def test_DELETE(self, request_method):
        request_method.return_value = mock_response('delete')
        self.cs.delete('user')
        self.assertEqual(request_method.call_args[0],
            ('delete', _('repos/octocat/oc_repo/collaborators/user')))

from pygithub3.exceptions import BadRequest, NotFound
from pygithub3.services.base import Service, MimeTypeMixin
from .comments import Comments


class PullRequests(Service, MimeTypeMixin):
    """Consume `Pull Request API <http://developer.github.com/v3/pulls/>`_"""

    def __init__(self, **config):
        self.comments = Comments(**config)
        super(PullRequests, self).__init__(**config)

    def list(self, user=None, repo=None):
        """List all of the pull requests for a repo

        :param str user: Username
        :param str repo: Repository

        """
        return self._get_result(
            self.make_request('pull_requests.list', user=user, repo=repo)
        )

    def get(self, number, user=None, repo=None):
        """Get a single pull request

        :param str number: The number of the pull request to get
        :param str user: Username
        :param str repo: Repository

        """
        return self._get(
            self.make_request('pull_requests.get', number=number, user=user,
                              repo=repo)
        )

    def create(self, body, user=None, repo=None):
        """Create a pull request

        :param dict body: Data for the new pull request
        :param str user: Username
        :param str repo: Repository

        """
        return self._post(
            self.make_request('pull_requests.create', body=body, user=user,
                              repo=repo)
        )

    def update(self, number, body, user=None, repo=None):
        """Update a pull request

        :param str number: The number of the the pull request to update
        :param dict body: The data to update the pull request with
        :param str user: Username
        :param str repo: Repository

        """
        return self._patch(
            self.make_request('pull_requests.update', number=number,
                              body=body, user=user, repo=repo)
        )

    def list_commits(self, number, user=None, repo=None):
        """List the commits for a pull request

        :param str number: The number of the pull request to list commits for
        :param str user: Username
        :param str repo: Repository

        """
        return self._get_result(
            self.make_request('pull_requests.list_commits', number=number,
                              user=user, repo=repo)
        )

    def list_files(self, number, user=None, repo=None):
        """List the files for a pull request

        :param str number: The number of the pull request to list files for
        :param str user: Username
        :param str repo: Repository

        """
        return self._get_result(
            self.make_request('pull_requests.list_files', number=number,
                              user=user, repo=repo)
        )

    def merge_status(self, number, user=None, repo=None):
        """Gets whether a pull request has been merged or not.

        :param str number: The pull request to check
        :param str user: Username
        :param str repo: Repository

        """
        # for this to work with a proper Resource, we would need to pass the
        # response's status code to the Resource constructor, and that's kind
        # of scary
        try:
            resp = self._client.get(
                self.make_request('pull_requests.merge_status', number=number,
                                user=user, repo=repo)
            )
        except NotFound:
            return False
        code = resp.status_code
        if code == 204:
            return True
        # TODO: more flexible way to return arbitrary objects based on
        # response.  Probably something on Request
        raise BadRequest('got code %s: %s' % (code, resp.content))
        # again, I'm sorry.

    def merge(self, number, message='', user=None, repo=None):
        """Merge a pull request.

        :param str number: The pull request to merge
        :param str user: Username
        :param str repo: Repository

        This currently raises an HTTP 405 error if the request is not
        mergable.

        """
        body = {'commit_message': message}
        return self._put(
            self.make_request('pull_requests.merge', number=number,
                              body=body, user=user, repo=repo)
        )

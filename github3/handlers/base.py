#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author: David Medina

from github3.core import Paginate
from github3.converters import Modelizer

class Handler(object):
    """ Handler base. Requests to API and modelize responses """

    def __init__(self, gh):
        self._gh = gh
        super(Handler, self).__init__()

    def _prefix_resource(self, resource):
        prefix = getattr(self, 'prefix', '')
        return '/'.join((prefix, resource))

    def _get_converter(self, kwargs):
        converter = kwargs.get(
            'converter', # 1. in kwargs
            getattr(self, 'converter', # 2. in handler
            Modelizer())) # 3. Default

        return converter

    def _bool(self, resource, **kwargs):
        """ Handler request to boolean response """

        from github3.exceptions import NotFound
        resource = self._prefix_resource(resource)
        try:
            response = self._gh.head(resource, **kwargs)
        except NotFound:
            return False
        assert response.status_code == 204
        return True

    #TODO: if limit is multiple of per_page... it do another request for nothing
    def _get_resources(self, resource, model=None, limit=None, **kwargs):
        """ Hander request to multiple resources """

        resource = self._prefix_resource(resource)
        page_resources = Paginate(resource, self._gh.get)
        counter = 1
        for page in page_resources:
            for raw_resource in page:
                if limit and counter > limit: break
                counter += 1
                converter = self._get_converter(kwargs)
                converter.inject(model)
                yield converter.loads(raw_resource)
            else:
                continue
            break

    def _get_resource(self, resource, model=None, **kwargs):
        """ Handler request to single resource """

        resource = self._prefix_resource(resource)
        raw_resource = self._gh.get(resource)
        converter = self._get_converter(kwargs)
        converter.inject(model)
        return converter.loads(raw_resource)

    def _post_resource(self, resource, data, model=None, **kwargs):
        """ Handler request to create a resource """

        resource = self._prefix_resource(resource)
        raw_resource = self._gh.post(resource, data=data)
        converter = self._get_converter(kwargs)
        converter.inject(model)
        return converter.loads(raw_resource)

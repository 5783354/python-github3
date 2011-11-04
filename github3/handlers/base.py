#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author: David Medina

class Handler(object):
    """ Abstract handler, that inject github.api """

    def __init__(self, gh):
        self._gh = gh
        super(Handler, self).__init__()

    def _extend_url(self, *args):
        return self._url + args

    def _get_raw(self, *args, **kwargs):
        url = self._extend_url(*args)
        return self._gh._get_raw(url, **kwargs)

    def _get_bool(self, *args):
        url = self._extend_url(*args)
        return self._gh._get_bool(url)

    def _get_resource(self, *args, **kwargs):
        url = self._extend_url(*args)
        map_model = kwargs.get('model', self._model)
        return self._gh._get_resource(url, map_model, **kwargs)

    def _get_resources(self, *args, **kwargs):
        url = self._extend_url(*args)
        map_model = kwargs.get('model', self._model)
        return self._gh._get_resources(url, map_model, **kwargs)

    def _post_raw(self, *args, **kwargs):
        url = self._extend_url(*args)
        return self._gh._post_raw(url, **kwargs)

    def _delete_raw(self, *args, **kwargs):
        url = self._extend_url(*args)
        return self._gh._delete_raw(url, **kwargs)


#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from .core import Converter


class Rawlizer(Converter):
    """ Raw converter """

    def inject(self, fake):
        pass

    def loads(self, raw_resource):
        return raw_resource

    def dumps(self):
        pass


class Json(Converter):
    """ Json converter """

    def __init__(self):
        import json
        self.parser = json

    def inject(self, fake):
        pass

    def loads(self, raw_resource):
        return self.parser.dumps(raw_resource)

    def dumps(self):
        pass


class Modelizer(Converter):
    """ Own model converter """

    def __init__(self, model=None):
        if model:
            self.inject(model)

    def _parse_date(self, string_date):
        from datetime import datetime
        try:
            date = datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%SZ')
        except TypeError:
            date = None

        return date

    def inject(self, model):
        self.model = model

    def _parse_map(self, model, raw_resource):
        if hasattr(raw_resource, 'items'):
            return Modelizer(model).loads(raw_resource)

    def _parse_collection_map(self, model, raw_resources):
        # Dict of resources (Ex: Gist file)
        if hasattr(raw_resources, 'items'):
            dict_map = {}
            for key, raw_resource in raw_resources.items():
                dict_map[key] = Modelizer(model).loads(raw_resource)
            return dict_map
        # list of resources
        elif hasattr(raw_resources, '__iter__'):
            return [Modelizer(model).loads(raw_resource)
                    for raw_resource in raw_resources]

    def loads(self, raw_resource):
        attrs = {}
        if not getattr(self, 'model', False):
            raise NotImplementedError("%s needs model attr" %
                self.__class__.__name__)
        idl = self.model.idl()
        attrs.update(
            {attr: raw_resource[attr] for attr in idl.get('strs', ())
             if attr in raw_resource})
        attrs.update(
            {attr: raw_resource[attr] for attr in idl.get('ints', ())
             if attr in raw_resource})
        attrs.update(
            {attr: self._parse_date(raw_resource[attr])
             for attr in idl.get('dates', ()) if attr in raw_resource})
        attrs.update(
            {attr: raw_resource[attr] for attr in idl.get('bools', ())
             if attr in raw_resource})
        attrs.update(
            {attr: self._parse_map(model, raw_resource[attr])
             for attr, model in idl.get('maps', {}).items()
             if attr in raw_resource})
        attrs.update(
            {attr: self._parse_collection_map(model, raw_resource[attr])
             for attr, model in idl.get('collection_maps', {}).items()
             if attr in raw_resource})

        return self.model(attrs)

    def dumps(self, model):
        # return JSON
        pass

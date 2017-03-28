# -*- coding: utf-8 -*-

import json


class Documentation(object):

    HUG_TYPE_TRANSLATION = {
        'A Whole number': 'integer',
        'Accepts a JSON formatted data structure': 'object',
        'Basic text / string value': 'string',
        'Multiple Values': 'array',
    }

    def __init__(self, hug_doc, version='1.0', title='REST API', host='localhost', schemas=None, consumes=None, produces=None):
        self._content = {
            'swagger': '2.0',
            'info': {
                'version': version,
                'title': title,
            },
            'host': host,
            'schemes': ['http'] if schemas is None else schemas,
            'consumes': ['application/json'] if consumes is None else consumes,
            'produces': ['application/json'] if produces is None else produces,
            'paths': {},
        }
        self.parse_hug_doc(hug_doc)

    def parse_hug_doc(self, hug_doc):
        for url, spec in hug_doc.items():
            self._content['paths'][url] = {}
            for method, detail in spec.items():
                self._content['paths'][url][method.lower()] = {
                    'description': detail.get('usage', url),
                    'parameters': [{
                        'name': k,
                        'in': 'query' if method == 'GET' else 'body',
                        'required': 'default' not in v,
                        'type': self.HUG_TYPE_TRANSLATION.get(v.get('type', ''), 'any'),
                    } for k, v in detail.get('inputs', {}).items()],
                    'responses': {
                        '200': {
                            'description': 'Success',
                        }
                    }
                }

    @property
    def content(self):
        return json.dumps(self._content)

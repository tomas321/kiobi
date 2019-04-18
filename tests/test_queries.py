#!/usr/bin/env python3

from copy import deepcopy
from unittest import TestCase

from kiobi.kibana_objects import query

dummy_host = 'dummy_host:1111'

retrieve_all_objects_request_params = {
    'host': dummy_host,
    'page': "1",
    'per_page': "20"
}
expected_retrieve_all_objects_request = {
    "url": "{}/api/saved_objects/_find?type=visualization&type=search&type=index-pattern&type=dashboard&per_page=20&page=1".format(
        dummy_host)
}

retrieve_objects_by_title_params = {
    'host': dummy_host,
    'pattern': 'my_title*'
}
expected_retrieve_all_objects_by_title = {
    "url": "{}/api/saved_objects/_find?type=visualization&type=search&type=index-pattern&type=dashboard&search={}&search_fields=title".format(
        dummy_host, retrieve_objects_by_title_params['pattern'])
}
expected_retrieve_specific_objects_by_title = {
    "url": "{}/api/saved_objects/_find?type=visualization&type=search&type=index-pattern&type=dashboard&search={}&search_fields=title".format(
        dummy_host, retrieve_objects_by_title_params['pattern'])
}

expexted_data = [
    {
        "type": "dashboard",
        "id": "dummy_id",
        "attributes": {},
        "updated_at": "2019-04-18T08:45:25.555Z",
        "version": "1122"
    },
    {
        "type": "visualization",
        "id": "dummy_id2",
        "attributes": {},
        "updated_at": "2019-04-12T08:45:25.555Z",
        "version": "1133"
    }
]
expected_bulk_create_request = {
    'url': '{}/api/saved_objects/_bulk_create'.format(dummy_host),
    'data': expexted_data
}


class TestQueries(TestCase):

    def test_retrieve_all_objects_request_should_compose_correctly(self):
        actual_request = query.retrieve_all_saved_objects_request_uri(**retrieve_all_objects_request_params)

        self.assertDictEqual(actual_request, expected_retrieve_all_objects_request)

    def test_retrieve_objects_by_title_should_compose_correctly_without_specific_type(self):
        actual_request = query.retrieve_saved_objects_by_title(**retrieve_objects_by_title_params)

        self.assertDictEqual(actual_request, expected_retrieve_all_objects_by_title)

    def test_retrieve_objects_by_title_should_compose_correctly_with_specific_type(self):
        params = deepcopy(retrieve_objects_by_title_params)
        params['types'] = ['visualization', 'search', 'index-pattern', 'dashboard']
        actual_request = query.retrieve_saved_objects_by_title(**params)

        self.assertDictEqual(actual_request, expected_retrieve_all_objects_by_title)

    def test_bulk_create_objects_request_should_compose_correctly(self):
        actual_request = query.bulk_create_objects_query(dummy_host, expexted_data)

        self.assertDictEqual(actual_request, expected_bulk_create_request)

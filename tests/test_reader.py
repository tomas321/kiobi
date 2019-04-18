#!/usr/bin/env python3

from ast import literal_eval
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from kiobi.kibana_objects.push.reader import read_objects_file

dummy_filepath = "/path/to/saved/objects.json"
test_saved_objects = '''{
    "page": 1,
    "per_page": 20,
    "total": 3,
    "saved_objects": [
        {
            "type": "dashboard",
            "id": "dashboard:id",
            "attributes": {},
            "updated_at": "2019-04-18T08:45:25.555Z",
            "version": "112233"
        },
        {
            "type": "dashboard",
            "id": "dashboard:id2",
            "attributes": {},
            "updated_at": "2019-04-18T08:56:25.555Z",
            "version": "112233"
        },
        {
            "type": "search",
            "id": "search:id",
            "attributes": {},
            "version": "112233"
        }
    ]
}'''
expected_saved_objects = {
    "page": 1,
    "per_page": 20,
    "total": 3,
    "saved_objects": [
        {
            "type": "dashboard",
            "id": "dashboard:id",
            "attributes": {},
            "version": "112233"
        },
        {
            "type": "dashboard",
            "id": "dashboard:id2",
            "attributes": {},
            "version": "112233"
        },
        {
            "type": "search",
            "id": "search:id",
            "attributes": {},
            "version": "112233"
        }
    ]
}


class TestKibanaObjectsReader(TestCase):

    @patch("kiobi.kibana_objects.push.reader.open")
    def test_reader_should_remove_updated_at_field_from_objects(self, open_mock):
        open_mock.return_value.__enter__.return_value = StringIO(initial_value=test_saved_objects)

        objects = read_objects_file(dummy_filepath)
        self.assertDictEqual(literal_eval(objects), expected_saved_objects)

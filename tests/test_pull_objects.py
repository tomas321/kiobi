#!/usr/bin/env python3

from copy import deepcopy
from unittest.mock import MagicMock
from unittest import TestCase

all_objects_expected_reply = {
  "page": 1,
  "per_page": 20,
  "total": 2,
  "saved_objects": [
    {
      "type": "visualization",
      "id": "aaaaaaaaaaaa",
      "attributes": {
        "title": "dummy-time-characteristics"
      },
      "version": 1
    },
    {
      "type": "visualization",
      "id": "bbbbbbbbbbbb",
      "attributes": {
        "title": "normal-distribution"
      },
      "version": 2
    }
  ]
}

class TestPullObjectsToKibana(TestCase):

    def test_retrieving_all_objects_should_succeed(self):
        request_mock = MagicMock()
        all_objects_reply = deepcopy(all_objects_expected_reply)
        # call function from pull_objects

        request_mock.get.return_value = all_objects_reply
        # processing is called once with ...

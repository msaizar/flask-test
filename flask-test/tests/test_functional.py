# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for
import json
from .factories import FeatureFactory


class TestFunctional:

    def test_can_get_homepage(self, db, testapp):
        """Homepage works."""
        res = testapp.get('/')
        assert res.status_int == 200

    def test_client_selection_list(self, db, testapp):
        """
        Client list is Client A, Client B, Client C, anything else should
        return an error
        """
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client B',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client C',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client D',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        }, status=400)
        assert res.status_int == 400

    def test_product_area_selection_list(self, db, testapp):
        """
        Product Area list is Policies, Billing, Claims, Reports, anything else
        should return an error
        """
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Billing', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client B',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Claims', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client C',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Reports', 'description': 'Some Description'
        })
        assert res.status_int == 200
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client C',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200

        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client B',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Invalid', 'description': 'Some Description'
        }, status=400)
        assert res.status_int == 400

    def test_client_priority_reordering(self, db, testapp):
        """
        Client Priority numbers should not repeat for the given client,
        so if a priority is set on a new feature as "1", then all other
        feature requests for that client should be reordered.

        4 features, priority 1 to 4. We'll post a new feature with priority 1.
        Other priorities should add 1.
        """
        feature_1 = FeatureFactory(client='Client A', client_priority=1)
        feature_2 = FeatureFactory(client='Client A', client_priority=2)
        feature_3 = FeatureFactory(client='Client A', client_priority=3)
        feature_4 = FeatureFactory(client='Client A', client_priority=4)

        db.session.commit()
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert feature_1.client_priority == 2
        assert feature_2.client_priority == 3
        assert feature_3.client_priority == 4
        assert feature_4.client_priority == 5

        # Update an existing feature, see if it still adds 1 to the others
        res = testapp.put('/features/1', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '4', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })

        assert feature_1.client_priority == 4
        assert feature_2.client_priority == 3
        assert feature_3.client_priority == 5
        assert feature_4.client_priority == 6

        # Make sure features for other clients dont reorder the others
        res = testapp.post('/features/', {
            'title': 'Another Title', 'client': 'Client B',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert feature_1.client_priority == 4
        assert feature_2.client_priority == 3
        assert feature_3.client_priority == 5
        assert feature_4.client_priority == 6

# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for
import json
from .factories import FeatureFactory


class TestFeaturesAPI:

    def test_can_get_homepage(self, db, testapp):
        """Homepage works."""
        # Goes to homepage
        res = testapp.get('/')
        assert res.status_int == 200

    def test_get_list(self, db, testapp):
        """Show alert on logout."""
        res = testapp.get('/features/')
        result = res.json
        assert res.status_int == 200
        assert len(result['features']) == 0
        feature_1 = FeatureFactory()
        feature_2 = FeatureFactory()
        db.session.commit()
        res = testapp.get('/features/')
        result = res.json
        assert len(result['features']) == 2

    def test_get_single(self, db, testapp):
        """Show alert on logout."""
        res = testapp.get('/features/1', status=404)
        feature_1 = FeatureFactory()
        db.session.commit()
        res = testapp.get('/features/1')
        result = res.json
        assert 'feature' in result
        assert result['feature']['id'] == 1
        assert res.status_int == 200

    def test_post_invalid(self, db, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.post('/features/', status=400)
        result = res.json
        assert 'errors' in result
        assert 'client' in result['errors']
        assert 'client_priority' in result['errors']
        assert 'description' in result['errors']
        assert 'product_area' in result['errors']
        assert 'target_date' in result['errors']
        assert 'title' in result['errors']
        assert res.status_int == 400

    def test_post_valid(self, db, testapp):
        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200

    def test_put_valid(self, db, testapp):
        feature_1 = FeatureFactory()
        db.session.commit()
        res = testapp.put('/features/1', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200

    def test_put_invalid(self, db, testapp):
        feature_1 = FeatureFactory()
        db.session.commit()
        res = testapp.put('/features/1', status=400)
        result = res.json
        assert 'errors' in result
        assert 'client' in result['errors']
        assert 'client_priority' in result['errors']
        assert 'description' in result['errors']
        assert 'product_area' in result['errors']
        assert 'target_date' in result['errors']
        assert 'title' in result['errors']
        assert res.status_int == 400

    def test_delete(self, db, testapp):
        res = testapp.delete('/features/1', status=404)
        feature_1 = FeatureFactory()
        res = testapp.delete('/features/1')
        assert res.status_int == 200

    def test_client_priority_reordering(self, db, testapp):
        """
        4 features, priority 1 to 4. We'll post a new feature with priority 1.
        Other features should be updated.
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

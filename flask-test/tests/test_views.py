# -*- coding: utf-8 -*-
"""View tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for
import json
from .factories import FeatureFactory


class TestFeaturesAPI:
    """
    Features API endpoint tests.
    """

    def test_get_list(self, db, testapp):
        """
        Test feature list endpoint, make sure the
        correct number of items are returned
        """

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
        """
        get single feature endpoint, 404 if no feature is found,
        200 and feature if it found
        """

        res = testapp.get('/features/1', status=404)
        feature_1 = FeatureFactory()
        db.session.commit()
        res = testapp.get('/features/1')
        result = res.json
        assert 'feature' in result
        assert result['feature']['id'] == 1
        assert res.status_int == 200

    def test_post_invalid(self, db, testapp):
        """post empty feature, check that all errors are there"""

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
        """post valid feature, returns 200"""

        res = testapp.post('/features/', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200

    def test_put_valid(self, db, testapp):
        """update valid feature, returns 200"""

        feature_1 = FeatureFactory()
        db.session.commit()
        res = testapp.put('/features/1', {
            'title': 'Some Title', 'client': 'Client A',
            'client_priority': '1', 'target_date': '2020-10-10',
            'product_area': 'Policies', 'description': 'Some Description'
        })
        assert res.status_int == 200

    def test_put_invalid(self, db, testapp):
        """udpate invalid feature, returns 400, check all errors are there"""

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
        """
        delete single feature endpoint, 404 if no feature is found,
        200 if found
        """
        res = testapp.delete('/features/1', status=404)
        feature_1 = FeatureFactory()
        res = testapp.delete('/features/1')
        assert res.status_int == 200

# -*- coding: utf-8 -*-
"""Model unit tests."""
from app.database import db
import datetime as dt

import pytest

from .factories import FeatureFactory


@pytest.mark.usefixtures('db')
class TestFeatureModel:
    """Feature Model tests."""

    def test_repr(self):
        feature = FeatureFactory(
            title="Title", description="Description", client="Client A",
            client_priority=1, target_date=dt.date(2020, 10, 10),
            product_area="Policies"
        )
        assert feature.__repr__() == '<Feature Title>'

    def test_to_json(self):
        """Convert model to JSON."""
        feature = FeatureFactory(
            title="Title", description="Description", client="Client A",
            client_priority=1, target_date=dt.date(2020, 10, 10),
            product_area="Policies"
        )
        db.session.commit()
        obj = {
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'client': feature.client,
            'client_priority': feature.client_priority,
            'target_date': '2020-10-10',
            'product_area': feature.product_area
        }
        serialized = feature.to_json()
        assert serialized == obj

        feature = FeatureFactory(
            title="Title", description="Description", client="Client A",
            client_priority=1, target_date=None,
            product_area="Policies"
        )
        db.session.commit()
        obj = {
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'client': feature.client,
            'client_priority': feature.client_priority,
            'target_date': None,
            'product_area': feature.product_area
        }
        serialized = feature.to_json()
        assert serialized == obj

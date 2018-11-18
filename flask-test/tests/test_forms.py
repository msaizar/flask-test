# -*- coding: utf-8 -*-
"""Test forms."""
import datetime
from app.feature.forms import FeatureForm


class TestFeatureForm:
    """Feature form"""

    def test_validate_success(self, db):
        """Register with success."""
        form = FeatureForm(
            title='Some Title', description='Some Description',
            client='Client A', client_priority=1,
            target_date=datetime.date(2020, 10, 10), product_area='Policies'
        )
        assert form.validate() is True

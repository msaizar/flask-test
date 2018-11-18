# -*- coding: utf-8 -*-
"""Factories to help in tests."""
import datetime
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDate

from app.database import db
from app.feature.models import Feature


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class FeatureFactory(BaseFactory):
    """Feature factory."""

    title = Sequence(lambda n: 'Feature {0}'.format(n))
    description = Sequence(lambda n: 'Description {0}'.format(n))
    client = FuzzyChoice(['Client A', 'Client B', 'Client C'])
    client_priority = Sequence(lambda n: n)
    target_date = FuzzyDate(datetime.date.today())
    product_area = FuzzyChoice(['Policies', 'Billing', 'Claims', 'Reports'])

    class Meta:
        """Factory configuration."""
        model = Feature

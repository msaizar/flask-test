from app import app
from app.database import db
from .forms import FeatureForm
from .models import Feature
from flask import render_template, flash, redirect, url_for, jsonify, Blueprint
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound


blueprint = Blueprint('feature', __name__, static_folder='../static')


class FeatureAPI(MethodView):

    def get(self, feature_id):
        """
        If an id is present, return the serialized feature or return a 404.
        If not return a serialized feature list ordered by client and priority.
        """

        if feature_id is None:
            return jsonify(
                features=[i.to_json() for i in Feature.query.order_by(
                    Feature.client.asc(), Feature.client_priority.desc()
                    )]
                )
        else:
            feature = Feature.query.get_or_404(feature_id)
            return jsonify(feature=feature.to_json())

    def delete(self, feature_id):
        f = Feature.query.get_or_404(feature_id)
        db.session.delete(f)
        db.session.commit()
        return jsonify({'success': True})

    def process_feature(self, feature, form):
        """
        Add/Update a feature
        Method to be used for post/put requests.

        Find features with the new priority and count them

        While there are two of them:
            Increment the priority of the one that is not the new/last updated
            Find features with the new priority and count them

        #TODO: I'm returning all features, replacing the
        entire array on the frontend. Ideally we should only return
        the objects that were updated, and update only those
        on the frontend.
        """

        db.session.add(feature)

        client = form.client.data
        client_priority = form.client_priority.data

        feature_query = Feature.query.filter_by(
            client=client,
            client_priority=client_priority
        )
        existing_features_count = feature_query.count()

        last_updated = feature

        while existing_features_count > 1:
            feature_to_update = feature_query.filter(
                Feature.id != last_updated.id
            ).first()
            client_priority += 1
            feature_to_update.client_priority = client_priority
            feature_query = Feature.query.filter_by(
                client=client,
                client_priority=client_priority
            )
            existing_features_count = feature_query.count()
            last_updated = feature_to_update

        db.session.commit()
        return jsonify(features=[
            i.to_json() for i in Feature.query.order_by(
                Feature.client.asc(), Feature.client_priority.desc()
            )
        ])

    def put(self, feature_id):
        """
        Returns all features or form errors as JSON.
        """
        form = FeatureForm()
        if form.validate():
            feature = Feature.query.get(feature_id)
            form.populate_obj(feature)
            return self.process_feature(feature, form)
        else:
            return jsonify(errors=form.errors), 400

    def post(self):
        """
        Returns all features or form errors as JSON.
        """
        form = FeatureForm()
        if form.validate():
            feature = Feature()
            form.populate_obj(feature)
            return self.process_feature(feature, form)
        else:
            return jsonify(errors=form.errors), 400


@blueprint.route('/', methods=['GET'])
def homepage():
    """
    Homepage, returns the main app frontend with the form.

    #TODO: Move form to the frontend. Everything but initial display is
    being processed there.
    """

    form = FeatureForm()
    return render_template('index.html', form=form)


feature_view = FeatureAPI.as_view('feature_api')
blueprint.add_url_rule(
    '/features/', defaults={'feature_id': None},
    view_func=feature_view, methods=['GET']
)
blueprint.add_url_rule('/features/', view_func=feature_view, methods=['POST'])
blueprint.add_url_rule(
    '/features/<int:feature_id>', view_func=feature_view,
    methods=['GET', 'PUT', 'DELETE']
)

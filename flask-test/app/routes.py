from app import app, db
from app.forms import FeatureCreateForm
from app.models import Feature
from flask import render_template, flash, redirect, url_for, jsonify
from flask.views import MethodView


class FeatureAPI(MethodView):

    def get(self, feature_id):
        if feature_id is None:
            return jsonify(
                features=[i.to_json() for i in Feature.query.order_by(
                    Feature.client.asc(), Feature.client_priority.desc()
                    )]
                )
        else:
            return jsonify(feature=Feature.query.get(feature).to_json())

    def delete(self, feature_id):
        f = Feature.query.get(feature_id)
        db.session.delete(f)
        db.session.commit()
        return jsonify({'success': True})

    def process_feature(self, feature, form):
        db.session.add(feature)

        client = form.client.data
        client_priority = form.client_priority.data

        feature_query = Feature.query.filter_by(
            client=client,
            client_priority=client_priority
        )
        existing_features_count = feature_query.count()

        while existing_features_count > 1:
            feature_to_update = feature_query.first()
            client_priority += 1
            feature_to_update.client_priority = client_priority
            feature_query = Feature.query.filter_by(
                client=client,
                client_priority=client_priority
            )
            existing_features_count = feature_query.count()
        db.session.commit()
        return jsonify(features=[
            i.to_json() for i in Feature.query.order_by(
                Feature.client.asc(), Feature.client_priority.desc()
            )
        ])

    def put(self, feature_id):
        form = FeatureCreateForm()
        if form.validate():
            feature = Feature.query.get(feature_id)
            form.populate_obj(feature)
            return self.process_feature(feature, form)
        else:
            return jsonify(errors=form.errors), 400

    def post(self):
        form = FeatureCreateForm()
        if form.validate():
            feature = Feature()
            form.populate_obj(feature)
            return self.process_feature(feature, form)
        else:
            return jsonify(errors=form.errors), 400


@app.route('/', methods=['GET'])
def homepage():
    form = FeatureCreateForm()
    return render_template('index.html', form=form)


feature_view = FeatureAPI.as_view('feature_api')
app.add_url_rule('/features/', defaults={'feature_id': None},
                 view_func=feature_view, methods=['GET'])
app.add_url_rule('/features/', view_func=feature_view, methods=['POST'])
app.add_url_rule('/features/<int:feature_id>', view_func=feature_view,
                 methods=['GET', 'PUT', 'DELETE'])

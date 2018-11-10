from app import app, db
from app.forms import FeatureCreateForm
from app.models import Feature
from flask import render_template, flash, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def feature_create():
    form = FeatureCreateForm()
    if form.validate_on_submit():
        feature = Feature(
            title=form.title.data,
            description=form.description.data,
            client=form.client.data,
            client_priority=form.client_priority.data,
            target_date=form.target_date.data,
            product_area=form.product_area.data
        )
        
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

        flash('Feature request for {} created'.format(form.client.data))
        return redirect(url_for('feature_create'))
    return render_template('index.html', form=form)
    

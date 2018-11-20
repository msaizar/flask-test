function FeaturesViewModel() {
    var self = this;
    self.featuresURI = '/features/';
    self.features = ko.observableArray();
    self.show = ko.observable(true);
    
    
    self.ajax = function(uri, method, data) {
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
            }
        };
        return $.ajax(request);
    }

    self.beginAdd = function() {
        self.show(false);
        featureFormViewModel.cleanForm();
        featureFormViewModel.show(true);
    }
    self.beginEdit = function(feature) {
        self.show(false);
        featureFormViewModel.setForm(feature);
        featureFormViewModel.show(true);
    }

    self.remove = function(feature) {
        var uri = self.featuresURI + feature.id();
        self.ajax(uri, 'DELETE', feature).done(function(data) {
            self.features.remove(feature);
        });
    }

    self.initFeaturesArray = function(data) {
        self.features.removeAll();
        for (var i = 0; i < data.features.length; i++) {
            self.features.push({
                id: ko.observable(data.features[i].id),
                title: ko.observable(data.features[i].title),
                description: ko.observable(data.features[i].description),
                client: ko.observable(data.features[i].client),
                client_priority: ko.observable(data.features[i].client_priority),
                target_date: ko.observable(data.features[i].target_date),
                product_area: ko.observable(data.features[i].product_area)
            });
        }
        featureFormViewModel.show(false);
        self.show(true);
        
    }
    self.ajax(self.featuresURI, 'GET').done(function(data) {
        self.initFeaturesArray(data);
    });


    self.saveFeature = function(feature) {
        if (feature.id != undefined) {
            var uri = self.featuresURI + feature.id;
            var method = 'PUT';
        }
        else {
            var uri = self.featuresURI;
            var method = 'POST';
        }
        self.ajax(uri, method, feature).done(function(data) {
            self.initFeaturesArray(data);
        }).fail(function (data) {
            featureFormViewModel.formErrors(data.responseJSON);
        });
    }
}


function FeatureFormViewModel() {
    var self = this;
    self.id = ko.observable();
    self.title = ko.observable();
    self.description = ko.observable();
    self.client = ko.observable();
    self.client_priority = ko.observable();
    self.target_date = ko.observable();
    self.product_area = ko.observable();
    
    self.title_errors = ko.observableArray();
    self.description_errors = ko.observableArray();
    self.client_errors = ko.observableArray();
    self.client_priority_errors = ko.observableArray();
    self.target_date_errors = ko.observableArray();
    self.product_area_errors = ko.observableArray();
    
    self.show = ko.observable(false);
    self.removeFormErrors = function() {
        self.title_errors.removeAll();
        self.description_errors.removeAll();
        self.client_errors.removeAll();
        self.client_priority_errors.removeAll();
        self.target_date_errors.removeAll();
        self.product_area_errors.removeAll();
    }
    
    self.cleanForm = function() {
        self.id(null)
        self.title('');
        self.description('');
        self.client('');
        self.client_priority('');
        self.target_date('');
        self.product_area('');
        self.removeFormErrors();
    }
    
    self.setForm = function(feature) {
        self.id(feature.id())
        self.title(feature.title());
        self.description(feature.description());
        self.client(feature.client());
        self.client_priority(feature.client_priority());
        self.target_date(feature.target_date());
        self.product_area(feature.product_area());
        self.removeFormErrors();
    }

    self.formErrors = function(response) {
        self.removeFormErrors();

        $.each(response.errors.title, function(i, e) {
            self.title_errors.push(e)
        })
        $.each(response.errors.description, function(i, e) {
            self.description_errors.push(e)
        })
        $.each(response.errors.client, function(i, e) {
            self.client_errors.push(e)
        })
        $.each(response.errors.client_priority, function(i, e) {
            self.client_priority_errors.push(e)
        })
        $.each(response.errors.target_date, function(i, e) {
            self.target_date_errors.push(e)
        })
        $.each(response.errors.product_area, function(i, e) {
            self.product_area_errors.push(e)
        })
        
    }
    self.cancel = function() {
        self.show(false);
        featuresViewModel.show(true);
    }
    self.saveFeature = function() {
        if (self.id() != undefined) {
            var new_feature = {
                id: self.id(),
                title: self.title(),
                description: self.description(),
                client: self.client(),
                client_priority: self.client_priority(),
                target_date: self.target_date(),
                product_area: self.product_area(),
            }
        }
        else {
            var new_feature = {
                title: self.title(),
                description: self.description(),
                client: self.client(),
                client_priority: self.client_priority(),
                target_date: self.target_date(),
                product_area: self.product_area(),
            }
        }
        featuresViewModel.saveFeature(new_feature);
    }
}
var featuresViewModel = new FeaturesViewModel();
var featureFormViewModel = new FeatureFormViewModel();
ko.applyBindings(featuresViewModel, $('#feature_list')[0]);
ko.applyBindings(featureFormViewModel, $('#feature_form')[0]);

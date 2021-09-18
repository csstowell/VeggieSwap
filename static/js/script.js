// Code goes here

PersonModel = function () {
    var self = this;
    this.FirstName = ko.observable();
    this.LastName = ko.observable();
}

PersonViewModel = function () {
    var model = new PersonModel();

    function loadModel(data) {
        model.FirstName(data.FirstName);
        model.LastName(data.LastName);
    }

    return {
        Model: model,
        LoadModel: loadModel
    };
}

var viewModel = new PersonViewModel();
ko.applyBindings(viewModel.Model);

showEditModal = function () {
    // Need to replace with data from database
    var data = {
        FirstName: 'John',
        LastName: 'Smith'
    };

    viewModel.LoadModel(data);

    $('#modalHeader').html('Edit Person');
    $('#modalForm').modal('toggle');

    $('#SaveButton').off('click').on('click', editItem);
};

showCreateModal = function () {
    var data = {
        FirstName: '',
        LastName: ''
    };

    viewModel.LoadModel(data);

    $('#modalHeader').html('Add Person');
    $('#modalForm').modal('toggle');

    $('#SaveButton').off('click').on('click', createItem);
}

function createItem() {
    toastr.success(viewModel.Model.FirstName() + ' Created!');
}

function editItem() {
    // logic for updating an existing item
    toastr.success(viewModel.Model.FirstName() + ' Updated!');
}
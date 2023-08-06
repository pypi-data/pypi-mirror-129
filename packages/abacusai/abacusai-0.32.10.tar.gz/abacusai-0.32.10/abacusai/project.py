from .return_class import AbstractApiClass


class Project(AbstractApiClass):
    """
        A project is a container which holds datasets, models and deployments
    """

    def __init__(self, client, projectId=None, name=None, useCase=None, createdAt=None, featureGroupsEnabled=None):
        super().__init__(client, projectId)
        self.project_id = projectId
        self.name = name
        self.use_case = useCase
        self.created_at = createdAt
        self.feature_groups_enabled = featureGroupsEnabled

    def __repr__(self):
        return f"Project(project_id={repr(self.project_id)},\n  name={repr(self.name)},\n  use_case={repr(self.use_case)},\n  created_at={repr(self.created_at)},\n  feature_groups_enabled={repr(self.feature_groups_enabled)})"

    def to_dict(self):
        return {'project_id': self.project_id, 'name': self.name, 'use_case': self.use_case, 'created_at': self.created_at, 'feature_groups_enabled': self.feature_groups_enabled}

    def refresh(self):
        self.__dict__.update(self.describe().__dict__)
        return self

    def describe(self):
        return self.client.describe_project(self.project_id)

    def list_datasets(self):
        return self.client.list_project_datasets(self.project_id)

    def get_schema(self, dataset_id):
        return self.client.get_schema(self.project_id, dataset_id)

    def rename(self, name):
        return self.client.rename_project(self.project_id, name)

    def delete(self):
        return self.client.delete_project(self.project_id)

    def set_feature_mapping(self, feature_group_id, feature_name, feature_mapping, nested_column_name=None):
        return self.client.set_feature_mapping(self.project_id, feature_group_id, feature_name, feature_mapping, nested_column_name)

    def validate(self):
        return self.client.validate_project(self.project_id)

    def set_column_data_type(self, dataset_id, column, data_type):
        return self.client.set_column_data_type(self.project_id, dataset_id, column, data_type)

    def set_column_mapping(self, dataset_id, column, column_mapping):
        return self.client.set_column_mapping(self.project_id, dataset_id, column, column_mapping)

    def remove_column_mapping(self, dataset_id, column):
        return self.client.remove_column_mapping(self.project_id, dataset_id, column)

    def list_feature_groups(self, filter_project_feature_group_type=None):
        return self.client.list_project_feature_groups(self.project_id, filter_project_feature_group_type)

    def get_training_config_options(self):
        return self.client.get_training_config_options(self.project_id)

    def train_model(self, name=None, training_config={}, refresh_schedule=None):
        return self.client.train_model(self.project_id, name, training_config, refresh_schedule)

    def create_model_from_python(self, function_source_code, train_function_name, predict_function_name, training_input_tables=[], name=None):
        return self.client.create_model_from_python(self.project_id, function_source_code, train_function_name, predict_function_name, training_input_tables, name)

    def list_models(self):
        return self.client.list_models(self.project_id)

    def create_deployment_token(self):
        return self.client.create_deployment_token(self.project_id)

    def list_deployments(self):
        return self.client.list_deployments(self.project_id)

    def list_deployment_tokens(self):
        return self.client.list_deployment_tokens(self.project_id)

    def list_refresh_policies(self, dataset_ids=[], model_ids=[], deployment_ids=[], batch_prediction_ids=[]):
        return self.client.list_refresh_policies(self.project_id, dataset_ids, model_ids, deployment_ids, batch_prediction_ids)

    def list_batch_predictions(self):
        return self.client.list_batch_predictions(self.project_id)

    def attach_dataset(self, dataset_id, project_dataset_type):
        return self.client.attach_dataset_to_project(dataset_id, self.project_id, project_dataset_type)

    def remove_dataset(self, dataset_id):
        return self.client.remove_dataset_from_project(dataset_id, self.project_id)

    def create_model_from_functions(self, train_function: callable, predict_function: callable, training_input_tables: list = None):
        return self.client.create_model_from_functions(self.project_id, train_function, predict_function, training_input_tables)

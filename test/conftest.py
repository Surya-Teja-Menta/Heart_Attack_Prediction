import yaml,os,pytest,json
import prediction_service
@pytest.fixture

def config(config_path='params.yaml'):
    with open(config_path) as file:
        config=yaml.load(file)
    return config



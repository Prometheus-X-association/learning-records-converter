import json
from os import listdir, path

import pytest
from fastapi.testclient import TestClient
from utils.utils_text import random_case_in_string

from app.api.endpoints import app
from app.api.schemas import TransformInputTraceRequestModel, TransformInputTraceResponseModel
from app.xapi_converter.transformer.mapping_input import get_config_model_from_yaml_file

base_path_file = "tests/data/"
input_json_path_file = path.join(base_path_file, "input_data")
basic_mapping_config_path_file = path.join(
    base_path_file, "mapping_output_data_basic/mapping_config_example.yml"
)
basic_output_json_path_file = path.join(base_path_file, "mapping_output_data_basic/output_data")

list_input_json = listdir(input_json_path_file)
mapping_model = get_config_model_from_yaml_file(basic_mapping_config_path_file)
input_format = "fake_scorm"
output_format = "fake_xapi"
test_client = TestClient(app)


############### Test /convert endpoint - SUCCESS ###############
@pytest.mark.parametrize(
    "input_format, output_format, input_json, output_json",
    [
        (
            random_case_in_string(input_format),
            random_case_in_string(output_format),
            path.join(input_json_path_file, filename),
            path.join(basic_output_json_path_file, filename),
        )
        for filename in list_input_json
    ],
)
def test_mapping(input_format, output_format, input_json, output_json):
    # Get data
    input_trace = json.load(open(input_json))
    output_trace = json.load(open(output_json))
    payload = json.loads(
        TransformInputTraceRequestModel(
            input_format=input_format, output_format=output_format, input_trace=input_trace
        ).model_dump_json()
    )

    # Classic behavior
    response = test_client.post("/convert", json=payload)
    print(response.text)
    assert response.status_code == 200
    assert TransformInputTraceResponseModel(**response.json()).output_trace == output_trace

    # No input_format passed
    payload.pop("input_format")
    response = test_client.post("/convert", json=payload)
    assert response.status_code == 200
    assert TransformInputTraceResponseModel(**response.json()).output_trace == output_trace


############### Test /convert endpoint - FAILURE ###############
@pytest.mark.parametrize(
    "input_format, output_format, input_trace, exception_class",
    [
        ("fake_xapi", "fake_xapi", {}, Exception),
        ("fake_xapi", "fake_scorm", {}, Exception),
        ("fake_xapiii", "fake_xapi", {}, Exception),
        ("fake_xapi", "fake_xapiii", {}, Exception),
        (None, "fake_scorm", {}, Exception),
        (None, None, {}, Exception),
        ("fake_xapi", None, {}, Exception),
        ("fake_scorm", "fake_xapi", {"no_key": 10}, Exception),
        (1, "fake_xapi", {}, Exception),
        ("fake_xapi", [], {}, Exception),
    ],
)
def test_mapping_failure(input_format, output_format, input_trace, exception_class):
    with pytest.raises(exception_class) as e_info:
        payload = json.loads(
            TransformInputTraceRequestModel(
                input_format=input_format, output_format=output_format, input_trace=input_trace
            ).model_dump_json()
        )
        response = test_client.post("/convert", json=payload)
        if response.status_code >= 400:
            raise ValueError(response.text)

import json
import pathlib
from os import path

import pytest
from fastapi.testclient import TestClient

from app.api.endpoints import app
from app.api.schemas import ValidateInputTraceRequestModel, ValidateInputTraceResponseModel

base_path_file = "tests/data/"
input_json_path_file = path.join(base_path_file, "mock_format")
mock_format_folder = pathlib.Path(input_json_path_file)

list_tuple_args = []

for each_folder in mock_format_folder.iterdir():
    list_input_json = list(each_folder.iterdir())
    list_tuple_args.extend([(each_folder.name, input_json) for input_json in list_input_json])

test_client = TestClient(app)


############### Test /validate endpoint - SUCCESS ###############
@pytest.mark.parametrize("input_format, input_json", list_tuple_args)
def test_validation(input_format, input_json):
    # Get data
    input_trace = json.load(open(input_json))
    payload = json.loads(
        ValidateInputTraceRequestModel(
            input_format=input_format, input_trace=input_trace
        ).model_dump_json()
    )
    print("FILE:", input_json)

    # Classic behavior
    response = test_client.post("/validate", json=payload)
    assert response.status_code == 200
    assert ValidateInputTraceResponseModel(**response.json()).input_format.value == input_format

    # No input_format passed
    payload.pop("input_format")
    response = test_client.post("/validate", json=payload)
    assert response.status_code == 200
    assert ValidateInputTraceResponseModel(**response.json()).input_format.value == input_format


############### Test /validate endpoint - FAILURE ###############
@pytest.mark.parametrize(
    "input_format, input_trace, exception_class",
    [
        ("fake_xapi", {}, Exception),
        ("fake_xapiii", "tests/data/mock_format/imscaliper1_2/annotation_event.json", Exception),
        ("imscaliper1_1", "tests/data/mock_format/imscaliper1_2/annotation_event.json", Exception),
        ("fake_xapi", None, Exception),
        ("fake_xapi", 1, Exception),
        ("fake_xapi", "trace json string", Exception),
        ({}, None, Exception),
        (1, 1, Exception),
        ([], "trace json string", Exception),
        (None, {"a": "b"}, Exception),
        (None, 1, Exception),
        (None, "trace json string", Exception),
    ],
)
def test_validation_failure(input_format, input_trace: dict | str, exception_class):
    with pytest.raises(exception_class) as e_info:
        payload = json.loads(
            ValidateInputTraceRequestModel(
                input_format=input_format,
                input_trace=(
                    input_trace if isinstance(input_trace, dict) else json.load(open(input_trace))
                ),
            ).model_dump_json()
        )
        response = test_client.post("/validate", json=payload)
        if response.status_code >= 400:
            raise ValueError(response.text)

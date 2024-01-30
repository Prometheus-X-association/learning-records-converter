import json
from os import listdir, path

import pytest

from app.xapi_converter.transformer.mapping_input import (
    MappingInput,
    get_config_model_from_yaml_file,
)

base_path_file = "tests/tests_xapi_converter/tests_transformer/data/"
input_json_path_file = path.join(base_path_file, "input_data")
basic_mapping_config_path_file = path.join(
    base_path_file, "mapping_output_data_basic/mapping_config_example.yml"
)
basic_output_json_path_file = path.join(base_path_file, "mapping_output_data_basic/output_data")


############### Test mapping config file ###############

list_input_json = listdir(input_json_path_file)
mapping_model = get_config_model_from_yaml_file(basic_mapping_config_path_file)


@pytest.mark.parametrize(
    "input_json, mapping_config, output_json",
    [
        (
            path.join(input_json_path_file, filename),
            mapping_model,
            path.join(basic_output_json_path_file, filename),
        )
        for filename in list_input_json
    ],
)
def test_mapping(input_json, mapping_config, output_json):
    mapping_input = MappingInput(None, mapping_config, None)  # type: ignore
    input_trace = json.load(open(input_json))
    result_trace = mapping_input.mapping(input_trace=input_trace)
    output_trace = json.load(open(output_json))
    assert output_trace == result_trace

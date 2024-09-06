import json
from os import listdir, path

import pytest
from enums import CustomTraceFormatModelEnum
from trace_formats.enums import TraceFormatEnum
from trace_formats.models.mapping_config import CompleteConfigModel

from app.xapi_converter.transformer.mapping_input import (
    MappingInput,
    get_config_model_from_yaml_file,
    get_mapping_by_input_and_output_format,
)

############### Test mapping config file ###############
base_path_file = "tests/data/"
input_json_path_file = path.join(base_path_file, "input_data")
basic_mapping_config_path_file = path.join(
    base_path_file, "mapping_output_data_basic/mapping_config_example.yml"
)
basic_output_json_path_file = path.join(base_path_file, "mapping_output_data_basic/output_data")

list_input_json = listdir(input_json_path_file)
mapping_model = get_config_model_from_yaml_file(basic_mapping_config_path_file)


############### Test Mapping class ###############
@pytest.mark.parametrize(
    "input_format, output_format, input_json, mapping_config, output_json",
    [
        (
            CustomTraceFormatModelEnum.FAKE_SCORM,
            CustomTraceFormatModelEnum.FAKE_XAPI,
            path.join(input_json_path_file, filename),
            mapping_model,
            path.join(basic_output_json_path_file, filename),
        )
        for filename in list_input_json
    ],
)
def test_mapping_class(input_format, output_format, input_json, mapping_config, output_json):
    mapping_input = MappingInput(input_format, mapping_config, output_format)  # type: ignore
    input_trace = json.load(open(input_json))
    result_trace = mapping_input.run(input_trace=input_trace)
    output_trace = json.load(open(output_json))
    assert output_trace == result_trace


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


############### Test getting mapping config file ###############
@pytest.mark.parametrize(
    "file_path",
    ["tests/data/mapping_output_data_basic/mapping_config_example.yml"],
)
def test_get_config_model_from_yaml_file(file_path: str):
    response = get_config_model_from_yaml_file(file_path=file_path)
    assert isinstance(response, CompleteConfigModel)


############### Test getting mapping config file by input and output ###############
@pytest.mark.parametrize(
    "input_format, output_format",
    [
        ("xAPI", "SCORM_1_1"),
        ("Scorm_1_1", "xAPI"),
        (CustomTraceFormatModelEnum.XAPI, CustomTraceFormatModelEnum.SCORM_1_1),  # type: ignore
    ],
)
def test_get_mapping_by_input_and_output_format(
    input_format: str | TraceFormatEnum, output_format: str | TraceFormatEnum
):
    assert isinstance(
        get_mapping_by_input_and_output_format(input_format, output_format), CompleteConfigModel
    )

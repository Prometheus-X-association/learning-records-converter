# Learning Records to xAPI

# Overview
The aim of this part is to convert a Learning Record to XAPI. In order to do this, we will set up two consecutive processes : **Input Data Validation**, and **Data Transformation**.
- **Input Data Validation** will be responsible for interpreting and validating the input data format
(supplied in JSON format),
- **Data Transformation** will be in charge of transforming input data into XAPI format, where possible.

# Table
1. [Input Data Validation](#input-data-validation)
   - [Pydantic File](#pydantic-file)
   
3. [Data Transformation](#data-transformation)
    - [YAML File](#yaml-file)
        - [Mapping](#yaml-mapping)
        - [Default](#yaml-default)
        - [Metadata](#yaml-metadata)
    - [Python mapping](#python-mapping)
    - [How to create my own YAML file?](#create-own-yaml)


# Input Data Validation <a name="input-data-validation"></a>
## Pydantic File <a name="pydantic-file"></a>
### Overview
The Validation Config is a Pydantic (.py) file used to validate the format of an input file. An example can be found here [examples/version_1.py]

WIP

# Data Transformation <a name="data-transformation"></a>
## YAML File <a name="yaml-file"></a>
### Overview
The Transformation Config is a YAML file used to define mappings and transformations from a source format (e.g., SCORM) to a target format (e.g., xAPI). An example can be found here [examples/version_1.yml]

The Transformation Config file follows a specific structure:

```yaml
version: 1.0
input_format: "SCORM"
output_format: "xAPI"
mappings:
  # ... (see mappings section)
default_values:
  # ... (see default values section)
metadata:
  # ... (see metadata section)
```
- `version`: Specifies the version of the configuration file.
- `input_format`: Indicates the input format for the mappings.
- `output_format`: Indicates the output format for the mappings.
- `mappings`: Describes the data mappings from the source to the target format.
- `default_values`: Specifies default values for certain output fields.
- `metadata`: Provides metadata information about the configuration.

### Mapping <a name="yaml-mapping"></a>
`mappings` indicates how to transform the input trace into the output format. 

```yaml
mappings:
  - description: "Type mapping" # Optional
    input_fields: ["cmi.object.type"]
    output_fields:
      # ... (see output_fields section)
```
- `description`: Optional. Specify a description for the mapping element.
- `input_fields`: A list of strings indicating the fields to use. The paths are specified using the json dotted format. an integer in the path is considered as a list index.
- `output_fields`: Action to apply for the output trace.

#### Output Fields <a name="output-field"></a>
The action can be applied for one or multiple outputs.
##### For multiple correspondance
```yaml
output_fields:
  multiple: 
    # ... (see output_fields section)
```
- `multiple`: Multiple (list) of [output field](#output-field)

##### For only a single correspondance
```yaml
output_fields:
  output_field: "actor.mbox"
  value: "default_value_here"
```
- `output_field`: Output corresponding field

#### Transformation
- `custom`: List of string representing a python lambda to execute some code by using the inputs values. Some utils exists in order to use it directly in the lambda

##### Static value
```yaml
value: "searched"
```
- `value`: Static value to map the output with. Essentially used for the default section.

##### Switch cases
```yaml
switch:
  - condition: "lambda a: is_empty(a)"
    # ... (other fields from the output_field section)
```
- `switch`: Like in some programming languages, this is a list of cases with each a condition. The first case with a correct condition wil be used for the output.
- `condition`: Python lambda with a boolean response to verify condition. There can be (only one) "default" condition where if none of the conditions before have passed, it will still apply the default one. This condition needs to be placed at the end of the list and is not mandatory.
- All the other output fields can be found [here](#output-field)

### Default <a name="yaml-default"></a>
The `default_values` section specifies default values for certain output fields. This ensures that if a field is missing in the source data, a default value is used.

```yaml
default_values:
  - description: ""
    output_field: "actor.mbox"
    value: "default_value_here"
    # ... (same as the output_field section)
```
- All the output fields can be found [here](#output-field)

### Metadata <a name="yaml-metadata"></a>
The `metadata` section provides additional information about the configuration, such as the author and publication date.

```yaml
metadata:
  author: "Your Name"
  date:
    publication: "2023-01-01"
    update: "2023-02-01"
```

## Python mapping <a name="python-mapping"></a>
The main mapping is done using the `app.xapi_converter.transformer.mapping_input.MappingInput` class. To initiate it, an input format and the corresponding mappping configuration is needed. By default, the output_format is xAPI. This class is complexe enough, it will not determine the correct mapping configuration to use depending on the input and output format, nor will it guess the input format from the input trace. However, other methods will be created to help with these problems. Once all the information are gathered, the mapping class will handle the rest.

In terms of organization in the `MappingInput` class, each YAML bloc is handled by a python function (transformation with multiple lambda function, switch cases...). This allows the code to easily understand the config file however it is written.

In addtion, a `config_runnable_function.py` file is present in the module. It utilies all methods the config file can call. Additional methods can be implemeted here.

The `run` method is called to start the transformation. It will check if the input_trace is in the correct format, apply the mapping, and check the output_trace format before returning the converted trace.
Here is a small diagram to summerise the process:

IMAGE

An endpoint exist to call this method. Its purpose is to test, validate or just try out the mapping process. Here a is diagram to explain the process

IMAGE



## How to create my own YAML file? <a name="create-own-yaml"></a>

Please refer to the [YAML File](#yaml-file) section to create your own config file. The example (in the `example` folder) can also help with understanding and creating a new YAML file. Once this file is created, here are the steps to follow:
- Save your yaml file at `app/common/mappers`
- Name it with something recognizable
- If the input format model is not yet created, please create it at `app/common/models/custom_trace_formats` in a new file and import it into the `__init__.py` file.
- In `app/common/enums/custom_trace_format.py` update :
    - CAUTION: For all Enums, all keys of a same format has to be the same everywhere (if the chossen name is `NEW_FORMAT`, it has to be like so everywhere).

    **Model**
    - `CustomTraceFormatModelEnum` - Add new trace format pydantic model (example: `NEW_FORMAT = NewFormatModel`). This Enum regroups all the trace format models.

    **Transform input traces (that are in other formats) into NewFormat**
    - There is an Enum for each possible output format (xAPI, SCORM...). If you wish to have a mapping where the new trace format is the output format, you will have to create a new Enum like so
    ```python
    class TraceFormatToNewFormatMappingEnum(TraceFormatEnum):
        SCORM_1_1 = "path/file1.yaml"
        XAPI = "path/file2.yaml"
    ```
    - For each key, give the path to locate the yaml mapping file.
        - For example, in this Enum, to transform `xAPI` to `NewFormat` we need to use `path/file2.yaml` config file.
    - Then in `CustomTraceFormatOutputMappingEnum`, associate the newly created mapping enum with the corresponding key
    ```python
    @extend_enum(TraceFormatOutputMappingEnum)
    class CustomTraceFormatOutputMappingEnum(TraceFormatEnum):
        NEW_FORMAT = TraceFormatToNewFormatMappingEnum
    ```
    - For information: By using `@extend_enum(TraceFormatOutputMappingEnum)` the other mapping enum are preserved.
    
    **Transform input trace (that are in NewFormat format) into other formats** 
    - If you wish to add a mapping for new_format into an existing output (NewFormat to xAPI for example), you have to inherit or directly modify the corresponding output mapping enum.
    Here is an example in which we add a new mapping file for NewFormat to xAPI
    ```python
    @extend_enum(TraceFormatToXapiMappingEnum)
    class CustomTraceFormatToXapiMappingEnum(TraceFormatEnum):
        NEW_FORMAT = "path/file.yaml"

    @extend_enum(TraceFormatOutputMappingEnum)
    class CustomTraceFormatOutputMappingEnum(TraceFormatEnum):
        XAPI = CustomTraceFormatToXapiMappingEnum
    ```
    - `TraceFormatToXapiMappingEnum` is the Enum that maps traces into xAPI. Since it is in not recommended to modify `TraceFormatToXapiMappingEnum` directly (because it is in `trace_formats` git submodule), we use `extend_enum` to inherit `TraceFormatToXapiMappingEnum` into `CustomTraceFormatToXapiMappingEnum`
    - The xAPI mapping Enum has also changed so we associate the correct Enum in `CustomTraceFormatOutputMappingEnum` so that we do not directly change `TraceFormatOutputMappingEnum` (because it is in `trace_formats` git submodule).

    - Once again, be careful, all the Enum keys must be the same in every Enum.
    

As reference, look at `app/common/trace_formats/enums/trace_format.py`










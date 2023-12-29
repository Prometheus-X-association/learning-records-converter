# Learning Records to xAPI

# Overview
The aim of this part is to convert a Learning Record to XAPI. In order to do this, we will set up two consecutive processes : **Input Data Validation**, and **Data Transformation**.
- **Input Data Validation** will be responsible for interpreting and validating the input data format
(supplied in JSON format),
- **Data Transformation** will be in charge of transforming input data into XAPI format, where possible.

# Table
1. [Input Data Validation](#input-data-validation)
2. [Data Transformation](#data-transformation)
    - [YAML File](#yaml-file)
        - [Mapping](#yaml-mapping)
        - [Default](#yaml-default)
        - [Metadata](#yaml-metadata)
    - [Python mapping](#python-mapping)
    - [How to create my own YAML file?](#create-own-yaml)


# Input Data Validation <a name="input-data-validation"></a>

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
- `input_fields`: A list of strings indicating the fields to use. The paths are specified usning the json dotted format. an integer in the path is considered as a list index.
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
    transformation: # Optional, see tranformation section)
      value: "default_value_here"
```
- `output_field`: Output corresponding field
- `transformation`: Transformation to apply. If not transformation is specified, a direct mapping is done.

#### Transformation
The `transformation` section defines the action to apply for the mapping concerned. Several transformations
are possible and others will be added as the projet goes.
##### Apply custom python code
```yaml
transformation: 
    custom:
      - "lambda a, b: a + b"
      - "lambda val: str(val) + '.com'"
```
- `custom`: List of string representing a python lambda to execute some code by using the inputs values. Some utils exists in order to use it directly in the lambda

##### Static value
```yaml
transformation: 
    value: "searched"
```
- `value`: Static value to map the output with. Essentially used for the default section.

##### Switch cases
```yaml
transformation: 
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
    transformation:
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
The main mapping is done using the `app.xapi_converter.mapping_input.MappingInput` class. To initiate it, an input format, output format and the corresponding mappping configuration is needed. This class is complexe enough, it will not determine he correction mapping configuration to use depending on the input and output format, not will it guess the input format format the input trace. However, other methods will be created to help with these problems. Once all the information are gathered, the mapping class will handle the rest.

In terms of organization in the `MappingInput` class, each YAML bloc is handled by a python function. This allows the code to easily understand the config file however it is written.

In addtion, a `config_runnable_function.py` file in present in the module. It utilies all methods the config file can call. Additional methods can be implemeted here.

## How to create my own YAML file? <a name="create-own-yaml"></a>













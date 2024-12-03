# Learning Records to xAPI

## Overview
The aim of this process is to convert Learning Records to xAPI format. This involves two consecutive steps: **Input Data Validation** and **Data Transformation**.
- **Input Data Validation** is responsible for interpreting and validating the input data format.
- **Data Transformation** is in charge of transforming input data into xAPI format, where possible.

## Table of Contents
1. [Input Data Validation](#input-data-validation)
   - [Pydantic File](#pydantic-file)
2. [Data Transformation](#data-transformation)
    - [YAML File](#yaml-file)
        - [Mapping](#yaml-mapping)
        - [Profiles](#yaml-profiles)
        - [Default](#yaml-default)
        - [Metadata](#yaml-metadata)
    - [Create your own YAML file](#create-own-yaml)

## Input Data Validation <a name="input-data-validation"></a>
### Pydantic File <a name="pydantic-file"></a>
### Overview
The Validation Config is a Pydantic (.py) file used to validate the format of an input file. It defines the structure and types of the input data, ensuring that the data conforms to the expected format before transformation.

## Data transformation <a name="data-transformation"></a>
### YAML file <a name="yaml-file"></a>
#### Overview
The Transformation Config is a YAML file that defines mappings and transformations from a source format (e.g., SCORM, IMS Caliper) to a target format (e.g., xAPI). 

The Transformation Config file follows this structure:

```yaml
version: 1.0
input_format: "SOURCE_FORMAT"
output_format: "TARGET_FORMAT"
mappings:
  # Mapping rules (see mappings section)
default_values:
  # Default values (see default values section)
metadata:
  # Metadata information (see metadata section)
```

- `version`: Specifies the version of the configuration file.
- `input_format`: Indicates the input format for the mappings.
- `output_format`: Indicates the output format for the mappings.
- `mappings`: Describes the data mappings from the source to the target format.
- `default_values`: Specifies default values for certain output fields.
- `metadata`: Provides metadata information about the configuration.

#### Mapping <a name="yaml-mapping"></a>
The `mappings` section defines how to transform the input trace into the output format. Each mapping rule has this structure:

```yaml
- description: "Optional description"
  input_fields: ["field.path", "otherfield.path.subpath"]
  output_fields:
    # Output field definition
```

- `description`: Optional. Describes the mapping rule.
- `input_fields`: A list of input fields to use. Paths use dot notation; integers in the path are treated as list indices.
- `output_fields`: Defines the action to apply for the output trace.

##### Output fields <a name="output-field"></a>
Output fields can be defined in several ways:

1. **Static value**:
   ```yaml
   output_field: "target.field"
   value: "static_value"
   ```
- `value`: Static value to map the output with. Essentially used for the default section.

2. **Custom transformation**:
   ```yaml
   output_field: "target.field"
   custom:
     - "lambda x: some_function(x)"
   ```
- `custom`: Defines a python lambda to execute some code by using the inputs values. Some functions exists in order to use it directly in the lambda

3. **Switch cases**:
   ```yaml
   switch:
     - condition: "lambda a: some_condition(a)"
       output_field: "target.field"
       value: "value_if_true"
   ```
- `switch`: Like in some programming languages, this is a list of cases with each a condition. The first case with a correct condition wil be used for the output.
- `condition`: Python lambda with a boolean response to verify condition. There can be a "default" condition where if none of the conditions before have passed, it will still apply the default one. This condition needs to be placed at the end of the list and is not mandatory.
- All the other output fields can be found [here](#output-field)

4. **Multiple outputs**:
   ```yaml
   multiple:
     - output_field: "target.field1"
       value: "value1"
     - output_field: "target.field2"
       custom:
         - "lambda x: some_function(x)"
   ```
- `multiple`: Multiple (list) of [output field](#output-field)

5. **Profile association**:
   ```yaml
   profile: "profile.name"
   ```
Profiles are used to enrich and validate the trace.
The LRC supports multiple profiles, including LMS, Forum, and Assessment profiles.

#### Profiles <a name="yaml-profiles"></a>

In the LRC, profiles and their templates are referenced using the format `profile_name.template_name`. This convention is crucial for correctly applying profile-specific rules to xAPI statements.

##### Structure
- `profile_name`: The name of the profile (e.g., "lms", "forum", "assessment")
- `template_name`: The specific template within that profile (e.g., "accessed-page", "posted-reply", "completed-quiz")

Example: `lms.accessed-page`

##### Implications

1. **Profile Selection**: 
   - The `profile_name` determines which JSON-LD profile file is used for enrichment and validation.
   - It corresponds to one of the profiles defined in the `PROFILES_NAMES` environment variable.

2. **Template Application**:
   - The `template_name` identifies a specific StatementTemplate within the chosen profile.
   - This template contains rules for structuring and validating the xAPI statement.

3. **Enrichment Process**:
   - When a `profile_name.template_name` is specified in the YAML configuration, the LRC will:
     a. Load the corresponding profile JSON-LD file.
     b. Find the specified template within that profile.
     c. Apply the template's rules to enrich the xAPI statement.

4. **Validation**:
   - The specified template's rules are used to validate the xAPI statement.
   - This includes checking for required fields, correct verb usage, and proper activity types.

5. **Recommendations**:
   - Recommendations for improving the xAPI statement are based on the specified template's rules.


#### Default <a name="yaml-default"></a>
The `default_values` section specifies default values for certain output fields:

```yaml
default_values:
  - output_field: "default.field"
    value: "default_value"
```

#### Metadata <a name="yaml-metadata"></a>
The `metadata` section provides information about the configuration:

```yaml
metadata:
  author: "Author Name"
  date:
    publication: "2023-01-01"
    update: "2023-02-01"
```

### Available Functions in Lambdas
When writing custom transformations in your mapping files, several utility functions are available for use in your lambda expressions:

**Date and Time Functions**

```python
parse_date(date: str | int, date_format: str | None = None, user_locale: str | None = None) -> str | None
```
- Converts various date formats to ISO 8601 format
- Supports custom date formats and locales
- Handles timestamps, string dates, and common formats

**URL and Path Functions**

```python
urlparse(url: str) -> ParseResult
```
- Parses URLs into components
- Access scheme, netloc, path, params, query, and fragment
 
```python
path_join(*paths: str) -> str
```
- Joins URL or file system paths
- Handles leading/trailing slashes correctly

**String Functions**
```python
search(pattern, string)
```
Search for pattern in string

```python
match(pattern, string)
```
Match pattern at start of string

**Data Validation**

```python
is_empty(x: Any) -> bool
```
Checks if a value is empty (None, empty string, empty list/dict, etc.).


## How to create my own YAML file? <a name="create-own-yaml"></a>

Please refer to the [YAML File](#yaml-file) section to create your own config file. The example (in the `example` folder) can also help with understanding and creating a new YAML file. Once this file is created, here are the steps to follow:
- Save your yaml file at `data/mappers`
- Name it with something recognizable
- If the input format model is not yet created, please create it at `app/common/models/custom_trace_formats` in a new file and import it into the `__init__.py` file.
- In `app/common/extensions/enums/custom_trace_formats.py` update :
    - CAUTION: For all Enums, all keys of a same format has to be the same everywhere (if the choosen name is `NEW_FORMAT`, it has to be like so everywhere).

    **Model**
    - `CustomTraceFormatModelEnum` - Add new trace format pydantic model (example: `NEW_FORMAT = NewFormatModel`). This Enum regroups all the trace format models.

    **Transform input traces (that are in other formats) into NewFormat**
    - There is an Enum for each possible output format (xAPI, SCORM...). If you wish to have a mapping where the new trace format is the output format, you will have to create a new Enum like so
    ```python
    class TraceFormatToNewFormatMappingEnum(TraceFormatEnum):
        SCORM_1_1 = "data/mappers/mapping_scorm_to_newformat.yaml"
        XAPI = "data/mappers/mapping_xapi_to_newformat.yaml"
    ```
    - For each key, give the path to locate the yaml mapping file.
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
        NEW_FORMAT = "data/mappers/mapping_newformat_to_xapi.yaml"

    @extend_enum(TraceFormatOutputMappingEnum)
    class CustomTraceFormatOutputMappingEnum(TraceFormatEnum):
        XAPI = CustomTraceFormatToXapiMappingEnum
    ```
    - `TraceFormatToXapiMappingEnum` is the Enum that maps traces into xAPI. Since it is in not recommended to modify `TraceFormatToXapiMappingEnum` directly (because it is in `trace_formats` git submodule), we use `extend_enum` to inherit `TraceFormatToXapiMappingEnum` into `CustomTraceFormatToXapiMappingEnum`
    - The xAPI mapping Enum has also changed so we associate the correct Enum in `CustomTraceFormatOutputMappingEnum` so that we do not directly change `TraceFormatOutputMappingEnum` (because it is in `trace_formats` git submodule).

    - Once again, be careful, all the Enum keys must be the same in every Enum.
    

As reference, look at `app/common/enums/trace_formats.py`

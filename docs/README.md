# Learning Records Converter (LRC)

# Overview
Learning Records are available in many formats, either standardized (xAPI, SCORM, IMS Caliper, cmi5) or proprietary (Google Classroom, MS Teams, csv, etc). This wide vairety of format is a barrier to many use cases of learning records as this prevent the easy combination and sharing of learning records datasets from multiple sources or organizations.

The Learning Records Converter is a parser translating datasets of learning traces according to a common xAPI profile.

This documentation explains the general operation of the LRC. 

IMAGE

The project is seperated into different modules, each having its own objectives:
- `api`: LRC's API used to convert different Learning Records
- `common`: A set of code that are used in several places in the project (models, utils, enumerates...)
- `dases_enricher`: Transform a basic xAPI trace into a DASES profile trace.
- `xapi_converter`: Convert any Learning Trace (in any format) into a xAPI format.

# Table
1. Learning Records to xAPI
2. xAPI to DASES
3. Endpoints

# Authors

# Other sources
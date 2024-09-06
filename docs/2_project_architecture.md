# LRC project architecture
Explanation of the project architecture
The `mapper` is responsible for converting the traces.
The `profile_enricher` is responsible for enriching and validating DASES profiles.
The `architecture` folder contains the additional building blocks that are useful for the project (logging, configuration, etc.).


```
.
├── .env                    # Environment variables for the project
├── .env.default            # Default environment variables (template for .env)
├── Pipfile                 # Pipenv file for managing project dependencies
├── app/
│   ├── api/
│   │   ├── endpoints.py    # FastAPI router and endpoint definitions
│   │   ├── exceptions.py   # Custom exception classes for the API
│   │   └── schemas.py      # Pydantic models for request/response schemas
│   ├── common/
│   │   ├── enums/
│   │   │   └── trace_formats.py # Base trace formats definitions
│   │   ├── extensions/
│   │   │   ├── enums.py         # Custom trace formats definitions
│   │   │   ├── mappers          # Custom mappings
│   │   │   └── models           # Custom traces Pydantic models 
│   │   ├── models/
│   │   │   ├── trace.py         # Trace model definition
│   │   │   └── trace_formats    # Pydantic models for base trace formats
│   │   ├── type/
│   │   │   └── types.py         # Custom type definitions
│   │   └── utils/               # Utility functions
│   ├── infrastructure/
│   │   ├── config/
│   │   │   ├── contract.py    # Abstract base class for configuration
│   │   │   └── envconfig.py   # Environment configuration implementation
│   │   └── logging/
│   │       ├── contract.py    # Abstract base class for logging
│   │       └── jsonlogger.py  # JSON logger implementation
│   ├── mapper/
│   │   ├── mapper.py          # Main mapper class for trace conversion
│   │   ├── mapping_engine.py  # Engine for applying mapping rules
│   │   ├── exceptions.py      # Mapper-specific exceptions
│   │   ├── models/
│   │   │   ├── mapping_models.py  # Models for mapping operations
│   │   │   └── mapping_schema.py  # Schema for mapping configurations
│   │   └── repositories/
│   │       ├── contracts/
│   │       │   └── repository.py  # Abstract base class for mapping repositories
│   │       └── yaml/
│   │           └── yaml_repository.py  # YAML-based mapping repository
│   └── profile_enricher/
│       ├── profiler.py        # Main profiler class for trace enrichment
│       ├── exceptions.py      # Profiler-specific exceptions
│       ├── types.py           # Type definitions for profiler
│       ├── utils/
│       │   └── jsonpath.py    # JSONPath utility functions
│       ├── profiles/
│       │   └── jsonld.py      # JSON-LD profile models and utilities
│       ├── repositories/
│       │   ├── contracts/
│       │   │   └── repository.py  # Abstract base class for profile repositories
│       │   └── jsonld/
│       │       ├── jsonld_repository.py  # JSON-LD profile repository
│       │       ├── profile_loader.py     # Profile loading utilities
│       │       ├── trace_enricher.py     # Trace enrichment implementation
│       │       └── trace_validator.py    # Trace validation against profiles
│       └── scripts/
│           └── jsonld_profiles_updater.py  # Script for updating JSON-LD profiles
└── data/
    ├── dases_profiles/        # Directory for storing DASES profiles
    └── mappers/               # Directory for mapping configuration files
```

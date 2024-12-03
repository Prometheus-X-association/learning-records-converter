# LRC project architecture
Explanation of the project architecture
The `mapper` is responsible for converting the traces.
The `profile_enricher` is responsible for enriching and validating DASES profiles.
The `parser` is responsible for parsing custom files (CSV) into JSON.
The `architecture` folder contains the additional building blocks that are useful for the project (logging, configuration, etc.).


```
.
├── .env                            # Environment variables for the project
├── .env.default                    # Default environment variables (template for .env)
├── Pipfile                         # Pipenv file for managing project dependencies
├── pyproject.toml                  # Project configuration and tool settings
├── app/
│   ├── api/                        # API module - FastAPI implementation
│   │   ├── dependencies.py         # FastAPI dependency injection configurations
│   │   ├── exception_handlers.py   # Exception handlers configuration
│   │   ├── main.py                # FastAPI application initialization and configuration
│   │   ├── routers/               # API routes organization
│   │   │   └── traces.py          # Trace-related endpoints (convert, validate, etc.)
│   │   └── schemas.py             # Pydantic models for request/response schemas
│   │
│   ├── common/                     # Common module - Shared resources
│   │   ├── enums/
│   │   │   └── trace_formats.py    # Base trace formats definitions
│   │   ├── extensions/
│   │   │   ├── enums.py           # Custom trace formats definitions
│   │   │   ├── mappers/           # Custom mappings directory
│   │   │   └── models/            # Custom traces Pydantic models 
│   │   ├── models/
│   │   │   ├── trace.py           # Trace model definition
│   │   │   └── trace_formats/     # Pydantic models for base trace formats
│   │   ├── common_types.py        # Custom type definitions
│   │   ├── exceptions.py          # Base application exceptions
│   │   └── utils/                 # Utility functions
│   │
│   ├── infrastructure/            # Infrastructure module - Foundation services
│   │   ├── config/
│   │   │   ├── contract.py        # Abstract base class for configuration
│   │   │   └── envconfig.py       # Environment configuration implementation
│   │   └── logging/
│   │       ├── contract.py        # Abstract base class for logging
│   │       └── jsonlogger.py      # JSON logger implementation
│   │
│   ├── mapper/                    # Mapper module - Format conversion
│   │   ├── available_functions/
│   │   │   └── mapping_runnable_functions.py  # Functions available in mappings
│   │   ├── exceptions.py          # Mapper-specific exceptions
│   │   ├── mapper.py              # Main mapper class for trace conversion
│   │   ├── mapping_engine.py      # Engine for applying mapping rules
│   │   ├── models/
│   │   │   ├── mapping_models.py  # Models for mapping operations
│   │   │   └── mapping_schema.py  # Schema for mapping configurations
│   │   └── repositories/
│   │       ├── contracts/
│   │       │   └── repository.py  # Abstract base class for mapping repositories
│   │       └── yaml/
│   │           └── yaml_repository.py  # YAML-based mapping repository
│   │
│   ├── parsers/                   # Parsers module - Input parsing
│   │   ├── contracts/
│   │   │   └── parser.py          # Abstract base class for parsers
│   │   ├── csv/
│   │   │   └── parser.py          # CSV parser implementation
│   │   ├── exceptions.py          # Parser-specific exceptions
│   │   ├── factory.py             # Parser factory class
│   │   ├── jsonencoder.py         # JSON encoding utilities
│   │   └── types.py               # Parser-specific types
│   │
│   └── profile_enricher/          # Profile Enricher module - xAPI profiles
│       ├── exceptions.py          # Profiler-specific exceptions
│       ├── profiler.py            # Main profiler class
│       ├── profiler_types.py      # Type definitions for profiler
│       ├── profiles/
│       │   └── jsonld.py          # JSON-LD profile models and utilities
│       ├── repositories/
│       │   ├── contracts/
│       │   │   └── repository.py  # Abstract base class for profile repositories
│       │   └── jsonld/
│       │       ├── jsonld_repository.py  # JSON-LD profile repository
│       │       ├── profile_loader.py     # Profile loading utilities
│       │       ├── trace_enricher.py     # Trace enrichment implementation
│       │       └── trace_validator.py    # Trace validation against profiles
│       ├── scripts/
│       │   └── jsonld_profiles_updater.py  # Profile update automation
│       └── utils/
│           └── jsonpath.py         # JSONPath utility functions
│
├── data/                          # Data storage
│   ├── dases_profiles/            # Directory for storing DASES profiles
│   └── mappers/                   # Directory for mapping configuration files
│
└── docs/                          # Documentation
```

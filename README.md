# Ariane LRC service
Explanation of the project architecture

```
LRC/
│
├── app/                                    # Application code
│   ├── __init__.py                         # Makes app a Python package
│   ├── main.py                             # FastAPI app instance and routes
│   ├── dependencies.py                     # Dependency management for FastAPI
│   ├── api/                                # API route handlers
│   │   ├── __init__.py
│   │   ├── endpoints.py                    # Endpoints for the LRC API
│   │   └── schemas.py                      # Pydantic models for request and response data
│   │
│   ├── xapi_converter/                     # Bloc for converting to xAPI format
│   │   ├── __init__.py
│   │   ├── validator/                      # Input data validation for xAPI conversion
│   │   │   └── __init__.py
│   │   └── transformer/                    # Data transformation to xAPI format
│   │       └── __init__.py
│   │
│   ├── dases_enricher/                     # Bloc for converting to DASES profiles
│   │   ├── __init__.py
│   │   ├── actor_identity/                 # Actor identity bloc
│   │   │   ├── __init__.py
│   │   │   ├── components/                 # Components used for bloc
│   │   │   │   └── __init__.py
│   │   │   ├── policies/                   # Action for specific policy
│   │   │   │   └── __init__.py
│   │   │   └── actor_processor.py
│   │   │
│   │   ├── action_verb/                    # Action verb bloc
│   │   │   ├── __init__.py
│   │   │   ├── components/                 # Components used for bloc
│   │   │   │   └── __init__.py
│   │   │   ├── policies/                   # Action for specific policy
│   │   │   │   └── __init__.py
│   │   │   └── verb_processor.py
│   │   │
│   │   ├── learning_object/                # Learning object bloc
│   │   │   ├── __init__.py
│   │   │   ├── components/                 # Components used for bloc
│   │   │   │   └── __init__.py
│   │   │   ├── policies/                   # Action for specific policy
│   │   │   │   └── __init__.py
│   │   │   └── object_processor.py
│   │   │
│   │   ├── context/                        # Context bloc
│   │   │   ├── __init__.py
│   │   │   ├── components/                 # Components used for bloc
│   │   │   │   └── __init__.py
│   │   │   ├── policies/                   # Action for specific policy
│   │   │   │   └── __init__.py
│   │   │   └── context_processor.py
│   │   │
│   │   ├── datetime/                       # Datetime bloc
│   │   │   ├── __init__.py
│   │   │   ├── components/                 # Components used for bloc
│   │   │   │   └── __init__.py
│   │   │   ├── policies/                   # Action for specific policy
│   │   │   │   └── __init__.py
│   │   │   └── datetime_processor.py
│   │   │
│   │   └── result/                         # (Optional) Result bloc
│   │       ├── __init__.py
│   │       ├── components/                 # Components used for bloc
│   │       │   └── __init__.py
│   │       ├── policies/                   # Action for specific policy
│   │       │   └── __init__.py
│   │       └── result_processor.py
│   │
│   └── common/                             # Common utilities and shared resources
│       ├── __init__.py
│       └── utils/                          # Common utilities
│           ├── __init__.py
│           └── utils_dict.py               # Common utility functions seperated by types/categories
│
├── tests/                                  # Automated tests
│   ├── __init__.py
│   ├── test_xapi_converter.py              # Tests for xapi_converter bloc
│   └── test_dases_enricher.py              # Tests for dases_enricher bloc
│
├── deployment/                             # Deployment configurations
│   ├── Docker/                             # Dockerfiles and related configurations
│   │   └── Dockerfile
│   └── Kubernetes/                         # Kubernetes deployment manifests
│       ├── deployment.yaml
│       └── service.yaml
│
├── docs/                                   # Documentation files
│   ├── LRC_Global.png                      # Architecture overview diagram
│   ├── LRC_Phase1.png                      # Detailed phase 1 architecture diagram
│   ├── LRC_Phase1_FlowChart.png            # Phase 1 flowchart
│   └── LRC_Phase2.png                      # Detailed phase 2 architecture diagram
│
├── .env                                    # Environment variables
├── Pipfile                                 # Pipenv file for dependency management
├── README.md                               # Project README
└── setup.py                                # Setup script for the package
```

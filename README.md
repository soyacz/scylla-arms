# scylla-arms
Pipelines and tasks management for ScyllaDB team

Based on `invoke` project: https://docs.pyinvoke.org/en/stable/index.html
# installation
clone repository
```poetry install```

# Usage
`arms --help`

# Differences between invoke and arms:
1. `arms` provides persistent storage for dictionaries -
to enable passing params from one task to another when tasks are executed separately
2. `arms` provides `Settings` class (based on `pydantic` `BaseSettings` class) - 
which can use parameters from Jenkins params (when `JENKINS_PARAMS` env variable is present)

# Examples
See `tasks` directory for examples how can be used.
See also jenkinsfiles for sample jenkins pipelines and how it can be used there.

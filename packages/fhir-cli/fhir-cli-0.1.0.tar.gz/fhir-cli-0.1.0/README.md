# DBTonFHIR

## Description

<!-- Describe the feature and how it solves the problem. -->

The goal is to be able to map from a given source to a FHIR server without the help of a gui leveraging existing tools
such as git and DBT.

## Setup and installation

### Prerequisites
- Python 3.9+

### Base setup
- Create an `.env` file and specify your own configuration (see `.env.template`)

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/base.txt
pre-commit install 
```

### Tests setup

```shell
pip install -r requirements/tests.txt
```

## Fhir Cli

### Install

```shell
make install 
```

### Usage

```shell
fhir --help
```

### Build package

```shell
make build
```

## Datawarehouse

### Administration

#### Create a new project database

```shell
fhir admin init --database=<target_db>
```

#### Create a new project connector

```shell
fhir admin conect --database=<target_db>
```

#### Create a new project user

```shell
fhir admin createuser --database=<target_db> --user=<username>
```

### Postgresql foreign data wrapper

A foreign data wrapper allows to add foreign tables from a distant database into a local schema

```postgresql
CREATE SERVER server_name
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'host', port 'port', dbname 'dbname');

CREATE USER MAPPING FOR local_user
    SERVER server_name
    OPTIONS (user 'username', password 'password');

CREATE SCHEMA local_schema;

IMPORT FOREIGN SCHEMA foreign_schema
FROM SERVER server_name INTO local_schema;

SET search_path TO local_schema;

-- show foreign tables
\detr
```

## DBT

### Usage

#### Run DBT

To run your models

```shell
fhir dbt run
```

#### References

To indicate that a FROM clause references a DBT models, use the `dbt-ref` keywork in a comment on the same line.

```postgresql
FROM patient -- dbt-ref
```

After the run, this line will be compiled into

```postgresql
FROM {{ref('patient')}}
```

#### Lint your sql files

```shell
sqlfluff lint schemas
```

or

```shell
make lint
```

#### Validate a fhir model

```shell
fhir validate <fhir_model>
```

#### Run DBT tests
```shell
fhir dbt test
```

## Conventions and good practices

- A mapping model should follow this naming format in snake case `{resource_type}_{profile_name}.sql` and be in its `fhir`
  folder
- In the `models` folder, your sql files should be in their correct directory according to the FROM clause 
  (eg. if the sql statement queries FROM `mimiciii.patients`, the sql file should be in `models/mimiciii/patients`)
- A fhir model musts have exactly two columns: an unique column `id` and the fhir object column `fhir`
- The `id` column should be ddeclared in the base models as a primary key
- A fhir model musts not contain any clause except the FROM clause
- The sql code musts be in full english (thus including aliases)
- The comments should be in english but an exception can be made when some concepts are hard to translate (eg. a pathology)
- The function `fhir_id` musts be used for `id` fields
- The function `fhir_ref` musts be used for `reference` fields
- Use `json_build_object`, `json_build_array` and `json_agg` to build your fhir object
- Add generic DBT tests to your Fhir models (eg. enforce unique and non null constraints on the `id` column)

## IntelliJ/Pycharm setup

### Configure data source

<img width="1135" alt="Screenshot 2021-11-09 at 15 39 06" src="https://user-images.githubusercontent.com/34629112/140945483-34ccd72e-da4d-498a-bf7b-b8ae774d325c.png">

### Highlight DBT references

<img width="921" alt="Screenshot 2021-11-09 at 16 57 16" src="https://user-images.githubusercontent.com/34629112/140958860-bd06a205-4426-4353-8a0d-8c0ee687e1bd.png">

## OMOP

### Vocabulary

- Download vocabularies at https://athena.ohdsi.org/
- Create a `vocabulary` folder and extract the files there

### CDM 5.4

To build the OMOP CDM 5.4 schema in your target database, execute the following files in this order:

1. `OMOPCDM_postgresql_5.4_ddl.sql`
2. `OMOPCDM_postgresql_5.4_primary_keys.sql`
3. `vocabulary.sql`
4. `OMOPCDM_postgresql_5.4_constraints.sql`
5. `OMOPCDM_postgresql_5.4_indices.sql`

## Tests

### Unit tests
```shell
make unit-tests
```
### End to end tests
```shell
make e2e-tests
```

## Implementation

![arkhn](https://user-images.githubusercontent.com/34629112/143152402-6b2522b2-7cd3-4fc5-8843-381a723ea3d8.jpg)

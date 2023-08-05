# pytest db plugin
uploading test stdout & stderr to a DB for easy debugging and comparison

### Installtion
- for es db client: `pip install pytest-db[es]`
- for only default (local files) db client: `pip install pytest-db`

### Flow
1. pytest test ends
2. pytest test teardown starts
3. plugin starts
4. plugin connects to DB
5. plugin collects all sources
6. plugin uploads all sources
7. plugin ends DB connection
8. plugin ends

### Invocation
- `pytest ...`
    - as long as the plugin is installed, and the url is provided, the plugin will attempt to upload
    - if the plugin is installed but a config file is not present / malformed / missing url, a warning will be displayed in the end of the test

### Configuration
- minimal
- optional
    - not having one will not break the test
    - not having one will mean nothing is uploaded UNLESS the url param is
        passed in the invocation command
        - a default db client will be used in such cases and the data will be written into "/tmp"
- will be located in invocation directory
- name: ".config.toml"
- allows for customizing:
    1. DB url and authentication
    2. DB interaction failure should fail test [default: false]
- toml format (see [example](#es))
- see [supported dbs](#supported-db)
### Compitability
- python3.6+
- pytest
- enables adding additional data. see [additional-data](#additional-data)
### Supported DB
- local file system (local)
- Elasticsearch (es)
### Additional data
- each upload can include additional keys and values
- the key will be defined in the config file
- the value will be defined as a either
    - const
    - function that will be invoked in after collecting the doc
    - supported function languages:
        - bash
        - python
    - config file example:
```toml
...
[additional-data]
[additional-data.consts]
name = 'my-name'

[additional-data.bash]
os = 'lsb_release -sr'

[additional-data.python]
current directory = 'import os; print(os.getcwd())' 
```
- *python functions will be called using `exec`*
- *bash functions will be called using `subprocess.check_output`*

### Config File Example
##### ES
```toml
# optional
title = 'my pytest db plugin config'
user = 'avin'

# required
type = 'es'
url = 'my-url'
index = 'my-index'

# optional
must-upload = true

[additional-data]
    [additional-data.consts]
    name = 'avin'

    [additional-data.bash]
    os = 'lsb_release -sr'

    [additional-data.python]
    current directory = 'import os; print(os.getcwd())' 
```

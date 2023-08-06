<h1 align = "center"> expdb </h1>
<p align = "center"><i> Python library and CLI for exporting MySQL databases </i></p>

<p align = "center">
  <a href = "https://www.python.org"><img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href = "https://www.mysql.com/"><img src=https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white/></a>
  <a href = "./LICENSE"><img src = "https://img.shields.io/github/license/Devansh3712/PySQL?style=for-the-badge"></a>
</p>

---

## Installation

- Pre-requisites
    - `MySQL server`
    - `Python 3.9+`

- Using `git`
    - Clone the repository to your local machine
    ```console
    git clone https://github.com/Devansh3712/expdb.git
    ```
    - Install
    ```console
    python setup.py install
    ```

- Using PyPI
    - Windows
    ```console
    pip install expdb
    ```
    - Linux/MacOS
    ```console
    pip3 install expdb
    ```

## Usage

- CLI
    ```
    Usage: expdb [OPTIONS] COMMAND [ARGS]...

    CLI for exporting MySQL databases in various file formats

    Available formats: BIN, CSV, JSON, SQL

    Options:
    --help  Show this message and exit.

    Commands:
    exportall   Export all tables from a database
    exportdb    Export a whole database in SQL file format
    exportmany  Export multiple tables from a database
    exportone   Export a single table from a database
    ```
    - `exportall`
    Exports all tables in the input database

    - `exportdb`
    Export a whole database in SQL format

    - `exportmany`
    Export multiple tables from the input database

    - `exportone`
    Export a single table from the input database

- Library

```python
from expdb import JSON

OBJ = JSON(username = "root", password = "root", database = "test")
EXPORT = OBJ.exportmany(tables = ["users", "sales"])
```

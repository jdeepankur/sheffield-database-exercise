# Sheffield Junior Programmer Exercise

*A Python application demonstrating data ingestion, a REST API, and a CSV export pipeline backed by MySQL*

---

## Contents

1. [Running the Application](#1-running-the-application)
2. [Design & Implementation](#2-design--implementation)
3. [Application Flow](#3-application-flow)
4. [Future Improvements](#4-future-improvements)

---

## 1. Running the Application

This section provides complete, step-by-step instructions for setting up and running every component of the application from a clean checkout.

### 1.1 Prerequisites

Before proceeding, ensure the following software is installed and available on your `PATH`:

- **Python 3.11+** — the application uses f-string features and walrus operators that require Python 3.8 at minimum; 3.11 is recommended.
- **Docker** — the database setup script automatically pulls and starts a `mysql:latest` container. Docker must be running before any Python script is executed.
- **pip** — used to install Python dependencies.

### 1.2 Clone the Repository and Install Dependencies

```bash
# From the root of the repository
pip install -r requirements.txt
```

All required packages are pinned in `requirements.txt`. If you encounter issues, a possible reason is that your mySQL installation is outdated and cached. In that case, you could run the following:
```bash
# From the root of the repository
python3 -m pip install mysql-connector-python==9.6.0 --force-reinstall
```

### 1.3 Configure the Environment File

The application reads all configuration from a `.env` file in the project root. An example is provided:

```bash
cp .env.example .env
```

The default values work out of the box if you are running Docker locally. Edit `.env` only if you need a different port or database password:

| Variable      | Default    |
|---------------|------------|
| `DB_HOST`     | localhost  |
| `DB_NAME`     | shopdb     |
| `DB_USER`     | root       |
| `DB_PASSWORD` | p@ssw0rd   |
| `DB_PORT`     | 3306       |
| `API_PORT`    | 8000       |
| `OUTPUT_DIR`  | output     |

### 1.4 Step 1 — Set Up the Database and Import Data

Run `task_one.py` to seed the database. This script will:

1. Invoke `utilities/dbsetup.py`, which checks whether a Docker container named `mySQL-shop` is already running. If not, it either restarts an existing stopped container or creates a fresh one with `docker run`.
2. Wait (with a live progress bar) until MySQL is accepting connections.
3. Create the `shopdb` database if it does not exist.
4. Read `data/customers_data.csv` and `data/orders_data.csv`, creating the `customers` and `orders` tables automatically, then inserting every row that does not already exist.

```bash
python task_one.py
```

Expected output:

```
Task 1 has run successfully.
The database has been populated with data from the CSV files.
```

### 1.5 Step 2 — Start the REST API

```bash
python task_two.py
```

The Flask development server starts on the port defined by `API_PORT` (default `8000`). Keep this terminal open while using the API.

**Available endpoints:**

| URL | Description |
|-----|-------------|
| `GET /customer/{id}` | Returns customer profile and orders as JSON |
| `GET /customer/{id}?pretty=true` | Returns the same data formatted as HTML |

**Example requests:**

```bash
# JSON response
curl http://localhost:8000/customer/CUS2279

# HTML response
curl http://localhost:8000/customer/CUS2279?pretty=true

# Open in a browser for the HTML view
open http://localhost:8000/customer/CUS2279?pretty=true
```

### 1.6 Step 3 — Run the Export Script

```bash
python task_three.py
```

This produces two files in the directory specified by `OUTPUT_DIR` (default `output/`):

- `output/active_customers.csv` — all customers whose `Status` is `Active`, with a computed `Full Name` column appended.
- `output/active_customer_orders.csv` — all orders belonging to those active customers, with a computed `Total Price` column appended.

Reference outputs are available in `output.example/` for comparison.

### 1.7 Optional — Regenerate Sample Data

If you wish to produce a fresh randomised dataset before running the pipeline:

```bash
python utilities/data_generator.py
```

This overwrites `data/customers_data.csv` and `data/orders_data.csv` with 50 new synthetic records each.

---

## 2. Design & Implementation

### 2.1 Database: MySQL via Docker

MySQL was chosen as the relational database for several practical reasons:

- **Structured, relational data** — the dataset consists of two clearly related entities (customers and orders) with a foreign-key relationship on `CustomerID`. A relational database is a natural and well-supported fit.
- **Ubiquity and tooling** — MySQL is one of the most widely deployed databases; it has mature Python drivers, excellent documentation, and broad familiarity.
- **Docker for portability** — wrapping MySQL in a Docker container removes the need for reviewers to install and configure a local MySQL server. The setup script in `utilities/dbsetup.py` handles container lifecycle automatically (start, restart, create), making the application self-contained with zero manual DB configuration.
- **Schema-free table creation** — because the CSV column names are used directly to create the table schema at insertion time, the application can adapt to different CSV structures without hard-coded `CREATE TABLE` statements. All columns use `VARCHAR(255)`, which is flexible enough for the data at hand.

A lightweight alternative like SQLite would have eliminated the Docker dependency entirely, but MySQL better reflects a production-like setup and demonstrates networking, container orchestration, and real TCP connectivity.

### 2.2 Web Framework: Flask

Flask was selected for the API layer because:

- **Minimal overhead** — the API surface is a single endpoint. Flask imposes no boilerplate beyond what is needed, keeping the code concise.
- **Flexibility** — the custom `optionalParam` decorator in `utilities/api.py` integrates cleanly with Flask's request context, allowing query-string parameters to be declared and type-validated inline with the view function.
- **Dual-format responses** — the same endpoint serves both JSON (for machine consumers) and HTML (for browser viewing) via the `?pretty=true` query parameter. Flask's minimal structure made it straightforward to branch on this parameter and return either `dict` (auto-serialised to JSON by Flask) or a raw HTML string.

### 2.3 Key Libraries

| Library | Reason for inclusion |
|---------|----------------------|
| `mysql-connector-python` | Official MySQL driver for Python; provides the cursor interface used throughout `database.py`. |
| `python-dotenv` / `dotenv` | Reads the `.env` file; cleanly separates secrets and config from source code, following twelve-factor app principles. |
| `rich` | Renders the animated spinner and progress bar while waiting for MySQL to become available, giving clear visual feedback during startup. |
| `flask-marshmallow` / `Flask-SQLAlchemy` | Included in `requirements.txt` for potential structured serialisation and ORM use; not yet actively used in the current codebase. |
| `names` / `rstr` | Used by `data_generator.py` to produce realistic synthetic customer records with valid-looking names, emails, and UK phone numbers. |

### 2.4 Notable Design Decisions

**SQL injection guard.** Rather than switching to parameterised queries at the driver level (the conventional approach), a decorator `sql_guard` was implemented to check all string arguments for injection tokens (`;` and `--`) before any SQL is executed. This is a defence-in-depth measure layered on top of the existing query structure, and allows use to take better advantage of both f-string readability and the customised control that Python offers in general.

**Table and schema auto-creation.** The `Database.ensureTable` method creates the table on the first insert, deriving column names from the CSV headers. This avoids any migration tooling for a project of this scale and keeps setup to a single script run.

**Dual-format API.** The decision to return both JSON and HTML from the same endpoint — controlled by `?pretty=true` — was made to support both programmatic API consumers and quick human inspection in a browser without requiring a separate frontend server.

**Functional column transformation in `task_three.py`.** The `addNewField` function is written in a generic, functional style: it accepts a list of field names and an arbitrary `operation` callable, then appends the result as a new column. This means the same function handles both the string concatenation of `Full Name` and the numeric multiplication of `Total Price`, keeping the export logic DRY.

---

## 3. Application Flow

This section traces data through all three tasks and the supporting utilities.

### 3.1 Overview

```
CSV files  →  task_one.py   →  MySQL (Docker)
MySQL      →  task_two.py   →  HTTP endpoint
MySQL      →  task_three.py →  Output CSVs
```

### 3.2 Task 1 — Data Ingestion

1. `task_one.py` imports `Database` from `utilities/database.py`. This import triggers the module-level setup code in `database.py`: `dbsetup.run()` is called, which inspects running Docker containers and either creates, restarts, or does nothing with the `mySQL-shop` container. `dbsetup.wait()` then polls MySQL on the configured port until it accepts connections (up to 30 attempts, 2 seconds apart).
2. A MySQL connection is established and a buffered cursor created. The `shopdb` database is created if absent, then selected.
3. For each CSV file (`customers_data.csv`, `orders_data.csv`), the script:
   - Opens the file and reads the header row, stripping spaces from column names (e.g. `First Name` becomes `FirstName`).
   - For each subsequent row, calls `Database.getRow(table, primaryKey, id)` to check whether a record with that ID already exists.
   - If no existing record is found, calls `Database.insert(table, columns, row)`, which first ensures the table exists (creating it with all-`VARCHAR(255)` columns if not), then executes the `INSERT` statement.
4. Every insert is immediately committed. The idempotency check (`getRow` before `insert`) means re-running `task_one.py` is safe and will not duplicate rows.

### 3.3 Task 2 — REST API

1. `task_two.py` imports `Database` (triggering the same Docker/MySQL startup described above) and registers a single Flask route: `GET /customer/<id>`.
2. The view function `fetchCustomer` is decorated with `@api.optionalParam("pretty", False, type=bool)`. At request time the decorator reads `?pretty` from the query string, coerces it to `bool`, falls back to `False` if the coercion fails, and sets it as an attribute on the wrapper function so the body can access it as `fetchCustomer.pretty`.
3. **JSON path** (`pretty=False`, the default):
   - `Database.getRow("customers", "UniqueID", id)` is called. If no record is returned, a `{"error": "Customer not found"}` dict is returned, which Flask serialises to JSON with a 200 status.
   - Otherwise, all orders for that customer are fetched from `Database.getRow("orders", "CustomerID", customer[0])`.
   - A structured response dict is assembled with a `"Customer Profile"` key and, if orders exist, an `"Orders"` key whose sub-keys are order IDs. Flask auto-serialises this to JSON.
4. **HTML path** (`pretty=true`):
   - The customer tuple is passed through `utilities/html.py`'s `htmlClean` function, which applies `html.escape` to every field, guarding against stored XSS before the values are interpolated into an HTML template string.
   - Customer details are rendered as an HTML table. Orders, if present, are appended as additional tables below.
   - The raw HTML string is returned directly; Flask sends it with a `text/html` content type.
5. `api.start()` calls `app.run(port=env("API_PORT"))`, starting the development server.

### 3.4 Task 3 — Export Script

1. All column names for the `customers` table are retrieved via `Database.getHeaders("customers")` (which issues `SHOW COLUMNS`).
2. Active customers are fetched with `Database.getRow("customers", "Status", "Active")`, returning a list of tuples.
3. `addNewField` is called to append a `Full Name` column: it iterates over every customer tuple, calls `wordjoin(FirstName, Surname)` (a simple `" ".join(*args)`), and appends the result to the tuple. The `customer_headers` list is also extended in-place.
4. For each active customer a dictionary entry is created mapping their `UniqueID` to their orders (fetched by `CustomerID`).
5. Order numeric fields (`UnitPrice`, `Quantity`) are converted from strings to Python numbers using `eval`. A `Total Price` column is then appended by `addNewField` using `operator.mul` and a `".2f"` format string.
6. The output directory (`OUTPUT_DIR` from `.env`) is created if it does not exist. Both CSV files are written by joining headers and row values with commas.

---

## 4. Future Improvements

Given more time, the following changes and additions would be prioritised.

### 4.1 Parameterised SQL Queries

The current `sql_guard` decorator checks for `;` and `--` tokens as a defence against injection, but this approach is inherently incomplete — there are injection payloads that do not use these tokens. The correct fix is to replace all f-string SQL construction with parameterised queries using the `%s` placeholder syntax supported by `mysql-connector-python`:

```python
cursor.execute(
    "SELECT * FROM %s WHERE %s = %s",
    (table, column, value)
)
```

This delegates escaping entirely to the driver and eliminates the class of vulnerability at source.

### 4.2 Replace `eval` with Explicit Type Conversion

In `task_three.py`, string values from the database are converted to numbers using `eval`. While the data originates from a controlled CSV source, `eval` is an unnecessary security risk. Replacing it with `float()` or `int()` would be both safer and more explicit.

### 4.3 A Production WSGI Server

Flask's built-in development server is single-threaded and not suitable for production or concurrent load testing. The application would benefit from being served via more production-friendly alternatives such as **Gunicorn** or **uWSGI**:


### 4.4 Proper HTTP Status Codes and Error Handling

The "Customer not found" response currently returns HTTP 200. A `404 Not Found` would be more semantically correct and easier to handle by API consumers. Similarly, unhandled exceptions (e.g. database connection failures mid-request) should be caught and returned as `500 Internal Server Error` rather than an unhandled Python traceback.

### 4.5 Database Connection Pooling

The application opens a single persistent `mysql.connector` connection at module import time. Under concurrent API load this will fail or produce race conditions. Switching to `mysql.connector.pooling.MySQLConnectionPool` or using SQLAlchemy's connection pool (already in `requirements.txt` via Flask-SQLAlchemy) would resolve this.

### 4.6 A Proper ORM Layer

`Flask-SQLAlchemy` and `flask-marshmallow` are already listed as dependencies. Migrating `utilities/database.py` to use SQLAlchemy models would bring typed schemas, automatic migration support (via Alembic), and eliminate the need for the hand-rolled `Database` wrapper class entirely.

### 4.7 Tests

There are currently no automated tests. A minimal test suite using `pytest` and Flask's built-in test client would cover:

- `GET /customer/<id>` returns correct JSON structure.
- `GET /customer/<id>?pretty=true` returns valid HTML.
- `GET /customer/INVALID` returns a 404.
- `task_three.py` output CSVs match expected headers and row counts.

### 4.8 Structured Logging

Print statements are used for status output. Replacing these with Python's `logging` module would allow log levels to be controlled via environment variables and log output to be directed to files or a log aggregator in production.

### 4.9 Docker Compose

Currently the application depends on Docker being installed but manages the container itself through `subprocess` calls. A `docker-compose.yml` would replace this ad-hoc orchestration with a declarative definition, making the full stack (MySQL + Python app) startable with a single `docker compose up` command and easier to integrate into CI pipelines.

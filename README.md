[Backend Service (Python/Node)]
  - Handles dataset ingestion (JSON → DB)
  - Exposes API endpoints (optional)
  - Can run unit tests

[Database (PostgreSQL / SQLite)]
  - Stores dataset
  - Allows queries by Grafana

[Grafana Frontend]
  - Connects to DB
  - Dashboards / panels visualize data
  - Users can customize variables, axes, filters

[Containerization]
  - Docker Compose orchestrates backend, DB, and Grafana

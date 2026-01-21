# Task
Goal: Using the provided data from some of our systems, create a fullstack application with a
customizable visualization for it.
Context: A core part of our product offering is visualizing data we collect from our clients. In the
field, we have systems that are taking pictures of products, collecting data about the state of the
molding machine, running AI inference models, and making predictions about the state of the
product. All of this data is available to us to use in informative visualizations that can help
demonstrate our value.
Requirements:
Backend
● Use the dataset provided at: https://static.krevera.com/dataset.json. This dataset
is structured as a list of objects representing real data from some of our systems.
Each entry is a product we inspected for defects.
● Your backend must access the dataset offline, i.e. you should not have it make
requests to the dataset at the provided URL directly. There should be a
seeding/ingest step of some kind that pulls the dataset into your application only
once. Likewise, you should not do this step manually and package the dataset
with your code because...
● Your backend should take a URL as an input to a dataset in the same format as
the one provided. We will be using a different (larger) dataset to evaluate your
application.
Frontend
● Create a visualization of one or more aspects of this dataset. This is purposely
open ended, you can use whatever data you want from the dataset. That being
said, you should probably incorporate something from every product entry in it.
● Your visualization must be customizable in some way by the user.
○ Example: you decide to make a graph of data from the molding machine
over time. An acceptable customization could be that the user chooses in
the frontend which variable (or variables) are being plotted on the graph.
Alternatively, maybe the user can customize the X axis to group data by
days or hours.

Your project must have clear instructions on how to run it, how to set the dataset URL,
and a brief description of what features it includes (see next section).

Additional Features (complete at least 2):
Your application is containerized
Your application uses a language for the frontend that is different from the backend
Your application works on mobile clients
Your application uses a database to store the dataset
Your application has more than one visualization
Your application uses LocalStack to emulate AWS services
Your application has a test suite
Thinking of something else you want to do? Let us know!
Grading Criteria:
The application meets all the functional requirements for the frontend and backend
The application includes documentation on how to run it and a brief description of its
capabilities
The application has at least 2 of the additional features listed
The application has good code quality and is written with best practices in mind
The application is performant with larger datasets

# Project Structure

This project is organized into the following directories:

- `backend/`: Contains the Python FastAPI application that provides an API for the data.
- `grafana/`: Contains configuration files for Grafana, including provisioning for the datasource and dashboards.
- `scripts/`: Contains the data ingestion script.
- `dataset.json`: The raw dataset file.
- `setup.sh`: A script to set up the project.

# Setup

1.  **Install dependencies:**
    - Python 3.9+
    - Poetry (for Python dependency management)
    - PostgreSQL
    - Grafana

2.  **Configure environment variables:**
    Create a `.env` file in the root of the project and add the following:
    ```
    DATABASE_URL="postgresql://user:password@localhost/db"
    DATASET_URL="https://static.krevera.com/dataset.json"
    POSTGRES_USER="user"
    POSTGRES_PASSWORD="password"
    POSTGRES_DB="db"
    ```

3.  **Setup the backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    cd ..
    ```

4.  **Setup the database:**
    - Make sure your PostgreSQL server is running.
    - Create a database, user, and password that match the values in your `.env` file.

5.  **Ingest the data:**
    ```bash
    python scripts/ingest_data.py
    ```

# Running the Application

1.  **Start the backend:**
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

2.  **Start Grafana:**
    - Follow the instructions for your operating system to start the Grafana server.
    - Open Grafana in your browser (usually at `http://localhost:3000`).
    - The PostgreSQL datasource and a default dashboard will be pre-configured.

# Features

- **Backend API:** A Python FastAPI backend provides an API for the data.
- **PostgreSQL Database:** The dataset is stored in a PostgreSQL database.
- **Grafana Frontend:** Grafana is used to visualize the data from the PostgreSQL database.
- **Data Ingestion Script:** A script is provided to fetch the dataset from a URL and ingest it into the database.
- **Customizable Visualizations:** Grafana dashboards can be customized by the user.
- **Separate Frontend and Backend:** The application uses Python for the backend and Grafana for the frontend.
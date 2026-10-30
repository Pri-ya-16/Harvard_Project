# 🏛️ Harvard Artifacts Explorer

An interactive web application built with **Streamlit** and **Microsoft SQL Server** to explore, analyze, and query artifact metadata, media, and color palettes from the **Harvard Art Museums Data API**.

## 📌 Features

* **Interactive SQL Querying**: Run 20+ pre-defined analytical queries directly on a SQL Server database.

* **Dynamic Parameter Inputs**: Search specific artifact colors and attributes interactively.

* **Data Export**: Easily export query results to CSV format.

* **Database Status Inspection**: Built-in tools to inspect SQL Server tables and schema connection states.

## 🛠️ Tech Stack & Requirements

* **Frontend & Interface**: [Streamlit](https://streamlit.io/)

* **Database**: Microsoft SQL Server

* **Data Processing**: Python (`pandas`, `requests`, `pyodbc`)

* **API Data Source**: [Harvard Art Museums API](https://github.com/harvardartmuseums/api-docs)

## 📂 Project Structure

```
├── app.py              # Main Streamlit web application
├── Classification.py   # Script to fetch records by classification from API
├── code.py             # Script to fetch available classifications
├── sqlconnection.py    # Database connection test script
└── README.md           # Project documentation

```

## 🗄️ Database Schema

The database (`HarvardArtDB`) structured in SQL Server includes three core tables:

1. **`dbo.artifact_metadata`**: Contains artifact details such as `id`, `title`, `culture`, `period`, `century`, `department`, and `accessionyear`.

2. **`dbo.artifact_media`**: Tracks media assets with `objectid`, `imagecount`, `mediacount`, `datebegin`, `dateend`, and `rank`.

3. **`dbo.artifact_colors`**: Maps color palettes per artifact including `objectid`, `color`, `hue`, `spectrum`, `percent`, and `css3`.

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed alongside **ODBC Driver 17 for SQL Server** and Microsoft SQL Server Express.

### 2. Install Dependencies

```
pip install streamlit pandas pyodbc requests

```

### 3. Database Configuration

Make sure your SQL Server database is created (`HarvardArtDB`) and update your database credentials in `app.py` if necessary:

```
r"DRIVER={ODBC Driver 17 for SQL Server};"
r"SERVER=YOUR_SERVER_NAME;"
r"DATABASE=HarvardArtDB;"

```

### 4. Run the Application

Launch the Streamlit web server:

```
streamlit run app.py

```

## 📊 Example Queries Handled

* Fetch 11th-century Byzantine artifacts

* Calculate average media ranks and coverage percentages

* Filter artifacts by accession year and specific historical periods

* Detailed breakdown of color palettes and hues per artifact classification
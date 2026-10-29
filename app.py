
import streamlit as st
import pandas as pd
import pyodbc

# --------------------------------------------------
# 1. Streamlit page settings
# --------------------------------------------------
st.set_page_config(
    page_title="Harvard Artifacts Explorer",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Harvard Artifacts Explorer")
st.write("Explore Harvard Art Museums data using SQL queries.")

# --------------------------------------------------
# 2. Connect to SQL Server
# --------------------------------------------------
@st.cache_resource
def get_connection():
    return pyodbc.connect(
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=PRIYA\SQLEXPRESS;"
        r"DATABASE=HarvardArtDB;"
        r"Trusted_Connection=yes;"
        r"TrustServerCertificate=yes;"
    )


# --------------------------------------------------
# 3. SQL queries
# All table names use the dbo schema
# --------------------------------------------------
queries = {
    "1. 11th-century Byzantine artifacts": """
        SELECT *
        FROM dbo.artifact_metadata
        WHERE century LIKE '%11th%'
          AND culture LIKE '%Byzantine%';
    """,

    "2. Unique cultures": """
        SELECT DISTINCT culture
        FROM dbo.artifact_metadata
        WHERE culture IS NOT NULL
        ORDER BY culture;
    """,

    "3. Artifacts from the Archaic Period": """
        SELECT *
        FROM dbo.artifact_metadata
        WHERE period LIKE '%Archaic%';
    """,

    "4. Titles by accession year (descending)": """
        SELECT title, accessionyear
        FROM dbo.artifact_metadata
        ORDER BY accessionyear DESC;
    """,

    "5. Artifact count per department": """
        SELECT department, COUNT(*) AS artifact_count
        FROM dbo.artifact_metadata
        GROUP BY department
        ORDER BY artifact_count DESC;
    """,

    "6. Artifacts with more than one image": """
        SELECT m.id, m.title, a.imagecount
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        WHERE a.imagecount > 1;
    """,

    "7. Average media rank": """
        SELECT AVG(CAST([rank] AS FLOAT)) AS average_rank
        FROM dbo.artifact_media;
    """,

    "8. Color count greater than media count": """
        SELECT objectid, colorcount, mediacount
        FROM dbo.artifact_media
        WHERE colorcount > mediacount;
    """,

    "9. Artifacts dated 1500–1600": """
        SELECT m.id, m.title, a.datebegin, a.dateend
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        WHERE a.datebegin <= 1600
          AND a.dateend >= 1500;
    """,

    "10. Artifacts with no media files": """
        SELECT COUNT(*) AS artifacts_without_media
        FROM dbo.artifact_metadata AS m
        LEFT JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        WHERE a.objectid IS NULL
           OR a.mediacount = 0;
    """,

    "11. Distinct color hues": """
        SELECT DISTINCT hue
        FROM dbo.artifact_colors
        WHERE hue IS NOT NULL
        ORDER BY hue;
    """,

    "12. Top five colors by frequency": """
        SELECT TOP 5 color, COUNT(*) AS frequency
        FROM dbo.artifact_colors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY frequency DESC;
    """,

    "13. Average coverage percentage by hue": """
        SELECT hue, AVG(percent) AS average_coverage
        FROM dbo.artifact_colors
        WHERE hue IS NOT NULL
        GROUP BY hue
        ORDER BY average_coverage DESC;
    """,

    "14. Colors for a given artifact ID": """
        SELECT objectid, color, spectrum, hue, percent, css3
        FROM dbo.artifact_colors
        WHERE objectid = ?;
    """,

    "15. Total color entries": """
        SELECT COUNT(*) AS total_color_entries
        FROM dbo.artifact_colors;
    """,

    "16. Titles and hues for Byzantine artifacts": """
        SELECT DISTINCT m.title, c.hue
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_colors AS c
            ON m.id = c.objectid
        WHERE m.culture LIKE '%Byzantine%'
        ORDER BY m.title;
    """,

    "17. Each artifact title and its hues": """
        SELECT m.title, c.hue
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_colors AS c
            ON m.id = c.objectid
        ORDER BY m.title;
    """,

    "18. Titles, cultures and ranks where period is not null": """
        SELECT m.title, m.culture, a.[rank]
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        WHERE m.period IS NOT NULL
          AND LTRIM(RTRIM(m.period)) <> '';
    """,

    "19. Top-10-ranked artifacts containing Grey": """
        SELECT DISTINCT m.title, a.[rank], c.hue
        FROM dbo.artifact_metadata AS m
        INNER JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        INNER JOIN dbo.artifact_colors AS c
            ON m.id = c.objectid
        WHERE a.[rank] <= 10
          AND c.hue = 'Grey'
        ORDER BY a.[rank];
    """,

    "20. Count by classification and average media count": """
        SELECT
            m.classification,
            COUNT(*) AS artifact_count,
            AVG(CAST(a.mediacount AS FLOAT)) AS average_media_count
        FROM dbo.artifact_metadata AS m
        LEFT JOIN dbo.artifact_media AS a
            ON m.id = a.objectid
        GROUP BY m.classification
        ORDER BY artifact_count DESC;
    """,

}


# --------------------------------------------------
# 4. Check connection and display database status
# --------------------------------------------------
try:
    connection = get_connection()

    database_name = pd.read_sql_query(
        "SELECT DB_NAME() AS database_name;",
        connection
    ).iloc[0, 0]

    st.success(f"Connected to SQL Server database: {database_name}")

except Exception as error:
    st.error("Could not connect to SQL Server.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# 5. Display database tables for troubleshooting
# --------------------------------------------------
with st.expander("Check database tables"):
    try:
        tables = pd.read_sql_query("""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME;
        """, connection)

        st.dataframe(tables, use_container_width=True)

    except Exception as error:
        st.error(str(error))


# --------------------------------------------------
# 6. Select and execute a query
# --------------------------------------------------
st.subheader("SQL Query Explorer")

selected_question = st.selectbox(
    "Choose a question",
    list(queries.keys())
)

# Show the SQL query being executed
with st.expander("View SQL query"):
    st.code(queries[selected_question], language="sql")

# Question 14 requires an artifact ID
artifact_id = None

if selected_question.startswith("14."):
    artifact_id = st.number_input(
        "Enter Harvard artifact ID",
        min_value=1,
        step=1
    )

if st.button("Run Query", type="primary"):
    try:
        cursor = connection.cursor()

        if selected_question.startswith("14."):
            cursor.execute(
                queries[selected_question],
                (int(artifact_id),)
            )
        else:
            cursor.execute(queries[selected_question])

        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            result = pd.DataFrame.from_records(
                rows,
                columns=columns
            )

            st.success(
                f"Query executed successfully. "
                f"Rows returned: {len(result)}"
            )

            # Summary for numeric result columns
            if len(result.columns) == 1 and len(result) == 1:
                st.metric(
                    label=result.columns[0],
                    value=str(result.iloc[0, 0])
                )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

            # Download results
            st.download_button(
                label="Download results as CSV",
                data=result.to_csv(index=False).encode("utf-8"),
                file_name="harvard_query_results.csv",
                mime="text/csv"
            )

        else:
            st.success("Query executed successfully.")

        cursor.close()

    except Exception as error:
        st.error("Unable to execute the query.")
        st.code(str(error))

        st.info(
            "Verify the table schema, column names, and database contents."
        )

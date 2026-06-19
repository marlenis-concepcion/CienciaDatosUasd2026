"""ETL module for loading OULAD data into PostgreSQL database."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger(__name__)


class PostgreSQLLoader:
    """Handles ETL operations for OULAD data into PostgreSQL."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "oulad_uasd",
        user: str = "postgres",
        password: str = "",
        min_pool_size: int = 2,
        max_pool_size: int = 10,
    ):
        """Initialize PostgreSQL connection pool."""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_string = (
            f"postgresql://{user}:{password}@{host}:{port}/{database}"
        )

        try:
            self.pool = SimpleConnectionPool(
                min_pool_size,
                max_pool_size,
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                connect_timeout=10,
            )
            logger.info("PostgreSQL connection pool created successfully.")
        except psycopg2.Error as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise

    def get_connection(self):
        """Get a connection from the pool."""
        return self.pool.getconn()

    def release_connection(self, conn):
        """Release a connection back to the pool."""
        self.pool.putconn(conn)

    def close_all_connections(self):
        """Close all connections in the pool."""
        self.pool.closeall()

    def init_database(self, schema_script: Path) -> bool:
        """Execute schema creation script."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            with open(schema_script, "r") as f:
                schema_sql = f.read()

            cursor.execute(schema_sql)
            conn.commit()

            self._log_load("schema_creation", 0, "completed", None)
            logger.info("Database schema created successfully.")
            return True

        except Exception as e:
            logger.error(f"Error creating schema: {e}")
            conn.rollback()
            self._log_load("schema_creation", 0, "failed", str(e))
            return False
        finally:
            self.release_connection(conn)

    def load_courses(self, df: pd.DataFrame) -> int:
        """Load courses data."""
        if df.empty:
            return 0

        conn = self.get_connection()
        cursor = conn.cursor()
        start_time = datetime.now()

        try:
            data = [
                (row["code_module"], row["code_presentation"], row["module_presentation_length"])
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO courses (code_module, code_presentation, module_presentation_length)
                   VALUES %s ON CONFLICT (code_module) DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("courses", record_count, "completed", None)
            logger.info(f"Loaded {record_count} course records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading courses: {e}")
            conn.rollback()
            self._log_load("courses", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def load_student_info(self, df: pd.DataFrame) -> int:
        """Load student information with ordinal encoding."""
        if df.empty:
            return 0

        df = self._encode_ordinals(df)
        conn = self.get_connection()
        cursor = conn.cursor()
        start_time = datetime.now()

        try:
            data = [
                (
                    row["id_student"],
                    row["code_module"],
                    row["code_presentation"],
                    row.get("gender"),
                    row.get("gender_ordinal"),
                    row.get("region"),
                    row.get("region_ordinal"),
                    row.get("highest_education"),
                    row.get("highest_education_ordinal"),
                    row.get("imd_band"),
                    row.get("imd_band_ordinal"),
                    row.get("imd_midpoint"),
                    row.get("age_band"),
                    row.get("age_band_ordinal"),
                    row.get("num_of_prev_attempts"),
                    row.get("studied_credits"),
                    row.get("disability"),
                    row.get("disability_ordinal"),
                    row.get("final_result"),
                    row.get("final_result_ordinal"),
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO student_info
                   (id_student, code_module, code_presentation, gender, gender_ordinal,
                    region, region_ordinal, highest_education, highest_education_ordinal,
                    imd_band, imd_band_ordinal, imd_midpoint, age_band, age_band_ordinal,
                    num_of_prev_attempts, studied_credits, disability, disability_ordinal,
                    final_result, final_result_ordinal)
                   VALUES %s ON CONFLICT DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("student_info", record_count, "completed", None)
            logger.info(f"Loaded {record_count} student records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading student info: {e}")
            conn.rollback()
            self._log_load("student_info", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def load_assessments(self, df: pd.DataFrame) -> int:
        """Load assessment data with ordinal encoding."""
        if df.empty:
            return 0

        df = self._encode_ordinals(df)
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            data = [
                (
                    row["id_assessment"],
                    row["code_module"],
                    row.get("id_type"),
                    row.get("assessment_type"),
                    row.get("assessment_type_ordinal"),
                    row["date"],
                    row["weight"],
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO assessments
                   (id_assessment, code_module, id_type, assessment_type, assessment_type_ordinal,
                    date, weight)
                   VALUES %s ON CONFLICT (id_assessment) DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("assessments", record_count, "completed", None)
            logger.info(f"Loaded {record_count} assessment records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading assessments: {e}")
            conn.rollback()
            self._log_load("assessments", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def load_student_assessments(self, df: pd.DataFrame) -> int:
        """Load student assessment scores."""
        if df.empty:
            return 0

        df = self._encode_ordinals(df)
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            data = [
                (
                    row["id_assessment"],
                    row["id_student"],
                    row["date_submitted"],
                    row.get("is_banked"),
                    row.get("score"),
                    row.get("score_ordinal"),
                    row.get("score_category"),
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO student_assessment
                   (id_assessment, id_student, date_submitted, is_banked, score, score_ordinal, score_category)
                   VALUES %s ON CONFLICT DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("student_assessment", record_count, "completed", None)
            logger.info(f"Loaded {record_count} student assessment records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading student assessments: {e}")
            conn.rollback()
            self._log_load("student_assessment", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def load_vle(self, df: pd.DataFrame) -> int:
        """Load VLE (Virtual Learning Environment) resources."""
        if df.empty:
            return 0

        df = self._encode_ordinals(df)
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            data = [
                (
                    row["id_site"],
                    row["code_module"],
                    row.get("id_week"),
                    row.get("activity_type"),
                    row.get("activity_type_ordinal"),
                    row.get("week_from"),
                    row.get("week_to"),
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO vle
                   (id_site, code_module, id_week, activity_type, activity_type_ordinal, week_from, week_to)
                   VALUES %s ON CONFLICT (id_site) DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("vle", record_count, "completed", None)
            logger.info(f"Loaded {record_count} VLE records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading VLE: {e}")
            conn.rollback()
            self._log_load("vle", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def load_student_vle(self, df: pd.DataFrame) -> int:
        """Load student VLE interactions with ordinal encoding."""
        if df.empty:
            return 0

        df = self._encode_ordinals(df)
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            data = [
                (
                    row["id_site"],
                    row["id_student"],
                    row["date"],
                    row["sum_click"],
                    row.get("sum_click_ordinal"),
                    row.get("click_category"),
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """INSERT INTO student_vle
                   (id_site, id_student, date, sum_click, sum_click_ordinal, click_category)
                   VALUES %s ON CONFLICT DO NOTHING""",
                data,
                page_size=1000,
            )

            conn.commit()
            record_count = cursor.rowcount
            self._log_load("student_vle", record_count, "completed", None)
            logger.info(f"Loaded {record_count} student VLE records.")
            return record_count

        except Exception as e:
            logger.error(f"Error loading student VLE: {e}")
            conn.rollback()
            self._log_load("student_vle", 0, "failed", str(e))
            return 0
        finally:
            self.release_connection(conn)

    def create_fulldomaine_views(self) -> bool:
        """Create FullDomain aggregated views."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Populate FullDomain Assessment
            cursor.execute("""
                INSERT INTO fulldomaine_assessment
                (id_student, id_assessment, code_module, assessment_type, assessment_weight,
                 student_score, score_ordinal, score_performance, date_submitted, days_to_deadline, is_banked)
                SELECT
                    sa.id_student,
                    sa.id_assessment,
                    a.code_module,
                    a.assessment_type,
                    a.weight,
                    sa.score,
                    sa.score_ordinal,
                    CASE
                        WHEN sa.score IS NULL THEN 'No Submitted'
                        WHEN sa.score >= 70 THEN 'Excellent'
                        WHEN sa.score >= 60 THEN 'Good'
                        WHEN sa.score >= 50 THEN 'Pass'
                        ELSE 'Fail'
                    END,
                    sa.date_submitted,
                    (a.date - sa.date_submitted),
                    sa.is_banked
                FROM student_assessment sa
                JOIN assessments a ON sa.id_assessment = a.id_assessment
                ON CONFLICT DO NOTHING
            """)

            # Populate FullDomain VLE
            cursor.execute("""
                INSERT INTO fulldomaine_vle
                (id_student, id_site, code_module, activity_type, date_accessed, week_accessed,
                 total_clicks, click_ordinal, engagement_level, is_first_14_days)
                SELECT
                    sv.id_student,
                    sv.id_site,
                    v.code_module,
                    v.activity_type,
                    sv.date,
                    v.id_week,
                    sv.sum_click,
                    sv.sum_click_ordinal,
                    CASE
                        WHEN sv.sum_click = 0 THEN 'None'
                        WHEN sv.sum_click <= 5 THEN 'Low'
                        WHEN sv.sum_click <= 20 THEN 'Medium'
                        ELSE 'High'
                    END,
                    CASE WHEN sv.date <= 14 THEN 1 ELSE 0 END
                FROM student_vle sv
                JOIN vle v ON sv.id_site = v.id_site
                ON CONFLICT DO NOTHING
            """)

            conn.commit()
            logger.info("FullDomain views created successfully.")
            return True

        except Exception as e:
            logger.error(f"Error creating FullDomain views: {e}")
            conn.rollback()
            return False
        finally:
            self.release_connection(conn)

    def _encode_ordinals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables as ordinals."""
        ordinal_mappings = {
            "gender": {"M": 1, "F": 0},
            "disability": {"Y": 1, "N": 0},
            "final_result": {"Withdrawn": 0, "Fail": 1, "Pass": 2, "Distinction": 3},
            "assessment_type": {"TMA": 1, "CMA": 2, "Exam": 3},
            "age_band": {
                "0-35": 1,
                "35-55": 2,
                "55<=": 3,
            },
            "highest_education": {
                "No Formal quals": 1,
                "Lower Than A Level": 2,
                "A Level or Equivalent": 3,
                "HE Qualification": 4,
                "Post Graduate Qualification": 5,
            },
        }

        for col, mapping in ordinal_mappings.items():
            if col in df.columns:
                ordinal_col = f"{col}_ordinal"
                df[ordinal_col] = df[col].map(mapping)

        # Encode score as ordinal
        if "score" in df.columns:
            df["score_ordinal"] = pd.cut(
                df["score"], bins=5, labels=[1, 2, 3, 4, 5], ordered=True
            ).astype("Int64")

        if "sum_click" in df.columns:
            df["sum_click_ordinal"] = pd.cut(
                df["sum_click"], bins=5, labels=[1, 2, 3, 4, 5], ordered=True
            ).astype("Int64")

        return df

    def _log_load(self, table_name: str, record_count: int, status: str, error: Optional[str]):
        """Log data load operation."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """INSERT INTO data_load_log (table_name, records_loaded, load_start, load_end, status, error_message)
                   VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s)""",
                (table_name, record_count, status, error),
            )
            conn.commit()
        except Exception as e:
            logger.warning(f"Could not log load operation: {e}")
        finally:
            self.release_connection(conn)


def load_oulad_to_postgresql(
    oulad_df: pd.DataFrame,
    host: str = "localhost",
    port: int = 5432,
    database: str = "oulad_uasd",
    user: str = "postgres",
    password: str = "",
    schema_script: Optional[Path] = None,
) -> bool:
    """
    High-level function to load OULAD data into PostgreSQL.

    Args:
        oulad_df: DataFrame with OULAD data
        host: PostgreSQL host
        port: PostgreSQL port
        database: Database name
        user: Database user
        password: Database password
        schema_script: Path to SQL schema file

    Returns:
        bool: True if successful, False otherwise
    """
    loader = PostgreSQLLoader(host=host, port=port, database=database, user=user, password=password)

    try:
        if schema_script and schema_script.exists():
            if not loader.init_database(schema_script):
                return False

        # Load dimension tables first
        loader.load_courses(oulad_df[["code_module", "code_presentation", "module_presentation_length"]].drop_duplicates())
        loader.load_student_info(oulad_df)

        # Load fact tables
        # Note: You'll need to extract these from the original OULAD files
        # loader.load_assessments(assessments_df)
        # loader.load_student_assessments(student_assessments_df)
        # loader.load_vle(vle_df)
        # loader.load_student_vle(student_vle_df)

        # Create FullDomain views
        loader.create_fulldomaine_views()

        logger.info("OULAD data loaded successfully to PostgreSQL.")
        return True

    except Exception as e:
        logger.error(f"Error in ETL process: {e}")
        return False
    finally:
        loader.close_all_connections()

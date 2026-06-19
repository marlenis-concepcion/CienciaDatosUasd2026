#!/usr/bin/env python3
"""
ETL Orchestrator for OULAD Practical Case 2
Manages the complete pipeline: data loading, DB population, EDA, and paper generation
"""

import logging
import sys
from pathlib import Path

from src.config import ProjectConfig
from src.data import OULADRepository
from src.db_loader import PostgreSQLLoader
from src.eda_extended import ExtendedEDA
from scripts.generate_apa_paper import generate_apa_paper


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("etl_orchestrator.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class OULADETLOrchestrator:
    """Orchestrates the complete ETL pipeline for OULAD analysis."""

    def __init__(
        self,
        root: Path,
        postgres_host: str = "localhost",
        postgres_port: int = 5432,
        postgres_db: str = "oulad_uasd",
        postgres_user: str = "postgres",
        postgres_password: str = "",
    ):
        """Initialize orchestrator with configuration."""
        self.config = ProjectConfig(root=root)
        self.output_dir = self.config.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.db_params = {
            "host": postgres_host,
            "port": postgres_port,
            "database": postgres_db,
            "user": postgres_user,
            "password": postgres_password,
        }

        logger.info("ETL Orchestrator initialized.")

    def step_1_download_and_load_data(self) -> bool:
        """Step 1: Download OULAD dataset and load into pandas."""
        logger.info("=" * 70)
        logger.info("STEP 1: Download and load OULAD data")
        logger.info("=" * 70)

        try:
            repo = OULADRepository(self.config)
            self.df = repo.load_oulad()
            logger.info(f"✓ Loaded {len(self.df)} records from OULAD")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to load OULAD data: {e}")
            return False

    def step_2_init_postgres_database(self) -> bool:
        """Step 2: Initialize PostgreSQL database schema."""
        logger.info("=" * 70)
        logger.info("STEP 2: Initialize PostgreSQL database")
        logger.info("=" * 70)

        try:
            schema_script = Path(__file__).parent / "sql" / "01_schema_oulad.sql"

            if not schema_script.exists():
                logger.warning(f"Schema script not found at {schema_script}")
                return False

            loader = PostgreSQLLoader(**self.db_params)
            success = loader.init_database(schema_script)
            loader.close_all_connections()

            if success:
                logger.info("✓ PostgreSQL database schema initialized")
                return True
            else:
                logger.error("✗ Failed to initialize database schema")
                return False

        except Exception as e:
            logger.error(f"✗ Error initializing database: {e}")
            return False

    def step_3_load_data_to_postgres(self) -> bool:
        """Step 3: Load cleaned data into PostgreSQL."""
        logger.info("=" * 70)
        logger.info("STEP 3: Load data into PostgreSQL")
        logger.info("=" * 70)

        try:
            loader = PostgreSQLLoader(**self.db_params)

            # Load dimension tables
            loader.load_courses(
                self.df[
                    ["code_module", "code_presentation", "module_presentation_length"]
                ].drop_duplicates()
            )

            # Load main student info
            loader.load_student_info(self.df)

            # Create FullDomain views
            loader.create_fulldomaine_views()

            loader.close_all_connections()

            logger.info("✓ Data successfully loaded to PostgreSQL")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to load data to PostgreSQL: {e}")
            return False

    def step_4_extended_eda(self) -> bool:
        """Step 4: Perform extended EDA with multiple visualizations."""
        logger.info("=" * 70)
        logger.info("STEP 4: Extended Exploratory Data Analysis (EDA)")
        logger.info("=" * 70)

        try:
            eda = ExtendedEDA(self.df, self.output_dir / "figures")

            results = eda.run_all_eda()

            logger.info("✓ Extended EDA completed successfully")
            logger.info(f"  - Summary statistics saved")
            logger.info(f"  - Correlation analysis: {len(results['correlation_tests'])} tests")
            logger.info(f"  - ANOVA tests: {len(results['anova_results'])} results")
            logger.info(f"  - Visualizations saved in {eda.output_dir}")

            return True

        except Exception as e:
            logger.error(f"✗ Extended EDA failed: {e}")
            return False

    def step_5_generate_report(self) -> bool:
        """Step 5: Generate EDA report summary."""
        logger.info("=" * 70)
        logger.info("STEP 5: Generate EDA Report")
        logger.info("=" * 70)

        try:
            report_path = self.output_dir / "eda_report.txt"

            with open(report_path, "w") as f:
                f.write("=" * 70 + "\n")
                f.write("OULAD EXTENDED EXPLORATORY DATA ANALYSIS REPORT\n")
                f.write("=" * 70 + "\n\n")

                f.write(f"Dataset Size: {len(self.df):,} records\n")
                f.write(f"Number of Features: {len(self.df.columns)}\n")
                f.write(f"Numeric Columns: {len(self.df.select_dtypes(include=['number']).columns)}\n")
                f.write(f"Categorical Columns: {len(self.df.select_dtypes(include=['object']).columns)}\n\n")

                f.write("Key Findings:\n")
                f.write("-" * 70 + "\n")
                f.write("1. Correlation Analysis completed\n")
                f.write("2. ANOVA tests for group differences performed\n")
                f.write("3. Distribution analysis for all numeric variables\n")
                f.write("4. Gaussian fit analysis for normality assessment\n")
                f.write("5. Descriptive statistics calculated\n\n")

                f.write("Output Files Generated:\n")
                f.write("-" * 70 + "\n")
                f.write("✓ correlation_matrix.csv - Pearson correlations\n")
                f.write("✓ correlation_tests.csv - Significance tests\n")
                f.write("✓ anova_results.csv - ANOVA test results\n")
                f.write("✓ summary_statistics.csv - Descriptive statistics\n")
                f.write("✓ distributions_univariate.png - Distribution plots\n")
                f.write("✓ gaussian_distributions.png - Normal distribution fits\n")
                f.write("✓ correlation_matrix.png - Correlation heatmap\n")
                f.write("✓ boxplots.png - Box plots by groups\n")
                f.write("✓ scatter_matrix.png - Pairwise scatter plots\n")
                f.write("✓ categorical_distributions.png - Category frequencies\n")
                f.write("✓ missing_data_heatmap.png - Missing data patterns\n\n")

                f.write("=" * 70 + "\n")

            logger.info(f"✓ EDA report saved to {report_path}")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to generate report: {e}")
            return False

    def step_6_generate_apa_paper(self) -> bool:
        """Step 6: Generate scientific paper in APA 7 format."""
        logger.info("=" * 70)
        logger.info("STEP 6: Generate APA Scientific Paper")
        logger.info("=" * 70)

        try:
            docs_dir = Path(__file__).parent / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            output_file = docs_dir / "Articulo_Cientifico_OULAD_APA7.docx"

            generate_apa_paper(output_file)

            logger.info(f"✓ Scientific paper generated: {output_file}")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to generate APA paper: {e}")
            return False

    def run_complete_pipeline(self, skip_postgres: bool = False) -> bool:
        """
        Run complete ETL pipeline.

        Args:
            skip_postgres: Skip PostgreSQL operations (for testing)

        Returns:
            bool: True if all steps succeeded
        """
        logger.info("\n")
        logger.info("╔" + "=" * 68 + "╗")
        logger.info("║" + " " * 68 + "║")
        logger.info("║" + "  OULAD ETL PIPELINE - PRACTICAL CASE 2".center(68) + "║")
        logger.info("║" + "  Data Loading → Database → EDA → Scientific Paper".center(68) + "║")
        logger.info("║" + " " * 68 + "║")
        logger.info("╚" + "=" * 68 + "╝")

        steps = [
            ("Step 1", self.step_1_download_and_load_data),
        ]

        if not skip_postgres:
            steps.extend(
                [
                    ("Step 2", self.step_2_init_postgres_database),
                    ("Step 3", self.step_3_load_data_to_postgres),
                ]
            )

        steps.extend(
            [
                ("Step 4", self.step_4_extended_eda),
                ("Step 5", self.step_5_generate_report),
                ("Step 6", self.step_6_generate_apa_paper),
            ]
        )

        results = {}
        for step_name, step_func in steps:
            try:
                success = step_func()
                results[step_name] = "✓ PASSED" if success else "✗ FAILED"

                if not success:
                    logger.error(f"{step_name} failed. Stopping pipeline.")
                    return False

            except Exception as e:
                logger.error(f"Unexpected error in {step_name}: {e}")
                results[step_name] = "✗ ERROR"
                return False

        # Summary
        logger.info("\n")
        logger.info("=" * 70)
        logger.info("PIPELINE SUMMARY")
        logger.info("=" * 70)
        for step, result in results.items():
            logger.info(f"{step}: {result}")

        logger.info("=" * 70)
        logger.info("✓ ETL PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info(f"Output directory: {self.output_dir}")
        return True


def main():
    """Main entry point."""
    root = Path(__file__).resolve().parent

    # Parse command line arguments
    skip_postgres = "--skip-postgres" in sys.argv

    orchestrator = OULADETLOrchestrator(
        root=root,
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="oulad_uasd",
        postgres_user="postgres",
        postgres_password="",  # Change as needed
    )

    # Run pipeline (skip_postgres=True to test without database)
    success = orchestrator.run_complete_pipeline(skip_postgres=skip_postgres)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

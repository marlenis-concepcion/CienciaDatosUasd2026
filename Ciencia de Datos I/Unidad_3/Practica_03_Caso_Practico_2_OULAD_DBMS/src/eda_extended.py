"""Extended EDA module with comprehensive visualizations for OULAD analysis."""

import logging
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 10


class ExtendedEDA:
    """Comprehensive exploratory data analysis with multiple visualization types."""

    def __init__(self, df: pd.DataFrame, output_dir: Path):
        """
        Initialize EDA.

        Args:
            df: DataFrame to analyze
            output_dir: Directory to save visualizations
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    def generate_summary_statistics(self) -> pd.DataFrame:
        """Generate comprehensive summary statistics."""
        summary = pd.DataFrame(
            {
                "dtype": self.df.dtypes,
                "non_null": self.df.count(),
                "null_count": self.df.isnull().sum(),
                "null_pct": (self.df.isnull().sum() / len(self.df) * 100).round(2),
                "unique_values": self.df.nunique(),
            }
        )

        for col in self.numeric_cols:
            summary.loc[col, "mean"] = self.df[col].mean()
            summary.loc[col, "std"] = self.df[col].std()
            summary.loc[col, "min"] = self.df[col].min()
            summary.loc[col, "max"] = self.df[col].max()
            summary.loc[col, "median"] = self.df[col].median()
            summary.loc[col, "skew"] = self.df[col].skew()
            summary.loc[col, "kurtosis"] = self.df[col].kurtosis()

        summary.to_csv(self.output_dir / "summary_statistics.csv")
        return summary

    def plot_distribution_univariate(self) -> None:
        """Plot univariate distributions for all numeric columns."""
        n_cols = min(len(self.numeric_cols), 20)
        n_rows = (n_cols + 2) // 3

        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 4 * n_rows))
        axes = axes.flatten()

        for idx, col in enumerate(self.numeric_cols[:n_cols]):
            axes[idx].hist(self.df[col].dropna(), bins=30, edgecolor="black", alpha=0.7)
            axes[idx].set_title(f"Distribution: {col}")
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel("Frequency")
            axes[idx].grid(True, alpha=0.3)

        for idx in range(n_cols, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.savefig(self.output_dir / "distributions_univariate.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Univariate distributions saved.")

    def plot_gaussian_bell_curves(self) -> None:
        """Plot Gaussian bell curves (normal distributions) for numeric columns."""
        n_cols = min(len(self.numeric_cols), 12)
        n_rows = (n_cols + 2) // 3

        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 4 * n_rows))
        axes = axes.flatten()

        for idx, col in enumerate(self.numeric_cols[:n_cols]):
            data = self.df[col].dropna()
            mu, sigma = data.mean(), data.std()

            # Histogram
            axes[idx].hist(data, bins=30, density=True, alpha=0.7, edgecolor="black", label="Data")

            # Gaussian fit
            x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
            axes[idx].plot(x, stats.norm.pdf(x, mu, sigma), "r-", linewidth=2, label="Gaussian fit")

            axes[idx].set_title(f"Gaussian Distribution: {col}\nμ={mu:.2f}, σ={sigma:.2f}")
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel("Density")
            axes[idx].legend()
            axes[idx].grid(True, alpha=0.3)

        for idx in range(n_cols, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.savefig(self.output_dir / "gaussian_distributions.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Gaussian distributions saved.")

    def plot_boxplots(self) -> None:
        """Plot boxplots for numeric columns grouped by categorical variables."""
        if not self.categorical_cols:
            logger.warning("No categorical columns for boxplot grouping.")
            return

        n_categorical = min(len(self.categorical_cols), 4)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for idx, cat_col in enumerate(self.categorical_cols[:n_categorical]):
            if idx < len(axes):
                # Select first numeric column for visualization
                numeric_col = self.numeric_cols[0] if self.numeric_cols else None
                if numeric_col:
                    sns.boxplot(data=self.df, x=cat_col, y=numeric_col, ax=axes[idx])
                    axes[idx].set_title(f"Boxplot: {numeric_col} by {cat_col}")
                    axes[idx].tick_params(axis="x", rotation=45)

        for idx in range(n_categorical, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.savefig(self.output_dir / "boxplots.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Boxplots saved.")

    def plot_correlation_matrix(self) -> pd.DataFrame:
        """Plot correlation matrix heatmap."""
        if len(self.numeric_cols) < 2:
            logger.warning("Not enough numeric columns for correlation analysis.")
            return pd.DataFrame()

        corr_matrix = self.df[self.numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            ax=ax,
            cbar_kws={"label": "Correlation Coefficient"},
            vmin=-1,
            vmax=1,
        )
        ax.set_title("Correlation Matrix Heatmap", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(self.output_dir / "correlation_matrix.png", dpi=300, bbox_inches="tight")
        plt.close()

        corr_matrix.to_csv(self.output_dir / "correlation_matrix.csv")
        logger.info("Correlation matrix saved.")
        return corr_matrix

    def plot_scatter_matrix(self, sample_size: int = 1000) -> None:
        """Plot scatter matrix for numeric columns."""
        if len(self.numeric_cols) < 2:
            logger.warning("Not enough numeric columns for scatter matrix.")
            return

        # Sample if dataframe is too large
        if len(self.df) > sample_size:
            plot_df = self.df.sample(n=sample_size, random_state=42)
        else:
            plot_df = self.df

        try:
            from pandas.plotting import scatter_matrix

            fig = scatter_matrix(
                plot_df[self.numeric_cols[:5]],
                figsize=(12, 10),
                diagonal="hist",
                alpha=0.5,
                s=30,
            )
            plt.suptitle("Scatter Matrix of Numeric Variables", fontsize=14, fontweight="bold", y=1.001)
            plt.tight_layout()
            plt.savefig(self.output_dir / "scatter_matrix.png", dpi=300, bbox_inches="tight")
            plt.close()
            logger.info("Scatter matrix saved.")
        except Exception as e:
            logger.warning(f"Could not create scatter matrix: {e}")

    def plot_confusion_matrices(self, y_true: pd.Series, y_pred_dict: dict) -> None:
        """
        Plot confusion matrices for binary classification.

        Args:
            y_true: True labels
            y_pred_dict: Dictionary of {model_name: predictions}
        """
        n_models = len(y_pred_dict)
        fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4))

        if n_models == 1:
            axes = [axes]

        for idx, (model_name, y_pred) in enumerate(y_pred_dict.items()):
            cm = confusion_matrix(y_true, y_pred)
            disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negative", "Positive"])
            disp.plot(ax=axes[idx], cmap="Blues", values_format="d")
            axes[idx].set_title(f"Confusion Matrix: {model_name}")

            # Add metrics
            tn, fp, fn, tp = cm.ravel()
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            metrics_text = f"Acc: {accuracy:.3f}\nPrec: {precision:.3f}\nRec: {recall:.3f}\nF1: {f1:.3f}"
            axes[idx].text(
                0.5, -0.25, metrics_text, transform=axes[idx].transAxes, ha="center", fontsize=10
            )

        plt.tight_layout()
        plt.savefig(self.output_dir / "confusion_matrices.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Confusion matrices saved.")

    def plot_categorical_distributions(self) -> None:
        """Plot distributions for categorical variables."""
        if not self.categorical_cols:
            logger.warning("No categorical columns to plot.")
            return

        n_cols = min(len(self.categorical_cols), 8)
        n_rows = (n_cols + 1) // 2

        fig, axes = plt.subplots(n_rows, 2, figsize=(14, 4 * n_rows))
        axes = axes.flatten()

        for idx, col in enumerate(self.categorical_cols[:n_cols]):
            value_counts = self.df[col].value_counts().head(10)
            axes[idx].bar(range(len(value_counts)), value_counts.values, color="steelblue", edgecolor="black")
            axes[idx].set_xticks(range(len(value_counts)))
            axes[idx].set_xticklabels(value_counts.index, rotation=45, ha="right")
            axes[idx].set_title(f"Distribution: {col}")
            axes[idx].set_ylabel("Count")
            axes[idx].grid(True, alpha=0.3, axis="y")

        for idx in range(n_cols, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.savefig(self.output_dir / "categorical_distributions.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Categorical distributions saved.")

    def plot_missing_data_heatmap(self) -> None:
        """Plot heatmap of missing data patterns."""
        missing_data = self.df.isnull()

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            missing_data.iloc[:100],  # Show first 100 rows
            cbar=True,
            yticklabels=False,
            ax=ax,
            cmap="YlOrRd",
        )
        ax.set_title("Missing Data Heatmap (First 100 Rows)", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(self.output_dir / "missing_data_heatmap.png", dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Missing data heatmap saved.")

    def perform_anova_tests(self) -> pd.DataFrame:
        """Perform ANOVA tests for numeric variables by group."""
        results = []

        if not self.categorical_cols or not self.numeric_cols:
            logger.warning("Not enough columns for ANOVA testing.")
            return pd.DataFrame()

        for cat_col in self.categorical_cols[:3]:  # Test first 3 categorical vars
            for num_col in self.numeric_cols[:5]:  # Test first 5 numeric vars
                groups = [group[num_col].dropna() for name, group in self.df.groupby(cat_col)]

                if len(groups) > 1:
                    f_stat, p_value = stats.f_oneway(*groups)
                    results.append(
                        {
                            "Categorical": cat_col,
                            "Numeric": num_col,
                            "F-Statistic": f_stat,
                            "P-Value": p_value,
                            "Significant": "Yes" if p_value < 0.05 else "No",
                        }
                    )

        results_df = pd.DataFrame(results)
        if not results_df.empty:
            results_df.to_csv(self.output_dir / "anova_results.csv", index=False)
            logger.info("ANOVA tests completed.")

        return results_df

    def perform_correlation_tests(self) -> pd.DataFrame:
        """Perform correlation significance tests."""
        if len(self.numeric_cols) < 2:
            logger.warning("Not enough numeric columns for correlation tests.")
            return pd.DataFrame()

        results = []
        corr_matrix = self.df[self.numeric_cols].corr()

        for i, col1 in enumerate(self.numeric_cols):
            for col2 in self.numeric_cols[i + 1 :]:
                correlation = corr_matrix.loc[col1, col2]
                # Pearson correlation test - align both series
                valid_idx = self.df[[col1, col2]].dropna().index
                col1_data = self.df.loc[valid_idx, col1]
                col2_data = self.df.loc[valid_idx, col2]

                if len(col1_data) > 2:  # Need at least 3 points for correlation
                    try:
                        r, p_value = stats.pearsonr(col1_data, col2_data)
                        results.append(
                            {
                                "Variable1": col1,
                                "Variable2": col2,
                                "Correlation": correlation,
                                "P-Value": p_value,
                                "Significant": "Yes" if p_value < 0.05 else "No",
                            }
                        )
                    except Exception as e:
                        logger.debug(f"Skipping correlation {col1}-{col2}: {e}")
                        continue

        results_df = pd.DataFrame(results).sort_values("Correlation", key=abs, ascending=False)
        if not results_df.empty:
            results_df.to_csv(self.output_dir / "correlation_tests.csv", index=False)
            logger.info("Correlation tests completed.")

        return results_df

    def calculate_descriptive_statistics(self) -> dict:
        """Calculate extended descriptive statistics."""
        stats_dict = {}

        for col in self.numeric_cols:
            data = self.df[col].dropna()
            stats_dict[col] = {
                "count": len(data),
                "mean": data.mean(),
                "median": data.median(),
                "mode": data.mode().values[0] if not data.mode().empty else None,
                "std": data.std(),
                "variance": data.var(),
                "min": data.min(),
                "q1": data.quantile(0.25),
                "q3": data.quantile(0.75),
                "max": data.max(),
                "range": data.max() - data.min(),
                "iqr": data.quantile(0.75) - data.quantile(0.25),
                "skewness": data.skew(),
                "kurtosis": data.kurtosis(),
                "cv": data.std() / data.mean() if data.mean() != 0 else np.nan,
            }

        stats_df = pd.DataFrame(stats_dict).T
        stats_df.to_csv(self.output_dir / "descriptive_statistics.csv")
        logger.info("Descriptive statistics calculated.")

        return stats_dict

    def run_all_eda(self, y_true: Optional[pd.Series] = None, y_pred_dict: Optional[dict] = None) -> dict:
        """
        Run all EDA analyses and generate visualizations.

        Args:
            y_true: Optional true labels for confusion matrices
            y_pred_dict: Optional dictionary of predictions for each model

        Returns:
            Dictionary with all analysis results
        """
        logger.info("Starting extended EDA analysis...")

        results = {
            "summary_statistics": self.generate_summary_statistics(),
            "descriptive_statistics": self.calculate_descriptive_statistics(),
            "correlation_matrix": self.plot_correlation_matrix(),
            "correlation_tests": self.perform_correlation_tests(),
            "anova_results": self.perform_anova_tests(),
        }

        self.plot_distribution_univariate()
        self.plot_gaussian_bell_curves()
        self.plot_boxplots()
        self.plot_categorical_distributions()
        self.plot_scatter_matrix()
        self.plot_missing_data_heatmap()

        if y_true is not None and y_pred_dict is not None:
            self.plot_confusion_matrices(y_true, y_pred_dict)

        logger.info("Extended EDA analysis completed.")
        return results

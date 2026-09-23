from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


class EDAReporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        sns.set_theme(style="whitegrid")

    def run(self, data: pd.DataFrame) -> dict[str, float]:
        numeric = [
            "clicks_28d",
            "dias_activos_28d",
            "studied_credits",
            "num_of_prev_attempts",
            "promedio_evaluaciones",
        ]
        description = data[numeric].describe().T
        description["skewness"] = data[numeric].skew()
        description["kurtosis"] = data[numeric].kurtosis()
        description.to_csv(self.output_dir / "descriptiva_univariada.csv")
        data.isna().sum().rename("faltantes").to_csv(
            self.output_dir / "auditoria_missing.csv"
        )

        self._plots(data)
        pass_clicks = data.loc[data["aprobo"] == 1, "clicks_28d"]
        no_pass_clicks = data.loc[data["aprobo"] == 0, "clicks_28d"]
        test = stats.mannwhitneyu(pass_clicks, no_pass_clicks, alternative="two-sided")
        effect_r = (2 * test.statistic) / (len(pass_clicks) * len(no_pass_clicks)) - 1
        return {
            "mann_whitney_u": float(test.statistic),
            "p_value": float(test.pvalue),
            "rank_biserial_r": float(effect_r),
            "media_clicks_aprueba": float(pass_clicks.mean()),
            "media_clicks_no_aprueba": float(no_pass_clicks.mean()),
        }

    def _plots(self, data: pd.DataFrame) -> None:
        sample = data.sample(min(len(data), 6000), random_state=8237)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.histplot(data=sample, x="clicks_28d", hue="aprobo", bins=40, ax=axes[0, 0])
        axes[0, 0].set_title("Distribución de clics tempranos")
        sns.boxplot(data=sample, x="final_result", y="clicks_28d", ax=axes[0, 1])
        axes[0, 1].set_title("Box plot por resultado final")
        sns.scatterplot(
            data=sample,
            x="clicks_28d",
            y="promedio_evaluaciones",
            hue="aprobo",
            alpha=0.45,
            ax=axes[1, 0],
        )
        axes[1, 0].set_title("Dispersión: clics y promedio")
        corr = sample[
            ["clicks_28d", "dias_activos_28d", "studied_credits",
             "num_of_prev_attempts", "promedio_evaluaciones", "aprobo"]
        ].corr(method="spearman")
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=axes[1, 1])
        axes[1, 1].set_title("Correlación de Spearman")
        plt.tight_layout()
        plt.savefig(self.output_dir / "eda_alto_nivel.png", dpi=180, bbox_inches="tight")
        plt.close()

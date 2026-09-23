import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Practica_Unidad_4_Metricas_Inferenciales_ML.ipynb"


def markdown(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


cells = [
    markdown(
        """
        # Ensayo experimental con métricas descriptivas, inferenciales y aprendizaje automático

        **Universidad Autónoma de Santo Domingo (UASD)**  
        **Asignatura:** Ciencia de Datos I (INF-8237-C2)  
        **Unidad:** Unidad 4: Introducción a Machine Learning (ML)  
        **Participante:** Marlenis Judith Concepción Cuevas  
        **Actividad:** Recuperación de puntos  
        **Fecha:** ____________________

        > **Propósito.** Realizar un análisis exploratorio de datos (EDA), aplicar pruebas de
        > hipótesis y comparar técnicas estadísticas con modelos básicos de aprendizaje
        > automático. Los datos utilizados son sintéticos y reproducibles; no corresponden a
        > estudiantes reales.
        """
    ),
    markdown(
        """
        ## Resumen

        Esta práctica integra estadística descriptiva, estadística inferencial y aprendizaje
        automático sobre un conjunto sintético de desempeño académico. Se examinan la
        distribución y calidad de los datos, la relación entre horas de estudio y calificación,
        diferencias entre grupos y asociaciones entre variables categóricas. Para ello se
        aplican las correlaciones de Pearson y Spearman, una prueba *t* de muestras
        independientes, ANOVA de una vía y chi-cuadrado. Además, se ajustan una regresión
        lineal, una máquina de vectores de soporte (SVM) y una red neuronal artificial (ANN)
        básica. La interpretación distingue entre significancia estadística, magnitud del
        efecto y capacidad predictiva. El flujo usa una semilla fija para facilitar su
        reproducción en Google Colab.

        **Palabras clave:** análisis exploratorio, inferencia estadística, correlación,
        regresión, aprendizaje automático
        """
    ),
    markdown(
        """
        ## 1. Reflexión sobre estadística inferencial y aprendizaje automático

        La estadística inferencial y el aprendizaje automático pueden trabajar con los mismos
        datos, pero responden preguntas diferentes. La inferencia busca estimar, contrastar y
        explicar relaciones en una población a partir de una muestra. Por eso presta atención a
        hipótesis, supuestos, intervalos de confianza, valores *p* y tamaños del efecto. El
        aprendizaje automático se concentra principalmente en aprender patrones que generalicen
        a observaciones nuevas. James et al. (2021) destacan la importancia de evaluar ese
        desempeño con observaciones no utilizadas para ajustar el modelo. Por ello se emplean
        métricas como MAE, R², exactitud, precisión, exhaustividad y F1.

        No existe una oposición absoluta entre ambos enfoques. La inferencia permite responder
        si la evidencia apoya una relación y cuán grande podría ser; ML permite comprobar si esa
        información tiene utilidad predictiva fuera de la muestra de entrenamiento. Una
        asociación estadísticamente significativa no garantiza una predicción útil y una buena
        predicción no demuestra causalidad (Field, 2018).
        """
    ),
    markdown(
        """
        ## 2. Respuestas sobre el video de correlaciones

        1. **¿Qué mide una correlación?** Mide la dirección y la intensidad de la asociación
           entre dos variables. No demuestra que una variable cause la otra.
        2. **¿Qué indica el signo?** Un coeficiente positivo indica que las variables tienden a
           moverse en el mismo sentido; uno negativo indica que tienden a moverse en sentidos
           opuestos.
        3. **¿Qué indica la magnitud?** Cuanto más se aproxima el valor absoluto del coeficiente
           a 1, más intensa es la asociación. Los puntos de corte son orientativos y deben
           interpretarse según el contexto. El material señala que “entre más cercano sea el
           valor al valor absoluto de uno [...] más fuerte es la correlación” (Material
           audiovisual sobre correlaciones, s.f., 4:11).
        4. **¿Cuándo se usa Pearson?** Para evaluar asociación lineal entre variables
           cuantitativas cuando sus supuestos resultan razonables y no dominan valores atípicos
           influyentes.
        5. **¿Cuándo se usa Spearman?** Para variables al menos ordinales o cuando interesa una
           relación monotónica, especialmente si la normalidad o linealidad no es adecuada.
        6. **¿Qué significa p < .05?** Bajo la hipótesis nula y los supuestos de la prueba, el
           resultado observado sería poco compatible con ausencia de asociación. No representa
           la probabilidad de que la hipótesis nula sea verdadera.
        7. **Interpretación de ρ = .64, p = .07.** La asociación observada es positiva y de
           magnitud moderada a alta, pero no alcanza significancia con α = .05.
        8. **Interpretación de r = .92, p = .04.** La asociación observada es positiva, muy
           fuerte y estadísticamente significativa con α = .05.

        **Observación crítica.** El video ofrece reglas introductorias útiles, aunque elegir
        Pearson o Spearman no depende únicamente de que la muestra sea mayor o menor que 30.
        También deben examinarse el nivel de medición, la forma de la relación, la distribución,
        los valores atípicos, la independencia y el objetivo analítico.
        """
    ),
    markdown(
        """
        ## 3. Preparación del entorno

        Las bibliotecas utilizadas vienen instaladas normalmente en Google Colab. Al ejecutar
        el cuaderno se crea la carpeta `evidencias_unidad4`, donde se guardan las figuras y las
        tablas principales.
        """
    ),
    code(
        """
        import warnings
        from pathlib import Path

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
        from scipy import stats
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import (
            ConfusionMatrixDisplay,
            accuracy_score,
            classification_report,
            mean_absolute_error,
            r2_score,
        )
        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.svm import SVC

        warnings.filterwarnings("ignore")
        sns.set_theme(style="whitegrid", palette="deep")
        RANDOM_STATE = 8237
        EVIDENCIAS = Path("evidencias_unidad4")
        EVIDENCIAS.mkdir(exist_ok=True)
        print("Entorno preparado. Evidencias:", EVIDENCIAS.resolve())
        """
    ),
    markdown(
        """
        ## 4. Datos y preguntas de investigación

        Se simulan 240 observaciones con variables de hábitos de estudio, asistencia,
        motivación, método de enseñanza y desempeño.

        - **H1 (correlación):** las horas de estudio se asocian positivamente con la calificación.
        - **H2 (t-test):** la calificación media difiere entre estudiantes con y sin tutoría.
        - **H3 (ANOVA):** la calificación media difiere entre métodos de enseñanza.
        - **H4 (chi-cuadrado):** aprobar y poseer motivación alta no son independientes.
        - **ML:** las características observadas permiten predecir calificación y aprobación.
        """
    ),
    code(
        """
        rng = np.random.default_rng(RANDOM_STATE)
        n = 240

        horas_estudio = np.clip(rng.normal(8, 3, n), 1, 18)
        asistencia = np.clip(rng.normal(82, 10, n), 45, 100)
        motivacion = np.clip(np.rint(rng.normal(3.2, 1.0, n)), 1, 5).astype(int)
        tutoria = rng.choice(["Sí", "No"], n, p=[0.42, 0.58])
        metodo = rng.choice(["Tradicional", "Híbrido", "Interactivo"], n, p=[0.34, 0.33, 0.33])
        dispositivo = rng.choice(["Computadora", "Tableta", "Teléfono"], n, p=[0.58, 0.14, 0.28])

        efecto_tutoria = np.where(tutoria == "Sí", 3.0, 0.0)
        efecto_metodo = pd.Series(metodo).map(
            {"Tradicional": 0.0, "Híbrido": 2.0, "Interactivo": 4.5}
        ).to_numpy()
        ruido = rng.normal(0, 5.5, n)
        calificacion = np.clip(
            20 + 2.7 * horas_estudio + 0.28 * asistencia + 2.2 * motivacion
            + efecto_tutoria + efecto_metodo + ruido,
            0,
            100,
        )

        df = pd.DataFrame({
            "horas_estudio": horas_estudio.round(1),
            "asistencia": asistencia.round(1),
            "motivacion": motivacion,
            "tutoria": tutoria,
            "metodo": metodo,
            "dispositivo": dispositivo,
            "calificacion": calificacion.round(1),
        })
        df["aprobo"] = np.where(df["calificacion"] >= 70, "Sí", "No")
        df["motivacion_alta"] = np.where(df["motivacion"] >= 4, "Sí", "No")

        # Se agregan pocos faltantes para documentar su tratamiento en el EDA.
        for columna in ["horas_estudio", "asistencia"]:
            indices = rng.choice(df.index, size=4, replace=False)
            df.loc[indices, columna] = np.nan

        df.head()
        """
    ),
    markdown(
        """
        ## 5. Análisis exploratorio de datos (EDA)

        El EDA comprueba dimensiones, tipos de variables, datos faltantes, medidas descriptivas,
        distribuciones, valores atípicos y relaciones preliminares. Los faltantes numéricos se
        imputan con la mediana, una decisión robusta y fácil de reproducir para este ejercicio.
        """
    ),
    code(
        """
        print("Dimensiones:", df.shape)
        display(pd.DataFrame({"tipo": df.dtypes, "faltantes": df.isna().sum()}))
        display(df.describe(include="all").T)

        df_limpio = df.copy()
        for columna in ["horas_estudio", "asistencia"]:
            df_limpio[columna] = df_limpio[columna].fillna(df_limpio[columna].median())

        print("Duplicados:", df_limpio.duplicated().sum())
        print("Faltantes después de imputar:", int(df_limpio.isna().sum().sum()))
        df_limpio.to_csv(EVIDENCIAS / "datos_sinteticos_limpios.csv", index=False)
        """
    ),
    code(
        """
        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        sns.histplot(df_limpio["calificacion"], kde=True, ax=axes[0, 0])
        axes[0, 0].set_title("Distribución de calificaciones")
        sns.scatterplot(
            data=df_limpio, x="horas_estudio", y="calificacion",
            hue="aprobo", ax=axes[0, 1]
        )
        axes[0, 1].set_title("Horas de estudio y calificación")
        sns.boxplot(data=df_limpio, x="metodo", y="calificacion", ax=axes[1, 0])
        axes[1, 0].set_title("Calificación por método")
        sns.countplot(data=df_limpio, x="aprobo", hue="motivacion_alta", ax=axes[1, 1])
        axes[1, 1].set_title("Aprobación y motivación alta")
        plt.tight_layout()
        plt.savefig(EVIDENCIAS / "figura_1_eda.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    code(
        """
        numericas = ["horas_estudio", "asistencia", "motivacion", "calificacion"]
        matriz = df_limpio[numericas].corr(method="pearson")
        plt.figure(figsize=(7, 5))
        sns.heatmap(matriz, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Matriz de correlaciones de Pearson")
        plt.tight_layout()
        plt.savefig(EVIDENCIAS / "figura_2_correlaciones.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    markdown(
        """
        ## 6. Pruebas inferenciales

        Se utiliza un nivel de significancia α = .05. Además del valor *p*, se informa una
        medida de magnitud cuando corresponde. Una decisión estadística se redacta como
        “rechazar” o “no rechazar” H0; no se afirma que H0 haya sido probada como verdadera.
        """
    ),
    code(
        """
        alpha = 0.05

        shapiro_horas = stats.shapiro(df_limpio["horas_estudio"])
        shapiro_nota = stats.shapiro(df_limpio["calificacion"])
        pearson = stats.pearsonr(df_limpio["horas_estudio"], df_limpio["calificacion"])
        spearman = stats.spearmanr(df_limpio["horas_estudio"], df_limpio["calificacion"])

        resultados_correlacion = pd.DataFrame({
            "Análisis": [
                "Shapiro: horas de estudio",
                "Shapiro: calificación",
                "Correlación de Pearson",
                "Correlación de Spearman",
            ],
            "Estadístico": [
                shapiro_horas.statistic,
                shapiro_nota.statistic,
                pearson.statistic,
                spearman.statistic,
            ],
            "p": [
                shapiro_horas.pvalue,
                shapiro_nota.pvalue,
                pearson.pvalue,
                spearman.pvalue,
            ],
        })
        display(resultados_correlacion.round(4))
        print(
            f"Pearson: r = {pearson.statistic:.3f}, p = {pearson.pvalue:.4g}. "
            + ("Se rechaza H0." if pearson.pvalue < alpha else "No se rechaza H0.")
        )
        print(
            f"Spearman: ρ = {spearman.statistic:.3f}, p = {spearman.pvalue:.4g}. "
            + ("Se rechaza H0." if spearman.pvalue < alpha else "No se rechaza H0.")
        )
        """
    ),
    code(
        """
        con_tutoria = df_limpio.loc[df_limpio["tutoria"] == "Sí", "calificacion"]
        sin_tutoria = df_limpio.loc[df_limpio["tutoria"] == "No", "calificacion"]
        t_result = stats.ttest_ind(con_tutoria, sin_tutoria, equal_var=False)

        diferencia = con_tutoria.mean() - sin_tutoria.mean()
        var_pooled = (
            ((len(con_tutoria) - 1) * con_tutoria.var(ddof=1)
             + (len(sin_tutoria) - 1) * sin_tutoria.var(ddof=1))
            / (len(con_tutoria) + len(sin_tutoria) - 2)
        )
        cohen_d = diferencia / np.sqrt(var_pooled)

        display(pd.DataFrame({
            "Grupo": ["Con tutoría", "Sin tutoría"],
            "n": [len(con_tutoria), len(sin_tutoria)],
            "Media": [con_tutoria.mean(), sin_tutoria.mean()],
            "DE": [con_tutoria.std(ddof=1), sin_tutoria.std(ddof=1)],
        }).round(2))
        print(f"Welch t = {t_result.statistic:.3f}, p = {t_result.pvalue:.4g}, d = {cohen_d:.3f}")
        print("Decisión:", "Se rechaza H0." if t_result.pvalue < alpha else "No se rechaza H0.")
        """
    ),
    code(
        """
        grupos_metodo = [
            grupo["calificacion"].to_numpy()
            for _, grupo in df_limpio.groupby("metodo")
        ]
        anova = stats.f_oneway(*grupos_metodo)

        media_general = df_limpio["calificacion"].mean()
        ss_entre = sum(
            len(grupo) * (grupo["calificacion"].mean() - media_general) ** 2
            for _, grupo in df_limpio.groupby("metodo")
        )
        ss_total = ((df_limpio["calificacion"] - media_general) ** 2).sum()
        eta_cuadrado = ss_entre / ss_total

        display(
            df_limpio.groupby("metodo")["calificacion"]
            .agg(["count", "mean", "std"]).round(2)
        )
        print(
            f"ANOVA: F = {anova.statistic:.3f}, p = {anova.pvalue:.4g}, "
            f"η² = {eta_cuadrado:.3f}"
        )
        print("Decisión:", "Se rechaza H0." if anova.pvalue < alpha else "No se rechaza H0.")

        if anova.pvalue < alpha:
            print("\\nComparaciones exploratorias de Welch con ajuste Bonferroni:")
            metodos = sorted(df_limpio["metodo"].unique())
            comparaciones = []
            for i, metodo_a in enumerate(metodos):
                for metodo_b in metodos[i + 1:]:
                    a = df_limpio.loc[df_limpio["metodo"] == metodo_a, "calificacion"]
                    b = df_limpio.loc[df_limpio["metodo"] == metodo_b, "calificacion"]
                    prueba = stats.ttest_ind(a, b, equal_var=False)
                    comparaciones.append({
                        "Comparación": f"{metodo_a} vs. {metodo_b}",
                        "p original": prueba.pvalue,
                        "p Bonferroni": min(prueba.pvalue * 3, 1.0),
                    })
            display(pd.DataFrame(comparaciones).round(4))
        """
    ),
    code(
        """
        contingencia = pd.crosstab(df_limpio["motivacion_alta"], df_limpio["aprobo"])
        chi2, p_chi, gl, esperadas = stats.chi2_contingency(contingencia)
        n_total = contingencia.to_numpy().sum()
        v_cramer = np.sqrt(
            chi2 / (n_total * min(contingencia.shape[0] - 1, contingencia.shape[1] - 1))
        )

        display(contingencia)
        display(pd.DataFrame(
            esperadas, index=contingencia.index, columns=contingencia.columns
        ).round(2).rename_axis("Frecuencias esperadas"))
        print(f"χ²({gl}) = {chi2:.3f}, p = {p_chi:.4g}, V de Cramér = {v_cramer:.3f}")
        print("Decisión:", "Se rechaza H0." if p_chi < alpha else "No se rechaza H0.")
        """
    ),
    markdown(
        """
        ## 7. Regresión lineal

        La regresión estima una variable cuantitativa. Se separa 25 % de los datos para prueba,
        evitando evaluar el modelo con las mismas observaciones usadas para ajustarlo. La MAE
        expresa el error medio en puntos de calificación y R² resume la proporción de variación
        explicada en el conjunto de prueba.
        """
    ),
    code(
        """
        features_reg = ["horas_estudio", "asistencia", "motivacion", "tutoria", "metodo"]
        X_reg = df_limpio[features_reg]
        y_reg = df_limpio["calificacion"]
        X_train, X_test, y_train, y_test = train_test_split(
            X_reg, y_reg, test_size=0.25, random_state=RANDOM_STATE
        )

        numericas_reg = ["horas_estudio", "asistencia", "motivacion"]
        categoricas_reg = ["tutoria", "metodo"]
        preprocesador_reg = ColumnTransformer([
            ("num", StandardScaler(), numericas_reg),
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categoricas_reg),
        ])
        modelo_reg = Pipeline([
            ("preprocesamiento", preprocesador_reg),
            ("modelo", LinearRegression()),
        ])
        modelo_reg.fit(X_train, y_train)
        pred_reg = modelo_reg.predict(X_test)

        mae = mean_absolute_error(y_test, pred_reg)
        r2 = r2_score(y_test, pred_reg)
        print(f"MAE de prueba: {mae:.2f} puntos")
        print(f"R² de prueba: {r2:.3f}")

        plt.figure(figsize=(6, 5))
        sns.scatterplot(x=y_test, y=pred_reg)
        limites = [min(y_test.min(), pred_reg.min()), max(y_test.max(), pred_reg.max())]
        plt.plot(limites, limites, "--", color="black")
        plt.xlabel("Calificación real")
        plt.ylabel("Calificación predicha")
        plt.title("Regresión lineal: valores reales y predichos")
        plt.tight_layout()
        plt.savefig(EVIDENCIAS / "figura_3_regresion.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    markdown(
        """
        ## 8. Clasificación con SVM y ANN básica

        Se predice si el estudiante aprueba. La división se estratifica para conservar la
        proporción de clases. El escalamiento se aprende únicamente con entrenamiento mediante
        un `Pipeline`, lo cual reduce el riesgo de fuga de información. Se comparan SVM con
        kernel RBF y un perceptrón multicapa (MLP), utilizado aquí como ANN básica.
        """
    ),
    code(
        """
        features_clf = [
            "horas_estudio", "asistencia", "motivacion",
            "tutoria", "metodo", "dispositivo",
        ]
        X_clf = df_limpio[features_clf]
        y_clf = (df_limpio["aprobo"] == "Sí").astype(int)
        X_train, X_test, y_train, y_test = train_test_split(
            X_clf,
            y_clf,
            test_size=0.25,
            random_state=RANDOM_STATE,
            stratify=y_clf,
        )

        numericas_clf = ["horas_estudio", "asistencia", "motivacion"]
        categoricas_clf = ["tutoria", "metodo", "dispositivo"]
        preprocesador_clf = ColumnTransformer([
            ("num", StandardScaler(), numericas_clf),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categoricas_clf),
        ])

        modelos = {
            "SVM": SVC(kernel="rbf", C=1.0, gamma="scale", random_state=RANDOM_STATE),
            "ANN básica": MLPClassifier(
                hidden_layer_sizes=(12, 6),
                activation="relu",
                max_iter=1500,
                random_state=RANDOM_STATE,
                early_stopping=True,
            ),
        }

        resumen_modelos = []
        predicciones = {}
        for nombre, estimador in modelos.items():
            pipeline = Pipeline([
                ("preprocesamiento", preprocesador_clf),
                ("modelo", estimador),
            ])
            pipeline.fit(X_train, y_train)
            pred = pipeline.predict(X_test)
            predicciones[nombre] = pred
            reporte = classification_report(y_test, pred, output_dict=True, zero_division=0)
            resumen_modelos.append({
                "Modelo": nombre,
                "Exactitud": accuracy_score(y_test, pred),
                "Precisión (aprueba)": reporte["1"]["precision"],
                "Exhaustividad (aprueba)": reporte["1"]["recall"],
                "F1 (aprueba)": reporte["1"]["f1-score"],
            })

        tabla_modelos = pd.DataFrame(resumen_modelos).set_index("Modelo")
        display(tabla_modelos.round(3))
        tabla_modelos.to_csv(EVIDENCIAS / "tabla_metricas_ml.csv")
        """
    ),
    code(
        """
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for ax, (nombre, pred) in zip(axes, predicciones.items()):
            ConfusionMatrixDisplay.from_predictions(
                y_test, pred, display_labels=["No", "Sí"], cmap="Blues",
                colorbar=False, ax=ax
            )
            ax.set_title(nombre)
        plt.tight_layout()
        plt.savefig(EVIDENCIAS / "figura_4_matrices_confusion.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    markdown(
        """
        ## 9. Conclusiones

        En términos generales, esta práctica muestra que la estadística inferencial y el
        aprendizaje automático se complementan. Las pruebas de hipótesis ayudan a valorar la
        evidencia y la magnitud de las asociaciones, mientras que la evaluación fuera de muestra
        permite estimar la capacidad predictiva. Como los datos son sintéticos y el diseño es
        observacional, los resultados sirven como demostración metodológica y no deben
        generalizarse a estudiantes reales ni interpretarse causalmente.
        """
    ),
    code(
        """
        mejor_modelo = tabla_modelos["F1 (aprueba)"].idxmax()
        mejor_f1 = tabla_modelos.loc[mejor_modelo, "F1 (aprueba)"]

        decision_cor = "se rechazó H0" if pearson.pvalue < alpha else "no se rechazó H0"
        decision_t = "se rechazó H0" if t_result.pvalue < alpha else "no se rechazó H0"
        decision_anova = "se rechazó H0" if anova.pvalue < alpha else "no se rechazó H0"
        decision_chi = "se rechazó H0" if p_chi < alpha else "no se rechazó H0"

        conclusion = f\"\"\"
        RESULTADOS PARA LA CONCLUSIÓN

        1. Correlación de Pearson: r = {pearson.statistic:.3f}, p = {pearson.pvalue:.4g};
           {decision_cor} con α = .05.
        2. Prueba t de Welch: t = {t_result.statistic:.3f}, p = {t_result.pvalue:.4g}
           y d de Cohen = {cohen_d:.3f}; {decision_t}.
        3. ANOVA: F = {anova.statistic:.3f}, p = {anova.pvalue:.4g}
           y η² = {eta_cuadrado:.3f}; {decision_anova}.
        4. Chi-cuadrado: χ²({gl}) = {chi2:.3f}, p = {p_chi:.4g}
           y V de Cramér = {v_cramer:.3f}; {decision_chi}.
        5. Regresión lineal: MAE = {mae:.2f} puntos y R² = {r2:.3f} en prueba.
        6. Mejor clasificador por F1 de la clase “aprueba”: {mejor_modelo},
           con F1 = {mejor_f1:.3f}.
        \"\"\"
        print(conclusion)

        (EVIDENCIAS / "conclusiones_resultados.txt").write_text(
            conclusion.strip(), encoding="utf-8"
        )
        """
    ),
    markdown(
        """
        ## Referencias

        Field, A. (2018). *Discovering statistics using IBM SPSS statistics* (5.ª ed.).
        SAGE Publications.

        James, G., Witten, D., Hastie, T. y Tibshirani, R. (2021). *An introduction to
        statistical learning: With applications in R* (2.ª ed.). Springer.
        https://doi.org/10.1007/978-1-0716-1418-1

        Material audiovisual sobre correlaciones. (s.f.). [Video proporcionado en el aula
        virtual de INF-8237-C2].

        Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O.,
        Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A.,
        Cournapeau, D., Brucher, M., Perrot, M. y Duchesnay, É. (2011). Scikit-learn:
        Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.
        """
    ),
    markdown(
        """
        ## Anexo A

        **Evidencias generadas**

        Al finalizar la ejecución, descargue o conserve junto con el cuaderno la carpeta
        `evidencias_unidad4`, que contiene:

        - Base sintética limpia en CSV.
        - Figura 1: panel del EDA.
        - Figura 2: matriz de correlaciones.
        - Figura 3: evaluación visual de la regresión.
        - Figura 4: matrices de confusión de SVM y ANN.
        - Tabla de métricas de clasificación.

        Para entregar en UASDVirtual, comparta el enlace de Google Colab con permiso
        **“Cualquier persona con el enlace puede ver”** y verifique que las salidas permanezcan
        guardadas en el cuaderno.
        """
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "colab": {
            "name": OUTPUT.name,
            "provenance": [],
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Cuaderno creado: {OUTPUT}")

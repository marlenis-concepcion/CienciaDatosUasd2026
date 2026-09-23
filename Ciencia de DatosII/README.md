# Ciencia de Datos II · Data Science II

**Marlenis Judith Concepción Cuevas** · INF-8239-C2 · Maestría en Ciencia de Datos e Inteligencia Artificial, Universidad Autónoma de Santo Domingo (UASD) · Docente / Instructor: Edwin Ramón José Nolasco

> **ES** · Ocho proyectos reproducibles: clasificación con SVM y ensambles, reducción dimensional y Green AI, clasificación de texto, visión con CNN, sistemas de recomendación, modelos generativos (VAE), auditoría de equidad y gobernanza de un sistema de apoyo a decisiones. Cada proyecto incluye descarga verificada de datos, auditoría, líneas base, decisión fijada en validación antes de tocar la prueba, pruebas automatizadas, notebook ejecutado y PDF de entrega.
>
> **EN** · Eight reproducible projects: SVM and ensemble classification, dimensionality reduction and Green AI, text classification, CNN-based vision, recommender systems, generative models (VAE), fairness auditing and governance of a decision-support system. Every project ships verified data download, data audit, baselines, a model decision locked on validation before touching the test set, automated tests, an executed notebook and a PDF report.

## Resultados / Results

| Unidad / Unit | Ejercicio / Exercise | Datos / Data | Enfoque / Approach | Resultado clave / Key result | Pruebas / Tests |
|---|---|---|---|---|---|
| I | [01 · SVM reproducible](Unidad%20I/Ejercicio%2001/README.md) | Ionosphere (UCI) | Pipeline SVM, CV estratificada / stratified CV | F1 macro **0.938** vs 0.391 baseline | 4 |
| I | [02 · Ensambles y Green AI](Unidad%20I/Ejercicio%2002/README.md) | Ionosphere (UCI) | SVM, PCA, RF, GB; Pareto de 4 objetivos / 4-objective Pareto | GB-50: F1 **0.922**, 50 KB, 0.012 ms/fila | 4 |
| II | [03 · Clasificador de texto](Unidad%20II/Ejercicio%2003/README.md) | SMS Spam Collection (UCI) | TF-IDF + Naive Bayes / Logistic Regression | F1 macro **0.976** vs 0.468 baseline; 434 duplicados eliminados antes de partir / duplicates removed before splitting | 13 |
| II | [04 · CNN y Model Card](Unidad%20II/Ejercicio%2004/README.md) | Fashion-MNIST | Denso vs CNN; costo vs precisión / dense vs CNN; cost vs accuracy | CNN F1 macro **0.919** vs 0.876 dense | 9 |
| III | [05 · Recomendador](Unidad%20III/Ejercicio%2005/README.md) | MovieLens (no redistribuido / not redistributed) | Popularidad, contenido, factorización, híbrido; Pareto NDCG–cobertura | Híbrido: NDCG@10 **0.059**, cobertura / coverage **+35 %** vs MF | 13 |
| III | [06 · VAE y Model Card](Unidad%20III/Ejercicio%2006/README.md) | Fashion-MNIST | Media, PCA, AE, VAE 2/16; fidelidad, diversidad, memoria | VAE 16: MSE **0.0140**, 10/10 clases, **0.5 %** posibles copias / possible copies | 12 |
| IV | [07 · Impacto y equidad](Unidad%20IV/Ejercicio%2007/README.md) | DSS territorial sintético / synthetic | Fairlearn, bootstrap, interseccional, NIST AI RMF, Ley 172-13 | Regla transparente: brecha de recall **0.011** vs 0.138 del modelo; decisión / decision **LIMITAR** | 23 |
| IV | [08 · Gobernanza y simulacro](Unidad%20IV/Ejercicio%2008/README.md) | DSS territorial sintético / synthetic | Inventario, retención, RACI, Datasheet, Model Card, monitoreo, runbook | Falla detectada en la **1.ª semana** (z = −7.8) / incident caught in week 1 | 34 |

**112 pruebas automatizadas / automated tests**, todas aprobadas / all passing.

## Qué demuestra este repositorio / What this repository demonstrates

| ES | EN |
|---|---|
| **Prevención de fuga:** deduplicación normalizada antes de partir, ajustes solo con entrenamiento dentro de pipelines, cortes temporales por usuario y auditoría por hash. | **Leakage prevention:** normalized deduplication before splitting, train-only fitting inside pipelines, per-user temporal splits and hash-based audits. |
| **Decisiones honestas:** cada modelo se elige con una regla escrita y fijada en validación; la prueba se usa una sola vez. Cuando la prueba contradice a la validación, se informa y no se cambia la decisión. | **Honest model selection:** each model is chosen by a written rule locked on validation; the test set is used once. When test disagrees with validation, it is reported, not re-tuned. |
| **Más allá de la exactitud:** F1 macro, métricas por clase, NDCG, cobertura, novedad, costo (parámetros, tiempo, tamaño) y fronteras de Pareto. | **Beyond accuracy:** macro F1, per-class metrics, NDCG, coverage, novelty, cost (parameters, time, size) and Pareto fronts. |
| **Análisis de errores:** 23 SMS mal clasificados leídos y categorizados, confusiones por clase en visión y fallos por nivel de actividad del usuario. | **Error analysis:** 23 misclassified SMS read and categorized, per-class confusions in vision, and failures by user activity level. |
| **Pruebas con propósito:** cada prueba documenta qué comprueba y por qué; una prueba detectó un error real del recomendador, que se corrigió. | **Purposeful tests:** every test documents what it checks and why; one test caught a real recommender bug, which was fixed. |
| **Documentación responsable:** Dataset Cards, Model Cards, System Card, licencias verificadas y declaración de uso de IA. | **Responsible documentation:** Dataset Cards, Model Cards, a System Card, verified licenses and AI-use declarations. |

## Hallazgos destacados / Notable findings

- **ES** · La CNN pequeña del proyecto base rendía por debajo de un modelo denso (F1 0.785); su promedio global perdía la posición espacial. Una CNN con `Flatten` subió a 0.919.
  **EN** · The base project's small CNN underperformed a dense model (F1 0.785) because global pooling discarded spatial position; a `Flatten` CNN reached 0.919.
- **ES** · En recomendación, más épocas de factorización bajan el RMSE pero empeoran el ranking: predecir bien el rating no es ordenar bien.
  **EN** · In recommendation, more factorization epochs lower RMSE but hurt ranking: predicting ratings well is not ranking well.
- **ES** · El VAE con latente 2 no genera la clase Pullover y produce prototipos borrosos; con latente 16 cubre las 10 clases sin memorizar el entrenamiento.
  **EN** · The latent-2 VAE never generates Pullover and produces blurry prototypes; latent-16 covers all 10 classes without memorizing training data.
- **ES** · El 30 % de los errores de spam provienen de etiquetas dudosas del propio corpus, no del modelo.
  **EN** · 30 % of the spam errors come from questionable labels in the corpus itself, not from the model.

## Unidades / Units

- **[Unidad I](Unidad%20I/README.md)** · Técnicas avanzadas de análisis de datos / Advanced data analysis techniques: SVM, kernels, ensembles, PCA, t-SNE, Green AI.
- **[Unidad II](Unidad%20II/README.md)** · Procesamiento de lenguaje natural y visión / NLP and computer vision: corpus auditing, TF-IDF, text classification, CNN, Model Cards.
- **[Unidad III](Unidad%20III/README.md)** · Recomendación y modelos generativos / Recommenders and generative models: content-based, matrix factorization, hybrids, autoencoders, VAE.
- **[Unidad IV](Unidad%20IV/README.md)** · Ética, privacidad, equidad y gobernanza / Ethics, privacy, fairness and governance: impact assessment, Fairlearn audit, NIST AI RMF, RACI, monitoring, incident drill, [final project](Unidad%20IV/Trabajo%20final/README.md).

## Stack

Python 3.12 (Unidad I: 3.9) · uv · scikit-learn · TensorFlow/Keras 2.21 · Fairlearn · pandas · NumPy · matplotlib · pytest · Jupyter · ReportLab

## Reproducir / Reproduce

```bash
cd "Unidad II/Ejercicio 03"      # o cualquier ejercicio / or any exercise
uv python install 3.12
uv sync                          # uv sync --extra cpu en proyectos con TensorFlow / for TensorFlow projects
uv run pytest -q
```

Cada README explica la descarga de datos, el entrenamiento y la generación del PDF. / Each README covers data download, training and PDF generation.

## Uso de IA / AI use

**ES** · Se usaron Claude Code, Codex y DeepSeek como apoyo. Cada ejercicio declara herramientas, prompts, verificaciones y correcciones; la autora responde por el código, las cifras y las conclusiones.
**EN** · Claude Code, Codex and DeepSeek were used as assistants. Each exercise declares tools, prompts, checks and corrections; the author is accountable for the code, figures and conclusions.

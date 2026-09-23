# Model Card · Fashion-MNIST CNN

## Modelo y versión
`cnn_flatten` (`models/cnn_flatten.keras`), TensorFlow/Keras 2.21, entrenado el 23 de septiembre de 2026 con semilla 42. Arquitectura: Conv2D(32, 3×3) → MaxPool → Conv2D(64, 3×3) → MaxPool → Flatten → Dropout(0.3) → Dense(128) → Dense(10, softmax). 421 642 parámetros. Adam, entropía cruzada, lotes de 128, hasta 30 épocas con parada temprana (paciencia 2, restaura los mejores pesos); se detuvo en la época 12.

## Uso previsto
Uso académico: clasificar imágenes de 28×28 en escala de grises de prendas del catálogo Fashion-MNIST en 10 categorías, y comparar el costo y el desempeño de modelos pequeños.

## Usos fuera de alcance
Fotografías reales de ropa, imágenes en color o con fondo, otras resoluciones, catálogos de otras tiendas o cualquier decisión automática sobre personas o productos sin revisión humana.

## Dataset y particiones
Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017; arXiv:1708.07747; licencia MIT; Zalando Research), obtenido con `tf.keras.datasets.fashion_mnist`.
- Auditoría (`reports/auditoria.json`): 60 000 imágenes de entrenamiento y 10 000 de prueba, 6000 y 1000 por clase; píxeles uint8 entre 0 y 255; sin duplicados exactos dentro de cada conjunto, sin imágenes de entrenamiento repetidas en prueba y sin etiquetas contradictorias.
- Validación: 6000 imágenes estratificadas (600 por clase) tomadas del entrenamiento oficial con semilla 42; índices en `reports/indices_validacion.csv`.
- Entrenamiento: 54 000 imágenes. Prueba: las 10 000 oficiales, usadas una sola vez después de fijar la decisión.

## Preprocesamiento
División entre 255 para escalar a [0, 1] y canal único añadido (28×28×1). No hay aumentación de datos. La validación de formato y rango se hace en `validate_images`.

## Métricas globales y por clase
Prueba: F1 macro **0.919**, accuracy **0.920**. Validación: F1 macro 0.926.

| Clase | Precisión | Recall | F1 | Errores |
|---|---|---|---|---|
| T-shirt/top | 0.849 | 0.909 | 0.878 | 91 |
| Trouser | 0.985 | 0.991 | 0.988 | 9 |
| Pullover | 0.889 | 0.854 | 0.871 | 146 |
| Dress | 0.918 | 0.931 | 0.925 | 69 |
| Coat | 0.861 | 0.897 | 0.879 | 103 |
| Sandal | 0.990 | 0.978 | 0.984 | 22 |
| **Shirt** | 0.807 | **0.728** | **0.766** | **272** |
| Sneaker | 0.928 | 0.990 | 0.958 | 10 |
| Bag | 0.983 | 0.982 | 0.982 | 18 |
| Ankle boot | 0.988 | 0.939 | 0.963 | 61 |

Confusión principal: Shirt → T-shirt/top (118), Shirt → Coat (69), T-shirt/top → Shirt (63), Pullover → Coat (62), Ankle boot → Sneaker (56).

## Comparación de costo
- Hardware: Apple M1 Pro, CPU (sin GPU), macOS 26.6, TensorFlow 2.21.0.
- Parámetros: línea base 0 · denso 50 890 · CNN base 19 466 · **CNN Flatten 421 642**.
- Tiempo de entrenamiento: denso 10.9 s (28 épocas) · CNN base 188.2 s (30 épocas, sin converger) · **CNN Flatten 86.8 s (12 épocas)**.
- Tiempo de inferencia: denso 0.008 ms/imagen · CNN base 0.028 ms · **CNN Flatten 0.032 ms**, en lotes de 256.
- Tamaño en disco: denso 619 KB · CNN base 262 KB · **CNN Flatten 4980 KB**.

| Modelo | F1 macro validación | F1 macro prueba |
|---|---|---|
| Línea base (clase más frecuente) | 0.018 | 0.018 |
| Denso (proyecto base) | 0.888 | 0.876 |
| CNN pequeña (proyecto base) | 0.854 | 0.847 |
| **CNN Flatten (elegida)** | **0.926** | **0.919** |

Decisión (`reports/decision.json`, fijada antes de la prueba): elegir el modelo con menos parámetros entre los que están a menos de 0.01 del mejor F1 macro de validación. Solo `cnn_flatten` cumplía. A cambio de +0.04 de F1 macro cuesta 8 veces más parámetros y 4 veces más tiempo de inferencia que el denso; en esta escala la inferencia sigue siendo inferior a 0.1 ms por imagen.

## Limitaciones y riesgos
- Shirt es la clase más débil (recall 0.73): se confunde con camisetas, abrigos y suéteres, que a 28×28 píxeles tienen la misma silueta.
- La CNN pequeña del proyecto base no converge en 8 épocas (F1 0.785, `reports/corrida_8_epocas/`) ni en 30; su promediado global pierde la posición de los rasgos.
- Resultados de una sola semilla y una sola partición; no se estimó la variabilidad entre ejecuciones.
- Las imágenes están centradas y normalizadas por el catálogo; el desempeño no se traslada a fotos reales.

## Supervisión y monitoreo
Registrar la distribución de clases predichas y la confianza media; revisar manualmente las predicciones de Shirt, T-shirt/top, Coat y Pullover con confianza inferior a 0.6; reevaluar con una muestra etiquetada si cambia la fuente de imágenes. Cualquier uso fuera del aula requiere reentrenar con datos del dominio.

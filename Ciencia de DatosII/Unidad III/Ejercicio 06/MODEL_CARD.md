# Model Card · Autoencoder y VAE

## Modelos y versiones
Entrenados el 23 de septiembre de 2026 con TensorFlow/Keras 2.21 y semilla 42 (`reports/metricas.json`).
- **AE 16** (proyecto base): Flatten → Dense(16, ReLU) → Dense(784, sigmoide). 25 888 parámetros.
- **VAE 2** (proyecto base): codificador Dense(128) → μ y log σ² de 2 dimensiones; decodificador Dense(128) → Dense(784). 202 516 parámetros.
- **VAE 16**: la misma arquitectura con latente 16. 207 920 parámetros. **Elegido.**
- Líneas base sin entrenamiento: imagen media de entrenamiento y PCA con 16 componentes.

## Uso previsto y usuarios
Uso académico: estudiar reconstrucción, espacio latente y generación de imágenes de 28×28 de Fashion-MNIST.

## Usos fuera de alcance
Generar datos sintéticos para sustituir datos reales en un análisis, anonimizar datos personales, fotografías reales o decisiones sobre personas o productos. **Generar datos sintéticos no garantiza privacidad por sí solo.**

## Dataset, licencia y particiones
Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017; licencia MIT), obtenido con `tf.keras.datasets`. Entrenamiento: 54 000 imágenes. Validación: 6000 imágenes aleatorias del entrenamiento oficial (semilla 42, `reports/indices_validacion.csv`). Prueba: 10 000 oficiales, usadas solo para medir reconstrucción y como referencia de memoria.

## Arquitectura y espacio latente
El VAE aprende una distribución gaussiana por imagen y se regulariza con la divergencia KL hacia N(0, I), lo que permite muestrear e interpolar. `reports/espacio_latente.png` muestra que en 2 dimensiones las clases de calzado, pantalones y bolsos se separan, mientras las prendas superiores se solapan.

## Métricas de reconstrucción y generación
| Modelo | MSE por píxel (prueba) | BCE por imagen (prueba) | Pérdida validación |
|---|---|---|---|
| Imagen media | 0.0866 | 385.0 | — |
| PCA 16 | 0.0198 | 249.3 | — |
| AE 16 | 0.0179 | 234.6 | — |
| VAE 2 | 0.0292 | 258.0 | 262.9 |
| **VAE 16** | **0.0140** | **223.9** | **242.6** |

Fidelidad, evaluada con un clasificador juez (exactitud 0.893 en prueba) sobre 1000 muestras de N(0, I): confianza media 0.625 para VAE 16 y 0.528 para VAE 2; las imágenes reales de prueba obtienen 0.900.

## Diversidad y vecinos cercanos
| Conjunto | Clases cubiertas | Entropía de clases | Dispersión | Distancia mediana al vecino de entrenamiento | Posibles copias |
|---|---|---|---|---|---|
| Real (prueba) | 10 | 0.998 | 11.24 | 3.52 | 5.0 % (por definición) |
| VAE 2 | 9 | 0.883 | 6.96 | 2.56 | 19.0 % |
| **VAE 16** | **10** | **0.981** | **8.55** | **3.62** | **0.5 %** |

"Posibles copias" es el porcentaje de muestras más cercanas a una imagen de entrenamiento que el 95 % de las imágenes reales de prueba (umbral 1.96). El VAE 2 no copia imágenes concretas: genera prototipos borrosos y simples, cercanos a muchas prendas de entrenamiento, y nunca produce Pullover.

## Hardware, tiempo y tamaño
Apple M1 Pro, CPU, TensorFlow 2.21. AE 16: 19.8 s (30 épocas), 331 KB. VAE 2: 41.2 s (40 épocas), 833 KB. VAE 16: 44.2 s (40 épocas), 854 KB. PCA: 0.2 s. Los tres modelos llegaron al máximo de épocas sin activar la parada temprana, por lo que podrían mejorar algo más.

## Limitaciones, riesgos y supervisión
- Las muestras son borrosas (BCE con decodificador denso); la confianza del juez es muy inferior a la de imágenes reales.
- El juez tiene sus propios errores (89.3 %); las medidas de fidelidad dependen de él.
- Una sola semilla; no se estimó la variabilidad.
- Antes de publicar datos sintéticos, revisar la distancia al vecino más cercano y la presencia de copias; documentar que no son datos reales.

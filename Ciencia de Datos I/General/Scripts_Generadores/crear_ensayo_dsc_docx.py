from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from html import escape


GENERAL = Path(__file__).resolve().parents[1]
OUT = GENERAL / "Documentos_Academicos" / "Ensayo_Origen_y_Evolucion_Ciencia_de_Datos_Marlenis.docx"


def p(text="", style=None, align=None, bold=False):
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f"<w:p>{ppr}<w:r>{rpr}<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r></w:p>"


def heading(text, level):
    style = {1: "Heading1", 2: "Heading2", 3: "Heading3"}[level]
    return p(text, style=style)


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def bullet(text):
    return (
        '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/>'
        '<w:numId w:val="1"/></w:numPr></w:pPr>'
        f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
    )


def table(rows):
    out = ['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/>'
           '<w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/>'
           '<w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/>'
           '</w:tblBorders></w:tblPr>']
    for row in rows:
        out.append("<w:tr>")
        for cell in row:
            out.append(f'<w:tc><w:tcPr><w:tcW w:w="2400" w:type="dxa"/></w:tcPr>{p(cell)}</w:tc>')
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


content = []

content += [
    p("Universidad Autónoma de Santo Domingo (UASD)", align="center", bold=True),
    p("Facultad de Ciencias", align="center"),
    p("Asignatura: Ciencias de Datos I / INF-8237-C2", align="center"),
    p("Ensayo 1: Origen y Evolución de la Ciencia de Datos", align="center", bold=True),
    p("", align="center"),
    p("Participante: Marlenis Judith Concepción Cuevas", align="center"),
    p("Docente: ______________________________", align="center"),
    p("Fecha: 17 de mayo de 2026", align="center"),
    p("Santo Domingo, República Dominicana", align="center"),
    page_break(),
]

content += [
    heading("Resumen", 1),
    p("La ciencia de datos es un campo interdisciplinario que surge de la convergencia entre el análisis estadístico, la computación, la minería de datos, el aprendizaje automático y las necesidades prácticas de extraer conocimiento de grandes volúmenes de información. Este ensayo analiza su origen y evolución a partir de fuentes científicas arbitradas y textos de alto impacto. Se revisa el papel fundacional de John W. Tukey, quien en 1962 propuso una reforma del análisis de datos al defender que el trabajo con datos constituía un campo intelectual propio. También se examina la contribución de William S. Cleveland, quien en 2001 usó explícitamente la expresión ciencia de datos para ampliar las áreas técnicas de la estadística. Se estudian las primeras revistas y conferencias vinculadas al área, especialmente KDD, ACM SIGKDD, Data Mining and Knowledge Discovery y Journal of Data Science. Asimismo, se contrasta la minería de datos con las matemáticas estadísticas, mostrando que la primera enfatiza el descubrimiento de patrones en bases de datos, mientras que la segunda aporta inferencia, probabilidad, estimación y validación de incertidumbre. Finalmente, se describe el surgimiento de los algoritmos de aprendizaje automático y las sociedades científicas que lideran el campo. La conclusión principal es que la ciencia de datos no reemplaza la estadística ni la informática, sino que las integra en una práctica orientada a producir conocimiento reproducible, predictivo, explicativo y útil para la toma de decisiones."),
    p("Palabras clave: ciencia de datos, minería de datos, aprendizaje automático, estadística, KDD."),
    page_break(),
    heading("Abstract", 1),
    p("Data science is an interdisciplinary field emerging from the convergence of statistical analysis, computing, data mining, machine learning, and the practical need to extract knowledge from large volumes of information. This essay analyzes its origin and evolution using peer-reviewed scientific sources and high-impact references. It reviews the foundational role of John W. Tukey, who in 1962 called for a reform of data analysis and argued that working with data represented an intellectual field of its own. It also examines William S. Cleveland’s contribution, who explicitly used the term data science in 2001 to expand the technical areas of statistics. The paper discusses early journals and conferences related to the field, particularly KDD, ACM SIGKDD, Data Mining and Knowledge Discovery, and Journal of Data Science. It also contrasts data mining with mathematical statistics, showing that data mining emphasizes pattern discovery in databases, while statistics provides inference, probability, estimation, and uncertainty validation. Finally, the paper describes the emergence of machine learning algorithms and the scientific societies leading the field. The main conclusion is that data science does not replace statistics or computer science; instead, it integrates them into a practice aimed at producing reproducible, predictive, explanatory, and useful knowledge for decision-making."),
    p("Keywords: data science, data mining, machine learning, statistics, KDD."),
    page_break(),
    heading("Tabla de contenido", 1),
    p("1. Origen y Evolución de la Ciencia de Datos"),
    p("1.1 Introducción"),
    p("1.2 Marco de referencia"),
    p("1.3 Padre fundador de la ciencia de datos"),
    p("1.4 Primeras revistas y conferencias científicas"),
    p("1.5 Minería de datos versus matemáticas estadísticas"),
    p("1.6 Surgimiento de los algoritmos"),
    p("1.7 Sociedades que lideran el campo"),
    p("1.8 Línea de tiempo"),
    p("1.9 Conclusiones"),
    p("Referencias"),
    p("Anexo"),
    page_break(),
]

content += [
    heading("Origen y Evolución de la Ciencia de Datos", 1),
    heading("Introducción", 2),
    p("La ciencia de datos, conocida también como Data Science o DSC, se ha convertido en una de las áreas más influyentes del conocimiento contemporáneo porque responde a una realidad concreta: las sociedades, empresas, gobiernos y comunidades científicas producen datos a una velocidad superior a la capacidad humana tradicional de analizarlos. Sin embargo, su origen no se limita al auge reciente del Big Data ni a la popularidad de la inteligencia artificial. La ciencia de datos tiene raíces profundas en la estadística, la computación, la minería de datos, la inteligencia artificial, la visualización y la investigación científica reproducible."),
    p("En una cita narrativa, Tukey (1962) defendió que el análisis de datos debía reconocerse como una actividad científica con identidad propia, distinta de la estadística matemática estrictamente formal. Esta idea es central porque anticipa una tensión que todavía existe: la diferencia entre hacer teoría estadística y trabajar con datos reales, incompletos, ruidosos, heterogéneos y dependientes del contexto. Más tarde, Cleveland (2001) propuso ampliar formalmente el campo de la estadística mediante un plan de acción centrado en el analista de datos, la computación, los modelos y la colaboración interdisciplinaria."),
    p("El objetivo de este ensayo es investigar la historia y evolución de la ciencia de datos, identificando su padre fundador, sus primeras revistas y conferencias científicas, el contraste entre minería de datos y matemáticas estadísticas, el surgimiento de los algoritmos y las sociedades que lideran el campo. Para ello se utilizan artículos arbitrados, libros académicos y fuentes científicas de alto impacto, siguiendo el estilo APA."),
    heading("Marco de referencia", 2),
    p("La ciencia de datos puede entenderse como un campo integrador. Donoho (2017) sostiene que la discusión moderna sobre el área debe ubicarse en una tradición más larga de análisis de datos, estadística computacional, investigación reproducible y aprendizaje desde datos. En ese sentido, DSC no es simplemente usar herramientas de programación ni construir modelos automáticos, sino organizar un proceso completo que va desde la formulación del problema hasta la comunicación de resultados."),
    p("Una cita parentética ayuda a precisar esta idea: la ciencia de datos se desarrolla en la intersección de estadística, computación, visualización, modelado, inferencia, bases de datos y conocimiento aplicado (Donoho, 2017; Cleveland, 2001; Fayyad et al., 1996). Esta condición interdisciplinaria explica por qué el campo no tiene una sola institución fundadora ni una fecha única de nacimiento, sino una trayectoria evolutiva."),
    p("En el plano metodológico, el campo se alimenta de tres líneas principales. La primera proviene de la estadística y su interés por la inferencia, la estimación, el diseño de estudios y la medición de incertidumbre. La segunda proviene de la informática, especialmente de bases de datos, algoritmos, sistemas distribuidos y lenguajes de programación. La tercera proviene del aprendizaje automático y la minería de datos, cuyo foco está en descubrir patrones y producir modelos predictivos útiles."),
    heading("Padre fundador de la ciencia de datos", 2),
    p("Aunque no existe un consenso absoluto sobre un único padre fundador, la literatura reconoce a John W. Tukey como una figura fundacional del pensamiento que dio origen a la ciencia de datos. En The Future of Data Analysis, Tukey (1962) propuso que el análisis de datos debía ocupar un lugar propio dentro de la actividad científica. Su aporte no consistió en crear un software ni una institución, sino en formular una visión: los datos no debían tratarse únicamente como insumos para probar teorías matemáticas, sino como objetos de exploración, descubrimiento y razonamiento."),
    p("Donoho (2017) retoma a Tukey como punto de partida para explicar cincuenta años de ciencia de datos. Según esta lectura, Tukey anticipó una reforma intelectual: aprender de los datos requería métodos, gráficos, experimentación computacional, criterio empírico y comunicación. Una breve cita textual resume su legado conceptual: Tukey apuntó hacia una ciencia cuyo interés era “learning from data” (Donoho, 2017, p. 745). Esta frase no debe entenderse como una definición completa, sino como una idea organizadora del campo."),
    p("No obstante, William S. Cleveland también ocupa un lugar decisivo. Cleveland (2001) usó explícitamente la expresión data science y propuso un plan para expandir las áreas técnicas de la estadística. Su propuesta incluyó computación con datos, pedagogía, modelos, teoría, herramientas y colaboración práctica. Por tanto, puede afirmarse que Tukey es el padre intelectual del análisis de datos moderno, mientras Cleveland es uno de los principales formalizadores del término ciencia de datos dentro de la estadística contemporánea."),
    heading("Primeras revistas y conferencias científicas", 2),
    p("La consolidación de un campo científico suele evidenciarse cuando aparecen revistas, conferencias, sociedades y comunidades de revisión por pares. En ciencia de datos, una de las tradiciones más tempranas fue la de Knowledge Discovery in Databases, conocida como KDD. El primer taller KDD se realizó en 1989, asociado a la comunidad de inteligencia artificial y bases de datos. Luego, la conferencia KDD se convirtió en una de las reuniones científicas más importantes para minería de datos, descubrimiento de conocimiento y análisis avanzado."),
    p("Fayyad et al. (1996) fueron fundamentales al organizar conceptualmente el proceso KDD. Estos autores definieron la minería de datos como una etapa dentro de un proceso más amplio que incluye selección, preprocesamiento, transformación, extracción de patrones, evaluación e interpretación. Su artículo en Communications of the ACM es una referencia obligatoria porque ayudó a distinguir entre minería de datos como técnica y descubrimiento de conocimiento como proceso completo."),
    p("Entre las primeras revistas relevantes se encuentra Data Mining and Knowledge Discovery, publicada por Springer desde 1997, con Usama Fayyad como editor fundador. Esta revista contribuyó a legitimar científicamente la minería de datos como área de investigación. Otra publicación significativa es Journal of Computational and Graphical Statistics, fundada en 1992, importante para la estadística computacional, visualización y análisis de datos. También se destaca Journal of Data Science, establecido en 2003, cuyo objetivo ha sido publicar investigaciones sobre métodos, computación y aplicaciones de ciencia de datos."),
    p("Estas publicaciones muestran que la ciencia de datos no nació de manera aislada. Surgió como resultado de la convergencia entre comunidades: estadísticos interesados en computación, informáticos interesados en datos, investigadores de inteligencia artificial interesados en aprendizaje automático y científicos aplicados interesados en resolver problemas reales."),
    heading("Minería de datos versus matemáticas estadísticas", 2),
    p("La relación entre minería de datos y matemáticas estadísticas es de complementariedad, pero también de contraste. La estadística matemática se fundamenta en probabilidad, inferencia, estimación, pruebas de hipótesis, distribuciones, modelos y teoría del error. Su pregunta central suele ser: ¿qué se puede inferir válidamente sobre una población o un proceso a partir de datos observados? En cambio, la minería de datos pregunta: ¿qué patrones útiles, novedosos o accionables pueden descubrirse en grandes bases de datos?"),
    p("Breiman (2001) explicó esta diferencia mediante la idea de dos culturas del modelado estadístico. Una cultura se centra en modelos probabilísticos que buscan explicar cómo se generaron los datos; la otra se centra en algoritmos que buscan predecir con precisión la salida a partir de entradas observadas. Este contraste es útil para comprender por qué la minería de datos y el aprendizaje automático no siempre tienen los mismos objetivos que la estadística inferencial clásica."),
    p("La minería de datos suele trabajar con grandes volúmenes de datos operacionales, bases transaccionales, registros digitales, textos, redes, imágenes o secuencias. Sus técnicas incluyen clasificación, agrupamiento, reglas de asociación, detección de anomalías, árboles de decisión, redes neuronales y métodos de reducción de dimensionalidad. La estadística matemática, por su parte, aporta criterios de validez: incertidumbre, sesgo, varianza, significancia, intervalos de confianza, diseño muestral y generalización."),
    p("Por eso, no es correcto afirmar que la minería de datos reemplaza a la estadística. Más bien, la ciencia de datos necesita ambas. Sin teoría estadística, los patrones pueden ser espurios; sin minería de datos y computación, muchos fenómenos contemporáneos serían imposibles de explorar a escala. Hastie et al. (2009) integran esta visión al presentar el aprendizaje estadístico como un puente entre inferencia, predicción y minería de datos."),
    heading("Surgimiento de los algoritmos", 2),
    p("El surgimiento de los algoritmos en ciencia de datos está relacionado con el desarrollo de la inteligencia artificial, el aprendizaje automático, la estadística computacional y el aumento de la capacidad de almacenamiento y procesamiento. Desde mediados del siglo XX se desarrollaron métodos de regresión, clasificación, árboles de decisión, clustering y redes neuronales. Sin embargo, su expansión se aceleró cuando las organizaciones comenzaron a acumular bases de datos masivas y cuando la computación permitió entrenar modelos complejos."),
    p("Mitchell (1997) definió el aprendizaje automático como el estudio de programas que mejoran su desempeño en una tarea a partir de la experiencia. Esta definición es importante porque desplaza el foco desde la programación explícita hacia el aprendizaje basado en datos. Posteriormente, Hastie et al. (2009) y James et al. (2021) sistematizaron métodos como regresión lineal, regresión logística, árboles, máquinas de soporte vectorial, métodos de remuestreo, regularización, clustering y aprendizaje supervisado y no supervisado."),
    p("El auge de los algoritmos también transformó la noción de evidencia. En la estadística clásica, la evidencia se relaciona con pruebas, estimadores y modelos interpretables. En ciencia de datos, además, se evalúa la capacidad predictiva mediante métricas como exactitud, precisión, sensibilidad, especificidad, error cuadrático medio, validación cruzada y desempeño fuera de muestra. Esta evolución no elimina la inferencia, pero amplía las formas de evaluar el conocimiento generado."),
    p("La aparición de algoritmos de aprendizaje profundo en el siglo XXI reforzó todavía más el crecimiento del campo. Sin embargo, la ciencia de datos no se reduce al deep learning. Incluye tareas previas y posteriores al modelado: calidad de datos, ingeniería de variables, ética, privacidad, comunicación, visualización, despliegue y monitoreo. Por eso, un científico de datos no solo ejecuta algoritmos; también formula preguntas, evalúa sesgos y traduce resultados para la toma de decisiones."),
    heading("Sociedades que lideran este campo", 2),
    p("Las sociedades científicas han sido esenciales para consolidar la ciencia de datos. Entre las principales se encuentra la Association for Computing Machinery, especialmente a través de ACM SIGKDD, grupo especializado en Knowledge Discovery and Data Mining. Esta sociedad organiza la conferencia KDD, una de las más influyentes del mundo en minería de datos, ciencia de datos aplicada y aprendizaje automático."),
    p("También destaca la American Statistical Association, que ha impulsado la integración entre estadística y ciencia de datos mediante publicaciones, secciones técnicas y debates curriculares. El Institute of Mathematical Statistics y la International Statistical Institute han contribuido desde la teoría estadística, la inferencia y la probabilidad. En el área de ingeniería y computación, el IEEE y sus sociedades relacionadas con inteligencia computacional y sistemas de información también lideran investigaciones sobre algoritmos, aprendizaje automático, big data y aplicaciones."),
    p("En Europa y otras regiones existen comunidades asociadas a bases de datos, inteligencia artificial y estadística aplicada que fortalecen el campo mediante congresos, revistas y estándares. La presencia de estas sociedades confirma que la ciencia de datos es un campo global, institucionalizado y sometido a revisión académica."),
    heading("Línea de tiempo", 2),
    p("Figura 1"),
    p("Línea de tiempo resumida de la evolución de la ciencia de datos"),
    table([
        ["Año", "Hito", "Importancia"],
        ["1962", "John W. Tukey publica The Future of Data Analysis.", "Plantea el análisis de datos como campo intelectual propio."],
        ["1989", "Primer taller KDD.", "Inicia una comunidad formal sobre descubrimiento de conocimiento en bases de datos."],
        ["1992", "Journal of Computational and Graphical Statistics.", "Fortalece la estadística computacional y gráfica."],
        ["1996", "Fayyad, Piatetsky-Shapiro y Smyth sistematizan KDD.", "Distingue minería de datos y proceso de descubrimiento de conocimiento."],
        ["1997", "Inicia Data Mining and Knowledge Discovery.", "Primera revista especializada de alto impacto en minería de datos."],
        ["2001", "Cleveland propone Data Science como ampliación de la estadística.", "Formaliza el término dentro de una agenda técnica."],
        ["2001", "Breiman publica Statistical Modeling: The Two Cultures.", "Contrasta modelado estadístico y modelado algorítmico."],
        ["2003", "Se establece Journal of Data Science.", "Promueve métodos, computación y aplicaciones de ciencia de datos."],
        ["2017", "Donoho publica 50 Years of Data Science.", "Reconstruye históricamente la identidad del campo."],
        ["2020 en adelante", "Expansión de IA, big data y ciencia reproducible.", "La ciencia de datos se consolida como práctica transversal."]
    ]),
    p("Nota. Elaboración propia con base en Tukey (1962), Fayyad et al. (1996), Cleveland (2001), Breiman (2001) y Donoho (2017)."),
    heading("Conclusiones", 2),
    p("La ciencia de datos tiene una evolución compleja y multidisciplinaria. Su origen intelectual puede rastrearse hasta John W. Tukey, quien defendió el análisis de datos como una actividad científica propia. Posteriormente, Cleveland contribuyó a formalizar el término ciencia de datos dentro de una agenda de expansión de la estadística. A partir de los años ochenta y noventa, la minería de datos, KDD y el aprendizaje automático aportaron métodos para descubrir patrones y construir modelos predictivos a gran escala."),
    p("El contraste entre minería de datos y matemáticas estadísticas muestra que ambas áreas cumplen funciones distintas. La minería de datos enfatiza el descubrimiento, la escala y la utilidad práctica; la estadística aporta inferencia, incertidumbre, rigor metodológico y validación. La ciencia de datos surge precisamente de integrar estas perspectivas, junto con programación, visualización, bases de datos y conocimiento del dominio."),
    p("Las revistas y conferencias como KDD, Data Mining and Knowledge Discovery, Journal of Computational and Graphical Statistics y Journal of Data Science demuestran que el campo se institucionalizó mediante mecanismos científicos revisados por pares. Asimismo, sociedades como ACM SIGKDD, ASA, IEEE, IMS e ISI continúan liderando su desarrollo. En conclusión, DSC no debe entenderse como una moda tecnológica, sino como una evolución científica orientada a aprender de los datos, producir conocimiento confiable y apoyar decisiones en contextos complejos."),
    page_break(),
    heading("Referencias", 1),
    p("Breiman, L. (2001). Statistical modeling: The two cultures. Statistical Science, 16(3), 199–231. https://doi.org/10.1214/ss/1009213726"),
    p("Casella, G., & Berger, R. L. (2002). Statistical inference (2nd ed.). Duxbury."),
    p("Cleveland, W. S. (2001). Data science: An action plan for expanding the technical areas of the field of statistics. International Statistical Review, 69(1), 21–26."),
    p("Donoho, D. (2017). 50 years of data science. Journal of Computational and Graphical Statistics, 26(4), 745–766. https://doi.org/10.1080/10618600.2017.1384734"),
    p("Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). The KDD process for extracting useful knowledge from volumes of data. Communications of the ACM, 39(11), 27–34. https://doi.org/10.1145/240455.240464"),
    p("Han, J., Kamber, M., & Pei, J. (2011). Data mining: Concepts and techniques (3rd ed.). Morgan Kaufmann."),
    p("Hastie, T., Tibshirani, R., & Friedman, J. (2009). The elements of statistical learning: Data mining, inference, and prediction (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-84858-7"),
    p("James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An introduction to statistical learning: With applications in R (2nd ed.). Springer. https://doi.org/10.1007/978-1-0716-1418-1"),
    p("Mitchell, T. M. (1997). Machine learning. McGraw-Hill. https://www.cs.cmu.edu/~tom/mlbook.html"),
    p("Tukey, J. W. (1962). The future of data analysis. The Annals of Mathematical Statistics, 33(1), 1–67."),
    p("Witten, I. H., Frank, E., Hall, M. A., & Pal, C. J. (2016). Data mining: Practical machine learning tools and techniques (4th ed.). Morgan Kaufmann."),
    page_break(),
    heading("Anexo", 1),
    heading("Anexo A. Código QR para acceder en línea", 2),
    p("Inserte aquí el código QR generado después de subir la línea de tiempo o el documento a Google Drive, OneDrive, Canva, Genially o cualquier repositorio en línea. En el cuerpo del documento ya se incluyó la Figura 1 con la línea de tiempo resumida."),
    p("Enlace sugerido para el QR: pegar aquí el enlace público del documento o de la infografía en línea."),
    heading("Anexo B. Recomendación para generar el QR", 2),
    p("1. Subir el documento o la infografía a Google Drive o Canva."),
    p("2. Configurar el enlace como público o visible para quien tenga el enlace."),
    p("3. Generar el QR con el enlace público."),
    p("4. Insertar la imagen del QR en este anexo antes de entregar el archivo final."),
]


styles = """
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="220" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:i/></w:rPr></w:style>
</w:styles>
"""

numbering = """
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>
"""

document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
{''.join(content)}
<w:sectPr>
<w:pgSz w:w="12240" w:h="15840"/>
<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
</w:sectPr>
</w:body>
</w:document>
"""

content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>
"""

rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>
"""

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering)
    z.writestr("word/_rels/document.xml.rels", doc_rels)

print(OUT.resolve())

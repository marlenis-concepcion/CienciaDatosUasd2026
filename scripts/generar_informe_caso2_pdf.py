from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "caso_practico_2_sakila_crud_orm" / "docs" / "informe" / "Informe_Caso_2_Sakila_APA_UASD.pdf"

DPI = 300
PAGE_W = int(8.5 * DPI)
PAGE_H = int(11 * DPI)
MARGIN = DPI
TEXT_W = PAGE_W - (MARGIN * 2)
TOP = MARGIN
BOTTOM = PAGE_H - MARGIN
INK = (28, 34, 42)
MUTED = (82, 92, 105)
LINE = (198, 207, 218)
GREEN = (31, 122, 92)
BLUE = (35, 100, 170)
PAPER = (255, 255, 255)


def font(name, size):
    paths = {
        "regular": [
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
            "/System/Library/Fonts/Times.ttc",
        ],
        "bold": [
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
            "/System/Library/Fonts/Times.ttc",
        ],
        "italic": [
            "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
            "/System/Library/Fonts/Times.ttc",
        ],
    }
    for path in paths[name]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


F12 = font("regular", 50)
F12B = font("bold", 50)
F12I = font("italic", 50)
F14B = font("bold", 58)
F16B = font("bold", 66)
F18B = font("bold", 76)
F22B = font("bold", 92)
F10 = font("regular", 42)
F10B = font("bold", 42)


def text_width(draw, text, face):
    return draw.textbbox((0, 0), text, font=face)[2]


def text_height(draw, text, face):
    box = draw.textbbox((0, 0), text, font=face)
    return box[3] - box[1]


class Document:
    def __init__(self):
        self.pages = []
        self.page = None
        self.draw = None
        self.y = TOP
        self.page_number = 0

    def new_page(self, number=True):
        if self.page is not None:
            self.pages.append(self.page)
        self.page_number += 1
        self.page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.draw = ImageDraw.Draw(self.page)
        self.y = TOP
        if number:
            num = str(self.page_number)
            self.draw.text((PAGE_W - MARGIN - text_width(self.draw, num, F12), 115), num, fill=INK, font=F12)

    def save(self):
        if self.page is not None:
            self.pages.append(self.page)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        self.pages[0].save(OUT, "PDF", resolution=DPI, save_all=True, append_images=self.pages[1:])
        print(OUT.relative_to(ROOT))

    def ensure(self, needed):
        if self.y + needed > BOTTOM:
            self.new_page()

    def center(self, text, face=F12, fill=INK, gap=32):
        w = text_width(self.draw, text, face)
        self.draw.text(((PAGE_W - w) / 2, self.y), text, fill=fill, font=face)
        self.y += text_height(self.draw, text, face) + gap

    def left(self, text, face=F12, fill=INK, x=MARGIN, gap=26):
        self.draw.text((x, self.y), text, fill=fill, font=face)
        self.y += text_height(self.draw, text, face) + gap

    def heading(self, text):
        self.ensure(130)
        self.center(text, F14B, gap=44)

    def subheading(self, text):
        self.ensure(95)
        self.left(text, F12B, gap=28)

    def rule(self, color=LINE):
        self.draw.line((MARGIN, self.y, PAGE_W - MARGIN, self.y), fill=color, width=3)
        self.y += 42

    def wrap(self, text, face, width):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if text_width(self.draw, trial, face) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def paragraph(self, text, indent=True, face=F12, fill=INK):
        line_gap = 84
        first_indent = 150 if indent else 0
        lines = self.wrap(text, face, TEXT_W - first_indent)
        for i, line in enumerate(lines):
            self.ensure(line_gap + 10)
            x = MARGIN + (first_indent if i == 0 else 0)
            self.draw.text((x, self.y), line, fill=fill, font=face)
            self.y += line_gap
        self.y += 22

    def bullet(self, text):
        line_gap = 72
        bullet_x = MARGIN + 45
        text_x = MARGIN + 90
        lines = self.wrap(text, F12, TEXT_W - 120)
        for i, line in enumerate(lines):
            self.ensure(line_gap + 10)
            if i == 0:
                self.draw.text((bullet_x, self.y), "•", fill=INK, font=F12)
            self.draw.text((text_x, self.y), line, fill=INK, font=F12)
            self.y += line_gap
        self.y += 10

    def reference(self, text):
        line_gap = 72
        hanging = 150
        lines = self.wrap(text, F12, TEXT_W - hanging)
        for i, line in enumerate(lines):
            self.ensure(line_gap + 10)
            x = MARGIN if i == 0 else MARGIN + hanging
            width = TEXT_W if i == 0 else TEXT_W - hanging
            if i == 0:
                lines = self.wrap(text, F12, width)
            self.draw.text((x, self.y), line, fill=INK, font=F12)
            self.y += line_gap
        self.y += 18


def cover(doc):
    doc.new_page(number=False)
    doc.y = 250
    doc.center("Universidad Autónoma de Santo Domingo", F18B, gap=34)
    doc.center("Facultad de Ingeniería y Arquitectura", F14B, gap=28)
    doc.center("Asignatura: INF-8237 Ciencia de Datos I", F12B, gap=24)
    doc.y += 230
    doc.rule(GREEN)
    doc.center("Caso práctico 2", F18B, gap=38)
    doc.center("CRUD/ORM nativo basado en POO y estructuras de datos", F16B, gap=30)
    doc.center("en MySQL Sakila", F16B, gap=42)
    doc.rule(GREEN)
    doc.y += 230
    rows = [
        ("Equipo:", "UASDVirtual"),
        ("Integrante:", "Marlenis Judith Concepción Cuevas"),
        ("Facilitador:", "Dr. Silverio del Orbe"),
        ("Fecha:", "4 de junio de 2026"),
    ]
    for label, value in rows:
        w = text_width(doc.draw, label, F12B)
        x = (PAGE_W - 1050) / 2
        doc.draw.text((x, doc.y), label, fill=INK, font=F12B)
        doc.draw.text((x + w + 26, doc.y), value, fill=INK, font=F12)
        doc.y += 86


def toc(doc):
    doc.new_page()
    doc.heading("Tabla de contenido")
    entries = [
        ("Resumen", "3"),
        ("Abstract", "4"),
        ("Introducción", "5"),
        ("Marco de referencia", "6"),
        ("Descripción del caso práctico", "7"),
        ("Arquitectura del sistema", "8"),
        ("Implementación del CRUD/ORM", "9"),
        ("Pruebas y resultados", "10"),
        ("Conclusiones", "11"),
        ("Referencias", "12"),
        ("Anexos", "13"),
    ]
    for title, page in entries:
        doc.ensure(80)
        left = MARGIN
        right = PAGE_W - MARGIN - text_width(doc.draw, page, F12)
        dots_width = right - left - text_width(doc.draw, title, F12) - 20
        dots = "." * max(10, int(dots_width / 18))
        doc.draw.text((left, doc.y), title, fill=INK, font=F12)
        doc.draw.text((left + text_width(doc.draw, title, F12) + 12, doc.y), dots, fill=MUTED, font=F12)
        doc.draw.text((right, doc.y), page, fill=INK, font=F12)
        doc.y += 78


def content(doc):
    doc.new_page()
    doc.heading("Resumen")
    doc.paragraph(
        "Este informe presenta el desarrollo del Caso práctico 2 de la Unidad 2 de Ciencia de Datos I, "
        "consistente en la creación de un CRUD/ORM nativo en Python para operar sobre la base de datos "
        "Sakila de MySQL. La solución utiliza programación orientada a objetos para representar entidades "
        "relacionales como países, ciudades, películas e inventario mediante clases de dominio, repositorios, "
        "controladores, servicios y un contexto de base de datos. El proyecto incorpora estructuras de datos "
        "como listas de entidades, diccionarios para caché y un historial de operaciones para evidenciar el "
        "uso de abstracciones propias de Python. Para facilitar la ejecución por los integrantes del equipo, "
        "se prepararon scripts de inicio para Mac, Linux y Windows que levantan MySQL en Docker, importan "
        "Sakila, verifican la conexión y abren el menú interactivo del CRUD. Además del flujo crear, leer, "
        "actualizar y eliminar, el trabajo incluye importación y exportación en CSV y JSON, diez consultas "
        "SQL, restricciones de integridad mediante unique constraints y métricas descriptivas fundamentales "
        "como media, rango, desviación estándar, varianza y covarianza. Los resultados demuestran una "
        "arquitectura modular y escalable, cercana al patrón ORM, donde los cambios del modelo pueden "
        "mantenerse separados de la conexión, la lógica de aplicación y la interfaz de consola. La propuesta "
        "fortalece la comprensión práctica de bases de datos relacionales, consumo programático de datos y "
        "organización de código reutilizable para proyectos de ciencia de datos."
    )
    doc.subheading("Palabras clave")
    doc.paragraph("CRUD, ORM, Sakila, MySQL, Python, estructuras de datos.", indent=False)

    doc.new_page()
    doc.heading("Abstract")
    doc.paragraph(
        "This report presents the development of Practical Case 2 for Data Science I, focused on building "
        "a native CRUD/ORM in Python over the MySQL Sakila sample database. The solution applies object-"
        "oriented programming to represent countries, cities, films and inventory as domain entities, while "
        "repositories, controllers, services and a database context organize the application flow. The project "
        "also uses Python data structures such as entity lists, dictionaries for cache management and an "
        "operation history. To support reproducible execution, the repository includes quickstart scripts for "
        "Mac, Linux and Windows that start MySQL with Docker, import Sakila, test the connection and launch "
        "the interactive CRUD menu. The work also includes CSV and JSON import/export, ten SQL queries, "
        "integrity constraints and descriptive metrics such as mean, range, standard deviation, variance and "
        "covariance. Overall, the solution demonstrates a modular structure that separates persistence, "
        "business flow and user interaction."
    )
    doc.subheading("Keywords")
    doc.paragraph("CRUD, ORM, Sakila, MySQL, Python, data structures.", indent=False)

    doc.new_page()
    doc.heading("Introducción")
    doc.paragraph(
        "La manipulación de datos en ciencia de datos requiere comprender tanto la estructura de los datos "
        "como los mecanismos usados para consultarlos, transformarlos y validarlos. En este caso práctico se "
        "utiliza Sakila, una base de datos de ejemplo de MySQL, para construir una solución que conecta Python "
        "con un sistema gestor relacional y permite ejecutar operaciones CRUD desde una interfaz de consola."
    )
    doc.paragraph(
        "La actividad responde al objetivo de crear un CRUD/ORM nativo basado en programación orientada a "
        "objetos y estructuras de datos. El enfoque ORM permite representar tablas como objetos de dominio y "
        "encapsular las operaciones SQL en repositorios y servicios, reduciendo la dependencia directa entre "
        "la interfaz de usuario y las consultas de base de datos (Fowler, 2002)."
    )

    doc.new_page()
    doc.heading("Marco de referencia")
    doc.paragraph(
        "Un CRUD agrupa las operaciones crear, leer, actualizar y eliminar, necesarias para administrar "
        "registros persistentes. En bases de datos relacionales, estas acciones se implementan mediante "
        "instrucciones SQL como INSERT, SELECT, UPDATE y DELETE. Oracle (s.f.) presenta Sakila como una base "
        "de datos de ejemplo útil para practicar relaciones entre tablas de un sistema de alquiler de películas."
    )
    doc.paragraph(
        "Python facilita este tipo de solución por su soporte para clases, dataclasses, listas, diccionarios "
        "y módulos reutilizables. La documentación oficial de Python describe las clases como un mecanismo "
        "para combinar datos y comportamiento dentro de una misma estructura (Python Software Foundation, s.f.). "
        "Docker, por su parte, permite ejecutar servicios como MySQL en contenedores reproducibles, lo que "
        "reduce diferencias entre equipos de trabajo (Docker, s.f.)."
    )

    doc.new_page()
    doc.heading("Descripción del caso práctico")
    doc.paragraph(
        "El proyecto gestiona las entidades country, city, film e inventory de Sakila. Estas entidades cubren "
        "los requisitos de países, ciudades, películas e inventario planteados en la asignación. La conexión "
        "se configura mediante variables de entorno y puede ejecutarse con MySQL local o con el contenedor "
        "Docker preparado para el proyecto."
    )
    doc.paragraph(
        "El alcance técnico incluye diez consultas SQL, operaciones CRUD, importación y exportación de datos "
        "en CSV y JSON, métricas descriptivas y restricciones de integridad para mejorar la calidad de los "
        "datos. La solución se orienta a demostrar dominio de estructuras de datos, separación de responsabilidades "
        "y consumo programático de una base de datos relacional."
    )

    doc.new_page()
    doc.heading("Arquitectura del sistema")
    for item in [
        "db.py: administra la conexión a MySQL y el manejo transaccional.",
        "dbcontext.py: centraliza repositorios, caché e historial de operaciones.",
        "models.py: define entidades y ModelCollection como lista de objetos.",
        "repositories.py: implementa CRUD genérico y repositorios concretos.",
        "controllers.py y services.py: separan el flujo de aplicación de la persistencia.",
        "structures.py: contiene caché de entidades e historial de consultas.",
        "metrics.py y reports.py: calculan media, rango, varianza, desviación y covarianza.",
        "import_export.py: permite importar y exportar datos CSV y JSON.",
        "main.py: ofrece el menú de consola para ejecutar la demostración.",
    ]:
        doc.bullet(item)

    doc.new_page()
    doc.heading("Implementación del CRUD/ORM")
    doc.paragraph(
        "La capa BaseRepository recibe una clase de modelo y construye consultas parametrizadas para crear, "
        "buscar por identificador, listar, actualizar y eliminar registros. Cada repositorio concreto hereda "
        "esa funcionalidad para una entidad específica. La interfaz de consola permite seleccionar países, "
        "ciudades, películas e inventario, introducir datos y observar el resultado devuelto como objeto."
    )
    doc.paragraph(
        "La implementación evita credenciales escritas directamente en el código y usa variables de entorno. "
        "Además, los scripts quickstart de Mac, Linux y Windows simplifican la preparación de MySQL/Sakila "
        "con Docker para que el equipo pueda repetir la demostración en diferentes computadoras."
    )

    doc.new_page()
    doc.heading("Pruebas y resultados")
    doc.paragraph(
        "Las pruebas unitarias disponibles validan estructuras de datos usadas por el proyecto. En la verificación "
        "local se ejecutó pytest sobre el Caso 2 y el resultado fue de dos pruebas aprobadas. También se comprobó "
        "la conexión a MySQL Sakila por Docker, obteniendo conexión exitosa, nombre de base de datos sakila y "
        "versión MySQL 8.0.46."
    )
    for item in [
        "Create: creación de países de prueba desde el menú.",
        "Read: búsqueda por ID y listado de entidades.",
        "Update: modificación de registros seleccionados.",
        "Delete: eliminación de registros de prueba.",
        "Métricas: cálculo descriptivo sobre longitud, tarifa y costo de películas.",
        "SQL: ejecución de diez consultas y script de unique constraints.",
    ]:
        doc.bullet(item)

    doc.new_page()
    doc.heading("Conclusiones")
    doc.paragraph(
        "La solución cumple el objetivo principal de implementar un CRUD/ORM nativo sobre Sakila usando POO "
        "y estructuras de datos. La separación entre contexto, modelos, repositorios, controladores y servicios "
        "facilita ampliar el sistema a nuevas tablas sin reescribir toda la aplicación. La automatización con "
        "Docker mejora la reproducibilidad para los integrantes del equipo y permite generar evidencias reales "
        "de ejecución."
    )
    doc.paragraph(
        "Como mejora futura, se recomienda ampliar las pruebas de integración, agregar validaciones de negocio "
        "más detalladas antes de insertar o actualizar datos y completar anexos con capturas finales de cada "
        "operación requerida por la rúbrica."
    )

    doc.new_page()
    doc.heading("Referencias")
    for ref in [
        "Docker. (s.f.). Docker documentation. https://docs.docker.com/",
        "Fowler, M. (2002). Patterns of enterprise application architecture. Addison-Wesley.",
        "Oracle. (s.f.). Sakila sample database. MySQL documentation. https://dev.mysql.com/doc/sakila/en/",
        "Python Software Foundation. (s.f.). The Python tutorial. https://docs.python.org/3/tutorial/",
    ]:
        doc.reference(ref)

    doc.new_page()
    doc.heading("Anexos")
    for item in [
        "Anexo A. Código fuente relevante: carpeta src/ del Caso práctico 2.",
        "Anexo B. Evidencias de ejecución: capturas de conexión, CRUD, métricas y pruebas.",
        "Anexo C. Scripts SQL: consultas y unique constraints incluidos en la carpeta sql/.",
        "Anexo D. Uso de agentes IA: apoyo en documentación, automatización y revisión.",
    ]:
        doc.bullet(item)


def main():
    doc = Document()
    cover(doc)
    toc(doc)
    content(doc)
    doc.save()


if __name__ == "__main__":
    main()

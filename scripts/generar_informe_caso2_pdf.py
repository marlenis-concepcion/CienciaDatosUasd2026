from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "caso_practico_2_sakila_crud_orm" / "docs" / "informe" / "Informe_Caso_2_Sakila_APA_UASD.pdf"

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN = 72
FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_SIZE = 12
LINE_HEIGHT = 24


def pdf_escape(text):
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", "")
    )


class PdfDoc:
    def __init__(self):
        self.pages = []
        self.current = []
        self.y = PAGE_HEIGHT - MARGIN

    def new_page(self):
        if self.current:
            self.pages.append(self.current)
        self.current = []
        self.y = PAGE_HEIGHT - MARGIN

    def finish(self):
        if self.current:
            self.pages.append(self.current)

    def add_text(self, text, x=MARGIN, size=FONT_SIZE, font=FONT):
        safe = pdf_escape(text)
        self.current.append(f"BT /{font} {size} Tf {x} {self.y:.2f} Td ({safe}) Tj ET")
        self.y -= LINE_HEIGHT

    def add_center(self, text, size=FONT_SIZE, font=FONT):
        width_estimate = len(text) * size * 0.25
        x = max(MARGIN, (PAGE_WIDTH - width_estimate) / 2)
        self.add_text(text, x=x, size=size, font=font)

    def paragraph(self, text, indent=True):
        width_chars = 86
        words = textwrap.wrap(text, width=width_chars)
        first = True
        for line in words:
            if self.y < MARGIN + LINE_HEIGHT:
                self.new_page()
            x = MARGIN + (36 if indent and first else 0)
            self.add_text(line, x=x)
            first = False
        self.y -= LINE_HEIGHT / 2

    def heading(self, text):
        if self.y < MARGIN + (LINE_HEIGHT * 2):
            self.new_page()
        self.add_text(text, font=FONT_BOLD)

    def bullet(self, text):
        for i, line in enumerate(textwrap.wrap(text, width=80)):
            if self.y < MARGIN + LINE_HEIGHT:
                self.new_page()
            prefix = "- " if i == 0 else "  "
            self.add_text(prefix + line, x=MARGIN + 18)


def build_content(pdf):
    pdf.add_center("Universidad Autonoma de Santo Domingo", font=FONT_BOLD)
    pdf.add_center("Facultad de Ingenieria y Arquitectura")
    pdf.add_center("Asignatura: INF-8237 Ciencia de Datos I")
    pdf.y -= LINE_HEIGHT * 4
    pdf.add_center("Caso practico 2", size=14, font=FONT_BOLD)
    pdf.add_center("CRUD/ORM nativo basado en POO y estructuras de datos en MySQL Sakila", font=FONT_BOLD)
    pdf.y -= LINE_HEIGHT * 3
    pdf.add_center("Equipo: UASDVirtual")
    pdf.add_center("Integrante: Marlenis Judith Concepcion Cuevas")
    pdf.add_center("Facilitador: [Completar]")
    pdf.add_center("Fecha: 4 de junio de 2026")
    pdf.new_page()

    pdf.heading("Resumen")
    pdf.paragraph(
        "Este informe presenta el desarrollo del Caso practico 2 de la Unidad 2 de Ciencia de Datos I, "
        "consistente en la creacion de un CRUD/ORM nativo en Python para operar sobre la base de datos "
        "Sakila de MySQL. La solucion utiliza programacion orientada a objetos para representar entidades "
        "relacionales como paises, ciudades, peliculas e inventario mediante clases de dominio, repositorios, "
        "controladores, servicios y un contexto de base de datos. El proyecto incorpora estructuras de datos "
        "como listas de entidades, diccionarios para cache y un historial de operaciones para evidenciar el "
        "uso de abstracciones propias de Python. Para facilitar la ejecucion por los integrantes del equipo, "
        "se prepararon scripts de inicio para Mac, Linux y Windows que levantan MySQL en Docker, importan "
        "Sakila, verifican la conexion y abren el menu interactivo del CRUD. Ademas del flujo crear, leer, "
        "actualizar y eliminar, el trabajo incluye importacion y exportacion en CSV y JSON, diez consultas "
        "SQL, restricciones de integridad mediante unique constraints y metricas descriptivas fundamentales "
        "como media, rango, desviacion estandar, varianza y covarianza. Los resultados demuestran una "
        "arquitectura modular y escalable, cercana al patron ORM, donde los cambios del modelo pueden "
        "mantenerse separados de la conexion, la logica de aplicacion y la interfaz de consola. La propuesta "
        "fortalece la comprension practica de bases de datos relacionales, consumo programatico de datos y "
        "organizacion de codigo reutilizable para proyectos de ciencia de datos."
    )

    pdf.heading("Introduccion")
    pdf.paragraph(
        "La manipulacion de datos en ciencia de datos requiere comprender tanto la estructura de los datos "
        "como los mecanismos usados para consultarlos, transformarlos y validarlos. En este caso practico "
        "se utiliza Sakila, una base de datos de ejemplo de MySQL, para construir una solucion que conecta "
        "Python con un sistema gestor relacional y permite ejecutar operaciones CRUD desde una interfaz de "
        "consola."
    )
    pdf.paragraph(
        "La actividad responde al objetivo de crear un CRUD/ORM nativo basado en programacion orientada a "
        "objetos y estructuras de datos. El enfoque ORM permite representar tablas como objetos de dominio "
        "y encapsular las operaciones SQL en repositorios y servicios, reduciendo la dependencia directa "
        "entre la interfaz de usuario y las consultas de base de datos (Fowler, 2002)."
    )

    pdf.heading("Marco de referencia")
    pdf.paragraph(
        "Un CRUD agrupa las operaciones create, read, update y delete, necesarias para administrar registros "
        "persistentes. En bases de datos relacionales, estas acciones se implementan mediante instrucciones "
        "SQL como INSERT, SELECT, UPDATE y DELETE. MySQL documenta Sakila como una base de datos de ejemplo "
        "util para practicar relaciones entre tablas de un sistema de alquiler de peliculas (Oracle, s.f.)."
    )
    pdf.paragraph(
        "Python facilita este tipo de solucion por su soporte para clases, dataclasses, listas, diccionarios "
        "y modulos reutilizables. La documentacion oficial de Python describe las clases como un mecanismo "
        "para combinar datos y comportamiento dentro de una misma estructura (Python Software Foundation, "
        "s.f.). Docker, por su parte, permite ejecutar servicios como MySQL en contenedores reproducibles, "
        "lo que reduce diferencias entre equipos de trabajo (Docker, s.f.)."
    )

    pdf.heading("Descripcion del caso practico")
    pdf.paragraph(
        "El proyecto gestiona las entidades country, city, film e inventory de Sakila. Estas entidades cubren "
        "los requisitos de paises, ciudades, peliculas e inventario planteados en la asignacion. La conexion "
        "se configura mediante variables de entorno y puede ejecutarse con MySQL local o con el contenedor "
        "Docker preparado para el proyecto."
    )

    pdf.heading("Arquitectura del sistema")
    for item in [
        "db.py: administra la conexion a MySQL y el manejo transaccional.",
        "dbcontext.py: centraliza repositorios, cache e historial.",
        "models.py: define entidades y ModelCollection como lista de objetos.",
        "repositories.py: implementa CRUD generico y repositorios concretos.",
        "controllers.py y services.py: separan el flujo de aplicacion de la persistencia.",
        "structures.py: contiene cache de entidades e historial de consultas.",
        "metrics.py y reports.py: calculan media, rango, varianza, desviacion y covarianza.",
        "import_export.py: permite importar y exportar datos CSV y JSON.",
        "main.py: ofrece el menu de consola para ejecutar la demostracion.",
    ]:
        pdf.bullet(item)
    pdf.y -= LINE_HEIGHT / 2

    pdf.heading("Implementacion del CRUD")
    pdf.paragraph(
        "La capa BaseRepository recibe una clase de modelo y construye consultas parametrizadas para crear, "
        "buscar por identificador, listar, actualizar y eliminar registros. Cada repositorio concreto hereda "
        "esa funcionalidad para una entidad especifica. La interfaz de consola permite seleccionar paises, "
        "ciudades, peliculas e inventario, introducir datos y observar el resultado devuelto como objeto."
    )

    pdf.heading("Pruebas y resultados")
    pdf.paragraph(
        "Las pruebas unitarias disponibles validan estructuras de datos usadas por el proyecto. En la "
        "verificacion local se ejecuto pytest sobre el Caso 2 y el resultado fue de dos pruebas aprobadas. "
        "Tambien se comprobo la conexion a MySQL Sakila por Docker, obteniendo conexion exitosa, nombre de "
        "base de datos sakila y version MySQL 8.0.46."
    )
    for item in [
        "Create: creacion de paises de prueba desde el menu.",
        "Read: busqueda por ID y listado de entidades.",
        "Update: modificacion de registros seleccionados.",
        "Delete: eliminacion de registros de prueba.",
        "Metricas: calculo descriptivo sobre longitud, tarifa y costo de peliculas.",
        "SQL: ejecucion de diez consultas y script de unique constraints.",
    ]:
        pdf.bullet(item)

    pdf.heading("Conclusiones")
    pdf.paragraph(
        "La solucion cumple el objetivo principal de implementar un CRUD/ORM nativo sobre Sakila usando POO "
        "y estructuras de datos. La separacion entre contexto, modelos, repositorios, controladores y servicios "
        "facilita ampliar el sistema a nuevas tablas sin reescribir toda la aplicacion. La automatizacion con "
        "Docker mejora la reproducibilidad para los integrantes del equipo y permite generar evidencias reales "
        "de ejecucion. Como mejora futura, se recomienda ampliar las pruebas de integracion y agregar validaciones "
        "de negocio mas detalladas antes de insertar o actualizar datos."
    )

    pdf.heading("Referencias")
    refs = [
        "Docker. (s.f.). Docker documentation. https://docs.docker.com/",
        "Fowler, M. (2002). Patterns of enterprise application architecture. Addison-Wesley.",
        "Oracle. (s.f.). Sakila sample database. MySQL documentation. https://dev.mysql.com/doc/sakila/en/",
        "Python Software Foundation. (s.f.). The Python tutorial. https://docs.python.org/3/tutorial/",
    ]
    for ref in refs:
        pdf.paragraph(ref, indent=False)

    pdf.heading("Anexos")
    for item in [
        "Anexo A. Codigo fuente relevante: carpeta src/ del Caso practico 2.",
        "Anexo B. Evidencias de ejecucion: capturas de conexion, CRUD, metricas y pruebas.",
        "Anexo C. Scripts SQL: consultas y unique constraints incluidos en la carpeta sql/.",
        "Anexo D. Uso de agentes IA: apoyo en documentacion, automatizacion y revision.",
    ]:
        pdf.bullet(item)


def write_pdf(pdf):
    pdf.finish()
    objects = []

    def add_obj(data):
        objects.append(data)
        return len(objects)

    font_obj = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>")
    bold_obj = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>")
    page_objs = []

    for index, commands in enumerate(pdf.pages, start=1):
        commands_with_page = list(commands)
        page_text = f"{index}"
        commands_with_page.append(
            f"BT /{FONT} 12 Tf {PAGE_WIDTH - MARGIN} {PAGE_HEIGHT - 42} Td ({page_text}) Tj ET"
        )
        stream = "\n".join(commands_with_page).encode("latin-1", errors="replace")
        content_obj = add_obj(f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream")
        page_obj = add_obj(
            f"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /{FONT} {font_obj} 0 R /{FONT_BOLD} {bold_obj} 0 R >> >> "
            f"/Contents {content_obj} 0 R >>"
        )
        page_objs.append(page_obj)

    kids = " ".join(f"{obj} 0 R" for obj in page_objs)
    pages_obj = add_obj(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_objs)} >>")

    fixed_objects = []
    for obj in objects:
        if isinstance(obj, str):
            fixed_objects.append(obj.replace("/Parent 0 0 R", f"/Parent {pages_obj} 0 R"))
        else:
            fixed_objects.append(obj)
    objects[:] = fixed_objects

    catalog_obj = add_obj(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>")

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("latin-1"))
        if isinstance(obj, bytes):
            output.extend(obj)
        else:
            output.extend(obj.encode("latin-1", errors="replace"))
        output.extend(b"\nendobj\n")

    xref_start = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF\n".encode("latin-1")
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(output)
    print(OUT)


def main():
    pdf = PdfDoc()
    build_content(pdf)
    write_pdf(pdf)


if __name__ == "__main__":
    main()

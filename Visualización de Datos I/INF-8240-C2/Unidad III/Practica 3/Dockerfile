# Dashboard web interactivo de Industrias Caribe (Unidad III)
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir pandas matplotlib seaborn streamlit plotly
COPY Practica_Produccion/produccion_dashboard.py Practica_Produccion/IndustriasCaribe_Produccion.csv Practica_Produccion/
COPY Practica_Reclamos/reclamos_dashboard.py Practica_Reclamos/IndustriasCaribe_Reclamos.csv Practica_Reclamos/
COPY dashboard_web/app.py dashboard_web/
EXPOSE 8501
CMD ["streamlit", "run", "dashboard_web/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--browser.gatherUsageStats=false"]

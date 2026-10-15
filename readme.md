# API Unificada - Proyectos y Actividades Académicas de Ingeniería

Plataforma de servicios backend desarrollada con **FastAPI** que integra, en una sola aplicación web modular, todos los proyectos, algoritmos y prácticas académicas de la materia de Lenguajes de Computación y Análisis de Algoritmos.

---

## 🚀 Módulos Disponibles

1. **Cadenas y Lenguajes Formales:** 
   - Operaciones sobre cadenas (concatenación, inversión, potencias).
   - Operaciones entre lenguajes (unión, intersección, diferencia, concatenación, complemento, clausura de Kleene y generación de universo de cadenas sobre un alfabeto $\Sigma$).
2. **Benchmarking de Algoritmos de Ordenamiento:** 
   - Comparativa de rendimiento computacional entre *Insertion Sort* ($O(n^2)$) y *Merge Sort* ($O(n \log n)$).
3. **Verificación del Último Teorema de Fermat:** 
   - Exploración computacional de la ecuación $x^n + y^n = z^n$ para valores dados.
4. **Analizador de Complejidad Algorítmica:** 
   - Detección automática de complejidad temporal asintótica (Big-O / Big-$\Omega$) a partir de código fuente y generación de reportes comentados.
5. **Búsqueda Informada en Grafos:** 
   - Algoritmos de búsqueda heurística *Greedy Search* y *A* Search* aplicados sobre estructuras de grafos personalizadas.
6. **Algoritmos P y NP:** 
   - Resolución de rutas óptimas mediante *Dijkstra* (Clase P), *TSP Voraz* (Aproximación polinómica) y *TSP Exacto* mediante Programación Dinámica (Clase NP con optimización de máscara de bits).

---

## 🛠️ Requisitos del Sistema

- **Python** (versión 3.10 o superior recomendada).
- Librerías necesarias:
  - `fastapi`
  - `uvicorn`
  - `pydantic`

---

## ⚙️ Instalación y Configuración

1. Clona o descarga el repositorio en tu equipo local.
2. Abre una terminal (como PowerShell en Windows) y navega hasta la carpeta del proyecto.
3. Instala las dependencias ejecutando (si no las tienes instaladas):
   ```bash
   pip install fastapi uvicorn pydantic
   ```

---

## ▶️ Ejecución del Servidor

Para evitar bloqueos de ejecución de ejecutables (`.exe`) en entornos con políticas estrictas de Windows, arranca la aplicación utilizando Uvicorn como módulo de Python:

```bash
python -m uvicorn main:app --reload
```

Una vez iniciado el servidor, verás una salida indicando que está activo en `http://127.0.0.1:8000`.

---

## 📖 Documentación Interactiva (Swagger UI)

Una vez que el servidor esté en marcha, abre tu navegador web favorito y accede a:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Desde ahí podrás interactuar directamente con cada uno de los endpoints de la API, enviar datos de prueba mediante JSON o archivos y visualizar los resultados en tiempo real.
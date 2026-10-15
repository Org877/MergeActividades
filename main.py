from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Set, Dict, Tuple, Optional
import itertools
import sys
import time
import random
import platform
import tracemalloc
from heapq import heappush, heappop

app = FastAPI(
    title="API Unificada - Proyectos y Actividades Académicas de Ingeniería",
    version="3.0.0",
    description="Plataforma completa que integra Autómatas, Ordenamiento, Fermat, Complejidad, Búsqueda Informada y Algoritmos P/NP."
)

sys.setrecursionlimit(10_000)

# =====================================================================
# 1. MODELOS Y ENDPOINTS DE CADENAS Y LENGUAJES
# =====================================================================

class Lenguaje(BaseModel):
    L: List[str] = []
    M: List[str] = []
    sigma: List[str] = []
    k: int = 0

@app.get("/cadenas/concatenar/{x}/{y}", tags=["Cadenas y Lenguajes"])
def concatenar_cadenas(x: str, y: str):
    return {"resultado": x + y}

@app.get("/cadenas/unir/{x}/{y}", tags=["Cadenas y Lenguajes"])
def unir_cadenas(x: str, y: str):
    return {"resultado": x + y}

@app.get("/cadenas/potencia/{x}", tags=["Cadenas y Lenguajes"])
def potencia_cadenas(x: str, k: int):
    if k <= 0:
        return {"resultado": ""}
    return {"resultado": x * k}

@app.get("/cadenas/invertir/{x}", tags=["Cadenas y Lenguajes"])
def invertir_cadenas(x: str):
    return {"resultado": x[::-1]}

def calcular_universo(sigma: Set[str], k: int) -> Set[str]:
    universo = {""}
    for longitud in range(1, k + 1):
        combinaciones = itertools.product(sigma, repeat=longitud)
        universo.update({"".join(cadena) for cadena in combinaciones})
    return universo

def kleene(L: set, k: int) -> set:
    resultado = {""}
    auxiliar = {""}
    for _ in range(k):
        C = {x + y for x in auxiliar for y in L}
        auxiliar = C
        resultado = resultado.union(auxiliar)
    return resultado

@app.post("/lenguajes/union", tags=["Cadenas y Lenguajes"])
def union_lenguajes(parametro: Lenguaje):
    L, M = set(parametro.L), set(parametro.M)
    resultado = L.union(M)
    return {"operacion": "union", "L": sorted(list(L)), "M": sorted(list(M)), "resultado": sorted(list(resultado))}

@app.post("/lenguajes/interseccion", tags=["Cadenas y Lenguajes"])
def interseccion_lenguajes(parametro: Lenguaje):
    L, M = set(parametro.L), set(parametro.M)
    resultado = L.intersection(M)
    return {"operacion": "interseccion", "L": sorted(list(L)), "M": sorted(list(M)), "resultado": sorted(list(resultado))}

@app.post("/lenguajes/diferencia", tags=["Cadenas y Lenguajes"])
def diferencia_lenguajes(parametro: Lenguaje):
    L, M = set(parametro.L), set(parametro.M)
    resultado = L.difference(M)
    return {"operacion": "diferencia", "L": sorted(list(L)), "M": sorted(list(M)), "resultado": sorted(list(resultado))}

@app.post("/lenguajes/concatenar", tags=["Cadenas y Lenguajes"])
def concatenar_lenguajes(parametro: Lenguaje):
    L, M = set(parametro.L), set(parametro.M)
    C = {x + y for x in L for y in M}
    return {"operacion": "concatenacion", "L": sorted(list(L)), "M": sorted(list(M)), "resultado": sorted(list(C))}

@app.post("/lenguajes/universo", tags=["Cadenas y Lenguajes"])
def generar_universo(parametro: Lenguaje):
    sigma = set(parametro.sigma)
    universo = calcular_universo(sigma, parametro.k)
    return {"operacion": "universo", "sigma": sorted(list(sigma)), "k": parametro.k, "resultado": sorted(list(universo))}

@app.post("/lenguajes/complemento", tags=["Cadenas y Lenguajes"])
def complemento_lenguajes(parametro: Lenguaje):
    sigma = set(parametro.sigma)
    universo = calcular_universo(sigma, parametro.k)
    L = set(parametro.L)
    resultado = universo.difference(L)
    return {"operacion": "complemento", "L": sorted(list(L)), "sigma": sorted(list(sigma)), "k": parametro.k, "resultado": sorted(list(resultado))}

@app.post("/lenguajes/kleene", tags=["Cadenas y Lenguajes"])
def clausura_kleene(parametro: Lenguaje):
    L = set(parametro.L)
    resultado = kleene(L, parametro.k)
    return {"operacion": "kleene", "L": sorted(list(L)), "k": parametro.k, "resultado": sorted(list(resultado))}


# =====================================================================
# 2. ALGORITMOS DE ORDENAMIENTO (Inserción vs Mezcla)
# =====================================================================

def insertion_sort(arr):
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
    return arr

def merge(izq, der):
    resultado = []
    i = j = 0
    n_izq, n_der = len(izq), len(der)
    while i < n_izq and j < n_der:
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    medio = len(arr) // 2
    return merge(merge_sort(arr[:medio]), merge_sort(arr[medio:]))

@app.get("/ordenamiento/probar", tags=["Benchmarking Ordenamiento"])
def probar_ordenamiento(n: int = 500):
    datos = [random.randint(1, n) for _ in range(n)]
    return {
        "tamaño": n,
        "insercion_ok": insertion_sort(datos.copy()) == sorted(datos),
        "mezcla_ok": merge_sort(datos.copy()) == sorted(datos)
    }


# =====================================================================
# 3. TEOREMA DE FERMAT (Actividad 10)
# =====================================================================

@app.get("/fermat/evaluar/{n}", tags=["Teorema de Fermat"])
def evaluar_fermat(n: int, limite: int = 20):
    encontrados = []
    for x in range(1, limite + 1):
        for y in range(1, limite + 1):
            for z in range(1, limite + 1):
                if x**n + y**n == z**n:
                    encontrados.append({"x": x, "y": y, "z": z, "n": n})
    return {"total_encontrados": len(encontrados), "soluciones": encontrados}


# =====================================================================
# 4. ANALIZADOR DE COMPLEJIDAD ALGORÍTMICA (Big-O / Big-Omega)
# =====================================================================

def detectar_complejidad_linea(linea):
    linea = linea.strip()
    if linea.startswith(("def", "if", "return", "=")):
        return "O(1)"
    if linea.startswith("for"):
        return "O(n)"
    if linea.startswith("while"):
        return "O(log n)"
    return "O(1)"

def detectar_complejidad_global(codigo):
    cantidad_for = codigo.count("for")
    if cantidad_for >= 2:
        return "O(n²)"
    if cantidad_for == 1:
        return "O(n)"
    if "while" in codigo:
        return "O(log n)"
    return "O(1)"

def obtener_big_omega(big_o):
    equivalencias = {"O(1)": "Ω(1)", "O(log n)": "Ω(1)", "O(n)": "Ω(n)", "O(n²)": "Ω(n²)"}
    return equivalencias.get(big_o, "Ω(1)")

def generar_codigo_comentado(codigo):
    lineas = codigo.splitlines()
    resultado, complejidades = [], []
    for linea in lineas:
        if not linea.strip():
            resultado.append("")
            continue
        complejidad = detectar_complejidad_linea(linea)
        complejidades.append(complejidad)
        resultado.append(f"{linea}    # {complejidad}")

    dominante = detectar_complejidad_global(codigo)
    big_omega = obtener_big_omega(dominante)
    resumen = f"\n'''\nRESUMEN DE COMPLEJIDAD\nComplejidades: {' + '.join(complejidades)}\nDominante: {dominante}\nBig-O: {dominante}\nBig-Omega: {big_omega}\n'''"
    resultado.append(resumen)
    return "\n".join(resultado)

@app.post("/complexity/analyze", tags=["Analizador de Complejidad"])
async def analyze_complexity(file: UploadFile = File(...)):
    codigo = (await file.read()).decode("utf-8")
    return {"archivo": file.filename, "codigo_comentado": generar_codigo_comentado(codigo)}

@app.post("/complexity/worst-case", tags=["Analizador de Complejidad"])
async def worst_case(file: UploadFile = File(...)):
    return {"big_o": detectar_complejidad_global((await file.read()).decode("utf-8"))}

@app.post("/complexity/best-case", tags=["Analizador de Complejidad"])
async def best_case(file: UploadFile = File(...)):
    codigo = (await file.read()).decode("utf-8")
    return {"big_omega": obtener_big_omega(detectar_complejidad_global(codigo))}


# =====================================================================
# 5. BÚSQUEDA INFORMADA EN GRAFOS (Greedy & A*)
# =====================================================================

class SearchRequestGraph(BaseModel):
    grafo: Dict[str, List[Tuple[str, float]]]
    origen: str
    destino: str
    limite_nodos: Optional[int] = None

@app.post("/search/greedy", tags=["Búsqueda Informada"])
def run_greedy(body: SearchRequestGraph):
    limite = body.limite_nodos if body.limite_nodos is not None else int(len(body.grafo) * 0.8)
    start_time = time.perf_counter()
    pq, visitados, max_mem, nodos_count = [], set(), 0, 0
    heappush(pq, (0, body.origen, [body.origen]))
    camino = [body.origen]

    while pq:
        max_mem = max(max_mem, len(pq))
        if nodos_count >= limite:
            break
        _, actual, camino = heappop(pq)
        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_count += 1

        if actual == body.destino:
            break

        for vecino, peso in body.grafo.get(actual, []):
            if vecino not in visitados:
                heappush(pq, (0, vecino, camino + [vecino]))

    end_time = time.perf_counter()
    return {
        "total_nodos_visitados": nodos_count,
        "solucion": camino[-1] == body.destino if camino else False,
        "ruta_solucion": camino,
        "t_n": round((end_time - start_time) * 1000, 4),
        "s_n": max_mem
    }

@app.post("/search/star", tags=["Búsqueda Informada"])
def run_star(body: SearchRequestGraph):
    limite = body.limite_nodos if body.limite_nodos is not None else int(len(body.grafo) * 0.8)
    start_time = time.perf_counter()
    pq, g_costs, visitados, max_mem, nodos_count = [], {body.origen: 0}, set(), 0, 0
    heappush(pq, (0, 0, body.origen, [body.origen]))
    camino = [body.origen]

    while pq:
        max_mem = max(max_mem, len(pq))
        if nodos_count >= limite:
            break
        f, g, actual, camino = heappop(pq)
        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_count += 1

        if actual == body.destino:
            break

        for vecino, peso in body.grafo.get(actual, []):
            nuevo_g = g + peso
            if vecino not in g_costs or nuevo_g < g_costs[vecino]:
                g_costs[vecino] = nuevo_g
                heappush(pq, (nuevo_g, nuevo_g, vecino, camino + [vecino]))

    end_time = time.perf_counter()
    return {
        "total_nodos_visitados": nodos_count,
        "solucion": camino[-1] == body.destino if camino else False,
        "ruta_solucion": camino,
        "t_n": round((end_time - start_time) * 1000, 4),
        "s_n": max_mem
    }


# =====================================================================
# 6. ALGORITMOS P Y NP (Dijkstra y TSP)
# =====================================================================

class SyntheticGraphReq(BaseModel):
    num_nodes: int
    weighted: Optional[bool] = True

class MatrixSearchReq(BaseModel):
    graph: List[List[float]]
    start_node: int
    end_node: int

class TspReq(BaseModel):
    graph: List[List[float]]
    start_node: Optional[int] = 0

@app.post("/api/graph/generate", tags=["Algoritmos P y NP"])
def generate_synthetic_graph_endpoint(req: SyntheticGraphReq):
    if req.num_nodes < 2:
        raise HTTPException(status_code=400, detail="Mínimo 2 nodos.")
    graph = [[0.0] * req.num_nodes for _ in range(req.num_nodes)]
    for i in range(req.num_nodes):
        for j in range(req.num_nodes):
            if i != j and j > i:
                w = float(random.randint(1, 100)) if req.weighted else 1.0
                graph[i][j] = graph[j][i] = w
    return {"num_nodes": req.num_nodes, "graph": graph}

@app.post("/api/algorithm/dijkstra", tags=["Algoritmos P y NP"])
def dijkstra_endpoint(req: MatrixSearchReq):
    tracemalloc.start()
    t0 = time.perf_counter()
    n = len(req.graph)
    distances = {i: float('inf') for i in range(n)}
    distances[req.start_node] = 0.0
    pq = [(0.0, req.start_node)]
    paths = {req.start_node: [req.start_node]}
    nodes_visited = 0

    while pq:
        d, u = heappop(pq)
        nodes_visited += 1
        if u == req.end_node:
            break
        if d > distances[u]:
            continue
        for v in range(n):
            w = req.graph[u][v]
            if w > 0 and u != v:
                nd = d + w
                if nd < distances[v]:
                    distances[v] = nd
                    paths[v] = paths[u] + [v]
                    heappush(pq, (nd, v))

    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "Dijkstra (P)",
        "result": {
            "execution_time_ms": round((t1 - t0) * 1000, 4),
            "memory_consumed_kb": round(peak / 1024, 2),
            "nodes_visited": nodes_visited,
            "path_cost": distances[req.end_node] if distances[req.end_node] != float('inf') else -1,
            "path": paths.get(req.end_node, [])
        }
    }

@app.post("/api/algorithm/tsp-greedy", tags=["Algoritmos P y NP"])
def tsp_greedy_endpoint(req: TspReq):
    tracemalloc.start()
    t0 = time.perf_counter()
    n = len(req.graph)
    unvisited = set(range(n))
    current = req.start_node
    unvisited.remove(current)
    path, total_cost, nodes_visited = [current], 0.0, 1

    while unvisited:
        next_node = min(unvisited, key=lambda node: req.graph[current][node])
        total_cost += req.graph[current][next_node]
        current = next_node
        unvisited.remove(current)
        path.append(current)
        nodes_visited += 1

    total_cost += req.graph[current][req.start_node]
    path.append(req.start_node)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "TSP Voraz (Aproximación P)",
        "result": {
            "execution_time_ms": round((t1 - t0) * 1000, 4),
            "memory_consumed_kb": round(peak / 1024, 2),
            "nodes_visited": nodes_visited,
            "path_cost": total_cost,
            "path": path
        }
    }

@app.post("/api/algorithm/tsp-exact", tags=["Algoritmos P y NP"])
def tsp_exact_endpoint(req: TspReq):
    n = len(req.graph)
    if n > 15:
        raise HTTPException(status_code=400, detail="El TSP exacto está limitado a un máximo de 15 nodos.")
    
    tracemalloc.start()
    t0 = time.perf_counter()
    memo = {}
    nodes_visited = 0

    def visit(mask, pos):
        nonlocal nodes_visited
        nodes_visited += 1
        if mask == (1 << n) - 1:
            return req.graph[pos][0], [pos, 0]
        if (mask, pos) in memo:
            return memo[(mask, pos)]

        ans, best_path = float('inf'), []
        for nxt in range(n):
            if not (mask & (1 << nxt)) and req.graph[pos][nxt] > 0:
                nc, np_path = visit(mask | (1 << nxt), nxt)
                cost = req.graph[pos][nxt] + nc
                if cost < ans:
                    ans = cost
                    best_path = [pos] + np_path
        memo[(mask, pos)] = (ans, best_path)
        return ans, best_path

    min_cost, path = visit(1, 0)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algorithm": "TSP Exacto - Programación Dinámica (NP)",
        "result": {
            "execution_time_ms": round((t1 - t0) * 1000, 4),
            "memory_consumed_kb": round(peak / 1024, 2),
            "nodes_visited": nodes_visited,
            "path_cost": min_cost,
            "path": path
        }
    }

# =====================================================================
# ENDPOINT RAÍZ
# =====================================================================

@app.get("/")
def root():
    return {
        "mensaje": "¡Servidor unificado activo con éxito!",
        "documentacion_interactiva": "/docs",
        "modulos_disponibles": [
            "Cadenas y Lenguajes Formales",
            "Benchmarking de Ordenamiento (Inserción vs Mezcla)",
            "Teorema de Fermat",
            "Analizador de Complejidad (Big-O / Big-Omega)",
            "Búsqueda Informada en Grafos (Greedy y A*)",
            "Algoritmos P y NP (Dijkstra, TSP Voraz y TSP Exacto)"
        ]
    }
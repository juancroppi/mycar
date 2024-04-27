from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from models.cars import Marca, Modelo
import os
import json
from db_connect import connect_to_database
from typing import List, Optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar los datos desde el archivo JSON
with open('data.json') as f:
    datos = json.load(f)
    marcas = datos['marcas']

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(os.getcwd(), "index.html")) as f:
        html_content = f.read()
    return html_content

# Ruta para obtener todas las marcas
@app.get("/obtenerMarcas", response_model=List[Marca])
def obtener_marcas():
    try:
        connection, cur = connect_to_database()

        if connection and cur:
            cur.execute('SELECT * FROM marcas')

            marcas = []
            for reg in cur.fetchall():
                marca = Marca(id_marca=reg[0], nombre=reg[1])
                marcas.append(marca)

            connection.close()
            return marcas

        else:
            return None

    except Exception as e:
        print("Error al obtener las marcas:", e)
        return None


# Ruta para obtener todos los modelos de una marca
@app.get("/obtenerModelosPorMarca/{id_marca}", response_model=List[Modelo])
def obtener_modelos_por_marca(id_marca: int, precioDesde: Optional[float] = None, precioHasta: Optional[float] = None):
    try:
        connection, cur = connect_to_database()
        if connection and cur:
            if id_marca == 0:
                if precioHasta > 0:
                    cur.execute('SELECT * FROM modelos WHERE precio >= %(precioDesde)s AND precio < %(precioHasta)s', {'precioDesde': precioDesde, 'precioHasta': precioHasta})
                else:
                    cur.execute('SELECT * FROM modelos WHERE precio >= %(precioDesde)s', {'precioDesde': precioDesde})
            else:
                if precioHasta > 0:
                    cur.execute('SELECT * FROM modelos WHERE id_marca = %(id_marca)s AND precio >= %(precioDesde)s AND precio < %(precioHasta)s', {'id_marca': id_marca, 'precioDesde': precioDesde, 'precioHasta': precioHasta})
                else:
                    cur.execute('SELECT * FROM modelos WHERE id_marca = %(id_marca)s AND precio >= %(precioDesde)s', {'id_marca': id_marca, 'precioDesde': precioDesde})

            modelos = []
            for reg in cur.fetchall():
                id = reg[2]
                marc = obtener_marca(id)
                modelo = Modelo(id_modelo=reg[0], nombre=reg[1], id_marca=reg[2], descripcion=reg[3], precio=reg[4], marca=marc)
                modelos.append(modelo)

            connection.close()
            return modelos

        else:
            return None

    except Exception as e:
        print("Error al obtener los modelos:", e)
        return None

# Ruta para obtener todos los modelos de una marca
@app.get("/obtenerMarca/{id_marca}", response_model=Marca)
def obtener_marca(id_marca: int):
    try:
        connection, cur = connect_to_database()

        if connection and cur:
            cur.execute('SELECT * FROM marcas WHERE id = %(id_marca)s', {'id_marca': id_marca})

            marca = cur.fetchone()
            connection.close()
            if marca:
                return Marca(id_marca=marca[0], nombre=marca[1])
            else: 
                return None

        else:
            return None

    except Exception as e:
        print("Error al obtener la marca:", e)
        return None


@app.get("/obtenerNombreMarca/{id_marca}", response_model=str)
def obtener_nombre_marca(id_marca: int):
    try:
        connection, cur = connect_to_database()

        if connection and cur:
            cur.execute('SELECT nombre FROM marcas WHERE id = %(id_marca)s', {'id_marca': id_marca})

            nombre = cur.fetchone()

            connection.close()
            if nombre:
                return nombre[0]
            else: 
                return ""

        else:
            return None

    except Exception as e:
        print("Error al obtener el nombre:", e)
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
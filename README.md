
# Backend (Electrónica General)

> **Advertencia:** Trabajo en progreso.

Sistema de reconocimiento de placas.

## Instalación

1. Descarge e instale Python.
2. Clone este repositorio.
3. Cree un entorno virtual dentro del directorio del proyecto: `python -m venv --upgrade-deps .`.
4. Active el entorno virtual (ejecutando el archivo correspondiente en `bin`), revise <https://docs.python.org/es/3/tutorial/venv.html>.
5. Instale las dependencias: `pip install -r requeriments.txt`.

## Uso

Ejecute el _script_ principal con: `python main.py`.

Ejecute la variante: `python main.py debug` si desea ver el proceso de forma detallada.

## Solución de problemas

Si no puede ver las imágenes asegúrese de que su instalación de Python tenga TkInter instalado, o de lo contrario, instale PyQt6.

Hasta el momento ha sido desarrollado desde Linux, aún no se ha probado en Windows. _PRs_ en GitHub bienvenidos.

La instalación de las dependencias requiere alrededor de **1.2GiB** de espacio disponible, además, la primera vez que ejecute el programa, descargará alrededor de **1GiB** con los datos de reconocimiento de texto.

## Créditos

- <https://www.geeksforgeeks.org/automatic-license-number-plate-recognition-system/>

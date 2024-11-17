# Parking (Parqueadero)

> **Advertencia:** Trabajo en progreso.

Sistema de parqueadero automatizado, con reconocimiento de texto de la placa incluido.

## Inicio rápido

El sistema de construcción utiliza [Hatch](https://hatch.pypa.io), por lo que necesitará tener instalada una versión de Python reciente, luego ejecute:

```sh
pip install hatch
```

Actualmente se proveen dos comandos:

- `hatch run app`: Para ejecutar el servidor web.
- `hatch run tool:format`: Para formatear el código Python.

Probablemente desee utilizar el primer comando si solo desea ver el proyecto.

Si desea ayudar en el desarrollo necesitará instalar [Bun](https://bun.sh). Luego ejecute el siguiente comando:

```sh
bun install
```

Luego haga los cambios respectivos, y antes de confirmar sus cambios ejecute `hatch run tool:all` y solucione los errores (si los hay).

## Configuración

El servidor se puede configurar utilizando las siguientes variables de entorno:

- `FLASK_DEBUG`: Acepta los valores `0` y `1`, el cual alterna el modo de depuración para el servidor.
- `CAPTURE_URL`: Una URL que responde con una imagen en formato JPEG, utilizado para obtener imágenes de la entrada del parqueadero.
- `PLATES_DIR`: Ruta donde se guardarán las fotos de las placas, el directorio debe existir.

## Información adicional

La instalación de las dependencias requiere alrededor de **1.2GiB** de espacio disponible, además, la primera vez que ejecute el programa, descargará alrededor de **1GiB** con los datos para el reconocimiento de texto.

## Créditos

- <https://www.geeksforgeeks.org/automatic-license-number-plate-recognition-system/>

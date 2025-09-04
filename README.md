<br/>
<p align="center">
  <a href="https://github.com/hadessoft/Triz2ngPAWS">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Triz2ngPAWS</h3>

  <p align="center">
    por Tranqui69
    <br/>
    <br/>
    <a href="https://github.com/hadessoft/Triz2ngPAWS"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/hadessoft/Triz2ngPAWS">View Demo</a>
    .
    <a href="https://github.com/hadessoft/Triz2ngPAWS/issues">Report Bug</a>
    .
    <a href="https://github.com/hadessoft/Triz2ngPAWS/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/hadessoft/Triz2ngPAWS/total) ![Contributors](https://img.shields.io/github/contributors/hadessoft/Triz2ngPAWS?color=dark-green) ![Issues](https://img.shields.io/github/issues/hadessoft/Triz2ngPAWS) ![License](https://img.shields.io/github/license/hadessoft/Triz2ngPAWS) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

![Screen Shot](images/screenshot.png)

Triz2ngPAWS versión 1.0 250904 (c) 2025 Tranqui69

Triz2ngPAWS es un script de Python 3.x que permite generar un acrhivo .txp utilizado por ngPAWS de Uto a partir de un fichero creado con la utilidad de escritorio Trizbort. Esta herramienta solo trata de ayudar en el diseño inicial de las aventuras de texto y puede servir como referencia a la hora de iniciarse en el mundo del desarrollo.

La herramienta está en una fase aún temprana de desarrollo y puede presentar errores.

Si lo que buscas es convertir de Trizbort a DAAD tu herramienta es Triz2DAAD de Pedro Fernández (aka: rockersuke)

## Built With

Pyhton 3.x y Visual Studio Code

## Getting Started

Instala Python, clona el repositorio y ejecuta el archivo, se generará un archivo *.txp con el mismo nombre que contendrá una base de datos de inicio con los parámetros deseados.

### Prerequisites

Python 3.x

### Installation

Clone the repo
https://github.com/hadessoft/Triz2ngPAWS

## Usage

py triz2ngPAWS.py archive.trizbort

## Roadmap

See the [open issues](https://github.com/hadessoft/Triz2ngPAWS/issues) for a list of proposed features (and known issues).

## Versiones

- 0.0.2b11

    Versión inicial.

- 0.0.2b12
    
    Corregido un error que hacía que las variables de las localidades apareciesen en blanco. (Se tomaba como referencia su descripión y no su nombre)
    Corregido un error en la codificación de las variables de objetos con caracteres especiales.
    Añadido un contador de control para que no se repitan las variables de localidades si estas tienen el mismo nombre.

- 0.0.2b13    

    Corregido un error en la codificación de las variables las localidades con caracteres especiales.

- 0.0.3b1

    Añadido el segmento de /CTL que aparecía en blanco (al parecer no es opcional)
    Añadida la cabecera /OTX que faltaba en la descripción de los objetos
    Se ha añadido un código al PROCESS 1 que mueve automáticamente al jugador a la localidad marcada como Inicio o, en su defecto a la primera que no es un contenedor. 
    Los objetos deberán definirse como NOMBRE ADJETIVO o NOMBRE a secas. Haciendo esto se añadirán al vocabulario en la zona designada para ello.
    [ ] Falta añadir comprobación de objetos duplicados
    [x] Aparece un error al compilar con el pronombre LA (?¿) el compilador txtpaws lo marca como duplicado.

- 0.0.4b1

    Solucionado el error del pronombre, lo causaba una localidad llamada A, al añadir el prefijo l de localidad, la confundía con el pronombre. Ahora los prefijos de localidad serán "loc_" y los de objetos "obj_" para mejorar su lectura y evitar duplicidades.

- 0.0.5b1

    Cambiada la funcion de sustitución de carácteres acentuados para evitar usar librerías externas innecesarias.
    Corregido un problema que asignaba los objetos a una localidad inferior a la que les correspondía.
    Añadida comprobación para evitar que las descripciones de las localidades queden en blanco. Ahora, si no hay descripción se añade el nombre de la localidad.

- 1.0

    Correción en la lectura de caracteres UTF8.


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/hadessoft/Triz2ngPAWS/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/hadessoft/Triz2ngPAWS/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Licencia

Distributed under the MIT License. See [LICENSE](https://github.com/hadessoft/Triz2ngPAWS/blob/main/LICENSE.md) for more information.

## Autores

* **Tranqui69** - *Tranquilino Rodríguez* - [Tranqui69](https://twitter.com/tranqui69) - *Diseño incial*

## Agradecimientos

* [Club de Aventuras AD](https://caad.club/)
* [Trizbort](https://www.trizbort.com/)
* [rockersuke](https://github.com/rockersuke/)
* [Utodev](https://github.com/Utodev/ngPAWS/)


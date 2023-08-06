# PyCourse
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
 [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
 [![PyPI version](https://badge.fury.io/py/pysupuesto.svg)](https://pypi.org/project/pysupuesto/) 
 [![Twitter](https://img.shields.io/twitter/follow/matog?style=social)](https://twitter.com/mato)

### DOCUMENTANCIÓN EN ELABORACIÓN

Modulo de python que permite procesar información de determinas instancias de evaluación (previamente configuradas) y calcular si un alumno aprobó el curso o no.

Los cursos (fundamentalmente los unversitarios) pueden tener diferentes instancias de evaluación, cada una con sus requerimientos para aprobarlas.

Supongamos un curso que tiene 2 parciales, cada uno con su recuperatorio, pero el primer parcial se aprueba con 4, su recuperatorio con 4, pero el segundo parcial se aprueba con 6 y su recuperatorio con 7.

Configurando un sencillo `dictionary` de python con esta información y con los campos donde se almacenan los resultados de cada instancia, el módulo calcula si el alumno aprobó o no el curso, y en caso de haber aprobado, calcula el promedio con las notas de los examenes (parcial o recuperatorio) aprobados. 


## Requerimientos

- Python 3.8
- pandas=>1.3.3

## Modo de uso

### Instalación

	pip install pycourse

### Import

	import pycourse
	
### Configuración del `dictionary`de examenes y notas mínimas
 
	dict = {
            primer_instancia:{
                               'primer_parcial' : 4,
                               'primer_recuperatorio' : 4
                               },
            segunda_instancia:{
                               'segundo_parcial' : 4,
                               'segundo_recuperatorio' : 4
                               },
            tercer_instancia: {
                               'solo_un_examen' : 7
            }
                               
    }
	
El uso es relativamente sencillo. Sólo tener en cuenta que los nombres dentro de las `n` instancias corresponden a los nombres de las columnas donde se encuentran las notas de los alumnos de ese examen.

Luego, se llama a la función:

`approve (nombre_del_df, dict)`

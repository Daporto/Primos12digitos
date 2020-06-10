# Primos12digitos con mpi y cluster

Travis CI: [![Build Status](https://travis-ci.org/ocramz/docker.openmpi.svg?branch=master)](https://travis-ci.org/ocramz/docker.openmpi)

Este programa encuentra todos los número primos de 12 digitos implementando un sistema de cluster junto con la libreria mpi, permitiendo así la ejecución de procesos en paralelo.

## Intrucciones para la ejecucion del programa

1. Una vez haya clonado el repositorio y se encuentre dentro del mismo, debera instalar la imagen de docker ejecutando el siguiente comando:

```
docker pull daporto/openmpi_y_cluster:latest
```

2. Deberemos ejecutar el siguiente comando, el cual crea un contenedor `mpi_head` y el numero de contenedores de tipo `mpi_node` que deseemos (este proceso puede tardar un poco), en este caso el número de `mpi_node` puede ser 4 por ejemplo:

```
docker-compose scale mpi_head=1 mpi_node=4
```
3. Una vez todos los contenedores esten corriendo, deberemos ejecutar el siguiente comando para conectarnos al contenedor `mpi_head`y correr nuestro programa que en nuestro caso sera primos12d.py. cabe mencionar que en el comando se utiliza de ejemplo 5 procesos para correr el programa, pero este valor puede ser cambiado por el valor que se desee:

```
    docker-compose exec --user mpirun --privileged mpi_head mpirun -n 5 python3 /home/mpirun/mpi4py_benchmarks/primos12d.py
    ----------------------------------------- ----------- --------------------------------------------------
    1.                                        2.          3.
```

## Distribución del trabajo en el algoritmo

Para distribuir el trabajo entre los n procesos, Creamos varias funciones que nos calculaban en que rango de números debía hacer la búsqueda de primos cada proceso, de tal forma que la carga entre los procesos sea lo mas balanceada posible y de esta manera optimizar los tiempo de búsqueda.

## Credits

Para la implementación del cluster y los contenedores se utilizo la solución alojada en: https://github.com/oweidner/docker.openmpi.git

#!/usr/bin/env python3
"""
Generador de ejemplares aleatorios para el problema de bin packing.

Cada ejemplar es un archivo .csv con una pieza por renglón. La capacidad
de cada contenedor es 1, y los tamaños cumplen 0 < a_i < 1.

Uso:
    python generar_ejemplar.py 100
"""

import argparse
import csv
import os
import random
import sys

"""Genera una lista de n tamaños uniformes en el rango [minimo, maximo]."""
def generar_piezas(n, minimo, maximo, decimales, rng):
    piezas = []
    while len(piezas) < n:
        tam = round(rng.uniform(minimo, maximo), decimales)
        if 0 < tam < 1:
            piezas.append(tam)
    return piezas

"""Escribe el .csv con codificacion utf-8."""
def escribir_csv(ruta, piezas, decimales, semilla):
    total = sum(piezas)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        f.write(f"# piezas: {len(piezas)}\n")
        f.write(f"# semilla: {semilla}\n")
        f.write(f"# suma de tamaños: {total:.{decimales}f}\n")
        escritor = csv.writer(f)
        escritor.writerow(["pieza", "tamaño"])
        for i, tam in enumerate(piezas, start=1):
            escritor.writerow([i, f"{tam:.{decimales}f}"])


"""Si la ruta ya existe, devuelve una con sufijo (_1, _2, ...) que no exista"""
def ruta_disponible(ruta):
    if not os.path.exists(ruta):
        return ruta
    base, ext = os.path.splitext(ruta)
    k = 1
    while os.path.exists(f"{base}_{k}{ext}"):
        k += 1
    return f"{base}_{k}{ext}"


def leer_argumentos():
    p = argparse.ArgumentParser(
        description="=== Genera un ejemplar aleatorio de bin packing en formato .csv ==="
    )
    p.add_argument("n", type=int, help="número de piezas del ejemplar")
    p.add_argument("-o", "--salida",
                   help="nombre del archivo de salida (por omisión: ejemplar_n<N>.csv)")
    p.add_argument("--semilla", type=int, default=None,
                   help="semilla para reproducir el mismo ejemplar")
    p.add_argument("--min", type=float, default=0.01, dest="minimo",
                   help="tamaño mínimo de una pieza (por default 0.01)")
    p.add_argument("--max", type=float, default=0.99, dest="maximo",
                   help="tamaño máximo de una pieza (por omisión 0.99)")
    p.add_argument("--decimales", type=int, default=4,
                   help="decimales con los que se guardan los tamaños (por default 4)")
    args = p.parse_args()

    if args.n <= 0:
        p.error("el número de piezas debe ser un entero positivo")
    if not (0 < args.minimo <= args.maximo < 1):
        p.error("se necesita 0 < min <= max < 1")
    if args.decimales < 1:
        p.error("se necesita al menos 1 decimal")
    if args.minimo < 10 ** (-args.decimales):
        p.error("min es demasiado chico para el número de decimales elegido")
    return args


def main():
    args = leer_argumentos()
    semilla = args.semilla
    if semilla is None:
        semilla = random.SystemRandom().randrange(2**32) # para tener una semilla explicita reproducible
    rng = random.Random(semilla)
    piezas = generar_piezas(args.n, args.minimo, args.maximo, args.decimales, rng)

    salida = ruta_disponible(args.salida or f"ejemplar_n{args.n}.csv")
    escribir_csv(salida, piezas, args.decimales, semilla)

    print(f"Ejemplar guardado en {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

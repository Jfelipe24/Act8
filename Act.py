import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime

estructura = {}
jurados_por_mesa = {}
votantes = []
asistencias = []
resultados = []
cedulas_jurados = set()
cedulas_votantes = set()

def es_entero_positivo(valor):
    try:
        return int(valor) > 0
    except:
        return False


import flet as ft
import itertools


def obtener_prefijos(cadena):
    return [cadena[:i+1] for i in range(len(cadena))] + ["ε"]

def obtener_sufijos(cadena):
    return [cadena[i:] for i in range(len(cadena))] + ["ε"]

def obtener_subcadenas(cadena):
    n = len(cadena)
    subcadenas = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            subcadenas.add(cadena[i:j])
    return list(subcadenas) + ["ε"]



def kleene(alfabeto, longitud):
    resultado = ["ε"]
    for i in range(1, longitud + 1):
        for p in itertools.product(alfabeto, repeat=i):
            resultado.append("".join(p))
    return resultado


def positiva(alfabeto, longitud):
    resultado = []
    for i in range(1, longitud + 1):
        for p in itertools.product(alfabeto, repeat=i):
            resultado.append("".join(p))
    return resultado


def main(page: ft.Page):

    page.title = "Operaciones sobre Lenguajes"
    page.scroll = "adaptive"
    page.window_width = 700


    entrada_cadena = ft.TextField(label="Ingrese una cadena", width=300)

    resultado_cadena = ft.Text(size=14)

    texto_guardar = ""

    def calcular_cadena(e):
        nonlocal texto_guardar

        cadena = entrada_cadena.value

        if not cadena:
            resultado_cadena.value = "Ingrese una cadena válida"
            page.update()
            return

        prefijos = obtener_prefijos(cadena)
        sufijos = obtener_sufijos(cadena)
        subcadenas = obtener_subcadenas(cadena)

        texto = f"Resultados para: {cadena}\n\n"

        texto += "Prefijos:\n"
        texto += ", ".join(prefijos) + "\n\n"

        texto += "Sufijos:\n"
        texto += ", ".join(sufijos) + "\n\n"

        texto += "Subcadenas:\n"
        texto += ", ".join(subcadenas)

        texto_guardar = texto
        resultado_cadena.value = texto

        page.update()

    def guardar(e):
        if texto_guardar:
            with open("resultados.txt", "w", encoding="utf-8") as f:
                f.write(texto_guardar)

            resultado_cadena.value += "\n\nResultados guardados en resultados.txt"
            page.update()

    entrada_alfabeto = ft.TextField(label="Alfabeto (ej: a,b)", width=300)
    entrada_longitud = ft.TextField(label="Longitud máxima", width=150)

    resultado_kleene = ft.Text(size=14)

    def calcular_kleene(e):

        alfabeto = entrada_alfabeto.value.split(",")
        longitud = int(entrada_longitud.value)

        res = kleene(alfabeto, longitud)

        resultado_kleene.value = "Σ*:\n\n" + ", ".join(res)

        page.update()

    def calcular_positiva(e):

        alfabeto = entrada_alfabeto.value.split(",")
        longitud = int(entrada_longitud.value)

        res = positiva(alfabeto, longitud)

        resultado_kleene.value = "Σ+:\n\n" + ", ".join(res)

        page.update()


    seccion_cadenas = ft.Container( #Cadenas
        content=ft.Column(
            [
                ft.Text("Operaciones sobre Cadenas", size=20, weight="bold"),
                entrada_cadena,
                ft.Row(
                    [
                        ft.ElevatedButton("Calcular", on_click=calcular_cadena),
                        ft.ElevatedButton("Guardar resultados", on_click=guardar),
                    ]
                ),
                resultado_cadena,
            ]
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.GREY_200
    )


    seccion_kleene = ft.Container( #Kleene
        content=ft.Column(
            [
                ft.Text("Cerradura de Kleene y Positiva", size=20, weight="bold"),
                entrada_alfabeto,
                entrada_longitud,
                ft.Row(
                    [
                        ft.ElevatedButton("Calcular Σ*", on_click=calcular_kleene),
                        ft.ElevatedButton("Calcular Σ+", on_click=calcular_positiva),
                    ]
                ),
                resultado_kleene,
            ]
        ),
        padding=20,
        border_radius=10,
        bgcolor=ft.Colors.GREY_200
    )


    page.add(

        ft.Text(
            "Práctica 1 - Operaciones Básicas sobre Lenguajes",
            size=26,
            weight="bold"
        ),

        ft.Divider(),

        seccion_cadenas,

        ft.Divider(),

        seccion_kleene
    )


ft.app(target=main)
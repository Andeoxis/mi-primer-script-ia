import os
import json
import time
import random
from google import genai

# ====================================================
# 📦 TUS FUNCIONES (TUS NUEVAS CAJAS DE HERRAMIENTAS)
# ====================================================

def obtener_saludo_dinamico():
    """Revisa la hora del hardware y devuelve el saludo correspondiente."""
    hora_actual = time.localtime().tm_hour
    if hora_actual < 12:
        return "¡Buenos días"
    elif hora_actual < 19:
        return "¡Buenas tardes"
    else:
        return "¡Buenas noches"

def limpiar_consola_con_banner(saludo, nombre):
    """Limpia la pantalla y dibuja la interfaz limpia del chat."""
    os.system('cls')
    print("====================================================")
    print(f"{saludo}, {nombre}! Entorno de chat listo.")
    print("Para borrar la memoria escribe: limpiar")
    print("Para cerrar el programa escribe: salir")
    print("====================================================\n")


# ====================================================
# 🚀 ENTORNO PRINCIPAL (EL FLUJO DE TU PROGRAMA)
# ====================================================

# 1. Intentar leer los datos locales de tu JSON de forma segura
try:
    with open("perfil_usuario.json", "r", encoding="utf-8") as archivo:
        datos_perfil = json.load(archivo)
except FileNotFoundError:
    print("⚠️ ¡Advertencia! No se encontró 'perfil_usuario.json'. Usando perfil temporal.")
    datos_perfil = {
        "nombre": "Estudiante",
        "edad": "22",
        "ubicacion": "Cochabamba",
        "estilo_mentor": "Amistoso y motivador, usa modismos bolivianos como 'che' y 'viejo'."
    }

# 2. Configurar el Cliente (Pon aquí tu API Key real)
client = genai.Client(api_key="TU_CLAVE_API_REAL_AQUÍ")

instruccion_sistema = f"""
Actúa como un mentor experto en Inteligencia Artificial y programación. 
Estás hablando con {datos_perfil['nombre']}, un estudiante de {datos_perfil['edad']} años que vive en {datos_perfil['ubicacion']}.
Sé amable, directo y ayúdalo paso a paso sin abrumarlo con tecnicismos.

Forma de hablar obligatoria: {datos_perfil['estilo_mentor']}
"""

# 🔄 AQUÍ USAMOS TU PRIMER DEF: Guardamos el resultado en una variable
saludo_tiempo = obtener_saludo_dinamico()

# 🔄 AQUÍ USAMOS TU SEGUNDO DEF: Le pasamos los datos para que dibuje el banner
limpiar_consola_con_banner(saludo_tiempo, datos_perfil['nombre'])

historial_conversacion = [instruccion_sistema]
contador_mensajes = 1

# 3. EL BUCLE MÁGICO
while True:
    
    tu_mensaje = input(f"[{contador_mensajes}] Tú: ")
    
    if tu_mensaje.lower().strip() == "salir":
        despedidas = [
            f"\nMentor IA: ¡Ya, {datos_perfil['nombre']}! Cuidate, nos vemos.",
            f"\nMentor IA: ¡Chao, viejo! A meterle ganas al código.",
            f"\nMentor IA: ¡Nos vemos, campeón! Sigue programando duro.",
            f"\nMentor IA: ¡Hasta luego, che! Mañana le seguimos dando."
        ]
        print(random.choice(despedidas))
        break  
    
    if tu_mensaje.lower().strip() == "limpiar":
        historial_conversacion = [instruccion_sistema]
        contador_mensajes = 1
        
        # 🔄 ¡MIRA QUÉ LIMPIO! Reutilizamos la función aquí adentro también
        limpiar_consola_con_banner(saludo_tiempo, datos_perfil['nombre'])
        print(f"Mentor IA: ¡Memoria y terminal limpias! ¿De qué hablamos?")
        print("-" * 50)
        continue  
        
    historial_conversacion.append(f"\nUsuario dice: {tu_mensaje}")
    contexto_completo = "\n".join(historial_conversacion)
    
    tiempo_inicio = time.time()
    
    try:
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contexto_completo,
        )
        texto_respuesta = respuesta.text  
    except Exception as e:
        texto_respuesta = "¡Uy, viejo! Parece que tuvimos un pequeño problema de conexión con la matriz de la IA. Revisa tu internet o tu API Key y volvamos a intentar."
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    historial_conversacion.append(f"Mentor IA: {texto_respuesta}")
    
    print(f"\nMentor IA: {texto_respuesta}")
    print(f"⏱️ Tiempo de respuesta: {tiempo_total:.2f} segundos")
    print("-" * 50)
    
    contador_mensajes += 1
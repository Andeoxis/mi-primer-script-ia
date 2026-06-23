import os
import json
import time
import random
from datetime import datetime
from google import genai
from dotenv import load_dotenv

# Esto carga tu archivo .env en la memoria del programa
load_dotenv()

# ====================================================
# 🎨 PALETA DE COLORES ANSI (MANTENIÉNDOLO SIMPLE)
# ====================================================
VERDE = "\033[92m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ====================================================
# 📦 TUS FUNCIONES (TU CAJA DE HERRAMIENTAS)
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
    print(f"{CYAN}===================================================={RESET}")
    print(f"{AMARILLO}{saludo}, {nombre}! Entorno de chat estilizado.{RESET}")
    print("Para borrar la memoria escribe: 'limpiar'")
    print("Para cerrar el programa escribe: 'salir'")
    print(f"{CYAN}===================================================={RESET}\n")

def cargar_historial_guardado(instruccion_base):
    """Intenta cargar el historial previo de disco. Si no existe, inicia de cero."""
    try:
        with open("historial_chat.json", "r", encoding="utf-8") as archivo:
            print(f"🧠 {VERDE}¡Memoria recuperada! Cargando conversación anterior...{RESET}")
            time.sleep(1)
            return json.load(archivo)
    except FileNotFoundError:
        return [instruccion_base]

def guardar_historial_en_disco(historial):
    """Guarda de forma segura la lista de la conversación en un archivo JSON."""
    try:
        with open("historial_chat.json", "w", encoding="utf-8") as archivo:
            json.dump(historial, archivo, ensure_ascii=False, indent=4)
        print(f"\n💾 {VERDE}Historial guardado con éxito.{RESET}")
    except Exception as e:
        print(f"\n⚠️ {ROJO}No se pudo guardar el historial: {e}{RESET}")

def registrar_log_tecnico(mensaje_usuario, tiempo_respuesta, estado):
    """Registra la actividad del sistema en un archivo .txt plano."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{ahora}] ESTADO: {estado} | Usuario: '{mensaje_usuario}' | Latencia API: {tiempo_respuesta:.2f}s\n"
    try:
        with open("registro_asistente.txt", "a", encoding="utf-8") as log_file:
            log_file.write(linea_log)
    except Exception as e:
        print(f"⚠️ Error al escribir el log técnico: {e}")


# ====================================================
# 🚀 ENTORNO PRINCIPAL (EL FLUJO DE TU PROGRAMA)
# ====================================================

# 1. Leer los datos locales de tu perfil JSON
try:
    with open("perfil_usuario.json", "r", encoding="utf-8") as archivo:
        datos_perfil = json.load(archivo)
except FileNotFoundError:
    print(f"{AMARILLO}⚠️ ¡Advertencia! No se encontró 'perfil_usuario.json'. Usando perfil temporal.{RESET}")
    datos_perfil = {
        "nombre": "Estudiante",
        "edad": "22",
        "ubicacion": "Cochabamba",
        "estilo_mentor": "Amistoso y motivador, usa modismos bolivianos como 'che' y 'viejo'."
    }

# 2. Configurar el Cliente (Pon tu clave API aquí)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

instruccion_sistema = f"""
Actúa como un mentor experto en Inteligencia Artificial y programación. 
Estás hablando con {datos_perfil['nombre']}, un estudiante de {datos_perfil['edad']} años que vive en {datos_perfil['ubicacion']}.
Sé amable, directo y ayúdalo paso a paso sin abrumarlo con tecnicismos.

Forma de hablar obligatoria: {datos_perfil['estilo_mentor']}
"""

saludo_tiempo = obtener_saludo_dinamico()
limpiar_consola_con_banner(saludo_tiempo, datos_perfil['nombre'])

historial_conversacion = cargar_historial_guardado(instruccion_sistema)
contador_mensajes = len(historial_conversacion) // 2 + 1

limpiar_consola_con_banner(saludo_tiempo, datos_perfil['nombre'])

# 3. EL BUCLE MÁGICO
while True:
    
    # Añadimos un toque azul a la entrada del usuario
    tu_mensaje = input(f"[{contador_mensajes}] {AZUL}Tú:{RESET} ")
    
    if tu_mensaje.lower().strip() == "salir":
        despedidas = [
            f"\n{VERDE}Mentor IA: ¡Ya, {datos_perfil['nombre']}! Cuidate, nos vemos.{RESET}",
            f"\n{VERDE}Mentor IA: ¡Chao, viejo! A meterle ganas al código.{RESET}"
        ]
        print(random.choice(despedidas))
        guardar_historial_en_disco(historial_conversacion)
        registrar_log_tecnico("COMANDO_SALIR", 0.00, "SUCCESS_EXIT")
        break  
    
    if tu_mensaje.lower().strip() == "limpiar":
        historial_conversacion = [instruccion_sistema]
        contador_mensajes = 1
        if os.path.exists("historial_chat.json"):
            os.remove("historial_chat.json")
            
        limpiar_consola_con_banner(saludo_tiempo, datos_perfil['nombre'])
        print(f"Mentor IA: ¡Memoria limpia! ¿De qué hablamos?")
        print("-" * 50)
        registrar_log_tecnico("COMANDO_LIMPIAR", 0.00, "MEMORY_CLEARED")
        continue  
        
    historial_conversacion.append(f"\nUsuario dice: {tu_mensaje}")
    contexto_completo = "\n".join(historial_conversacion)
    
    tiempo_inicio = time.time()
    estado_peticion = "SUCCESS"
    
    try:
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contexto_completo,
        )
        texto_respuesta = respuesta.text  
    except Exception as e:
        texto_respuesta = "¡Uy, viejo! Parece que tuvimos un pequeño problema de conexión."
        estado_peticion = f"ERROR: {type(e).__name__}"
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    historial_conversacion.append(f"Mentor IA: {texto_respuesta}")
    
    # Imprimimos la respuesta en VERDE y los datos técnicos en AMARILLO/RESET
    print(f"\n{VERDE}Mentor IA: {texto_respuesta}{RESET}")
    print(f"{AMARILLO}⏱️ Tiempo de respuesta: {tiempo_total:.2f} segundos{RESET}")
    print(f"{CYAN}-" * 50 + f"{RESET}")    
    registrar_log_tecnico(tu_mensaje, tiempo_total, estado_peticion)
    
    contador_mensajes += 1
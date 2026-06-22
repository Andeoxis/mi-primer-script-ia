# Conexión Básica con Gemini API en Python

Este proyecto es mi primer paso conectando scripts de Python con modelos de lenguaje avanzados utilizando la API oficial de Google GenAI (`gemini-2.5-flash`).

## Lo que aprendí hoy:
* Configurar entornos de desarrollo en Windows y solucionar problemas de PATH con `pip`.
* Arquitectura lógica de comunicación de datos (Frontend -> API -> Backend).
* Manejo de formatos de intercambio de datos (JSON).
* Estructurar y leer bases de datos locales utilizando el formato **JSON**.
* Conceptos de **Inyección de Contexto** y Prompt Engineering para personalizar respuestas de IA.
* Debugging y resolución de errores de comunicación en APIs en la nube (Errores HTTP 503 y 404).
* Aprendi a generar un bucle para que con while se repita una accion
* Agragar condicionales booleanas (True or False)
* Usar el input para que este se detenga y espere mi respuesta
* Manejo de arrays/listas dinámicas para acumular el historial de chat con .append().
* Simulación de memoria en sistemas conversacionales "stateless" (sin estado) mediante concatenación de strings.
* Control de errores y sanitización de entradas con `.lower().strip()` para mitigar fallos por espacios en blanco accidentales del usuario.
* Implementación de comandos lógicos locales (`limpiar` y `salir`) utilizando estructuras condicionales para el control de flujo sin llamadas innecesarias a la API.
* Gestión de estados locales mediante variables de incremento numérico (`+= 1`) para el conteo y orden dinámico de interacciones.
* Medición de rendimiento y latencia de red calculando la diferencia de tiempo Unix (`time.time()`) en las peticiones a los servidores de Google.
* Manejo de respuestas dinámicas e impredecibles mediante la selección aleatoria de elementos (`random.choice()`) para mejorar la experiencia de usuario.
* Interacción directa con el sistema operativo a través del módulo `os` para la automatización de limpieza visual de la consola (`cls`).
* Inyección de lógica temporal utilizando estructuras condicionales `if/elif/else` y `time.localtime()` para personalizar la interfaz de usuario dinámicamente según la hora del sistema.
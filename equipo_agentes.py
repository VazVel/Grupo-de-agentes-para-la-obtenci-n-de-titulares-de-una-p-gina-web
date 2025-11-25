import autogen
import os
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "llama-3.1-8b-instant",  
        "api_key": os.environ.get("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }
]

# 1. Definición del Equipo de Agentes con Roles Especializados

# Agente 1: El Programador
programador = autogen.AssistantAgent(
    name="Programador",
    llm_config={"config_list": config_list},
    system_message="""
    Eres un programador Python senior. Tu rol es escribir código para cumplir con la tarea solicitada.
    No te salgas de tu rol de programador. Solo escribe código.
    Asegúrate de que tu código sea robusto y maneje posibles errores.
    """
)

# Agente 2: El Crítico de Código
critico = autogen.AssistantAgent(
    name="Critico_de_Codigo",
    llm_config={"config_list": config_list},
    system_message="""
    Eres un experto en revisión de código Python. Tu rol es evaluar el código escrito por el Programador.
    Busca bugs, sugiere mejoras en el estilo y la eficiencia, y verifica que el código cumpla con la tarea.
    Proporciona tu feedback en una lista de puntos. No escribas código completo.
    """
)

# Agente 3: El Ejecutor (nuestro proxy)
jefe_de_proyecto = autogen.UserProxyAgent(
    name="Jefe_de_Proyecto",
    human_input_mode="TERMINATE", 
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

# 2. Configuración del Chat Grupal (GroupChat)
agentes_del_grupo = [jefe_de_proyecto, programador, critico]
chat_grupal = autogen.GroupChat(
    agents=agentes_del_grupo,
    messages=[],
    max_round=12
)

# Creamos el "Orquestador" o "Manager" del chat
manager = autogen.GroupChatManager(
    groupchat=chat_grupal,
    llm_config={"config_list": config_list}
)

# 3. Inicio de la Tarea Colaborativa
print("▶️  Iniciando tarea de Web Scraping Colaborativo...")
jefe_de_proyecto.initiate_chat(
    manager,
    message="Extraer los titulares de la página principal de 'Hacker News' (https://news.ycombinator.com) y guardarlos en un archivo llamado 'titulares.txt'."
)
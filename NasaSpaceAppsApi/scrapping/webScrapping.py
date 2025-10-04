import requests
from bs4 import BeautifulSoup
import re
import textwrap
from typing import List, Dict

# IMPORTAR LIBRERÍA DE OPENAI
from openai import OpenAI 

# URL del artículo de PMC que proporcionaste
URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4136787/"


client = OpenAI() 

# ----------------------------------------------------------------------
# 1. Función de Limpieza y Extracción Estructurada (SIN CAMBIOS)
# (Mantenemos esta función tal como está, ya es muy buena)
# ----------------------------------------------------------------------
def fetch_and_clean_article(url: str) -> List[Dict[str, str]]:
    """
    Obtiene el contenido del artículo de PMC, lo limpia y lo estructura
    basándose en los encabezados (H2 y H3).
    """
    print(f"-> Obteniendo contenido de: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza error para códigos 4xx/5xx
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Selector clave: Encontrar la sección principal del artículo. 
    article_body = soup.find('div', class_='article') 
    if not article_body:
        article_body = soup.find('div', id='__main') 
    
    if not article_body:
        print("Advertencia: No se pudo identificar el cuerpo principal del artículo.")
        article_body = soup.body

    # Estructura para almacenar los chunks basados en secciones
    structured_chunks = []
    current_section_title = "Abstract" 
    current_section_content = []

    # Iterar sobre todos los elementos dentro del cuerpo del artículo
    for element in article_body.find_all(['h2', 'h3', 'p', 'h1']):
        text = element.get_text(strip=True)
        
        if not text:
            continue

        # Detección de encabezados (H2 y H3) para delimitar las secciones
        if element.name in ['h2', 'h3']:
            # Al encontrar un nuevo encabezado, guardamos el chunk anterior
            if current_section_content:
                full_content = " ".join(current_section_content)
                # Limpieza de referencias
                cleaned_content = re.sub(r'\[\d+\]|\[\d+–\d+\]|\[\d+,\s*\d+\]', '', full_content).strip()
                
                structured_chunks.append({
                    "section": current_section_title,
                    "raw_text": cleaned_content,
                    "source_url": url,
                    "html_tag": element.name
                })
            
            # Inicializar la nueva sección
            current_section_title = text
            current_section_content = []
            
        elif element.name == 'p':
            current_section_content.append(text)
            
    # No olvidar añadir el último chunk
    if current_section_content:
        full_content = " ".join(current_section_content)
        cleaned_content = re.sub(r'\[\d+\]|\[\d+–\d+\]|\[\d+,\s*\d+\]', '', full_content).strip()
        structured_chunks.append({
            "section": current_section_title,
            "raw_text": cleaned_content,
            "source_url": url,
            "html_tag": 'p (last section)'
        })

    # Filtrar chunks que son demasiado cortos (como solo un título o un número)
    return [c for c in structured_chunks if len(c['raw_text']) > 50]


# ----------------------------------------------------------------------
# 2. Función de Chunking Inteligente (CON INTEGRACIÓN DE OPENAI)
# ----------------------------------------------------------------------

def llm_intelligent_chunking(structured_chunks: List[Dict]) -> List[Dict]:
    """
    Procesa los chunks estructurados usando la API de OpenAI para crear
    resúmenes densos (Abstractive Chunking).
    """
    print("\n-> Procesando chunks con la API de OpenAI para generar resúmenes densos...")
    final_rag_chunks = []
    
    for i, chunk in enumerate(structured_chunks):
        section_title = chunk['section']
        raw_text = chunk['raw_text']
        
        # Opcional: Saltar secciones que son demasiado cortas o no son relevantes para RAG
        if len(raw_text) < 150: 
            print(f"   Saltando sección corta '{section_title}' ({len(raw_text)} caracteres).")
            # En lugar de resumir, usamos el texto limpio directamente
            text_for_embedding = raw_text
        else:
            print(f"   Resumiendo sección: {section_title} ({len(raw_text)} caracteres)...")
            
            # 1. Definición del Prompt para el Chunking Inteligente
            prompt = textwrap.dedent(f"""
                Eres un experto en investigación científica. Tu tarea es resumir el siguiente 
                texto de una sección de un artículo científico para optimizar su recuperación
                en un sistema RAG (Retrieval-Augmented Generation). 
                El resumen debe ser *denso en información*, cubriendo todos los hechos clave, 
                pero debe ser conciso y no exceder los 500 tokens.
                
                Título de la Sección: {section_title}
                
                Texto a resumir:
                ---
                {raw_text}
                ---
                
                Genera únicamente el texto del resumen denso.
            """).strip()
            
            # 2. Llamada a la API de OpenAI
            try:
                response = client.chat.completions.create(
                    model="gpt-4o", # O el modelo que prefieras (gpt-3.5-turbo es más rápido/barato)
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=550,
                    temperature=0.2
                )
                llm_output_text = response.choices[0].message.content
                # Añadir contexto al inicio del chunk para el embedding
                text_for_embedding = f"SECCIÓN: {section_title}. RESUMEN DENSO: {llm_output_text}"
                
            except Exception as e:
                print(f"!!! Error al llamar a la API para la sección {section_title}: {e}")
                # Si la IA falla, usamos el texto limpio original como fallback
                text_for_embedding = f"SECCIÓN: {section_title}. TEXTO COMPLETO: {raw_text}"


        final_rag_chunks.append({
            "id": f"chunk-{i+1}",
            "text_for_embedding": text_for_embedding, # Este es el texto vectorizado
            "section": chunk['section'],
            "source_url": chunk['source_url']
        })
        
    return final_rag_chunks

# ----------------------------------------------------------------------
# Ejecución principal (SIN CAMBIOS)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    
    # Paso 1: Obtener y estructurar el contenido del artículo
    structured_data = fetch_and_clean_article(URL)

    if structured_data:
        print(f"\n✅ Contenido estructurado. Se encontraron {len(structured_data)} secciones principales.")
        
        # Paso 2: Procesar los datos con la función de chunking inteligente (LLM de OpenAI)
        # Nota: Esto generará llamadas a la API y tendrá un costo.
        rag_chunks = llm_intelligent_chunking(structured_data)

        # Paso 3: Mostrar un ejemplo de los chunks listos para la indexación
        print("\n------------------------------------------------------------------")
        print("EJEMPLO DE CHUNKS LISTOS PARA ENVIAR A LA BASE DE DATOS VECTORIAL:")
        print("------------------------------------------------------------------")
        
        for i, chunk in enumerate(rag_chunks[:3]):
            print(f"\n--- CHUNK {i+1} (Sección: {chunk['section']}) ---")
            print(f"Texto para Embedding (Primeros 200 caracteres):\n{chunk['text_for_embedding'][:200]}...")
            print(f"Metadato Fuente: {chunk['source_url']}")
            
        print(f"\n*** Total de {len(rag_chunks)} chunks listos para la vectorización. ***")
    else:
        print("\n❌ Fallo en la obtención o procesamiento de datos.")

"""Integração do GrowUp com a LLM Gemini 2.5 Flash."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import construir_prompt

# Carrega as variáveis de ambiente do arquivo .env.
load_dotenv()


def gerar_resposta(pergunta: str, contexto: str) -> str:

    chave = os.getenv("GEMINI_API_KEY")

    if not chave:
        raise RuntimeError(
            "GEMINI_API_KEY não configurada."
        )

    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not isinstance(contexto, str) or not contexto.strip():
        raise ValueError("O contexto não pode estar vazio.")

    # Modelo padrão, configurável pelo arquivo .env.
    modelo = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    # Combina pergunta e documentação com as instruções.
    prompt = construir_prompt(pergunta, contexto)

    # Inicializa o cliente Gemini.
    cliente = genai.Client(api_key=chave)

    try:
        resposta = cliente.models.generate_content(
            model=modelo,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )

        texto = resposta.text

        if not texto or not texto.strip():
            raise RuntimeError(
                "O Gemini não retornou uma resposta textual."
            )

        return texto.strip()

    finally:
        cliente.close()

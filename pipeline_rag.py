
"""
GrowUp — Pipeline RAG
Pessoa 4: Integração da recuperação documental com Gemini.

Dependências:
- busca_chromadb.py (módulo da equipe)
- cliente_gemini.py
"""

import logging
import os

from busca_chromadb import buscar_documentos
from cliente_gemini import gerar_resposta

logger = logging.getLogger(__name__)

MENSAGEM_SEM_CONTEXTO = (
    "Não encontrei documentação suficiente "
    "para responder à pergunta com segurança."
)


def preparar_contexto(documentos, limite=12000):
    """
    Constrói o contexto para a LLM.

    Preserva os títulos, seções e URLs das fontes.
    O limite é medido em caracteres, não tokens.
    """

    if limite < 500:
        raise ValueError(
            "O limite de contexto deve ser de pelo menos 500."
        )

    partes = []
    fontes = []
    tamanho = 0

    for documento in documentos:
        texto = documento.get("texto", "").strip()

        if not texto:
            continue

        metadados = documento.get("metadados") or {}

        numero = len(fontes) + 1
        titulo = metadados.get("titulo", "Sem título")
        secao = metadados.get("secao", "Não informada")
        url = metadados.get("fonte", "")

        cabecalho = (
            f"[Fonte {numero}]\n"
            f"Título: {titulo}\n"
            f"Seção: {secao}\n"
            f"URL: {url}\n"
            "Conteúdo:\n"
        )

        restante = limite - tamanho - len(cabecalho) - 2

        if restante < 100:
            break

        trecho = texto[:restante]
        bloco = cabecalho + trecho

        partes.append(bloco)
        tamanho += len(bloco) + 2

        fontes.append({
            "numero": numero,
            "titulo": titulo,
            "secao": secao,
            "url": url,
            "id_documento": metadados.get(
                "document_id", ""
            ),
        })

        if len(trecho) < len(texto):
            break

    return "\n\n".join(partes), fontes


def responder(pergunta: str, quantidade: int = 3) -> dict:
    """
    Executa o Pipeline RAG completo.

    Etapas:
    1. Valida a pergunta.
    2. Recupera documentos no ChromaDB.
    3. Organiza o contexto.
    4. Envia a pergunta e o contexto ao Gemini.
    5. Retorna a resposta e as fontes.

    Esta função poderá ser utilizada pela Pessoa 5
    na implementação da API.
    """

    if not isinstance(pergunta, str):
        raise TypeError(
            "A pergunta deve ser uma string."
        )

    pergunta = pergunta.strip()

    if not pergunta:
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade < 1
    ):
        raise ValueError(
            "A quantidade deve ser um inteiro positivo."
        )

    try:
        # Etapa 1: recuperação documental.
        documentos = buscar_documentos(
            pergunta,
            quantidade=quantidade,
        )

        if not documentos:
            return {
                "resposta": MENSAGEM_SEM_CONTEXTO,
                "fontes": [],
                "avisos": [
                    "Nenhum documento recuperado."
                ],
                "estado": "contexto_insuficiente",
            }

        # Etapa 2: preparação do contexto.
        limite = int(
            os.getenv(
                "GROWUP_MAX_CONTEXT_CHARS",
                "12000"
            )
        )

        contexto, fontes = preparar_contexto(
            documentos,
            limite=limite,
        )

        if not contexto.strip():
            return {
                "resposta": MENSAGEM_SEM_CONTEXTO,
                "fontes": [],
                "avisos": [
                    "Contexto documental vazio."
                ],
                "estado": "contexto_insuficiente",
            }

        # Etapa 3: geração com a LLM.
        resposta = gerar_resposta(
            pergunta,
            contexto,
        )

        # Etapa 4: retorno estruturado.
        return {
            "resposta": resposta,
            "fontes": fontes,
            "avisos": [
                "As fontes foram recuperadas pela busca. "
                "A utilização efetiva de cada fonte "
                "não foi verificada automaticamente."
            ],
            "estado": "respondido",
        }

    except Exception:
        logger.exception(
            "Falha durante a execução do Pipeline RAG."
        )

        return {
            "resposta": (
                "Não foi possível processar "
                "a pergunta neste momento."
            ),
            "fontes": [],
            "avisos": [
                "Ocorreu um erro interno."
            ],
            "estado": "erro",
        }


if __name__ == "__main__":
    print("GrowUp — Pipeline RAG")
    print("Digite 'sair' para encerrar.")

    while True:
        pergunta = input(
            "\nSua pergunta: "
        ).strip()

        if pergunta.lower() == "sair":
            break

        if not pergunta:
            continue

        resultado = responder(pergunta)

        print(
            "\nEstado:",
            resultado["estado"]
        )

        print(
            "\nResposta:",
            resultado["resposta"]
        )

        print("\nFontes recuperadas:")

        for fonte in resultado["fontes"]:
            print(
                f"[Fonte {fonte['numero']}] "
                f"{fonte['titulo']}"
            )
            print(fonte["url"])

        for aviso in resultado["avisos"]:
            print("Aviso:", aviso)

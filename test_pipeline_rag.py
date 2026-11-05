import unittest
from unittest.mock import patch

from pipeline_rag import preparar_contexto, responder


class TestPipelineRAG(unittest.TestCase):
    """Testes das funções principais do pipeline."""

    def setUp(self):
        """Prepara documentos fictícios para os testes."""
        self.documentos = [
            {
                "id": "teste_chunk_0",
                "texto": (
                    "O optimization_level aceita "
                    "os valores 0, 1, 2 e 3."
                ),
                "metadados": {
                    "document_id": "teste",
                    "titulo": "Optimization levels",
                    "secao": "Optimization",
                    "fonte": "https://example.org/teste",
                },
                "distancia": 0.2,
            }
        ]

    def test_contexto_com_fontes(self):
        """Verifica a montagem do contexto e das fontes."""
        contexto, fontes = preparar_contexto(
            self.documentos
        )

        self.assertIn("optimization_level", contexto)
        self.assertIn("[Fonte 1]", contexto)
        self.assertEqual(len(fontes), 1)
        self.assertEqual(fontes[0]["numero"], 1)

    def test_pergunta_vazia(self):
        """Uma pergunta vazia deve gerar ValueError."""
        with self.assertRaises(ValueError):
            responder("   ")

    def test_pergunta_tipo_invalido(self):
        """A pergunta deve ser uma string."""
        with self.assertRaises(TypeError):
            responder(123)

    def test_quantidade_invalida(self):
        """A quantidade deve ser um inteiro positivo."""
        with self.assertRaises(ValueError):
            responder("Teste", quantidade=0)

    def test_limite_contexto_invalido(self):
        """O contexto exige um limite mínimo."""
        with self.assertRaises(ValueError):
            preparar_contexto(
                self.documentos,
                limite=100
            )

    @patch("pipeline_rag.buscar_documentos")
    def test_sem_documentos(self, mock_busca):
        """Verifica o retorno quando a busca não acha dados."""
        mock_busca.return_value = []

        resultado = responder("Pergunta de teste")

        self.assertEqual(
            resultado["estado"],
            "contexto_insuficiente"
        )
        self.assertEqual(resultado["fontes"], [])
        self.assertIn("resposta", resultado)

    @patch("pipeline_rag.gerar_resposta")
    @patch("pipeline_rag.buscar_documentos")
    def test_integracao_simulada(
        self,
        mock_busca,
        mock_gemini
    ):
        """Simula o fluxo completo de recuperação e geração."""
        mock_busca.return_value = self.documentos
        mock_gemini.return_value = (
            "Os níveis são 0, 1, 2 e 3."
        )

        resultado = responder(
            "Quais são os níveis de otimização?"
        )

        self.assertEqual(
            resultado["estado"],
            "respondido"
        )
        self.assertIn(
            "0, 1, 2 e 3",
            resultado["resposta"]
        )
        self.assertEqual(len(resultado["fontes"]), 1)

        mock_busca.assert_called_once()
        mock_gemini.assert_called_once()

    @patch("pipeline_rag.gerar_resposta")
    @patch("pipeline_rag.buscar_documentos")
    def test_falha_gemini(
        self,
        mock_busca,
        mock_gemini
    ):
        """Verifica o tratamento de falhas da LLM."""
        mock_busca.return_value = self.documentos
        mock_gemini.side_effect = RuntimeError(
            "Falha simulada na API"
        )

        resultado = responder("Pergunta de teste")

        self.assertEqual(
            resultado["estado"],
            "erro"
        )
        self.assertEqual(resultado["fontes"], [])

    @patch("pipeline_rag.gerar_resposta")
    @patch("pipeline_rag.buscar_documentos")
    def test_contexto_vazio(
        self,
        mock_busca,
        mock_gemini
    ):
        """Não chama a LLM se o documento não tem texto."""
        mock_busca.return_value = [
            {
                "texto": "",
                "metadados": {}
            }
        ]

        resultado = responder("Pergunta de teste")

        self.assertEqual(
            resultado["estado"],
            "contexto_insuficiente"
        )
        mock_gemini.assert_not_called()


if __name__ == "__main__":
    unittest.main()

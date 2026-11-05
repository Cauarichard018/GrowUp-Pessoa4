# GrowUp — Pipeline RAG e Integração com Gemini 2.5 Flash

**Projeto:** GrowUp  
**Responsável:** Pessoa 4  
**Módulo:** Pipeline RAG e integração com LLM  
**Linguagem:** Python  
**Modelo padrão:** Gemini 2.5 Flash

---

## 1. Apresentação

Este módulo é responsável pela integração entre o sistema de recuperação documental do GrowUp e um modelo de linguagem (LLM).

O objetivo é permitir que o usuário faça perguntas sobre a documentação do Qiskit e receba respostas em português, fundamentadas nos documentos recuperados.

A implementação utiliza a arquitetura **RAG (Retrieval-Augmented Generation)**, combinando recuperação de informações com geração de respostas por inteligência artificial.

## 2. Estado da entrega

Os arquivos da Pessoa 4 foram preparados para integrar a recuperação documental à API do Gemini.

**Implementado no código:**
- Construção de prompts em português.
- Cliente para comunicação com o Gemini.
- Organização do contexto recuperado.
- Retorno estruturado de respostas e fontes.
- Tratamento básico de erros.
- Testes unitários com simulações (mocks).

**Validações pendentes:**
- Execução dos testes em ambiente Python.
- Integração com a coleção real do ChromaDB.
- Comunicação real com a API do Gemini.
- Avaliação da qualidade e precisão das respostas.

A publicação dos arquivos no GitHub não significa que essas validações já foram concluídas.

## 3. Arquitetura do sistema

O Pipeline RAG segue o fluxo:

1. O usuário envia uma pergunta.
2. O módulo de recuperação consulta a base documental no ChromaDB.
3. Os documentos recuperados são organizados em um contexto textual.
4. O sistema constrói um prompt com instruções, contexto e pergunta.
5. O Gemini 2.5 Flash gera uma resposta.
6. O pipeline retorna a resposta, as fontes recuperadas e o estado do processamento.

**Fluxo resumido:**

```text
Pergunta do usuário
        |
        v
buscar_documentos()
        |
        v
ChromaDB
        |
        v
preparar_contexto()
        |
        v
construir_prompt()
        |
        v
Gemini 2.5 Flash
        |
        v
Resposta + Fontes + Estado
        |
        v
API da Pessoa 5
```

## 4. Estrutura dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `prompts.py` | Define as instruções e constrói o prompt. |
| `cliente_gemini.py` | Realiza a comunicação com o Gemini. |
| `pipeline_rag.py` | Coordena o fluxo de recuperação e geração. |
| `test_pipeline_rag.py` | Contém os testes automatizados do pipeline. |
| `requirements_pessoa4.txt` | Declara as dependências adicionais. |
| `.env.example` | Apresenta as configurações necessárias. |
| `README_PESSOA4.md` | Documenta a implementação e sua utilização. |

O repositório contém somente os arquivos da Pessoa 4. O módulo de recuperação documental é uma dependência externa desenvolvida pela equipe.

## 5. Integração com a recuperação documental

O arquivo `pipeline_rag.py` importa a função:

```python
from busca_chromadb import buscar_documentos
```

Essa função é responsável por recuperar os documentos relevantes no ChromaDB.

O pipeline espera receber documentos contendo texto e metadados, como título, seção e URL da fonte.

A integração foi projetada para utilizar a interface de recuperação existente, sem modificar o módulo desenvolvido pelo outro integrante da equipe.

**Importante:** para executar o pipeline completo, `busca_chromadb.py` e suas dependências precisam estar disponíveis no ambiente Python.

## 6. Preparação do contexto

A função `preparar_contexto()` transforma os documentos recuperados em blocos de texto que serão enviados à LLM.

Cada bloco contém:

- Identificador da fonte, como `[Fonte 1]`.
- Título do documento.
- Seção da documentação.
- URL de origem.
- Conteúdo textual recuperado.

O tamanho máximo do contexto pode ser configurado pela variável `GROWUP_MAX_CONTEXT_CHARS`.

O limite é medido em caracteres, não em tokens. Textos extensos podem ser truncados.

## 7. Construção dos prompts

O arquivo `prompts.py` define as instruções utilizadas pelo assistente.

As principais regras são:

- Responder em português brasileiro.
- Utilizar a documentação recuperada.
- Não inventar funções ou parâmetros do Qiskit.
- Preservar os nomes técnicos das APIs.
- Informar quando o contexto for insuficiente.
- Utilizar marcadores de fonte quando pertinente.
- Não afirmar que códigos ou circuitos foram executados.

A função `construir_prompt(pergunta, contexto)` combina essas instruções com os documentos recuperados e a pergunta do usuário.

## 8. Integração com Gemini 2.5 Flash

O arquivo `cliente_gemini.py` utiliza o SDK `google-genai` para enviar solicitações ao Gemini.

A função principal é:

```python
gerar_resposta(pergunta, contexto)
```

Ela executa as seguintes operações:

1. Carrega as configurações do ambiente.
2. Verifica a existência da chave de API.
3. Valida a pergunta e o contexto.
4. Constrói o prompt.
5. Envia a solicitação ao modelo configurado.
6. Extrai o texto retornado pela LLM.
7. Encerra o cliente.

O modelo padrão é `gemini-2.5-flash`, mas pode ser alterado por meio da variável `GEMINI_MODEL`.

A integração depende de uma chave de API válida e de acesso ao serviço do Gemini.

## 9. Instalação e configuração

### 9.1. Dependências

Em um ambiente que contenha os arquivos de recuperação da equipe, instale primeiro as dependências do projeto completo:

```bash
python -m pip install -r requirements.txt
```

Em seguida, instale as dependências adicionais da Pessoa 4:

```bash
python -m pip install -r requirements_pessoa4.txt
```

O arquivo `requirements_pessoa4.txt` contém:

```text
google-genai
python-dotenv
```

### 9.2. Variáveis de ambiente

Crie um arquivo `.env` local a partir do `.env.example`.

```env
GEMINI_API_KEY=COLOQUE_SUA_CHAVE_AQUI
GEMINI_MODEL=gemini-2.5-flash
GROWUP_MAX_CONTEXT_CHARS=12000
```

Substitua o valor de `GEMINI_API_KEY` por uma chave válida somente no arquivo `.env` local.

**Nunca publique a chave real no GitHub.**

## 10. Execução do Pipeline RAG

Com as dependências instaladas, a coleção ChromaDB preparada e a chave do Gemini configurada, execute:

```bash
python pipeline_rag.py
```

O programa solicitará uma pergunta.

Exemplo:

```text
Sua pergunta: Quais são os valores possíveis de optimization_level no Qiskit?
```

O sistema tentará recuperar documentos relevantes, gerar uma resposta e apresentar as fontes.

Digite `sair` para encerrar.

## 11. Testes automatizados

O arquivo `test_pipeline_rag.py` utiliza a biblioteca `unittest` e a ferramenta `unittest.mock`.

Os testes previstos verificam:

1. Construção do contexto com fontes.
2. Rejeição de perguntas vazias.
3. Rejeição de tipos de pergunta inválidos.
4. Rejeição de quantidades inválidas.
5. Validação do limite de contexto.
6. Tratamento de buscas sem documentos.
7. Integração simulada entre recuperação e geração.
8. Tratamento de falhas simuladas do Gemini.
9. Tratamento de documentos com texto vazio.

Para executar:

```bash
python -m unittest test_pipeline_rag.py -v
```

**Observação:** os testes simulam as chamadas ao ChromaDB e ao Gemini. Eles não comprovam, isoladamente, o funcionamento dos serviços reais.

Além disso, o módulo `busca_chromadb.py` precisa estar disponível para que o arquivo de testes consiga importar `pipeline_rag.py`.

## 12. Interface para a Pessoa 5

A função principal disponibilizada para integração com a futura API é:

```python
responder(pergunta, quantidade=3)
```

Exemplo de utilização:

```python
from pipeline_rag import responder

resultado = responder(
    "Quais são as etapas da transpilação no Qiskit?"
)

print(resultado["resposta"])
```

O retorno segue a estrutura:

```python
{
    "resposta": "Texto gerado ou mensagem informativa",
    "fontes": [
        {
            "numero": 1,
            "titulo": "Título do documento",
            "secao": "Seção consultada",
            "url": "https://exemplo.com",
            "id_documento": "identificador"
        }
    ],
    "avisos": [],
    "estado": "respondido"
}
```

### Estados possíveis

| Estado | Significado |
|---|---|
| `respondido` | O modelo retornou uma resposta textual. |
| `contexto_insuficiente` | Não foi possível construir contexto documental. |
| `erro` | Ocorreu uma falha durante o processamento. |

O estado `respondido` não representa uma garantia automática de correção factual.

A Pessoa 5 poderá utilizar esse retorno para construir os endpoints da API, sem precisar implementar novamente a lógica de recuperação e geração.

## 13. Limitações conhecidas

- A relevância dos documentos recuperados ainda não possui um filtro calibrado.
- A existência de documentos recuperados não garante que eles sejam suficientes para responder à pergunta.
- As fontes retornadas são fontes recuperadas; não existe verificação automática de cada citação gerada.
- O limite do contexto é definido por caracteres, e não por tokens.
- O texto documental pode ser truncado quando ultrapassa o limite.
- O pipeline não executa códigos ou circuitos Qiskit.
- A integração real depende do módulo ChromaDB da equipe.
- O funcionamento com o Gemini real ainda precisa ser validado.
- O tratamento de exceções retorna um estado genérico de erro; detalhes técnicos são registrados pelo logger.

## 14. Roteiro de validação

Antes da integração definitiva com a API da Pessoa 5:

- [ ] Instalar as dependências.
- [ ] Disponibilizar o módulo `busca_chromadb.py`.
- [ ] Confirmar que a coleção ChromaDB está indexada.
- [ ] Configurar uma chave válida do Gemini.
- [ ] Executar os testes automatizados.
- [ ] Executar perguntas reais sobre Qiskit.
- [ ] Verificar a pertinência das fontes recuperadas.
- [ ] Testar perguntas sem documentação suficiente.
- [ ] Verificar o tratamento de erros.
- [ ] Validar a interface `responder()` com a Pessoa 5.

## 15. Checklist de entrega

- [x] Código de construção de prompts preparado.
- [x] Cliente Gemini implementado no código.
- [x] Pipeline RAG estruturado.
- [x] Interface `responder()` definida.
- [x] Testes automatizados escritos.
- [x] Arquivo de dependências preparado.
- [x] Exemplo de configuração criado.
- [x] Documentação técnica elaborada.
- [ ] Testes automatizados executados e aprovados.
- [ ] Integração real com ChromaDB validada.
- [ ] Integração real com Gemini validada.
- [ ] Integração com a API da Pessoa 5 validada.

## 16. Conclusão

A entrega da Pessoa 4 apresenta a implementação proposta do Pipeline RAG do GrowUp, conectando a recuperação documental à geração de respostas com Gemini 2.5 Flash.

A estrutura separa as responsabilidades de recuperação, preparação do contexto, construção de prompts e comunicação com a LLM.

A função `responder()` fornece uma interface para a próxima etapa do projeto, permitindo que a Pessoa 5 desenvolva a API sobre o pipeline existente.

A implementação está documentada e preparada para validação, mas os testes reais ainda precisam ser realizados antes de considerar a integração concluída.

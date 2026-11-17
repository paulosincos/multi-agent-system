import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# Configuração dos modelos no Ollama
ollama_provider = OllamaProvider(base_url='http://localhost:11434/v1')
modelo_raciocinio = OpenAIChatModel(model_name='gemma-general', provider=ollama_provider)
modelo_codigo = OpenAIChatModel(model_name='bonsai-dev', provider=ollama_provider)

# =====================================================================
# 1. SUB-AGENTE DE ARQUIVOS (Tem tools apenas para ler/listar arquivos)
# =====================================================================
agente_arquivos = Agent(
    modelo_raciocinio,
    system_prompt='Você é um especialista em explorar diretórios e ler arquivos locais.'
)

@agente_arquivos.tool_plain
def listar_arquivos(diretorio: str = '.') -> list[str]:
    """Lista os arquivos de um diretório local."""
    return os.listdir(diretorio)

@agente_arquivos.tool_plain
def ler_arquivo(caminho: str) -> str:
    """Lê o conteúdo de um arquivo de texto."""
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

# =====================================================================
# 2. SUB-AGENTE PROGRAMADOR (Tem tools apenas para criar/testar código)
# =====================================================================
agente_coder = Agent(
    modelo_codigo,
    system_prompt='Você é um desenvolvedor Python. Escreva código limpo e salve nos arquivos solicitados.'
)

@agente_coder.tool_plain
def salvar_codigo(caminho: str, codigo: str) -> str:
    """Salva um código Python em um arquivo no disco."""
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(codigo)
    return f"Arquivo {caminho} salvo com sucesso."

# =====================================================================
# 3. AGENTE ORQUESTRADOR (Só enxerga Skills e os Sub-agentes)
# =====================================================================
orquestrador = Agent(
    modelo_raciocinio,
    system_prompt=(
        'Você é um Orquestrador. Analise o pedido do usuário, carregue as skills '
        'necessárias e delegue as etapas para os sub-agentes especializados.'
    )
)

@orquestrador.tool_plain
def carregar_skill(nome_skill: str) -> str:
    """Carrega diretrizes técnicas antes de delegar uma tarefa."""
    skills = {
        "refatoracao": "Sempre leia o arquivo original antes de criar uma versão melhorada.",
        "testes": "Todo código novo deve incluir funções de teste unitário."
    }
    return skills.get(nome_skill, "Skill não encontrada.")

# Delegação 1: Chama o agente_arquivos
@orquestrador.tool
async def consultar_arquivos(ctx: RunContext[None], instrucao: str) -> str:
    """Delega tarefas de leitura ou busca de arquivos para o agente_arquivos."""
    res = await agente_arquivos.run(instrucao, usage=ctx.usage)
    return res.output

# Delegação 2: Chama o agente_coder
@orquestrador.tool
async def solicitar_codigo(ctx: RunContext[None], especificacao: str) -> str:
    """Delega a criação ou edição de código para o agente_coder."""
    res = await agente_coder.run(especificacao, usage=ctx.usage)
    return res.output

# =====================================================================
# EXECUÇÃO
# =====================================================================
# resultado = orquestrador.run_sync(
#     "Veja quais arquivos existem na pasta atual, leia o 'app.py' e crie um 'test_app.py' seguindo a skill testes."
# )
# print(resultado.output)

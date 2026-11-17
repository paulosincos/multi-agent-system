# Multi-agent system

## Pré-requisitos

- Python 3.12
- Ollama instalado e em execução em `http://localhost:11434`
- Modelos prontos para executar

## Instalação

No Windows, abra o terminal na pasta do projeto e crie o ambiente virtual:

```powershell
py -3.12 -m venv venv
```

Ative o ambiente e instale as dependências:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se a ativação do ambiente estiver bloqueada pela política de execução do PowerShell, use o Python do ambiente diretamente:

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

O arquivo `requirements.txt` fixa as dependências diretas utilizadas pelo projeto.
O Ollama é um pré-requisito externo e não é instalado pelo `pip`.

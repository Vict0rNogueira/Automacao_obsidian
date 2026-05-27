# Obsidian_Auto

Pequena aplicação Flask para gerar arquivos Markdown organizados por matéria em um vault (por exemplo, Obsidian). A interface web permite adicionar conteúdos e gerar automaticamente os arquivos e links necessários.

**Estrutura do projeto**

- `app.py` - servidor Flask e lógica principal de geração de arquivos
- `requirements.txt` - dependências do projeto
- `templates/` - templates HTML (interface web)
- `static/` - arquivos estáticos (CSS)
- `utils/generator.py` - utilitários auxiliares

**Pré-requisitos**

- Python 3.10+ (recomendado)
- `pip` instalado

**Instalação (Windows)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Uso**

1. Ajuste o caminho do vault em `app.py` na variável `VAULT_PATH` para apontar para sua pasta do Obsidian.
2. Execute a aplicação:

```powershell
python app.py
```

3. Abra o navegador em `http://127.0.0.1:5000/` e use o formulário para gerar os arquivos Markdown.

**Observações**

- O servidor roda em modo de desenvolvimento (`debug=True`) por padrão. Para produção, configure um servidor WSGI adequado e desative o modo debug.
- Os arquivos gerados usam codificação `utf-8`.

**Contribuição**

Abra uma issue ou envie um pull request com melhorias.

**Licença**

Sem licença especificada — use conforme suas necessidades.

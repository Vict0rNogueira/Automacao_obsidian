# 📚 Obsidian Auto

Aplicação web Flask para gerar automaticamente arquivos Markdown organizados por matéria em um vault Obsidian. Integrada com a API Google Generative AI para processar conteúdo baseado em áudio.

## ✨ Funcionalidades

- 🎤 Processamento de áudio via Google Generative AI
- 📝 Geração automática de arquivos Markdown estruturados
- 🔗 Criação automática de links entre notas
- 💻 Interface web intuitiva e responsiva
- 📦 Organização automática por matérias/tópicos
- 🛡️ Manipulação segura de caminhos de arquivo

## 📋 Pré-requisitos

- Python 3.10+
- pip instalado
- Conta Google para usar a API Generative AI
- Vault Obsidian configurado localmente

## 🚀 Instalação

### Windows

```powershell
# Clonar o repositório
git clone https://github.com/seu-usuario/Obsidian_Auto.git
cd Obsidian_Auto

# Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### Linux/macOS

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/Obsidian_Auto.git
cd Obsidian_Auto

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

1. **Configure o caminho do vault Obsidian:**
   - Abra `app.py`
   - Localize a variável `VAULT_PATH`
   - Substitua pelo caminho da sua pasta Obsidian:
   
   ```python
   VAULT_PATH = Path(r"C:\Users\SeuUsuario\Documents\ObsidianVault")
   ```

2. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API Google:
   
   ```env
   GOOGLE_API_KEY=sua_chave_aqui
   ```

## 💡 Uso

1. Execute a aplicação:

```powershell
python app.py
```

2. Abra seu navegador e acesse:

```
http://127.0.0.1:5000/
```

3. Use a interface web para:
   - Fazer upload de arquivos de áudio
   - Adicionar conteúdo manualmente
   - Gerar arquivos Markdown organizados
   - Gerenciar matérias e tópicos

## 📁 Estrutura do Projeto

```
Obsidian_Auto/
├── app.py                 # Servidor Flask principal
├── gemini_service.py      # Integração com Google Generative AI
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
├── templates/            # Templates HTML
│   ├── index.html
│   └── dashboard.html
├── static/               # Arquivos estáticos
│   └── style.css
└── temp/                 # Pasta temporária (não incluir no git)
```

## 🔧 Configuração para Produção

Para usar em produção:

1. Desative o modo debug em `app.py`:
   ```python
   app.run(debug=False)
   ```

2. Use um servidor WSGI como Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

3. Configure variáveis de ambiente de forma segura

## 📝 Observações

- Os arquivos são gerados com codificação UTF-8
- A pasta `temp/` é usada para arquivos temporários e deve ser incluída em `.gitignore`
- O modo debug deve estar desativado em produção

## 🐛 Troubleshooting

**Erro: "Caminho do vault não encontrado"**
- Verifique se o caminho em `VAULT_PATH` está correto
- Use caminhos absolutos em vez de relativos

**Erro: "Chave de API inválida"**
- Verifique se a chave da API está corretamente configurada no `.env`
- Confirme se a chave tem permissões para usar a API Generative AI

**Erro: Permissão negada ao criar arquivos**
- Verifique as permissões da pasta do vault
- Garanta que o usuário tem acesso de escrita

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](../../issues) no repositório.

---

**Desenvolvido com ❤️ para melhorar sua produtividade no Obsidian**

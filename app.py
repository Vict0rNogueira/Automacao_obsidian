from flask import Flask, render_template, request
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# ==========================================
# CAMINHO DO VAULT
# ==========================================

VAULT_PATH = Path(r"C:\Users\viniu\OneDrive\Documentos\TJ CE 2026\Matérias")

# ==========================================
# GERAR MARKDOWN
# ==========================================

def gerar_markdown(data, materia, conteudo, notebooklm):

    pasta_materia = VAULT_PATH / materia

    pasta_materia.mkdir(parents=True, exist_ok=True)

    # ==========================================
    # ARQUIVO PRINCIPAL DA MATÉRIA
    # ==========================================

    arquivo_materia = pasta_materia / f"{materia}.md"

    if not arquivo_materia.exists():

        texto_inicial = f"""# {materia}

## Conteúdos

"""

        with open(arquivo_materia, "w", encoding="utf-8") as f:
            f.write(texto_inicial)

    # ==========================================
    # ADICIONAR LINK NO ARQUIVO DA MATÉRIA
    # ==========================================

    with open(arquivo_materia, "r", encoding="utf-8") as f:
        conteudo_atual = f.read()

    link_conteudo = f"- [[{conteudo}]]"

    if link_conteudo not in conteudo_atual:

        with open(arquivo_materia, "a", encoding="utf-8") as f:
            f.write(f"{link_conteudo}\n")

    # ==========================================
    # ARQUIVO DO CONTEÚDO
    # ==========================================

    arquivo_conteudo = pasta_materia / f"{conteudo}.md"

    if not arquivo_conteudo.exists():

        texto_conteudo = f"""# {conteudo}

Matéria: [[{materia}]]

Data: {data}

---

## NotebookLM
{notebooklm}

---

## Resumo

---

## Questões

---

## Revisão

- [ ] Revisar em 1 dia
- [ ] Revisar em 7 dias
- [ ] Revisar em 30 dias

---

## Anotações

"""

        with open(arquivo_conteudo, "w", encoding="utf-8") as f:
            f.write(texto_conteudo)

# ==========================================
# ROTA PRINCIPAL
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        materias = request.form.getlist("materia")
        conteudos = request.form.getlist("conteudo")
        notebooks = request.form.getlist("notebooklm")

        data = datetime.now().strftime("%Y-%m-%d")

        for i in range(len(materias)):

            gerar_markdown(
                data,
                materias[i],
                conteudos[i],
                notebooks[i]
            )

    return render_template("index.html")

# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
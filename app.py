# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from pathlib import Path
from datetime import datetime
from gemini_service import gerar_material_audio

from werkzeug.utils import secure_filename

import re
import os
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

# ==========================================
# CAMINHO DO VAULT
# ==========================================

VAULT_PATH = Path(
    r"Seu_Caminho_Obsidian"
)

# ==========================================
# PASTA TEMP
# ==========================================

UPLOAD_FOLDER = "temp"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==========================================
# LIMPAR NOME
# ==========================================

def limpar_nome_arquivo(nome):

    nome = re.sub(
        r'[\\/*?:"<>|]',
        "",
        nome
    )

    nome = nome.replace("  ", " ")

    return nome.strip()

# ==========================================
# GERAR MARKDOWN
# ==========================================

def gerar_markdown(
    data,
    materia,
    conteudo,
    notebooklm,
    resultado_ia
):
    try:
        conteudo_limpo = limpar_nome_arquivo(
            conteudo
        )

        # ==========================================
        # PASTA MATÉRIA
        # ==========================================

        pasta_materia = VAULT_PATH / materia

        logger.info(f"Criando pasta: {pasta_materia}")
        pasta_materia.mkdir(
            parents=True,
            exist_ok=True
        )
        logger.info(f"Pasta criada com sucesso: {pasta_materia}")

        # ==========================================
        # ARQUIVO PRINCIPAL
        # ==========================================

        arquivo_materia = (
            pasta_materia / f"{materia}.md"
        )

        logger.info(f"Criando arquivo: {arquivo_materia}")
        if not arquivo_materia.exists():

            with open(
                arquivo_materia,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    f"# {materia}\n\n## Conteudos\n\n"
                )
            logger.info(f"Arquivo principal criado: {arquivo_materia}")

        # ==========================================
        # ADICIONAR LINK
        # ==========================================

        with open(
            arquivo_materia,
            "r",
            encoding="utf-8"
        ) as f:

            texto_atual = f.read()

        link = f"- [[{conteudo_limpo}]]"

        if link not in texto_atual:

            with open(
                arquivo_materia,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(f"{link}\n")
            logger.info(f"Link adicionado ao arquivo: {link}")

        # ==========================================
        # ARQUIVO CONTEÚDO
        # ==========================================

        arquivo_conteudo = (
            pasta_materia / f"{conteudo_limpo}.md"
        )

        texto_markdown = f"""# {conteudo_limpo}

Materia: [[{materia}]]

Data: {data}

---

## NotebookLM

{notebooklm}

---

## Material Gerado pela IA

{resultado_ia}

---

## Anotacoes

"""

        logger.info(f"Salvando arquivo de conteúdo: {arquivo_conteudo}")
        with open(
            arquivo_conteudo,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(texto_markdown)
        logger.info(f"Arquivo de conteúdo salvo com sucesso: {arquivo_conteudo}")
        return True

    except Exception as e:
        logger.error(f"Erro ao gerar markdown: {e}")
        logger.error(traceback.format_exc())
        return False

# ==========================================
# DASHBOARD
# ==========================================

@app.route("/", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST":
        try:
            # ==========================================
            # FORMULÁRIO
            # ==========================================

            materia = request.form["materia"]
            conteudo = request.form["conteudo"]
            notebooklm = request.form["notebooklm"]
            audio = request.files["audio"]

            logger.info(f"POST recebido - Materia: {materia}, Conteudo: {conteudo}")

            data = datetime.now().strftime(
                "%Y-%m-%d"
            )

            # ==========================================
            # NOME SEGURO
            # ==========================================

            nome_audio = secure_filename(
                audio.filename
            )

            # ==========================================
            # CAMINHO
            # ==========================================

            caminho_audio = os.path.join(
                UPLOAD_FOLDER,
                nome_audio
            )

            # ==========================================
            # SALVAR ÁUDIO
            # ==========================================

            logger.info(f"Salvando áudio em: {caminho_audio}")
            audio.save(caminho_audio)
            logger.info(f"Áudio salvo com sucesso")

            # ==========================================
            # GERAR IA
            # ==========================================

            logger.info(f"Iniciando geração de conteúdo IA...")
            resultado_ia = gerar_material_audio(
                caminho_audio
            )
            logger.info(f"IA concluída. Resultado com {len(resultado_ia)} caracteres")

            # ==========================================
            # REMOVER TEMP
            # ==========================================

            if os.path.exists(caminho_audio):
                try:
                    os.remove(caminho_audio)
                    logger.info(f"Arquivo temporário removido")
                except Exception as e:
                    logger.warning(f"Não foi possível remover arquivo temporário: {e}")

            # ==========================================
            # GERAR MARKDOWN
            # ==========================================

            sucesso = gerar_markdown(
                data,
                materia,
                conteudo,
                notebooklm,
                resultado_ia
            )

            if sucesso:
                logger.info("Arquivos salvos com sucesso em Obsidian")
                return jsonify({"status": "success", "message": "Material salvo em Obsidian com sucesso!"}), 200
            else:
                logger.error("Falha ao salvar em Obsidian")
                return jsonify({"status": "error", "message": "Erro ao salvar em Obsidian. Verifique os logs."}), 500

        except Exception as e:
            logger.error(f"Erro no POST: {e}")
            logger.error(traceback.format_exc())
            return jsonify({"status": "error", "message": f"Erro: {str(e)}"}), 500

    return render_template(
        "dashboard.html"
    )

# ==========================================
# INICIAR
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
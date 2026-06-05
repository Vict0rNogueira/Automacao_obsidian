# -*- coding: utf-8 -*-

from google import genai
from google.genai import errors, types
from dotenv import load_dotenv
import os
import time
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

# ==========================================
# API KEY
# ==========================================

api_key = os.getenv(
    "GEMINI_API"
)

# ==========================================
# CLIENT
# ==========================================

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ==========================================
# ANALISAR ÁUDIO
# ==========================================

def gerar_material_audio(caminho_audio):
    try:
        logger.info(f"Iniciando upload do arquivo: {caminho_audio}")
        uploaded_file = client.files.upload(
            file=caminho_audio
        )
        logger.info(f"Arquivo enviado com sucesso: {uploaded_file.name}")

        prompt = """
        You are an educational assistant.

        Analyze this study podcast/audio and generate:

        1. Detailed summary
        2. 10 objective questions
        3. 10 flashcards
        4. Important topics
        5. Quick review

        Organize everything in markdown.
        """

        content = types.Content(
            role='user',
            parts=[
                types.Part.from_text(text=prompt),
                types.Part(uploaded_file),
            ],
        )

        tentativas = 3

        for tentativa in range(tentativas):

            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=content,
                )

                logger.info(f"Conteúdo gerado com sucesso (tentativa {tentativa + 1})")
                return response.text

            except Exception as e:

                logger.error(f"Erro Gemini (tentativa {tentativa + 1}): {e}")

                if isinstance(e, errors.ServerError) and getattr(e, 'status_code', None) == 429:
                    return (
                        "Erro ao gerar material IA: cota Gemini excedida. "
                        "Verifique faturamento/quota ou troque o modelo em GEMINI_MODEL."
                    )

                if isinstance(e, errors.ServerError) and getattr(e, 'status_code', None) == 503:
                    return (
                        "Erro ao gerar material IA: o modelo está temporariamente indisponível. "
                        "Tente novamente em alguns minutos."
                    )

                if tentativa < tentativas - 1:

                    logger.info(f"Aguardando 5 segundos antes da próxima tentativa...")
                    time.sleep(5)

                else:

                    return "Erro ao gerar material IA."

    except Exception as e:
        logger.error(f"Erro ao fazer upload do arquivo: {e}")
        logger.error(traceback.format_exc())
        return f"Erro ao processar áudio: {str(e)}"

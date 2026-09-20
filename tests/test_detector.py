#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes unitários e de não-regressão para scripts/detector_ptbr.py
Garante que novos padrões são detectados com precisão e que textos humanos legítimos
(falso-positivo negativo) continuem passando 100% limpos.
"""

import unittest
import sys
import subprocess
from pathlib import Path

# Adiciona scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from detector_ptbr import (
    analyze_text,
    strip_code_blocks,
    normalise_typography,
    visible_text,
    markdown_prose
)


class TestDetectorPTBR(unittest.TestCase):

    def test_gerundismo_detection(self):
        texto = "Prezados, vou estar enviando a planilha e estaremos realizando a checagem amanhã."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W1", rule_ids)
        self.assertGreater(res["score"], 0)

    def test_conclusivo_gerundio(self):
        texto = "O sistema atingiu 99% de uptime, demonstrando o compromisso com a qualidade."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W2", rule_ids)

    def test_arcaismos_oficiales(self):
        texto = "O projeto foi aprovado. Ademais, destarte cumpre salientar que os custos foram baixos."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W3", rule_ids)

    def test_abertura_generica(self):
        texto = "No cenário atual, a tecnologia desempenha um papel central."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W4", rule_ids)

    def test_falsos_amigos_traducao(self):
        texto = "Vamos mergulhar em uma rica tapeçaria de dados ao alavancar essa ferramenta."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W9", rule_ids)

    def test_clean_human_text_passes(self):
        texto = (
            "Lançamos hoje o novo painel de controle. Ele resolve um problema antigo: "
            "cruzar os dados da fatura levava quatro horas em planilhas manuais. "
            "Agora o relatório sai em dez segundos direto no navegador."
        )
        res = analyze_text(texto)
        self.assertEqual(res["total_violacoes"], 0)
        self.assertEqual(res["score"], 0)

    def test_shadowboxing_and_chatbot_residue(self):
        texto = "Você poderia pensar que a IA substitui o autor. Certamente! Espero que isso ajude!"
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W37", rule_ids)
        self.assertIn("W38", rule_ids)

    def test_code_blocks_are_protected(self):
        texto = """
Aqui está o código:
```python
# Não deve acusar falso positivo em código
def enviar():
    # ademais destarte outrossim
    return "vou estar enviando"
```
O código acima roda no servidor.
"""
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertNotIn("W1", rule_ids)
        self.assertNotIn("W3", rule_ids)

    def test_ignore_rules(self):
        texto = "Olha só: como fica o trânsito agora? — uma boa pergunta."
        res_normal = analyze_text(texto)
        self.assertTrue(any(v["regra_id"] in ["W12", "W17"] for v in res_normal["violacoes"]))

        res_ignored = analyze_text(texto, ignore_rules="W12,W17,W15")
        rule_ids = [v["regra_id"] for v in res_ignored["violacoes"]]
        self.assertNotIn("W12", rule_ids)
        self.assertNotIn("W17", rule_ids)
        self.assertNotIn("W15", rule_ids)
        self.assertEqual(res_ignored["score"], 0)

    def test_typography_normalization(self):
        # Aspas curvas, hífens tipográficos e espaços duros normalizados
        texto = "“No cenário atual”, não é sobre velocidade…\xa0alavancar o processo."
        normalizado = normalise_typography(texto)
        self.assertIn('"No cenário atual"', normalizado)
        self.assertNotIn('\xa0', normalizado)

    def test_visible_text_html(self):
        html_doc = """
        <html>
        <head><style>.hero { color: red; }</style></head>
        <body>
            <!-- Comentário ignorado -->
            <script>console.log("alavancar");</script>
            <div id="hero">
                <h1>Painel de Controle</h1>
                <p>O relat&oacute;rio sai em dez segundos.</p>
            </div>
        </body>
        </html>
        """
        texto_limpo = visible_text(html_doc)
        self.assertNotIn("alavancar", texto_limpo)
        self.assertNotIn("color: red", texto_limpo)
        self.assertIn("relatório sai em dez segundos", texto_limpo)

    def test_markdown_prose_isolation(self):
        # Garante que tabelas e listas não fundem células em falsas frases longas
        md = """
| Coluna 1 | Coluna 2 |
|---|---|
| Rápido | Seguro |
| Eficiente | Confiável |

- Primeiro item com um detalhe
- Segundo item com outro detalhe
"""
        prose = markdown_prose(md)
        res = analyze_text(prose, is_markdown=True)
        self.assertEqual(res["score"], 0)

    def test_w6_tricolon_detection(self):
        # Tríades de buzzwords corporativas
        texto_triade = "Nossa plataforma oferece agilidade, eficiência e inovação para o seu time."
        res = analyze_text(texto_triade)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W6", rule_ids)

        # Tríade de adjetivos promocionais
        texto_adjetivos = "Um sistema rápido, seguro e inteligente para o seu dia a dia."
        res_adj = analyze_text(texto_adjetivos)
        rule_ids_adj = [v["regra_id"] for v in res_adj["violacoes"]]
        self.assertIn("W6", rule_ids_adj)

        # Lista cotidiana legítima NÃO deve disparar W6 (guard contra falso positivo)
        texto_legitimo = "Comprei no mercado arroz, feijão e carne para o almoço."
        res_leg = analyze_text(texto_legitimo)
        rule_ids_leg = [v["regra_id"] for v in res_leg["violacoes"]]
        self.assertNotIn("W6", rule_ids_leg)

    def test_proof_social_fabrication(self):
        # Falsa prova social inflada sem auditoria
        texto_proof = "Nossa ferramenta já conta com mais de 10.000 clientes satisfeitos no Brasil."
        res_bloqueado = analyze_text(texto_proof, allow_proof=False)
        rule_ids = [v["regra_id"] for v in res_bloqueado["violacoes"]]
        self.assertIn("PROOF", rule_ids)
        self.assertGreater(res_bloqueado["score"], 0)

        # Com flag allow_proof, número real comprovado não penaliza o score
        res_permitido = analyze_text(texto_proof, allow_proof=True)
        self.assertEqual(res_permitido["score"], 0)

    def test_em_dash_same_sentence_window(self):
        # Dois travessões na mesma oração denunciam cadência artificial de IA
        texto_travessoes = "O sistema — desenvolvido com rigor — garante total estabilidade operacional."
        res = analyze_text(texto_travessoes)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W15", rule_ids)

    def test_empty_input_rejected_by_cli(self):
        # Executa o script via subprocess para validar que entrada vazia sai com código 1
        script_path = Path(__file__).parent.parent / "scripts" / "detector_ptbr.py"
        r = subprocess.run(
            [sys.executable, str(script_path), "--text", "   "],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("entrada vazia", r.stderr.lower())


if __name__ == "__main__":
    unittest.main()

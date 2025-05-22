from flask import Flask, jsonify, send_from_directory
from playwright.sync_api import sync_playwright
import traceback

app = Flask(__name__)

def gerar_chave_pix():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        contexto = navegador.new_context()
        pagina = contexto.new_page()

        print("🔁 Acessando site...")
        pagina.goto("https://bbg.bet")

        # Fechar popup inicial
        try:
            pagina.wait_for_selector("img.closeImg", timeout=15000)
            pagina.click("img.closeImg")
            print("Popup inicial fechado")
        except:
            print("Popup inicial não encontrado")

        # Clicar em "Entrar"
        pagina.click("a[href='/login?redirect=Home']")

        print("🔐 Fazendo login...")
        pagina.wait_for_selector("input[placeholder='Número de Celular']", timeout=15000)
        pagina.fill("input[placeholder='Número de Celular']", "21981383788")
        pagina.fill("input[placeholder='Senha']", "Thehacker3244@")
        pagina.click("button:has-text('Entrar')")

        # Fechar popup pós-login
        try:
            pagina.wait_for_selector("img.closeImg", timeout=15000)
            pagina.click("img.closeImg")
            print("Popup pós-login fechado")
        except:
            print("Popup pós-login não encontrado")

        print("💰 Acessando tela de depósito...")
        pagina.wait_for_selector("a.deposit", timeout=15000)
        pagina.click("a.deposit")

        pagina.wait_for_selector("input[placeholder='Min. 10']", timeout=15000)
        pagina.fill("input[placeholder='Min. 10']", "800")

        pagina.click("div.button.topUp.active")

        print("⏳ Aguardando chave Pix...")
        pagina.wait_for_selector("div#copy", timeout=20000)
        chave_pix = pagina.get_attribute("div#copy", "data-clipboard-text")

        navegador.close()
        print("✅ Chave Pix gerada:", chave_pix)
        return chave_pix

@app.route("/")
def serve_pix():
    return send_from_directory(".", "index.html")

@app.route("/gerar-pix", methods=["GET"])
def gerar_pix_endpoint():
    print("Iniciando geração da chave Pix...")
    try:
        chave = gerar_chave_pix()
        print("Chave Pix retornada:", chave)
        return jsonify({"chave_pix": chave})
    except Exception as e:
        print("Erro ao gerar chave Pix:")
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    # Para funcionar no Render
    app.run(host="0.0.0.0", port=10000)

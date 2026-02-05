import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "chave_mestra_super_secreta"

SENHA_ACESSO = "abaco1234"

def listar_slides():
    # Lista todos os arquivos .pdf dentro da pasta static
    caminho_static = os.path.join(app.root_path, 'static')
    arquivos = [f for f in os.listdir(caminho_static) if f.endswith('.pdf')]
    return arquivos

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("senha") == SENHA_ACESSO:
            session["logado"] = True
            return redirect(url_for("dashboard"))
        flash("Senha incorreta!")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logado"):
        return redirect(url_for("login"))
    
    slides = listar_slides()
    # Pega o slide selecionado da URL, ou o primeiro da lista
    slide_atual = request.args.get('slide', slides[0] if slides else None)
    
    return render_template("dashboard.html", slides=slides, slide_atual=slide_atual)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
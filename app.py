"""Biblioteca Pessoal - sistema simples de CRUD de livros com Flask + SQL Server."""
from flask import Flask, render_template, request, redirect, url_for, flash

from database import conectar

app = Flask(__name__)
app.secret_key = "projeto-faculdade"  # necessário para as mensagens (flash)

STATUS = ["Quero ler", "Lendo", "Lido"]


# READ
@app.route("/")
def listar_livros():
    """UC02 - Consultar livros (lista todos ou filtra pela busca)."""
    busca = request.args.get("busca", "").strip()
    conn = conectar()
    livros = conn.execute("""
        SELECT livro.*, categoria.nome AS categoria
        FROM livro JOIN categoria ON categoria.id = livro.categoria_id
        WHERE livro.titulo LIKE ? OR livro.autor LIKE ?
        ORDER BY livro.titulo
    """, (f"%{busca}%", f"%{busca}%")).fetchall()
    conn.close()
    return render_template("livros.html", livros=livros, busca=busca)


# CREATE
@app.route("/livros/novo", methods=["GET", "POST"])
def cadastrar_livro():
    """UC01 - Cadastrar livro."""
    conn = conectar()
    if request.method == "POST":
        dados = ler_formulario()
        if dados:
            conn.execute(
                "INSERT INTO livro (titulo, autor, ano, status, categoria_id) VALUES (?, ?, ?, ?, ?)",
                dados)
            conn.commit()
            conn.close()
            flash("Livro cadastrado com sucesso!", "ok")
            return redirect(url_for("listar_livros"))
    categorias = conn.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    conn.close()
    return render_template("livro_form.html", livro=None, categorias=categorias, status=STATUS)


# UPDATE
@app.route("/livros/<int:id>/editar", methods=["GET", "POST"])
def editar_livro(id):
    """UC03 - Editar livro."""
    conn = conectar()
    if request.method == "POST":
        dados = ler_formulario()
        if dados:
            conn.execute(
                "UPDATE livro SET titulo=?, autor=?, ano=?, status=?, categoria_id=? WHERE id=?",
                (*dados, id))
            conn.commit()
            conn.close()
            flash("Livro atualizado com sucesso!", "ok")
            return redirect(url_for("listar_livros"))
    livro = conn.execute("SELECT * FROM livro WHERE id = ?", (id,)).fetchone()
    categorias = conn.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    conn.close()
    if livro is None:
        flash("Livro não encontrado.", "erro")
        return redirect(url_for("listar_livros"))
    return render_template("livro_form.html", livro=livro, categorias=categorias, status=STATUS)


# DELETE
@app.route("/livros/<int:id>/excluir", methods=["POST"])
def excluir_livro(id):
    """UC04 - Excluir livro."""
    conn = conectar()
    conn.execute("DELETE FROM livro WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Livro excluído.", "ok")
    return redirect(url_for("listar_livros"))


def ler_formulario():
    """Lê e valida os campos do formulário de livro. Retorna None se houver erro."""
    titulo = request.form.get("titulo", "").strip()
    autor = request.form.get("autor", "").strip()
    ano = request.form.get("ano", "").strip()
    status = request.form.get("status", STATUS[0])
    categoria_id = request.form.get("categoria_id")

    if not titulo or not autor or not categoria_id:
        flash("Preencha título, autor e categoria.", "erro")
        return None
    if ano and not ano.isdigit():
        flash("O ano deve ser um número.", "erro")
        return None
    return (titulo, autor, int(ano) if ano else None, status, int(categoria_id))


# CREATE / READ
@app.route("/categorias", methods=["GET", "POST"])
def gerenciar_categorias():
    """UC05 - Gerenciar categorias (listar e cadastrar)."""
    conn = conectar()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("Informe o nome da categoria.", "erro")
        elif conn.execute("SELECT 1 FROM categoria WHERE nome = ?", (nome,)).fetchone():
            flash("Essa categoria já existe.", "erro")
        else:
            conn.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
            conn.commit()
            flash("Categoria cadastrada!", "ok")
    categorias = conn.execute("""
        SELECT categoria.*, COUNT(livro.id) AS qtd
        FROM categoria LEFT JOIN livro ON livro.categoria_id = categoria.id
        GROUP BY categoria.id, categoria.nome ORDER BY categoria.nome
    """).fetchall()
    conn.close()
    return render_template("categorias.html", categorias=categorias)


# DELETE
@app.route("/categorias/<int:id>/excluir", methods=["POST"])
def excluir_categoria(id):
    """UC05 - Gerenciar categorias (excluir). Não exclui se houver livros nela."""
    conn = conectar()
    em_uso = conn.execute("SELECT COUNT(*) FROM livro WHERE categoria_id = ?", (id,)).fetchone()[0]
    if em_uso:
        flash("Não é possível excluir: existem livros nessa categoria.", "erro")
    else:
        conn.execute("DELETE FROM categoria WHERE id = ?", (id,))
        conn.commit()
        flash("Categoria excluída.", "ok")
    conn.close()
    return redirect(url_for("gerenciar_categorias"))


if __name__ == "__main__":
    app.run(debug=True)

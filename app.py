from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import hashlib
import os 

app = Flask(__name__)
UPLOAD_FOLDER = r'C:\xampp\htdocs\imagens-produtos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key="segredo"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

#parte login
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        palavrapasse = request.form['password']
        password = hashlib.sha1(palavrapasse.encode("utf-8")).hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        account = cursor.fetchone()
        cursor.close()

        if account and account['tipo'] == 'administrador':
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect(url_for('dashboard'))

    return render_template("login.html")


# parte da dashboard
@app.route("/dashboard")
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        result = cursor.fetchone()
        total_users = result['total_users'] if result['total_users'] is not None else 0

        cursor.execute("SELECT SUM(stock) AS total_produtos FROM produtos")
        result = cursor.fetchone()
        total_produtos = result['total_produtos'] if result['total_produtos'] is not None else 0

        cursor.execute("SELECT SUM(quantidade) AS total_carrinho FROM carrinho")
        result = cursor.fetchone()
        total_carrinho = result['total_carrinho'] if result['total_carrinho'] is not None else 0

        cursor.execute("SELECT COUNT(*) AS low_stock FROM produtos WHERE stock < 5")
        result = cursor.fetchone()
        low_stock = result['low_stock'] if result['low_stock'] is not None else 0

        cursor.close()

        return render_template(
            "dashboard.html",
            email=session['email'],
            total_users=total_users,
            total_produtos=total_produtos,
            total_carrinho=total_carrinho,
            low_stock=low_stock
        )

    return redirect(url_for('login_page'))




# parte das avaliacoes
@app.route("/avaliacoes")
def avaliacoes():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM avaliacoes ORDER BY data_avaliacao ASC")
        avaliacoes = cursor.fetchall()
        cursor.close()
        return render_template("avaliacoes.html", avaliacoes=avaliacoes)
    return redirect(url_for('login_page'))

@app.route("/produto/<int:produto_id>")
def ver_produto(produto_id):
    return redirect(f"http://localhost/single-product.php?produto_id={produto_id}")

@app.route("/avaliacoes/delete/<int:avaliacao_id>")
def delete_avaliacao(avaliacao_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM avaliacoes WHERE id = %s", (avaliacao_id,))
        mysql.connection.commit()

        cursor.close()
        return redirect(url_for('avaliacoes'))
    return redirect(url_for('login_page'))




#parte do carrinho
@app.route("/carrinhos")
def carrinhos():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute(" SELECT user_id, SUM(quantidade) AS total_produtos, SUM(quantidade * preco_produto) AS preco_total FROM carrinho GROUP BY user_id ")
        carrinhos = cursor.fetchall()
        cursor.close()
        
        return render_template("carrinhos.html", carrinhos=carrinhos)
    return redirect(url_for('login_page'))

@app.route("/single-carrinho/<int:user_id>")
def single_carrinho(user_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(" SELECT * FROM carrinho WHERE user_id = %s", (user_id,))
        carrinho_itens = cursor.fetchall()

        total = sum(item['preco_produto'] * item['quantidade'] for item in carrinho_itens)

        cursor.close()
        return render_template("single-carrinho.html", carrinho_itens=carrinho_itens, total=total)
    return redirect(url_for('login_page'))

@app.route("/carrinho/delete/<int:user_id>")
def delete_carrinho(user_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM carrinho WHERE user_id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('carrinhos'))
    return redirect(url_for('login_page'))




#parte dos contatos
@app.route("/contactos")
def contactos():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM contactos ORDER BY id ASC")
        contactos = cursor.fetchall()
        cursor.close()
        return render_template("contactos.html", contactos=contactos)
    return redirect(url_for('login_page'))

@app.route("/contactos/delete/<int:contacto_id>")
def delete_contacto(contacto_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM contactos WHERE id = %s", (contacto_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('contactos'))
    return redirect(url_for('login_page'))




#parte dos produtso listados
@app.route("/envios")
def envios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM pedidos ORDER BY criado_em ASC")

    envios = cursor.fetchall()
    cursor.close()

    return render_template("envios.html", envios=envios)

@app.route("/envios/delete/<int:envio_id>")
def delete_envio(envio_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (envio_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("envios"))

@app.route("/envios/<int:envio_id>")
def single_envio(envio_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(" SELECT * FROM pedidos WHERE id = %s ", (envio_id,))
    envio = cursor.fetchone()

    if not envio:
        cursor.close()
        return redirect(url_for("envios"))

    cursor.execute(" SELECT nome_produto, quantidade, preco_unitario, subtotal FROM pedido_produtos WHERE pedido_id = %s ", (envio_id,))
    produtos = cursor.fetchall()

    subtotal_pedido = sum(p['subtotal'] for p in produtos)
    taxa_entrega = 50
    total_final = subtotal_pedido + taxa_entrega

    cursor.close()

    return render_template(
        "single-envio.html",
        envio=envio,
        produtos=produtos,
        subtotal_pedido=subtotal_pedido,
        taxa_entrega=taxa_entrega,
        total_final=total_final
    )

@app.route("/envios/toggle/<int:envio_id>")
def toggle_estado_envio(envio_id):
    if 'loggedin' not in session:
        return redirect(url_for('login_page'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT estado FROM pedidos WHERE id = %s", (envio_id,))
    envio = cursor.fetchone()

    if envio:
        novo_estado = "Pago" if envio['estado'] == "PorPagar" else "PorPagar"
        cursor.execute(
            "UPDATE pedidos SET estado = %s WHERE id = %s",
            (novo_estado, envio_id)
        )
        mysql.connection.commit()

    cursor.close()
    return redirect(url_for('envios'))


#parte ddos utilizadores
@app.route("/perfis")
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users ORDER BY id ASC")
        users = cursor.fetchall()
        cursor.close()
        return render_template("perfis.html", users=users)
    return redirect(url_for('login_page'))


@app.route("/perfis/delete/<int:user_id>")
def delete_user(user_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('perfis'))
    return redirect(url_for('login_page'))



#parte ddos produtcos
@app.route("/produtos")
def produtos():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM produtos ORDER BY id ASC")
        produtos = cursor.fetchall()
        cursor.close()
        return render_template("productos.html", produtos=produtos)
    return redirect(url_for('login_page'))

@app.route("/produtos/adicionar", methods=["GET", "POST"])
def add_produto():
    if 'loggedin' not in session:
        return redirect(url_for('login_page'))

    if request.method == "POST":
        nome = request.form['nome']
        categoria = request.form['categoria']
        preco = request.form['preco']
        precopromocional = request.form.get('precopromocional')
        altura = request.form.get('altura')
        largura = request.form.get('largura')
        comprimento = request.form.get('comprimento')
        peso = request.form.get('peso')
        ativo = request.form['ativo']
        stock = request.form['stock']
        marca = request.form['marca']
        cor = request.form['cor']
        descricao = request.form['descricao']

        imagem = request.files['imagem_principal']
        filename = secure_filename(imagem.filename)
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem.save(caminho_imagem)

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO produtos
            (nome, categoria, preco, preco_promocional, altura, largura, comprimento, peso, ativo, stock, marca, cor, descricao, imagem)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            nome, categoria, preco, precopromocional,
            altura, largura, comprimento, peso,
            ativo, stock, marca, cor, descricao, filename
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('produtos'))

    return render_template("add-product.html")


@app.route("/produtos/toggle/<int:produto_id>")
def toggle_produto(produto_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT ativo FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()

        if produto:
            novo_estado = 0 if produto['ativo'] == 1 else 1
            cursor.execute( "UPDATE produtos SET ativo = %s WHERE id = %s", (novo_estado, produto_id))
            mysql.connection.commit()

        cursor.close()
        return redirect(url_for('produtos'))

    return redirect(url_for('login_page'))


@app.route("/produtos/editar/<int:produto_id>", methods=["GET", "POST"])
def editar_produto(produto_id):
    if 'loggedin' not in session:
        return redirect(url_for('login_page'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        cursor.close()
        return redirect(url_for('produtos'))

    if request.method == "POST":
        nome = request.form['nome']
        categoria = request.form['categoria_id']
        preco = request.form['preco']
        precopromocional = request.form.get('precopromocional', None)
        altura = request.form.get('altura', None)
        largura = request.form.get('largura', None)
        comprimento = request.form.get('comprimento', None)
        peso = request.form.get('peso', None)
        ativo = request.form['ativo']
        stock = request.form['stock']
        marca = request.form['marca']
        cor = request.form['cor']
        descricao = request.form['descricao']

        cursor.execute(" UPDATE produtos SET nome=%s, categoria=%s, preco=%s, preco_promocional=%s, altura=%s, largura=%s, comprimento=%s, peso=%s, ativo=%s, stock=%s, marca=%s, cor=%s, descricao=%s WHERE id=%s ", (nome, categoria, preco, precopromocional, altura, largura, comprimento, peso, ativo, stock, marca, cor, descricao, produto_id))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('produtos'))

    cursor.close()
    return render_template("edit-product.html", produto=produto)







# ===========================
# LOGOUT
# ===========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# ===========================
# RODAR O APP
# ===========================
if __name__ == "__main__":
    app.run(debug=True)

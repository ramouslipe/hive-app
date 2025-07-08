from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)

@app.route('/index')
def index_redirect():
    return redirect('/')

@app.route('/')
def index():
    if 'id' not in session:
        return redirect('/login')  # redireciona se não estiver logado

    conn = get_connection()
    cur = conn.cursor()

    # Usuários
    cur.execute("SELECT * FROM Usuario ORDER BY id_usuario;")
    usuarios = cur.fetchall()

    # Avaliações
    cur.execute("""
        SELECT a.id_avaliacao, a.comentario, u.nome, j.titulo
        FROM Avaliacao a
        JOIN Usuario u ON a.id_usuario = u.id_usuario
        JOIN Jogo j ON a.id_jogo = j.id_jogo
        ORDER BY a.id_avaliacao;
    """)
    avaliacoes = cur.fetchall()

    # Desenvolvedoras
    cur.execute("SELECT * FROM Desenvolvedora ORDER BY id_desenvolvedora;")
    desenvolvedoras = cur.fetchall()

    # Jogos
    cur.execute("""
        SELECT j.id_jogo, j.titulo, j.preco, d.nome
        FROM Jogo j
        JOIN Desenvolvedora d ON j.id_desenvolvedora = d.id_desenvolvedora
        ORDER BY j.id_jogo;
    """)
    jogos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html',
        usuarios=usuarios,
        avaliacoes=avaliacoes,
        desenvolvedoras=desenvolvedoras,
        jogos=jogos
    )

# CRUD Usuários

@app.route('/usuarios')
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Usuario ORDER BY id_usuario;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('usuario/index.html', usuarios=usuarios)



@app.route('/usuario/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s);", (nome, email, senha))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    return render_template('usuario/add.html')


@app.route('/usuario/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cur.execute("UPDATE Usuario SET nome=%s, email=%s, senha=%s WHERE id_usuario=%s;", (nome, email, senha, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    cur.execute("SELECT * FROM Usuario WHERE id_usuario = %s;", (id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('usuario/edit.html', usuario=usuario)


@app.route('/usuario/delete/<int:id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Usuario WHERE id_usuario = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


# CRUD Jogos

@app.route('/jogos')
def listar_jogos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT j.id_jogo, j.titulo, j.preco, d.nome 
        FROM Jogo j
        JOIN Desenvolvedora d ON j.id_desenvolvedora = d.id_desenvolvedora
        ORDER BY j.id_jogo;
    """)
    jogos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jogo/index.html', jogos=jogos)

@app.route('/jogos/add', methods=['GET', 'POST'])
def adicionar_jogo():
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        preco = request.form['preco']
        id_desenvolvedora = request.form['id_desenvolvedora']
        cur.execute("INSERT INTO Jogo (titulo, preco, id_desenvolvedora) VALUES (%s, %s, %s);",
                    (titulo, preco, id_desenvolvedora))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/jogos')
    cur.execute("SELECT * FROM Desenvolvedora;")
    devs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jogo/add.html', desenvolvedoras=devs)

@app.route('/jogos/edit/<int:id>', methods=['GET', 'POST'])
def editar_jogo(id):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        preco = request.form['preco']
        id_desenvolvedora = request.form['id_desenvolvedora']
        cur.execute("UPDATE Jogo SET titulo=%s, preco=%s, id_desenvolvedora=%s WHERE id_jogo=%s;",
                    (titulo, preco, id_desenvolvedora, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/jogos')
    cur.execute("SELECT * FROM Jogo WHERE id_jogo = %s;", (id,))
    jogo = cur.fetchone()
    cur.execute("SELECT * FROM Desenvolvedora;")
    devs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jogo/edit.html', jogo=jogo, desenvolvedoras=devs)

@app.route('/jogos/delete/<int:id>')
def deletar_jogo(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Jogo WHERE id_jogo = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/jogos')

@app.route('/avaliacoes')
def listar_avaliacoes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id_avaliacao, a.comentario, u.nome, j.titulo
        FROM Avaliacao a
        JOIN Usuario u ON a.id_usuario = u.id_usuario
        JOIN Jogo j ON a.id_jogo = j.id_jogo
        ORDER BY a.id_avaliacao;
    """)
    avaliacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('avaliacao/index.html', avaliacoes=avaliacoes)

@app.route('/avaliacoes/add', methods=['GET', 'POST'])
def adicionar_avaliacao():
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        comentario = request.form['comentario']
        id_usuario = request.form['id_usuario']
        id_jogo = request.form['id_jogo']
        cur.execute("INSERT INTO Avaliacao (comentario, id_usuario, id_jogo) VALUES (%s, %s, %s);",
                    (comentario, id_usuario, id_jogo))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/avaliacoes')
    cur.execute("SELECT * FROM Usuario;")
    usuarios = cur.fetchall()
    cur.execute("SELECT * FROM Jogo;")
    jogos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('avaliacao/add.html', usuarios=usuarios, jogos=jogos)

@app.route('/avaliacoes/delete/<int:id>')
def deletar_avaliacao(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Avaliacao WHERE id_avaliacao = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/avaliacoes')

@app.route('/developer')
def listar_developers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Desenvolvedora ORDER BY id_desenvolvedora;")
    developers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('developer/index.html', developers=developers)

@app.route('/developer/add', methods=['GET', 'POST'])
def adicionar_developer():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Desenvolvedora (nome,email,senha) VALUES (%s,%s,%s);", (nome,email,senha,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/developer')
    return render_template('developer/add.html')

@app.route('/developer/delete/<int:id>')
def deletar_developer(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Desenvolvedora WHERE id_desenvolvedora = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/developer')

from flask import session, flash, render_template, request, redirect

app.secret_key = 'chave-super-secreta'  # Necessária para usar sessões

from flask import session, flash, render_template, request, redirect

app.secret_key = 'chave-super-secreta'  # já deve existir

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tipo = request.form['tipo']
        email = request.form['email']
        senha = request.form['senha']

        conn = get_connection()
        cur = conn.cursor()

        if tipo == 'usuario':
            cur.execute("SELECT id_usuario, nome FROM Usuario WHERE email = %s AND senha = %s;", (email, senha))
            usuario = cur.fetchone()
            if usuario:
                session['tipo'] = 'usuario'
                session['id'] = usuario[0]
                session['nome'] = usuario[1]
                cur.close()
                conn.close()
                return redirect('/usuario/home')

            else:
                flash('Usuário não encontrado ou senha incorreta.')

        elif tipo == 'developer':
            cur.execute("SELECT id_desenvolvedora, nome FROM Desenvolvedora WHERE email = %s AND senha = %s;", (email, senha))
            dev = cur.fetchone()
            if dev:
                session['tipo'] = 'developer'
                session['id'] = dev[0]
                session['nome'] = dev[1]
                cur.close()
                conn.close()
                return redirect('/developer/home')

            else:
                flash('Desenvolvedor não encontrado ou senha incorreta.')

        cur.close()
        conn.close()

    return render_template('login.html')


@app.route('/usuario/<int:id>')
def perfil_usuario(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, email FROM Usuario WHERE id_usuario = %s;", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return f"<h1>Bem-vindo, {user[0]}</h1><p>Email: {user[1]}</p>"


@app.route('/developer/<int:id>')
def perfil_developer(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM Desenvolvedora WHERE id_desenvolvedora = %s;", (id,))
    dev = cur.fetchone()
    cur.close()
    conn.close()
    return f"<h1>Dev logado: {dev[0]}</h1>"

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.')
    return redirect('/login')

@app.route('/usuario/home')
def usuario_home():
    if session.get('tipo') != 'usuario':
        return redirect('/login')
    return render_template('usuario/home.html', nome=session['nome'])

@app.route('/developer/home')
def developer_home():
    if session.get('tipo') != 'developer':
        return redirect('/login')
    return render_template('developer/home.html', nome=session['nome'])

@app.route('/usuario/biblioteca')
def biblioteca_usuario():
    if session.get('tipo') != 'usuario':
        return redirect('/login')

    id_usuario = session['id']

    conn = get_connection()
    cur = conn.cursor()

    # Primeiro obtemos o ID da biblioteca associada ao usuário
    cur.execute("SELECT id_biblioteca FROM Biblioteca WHERE id_usuario = %s;", (id_usuario,))
    biblioteca = cur.fetchone()

    if not biblioteca:
        cur.close()
        conn.close()
        return render_template('usuario/biblioteca.html', jogos=[])

    id_biblioteca = biblioteca[0]

    # Agora buscamos os jogos da biblioteca
    cur.execute("""
        SELECT j.id_jogo, j.titulo, j.preco, d.nome
        FROM Biblioteca_Jogo bj
        JOIN Jogo j ON bj.id_jogo = j.id_jogo
        JOIN Desenvolvedora d ON j.id_desenvolvedora = d.id_desenvolvedora
        WHERE bj.id_biblioteca = %s;
    """, (id_biblioteca,))
    
    jogos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('usuario/biblioteca.html', jogos=jogos)

@app.route('/usuario/loja', methods=['GET', 'POST'])
def loja_jogos():
    if session.get('tipo') != 'usuario':
        return redirect('/login')

    id_usuario = session['id']
    conn = get_connection()
    cur = conn.cursor()

    # Buscar biblioteca do usuário
    cur.execute("SELECT id_biblioteca FROM Biblioteca WHERE id_usuario = %s;", (id_usuario,))
    biblioteca = cur.fetchone()

    # Se o usuário ainda não tem biblioteca, cria
    if not biblioteca:
        cur.execute("INSERT INTO Biblioteca (id_usuario) VALUES (%s) RETURNING id_biblioteca;", (id_usuario,))
        id_biblioteca = cur.fetchone()[0]
        conn.commit()
    else:
        id_biblioteca = biblioteca[0]

    # Se o usuário enviou compra
    if request.method == 'POST':
        id_jogo = int(request.form['id_jogo'])

        # Registrar compra
        cur.execute("INSERT INTO Compra (id_usuario) VALUES (%s) RETURNING id_compra;", (id_usuario,))
        id_compra = cur.fetchone()[0]

        # Registrar item da compra
        cur.execute("INSERT INTO Item_compra (id_compra, id_jogo) VALUES (%s, %s);", (id_compra, id_jogo))

        # Adicionar o jogo à biblioteca
        cur.execute("INSERT INTO Biblioteca_Jogo (id_biblioteca, id_jogo) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (id_biblioteca, id_jogo))

        conn.commit()
        flash('Jogo comprado e adicionado à sua biblioteca com sucesso!')

    # Buscar todos os jogos disponíveis
    cur.execute("""
        SELECT j.id_jogo, j.titulo, j.preco, d.nome
        FROM Jogo j
        JOIN Desenvolvedora d ON j.id_desenvolvedora = d.id_desenvolvedora
        ORDER BY j.id_jogo;
    """)
    jogos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('usuario/loja.html', jogos=jogos)



if __name__ == '__main__':
    app.run(debug=True)
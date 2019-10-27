from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Jogo, Usuario


app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kukabr123'
app.config['MYSQL_DB'] = 'jogoteca'
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():

    lista = jogo_dao.listar()

    return render_template('lista.html', jogos=lista)

@app.route('/novo')
def novo():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    context = {
        'titulo': 'Novo Jogo'
    }

    return render_template('novo.html', **context)

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario = usuario_dao.buscar_por_id(request.form['usuario'])

    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não Logado, tente novamente!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')

    return redirect(url_for('index'))


app.run(debug=True)
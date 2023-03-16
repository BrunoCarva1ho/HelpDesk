from flask import Flask,render_template,request,redirect,url_for
from bd import mysql
from graf import grafico
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)

# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id
        
#     def get(user_id):
#         return User(user_id)


@app.route('/')
def index():
    return render_template('index.html')


#Função de login no site
@app.route('/entrar.html',methods=['post','get'])
def entrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        with mysql.cursor() as cur:
            #Testa se o login é de um administrador
            cur.execute('SELECT idAdmin FROM admin WHERE email=%s AND senha=%s', (email,senha) )
            id = cur.fetchall()

            #Se o id não foi preenchido
            if id == ():            
                #Procura os dados de email e senha no banco aluno
                cur.execute('SELECT idAluno FROM aluno WHERE email=%s AND senha=%s', (email,senha) )
                id = cur.fetchall()
            # else:
            #     user = User.authenticate(email,senha)
            #     login_user(user)
            #     return render_template('relatos.html',geral=geral,id=id)
                
            #Se o id não foi preenchido
            if id == ():            
                #Procura os dados de email e senha no banco professor
                cur.execute('SELECT idProfessor FROM professor WHERE email=%s AND senha=%s', (email,senha) )
                id = cur.fetchall()
            # else:
            #     user = User.authenticate(email,senha)
            #     login_user(user)
            
            #Se o id foi preenchido
            if id != ():    
                with mysql.cursor() as cur:
                    id = str(id)
                    id = id[2:3]
                    
                    cur.execute('SELECT * FROM relato')
                    geral = cur.fetchall()
                    
                    id = int(id)
                    return render_template('relatos.html',geral=geral,id=id)

    #Usuário e senha não encontrados retorna para a mesma pagina
    return render_template('entrar.html')


# @app.route('/sair')
# @login_required
# def sair():
#     logout_user()
#     return redirect('/')


@app.route('/cadastraraluno.html', methods =['get','POST'])
def cadastrarAluno():
    
    #Testa se é um method de inserção
    if request.method == 'POST':
        nome = request.form['nome']
        curso = request.form['curso']
        email = request.form['email']
        idade = request.form['idade']
        senha = request.form['senha']
        
        #Com o cursor do mysql, executa os comandos de consulta e inserção de dados
        with mysql.cursor() as cur:
            cur.execute('SELECT MAX(idAluno) FROM aluno')   #Consulta para obter o último idAluno cadastrado
            id = cur.fetchmany()
            id = str(id)
            id = id[2:3]
            id = int(id)
            id = id+2   #Faz com que o idAluno seja sempre ímpar
            
            cur.execute('INSERT INTO aluno(nome,curso,email,idade,senha,idAluno) VALUES (%s,%s,%s,%s,%s,%s)',(nome,curso,email,idade,senha,id ))
            cur.connection.commit()
                
            return render_template('entrar.html')
    
    return render_template('cadastraraluno.html')


@app.route('/cadastrarprofessor.html', methods =['get','POST'])
def cadastrarProfessor():
    
    if request.method == 'POST':
        nome = request.form['nome']
        departamento = request.form['departamento']
        email = request.form['email']
        idade = request.form['idade']
        senha = request.form['senha']
        
        with mysql.cursor() as cur:
            cur.execute('SELECT MAX(idProfessor) FROM professor')
            id = cur.fetchmany()
            id = str(id)
            id = id[2:3]
            id = int(id)
            id = id+2
            
            cur.execute('INSERT INTO professor(nome,departamento,email,idade,senha,idProfessor) VALUES (%s,%s,%s,%s,%s,%s)',(nome,departamento,email,idade,senha,id))
            cur.connection.commit()
                
            return render_template('entrar.html')
    
    return render_template('cadastrarprofessor.html')


@app.route('/relatos.html/<int:id>')
def relatos(id):

    grafico()
    
    with mysql.cursor() as cur:
        cur.execute('SELECT * FROM relato')
        geral = cur.fetchall()
    
    return render_template('relatos.html', geral=geral, id=id)

@app.route('/atualizar_grafico/<int:id>')
def atualizar_grafico(id):
    grafico()
    
    with mysql.cursor() as cur:
        cur.execute('SELECT * FROM relato')
        geral = cur.fetchall()
        
    return render_template("relatos.html",geral=geral,id=id)

@app.route('/historico.html/<id>')
def historico(id):
    
    with mysql.cursor() as cur:
        cur.execute("SELECT * FROM relato WHERE idAutor=%s",id)
        geral = cur.fetchall()
        
    return render_template('historico.html',geral=geral,id=id)


@app.route('/novorelato.html/<int:id>', methods=['post','get'])
def novorelato(id):
    
    if request.method == 'POST':
        relato = request.form['relato']
        intensidade = request.form['intensidade']
        frequencia = request.form['frequencia']
        
        with mysql.cursor() as cur:
            cur.execute('INSERT INTO relato (intensidade,frequencia,descricao,idAutor) VALUES (%s,%s,%s,%s)',(intensidade,frequencia,relato,id))
            cur.connection.commit()
            cur.execute('SELECT * FROM relato')
            geral = cur.fetchall()
            
            grafico()
            return render_template("/relatos.html",geral=geral,id=id )
        
    with mysql.cursor() as cur:
        cur.execute('SELECT * FROM relato')
        geral = cur.fetchall()
    
    return render_template("novorelato.html",geral=geral,id=id)


@app.route('/filtro.html/<int:id>', methods=['get','post'])
def filtro(id):
    
    intensidade = request.args.get('intensidade')
    frequencia = request.args.get('frequencia')
    
    if intensidade != '' and frequencia != '':
        with mysql.cursor() as cur:
            cur.execute('SELECT * FROM relato WHERE intensidade=%s AND frequencia=%s',(intensidade,frequencia))
            geral = cur.fetchall()
            return render_template("relatos.html",geral=geral,id=id)
        
    elif intensidade != '' or frequencia != '':
        with mysql.cursor() as cur:
            cur.execute('SELECT * FROM relato WHERE intensidade=%s OR frequencia=%s',(intensidade,frequencia))
            geral = cur.fetchall()
            return render_template("relatos.html",geral=geral,id=id)
    
    with mysql.cursor() as cur:
        cur.execute('SELECT * FROM relato ')
        geral = cur.fetchall()
    
    return render_template("relatos.html",geral=geral,id=id)


@app.route('/excluir/<idRelato>/<int:id>')
def excluir(idRelato,id):
    
    with mysql.cursor() as cur:
        cur.execute("delete FROM relato WHERE idRelato=%s",idRelato)
        cur.connection.commit()
        
        cur.execute('select * from relato')
        geral = cur.fetchall()
    
    
    return render_template("relatos.html", geral=geral, id=id)


@app.route('/excluir_historico/<idRelato>/<int:id>')
def excluir_historico(idRelato,id):
    
    with mysql.cursor() as cur:
        cur.execute("delete FROM relato WHERE idRelato=%s",idRelato)
        cur.connection.commit()
        
        cur.execute('select * from relato')
        geral = cur.fetchall()
    
    
    return render_template("historico.html", geral=geral, id=id)


if __name__ == '__main__':
    app.run(debug=True)

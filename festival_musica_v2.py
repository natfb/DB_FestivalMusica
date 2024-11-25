import mysql.connector
from mysql.connector import errorcode

# dicionario contendo codigo sql para criacao de tableas
tables = {
    'Festival': (
        """ CREATE TABLE Festival (
        cod_festival int PRIMARY KEY
        ) ENGINE=InnoDB """
    ),
    'Palco': (
        """CREATE TABLE Palco (
            cod_palco int PRIMARY KEY,
            nome varchar(100),
            capacidade int,
            local varchar(200),
            cod_festival int,
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Artista': (
        """ CREATE TABLE Artista (
            cod_artista int PRIMARY KEY,
            nome varchar(100),
            genero varchar(100),
            nacionalidade varchar(100)
            ) ENGINE=InnoDB """
    ),
    'Patrocinador': (
        """ CREATE TABLE Patrocinador (
            cod_patrocinador int PRIMARY KEY,
            nome varchar(100),
            tipo varchar(100),
            valor float,
            cod_festival int,
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Ingresso': (
        """ CREATE TABLE Ingresso (
            cod_ingresso int PRIMARY KEY,
            valor float,
            data date,
            tipo varchar(50)
            ) ENGINE=InnoDB """
    ),
    'Participante': (
        """ CREATE TABLE Participante (
            cod_participante int PRIMARY KEY,
            nome varchar(100),
            CPF varchar(14),
            email varchar(100)
            ) ENGINE=InnoDB """
    ),
    'Empresa': (
        """ CREATE TABLE Empresa (
            cod_empresa int PRIMARY KEY,
            valor float,
            cod_festival int,
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Alimentação': (
        """ CREATE TABLE Alimentação (
            local varchar(200),
            horario time,
            nome varchar(100),
            cod_empresa int,
            FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
            ) ENGINE=InnoDB """
    ),
    'Venda': (
        """ CREATE TABLE Venda (
        qtd int,
        cod_venda int PRIMARY KEY,
        cod_participante int,
        FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante)
        ) ENGINE=InnoDB """
    ),
    'Seguranca': (
        """ CREATE TABLE Seguranca (
            nome varchar(100),
            area varchar(100),
            turno varchar(50),
            cod_empresa int,
            FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
            ) ENGINE=InnoDB """
    ),
    'Funcionario': (
        """ CREATE TABLE Funcionario (
            cod_funcionario int PRIMARY KEY,
            nome varchar(100),
            funcao varchar(100),
            horario time,
            cod_empresa int,
            FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
            ) ENGINE=InnoDB """
    ),
    'Festival_Participante': (
        """ CREATE TABLE Festival_Participante (
            cod_participante int,
            cod_festival int,
            avaliacao varchar(50),
            genero_favorito varchar(50),
            genero_festival varchar(50),
            FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante),
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Performance': (
        """ CREATE TABLE Performance (
            hora_inicio time,
            hora_fim time,
            data date,
            cod_performance int PRIMARY KEY,
            cod_artista int,
            cod_palco int,
            FOREIGN KEY(cod_artista) REFERENCES Artista (cod_artista),
            FOREIGN KEY(cod_palco) REFERENCES Palco (cod_palco)
            ) ENGINE=InnoDB """
    ),
    'Venda_Ingresso': (
        """ CREATE TABLE Venda_Ingresso (
            valor float,
            data date,
            tipo varchar(50),
            cod_ingresso int,
            cod_venda int,
            FOREIGN KEY(cod_ingresso) REFERENCES Ingresso (cod_ingresso),
            FOREIGN KEY(cod_venda) REFERENCES Venda (cod_venda)
            ) ENGINE=InnoDB """
    ),
}

inserts = {
    'Festival': ("""
        INSERT INTO Festival (cod_festival) VALUES 
        (1), (2), (3), (4), (5)"""
    ),
    'Palco': ("""
        INSERT INTO Palco (cod_palco, nome, capacidade, local, cod_festival) 
        VALUES 
        (1, 'Palco Principal', 5000, 'Praça Central', 1),
        (2, 'Palco Secundário', 3000, 'Ginásio Local', 1),
        (3, 'Palco Alternativo', 2000, 'Praia do Centro', 2),
        (4, 'Palco VIP', 1500, 'Área VIP', 3),
        (5, 'Palco Sunset', 3500, 'Parque da Cidade', 4)"""
    ),
    'Artista': ("""INSERT INTO Artista (cod_artista, nome, genero, nacionalidade) 
        VALUES 
        (1, 'Banda Rock', 'Rock', 'Brasil'),
        (2, 'Cantor Pop', 'Pop', 'Estados Unidos'),
        (3, 'DJ Eletrônico', 'Eletrônica', 'Alemanha'),
        (4, 'Grupo Jazz', 'Jazz', 'França'),
        (5, 'Orquestra Clássica', 'Clássica', 'Itália'),
        (6, 'Rapper', 'Hip Hop', 'Brasil'),
        (7, 'Cantora Folk', 'Folk', 'Canadá'),
        (8, 'Banda Indie', 'Indie', 'Reino Unido'),
        (9, 'Cantor Sertanejo', 'Sertanejo', 'Brasil'),
        (10, 'Grupo Samba', 'Samba', 'Brasil') """
    ),
    'Patrocinador': ("""
        INSERT INTO Patrocinador (cod_patrocinador, nome, tipo, valor, cod_festival) 
        VALUES 
        (1, 'Marca A', 'Bebidas', 50000.00, 1),
        (2, 'Marca B', 'Alimentos', 30000.00, 2),
        (3, 'Marca C', 'Tecnologia', 70000.00, 3),
        (4, 'Marca D', 'Moda', 20000.00, 4),
        (5, 'Marca E', 'Entretenimento', 60000.00, 5)"""
    ),
    'Ingresso': ("""INSERT INTO Ingresso (cod_ingresso, valor, data, tipo) 
        VALUES 
        (1, 150.00, '2024-11-25', 'VIP'),
        (2, 80.00, '2024-11-26', 'Pista'),
        (3, 200.00, '2024-11-27', 'Camarote'),
        (4, 50.00, '2024-11-28', 'Estudante'),
        (5, 120.00, '2024-11-29', 'Premium')"""
    ),

    'Participante': ("""
        INSERT INTO Participante (cod_participante, nome, CPF, email) 
        VALUES 
        (1, 'João Silva', '123.456.789-00', 'joao@example.com'),
        (2, 'Maria Oliveira', '987.654.321-00', 'maria@example.com'),
        (3, 'Carlos Almeida', '456.789.123-11', 'carlos@example.com'),
        (4, 'Ana Costa', '789.123.456-22', 'ana@example.com'),
        (5, 'Pedro Santos', '321.654.987-33', 'pedro@example.com'),
        (6, 'Clara Nunes', '654.321.987-44', 'clara@example.com'),
        (7, 'Lucas Rocha', '111.222.333-55', 'lucas@example.com'),
        (8, 'Rafael Lima', '222.333.444-66', 'rafael@example.com'),
        (9, 'Larissa Silva', '333.444.555-77', 'larissa@example.com'),
        (10, 'Fernanda Sousa', '444.555.666-88', 'fernanda@example.com'),
        (11, 'Ricardo Araújo', '111.222.333-11', 'ricardo.araujo@example.com'),
        (12, 'Carolina Mendes', '222.333.444-22', 'carolina.mendes@example.com'),
        (13, 'Marcelo Barbosa', '333.444.555-33', 'marcelo.barbosa@example.com'),
        (14, 'Isabela Rocha', '444.555.666-44', 'isabela.rocha@example.com'),
        (15, 'Thiago Ribeiro', '555.666.777-55', 'thiago.ribeiro@example.com'),
        (16, 'Renata Gomes', '666.777.888-66', 'renata.gomes@example.com'),
        (17, 'Bruno Fernandes', '777.888.999-77', 'bruno.fernandes@example.com'),
        (18, 'Patrícia Nunes', '888.999.111-88', 'patricia.nunes@example.com'),
        (19, 'Gustavo Freitas', '999.111.222-99', 'gustavo.freitas@example.com'),
        (20, 'Vanessa Correia', '111.222.333-00', 'vanessa.correia@example.com'),
        (21, 'André Morais', '222.333.444-11', 'andre.morais@example.com'),
        (22, 'Larissa Figueiredo', '333.444.555-22', 'larissa.figueiredo@example.com'),
        (23, 'Rodrigo Silva', '444.555.666-33', 'rodrigo.silva@example.com')"""
    ),
    
    'Empresa': ("""INSERT INTO Empresa (cod_empresa, valor, cod_festival) 
        VALUES 
        (1, 20000.00, 1),
        (2, 15000.00, 2),
        (3, 18000.00, 3),
        (4, 22000.00, 4),
        (5, 25000.00, 5)"""
    ),
    'Alimentação': ("""
        INSERT INTO Alimentação (local, horario, nome, cod_empresa) 
        VALUES 
        ('Praça de Alimentação', '12:00:00', 'Lanchonete A', 1),
        ('Área Gourmet', '18:00:00', 'Restaurante B', 2),
        ('Praça Central', '14:00:00', 'Food Truck C', 3),
        ('Ginásio Local', '20:00:00', 'Cafeteria D', 4),
        ('Parque da Cidade', '13:00:00', 'Hamburgueria E', 5)
    """),
    "Venda": ("""
        INSERT INTO Venda (qtd, cod_venda, cod_participante) 
        VALUES 
        (2, 1, 1),
        (1, 2, 2),
        (3, 3, 3),
        (2, 4, 4),
        (4, 5, 5),
        (1, 6, 6),
        (2, 7, 7),
        (3, 8, 8),
        (1, 9, 9),
        (2, 10, 10)"""
    ),
    "Festival_Participante": ("""INSERT INTO Festival_Participante (cod_participante, cod_festival, avaliacao, genero_favorito, genero_festival) 
    VALUES 
    (1, 1, 'Gostou', 'Rock', 'Rock'), 
    (1, 2, 'Nao Gostou', 'Rock', 'Pop'), 
    (2, 1, 'Gostou', 'Rock', 'Rock'), 
    (2, 3, 'Gostou', 'Samba', 'Samba'), 
    (2, 4, 'Nao Gostou', 'Samba', 'Eletrônica'), 
    (3, 1, 'Gostou', 'Rock', 'Rock'), 
    (3, 2, 'Nao Gostou', 'Eletrônica', 'Pop'), 
    (3, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (4, 2, 'Gostou', 'Pop', 'Pop'), 
    (4, 3, 'Nao Gostou', 'Rock', 'Samba'), 
    (4, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (5, 1, 'Nao Gostou', 'Samba', 'Rock'), 
    (5, 3, 'Gostou', 'Samba', 'Samba'), 
    (6, 2, 'Gostou', 'Pop', 'Pop'), 
    (6, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (7, 1, 'Nao Gostou', 'Eletrônica', 'Rock'), 
    (7, 2, 'Gostou', 'Pop', 'Pop'), 
    (7, 3, 'Gostou', 'Samba', 'Samba'), 
    (7, 4, 'Nao Gostou', 'Rock', 'Eletrônica'),
	(8, 1, 'Gostou', 'Rock', 'Rock'), 
    (8, 2, 'Nao Gostou', 'Rock', 'Pop'), 
    (9, 1, 'Gostou', 'Rock', 'Rock'), 
    (9, 3, 'Gostou', 'Samba', 'Samba'), 
    (9, 4, 'Nao Gostou', 'Samba', 'Eletrônica'), 
    (10, 1, 'Gostou', 'Rock', 'Rock'), 
    (10, 2, 'Nao Gostou', 'Eletrônica', 'Pop'), 
    (10, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (11, 2, 'Gostou', 'Pop', 'Pop'), 
    (11, 3, 'Nao Gostou', 'Rock', 'Samba'), 
    (11, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (12, 1, 'Nao Gostou', 'Samba', 'Rock'), 
    (12, 3, 'Gostou', 'Samba', 'Samba'), 
    (12, 2, 'Gostou', 'Pop', 'Pop'), 
    (12, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (13, 1, 'Nao Gostou', 'Eletrônica', 'Rock'), 
    (13, 2, 'Gostou', 'Pop', 'Pop'), 
    (13, 3, 'Gostou', 'Samba', 'Samba'), 
    (13, 4, 'Nao Gostou', 'Rock', 'Eletrônica'),
	(14, 1, 'Gostou', 'Rock', 'Rock'), 
    (14, 2, 'Nao Gostou', 'Rock', 'Pop'), 
    (15, 1, 'Gostou', 'Rock', 'Rock'), 
    (15, 3, 'Gostou', 'Samba', 'Samba'), 
    (16, 4, 'Nao Gostou', 'Samba', 'Eletrônica'), 
    (17, 1, 'Gostou', 'Rock', 'Rock'), 
    (18, 2, 'Nao Gostou', 'Eletrônica', 'Pop'), 
    (19, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (20, 2, 'Gostou', 'Pop', 'Pop'), 
    (20, 3, 'Nao Gostou', 'Rock', 'Samba'), 
    (20, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (21, 1, 'Nao Gostou', 'Samba', 'Rock'), 
    (21, 3, 'Gostou', 'Samba', 'Samba'), 
    (22, 2, 'Gostou', 'Pop', 'Pop'), 
    (22, 4, 'Gostou', 'Eletrônica', 'Eletrônica'), 
    (23, 1, 'Nao Gostou', 'Eletrônica', 'Rock'), 
    (23, 2, 'Gostou', 'Pop', 'Pop'), 
    (23, 3, 'Gostou', 'Samba', 'Samba'), 
    (23, 4, 'Nao Gostou', 'Rock', 'Eletrônica')"""
    ),

    'Performance': ("""INSERT INTO Performance (hora_inicio, hora_fim, data, cod_performance, cod_artista, cod_palco) 
    VALUES 
    ('18:00:00', '20:00:00', '2024-11-25', 1, 1, 1),
    ('20:30:00', '22:30:00', '2024-11-25', 2, 2, 1),
    ('18:00:00', '20:00:00', '2024-11-26', 3, 3, 2),
    ('21:00:00', '23:00:00', '2024-11-26', 4, 4, 3),
    ('22:00:00', '23:30:00', '2024-11-27', 5, 5, 4),
    ('16:00:00', '18:00:00', '2024-11-27', 6, 6, 5),
    ('19:00:00', '21:00:00', '2024-11-28', 7, 7, 5),
    ('20:00:00', '22:00:00', '2024-11-29', 8, 8, 3) """
    ),
    'Venda_Ingresso': ("""INSERT INTO Venda_Ingresso (valor, data, tipo, cod_ingresso, cod_venda) 
    VALUES 
    (150.00, '2024-11-20', 'VIP', 1, 1),
    (80.00, '2024-11-21', 'Pista', 2, 2),
    (200.00, '2024-11-22', 'Camarote', 3, 3),
    (50.00, '2024-11-23', 'Estudante', 4, 4),
    (120.00, '2024-11-24', 'Premium', 5, 5),
    (150.00, '2024-11-25', 'VIP', 1, 6),
    (80.00, '2024-11-26', 'Pista', 2, 7),
    (200.00, '2024-11-27', 'Camarote', 3, 8),
    (50.00, '2024-11-28', 'Estudante', 4, 9),
    (120.00, '2024-11-29', 'Premium', 5, 10)"""
    )
}

# lista com todos os nomes das tabelas 
# ordem cosidera restricoes de chave primaria para futura exclusao
table_names = ['Alimentação', 'Funcionario', 'Seguranca', 'Empresa', 'Performance', 'Artista', 'Palco', 'Patrocinador', 'Venda_Ingresso', 'Ingresso', 'Venda', 'Festival_Participante', 'Participante', 'Festival']

# dicionario preenchido iterando tables_names para criar codigos drop table
drop = {}
for name in table_names:
    drop[name] = (f"drop table {name}") 
    

# conexao com bando de dados local
def connect_db():
    cnx = mysql.connector.connect(host='localhost', database='festival_musica', user='root', password='admin')
    if cnx.is_connected():
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados", linha[0])
        cursor.close()
    return cnx

# criacao de todas as tabelas
def create_all_tables(connect):
    print("\n---CRIAR TODAS AS TABELAS---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Drop {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def update(connect):
    return 0

def crud(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)


def update_test(connect): 
    return 0

def delete_test(connect):
    return 0

def consulta1(connect):
    # ver quantos cada empresa ganhou com ingressos em todos os festivais. 
    return 0

def consulta2(connect):
    # ver todos vestivais que um artista ja participou. n da grafico
    # ver vestivais que irao ocorrer em tal data e tal cidade. facil
    # ver quantos artistas um festival tem. x festival y n artistas. facil
    # Quantidade de ingressos vendidos em cada data
    # um participante ver quando ele comprou ingressos, data etc. facil
    return 0

def consulta3(connect):
    # valor gasto por cada participante com ingressos
    select_query = """SELECT 
        p.nome AS Nome_Participante,
        SUM(i.valor) AS Total_Gasto
    FROM 
        Participante p
    JOIN 
        Venda v ON p.cod_participante = v.cod_participante
    JOIN 
        Venda_Ingresso vi ON v.cod_venda = vi.cod_venda
    JOIN 
        Ingresso i ON vi.cod_ingresso = i.cod_ingresso
    GROUP BY 
        p.nome; """
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    return 0


def consulta_extra(connect):
    return 0

def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()

def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuído: ")
        codigo_f = input("Digite a coluna da chave primária: ")
        codigo = input("Digite o valor numérico do campo da chave primária: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão com o banco de dados foi encerrada!")
    

def ia_model(connect):
    
    import pandas as pd
    from sqlalchemy import create_engine
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    
    # Configurar a conexão com o banco de dados usando SQLAlchemy
    conexao = create_engine("mysql+pymysql://root:admin@localhost/festival_musica")

    query = "SELECT * FROM festival_participante"
    df = pd.read_sql(query, conexao)

    df.to_csv('festival_participante.csv', index=False)
    
    #CRIANDO MODELO
    ds = pd.read_csv("./festival_participante.csv")
    ds.head()

    #Entradas em X e saída em Y
    y = ds.iloc[:, 2].values

    ds.drop(columns=['cod_festival', 'avaliacao'], axis=1, inplace=True)
    ds.head()

    X = ds.iloc[:, 0:3].values

    genero_favorito = LabelEncoder()
    genero_festival = LabelEncoder()
    avaliacao = LabelEncoder()

    X[:, 1] = genero_favorito.fit_transform(X[:, 1])

    X[:, 2] = genero_festival.fit_transform(X[:, 2])

    y = avaliacao.fit_transform(y)

    entrada = X[:-1]

    saida = y[:-1]

    #Dividindo a base em dados de teste e dados de treinamento
    entrada_treino, entrada_teste, saida_treino, saida_teste = train_test_split(entrada, saida, random_state=0, train_size=0.75)

    # Treinando o modelo RandomForestClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(entrada_treino, saida_treino)

    # Fazendo previsões
    saida_pred = model.predict(entrada_teste)

    # Avaliando o modelo
    accuracy = accuracy_score(saida_teste, saida_pred)
    print(f"Acurácia do modelo: {accuracy:.2f}")

    saida_y = y[-1];
    entrada_X = X[-1];

    # Fazendo a previsão
    avaliacao_prevista = model.predict(entrada_X.reshape(1, -1))
    avaliacao_prevista

    print(f"Cliente irá gostar do próximo festival?: {'Provavelmente Sim' if avaliacao_prevista[0] == 0 else 'Provavelmente Não'}")
    
    if entrada_X[2] == 0:
        print('O gênero do festival é: Eletrônica')
    elif entrada_X[2] == 1:
        print('O gênero do festival é: Pop')
    elif entrada_X[2] == 2:
        print('O gênero do festival é: Rock')
    elif entrada_X[2] == 3:
        print('O gênero do festival é: Samba')
    
    if entrada_X[1] == 0:
        print('O participante prefere música Eletrônica')
    elif entrada_X[1] == 1:
        print('O participante prefere música Pop')
    elif entrada_X[1] == 2:
        print('O participante prefere ouvir bandas de Rock')
    elif entrada_X[1] == 3:
        print('O participante prefere ouvir Samba')
        

def limpar_terminal():
    
    import os
    # Limpa a tela dependendo do sistema operacional
    # os.system('cls' if os.name == 'nt' else 'clear')
    

# Main
try:
    
    limpar_terminal()
    
    # Estabelece Conexão com o DB
    con = connect_db()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD
        2.  TESTE - Create all tables
        3.  TESTE - Insert all values
        4.  TESTE - Update
        5.  TESTE - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. CONSULTA TABELAS INDIVIDUAIS
        11. UPDATE VALUES
        12. CLEAR ALL RESGATOCAO
        13. IA
        0.  DISCONNECT DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 13:
            print("Erro tente novamente!")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigada(o).")
                break
            else:
                break

        if choice == 1:
            crud(con)

        if choice == 2:
            limpar_terminal()
            create_all_tables(con)

        if choice == 3:
            limpar_terminal()
            insert_test(con)

        if choice == 4:
            limpar_terminal()
            update_test(con)

        if choice == 5:
            limpar_terminal()
            delete_test(con)

        if choice == 6:
            limpar_terminal()
            consulta1(con)

        if choice == 7:
            limpar_terminal()
            consulta2(con)

        if choice == 8:
            limpar_terminal()
            consulta3(con)

        if choice == 9:
            limpar_terminal()
            consulta_extra(con)

        if choice == 10:
            limpar_terminal()
            show_table(con)

        if choice == 11:
            limpar_terminal()
            update_value(con)

        if choice == 12:
            limpar_terminal()
            drop_all_tables(con)
            
        if choice == 13:
            limpar_terminal()
            ia_model(con)
            limpar_terminal()

    con.close()

except mysql.connector.Error as err:
    print("Erro na conexão com o banco de dados!", err.msg)
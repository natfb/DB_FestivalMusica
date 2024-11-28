import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import matplotlib.pyplot as plt 
# dicionario contendo codigo sql para criacao de tableas
tables = {
    'Festival': (
        """ CREATE TABLE Festival (
        cod_festival int PRIMARY KEY,
        nome varchar(100),
        cidade varchar(100),
        estado varchar(100),
        endereco varchar(100),
        data_fim date,
        genero_festival varchar(50),
        data_inicio date
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
            data date,
            tipo varchar(50),
            valor float,
            cod_festival int,
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Participante': (
        """ CREATE TABLE Participante (
            cod_participante int PRIMARY KEY,
            nome varchar(200),
            CPF varchar(14),
            email varchar(100),
            genero_favorito varchar(50)
            ) ENGINE=InnoDB """
    ),
    'Empresa': (
        """ CREATE TABLE Empresa (
            cod_empresa int PRIMARY KEY,
            nome varchar(100),
            cnpj varchar(18),
            cod_festival int,
            FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
            ) ENGINE=InnoDB """
    ),
    'Alimentacao': (
        """ CREATE TABLE Alimentacao (
            local varchar(200),
            horario time,
            cod_empresa int,
            FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
            ) ENGINE=InnoDB """
    ),
    'Venda': (
        """ CREATE TABLE Venda (
        qtd int,
        cod_venda int PRIMARY KEY,
        cod_participante int,
        cod_ingresso int,
        FOREIGN KEY(cod_ingresso) REFERENCES Ingresso (cod_ingresso),
        FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante)
        ) ENGINE=InnoDB """
    ),
    'Seguranca': (
        """ CREATE TABLE Seguranca (
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
    'Avaliacao': """CREATE TABLE Avaliacao (
        cod_avaliacao int PRIMARY KEY,
        descricao varchar(14),
        cod_participante int,
        cod_festival int,
        FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante),
        FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
    )"""
}

inserts = {
    'Festival': ("""
        INSERT INTO Festival (cod_festival, nome, cidade, estado, endereco, data_fim, genero_festival, data_inicio)
        VALUES
        (1, 'Rock in Rio', 'Rio de Janeiro', 'RJ', 'Av. Atlântica, 1000', '2024-12-05', 'Rock', '2024-12-01'),
        (2, 'Xxxperience Festival','São Paulo', 'SP', 'Parque Ibirapuera', '2024-11-30', 'Eletrônico', '2024-11-28'),
        (3, 'Jazz na Serra', 'Teresópolis', 'RJ', 'Praça do Alto', '2024-09-15', 'Jazz', '2024-09-12'),
        (4, 'Forró das Estrelas', 'Campina Grande', 'PB', 'Centro de Eventos', '2024-06-25', 'Forró', '2024-06-20'),
        (5, 'Pop in the Park', 'Curitiba', 'PR', 'Parque Barigui', '2024-10-10', 'Pop', '2024-10-07');"""
    ),
    'Palco': ("""
        INSERT INTO Palco (cod_palco, nome, capacidade, local, cod_festival) 
        VALUES 
        (1, 'Palco Principal', 5000, 'Praça Central', 3),
        (2, 'Palco Secundário', 3000, 'Ginásio Local', 3),
        (3, 'Palco Alternativo', 2000, 'Praia do Centro', 4),
        (4, 'Palco VIP', 1500, 'Área VIP', 5),
        (5, 'Palco Sunset', 3500, 'Parque da Cidade', 4);"""
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
        (10, 'Grupo Samba', 'Samba', 'Brasil'); """
    ),
    'Patrocinador': ("""
        INSERT INTO Patrocinador (cod_patrocinador, nome, tipo, valor, cod_festival) 
        VALUES 
        (1, 'Marca A', 'Bebidas', 50000.00, 5),
        (2, 'Marca B', 'Alimentos', 30000.00, 4),
        (3, 'Marca C', 'Tecnologia', 70000.00, 3),
        (4, 'Marca D', 'Moda', 20000.00, 4),
        (5, 'Marca E', 'Entretenimento', 60000.00, 5);"""
    ),
    'Ingresso': ("""
        INSERT INTO Ingresso (cod_ingresso, data, tipo, valor, cod_festival)
        VALUES
        (4, '2024-09-12', 'Pista', 100.00, 3),
        (5, '2024-06-20', 'Pista', 80.00, 4),
        (6, '2024-10-07', 'Pista', 120.00, 5),
        (7, '2024-12-02', 'Camarote', 300.00, 1),
        (8, '2024-11-29', 'VIP', 250.00, 2),
        (9, '2024-09-12', 'Pista', 100.00, 3),
        (10, '2024-09-12', 'Pista', 100.00, 3),
        (11, '2024-06-20', 'Pista', 80.00, 4),
        (12, '2024-10-07', 'Pista', 120.00, 5),
        (13, '2024-12-02', 'Camarote', 300.00, 1),
        (14, '2024-11-29', 'VIP', 250.00, 2),
        (15, '2024-09-12', 'Pista', 100.00, 3),
        (16, '2024-09-12', 'Pista', 100.00, 3),
        (17, '2024-06-20', 'Pista', 80.00, 4),
        (18, '2024-09-12', 'Pista', 100.00, 3),
        (19, '2024-10-07', 'Pista', 120.00, 5),
        (20, '2024-10-07', 'Pista', 120.00, 5),
        (21, '2024-12-02', 'Camarote', 300.00, 1),
        (22, '2024-09-12', 'Pista', 100.00, 3),
        (23, '2024-11-29', 'VIP', 250.00, 2),
        (24, '2024-09-12', 'Pista', 100.00, 3);"""
    ),

    'Participante': ("""
        INSERT INTO Participante (cod_participante, nome, CPF, email, genero_favorito)
        VALUES
        (1, 'Ana Silva', '123.456.789-00', 'ana@gmail.com', 'Rock'),
        (2, 'Carlos Pereira', '987.654.321-00', 'carlos@gmail.com', 'Eletrônico'),
        (3, 'Maria Oliveira', '321.654.987-00', 'maria.oliveira@gmail.com', 'Jazz'),
        (4, 'Pedro Santos', '741.852.963-00', 'pedro.santos@gmail.com', 'Forró'),
        (5, 'Joana Costa', '159.357.486-00', 'joana.costa@gmail.com', 'Pop'),
        (6, 'Lucas Almeida', '753.951.456-00', 'lucas.almeida@gmail.com', 'Rock'),
        (7, 'Fernanda Ribeiro', '987.321.654-00', 'fernanda.ribeiro@gmail.com', 'Eletrônico'),
        (8, 'Gabriel Lima', '654.987.321-00', 'gabriel.lima@gmail.com', 'MPB'),
        (9, 'Laura Nunes', '852.963.741-00', 'laura.nunes@gmail.com', 'Jazz'),
        (10, 'Rafael Souza', '123.789.456-00', 'rafael.souza@gmail.com', 'Forró'),
        (11, 'Beatriz Andrade', '456.321.789-00', 'beatriz.andrade@gmail.com', 'Pop'),
        (12, 'Thiago Mendes', '963.852.741-00', 'thiago.mendes@gmail.com', 'Rock'),
        (13, 'Juliana Barros', '147.258.369-00', 'juliana.barros@gmail.com', 'Eletrônico'),
        (14, 'Eduardo Martins', '369.258.147-00', 'eduardo.martins@gmail.com', 'Samba'),
        (15, 'Clara Fernandes', '159.753.486-00', 'clara.fernandes@gmail.com', 'Jazz'),
        (16, 'Henrique Gomes', '789.456.123-00', 'henrique.gomes@gmail.com', 'Forró'),
        (17, 'Sofia Carvalho', '321.654.987-11', 'sofia.carvalho@gmail.com', 'MPB'),
        (18, 'André Vasconcelos', '753.951.456-22', 'andre.vasconcelos@gmail.com', 'Samba'),
        (19, 'Isabela Rocha', '951.753.456-00', 'isabela.rocha@gmail.com', 'Pop'),
        (20, 'Leonardo Azevedo', '852.741.963-00', 'leonardo.azevedo@gmail.com', 'Rock'),
        (21, 'Paula Correia', '654.321.987-00', 'paula.correia@gmail.com', 'Jazz'),
        (22, 'Bruno Vieira', '369.147.258-00', 'bruno.vieira@gmail.com', 'Eletrônico'),
        (23, 'Vanessa Moreira', '789.123.456-00', 'vanessa.moreira@gmail.com', 'MPB');"""
    ),
    'Empresa': ("""
        INSERT INTO Empresa (cod_empresa, nome, cnpj, cod_festival)
        VALUES
        (1, 'Food Fast', '12.345.678/0001-99', 1),
        (2, 'SecurePro', '98.765.432/0001-11', 2);"""
    ),
    'Alimentacao': ("""
        INSERT INTO Alimentacao (local, horario, cod_empresa)
        VALUES
        ('Área Gourmet', '12:00:00', 1),
        ('Food Truck Central', '11:30:00', 1),
        ('Quiosque Leste', '13:00:00', 1),
        ('Zona Oeste - Bebidas', '10:00:00', 1);
    """),
    'Seguranca': ("""
        INSERT INTO Seguranca (area, turno, cod_empresa)
        VALUES
        ('Entrada Principal', 'Diurno', 2),
        ('Palco Principal', 'Noturno', 2),
        ('Área de Camping', 'Diurno', 2),
        ('Estacionamento', 'Noturno', 2);
    """),
    "Venda": ("""
        INSERT INTO Venda (qtd, cod_venda, cod_participante, cod_ingresso)
        VALUES
        (1, 3, 3, 4),
        (1, 4, 4, 5),
        (1, 5, 5, 6),
        (1, 6, 6, 7),
        (1, 7, 7, 8),
        (1, 8, 8, 9),
        (1, 9, 9, 10),
        (1, 10, 10, 11),
        (1, 11, 11, 12),
        (1, 12, 12, 13),
        (1, 13, 13, 14),
        (1, 14, 14, 15),
        (1, 15, 15, 16),
        (1, 16, 16, 17),
        (1, 17, 17, 18),
        (1, 18, 18, 19),
        (1, 19, 19, 20),
        (2, 20, 20, 21),
        (1, 21, 21, 22),
        (1, 22, 22, 23),
        (1, 23, 23, 24);"""
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
        ('20:00:00', '22:00:00', '2024-11-29', 8, 8, 3); """
    ),
    "Avaliacao": """
        INSERT INTO Avaliacao (cod_avaliacao, descricao, cod_participante, cod_festival)
        VALUES
        (1, 'Gostou', 3, 3),
        (2, 'Não gostou', 4, 4),
        (3, 'Gostou', 5, 5),
        (4, 'Não gostou', 6, 1),
        (5, 'Não gostou', 7, 2),
        (6, 'Gostou', 8, 3),
        (7, 'Não gostou', 9, 4),
        (8, 'Não gostou', 10, 5),
        (9, 'Não gostou', 11, 1),
        (10, 'Gostou', 12, 2),
        (11, 'Gostou', 13, 3),
        (12, 'Não gostou', 14, 4),
        (13, 'Gostou', 15, 5),
        (14, 'Não gostou', 16, 1),
        (15, 'Gostou', 17, 2),
        (16, 'Gostou', 18, 3),
        (17, 'Gostou', 19, 4),
        (18, 'Não gostou', 20, 5),
        (19, 'Gostou', 21, 1),
        (20, 'Não gostou', 22, 2),
        (21, 'Gostou', 23, 3);""",
    "Funcionario": ("""
        INSERT INTO Funcionario (cod_funcionario, nome, funcao, horario, cod_empresa)
        VALUES
        (1, 'João Silva', 'Segurança', '18:00:00', 2);""")
}

# lista com todos os nomes das tabelas 
# ordem cosidera restricoes de chave primaria para futura exclusao
table_names = ['Alimentacao', 'Funcionario', 'Seguranca', 'Empresa', 'Performance', 'Artista', 'Palco', 'Patrocinador', 'Venda', 'Ingresso', 'Avaliacao', 'Participante', 'Festival']

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
    select_query = """
    SELECT fes.nome, COUNT(*) as num_artistas
    FROM Festival as fes, Palco as p, Performance as per, Artista as ar
    WHERE fes.cod_festival = p.cod_festival and p.cod_palco = per.cod_palco and per.cod_artista = ar.cod_artista 
    GROUP BY(fes.nome)
    """
    print("\nConsulta 1\nMostrar a quantidade de artistas que irão performar em cada festival.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    for x in result:
        print(x)

    nome_festival = [row[0] for row in result]
    qnt_artistas = [row[1] for row in result]
    print(type(nome_festival), type(qnt_artistas))
    plt.figure(figsize=(10, 6))
    plt.bar(nome_festival, qnt_artistas)

    plt.title('Número de Artistas por Festival')
    plt.xlabel('Nome do Festival')
    plt.ylabel('Número de Artistas')

    plt.xticks(rotation=45, ha="right")

    # plt.tight_layout()
    plt.show()


def consulta2(connect):
    # ver quantos cada empresa ganhou com ingressos em todos os festivais.
    # ver todos vestivais que um artista ja participou. n da grafico
    # ver vestivais que irao ocorrer em tal data e tal cidade. facil
    # ver quantos artistas um festival tem. x festival y n artistas. facil
    # Quantidade de ingressos vendidos em cada data
    # um participante ver quando ele comprou ingressos, data etc. facil
    select_query = """
    SELECT fes.nome, SUM(i.valor * v.qtd) as total
    FROM Festival as fes, Ingresso as i, Venda as v
    WHERE fes.cod_festival = i.cod_festival and i.cod_ingresso = v.cod_ingresso 
    GROUP BY(fes.nome)
    """
    print("\nConsulta 2\nMostrar o valor total que cada festival lucrou com a venda de ingressos.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    for x in result:
        print(x)

    festivais = [row[0] for row in result]
    totais = [row[1] for row in result]

    plt.figure(figsize=(10, 6))
    plt.bar(festivais, totais, color='teal')

    plt.title("Total Arrecadado por Festival", fontsize=16)
    plt.xlabel("Festivais", fontsize=14)
    plt.ylabel("Valor Total (R$)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    plt.show()


def consulta3(connect):
    # valor gasto por cada participante com ingressos
    select_query = """
    SELECT 
    f.nome AS festival, 
    COUNT(DISTINCT CASE WHEN av.descricao = 'gostou' THEN av.cod_participante END) AS avaliacoes_positivas,
    COUNT(DISTINCT av.cod_avaliacao) AS total_avaliacoes
    FROM Festival as f
    LEFT JOIN Avaliacao av ON f.cod_festival = av.cod_festival
    LEFT JOIN Participante p ON av.cod_participante = p.cod_participante
    GROUP BY f.nome;
    """
    print("\nConsulta 2\nMostrar, para cada festival quantos participantes deixaram uma avaliação e quantas delas foram positivas.")
    # add qnts ele foi tb? n sei faezr
    cursor = connect.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    for x in result:
        print(x)
    
    # grafico
    festivais = [row[0] for row in result]
    avaliacoes_positivas = [row[1] for row in result]
    total_participantes = [row[2] for row in result]

    plt.figure(figsize=(10, 6))
    x = range(len(festivais))

    plt.bar(x, avaliacoes_positivas, width=0.4, label="Avaliações Positivas", color="green")

    plt.bar([i + 0.4 for i in x], total_participantes, width=0.4, label="Total de Participantes", color="blue")

    plt.xticks([i + 0.2 for i in x], festivais, rotation=45)
    plt.ylabel("Quantidade")
    plt.xlabel("Festivais")
    plt.title("Comparação de Avaliações Positivas e Total de Participantes por Festival")
    plt.legend()

    plt.tight_layout()
    plt.show()


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
        12. CLEAR ALL
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
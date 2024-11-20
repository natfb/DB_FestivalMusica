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
        (10, 'Fernanda Sousa', '444.555.666-88', 'fernanda@example.com')
    """),
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
    "Festival_Participante": ("""
    INSERT INTO Festival_Participante (cod_participante, cod_festival) 
    VALUES 
    (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 2), (7, 3), (8, 3), (9, 4), (10, 5);
    """
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
    return 0

def update_test(connect): 
    return 0

def delete_test(connect):
    return 0

def consulta1(connect):
    return 0

def consulta2(connect):
    return 0

def consulta3(connect):
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
    return 0

def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão com o banco de dados foi encerrada!")

# Main
try:
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
        0.  DISCONNECT DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 12:
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
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            consulta_extra(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

    con.close()

except mysql.connector.Error as err:
    print("Erro na conexão com o banco de dados!", err.msg)
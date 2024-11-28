-- Geração de Modelo físico
-- Sql ANSI 2003 - brModelo.



CREATE TABLE Palco (
cod_palco Texto(1) PRIMARY KEY,
nome Texto(1),
capacidade Texto(1),
local Texto(1),
cod_festival Texto(1)
)

CREATE TABLE Artista (
cod_artista Texto(1) PRIMARY KEY,
nome Texto(1),
genero Texto(1),
nacionalidade Texto(1)
)

CREATE TABLE Ingresso (
cod_ingresso Texto(1) PRIMARY KEY,
data Texto(1),
tipo Texto(1),
valor Texto(1)
)

CREATE TABLE Venda (
qtd Texto(1),
cod_venda Texto(1) PRIMARY KEY,
cod_participante Texto(1),
cod_ingresso Texto(1),
FOREIGN KEY(cod_ingresso) REFERENCES Ingresso (cod_ingresso)
)

CREATE TABLE Participante (
cod_participante Texto(1) PRIMARY KEY,
nome Texto(1),
CPF Texto(1),
email Texto(1),
genero_favorito Texto(1)
)

CREATE TABLE Funcionario (
cod_funcionario Texto(1) PRIMARY KEY,
nome Texto(1),
funcao Texto(1),
horario Texto(1),
cod_empresa Texto(1)
)

CREATE TABLE Festival (
cod_festival Texto(1) PRIMARY KEY,
cidade Texto(1),
estado Texto(1),
endereco Texto(1),
data_fim Texto(1),
genero_festival Texto(1),
data_inicio Texto(1)
)

CREATE TABLE Patrocinador (
cod_patrocinador Texto(1) PRIMARY KEY,
nome Texto(1),
tipo Texto(1),
valor Texto(1),
cod_festival Texto(1),
FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
)

CREATE TABLE Empresa (
cod_empresa Texto(1) PRIMARY KEY,
nome Texto(1),
cnpj Texto(1),
cod_festival Texto(1),
FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
)

CREATE TABLE Alimentacao (
local Texto(1),
horario Texto(1),
cod_empresa Texto(1),
FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
)

CREATE TABLE Seguranca (
area Texto(1),
turno Texto(1),
cod_empresa Texto(1),
FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)
)

CREATE TABLE Performance (
hora_inicio Texto(1),
hora_fim Texto(1),
data Texto(1),
cod_performance Texto(1) PRIMARY KEY,
cod_artista Texto(1),
cod_palco Texto(1),
FOREIGN KEY(cod_artista) REFERENCES Artista (cod_artista),
FOREIGN KEY(cod_palco) REFERENCES Palco (cod_palco)
)

CREATE TABLE Festival_Ingresso (
cod_ingresso Texto(1),
cod_festival Texto(1),
FOREIGN KEY(cod_ingresso) REFERENCES Ingresso (cod_ingresso),
FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
)

CREATE TABLE Avaliacao (
cod_avaliacao Texto(1) PRIMARY KEY,
descricao Texto(1),
cod_participante Texto(1),
cod_festival Texto(1),
FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante),
FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
)

ALTER TABLE Palco ADD FOREIGN KEY(cod_festival) REFERENCES Festival (cod_festival)
ALTER TABLE Venda ADD FOREIGN KEY(cod_participante) REFERENCES Participante (cod_participante)
ALTER TABLE Funcionario ADD FOREIGN KEY(cod_empresa) REFERENCES Empresa (cod_empresa)

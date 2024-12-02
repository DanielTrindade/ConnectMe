CREATE DATABASE connectme;
USE connectme;

CREATE TABLE ESTADO (
   estado_id INT AUTO_INCREMENT PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   uf CHAR(2) NOT NULL
);

CREATE TABLE MUNICIPIO (
   municipio_id INT AUTO_INCREMENT PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   estado_id INT NOT NULL,
   FOREIGN KEY (estado_id) REFERENCES ESTADO(estado_id)
);

CREATE TABLE USUARIO (
   usuario_id INT AUTO_INCREMENT PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   apelido VARCHAR(100) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   senha VARCHAR(255) NOT NULL,
   foto VARCHAR(255),
   biografia TEXT,
   data_nascimento DATE NOT NULL,
   municipio_id INT NOT NULL,
   FOREIGN KEY (municipio_id) REFERENCES MUNICIPIO(municipio_id)
);

CREATE TABLE GRUPO (
   grupo_id INT AUTO_INCREMENT PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   descricao TEXT,
   data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE POSTAGEM (
   postagem_id INT AUTO_INCREMENT PRIMARY KEY,
   conteudo TEXT NOT NULL,
   data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   tipo_midia VARCHAR(50),
   midia VARCHAR(255),
   usuario_id INT NOT NULL,
   grupo_id INT,
   FOREIGN KEY (usuario_id) REFERENCES USUARIO(usuario_id),
   FOREIGN KEY (grupo_id) REFERENCES GRUPO(grupo_id)
);

CREATE TABLE MENSAGEM (
   mensagem_id INT AUTO_INCREMENT PRIMARY KEY,
   conteudo TEXT NOT NULL,
   data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   remetente_id INT NOT NULL,
   destinatario_id INT NOT NULL,
   FOREIGN KEY (remetente_id) REFERENCES USUARIO(usuario_id),
   FOREIGN KEY (destinatario_id) REFERENCES USUARIO(usuario_id)
);

CREATE TABLE CONEXAO (
   conexao_id INT AUTO_INCREMENT PRIMARY KEY,
   data_conexao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   usuario_id1 INT NOT NULL,
   usuario_id2 INT NOT NULL,
   FOREIGN KEY (usuario_id1) REFERENCES USUARIO(usuario_id),
   FOREIGN KEY (usuario_id2) REFERENCES USUARIO(usuario_id)
);

CREATE TABLE INTERACAO (
   interacao_id INT AUTO_INCREMENT PRIMARY KEY,
   tipo VARCHAR(50) NOT NULL,
   data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   usuario_id INT NOT NULL,
   postagem_id INT NOT NULL,
   FOREIGN KEY (usuario_id) REFERENCES USUARIO(usuario_id),
   FOREIGN KEY (postagem_id) REFERENCES POSTAGEM(postagem_id)
);

CREATE TABLE MEMBRO_GRUPO (
   membro_id INT AUTO_INCREMENT PRIMARY KEY,
   papel VARCHAR(50) NOT NULL,
   data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   usuario_id INT NOT NULL,
   grupo_id INT NOT NULL,
   FOREIGN KEY (usuario_id) REFERENCES USUARIO(usuario_id),
   FOREIGN KEY (grupo_id) REFERENCES GRUPO(grupo_id)
);

CREATE INDEX idx_usuario_nome ON USUARIO(nome);
CREATE INDEX idx_postagem_data ON POSTAGEM(data_criacao);
CREATE INDEX idx_mensagem_data ON MENSAGEM(data_envio);
CREATE INDEX idx_conexao_usuarios ON CONEXAO(usuario_id1, usuario_id2);
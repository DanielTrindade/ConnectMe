from faker import Faker
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import os
from tqdm import tqdm
import argparse
import sys

load_dotenv()

fake = Faker('pt_BR')

def connect_db():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        sys.exit(1)

def populate_estados(cursor):
    estados = [['Acre','AC'], ['Alagoas','AL'], ['Amapá','AP'], ['Amazonas','AM'], 
               ['Bahia','BA'], ['Ceará','CE'], ['Distrito Federal','DF'], 
               ['Espírito Santo','ES'], ['Goiás','GO'], ['Maranhão','MA'], 
               ['Mato Grosso','MT'], ['Mato Grosso do Sul','MS'], 
               ['Minas Gerais','MG'], ['Pará','PA'], ['Paraíba','PB'], 
               ['Paraná','PR'], ['Pernambuco','PE'], ['Piauí','PI'], 
               ['Rio de Janeiro','RJ'], ['Rio Grande do Norte','RN'], 
               ['Rio Grande do Sul','RS'], ['Rondônia','RO'], ['Roraima','RR'], 
               ['Santa Catarina','SC'], ['São Paulo','SP'], ['Sergipe','SE'], 
               ['Tocantins','TO']]
    estado_ids = []
    for estado in tqdm(estados, desc="🌍 Populando estados ", unit="estado"):
        cursor.execute("INSERT INTO ESTADO (nome, uf) VALUES (%s, %s)", 
                      (estado[0], estado[1]))
        estado_ids.append(cursor.lastrowid)
    return estado_ids

def populate_municipios(cursor, estado_ids, num_municipios=500):
    municipio_ids = []
    for _ in tqdm(range(num_municipios), desc="🏘️ Populando municípios ", unit="município"):
        estado_id = random.choice(estado_ids)
        cursor.execute("INSERT INTO MUNICIPIO (nome, estado_id) VALUES (%s, %s)",
                      (fake.city(), estado_id))
        municipio_ids.append(cursor.lastrowid)
    return municipio_ids

def populate_usuarios(cursor, municipio_ids, num_usuarios=3000):
   usuarios = []
   
   for _ in tqdm(range(num_usuarios), desc="👤 Populando usuários ", unit="usuário"):
       email = fake.unique.email()
       data_nascimento = fake.date_of_birth(minimum_age=13, maximum_age=80)
       usuario = (
           fake.name(),
           fake.first_name(),
           email,
           fake.password(),
           fake.image_url(),
           fake.text(max_nb_chars=200),
           random.choice(municipio_ids),
           data_nascimento
       )
       
       cursor.execute("""
           INSERT INTO USUARIO (nome, apelido, email, senha, foto, biografia, 
                               municipio_id, data_nascimento)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """, usuario)
       usuarios.append(cursor.lastrowid)
           
   return usuarios

def populate_grupos(cursor, num_grupos=300):
    grupos = []
    for _ in tqdm(range(num_grupos), desc="👥 Populando grupos", unit="grupo"):
        grupo = (fake.company(), fake.text(max_nb_chars=200))
        cursor.execute("INSERT INTO GRUPO (nome, descricao) VALUES (%s, %s)", grupo)
        grupos.append(cursor.lastrowid)
    return grupos

def populate_membros_grupo(cursor, usuario_ids, grupo_ids, num_membros=3000):
    papeis = ['admin', 'moderador', 'membro']
    for _ in tqdm(range(num_membros), desc="🤝 Populando membros ", unit="membro"):
        membro = (
            random.choice(papeis),
            random.choice(usuario_ids),
            random.choice(grupo_ids)
        )
        try:
            cursor.execute("""
                INSERT INTO MEMBRO_GRUPO (papel, usuario_id, grupo_id)
                VALUES (%s, %s, %s)
            """, membro)
        except mysql.connector.Error:
            continue

def populate_postagens(cursor, usuario_ids, grupo_ids, num_postagens=5000, profile_post_percentage=0.5):
    tipos_midia = ['texto', 'imagem', 'video']
    postagens = []
    for _ in tqdm(range(num_postagens), desc="📝 Populando postagens ", unit="post"):
        tipo = random.choice(tipos_midia)
        midia = fake.image_url() if tipo != 'texto' else None
        
        # Determine if the post should be made on the user's profile or a group
        if random.random() < profile_post_percentage:
            grupo_id = None
        else:
            if grupo_ids:
                grupo_id = random.choice(grupo_ids)
            else:
                grupo_id = None
        
        postagem = (
            fake.text(max_nb_chars=500),
            tipo,
            midia,
            random.choice(usuario_ids),
            grupo_id
        )
        cursor.execute("""
            INSERT INTO POSTAGEM (conteudo, tipo_midia, midia, usuario_id, grupo_id)
            VALUES (%s, %s, %s, %s, %s)
        """, postagem)
        postagens.append(cursor.lastrowid)
    return postagens

def populate_conexoes(cursor, usuario_ids, num_conexoes=3000):
    for _ in tqdm(range(num_conexoes), desc="🔗 Populando conexões ", unit="conexão"):
        usuarios = random.sample(usuario_ids, 2)
        try:
            cursor.execute("""
                INSERT INTO CONEXAO (usuario_id1, usuario_id2)
                VALUES (%s, %s)
            """, usuarios)
        except mysql.connector.Error:
            continue

def populate_interacoes(cursor, usuario_ids, postagem_ids, num_interacoes=10000):
    tipos = ['curtida', 'compartilhamento', 'comentario']
    for _ in tqdm(range(num_interacoes), desc="❤️ Populando interações ", unit="interação"):
        interacao = (
            random.choice(tipos),
            random.choice(usuario_ids),
            random.choice(postagem_ids)
        )
        cursor.execute("""
            INSERT INTO INTERACAO (tipo, usuario_id, postagem_id)
            VALUES (%s, %s, %s)
        """, interacao)

def populate_mensagens(cursor, usuario_ids, num_mensagens=8000):
    for _ in tqdm(range(num_mensagens), desc="💬 Populando mensagens ", unit="mensagem"):
        usuarios = random.sample(usuario_ids, 2)
        mensagem = (
            fake.text(max_nb_chars=200),
            usuarios[0],
            usuarios[1]
        )
        cursor.execute("""
            INSERT INTO MENSAGEM (conteudo, remetente_id, destinatario_id)
            VALUES (%s, %s, %s)
        """, mensagem)

def get_statistics(cursor):
    stats = {}
    
    cursor.execute("SELECT COUNT(*), AVG(TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE())) FROM USUARIO")
    stats['usuarios'], stats['media_idade'] = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) FROM POSTAGEM WHERE grupo_id IS NULL")
    stats['posts_perfil'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM POSTAGEM WHERE grupo_id IS NOT NULL")
    stats['posts_grupos'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT tipo, COUNT(*) FROM INTERACAO GROUP BY tipo")
    stats['tipos_interacao'] = dict(cursor.fetchall())
    
    cursor.execute("""
        SELECT u.municipio_id, COUNT(*) as total 
        FROM USUARIO u 
        GROUP BY u.municipio_id 
        ORDER BY total DESC 
        LIMIT 1
    """)
    stats['maior_cidade'] = cursor.fetchone()[1]
    
    return stats

def print_stats(stats):
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS DE POPULAÇÃO DO BANCO")
    print("="*50)
    print(f"👥 Total de Usuários: {stats['usuarios']:,}")
    print(f"📅 Média de Idade: {stats['media_idade']:.1f} anos")
    print(f"🏠 Maior cidade tem {stats['maior_cidade']} usuários")
    print("\n📝 POSTS:")
    print(f"   • Em perfis: {stats['posts_perfil']:,}")
    print(f"   • Em grupos: {stats['posts_grupos']:,}")
    print("\n❤️ INTERAÇÕES:")
    for tipo, count in stats['tipos_interacao'].items():
        emoji = {"curtida": "👍", "compartilhamento": "🔄", "comentario": "💬"}
        print(f"   {emoji.get(tipo, '•')} {tipo}: {count:,}")

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE connectme")
        cursor.execute("USE connectme")
        print("Banco de dados 'connectme' criado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar o banco de dados 'connectme': {err}")
        sys.exit(1)
               
def truncate_tables(cursor):
    tables = ['INTERACAO', 'MENSAGEM', 'CONEXAO', 'POSTAGEM', 'MEMBRO_GRUPO', 'GRUPO', 'USUARIO', 'MUNICIPIO', 'ESTADO']
    for table in tables:
        try:
            cursor.execute(f"TRUNCATE TABLE {table}")
        except mysql.connector.Error as err:
            print(f"Erro ao truncar a tabela {table}: {err}")
            sys.exit(1)

PROPORCOES = {
    'usuarios': 3000,
    'grupos': 600,      
    'membros': 18000,      
    'postagens': 60000,   
    'conexoes': 15000,     
    'interacoes': 180000,  
    'mensagens': 90000,   
    'municipios': 1000
}

def main():
    parser = argparse.ArgumentParser(description='Populate a MySQL database with sample data.')
    parser.add_argument('--recreate', action='store_true', help='Truncate tables before populating')
    args = parser.parse_args()

    conn = connect_db()
    cursor = conn.cursor()

    if args.recreate:
        truncate_tables(cursor)
        print("Tabelas truncadas com sucesso.")
    else:
        print("Usando banco de dados e tabelas existentes.")

    estado_ids = populate_estados(cursor)
    municipio_ids = populate_municipios(cursor, estado_ids, PROPORCOES['municipios'])
    usuario_ids = populate_usuarios(cursor, municipio_ids, PROPORCOES['usuarios'])
    grupo_ids = populate_grupos(cursor, PROPORCOES['grupos'])
    populate_membros_grupo(cursor, usuario_ids, grupo_ids, PROPORCOES['membros'])
    postagem_ids = populate_postagens(cursor, usuario_ids, grupo_ids, PROPORCOES['postagens'])
    populate_conexoes(cursor, usuario_ids, PROPORCOES['conexoes'])
    populate_interacoes(cursor, usuario_ids, postagem_ids, PROPORCOES['interacoes'])
    populate_mensagens(cursor, usuario_ids, PROPORCOES['mensagens'])

    conn.commit()

    stats = get_statistics(cursor)
    print_stats(stats)

    cursor.close()
    conn.close()
    print("\n✨ População do banco concluída com sucesso! ✨")

if __name__ == "__main__":
    main()
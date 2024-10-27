
import sqlite3
import streamlit as st
import pandas as pd
import random

# Conexão com o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('cadastro.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero TEXT NOT NULL
        )
    ''')
    c.execute('CREATE TABLE IF NOT EXISTS sorteio (vencedor TEXT, numero TEXT)')
    conn.commit()
    conn.close()

# Função para adicionar um novo usuário
def add_usuario(nome, numero):
    conn = sqlite3.connect('cadastro.db')
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nome, numero) VALUES (?, ?)', (nome, numero))
    conn.commit()
    conn.close()

# Função para obter todos os usuários
def get_usuarios():
    conn = sqlite3.connect('cadastro.db')
    df = pd.read_sql_query('SELECT * FROM usuarios', conn)
    conn.close()
    return df

# Função para realizar o sorteio
def realizar_sorteio(usuarios):
    sorteio_numero = random.choice(usuarios['numero'].tolist())
    vencedor = usuarios[usuarios['numero'] == sorteio_numero].iloc[0]
    
    conn = sqlite3.connect('cadastro.db')
    c = conn.cursor()
    c.execute('INSERT INTO sorteio (vencedor, numero) VALUES (?, ?)', (vencedor['nome'], vencedor['numero']))
    conn.commit()
    conn.close()
    
    return vencedor

# Função para excluir o histórico de sorteios
def excluir_historico():
    conn = sqlite3.connect('cadastro.db')
    c = conn.cursor()
    c.execute('DELETE FROM sorteio')
    conn.commit()
    conn.close()

# Inicializa o banco de dados
init_db()

# Chave PIX (exemplo fictício)
pix_key = "00020101021126420014BR.GOV.BCB.PIX0120lucpaython@gmail.com52040000530398654041.005802BR5924Lucio Fabio Da Silva Oli6008SAOPAULO61080132305062070503***63046A4F"
senha_cadastro = "1286"

# Interface do Streamlit
st.title("sorteio do pix.")
st.subheader("o bilhete custa apenas um real.")
st.write("você só estará concorrendo\nse tiver realizado o pix.")
st.write("só assim poderá receber o seu prêmio.")
# Exibe a chave PIX
st.write(f"Para se cadastrar, realize um PIX para a chave: {pix_key}")

# Cadastro de usuário
senha = st.text_input("Digite a senha para liberar o cadastro:", type="password")
nome = st.text_input("Digite seu nome:")
if st.button("Cadastrar"):
    if senha == senha_cadastro and nome:
        # Gera um número de 3 dígitos
        numero = f"{random.randint(0, 999):03d}"
        add_usuario(nome, numero)
        st.success(f"Cadastro realizado com sucesso! O número do seu bilhete é: {numero}")

        # Verifica quantos usuários estão cadastrados
        usuarios = get_usuarios()
        total_cadastrados = len(usuarios)
        faltando = max(0, 10 - total_cadastrados)

        st.write(f"Total de cadastrados: {total_cadastrados}. Faltam {faltando} para o sorteio.")
        
        # Realiza o sorteio se houver 10 cadastrados
        if total_cadastrados >= 10:
            vencedor = realizar_sorteio(usuarios)
            st.success(f"O ganhador foi {vencedor['nome']} com o bilhete de número {vencedor['numero']}.")
    elif senha != senha_cadastro:
        st.error("Senha incorreta! Tente novamente.")
    else:
        st.error("Por favor, insira um nome válido.")

# Mostra os usuários cadastrados em tabela
if st.button("Ver Usuários Cadastrados"):
    usuarios = get_usuarios()
    if not usuarios.empty:
        usuarios_formatados = usuarios.copy()
        usuarios_formatados['info'] = usuarios_formatados.apply(lambda row: f"{row['nome']} (), bilhete ({row['numero']})", axis=1)
        st.table(usuarios_formatados[['info']])
    else:
        st.write("Nenhum usuário cadastrado.")

# Mostrar histórico de sorteios em tabela
if st.button("Ver Histórico de Sorteios"):
    conn = sqlite3.connect('cadastro.db')
    sorteios = pd.read_sql_query('SELECT * FROM sorteio', conn)
    conn.close()
    if not sorteios.empty:
        sorteios_formatados = sorteios.copy()
        sorteios_formatados['info'] = sorteios_formatados.apply(lambda row: f"{row['vencedor']} (), bilhete ({row['numero']})", axis=1)
        st.table(sorteios_formatados[['info']])
    else:
        st.write("Nenhum sorteio realizado ainda.")

# Excluir histórico de sorteios
senha_exclusao = st.text_input("Digite a senha para excluir o histórico:", type="password")
if st.button("Excluir Histórico"):
    if senha_exclusao == 1285:
        excluir_historico()
        st.success("Histórico de sorteios excluído com sucesso!")
    else:
        st.error("Senha incorreta! Não foi possível excluir o histórico.")
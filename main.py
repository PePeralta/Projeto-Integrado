import mysql.connector
import hashlib

print("Iniciar sessão")

email = input("Email: ")
senha = input("Senha: ")
senha_encr = hashlib.sha1(senha.encode()).hexdigest()

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

cur = con.cursor()

# Verificar login
cur.execute(
    "SELECT tipo FROM users WHERE email=%s AND password=%s",
    (email, senha_encr)
)

resultado = cur.fetchone()

if resultado:
    tipo_utilizador = resultado[0]
    print("✅ Login efetuado com sucesso!")

    if tipo_utilizador.lower() == "administrador":
        print("Certo, vamos prosseguir...")
        print("1 - Verificar os utilizadores")
        print("2 - Verificar os produtos")
        print("3 - Encerrar sessão")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            # Buscar todos os utilizadores
            cur.execute("SELECT id, username, email, password, data_registo, tipo FROM users")
            users = cur.fetchall()

            # Imprimir cabeçalho da tabela com mais espaçamento para Password
            print("\n{:<3} {:<20} {:<30}".format("ID", "Username", "Email"))
            print("-" * 140)

            # Imprimir cada utilizador
            for user in users:
                print("{:<3} {:<20} {:<30}".format(user[0], user[1], user[2]))
            
            print("\nDiz o ID do utilizador que queres ver")
            escolhido = input("ID: ")

            cur.execute(
                "SELECT id, username, email, password, data_registo, tipo FROM users WHERE id = %s",
                (escolhido,)
            )

            user = cur.fetchone()

            if user:
                print("\n📄 Informações do utilizador\n")
                print(f"ID:            {user[0]}")
                print(f"Username:      {user[1]}")
                print(f"Email:         {user[2]}")
                print(f"Password:      {user[3]}")
                print(f"Data registo:  {user[4]}")
                print(f"Tipo:          {user[5]}")
            else:
                print("❌ Utilizador não encontrado")



        else:
            print("Esta aplicação é apenas para administradores")
    else:
        print("Email ou palavra-passe incorretos")

cur.close()
con.close()

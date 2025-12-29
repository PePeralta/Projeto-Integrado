import mysql.connector

print("Iniciar sessão")


email = input("Email: ")
senha = input("Senha: ")
    
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
    
cur = con.cursor()
    
cur.execute("SELECT tipo FROM users WHERE email=%s AND password=%s",(email, senha))
    
resultado = cur.fetchone()
if resultado:
    tipo_utilizador = resultado[0]
    print("✅ Login efetuado com sucesso!")
    if tipo_utilizador.lower() == "administrador":
        print("Certo, vamos prosseguir...")
        print("1 - Verificar os utilizadores")
        print("2 - Verificar os produtos")
        print("3 - Encerrar sessão")
    else:
        print("Esta aplicação é apenas para administradores")
else:
        print("Email ou palavra-passe incorretos")
    
cur.close()
con.close()

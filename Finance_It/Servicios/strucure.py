import json, os

#USUARIOS EN ARCHIVO JSON
def load_users():
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo puede estar corrupto.")
                return []
    return []


def save_users(users):
    try:
        with open('usuarios.json', 'w') as f:
            json.dump(users, f)
    except Exception as e:
        print("Error al guardar usuarios:", e)  # Imprime el error en la consola

username= input ("ingrese username: ")
email = input ("ingrese email: ")
password = input ("ingrese password: ")

# Cargar usuarios desde el archivo JSON
users = load_users()

if not any(user['username'] == username or user['email'] == email for user in users):
    users.append({
        "username": username,
        "email": email,
        "password": password
    })
    save_users(users)
    print("Usuario guardado:", {"username": username, "email": email})
else:
    print(f"Usuario con username '{username}' o email '{email}' ya existe.")

# CRUD Contactos — Lab 11 | Gsoto 2026

Aplicación web de gestión de contactos con Flask + SQLite.
Funciona igual en Windows y Debian (AWS EC2).

---

## 🪟 INSTALACIÓN EN WINDOWS (instancia EC2 vía RDP)

### 1. Abrir PowerShell como Administrador y ejecutar:

```powershell
# Instalar Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Python
choco install python -y
refreshenv

# Verificar
python --version
```

### 2. Copiar la carpeta `crud_contactos` al escritorio y ejecutar:

```powershell
cd C:\Users\Administrator\Desktop\crud_contactos
pip install -r requirements.txt
python app.py
```

### 3. Abrir el navegador DENTRO de la instancia RDP:

```
http://localhost:5000
```

### 4. Para acceder desde TU PC local, abrir el puerto 5000 en AWS:
- EC2 → Security Groups → Inbound rules → Add rule
- Type: Custom TCP | Port: 5000 | Source: My IP
- Luego acceder en tu PC: http://<IP-PUBLICA-WINDOWS>:5000

---

## 🐧 INSTALACIÓN EN DEBIAN (instancia EC2 vía SSH)

### 1. Conectarse a la instancia:

```bash
ssh -i lab11-key.pem admin@<IP-PUBLICA-DEBIAN>
```

### 2. Instalar dependencias:

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```

### 3. Subir los archivos (desde tu PC local):

```bash
# Desde tu PC, en la carpeta donde está crud_contactos/
scp -i lab11-key.pem -r crud_contactos admin@<IP-PUBLICA-DEBIAN>:~
```

### 4. Instalar y correr:

```bash
cd ~/crud_contactos
pip3 install -r requirements.txt
python3 app.py
```

### 5. Abrir puerto 5000 en AWS Security Group (igual que Windows arriba)

### 6. Acceder desde tu PC:

```
http://<IP-PUBLICA-DEBIAN>:5000
```

---

## Estructura del proyecto

```
crud_contactos/
├── app.py              ← Backend Flask + lógica CRUD
├── requirements.txt    ← Dependencias (solo Flask)
├── contactos.db        ← Base de datos SQLite (se crea automáticamente)
└── templates/
    ├── base.html       ← Layout base
    ├── index.html      ← Lista de contactos + búsqueda
    └── form.html       ← Formulario agregar/editar
```

---

## Operaciones CRUD

| Operación | Ruta           | Método |
|-----------|----------------|--------|
| Listar    | /              | GET    |
| Buscar    | /?q=término    | GET    |
| Agregar   | /agregar       | GET/POST |
| Editar    | /editar/<id>   | GET/POST |
| Eliminar  | /eliminar/<id> | POST   |

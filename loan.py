import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Función para inicializar la base de datos y crear la tabla
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            password TEXT,
            monto REAL,
            plazo INTEGER,
            descuento_directo BOOLEAN,
            antiguedad TEXT,
            empresa TEXT,
            ingresos REAL,
            comentarios TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Plantilla HTML básica que contiene un formulario (puedes integrarla con tu diseño)
form_html = '''
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Solicitud de Préstamo</title>
</head>
<body>
  <h2>Formulario de Solicitud de Préstamo</h2>
  <form method="post">
    <!-- Datos Personales -->
    <input type="text" name="nombre" placeholder="Nombre" required><br>
    <input type="text" name="apellido" placeholder="Apellido" required><br>
    <input type="email" name="email" placeholder="Correo Electrónico" required><br>
    <input type="tel" name="telefono" placeholder="Teléfono" required><br>
    <input type="password" name="password" placeholder="Contraseña" required><br>
    
    <!-- Detalles del Préstamo -->
    <input type="number" name="monto" placeholder="Monto del Préstamo" required><br>
    <select name="plazo" required>
      <option value="">Selecciona el plazo</option>
      <option value="3">3 meses</option>
      <option value="6">6 meses</option>
      <option value="12">12 meses</option>
      <option value="24">24 meses</option>
    </select><br>
    <label>
      <input type="checkbox" name="descuento" required>
      Descuento Directo (Se descontará de su salario)
    </label><br>
    
    <!-- Información Adicional -->
    <input type="text" name="antiguedad" placeholder="Tiempo de Antigüedad (ej: 5 años en la empresa)" required><br>
    <input type="text" name="empresa" placeholder="Empresa donde labora" required><br>
    <input type="number" name="ingresos" placeholder="Ingresos Mensuales" required><br>
    <textarea name="comentarios" placeholder="Comentarios adicionales"></textarea><br>
    
    <button type="submit">Enviar Solicitud</button>
  </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def solicitud():
    if request.method == 'POST':
        # Extraer datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        password = request.form.get('password')
        monto = request.form.get('monto')
        plazo = request.form.get('plazo')
        # El checkbox devuelve "on" si está seleccionado
        descuento_directo = request.form.get('descuento') == 'on'
        antiguedad = request.form.get('antiguedad')
        empresa = request.form.get('empresa')
        ingresos = request.form.get('ingresos')
        comentarios = request.form.get('comentarios')
        
        # Insertar los datos en la base de datos
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO solicitudes 
            (nombre, apellido, email, telefono, password, monto, plazo, descuento_directo, antiguedad, empresa, ingresos, comentarios)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, email, telefono, password, monto, plazo, descuento_directo, antiguedad, empresa, ingresos, comentarios))
        conn.commit()
        conn.close()
        
        # Redirigir al dashboard
        return redirect('/dashboard')
    
    # Mostrar el formulario
    return render_template_string(form_html)

@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Dashboard</title>
    </head>
    <body>
      <h1>Dashboard</h1>
      <p><strong>Estado:</strong> Pendiente, Estamos analizando el préstamo.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const app = express();
const port = process.env.PORT || 3000;

// Configurar body-parser para recibir datos del formulario
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Abrir (o crear) la base de datos SQLite en un archivo
const db = new sqlite3.Database('./database.db', (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Conectado a la base de datos SQLite.');
});

// Crear la tabla "solicitudes" si no existe
db.run(`CREATE TABLE IF NOT EXISTS solicitudes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  apellido TEXT NOT NULL,
  email TEXT NOT NULL,
  telefono TEXT,
  password TEXT,
  monto REAL,
  plazo INTEGER,
  descuento_directo INTEGER,
  antiguedad TEXT,
  empresa TEXT,
  ingresos REAL,
  comentarios TEXT
)`);

// Endpoint para recibir el formulario y almacenar la solicitud
app.post('/submit', (req, res) => {
  const {
    nombre, apellido, email, telefono, password,
    monto, plazo, descuento, antiguedad, empresa, ingresos, comentarios
  } = req.body;
  
  // Convertir el checkbox a 1 (true) o 0 (false)
  const descuentoDirecto = descuento === 'on' ? 1 : 0;
  
  const sql = `INSERT INTO solicitudes 
    (nombre, apellido, email, telefono, password, monto, plazo, descuento_directo, antiguedad, empresa, ingresos, comentarios)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;
  const params = [nombre, apellido, email, telefono, password, monto, plazo, descuentoDirecto, antiguedad, empresa, ingresos, comentarios];

  db.run(sql, params, function(err) {
    if (err) {
      console.error(err.message);
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ message: "Solicitud guardada con éxito", id: this.lastID });
  });
});

// Endpoint para el dashboard (por ejemplo, para mostrar el estado)
app.get('/dashboard', (req, res) => {
  res.send(`
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
  `);
});

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});

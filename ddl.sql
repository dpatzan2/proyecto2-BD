DROP TABLE IF EXISTS Reservas;
DROP TABLE IF EXISTS Asientos;
DROP TABLE IF EXISTS EstadosAsiento;
DROP TABLE IF EXISTS Usuarios;
DROP TABLE IF EXISTS Secciones;
DROP TABLE IF EXISTS EstadosReserva;
DROP TABLE IF EXISTS Eventos;

-- Crear tabla de Eventos
CREATE TABLE Eventos (
    evento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    descripcion TEXT,
    capacidad_total INTEGER NOT NULL CHECK (capacidad_total > 0)
);

-- Crear tabla de Usuarios
CREATE TABLE Usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20)
);

-- Crear tabla de Estados de Asiento
CREATE TABLE EstadosAsiento (
    estado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Insertar estados básicos de asiento
INSERT INTO EstadosAsiento (nombre, descripcion) VALUES 
('disponible', 'El asiento está disponible para reserva'),
('reservado', 'El asiento ya ha sido reservado');

-- Crear tabla de Estados de Reserva
CREATE TABLE EstadosReserva (
    estado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Insertar estados básicos de reserva
INSERT INTO EstadosReserva (nombre, descripcion) VALUES 
('activa', 'La reserva está activa'),
('cancelada', 'La reserva ha sido cancelada');

-- Crear tabla de Secciones
CREATE TABLE Secciones (
    seccion_id SERIAL PRIMARY KEY,
    evento_id INTEGER NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    capacidad INTEGER NOT NULL CHECK (capacidad > 0),
    FOREIGN KEY (evento_id) REFERENCES Eventos(evento_id),
    UNIQUE(evento_id, nombre)
);

-- Crear tabla de Asientos
CREATE TABLE Asientos (
    asiento_id SERIAL PRIMARY KEY,
    seccion_id INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    estado_id INTEGER NOT NULL DEFAULT 1, -- 1 = disponible por defecto
    FOREIGN KEY (seccion_id) REFERENCES Secciones(seccion_id),
    FOREIGN KEY (estado_id) REFERENCES EstadosAsiento(estado_id),
    UNIQUE(seccion_id, numero)
);

-- Crear tabla de Reservas
CREATE TABLE Reservas (
    reserva_id SERIAL PRIMARY KEY,
    asiento_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INTEGER NOT NULL DEFAULT 1, -- 1 = activa por defecto
    FOREIGN KEY (asiento_id) REFERENCES Asientos(asiento_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (estado_id) REFERENCES EstadosReserva(estado_id)
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_secciones_evento ON Secciones(evento_id);
CREATE INDEX idx_asientos_seccion ON Asientos(seccion_id);
CREATE INDEX idx_asientos_estado ON Asientos(estado_id);
CREATE INDEX idx_reservas_asiento ON Reservas(asiento_id);
CREATE INDEX idx_reservas_usuario ON Reservas(usuario_id);
CREATE INDEX idx_reservas_estado ON Reservas(estado_id);
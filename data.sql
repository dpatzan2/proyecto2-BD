-- data.sql

-- Nuevo evento
INSERT INTO Eventos (nombre, fecha, descripcion, capacidad_total)
VALUES 
('Concierto de Rock', '2025-06-15 20:00:00', 'Concierto en vivo de la banda RockStar', 60);

-- Secciones para el evento
INSERT INTO Secciones (evento_id, nombre, capacidad)
VALUES 
(1, 'VIP', 10),
(1, 'General', 50);

-- Asientos para la sección VIP
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 1, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 2, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 3, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 4, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 5, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 6, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 7, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 8, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 9, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (1, 10, 1);

-- Asientos para la sección General
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 1, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 2, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 3, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 4, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 5, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 6, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 7, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 8, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 9, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 10, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 11, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 12, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 13, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 14, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 15, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 16, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 17, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 18, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 19, 1);
INSERT INTO Asientos (seccion_id, numero, estado_id) VALUES (2, 20, 1);

-- Usuarios
INSERT INTO Usuarios (nombre, email, telefono) VALUES 
('Juan Pérez', 'juan.perez@example.com', '555-1234'),
('María López', 'maria.lopez@example.com', '555-5678'),
('Carlos García', 'carlos.garcia@example.com', '555-9012'),
('Ana Martínez', 'ana.martinez@example.com', '555-3456');

-- NOTA: Se asume que los asientos se insertaron de forma secuencial. 
-- Los 10 primeros asientos (VIP) tendrán asiento_id de 1 a 10,
-- y los siguientes 20 asientos (General) tendrán asiento_id de 11 a 30.

-- Reserva de Juan Pérez para el asiento 1 de VIP (asiento_id = 1)
INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
VALUES (1, 1, CURRENT_TIMESTAMP, 1);

-- Reserva de María López para el asiento 2 de VIP (asiento_id = 2)
INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
VALUES (2, 2, CURRENT_TIMESTAMP, 1);

-- Reserva de Carlos García para el asiento 5 de la sección General (asiento_id = 15)
INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
VALUES (15, 3, CURRENT_TIMESTAMP, 1);

-- Reserva de Ana Martínez para el asiento 10 de la sección General (asiento_id = 20)
INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
VALUES (20, 4, CURRENT_TIMESTAMP, 1);

-- Actualizar el estado de los asientos a "reservado" (estado_id = 2)
UPDATE Asientos
SET estado_id = 2
WHERE asiento_id IN (1, 2, 15, 20);

Select * from Asientos;

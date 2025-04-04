import psycopg2
import threading
import time
from psycopg2 import errors

DB_CONFIG = {
    "host": "localhost",
    "dbname": "Proyecto_2",
    "user": "postgres",
    "password": "admin123"
}

def reservar_asiento(usuario_id, nivel_aislamiento):
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False 
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT usuario_id FROM Usuarios WHERE usuario_id = %s;", (usuario_id,))
        if cursor.fetchone() is None:
            print(f"Usuario {usuario_id}: No existe en la tabla Usuarios. Se omite la simulación para este usuario.")
            cursor.close()
            conn.close()
            return

        cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {nivel_aislamiento};")

        while True:
            cursor.execute("SELECT asiento_id FROM Asientos WHERE estado_id = 1 ORDER BY RANDOM() LIMIT 1;")
            asiento = cursor.fetchone()
            
            if asiento is None:
                print(f"Usuario {usuario_id}: No hay asientos disponibles.")
                break
            
            asiento_id = asiento[0]
            
            # Bloquear la fila del asiento seleccionado para evitar condiciones de carrera
            cursor.execute("SELECT estado_id FROM Asientos WHERE asiento_id = %s FOR UPDATE;", (asiento_id,))
            estado_actual = cursor.fetchone()[0]
            
            if estado_actual == 1:
                try:
                    cursor.execute("UPDATE Asientos SET estado_id = 2 WHERE asiento_id = %s;", (asiento_id,))
                    cursor.execute("""
                        INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
                        VALUES (%s, %s, CURRENT_TIMESTAMP, 1);
                    """, (asiento_id, usuario_id))
                    conn.commit()
                    print(f"Usuario {usuario_id}: Reserva exitosa del asiento {asiento_id} en [{nivel_aislamiento}].")
                    break
                except Exception as e:
                    conn.rollback()
                    print(f"Usuario {usuario_id}: Error al reservar el asiento {asiento_id} -> {e}. Reintentando...")
                    continue
            else:
                conn.rollback()
    except Exception as e:
        conn.rollback()
        print(f"Usuario {usuario_id}: Error -> {e}")
    finally:
        cursor.close()
        conn.close()

usuarios_concurrentes = 4 
niveles_aislamiento = ["READ COMMITTED"]

for nivel in niveles_aislamiento:
    print(f"\nEjecutando pruebas con nivel de aislamiento: {nivel}")
    threads = []
    for usuario in range(1, usuarios_concurrentes + 1):
        t = threading.Thread(target=reservar_asiento, args=(usuario, nivel))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Simulación finalizada para el nivel {nivel}.\n")

import psycopg2
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2 import errors

DB_CONFIG = {
    "host": "localhost",
    "dbname": "proyecto02",
    "user": "postgres",
    "password": "password"
}

TOTAL_USUARIOS = 600
MAX_ASIENTOS = 500
CONCURRENT_WORKERS = TOTAL_USUARIOS

start_barrier = threading.Barrier(TOTAL_USUARIOS)

fallos_totales = 0
fallos_lock = threading.Lock()

def elegir_nivel_aislamiento():
    print("Seleccione el nivel de aislamiento:")
    print("1. READ COMMITTED")
    print("2. REPEATABLE READ")
    print("3. SERIALIZABLE")
    opcion = input("Opción (1-3): ")
    if opcion == "1":
        return "READ COMMITTED"
    elif opcion == "2":
        return "REPEATABLE READ"
    elif opcion == "3":
        return "SERIALIZABLE"
    else:
        print("Opción inválida. Se usará READ COMMITTED por defecto.")
        return "READ COMMITTED"

def reset_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("UPDATE Asientos SET estado_id = 1;")
        cursor.execute("DELETE FROM Reservas;")
        cursor.close()
        conn.close()
        print("Base de datos reiniciada.\n")
    except Exception as e:
        print("Error reiniciando la base de datos:", e)

def reservar_asiento(usuario_id, nivel_aislamiento, max_attempts):
    global fallos_totales
    try:
        start_barrier.wait()
    except Exception as e:
        print(f"Usuario {usuario_id}: Error en barrier -> {e}")

    for intento in range(1, max_attempts + 1):
        inicio_transaccion = time.time()
        
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.set_session(isolation_level=nivel_aislamiento, autocommit=False)
            cursor = conn.cursor()

            cursor.execute("SELECT usuario_id FROM Usuarios WHERE usuario_id = %s;", (usuario_id,))
            if cursor.fetchone() is None:
                print(f"Usuario {usuario_id}: No existe en la tabla Usuarios.", flush=True)
                cursor.close()
                conn.close()
                return None

            cursor.execute("SELECT asiento_id FROM Asientos WHERE estado_id = 1 ORDER BY RANDOM() LIMIT 1;")
            row = cursor.fetchone()
            if row is None:
                with fallos_lock:
                    fallos_totales += 1
                print(f"Usuario {usuario_id} intento {intento}: No hay asientos disponibles.", flush=True)
                cursor.close()
                conn.close()
                return None

            asiento_id = row[0]
            cursor.execute("SELECT estado_id FROM Asientos WHERE asiento_id = %s FOR UPDATE;", (asiento_id,))
            estado_actual = cursor.fetchone()[0]
            if estado_actual == 1:
                cursor.execute("UPDATE Asientos SET estado_id = 2 WHERE asiento_id = %s;", (asiento_id,))
                cursor.execute("""
                    INSERT INTO Reservas (asiento_id, usuario_id, fecha_reserva, estado_id)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, 1);
                """, (asiento_id, usuario_id))
                conn.commit()
                duracion_ms = int((time.time() - inicio_transaccion) * 1000)
                print(f"Usuario {usuario_id}: Reserva exitosa del asiento {asiento_id} en [{nivel_aislamiento}] en {duracion_ms} ms (intento {intento}).", flush=True)
                cursor.close()
                conn.close()
                return duracion_ms
            else:
                conn.rollback()
                with fallos_lock:
                    fallos_totales += 1
                print(f"Usuario {usuario_id} intento {intento}: El asiento {asiento_id} ya estaba reservado, reintentando...", flush=True)
                cursor.close()
                conn.close()
                time.sleep(0.05 * intento)
                continue

        except (errors.SerializationFailure, errors.DeadlockDetected) as se:
            try:
                conn.rollback()
            except Exception:
                pass
            with fallos_lock:
                fallos_totales += 1
            print(f"Usuario {usuario_id} intento {intento}: Error de serialización/deadlock en [{nivel_aislamiento}], reintentando...", flush=True)
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass
            time.sleep(0.05 * intento)
            continue

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            with fallos_lock:
                fallos_totales += 1
            print(f"Usuario {usuario_id} intento {intento}: Error -> {e}", flush=True)
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass
            time.sleep(0.05 * intento)
            continue

    print(f"Usuario {usuario_id}: Falló en reservar asiento después de {max_attempts} intentos.", flush=True)
    return None

if __name__ == "__main__":
    nivel_aislamiento = elegir_nivel_aislamiento()
    if nivel_aislamiento == "READ COMMITTED":
        max_attempts = 3
    else:
        max_attempts = 10

    print(f"\n=== Iniciando simulación con {TOTAL_USUARIOS} usuarios y aislamiento: {nivel_aislamiento} ===")
    reset_db()

    inicio_simulacion = time.time()
    tiempos_reservas = []

    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        futures = {
            executor.submit(reservar_asiento, usuario, nivel_aislamiento, max_attempts): usuario
            for usuario in range(1, TOTAL_USUARIOS + 1)
        }
        for future in as_completed(futures):
            resultado = future.result()
            if resultado is not None:
                tiempos_reservas.append(resultado)

    tiempo_total_ms = int((time.time() - inicio_simulacion) * 1000)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Asientos WHERE estado_id = 2;")
        asientos_reservados_db = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error al consultar asientos reservados:", e)
        asientos_reservados_db = 0

    print("\n=== Resultados Finales ===")
    print(f"Asientos reservados (según BD): {asientos_reservados_db} de {MAX_ASIENTOS}")
    print(f"Usuarios sin asiento: {TOTAL_USUARIOS - asientos_reservados_db}")
    print(f"Total de intentos fallidos de reserva: {fallos_totales}")
    print(f"Tiempo total de simulación: {tiempo_total_ms} ms.")
    if tiempos_reservas:
        promedio_tiempo = int(sum(tiempos_reservas) / len(tiempos_reservas))
        print(f"Tiempo promedio por reserva exitosa: {promedio_tiempo} ms.")
    else:
        print("No hubo reservas exitosas.")

## Project Overview

This system simulates a real-world scenario where multiple users try to reserve seats for an event concurrently. It implements different transaction isolation levels to handle concurrent access and prevent data inconsistencies.

### Key Features

- Concurrent seat reservation simulation with up to 5, 200, 600, 1000 simultaneous users
- Support for multiple transaction isolation levels (READ COMMITTED, REPEATABLE READ, SERIALIZABLE)

## Prerequisites

- Python 3.x
- PostgreSQL 12 or higher
- psycopg2 (Python PostgreSQL adapter)

## Database Setup

1. Create a PostgreSQL database named 'proyecto02'
2. Execute the DDL script to create the database structure ddl.sql
3. Load the test data data.sql

## Configuration

Update the database configuration in `Reservar.py` if needed:

```python
DB_CONFIG = {
    "host": "localhost",
    "dbname": "proyecto02",
    "user": "postgres",
    "password": "password"
}
```

## Running the Simulation

1. Run the reservation simulation:
   ```bash
   python Reservar.py
   ```
2. Select the desired isolation level when prompted:
   - 1: READ COMMITTED (3 retry attempts)
   - 2: REPEATABLE READ (10 retry attempts)
   - 3: SERIALIZABLE (10 retry attempts)

## Understanding the Results

The simulation provides detailed statistics including:

- Number of successful reservations
- Number of failed attempts
- Total simulation time
- Average reservation time
- Number of users without seats

## Project Structure

- `ddl.sql`: Database schema definition
- `data.sql`: Test data population script
- `Reservar.py`: Main simulation program

### Database Schema

- **Eventos**: Event information
- **Usuarios**: User data
- **Asientos**: Seat management
- **Reservas**: Reservation records
- **EstadosAsiento**: Seat status definitions
- **EstadosReserva**: Reservation status definitions
- **Secciones**: Event sections

## Authors

- Diego Patzán: 23525
- Ihan Marroquin: 23108

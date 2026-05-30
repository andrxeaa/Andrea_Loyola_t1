# Sistema de Recompensas - Arquitectura Orientada a Eventos

Este proyecto implementa una solución de software basada en mensajería (RabbitMQ) y Arquitectura Hexagonal/Limpia para un sistema de fidelización de restaurantes.

## Arquitectura

Se ha utilizado una **Arquitectura Orientada a Eventos (EDA)** combinada con principios de **Clean Architecture / Hexagonal Architecture**:

- **Productor (Restaurant API):** Microservicio en FastAPI que recibe las transacciones de las cenas y publica el evento en RabbitMQ.
- **Consumidor (Rewards Worker):** Microservicio que escucha la cola de RabbitMQ, calcula los puntos y cashback ganados, y actualiza la cuenta del cliente.
- **Broker (RabbitMQ):** Actúa como middleware de mensajería para desacoplar ambos componentes.

La estructura interna de `src/` respeta la separación de capas (Core/Dominio y Casos de Uso, e Infraestructura/Adaptadores).

## Requisitos

- Python 3.11+
- Docker y Docker Compose (para RabbitMQ)
- Sonar Scanner (para análisis estático)

## Ejecución

1. **Levantar RabbitMQ:**
   ```bash
   docker-compose up -d
   ```

2. **Instalar dependencias:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # En Windows
   pip install -r requirements.txt
   ```

3. **Ejecutar el Consumidor (en una terminal):**
   ```bash
   python -m src.consumer
   ```

4. **Ejecutar el API Productor (en otra terminal):**
   ```bash
   python -m src.main
   ```
   El API estará disponible en `http://localhost:8000/docs`.

## Pruebas y Cobertura

Para ejecutar las pruebas y generar el reporte de cobertura (necesario para SonarQube):
```bash
pytest
```
Esto generará un archivo `coverage.xml`.

## SonarQube

Para ejecutar el análisis:
```bash
sonar-scanner
```
Asegúrese de haber ejecutado `pytest` primero para tener el archivo `coverage.xml`.

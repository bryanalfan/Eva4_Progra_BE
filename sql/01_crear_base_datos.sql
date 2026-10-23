-- 01. Crear la base de datos de la API de viajes y turismo.
-- Ejecutar con un usuario administrador:  mysql -u root -p < sql/01_crear_base_datos.sql
-- utf8mb4 permite almacenar cualquier carácter Unicode (tildes, ñ, emojis).
CREATE DATABASE IF NOT EXISTS turismo_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

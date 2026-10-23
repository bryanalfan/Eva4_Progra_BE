-- 02. Crear el usuario que usará Django para conectarse.
-- Ejecutar con un usuario administrador:  mysql -u root -p < sql/02_crear_usuario.sql
-- La contraseña debe coincidir con DB_PASSWORD del archivo .env
CREATE USER IF NOT EXISTS 'turismo_user'@'localhost' IDENTIFIED BY 'Cambiar_Password_123';

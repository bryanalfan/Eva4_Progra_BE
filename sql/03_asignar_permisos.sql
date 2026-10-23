-- 03. Conceder privilegios sobre la base de datos al usuario de Django.
-- Ejecutar con un usuario administrador:  mysql -u root -p < sql/03_asignar_permisos.sql
GRANT ALL PRIVILEGES ON turismo_db.* TO 'turismo_user'@'localhost';

-- Base temporal que Django crea al ejecutar las pruebas (python manage.py test).
GRANT ALL PRIVILEGES ON `test_turismo_db`.* TO 'turismo_user'@'localhost';

-- Aplicar los cambios de privilegios.
FLUSH PRIVILEGES;

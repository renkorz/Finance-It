CREATE TABLE Usuario (
   id_usuario int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   username varchar(50)  NOT NULL,
   password varchar(16)  NOT NULL,
   name varchar(100)  NOT NULL,
   last_name varchar(100)  NULL,
   mail varchar(100)  NOT NULL
);

CREATE TABLE Transacciones (
   id_transaccion int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   tipo_transaccion varchar(10)  NOT NULL COMMENT 'ingreso / gasto',
   fecha date  NULL
);

CREATE TABLE Reportes (
   id_reporte int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   reporte text  NOT NULL
);

CREATE TABLE Metas (
   goal_id int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   descripcion text  NULL,
   monto_objetivo int  NOT NULL,
   fecha_limite date  NULL
);

CREATE TABLE Ahorros (
   id_ahorros int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ahorro_total int  NOT NULL
);

INSERT INTO Usuario (username, password, name, last_name, mail) VALUES('admin', '12345', 'admin', '', 'admin@admin.com')
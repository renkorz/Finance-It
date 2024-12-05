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
   monto_transaccion int,
   fecha date  NULL,
   id_usuario int NOT NULL,
   FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Metas (
   goal_id int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   descripcion text  NULL,
   monto_objetivo int  NOT NULL,
   fecha_limite date  NULL,
   id_usuario int NOT NULL,
   FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Ahorros (
   id_ahorros int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ahorro_total int  NOT NULL,
   id_usuario int NOT NULL,
   FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Reportes (
   id_reporte int  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   reporte text  NOT NULL,
   id_usuario int NOT NULL,
   FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
   id_transaccion int NULL,
   goal_id INT NULL,
   id_ahorros int NULL, 
   FOREIGN KEY (id_ahorros) REFERENCES Ahorros(id_ahorros),
   FOREIGN KEY (id_transaccion) REFERENCES Transacciones(id_transaccion),
   FOREIGN KEY (goal_id) REFERENCES Metas(goal_id)
);
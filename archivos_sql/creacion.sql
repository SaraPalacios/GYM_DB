CREATE TABLE cliente(
  cliente_cc VARCHAR not NULL,
  nombre1_cliente VARCHAR not NULL,
  nombre2_cliente VARCHAR,
  apellido1_cliente varchar not NULL,
  apellido2_cliente varchar,
  objetivo varchar,
  PRIMARY key (cliente_cc)
);

create table instructor(
  instructor_cc VARCHAR not null,
  nom_instr varchar not null,
  apellido_istr varchar NOT NULL,
  especialidad varchar,
  PRIMARY key (instructor_cc)
);

create table ejercicio(
  ejercicio_ID serial not NULL,
  tipo_entrenamiento VARCHAR,
  parte_del_cuerpo VARCHAR NOT NULL,
  dificultad VARCHAR NOT NULL,
  PRIMARY KEY(ejercicio_ID)
);

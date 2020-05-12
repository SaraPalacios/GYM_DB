 --Ganar masa 
CREATE OR REPLACE FUNCTION PlanGanarMasa()
returns table(Entrenamiento VARCHAR, Dificultad VARCHAR, Parte_del_cuerpo VARCHAR,Instructor VARCHAR) as $$
BEGIN
	return QUERY
    SELECT ejercicio.tipo_entrenamiento,ejercicio.dificultad,ejercicio.parte_del_cuerpo, instructor.nom_instr
	from ejercicio join instructor on ejercicio.tipo_entrenamiento = instructor.especialidad
	where ejercicio.tipo_entrenamiento = 'flexibilidad'or ejercicio.tipo_entrenamiento = 'Fuerza'
	or ejercicio.tipo_entrenamiento = 'Equilibrio'
	ORDER BY RANDOM()
	LIMIT 4;
END;
$$
language plpgsql;

--Reduccion
CREATE OR REPLACE FUNCTION PlanReduccion()
returns table(Entrenamiento VARCHAR, Dificultad VARCHAR, Parte_del_cuerpo VARCHAR,Instructor VARCHAR) as $$
BEGIN
	return QUERY
    SELECT ejercicio.tipo_entrenamiento, ejercicio.dificultad,ejercicio.parte_del_cuerpo, instructor.nom_instr
	from ejercicio join instructor on ejercicio.tipo_entrenamiento = instructor.especialidad
	where ejercicio.tipo_entrenamiento = 'Cardio' or ejercicio.dificultad = 'medio'
	or ejercicio.tipo_entrenamiento = 'Fuerza' or ejercicio.dificultad = 'alto impacto'
	ORDER BY RANDOM()
	LIMIT 4;
END;
$$
language plpgsql;

--Principiante 
CREATE OR REPLACE FUNCTION PlanPrincipiante()
returns table(Entrenamiento VARCHAR, Dificultad VARCHAR, Parte_del_cuerpo VARCHAR,Instructor VARCHAR) as $$
BEGIN
	return QUERY
    SELECT ejercicio.tipo_entrenamiento, ejercicio.dificultad,ejercicio.parte_del_cuerpo, instructor.nom_instr
	from ejercicio join instructor on ejercicio.tipo_entrenamiento = instructor.especialidad
	where ejercicio.dificultad = 'bajo impacto'
	ORDER BY RANDOM()
	LIMIT 3;
END;
$$
language plpgsql;

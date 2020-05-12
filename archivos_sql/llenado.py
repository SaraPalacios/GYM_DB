import pandas as pd
import psycopg2
def InsertarEjercicio(tipo,parte,dif):
  return "INSERT INTO ejercicio(tipo_entrenamiento,parte_del_cuerpo,dificultad) VALUES ('"+tipo+"','"+parte+"','"+dif+"');"

def InsertarCliente(doc,nom1,nom2,ape1,ape2,obj):
  if nom2 == '-':
    sqlPart = "INSERT INTO cliente(cliente_cc,nombre1_cliente,apellido1_cliente,apellido2_cliente, objetivo) VALUES"
    return sqlPart+ "('"+str(doc)+"','"+nom1+"','"+ape1+"','"+ape2+"','"+obj+"');" 
  else:
    sqlPart = "INSERT INTO cliente(cliente_cc,nombre1_cliente,nombre2_cliente, apellido1_cliente, apellido2_cliente, objetivo) VALUES"
    return sqlPart+ "('"+str(doc)+"','"+nom1+"','"+nom2+"','"+ape1+"','"+ape2+"','"+obj+"');" 

info_ejercicios = pd.read_csv("ejercicios.csv", sep = ";", encoding = "latin1")
info_clientes = pd.read_csv("clientes.csv", sep = ";", encoding = "latin1").fillna('-')
    
hostname = 'rajje.db.elephantsql.com'
username = 'zuhonhle'
password = 'OWSH5KBapqO2LGvC4ija5MKbP_QvDuO9'
database = 'zuhonhle'
    
DBConnection = None
try:
    DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
	
    # crear un cursor para ejecutar comandos dentro de la DB
    cursorDB = DBConnection.cursor()
    for index,ejercicio in info_ejercicios.iterrows():
        tipo = ejercicio['tipo_entrenamiento']
        parte = ejercicio['parte']
        dif = ejercicio['dificultad']
        query = InsertarEjercicio(tipo,parte,dif)
        cursorDB.execute(query)
        
    for index,cliente in info_clientes.iterrows():
        documento = cliente['documento']
        apellido1 = cliente['apellido_1']
        apellido2 = cliente['apellido_2']
        nombre1 = cliente['nombre_1']
        nombre2 = cliente['nombre_2']
        obj = cliente['objetivo']
        query2 = InsertarCliente(documento,nombre1,nombre2,apellido1,apellido2,obj) 
        cursorDB.execute(query2)  
  
    DBConnection.commit() #no olvidar el COMMIT para hacer cambios permanentes en la base de datos central.
    # cerrar la conexión a la base de datos
    cursorDB.close() 
 
 
#si hay un error en la conexión informar
except (Exception, psycopg2.DatabaseError) as error:
        print('Error encontrado:',error)
#si algo no ha sido cubierto en los casos anteriores, cerrar la conexión a la base de datos
finally:
  if DBConnection is not None:
    DBConnection.close()
    print('en caso finally: cerrando la conexión a la DB.')

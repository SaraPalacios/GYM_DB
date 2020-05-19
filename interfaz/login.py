from flask import Flask, redirect, url_for, request, render_template
import psycopg2
import pandas as Pandas
app = Flask(__name__,template_folder='templates')



hostname = 'rajje.db.elephantsql.com'
username = 'zuhonhle'
password = 'OWSH5KBapqO2LGvC4ija5MKbP_QvDuO9'
database = 'zuhonhle'
    
def metodoParaImprimirUnDataFrameComoString(dataFrame):
    cols = dataFrame.columns
    resultado = '<table border="1"> '
    resultado += '<tr>'
    for col in cols:
        resultado += '<th scope= col> ' + col + ' </th>'
    resultado += '</tr>'
    for index,fila in dataFrame.iterrows():
        resultado += '<tr>'
        for campo in cols:
            resultado +='<td>'+str(fila[campo]) + '</td>'
        resultado +='</tr>'
    return resultado+ '</table>'

def queryComoDataFrame(sqlQuery):
  DBConnection = None #comenzamos creando un objeto conexión para conectarnos a la DB con los parámetros dados
  resultDataFrame = None #comenzamos con un objeto dataframe vacío.
  try:
    # conectar usando el método connect de pyscopg2
    print('Connecting to the PostgreSQL database...')
    DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    #usar el Pandas DataFrame para recibir el comando
    resultDataFrame = Pandas.read_sql_query(sqlQuery, DBConnection)
    DBConnection.close()
    return resultDataFrame
  except (Exception, psycopg2.DatabaseError) as error:
    print('Error en el Query:',error)
    return None
  #si algo no ha sido cubierto en los casos anteriores, cerrar la conexión a la base de datos
  finally:
    if DBConnection is not None:
      DBConnection.close()
    print('en caso finally: query ejecutado, resultados en un data frame.')
    
    
def InsertarCliente(query):
    DBConnection = None #comenzamos creando un objeto conexión para conectarnos a la DB con los parámetros dados
    resultDataFrame = None #comenzamos con un objeto dataframe vacío.
    try:
        # conectar usando el método connect de pyscopg2
        print('Connecting to the PostgreSQL database...')
        DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        cursorDB = DBConnection.cursor()
        cursorDB.execute(query)
        DBConnection.commit()
        cursorDB.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error en el Query:',error)
        return None
    #si algo no ha sido cubierto en los casos anteriores, cerrar la conexión a la base de datos
    finally:
        if DBConnection is not None:
            DBConnection.close()
            print('en caso finally: query ejecutado, el cliente ha sido insertado')
        


@app.route('/success/<name>')
def success(name):
    query = """SELECT cliente.cliente_cc, cliente.nombre1_cliente,cliente.apellido1_cliente, objetivo
                FROM cliente
                WHERE cliente.cliente_cc ='{}'""".format(name)
    us = queryComoDataFrame(query)
    stri = "<h1>Hola "
    if len(us.index) == 0:
        return redirect(url_for('cliente'))
    
    
    for idx, usuario in us.iterrows():
        name = str(usuario['nombre1_cliente'])
        apellido = str(usuario['apellido1_cliente'])
        purpose = str(usuario['objetivo'])
        
    stri += name + ' '+apellido +"</h1>"
    stri += " <p> De acuerdo con nuestra base de datos usted desea " +purpose + "</p>"
    stri += "<p> Por lo tanto queremos proponerle el siguiente plan "
    if purpose == "Reducir Grasa": 
        stri += "de Reducción: </p>"
        query2 = "SELECT * FROM PlanReduccion()"
        plan = queryComoDataFrame(query2)
        tabla = metodoParaImprimirUnDataFrameComoString(plan)
    elif purpose == "Ganar Masa":
        stri += "de Ganar Masa muscular: </p>"
        query2 = "SELECT * FROM PlanGanarMasa()"
        plan = queryComoDataFrame(query2)
        tabla = metodoParaImprimirUnDataFrameComoString(plan)
    else:
        stri += "para comenzar de cero su entrenamiento: </p>"
        query2 = "SELECT * FROM PlanPrincipiante()"
        plan = queryComoDataFrame(query2)
        tabla = metodoParaImprimirUnDataFrameComoString(plan)
        
    return stri + tabla
@app.route('/red',methods = ['POST'])
def red():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success',name = user))

@app.route('/login',methods = ['POST', 'GET'])
def login():
    return render_template('login.html')

  
@app.route('/cliente',methods = ['POST', 'GET'])
def cliente():
    return render_template('cliente.html')


@app.route('/llenado',methods = ['POST', 'GET'])
def llenado():
    if request.method == 'POST':
        prinom = request.form['Nombre1']
        secnom = request.form['Nombre2']
        priap = request.form['Apellido1']
        secap = request.form['Apellido2']
        cc  = request.form['Cedula']
        obj = request.form['Objetivo']
        if obj =='1':
            obj = 'Comenzar'
        elif obj =='2':
            obj = 'Ganar Masa'
        else:
            obj = 'Reducir Grasa'
        
        if secnom == '-':
            sqlPart = "INSERT INTO cliente(cliente_cc,nombre1_cliente,apellido1_cliente,apellido2_cliente, objetivo) VALUES"
            sqlPart += "('"+str(cc)+"','"+prinom+"','"+priap+"','"+secap+"','" +obj+"');"
        else:
            sqlPart = "INSERT INTO cliente(cliente_cc,nombre1_cliente,nombre2_cliente, apellido1_cliente, apellido2_cliente, objetivo) VALUES"
            sqlPart += "('"+str(cc)+"','"+prinom+"','"+secnom+"','"+priap+"','"+secap+"','"+obj+"');"
        InsertarCliente(sqlPart)
        return redirect(url_for('success',name = cc))
    
@app.route('/')
def home():
    return render_template('twobuts.html')  # return a string

if __name__ == '__main__':
   app.run(debug = True)

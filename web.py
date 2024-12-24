from flask import Flask, render_template, redirect, url_for, request, Response, session
from flask_mysqldb import MySQL, MySQLdb
app = Flask(__name__,template_folder='templates')

#base de datos
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='3054=HitM'
app.config['MYSQL_DB']='agencia'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    if request.method == 'POST' and 'correo' in request.form and 'password' in request.form:
        correo = request.form['correo']
        password = request.form['password']
        cursor.execute('SELECT * FROM usuarioscomunes WHERE email = %s AND cedula_identidad = %s', (correo, password))
        account = cursor.fetchone()
        if account:
            user = account['nombre']
            lastname = account['apellido']
            cursor.execute('SELECT id FROM usuarioscomunes WHERE email = %s AND cedula_identidad = %s', (correo, password))
            identificacion = cursor.fetchone()['id'][0]
            session['lastname'] = lastname
            session['user'] = user
            session['identificacion'] = identificacion
            session['tipo'] = 'Cliente comun'
            return render_template('session.html', user=session['user'], identificacion=session['identificacion'], tipo=session['tipo'])
        else:
            user = account['correo']
            nit = account['password']
            cursor.execute('SELECT * FROM clientescorporativos WHERE nombre_empresa = %s AND nit = %s', (user, nit))
            account = cursor.fetchone()
            if account:
                cursor.execute('SELECT id FROM clientescorporativos WHERE nombre_empresa = %s AND nit = %s', (user, nit))
                identificacion = cursor.fetchone()['id'][0]
                session['user'] = user
                session['nit'] = nit
                session['identificacion'] = identificacion
                session['tipo'] = 'ClienteCorporativo'
                return render_template('session.html', user=session['user'], identificacion=session['identificacion'], tipo=session['tipo'])
            else:
                return render_template('index.html')
    return render_template('index.html')
@app.route('/Informacion')
def information():
    return render_template('Contacts.html')

@app.route('/register/', methods=["GET", "POST"])
def user_register():
    if request.method == 'POST' and request.form.get('userType') == 'comun':
        try:
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            idCard = request.form['idCard']
            age = int(request.form['age']) if request.form['age'].isdigit() else None
            company = request.form['company']
            work_Address = request.form['workAddress']
            office_phone = request.form['officePhone']
            home_address = request.form['homeAddress']
            home_phone = request.form['homePhone']
            cell_phone = request.form['cellPhone']
            email = request.form['email']
            
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO usuarioscomunes '
                '(nombre, apellido, cedula_identidad, edad, empresa_trabajo, direccion_trabajo, telefono_oficina, direccion_habitacion, telefono_habitacion, celular, email) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (first_name, last_name, idCard, age, company, work_Address, office_phone, home_address, home_phone, cell_phone, email)
            )
            mysql.connection.commit()
        except Exception as e:
            print(f"Error al insertar datos: {e}")
        finally:
            cursor.close()
        return redirect(url_for('index'))
    elif request.method == 'POST' and request.form.get('userType') == 'corporativo':
        try:
            corporate_name = request.form['corporateName']
            contact_person = request.form['contactPerson']
            corporate_address = request.form['corporateAddress']
            corporate_phone = int(request.form['corporatePhone'])
            rif = request.form['rif']
            nit = request.form['nit']
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO clientescorporativos '
                '(nombre_empresa, persona_contacto, direccion, telefono, rif, nit) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (corporate_name,contact_person ,corporate_address ,corporate_phone ,rif ,nit )
            )
            mysql.connection.commit()
        except Exception as e:
            print(f"Error al insertar datos: {e}")
        finally:
            cursor.close()
        return redirect(url_for('index'))
    return render_template('user_register.html')

#FUNCION DE LOGIN
@app.route('/access/', methods=["GET", "POST"])
def lobby():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        try:
            estado_zona = request.form['estado_zona']
            destino = request.form['destino']
            vehiculo = request.form['vehiculo']
            fecha_salida = request.form['fecha_salida']
            cursor.execute('SELECT id FROM servicios WHERE tipo_servicio = %s', (vehiculo,))
            servicio_id = int(cursor.fetchone()['id'])
            # Buscar el ID en la tabla clientescorporativos
            nit = request.form.get('nit')
            cursor.execute('SELECT id FROM clientescorporativos WHERE nombre_empresa = %s and nit = %s', (session['user'], nit))
            account = cursor.fetchone()
            if account:
                identificacion = account['id']
                tipo = 'ClienteCorporativo'
            else:
                correo = 'moisesmachado2006@gmail.com'
                # Si no se encuentra en clientescorporativos, buscar en usuarioscomunes
                cursor.execute('SELECT id FROM usuarioscomunes WHERE email = %s', (correo,))
                account = cursor.fetchone()
                if account:
                    identificacion = account['id']
                    tipo = 'Cliente comun'
                else:
                    raise Exception("Usuario no encontrado en ninguna tabla")

            if identificacion:
                cursor.execute(
                    'INSERT INTO solicitudes '
                    '(cliente_tipo,cliente_id,destino,estado_zona,servicio_id,fecha_solicitud) '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (tipo, identificacion, destino, estado_zona, servicio_id, fecha_salida)
                )
                mysql.connection.commit()
            else:
                raise Exception("Identificación del cliente no válida")
        except Exception as e:
            print(f"Error De Solicitud: {e}")
        finally:
            cursor.close()
        return render_template('session.html', user=session['user'], identificacion=session['identificacion'], tipo=session['tipo'])
    return render_template('session.html', user=session['user'], identificacion=session['identificacion'], tipo=session['tipo'])

if __name__ == '__main__':
    app.secret_key= "3054=HitM"
    app.run(port = 50, debug = True)
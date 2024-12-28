<<<<<<< HEAD
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
=======
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory,session
from flask_mysqldb import MySQL, MySQLdb
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
# import MySQLdb

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Inicialización de SQL y LoginManager


#base de datos
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Clave123')
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='3054=HitM'
app.config['MYSQL_DB']='agencia'
app.config['MYSQL_CURSORCLASS']='DictCursor'

MySQL = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
#usuarios
class Cliente(UserMixin):
    def __init__(self, id_u, nombre, apellido, cedula_identidad, edad, empresa_trabajo, direccion_trabajo, telefono_oficina, direccion_habitacion, telefono_habitacion, celular, email, modalidad_servicio, ultimo_servicio_id, responsable_ultimo_servicio):
        self.id = id_u
        self.nombre = nombre
        self.apellido = apellido
        self.cedula_identidad = cedula_identidad
        self.edad = edad
        self.empresa_trabajo = empresa_trabajo
        self.direccion_trabajo = direccion_trabajo
        self.telefono_oficina = telefono_oficina
        self.direccion_habitacion = direccion_habitacion
        self.telefono_habitacion = telefono_habitacion
        self.celular = celular
        self.email = email
        self.modalidad_servicio = modalidad_servicio
        self.ultimo_servicio_id = ultimo_servicio_id
        self.responsable_ultimo_servicio = responsable_ultimo_servicio

    @staticmethod
    def get(user_id):
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarioscomunes WHERE id = %s', (user_id,))
        cliente = cursor.fetchone()
        if cliente:
            return Cliente(cliente['id'],
                            cliente['nombre'],
                            cliente['apellido'],
                            cliente['cedula_identidad'],
                            cliente['edad'],
                            cliente['empresa_trabajo'],
                            cliente['direccion_trabajo'],
                            cliente['telefono_oficina'],
                            cliente['direccion_habitacion'],
                            cliente['telefono_habitacion'],
                            cliente['celular'],
                            cliente['email'],
                            cliente['modalidad_servicio'],
                            cliente['ultimo_servicio_id'],
                            cliente['responsable_ultimo_servicio'])
        return None

class Corporativos(UserMixin):
    def __init__(self, id_c, nombre_empresa, persona_contacto, direccion, telefono, rif, nit, ultimo_servicio_id, responsable_ultimo_servicio):
        self.id = id_c
        self.nombre_empresa = nombre_empresa
        self.persona_contacto = persona_contacto
        self.direccion = direccion
        self.telefono = telefono
        self.rif = rif
        self.nit = nit
        self.ultimo_servicio_id = ultimo_servicio_id
        self.responsable_ultimo_servicio = responsable_ultimo_servicio

    @staticmethod
    def get(corp_id):
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clientescorporativos WHERE id = %s', (corp_id,))
        corporativo = cursor.fetchone()
        if corporativo:
            return Corporativos(corporativo['id'],
                                corporativo['nombre_empresa'],
                                corporativo['persona_contacto'],
                                corporativo['direccion'],
                                corporativo['telefono'],
                                corporativo['rif'],
                                corporativo['nit'],
                                corporativo['ultimo_servicio_id'],
                                corporativo['responsable_ultimo_servicio'])
        return None

@login_manager.user_loader
def load_user(user_id):
    if Cliente: return Cliente.get(int(user_id))
    else: return Corporativos.get(int(corp_id))

@app.route('/',methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'correo' in request.form and 'password' in request.form:
        correo = request.form['correo']
        password = request.form['password']
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarioscomunes WHERE email = %s', (correo,))
        cliente = cursor.fetchone()
        cursor.execute('SELECT * FROM clientescorporativos WHERE nombre_empresa = %s', (correo,))
        corporativo = cursor.fetchone()
        if cliente and password:
            login_user(Cliente.get(cliente['id']))
            session['user_id'] = cliente['id']
            session['user_type'] = 'Cliente comun' 
            return redirect(url_for('lobby'))
        elif corporativo and password:
            login_user(Corporativos.get(corporativo['id']))
            session['user_id'] = corporativo['id']
            session['user_type'] = 'ClienteCorporativo' 
            return redirect(url_for('lobby'))
        else:
            msg = 'datos invalidos'
            flash(msg)
    MySQL.connection.commit()
    return render_template('index.html', msg=msg)


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
            
            cursor = MySQL.connection.cursor()
            cursor.execute(
                'INSERT INTO usuarioscomunes '
                '(nombre, apellido, cedula_identidad, edad, empresa_trabajo, direccion_trabajo, telefono_oficina, direccion_habitacion, telefono_habitacion, celular, email) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (first_name, last_name, idCard, age, company, work_Address, office_phone, home_address, home_phone, cell_phone, email)
            )
            MySQL.connection.commit()
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
            cursor = MySQL.connection.cursor()
            cursor.execute(
                'INSERT INTO clientescorporativos '
                '(nombre_empresa, persona_contacto, direccion, telefono, rif, nit) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (corporate_name,contact_person ,corporate_address ,corporate_phone ,rif ,nit )
            )
            MySQL.connection.commit()
        except Exception as e:
            print(f"Error al insertar datos: {e}")
        finally:
            cursor.close()
        return redirect(url_for('index'))
    return render_template('user_register.html')

#FUNCION DE LOGIN
@app.route('/access', methods=["GET", "POST"])
@login_required
def lobby():
    if request.method == 'POST':
        msg = None
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        estado_zona = request.form['estado_zona']
        destino = request.form['destino']
        vehiculo = request.form['vehiculo']
        fecha_salida = request.form['fecha_salida']
        cursor.execute('SELECT id FROM servicios WHERE tipo_servicio = %s', (vehiculo,))
        servicio_id = int(cursor.fetchone()['id'])
        nit = request.form.get('nit')
        identificacion = session['user_id']
        tipo = session['user_type']
        if identificacion:
            cursor.execute(
                'INSERT INTO solicitudes '
                '(cliente_tipo,cliente_id,destino,estado_zona,servicio_id,fecha_solicitud) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (tipo, identificacion, destino, estado_zona, servicio_id, fecha_salida)
            )
            MySQL.connection.commit()
            msg = 'Solicitud Completada Exitosamente'
            flash(msg)
    return render_template('session.html',msg=msg)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key= "3054=HitM"
>>>>>>> 17a5b48 (mejora en la estructura del back-end)
    app.run(port = 50, debug = True)
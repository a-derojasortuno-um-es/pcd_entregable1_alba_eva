from enum import Enum

# Excepción que corresponde a cuando se han introducen datos que aún no están almacenados.
class NotFound(Exception):
    pass

# Excepción que salta cuando se han introducido datos incorrectos como asignaturas ya creadas, por ejemplo.
class Repeated(Exception):  
    pass

class Persona:
    def __init__(self,nombre,DNI,direccion,sexo):
        assert len(DNI)==9, 'Formato de DNI incorrecto.'
        assert sexo == 'M' or sexo == 'F', 'Opción inválida. Opciones válidad para sexo: M / F'
        assert type(nombre) == str, 'Formato del nombre incorrecto.'
        self.nombre = nombre
        self._DNI = DNI
        self._direccion  = direccion
        self._sexo = sexo
    # Método que será común a todas las clases heredadas y que devolverá los datos personales.
    def devuelveDatos(self): 
        return "Nombre: " + self.nombre + "\nDNI: " +str(self._DNI) + "\nDirección: " + str(self._direccion) + "\nSexo: " + self._sexo


class Miembro_departamento:
    def __init__(self, departamento):
        self._departamento = departamento
    
    # como el atributo departamento es privado, es necesario crear un método específico para obtenerlo.
    def get_dep(self):
        return self._departamento
    
    # para cambiar el departamento simplemente se intercambia el atributo por el nuevo departamento.
    def cambiar_dep(self, dep):
        self._departamento = dep


# Enumeración de los departamentos.
class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3
    

class Asignatura: 
    def __init__(self,nombre,creditos): 
        self.nombre = nombre
        self._creditos = creditos
        # Se crea un atributo extra para cada asignatura que contenga los profesores que imparten esta y los estudiantes que la cursan.
        self._roles = {'profesor':[],'estudiantes':[]}
    
    # Tanto en add_estudiante como en add_profesor se añaden sus objetos directamente a la lista de los roles para luego poder acceder a sus datos.

    def add_estudiante(self,estudiante): 
        self._roles['estudiantes'].append(estudiante)
    
    def add_profesor(self,profesor): 
        self._roles['profesor'].append(profesor) # Se acepta que una misma asignatura la den varios profesores.
    
    def del_estudiante(self,estudiante):
        self._roles['estudiantes'].remove(estudiante)

    def del_profesor(self,profesor):
        self._roles['profesor'].remove(profesor)

    # Se listan los estudiantes, con sus respectivos datos, que dan esta asignatura.
    def lista_estudiantes(self):
        print("Para la asignatura de",self.nombre,"se tienen los siguientes estudiantes: ")
        for i in self._roles['estudiantes']:
            print(i) 
    
    # La impresión de esta asignatura consistirá en su nombre, sus créditos, el número de estudiantes que la cursan porque se supone que los datos
    # de cada alumno no será relevante para la información de la asignatura en sí. Por último, se imprimen los profesores que la imparten.
    # En el caso de que no haya nadie que la de, se informará de ella, mientras que se hará una distinción por comas en el caso de que haya varios profesores
    # que la den.
    
    def __str__(self):
        cadena = 'Asignatura: '+self.nombre+'\nCréditos: '+str(self._creditos)+'\nNº estudiantes: '+str(len(self._roles["estudiantes"]))+'\nProfesores: '
        if len(self._roles["profesor"]) == 0:
            cadena += "No hay ningún profesor a cargo de esta asignatura aún."
        else:
            for i in range(len(self._roles["profesor"])):
                if i == len(self._roles["profesor"])-1:
                    cadena += self._roles["profesor"][i].nombre
                else:
                    cadena += self._roles["profesor"][i].nombre + ', '
        cadena += "\n"
        return cadena

# Investigador hereda de Persona.
class Investigador(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self._area = area
        # como se utiliza la composición, nada más crear el objeto Investigador, se crea su objeto Miembro_departamento.
        self.miembro  = Miembro_departamento(departamento) 

    def __str__(self):
        return self.devuelveDatos() +'\nArea de investigación: '+self._area+'\nDepartamento:'+str(self.miembro.get_dep())+'\n'

# ProfesorTitular hereda de Persona.
class ProfesorTitular(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area_inv, departamento):
        super().__init__(nombre, DNI, direccion, sexo)

        # Se añade la lista de asignaturas que el ProfesorTitular imparte para que a la hora de mostrar las asignatura que da, sea más sencillo mostrarlas.
        self.listaAsig = []

        # Por composición se inicializan tanto el objeto Investigador como el de Miembro_departamento asociado.
        self.rol_inv = Investigador(nombre, DNI ,direccion , sexo, area_inv, departamento)
        self.miembro  = Miembro_departamento(departamento) 
    
    # Para añadir y eliminar asignaturas del profesor simplemente se añaden los objetos Asignatura a la listaAsig.

    def add_asig(self,asig): 
        self.listaAsig.append(asig)
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    # Método para mostrar todas las asignaturas.

    def mostrar_asig(self):
        print(f"El profesor titular {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: 
           print(i,"\n")

    # Para imprimir el objeto ProfesorTitular no se incluye el área de investigación porque irá incluido en el objeto Investigador.

    def __str__(self):
        return self.devuelveDatos() + '\nDepartamento:'+str(self.miembro.get_dep())+'\n'
       
            
class ProfesorAsociado(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = [] # al igual que en ProfesorTitular se incluye la lista de las asignaturas.
        self.miembro  = Miembro_departamento(departamento)

    # Igual que en ProfesorTitular

    def add_asig(self,asig):
        self.listaAsig.append(asig) 
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def mostrar_asig(self):
        print(f"El profesor asociado {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: 
            print(i)

    def __str__(self):
        return self.devuelveDatos() + '\nDepartamento: '+str(self.miembro.get_dep())


# La clase Estudiante sigue el mismo patrón que ProfesorTitular y ProfesorAsociado.
class Estudiante(Persona):
    def __init__(self, nombre, DNI, direccion, sexo):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = []
    
    def add_asig(self,asig):
        self.listaAsig.append(asig) 
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def mostrar_asig(self):
        print("Estudiante:",self.nombre,"cursa las siguientes asignaturas: ")
        for i in self.listaAsig:
            print(i)
    
    def __str__(self):
        return self.devuelveDatos()


# En la clase principal de Universidad se incluirán todos los métodos accesibles para el usuario.
    
# Se incluyen listas que contendrán los objetos de cada tipo, así como un diccionario de que incluirá para cada departamento, qué profesores forman parte de él.
# Este diccionario simplificará bastante el método que se incluye más adelante y que imprime, para un departamento en cuestión, quiénes forman parte de él.
# Se ha tomado la decisión de incluir una lista de asignaturas totales que posee la universidad que, a pesar de que no tenga sentido aparente y como no se tiene
# ninguna clase Grado, unificará bastante el código y nos permitirá relacionar asignaturas con Estudiante y las dos clases Profesor.

class Universidad:
    def __init__(self,nombre,codpostal,ciudad):
        self.nombre = nombre
        self._codpostal = codpostal
        self._ciudad = ciudad
        self._lista_inves = []
        self._lista_prof_tit = []
        self._lista_prof_asoc = []
        self._lista_est = []
        self._lista_asig = []
        self._departamentos = {}  
    
    # Se hacen métodos privados que ayudarán a buscar objetos por su nombre para facilitar la lectura del código.

    # En el caso de asignatura y estudiante si no se ha encontrado ninguna coincidencia salta un error.
        
    def _buscaasig(self,nombre):
        try:
            i = 0
            fin = False
            while i < len(self._lista_asig) and not fin:
                if self._lista_asig[i].nombre == nombre:
                    asig = self._lista_asig[i]
                    fin = True
                i += 1
            return asig
        except:
            raise NotFound('Error. Esta asignatura no existe.')
    
    def _buscaestud(self,estudiante):
        try:
            i = 0
            fin = False
            while i < len(self._lista_est) and not fin:
                if self._lista_est[i].nombre == estudiante:
                    est = self._lista_est[i]
                    fin = True
                i += 1
            return est
        except:
            raise NotFound('Error. Este estudiante no existe.')
    
    # En el caso de los profesores y de Investigador, se ha optado por no invocar ningún error a priori y si no se ha encontrado ninguna coincidencia que se 
    # devuelve el objeto a None.
    # Se ha realizado de esta manera porque, con el objetivo de unificar los métodos de Profesor, se necesitará verificar si una persona es ProfesorTitular,
    # ProfesorAsociado o ninguna de la dos y se conseguirá comparando los resultados de la búsqueda de ambos objetos.   
    
    def _buscaprofAsoc(self,profesor): # buscamos por nombre 
        prof = None
        i = 0
        fin = False
        while i < len(self._lista_prof_asoc) and not fin:
            if self._lista_prof_asoc[i].nombre == profesor:
                prof = self._lista_prof_asoc[i]
                fin = True
            i += 1
        return prof
                
    def _buscaprofTitular(self,profesor):
        prof = None
        i = 0
        fin = False
        while i < len(self._lista_prof_tit) and not fin:
            if self._lista_prof_tit[i].nombre == profesor:
                prof = self._lista_prof_tit[i]
                fin = True
            i += 1
        return prof
            
    def _buscainvest(self,investigador):
        invest = None
        i = 0
        fin = False
        while i < len(self._lista_inves) and not fin:
            if self._lista_inves[i].nombre == investigador:
                invest = self._lista_inves[i]
                fin = True
            i += 1
        return invest
    
    # Se incluyen estos métodos privados para añadir y eliminar personas de un departamento con el fin de simplificar el código.
    
    def _add_persona_dep(self,pers,dep):
        if str(dep) in self._departamentos: 
            self._departamentos[str(dep)].append(pers) 
        else:
            self._departamentos[str(dep)] = [pers]
    
    def _del_pers_dep(self,pers):
        dep_ant = pers.miembro.get_dep()
        self._departamentos[str(dep_ant)].remove(pers)
    

    def add_estudiante(self,nombre,DNI,direccion,sexo):
        est = Estudiante(nombre,DNI,direccion,sexo)
        self._lista_est.append(est)
    
    # Si se incluye area de investigación querrá decir que es un ProfesorTitular, mientras que si no se incluye será un ProfesorAsociado.
    
    def add_prof(self,nombre,DNI,direccion,sexo,departamento,area_inv=None):
        if area_inv != None: # querrá decir que es un profesor titular
            prof = ProfesorTitular(nombre,DNI,direccion,sexo,area_inv,departamento)
            self._lista_prof_tit.append(prof)
            self._lista_inves.append(prof) # el profesor titular deberá estar, a su vez, en las dos listas. 
        else: # es un profesor asociado.
            prof = ProfesorAsociado(nombre,DNI,direccion,sexo,departamento)
            self._lista_prof_asoc.append(prof)
        
        # finalmente se añadirá al profesor en su respectivo departamento.
        self._add_persona_dep(prof,departamento)
     
    def add_investigador(self,nombre,DNI,direccion,sexo,area,departamento):
        invest = Investigador(nombre,DNI,direccion,sexo,area,departamento)
        self._lista_inves.append(invest)

        # Igual que en los métodos de los profesores.
        self._add_persona_dep(invest,departamento)
    
    def add_asig(self,nombre,creditos):
        for i in self._lista_asig:
            if i.nombre == nombre: # Controlar que no haya asignaturas repetidas.
                raise Repeated('Error. Ya hay una asignatura con este nombre.')
        asig = Asignatura(nombre,creditos)
        self._lista_asig.append(asig)

    def del_estudiante(self,estudiante):
        est = self._buscaestud(estudiante)
        self._lista_est.remove(est) # se elimina de la lista de estudiantes.
        for i in est.listaAsig: 
            i.del_estudiante(est) # de cada asignatura que tenga el estudiante se elimina a este mismo.

    # Se ha unificado en un mismo método la eliminación de cualquier tipo de profesor con el fin de hacer más sencilla la consulta para el usuario.
            
    def del_profesor(self,profesor):
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None: # El profesor no será asociado y, por tanto, se hace la búsqueda de los titulares.
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None: # Como el profesor no es ni asociado ni titular, entonces querrá decir que ese nombre no corresponde a ningún profesor.
                raise NotFound('Error. Este profesor no se encuentra en la base de datos') 
            else: # signfica que profesor es un profesor titular.
                self._del_pers_dep(prof_titular)
                self._lista_prof_tit.remove(prof_titular)
                self._lista_inves.remove(prof_titular) # al ser una composición también se elimina.
                for i in prof_titular.listaAsig: # se elimina de cada asignatura donde imparta clase al profesor titular.
                    i.del_profesor(prof_titular)
        else: # es un profesor asociado
            self._del_pers_dep(prof_asoc)
            self._lista_prof_asoc.remove(prof_asoc)
            for i in prof_asoc.listaAsig:
                i.del_profesor(prof_asoc)
        
    def del_investigador(self,investigador):
        try:
            invest = self._buscainvest(investigador)
            self._lista_inves.remove(invest)
            self._del_pers_dep(invest)
            if invest in self._lista_prof_tit:
                self._lista_prof_tit.remove(invest) # se elimina también de la lista de profesores titulares.
        except:
            raise NotFound('Error. Este investigador no se encuentra en la base de datos.')
        
    # Solo existirá un método único para cambiar el departamento. La forma de proceder será viendo si el objeto _buscar... devuelve None o si, por el contrario,
    # ha encontrado el objeto que se deseaba.
    # Primero se va a comprobar que el departamento insertado sea el correcto y si no, saldrá un error.

    # Como la variable dep será un objeto de la clase Departamento se debe meter en el diccionario de los departamentos propio de Universidad como un cadena de texto.

    def cambiar_dep(self,nombre, dep):
        assert dep == Departamento.DIIC or dep == Departamento.DIS or dep == Departamento.DITEC , 'Nombre de departamento inválido.'
        p = self._buscaprofAsoc(nombre)
        if p != None:
            self._del_pers_dep(p)
            p.miembro.cambiar_dep(dep)
            self._add_persona_dep(p,dep)
        else:
            pt = self._buscaprofTitular(nombre)
            if pt != None:
                self._del_pers_dep(pt)
                pt.miembro.cambiar_dep(dep)
                inv = self._buscainvest(nombre) 
                inv.miembro.cambiar_dep(dep)
                self._add_persona_dep(pt,dep)
            else:
                i = self._buscainvest(nombre)
                if self._buscainvest(nombre) != None:
                    self._del_pers_dep(i)
                    i.miembro.cambiar_dep(dep)
                    self._add_persona_dep(i,dep)
                else:
                    raise NotFound('Error. Esta persona no se encuentra en la base de datos.')
            
    def asignar_asig_est(self,estudiante,nom_asig):
        asig = self._buscaasig(nom_asig)
        est = self._buscaestud(estudiante)
        if asig in est.listaAsig:
            raise Repeated('Error. Esta asignatura ya estaba asignada a este estudiante.')
        est.add_asig(asig)
        asig.add_estudiante(est)
    
    def del_asig_est(self, estudiante, nom_asig):
        asig = self._buscaasig(nom_asig)
        est = self._buscaestud(estudiante)
        if asig not in est.listaAsig:
            raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del estudiante.')
        est.del_asig(asig)
        asig.del_estudiante(est)

    def asignar_asig_prof(self,profesor,nom_asig): # nombre del profesor asig y nombre de la asignatura.
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_tit = self._buscaprofTitular(profesor)
            if prof_tit == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # profesor titular
                if asig in prof_tit.listaAsig:
                    raise Repeated('Error. Esta asignatura ya estaba asignada a este profesor.')
                prof_tit.add_asig(asig)
                asig.add_profesor(prof_tit)
        else:
            if asig in prof_asoc.listaAsig:
                    raise Repeated('Error. Esta asignatura ya estaba asignada a este profesor.')
            prof_asoc.add_asig(asig)
            asig.add_profesor(prof_asoc)
    
    def del_asig_prof(self, profesor, nom_asig):
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_tit = self._buscaprofTitular(profesor)
            if prof_tit == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # profesor titular
                if asig not in prof_tit.listaAsig:
                    raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del profesor.')
                prof_tit.del_asig(asig)
                asig.del_profesor(prof_tit)
        else:
            if asig not in prof_asoc.listaAsig:
                    raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del profesor.')
            prof_asoc.del_asig(asig)
            asig.del_profesor(prof_asoc)
        
    def mostrar_asign_estudiante(self,estudiante): 
        est = self._buscaestud(estudiante)
        est.mostrar_asig()

    def mostrar_asign_profesor(self,profesor): 
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # signfica que profesor es un profesor titular.
                prof_titular.mostrar_asig()
        else: # es un profesor asociado
            prof_asoc.mostrar_asig()

# Como se ha almacenado el diccionario con los departamentos existentes y sus miembros, el método para mostrarlos será mucho más sencillo.
            
# Para que la impresión sea mucho más sencilla se eliminará el prefijo 'Departamento.' y nos quedaremos con el nombre en sí.

    def mostrar_dep(self,dep):
        try:
            print(f"--MIEMBROS DEL DEPARTAMENTO {str(dep)[13:]} --","\n")
            for i in self._departamentos[str(dep)]:
                print(i,"\n")
        except:
            raise NotFound('No se encuentra este departamento.')

    def mostrar_asignaturas(self):
        print("La Universidad",self.nombre,"imparte las siguientes asignaturas: ")
        for i in self._lista_asig:
            print(i,"\n")
    
    def mostrar_estudiantes_asign(self, nom_asig):
        a = self._buscaasig(nom_asig)
        a.lista_estudiantes()
    
    def mostrar_profesores(self):
        print("--PROFESORES ASOCIADOS--","\n")
        for asoc in self._lista_prof_asoc:
            print(asoc,"\n")
        print("--PROFESORES TITULARES--","\n")
        for tit in self._lista_prof_tit:
            print(tit)
    
    def mostrar_estudiantes(self):
        print("--LISTADO ESTUDIANTES--","\n")
        for est in self._lista_est:
            print(est,"\n")
    
    def mostrar_investigadores(self):
        print("--LISTADO INVESTIGADORES--","\n")
        for inv in self._lista_inves:
            print(inv,"\n")
    
    def __str__(self):
        return "Universidad " + self.nombre + " con código postal " + str(self._codpostal) + " situada en la ciudad de " + self._ciudad
    
        

uni = Universidad('UMU',30840,'Murcia')
print(uni)
uni.add_asig('Matemáticas', 6)
uni.add_asig('Física',4)
#uni.add_asig('Matemáticas',8) # saldrá error por repetir una asignatura ya creada.
uni.add_asig('Lengua',8)
uni.add_asig('Historia',6)
uni.mostrar_asignaturas()

uni.add_prof('Ana Martínez','12345678A','Murcia','F',Departamento.DIIC)
uni.asignar_asig_prof('Ana Martínez','Lengua')

uni.add_prof('Sara Lorente','45326678D','Sevilla','F',Departamento.DITEC)
uni.asignar_asig_prof('Sara Lorente','Historia')

uni.add_prof('Juan Fernández','12121212B','Madrid','M',Departamento.DIS)
uni.asignar_asig_prof('Juan Fernández','Física')
uni.asignar_asig_prof('Juan Fernández','Matemáticas')

uni.mostrar_asign_profesor('Juan Fernández')
    
uni.add_prof('Pepe Ruiz','90091234C','León','M',Departamento.DITEC,'Área de Computadores')
uni.asignar_asig_prof('Pepe Ruiz','Matemáticas')
uni.asignar_asig_prof('Pepe Ruiz','Historia')
    
uni.mostrar_profesores()

uni.cambiar_dep('Pepe Ruiz',Departamento.DIIC)

uni.mostrar_dep(Departamento.DIIC)

uni.mostrar_investigadores()

uni.mostrar_asignaturas()

uni.del_profesor('Juan Fernández')

uni.mostrar_profesores()
    
#uni.add_estudiante('Mar Soler', '571867890L', 'Valladolid', 'F') # tendrá un error de DNI por tener una longitud de 10, en vez de 9.

uni.add_estudiante('Manuel Rodríguez', '87654321M', 'Valladolid', 'M')
uni.asignar_asig_est('Manuel Rodríguez','Matemáticas')
uni.asignar_asig_est('Manuel Rodríguez','Física')

uni.add_estudiante('Emma García', '92302020P', 'Barcelona', 'F')
uni.asignar_asig_est('Emma García','Historia')
uni.asignar_asig_est('Emma García','Lengua')

uni.add_estudiante('Jose Domínguez', '22222222M', 'Bilbao', 'M')
#uni.asignar_asig_est('Jose Domínguez','Cálculo') # dará fallo porque la asignatura no se encontrará
uni.asignar_asig_est('Jose Domínguez','Física')

uni.mostrar_estudiantes()

uni.mostrar_asign_estudiante('Emma García')

uni.del_asig_est('Emma García','Lengua')

uni.mostrar_asign_estudiante('Emma García')

uni.del_estudiante('Jose Domínguez')

uni.mostrar_estudiantes()
    
uni.mostrar_estudiantes_asign('Física')


#TEST UNITARIOS

def test_del_profesor():
    uni.del_profesor('Ana Martínez')

def test_del_estudiante():
    uni.del_estudiante('Emma García')

def test_del_investigador():
    uni.del_investigador('Pepe Ruiz')

def test_add_asig():
    uni.add_asig('Biología',6)

def test_cambiar_dep():
    uni.cambiar_dep('Sara Lorente', Departamento.DIS) 

def test_asignar_asig_est():
    uni.asignar_asig_est('Manuel Rodríguez', 'Lengua')

def test_del_asig_est():
    uni.del_asig_est('Manuel Rodríguez','Lengua')

def test_asignar_asig_prof():
    uni.asignar_asig_prof('Sara Lorente', 'Física')

def test_del_asig_prof():
    uni.del_asig_prof('Sara Lorente', 'Física')

def test_mostrar_dep():
    uni.mostrar_dep(Departamento.DIIC)
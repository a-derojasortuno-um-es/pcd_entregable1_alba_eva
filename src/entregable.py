class PersonaNotFound(Exception):
    pass

class Persona:
    def __init__(self,nombre,DNI,direccion,sexo):
        self.nombre = nombre
        self.DNI = DNI
        self.direccion  = direccion
        self.sexo = sexo
    def devuelveDatos(self): # o __str__ --- método abstracto??
        return self.nombre + str(self.DNI) + str(self.direccion) + self.sexo

class miembro_departamento:
    def __init__(self,departamento):
        self.departamento = departamento
    
class Asignatura: 
    def __init__(self,nombre,creditos,roles={'profesor':[],'estudiantes':[]}): 
        self.nombre = nombre
        self.creditos = creditos
        self.roles = roles 
    
    def add_estudiante(self,estudiante): # se añade el objeto estudiante
        self.roles['estudiantes'].append(estudiante) # añadir el objeto o el nombre????
    
    def add_profesor(self,profesor): # una asignatura la pueden dar varios profesores.
        self.roles['profesor'].append(profesor)
    
    def del_estudiante(self,estudiante):
        self.roles['estudiantes'].remove(estudiante)

    def del_profesor(self,profesor):
        self.roles['profesor'].remove(profesor)

    def lista_estudiantes(self):
        print("Para la asignatura ",self.nombre," se tienen los siguientes estudiantes: ")
        for i in self.roles['estudiantes']:
            print(i) # pase lo que pase, si tiene un objeto o el nombre se imprimirá i.
    
    def __str__(self):
        result = ""
        result = result + "Asignatura:" + self.nombre + "con" + str(self.creditos) + "créditos," + len(self.roles["estudiantes"])  + "estudiantes y que la imparten los siguientes profesores: "
        for i in self.roles["profesor"]:
            result += "\n" + "Profesor:" + i.nombre # ver si se pone todos los datos del profesor o solo el nombre.
        return result

class Investigador(Persona):
    def __init__(self,nombre,DNI,direccion,sexo,area,departamento):
        super().__init__(self,nombre,DNI,direccion,sexo)
        self.area = area
        self.miembro = miembro_departamento(departamento) # Composición.

class ProfesorTitular(Persona):
    def __init__(self,nombre,DNI,direccion,sexo,area_inv,departamento,listaAsig=[]):
        super().__init__(self,nombre,DNI,direccion,sexo)
        self.listaAsig = listaAsig # contendrá los objetos de las asignaturas -- asignaturas diferentes. ** EXCEPCIÓN.
        self.rol_inv = Investigador(nombre,DNI,direccion,sexo,area_inv,departamento) # repetición de información.
        self.miembro = miembro_departamento(departamento)

    def add_asig(self,asig): # se implementará en la clase Universidad porque ahí estará la lista de asignaturas
        self.listaAsig.append(asig)

    def mostrar_asig(self):
        print(f"El profesor titular {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: # sup que son objetos
           print(i,"\n") # se imprime el objeto Asignatura.
        
            
class ProfesorAsociado(Persona):
    def __init__(self,nombre,DNI,direccion,sexo,departamento,listaAsig=[]): # se inicializa la lista de asignaturas a vacío.
        super().__init__(self,nombre,DNI,direccion,sexo)
        self.listaAsig = listaAsig # ¿método para añadir asignaturas a un profesor??
        self.miembro = miembro_departamento(departamento) # composición - se instancia a la vez la clase miembro_departamento
    
    def add_asig(self,asig):
        self.listaAsig.append(asig) # se mete el nombre de la asignatura o el objeto ????
    
    def mostrar_asig(self):
        print(f"El profesor asociado {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: # sup que son objetos
            print(i,"\n")


class Estudiante(Persona):
    def __init__(self,nombre,DNI,direccion,sexo,listaAsig=[]): # la lista de asignaturas en un principio está vacía.
        super().__init__(self,nombre,DNI,direccion,sexo)
        self.listaAsig = listaAsig
    
    def add_asig(self,asig):
        self.listaAsig.append(asig) 
    
    def mostrar_asig(self):
        print("El estudiante ",self.nombre," tiene la siguientes asignaturas: ")
        for i in self.listaAsig:
            print(i,"\n")

class Universidad:
    def __init__(self,nombre,codpostal,ciudad,lista_inves=[],lista_prof_tit=[],lista_prof_asoc=[],lista_est=[],lista_asig=[]):
        self.nombre = nombre
        self.codpostal = codpostal
        self.ciudad = ciudad
        self._lista_inves = lista_inves # a cada lista se añaden los objetos en sí para poder recuperar sus datos.
        self._lista_prof_tit = lista_prof_tit
        self._lista_prof_asoc = lista_prof_asoc
        self._lista_est = lista_est
        self._lista_asig = lista_asig

    
    # se va a diferenciar a la hora de asignar asignaturas a profesores entre su rol. --- nos ahorramos recorrer dos listas.
    # vale la pena?    
    
    def _buscaasig(self,nombre): # se hace un método para encontrar por el nombre de la asignatura el objeto.
        asig = None
        for i in self._listaasig:
            if i.nombre == nombre:
                asig = i # poner un break?
        return asig

    def _buscaprofAsoc(self,profesor): # buscamos por nombre o por DNI??
        prof = None
        for i in self._lista_prof_asoc:
            if i.nombre == profesor:
                prof = i
        return prof
        
    def _buscaprofTitular(self,profesor):
        prof = None
        for i in self._lista_prof_tit:
            if i.nombre == profesor:
                prof = i
        return prof
    
    def _buscaestud(self,estudiante):
        est = None
        for i in self._lista_est:
            if i.nombre == estudiante: # habrá que ver si se mira por nombre o por DNI.
                est = i
        return est
    
    def _buscainvest(self,investigador):
        invest = None
        for i in self._lista_inves:
            if i.nombre == investigador:
                invest = i
        return invest
    
    def add_estudiante(self,nombre,DNI,direccion,sexo):
        est = Estudiante(nombre,DNI,direccion,sexo)
        self._lista_est.append(est)
    
    def add_prof_titular(self,nombre,DNI,direccion,sexo,area_inv,departamento):
        prof_tit = ProfesorTitular(nombre,DNI,direccion,sexo,area_inv,departamento)
        self._lista_prof_tit.append(prof_tit)
        self._lista_inves.append(prof_tit) # el profesor titular deberá estar, a su vez, en las dos listas. -- unificar variables.
    
    def add_prof_asoc(self,nombre,DNI,direccion,sexo,departamento):
        prof_asoc = ProfesorAsociado(nombre,DNI,direccion,sexo,departamento)
        self._lista_prof_asoc.append(prof_asoc)
    
    def add_investigador(self,nombre,DNI,direccion,sexo,area,departamento):
        invest = Investigador(nombre,DNI,direccion,sexo,area,departamento)
        self._lista_inves.append(invest)
    
    def add_asig(self,nombre,creditos):
        asig = Asignatura(nombre,creditos) # ya se ha creado una nueva instancia de asignatura.
        self._lista_asig.append(asig)

    def del_estudiante(self,estudiante):
        try:
            est = self._buscaestud(estudiante)
            self._lista_est.remove(est) # se elimina de la lista de estudiantes.
            for i in est.listaAsig: # en la lista de asignaturas de estudiante estará almacenado los objetos asignaturas.
                i.del_estudiante(est) # habrá que eliminar de las asig que tenga el estudiante a este mismo.
        except:
            raise PersonaNotFound()
    
    def del_profesor(self,profesor):
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise PersonaNotFound() # ese nombre no corresponde a ningún profesor.
            else: # signfica que profesor es un profesor titular.
                prof = self._buscaprofTitular(profesor)
                self._lista_prof_tit.remove(prof)
                self._lista_inves.remove(prof) # al ser una composición también se elimina.
                for i in prof.listaAsig:
                    i.del_profesor(prof)
        else: # es un profesor asociado
            prof = self._buscaprofAsoc(profesor)
            self._lista_prof_asoc.remove(prof)
            for i in prof.listaAsig:
                i.del_profesor(prof)
        
    def del_investigador(self,investigador):
        try:
            invest = self._buscainvest(investigador)
            self._lista_inves.remove(invest)
            if invest in self._lista_prof_tit:
                self._lista_prof_tit.remove(invest) # se elimina también de la lista de investigadores.
        except:
            raise PersonaNotFound()
            
    def asignar_asig_est(self,estudiante,nom_asig):
        asig = self._buscaasig(nom_asig)
        est = self._buscaestud(estudiante)
        est.add_asig(asig)
        asig.add_estudiante(est)

    def asignar_asig_prof_asoc(self,profesor,nom_asig): # nombre del profesor asig y nombre de la asignatura.
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof = self._buscaprofAsoc(profesor)
        prof.add_asig(asig) # ya se mete en la lista de asignaturas personal de los profesores.
        asig.add_profesor(prof) # tipo de datos coinciden????
    
    def asignar_asig_prof_titular(self,profesor,nom_asig): # nombre del profesor asig y nombre de la asignatura.
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof = self._buscaprofTitular(profesor)
        prof.add_asig(asig)
        asig.add_profesor(prof)  ## ver si el tipo de datos coincide.
        
    def mostrar_lista_asig_est(self,estudiante): 
        est = self._buscaestud(estudiante)
        est.mostrar_asig()

    def mostrar_lista_asig_prof(self,profesor): 
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise PersonaNotFound()
            else: # signfica que profesor es un profesor titular.
                prof_titular.mostrar_asig()
        else: # es un profesor asociado
            prof_asoc.mostrar_asig()

    
    def mostrar_lista_asig_totales(self):
        print("La Universidad ",self.nombre," imparte las siguientes asignaturas: ")
        for i in self._lista_asig:
            print(i,"\n")
        
prof_est = {'Historia' : {'profesor' : ['Jaime'],'estudiantes' : ['Juan','Noa','Manuel']}}
print(prof_est['Historia']['estudiantes'])


### ver cuál va a ser la tira de comandos. ********
# add_asig
# hacer __str__ de asignatura. --  contar el número de estudiantes. -- nombre profesor y número de alumnos.
# __str__ profesor y estudiante: no mostrar la lista de asignaturas.




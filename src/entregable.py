from enum import Enum

class NotFound(Exception):
    pass

class Repeated(Exception):
    pass

class Persona:
    def __init__(self,nombre,DNI,direccion,sexo):
        assert len(DNI)==9, 'Formato de DNI incorrecto.'
        assert sexo == 'M' or sexo == 'F', 'Opción inválida. Opciones válidad para sexo: M / F'
        assert type(nombre) == str, 'Formato del nombre incorrecto.'
        self.nombre = nombre
        self.DNI = DNI
        self.direccion  = direccion
        self.sexo = sexo
    def devuelveDatos(self): 
        return "Nombre: " + self.nombre + "\nDNI: " +str(self.DNI) + "\nDirección: " + str(self.direccion) + "\nSexo: " + self.sexo


class Miembro_departamento:
    def __init__(self, departamento):
        self.departamento = departamento
    
    def get_dep(self):
        return self.departamento
    
    def cambiar_dep(self, dep):
        self.departamento = dep


class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3
    

class Asignatura: 
    def __init__(self,nombre,creditos): 
        self.nombre = nombre
        self.creditos = creditos
        self.roles = {'profesor':[],'estudiantes':[]}
    
    def add_estudiante(self,estudiante): # se añade el objeto estudiante
        self.roles['estudiantes'].append(estudiante) # añadir el objeto o el nombre????
    
    def add_profesor(self,profesor): # una asignatura la pueden dar varios profesores.
        self.roles['profesor'].append(profesor)
    
    def del_estudiante(self,estudiante):
        self.roles['estudiantes'].remove(estudiante)

    def del_profesor(self,profesor):
        self.roles['profesor'].remove(profesor)

    def lista_estudiantes(self):
        print("Para la asignatura de",self.nombre,"se tienen los siguientes estudiantes: ")
        for i in self.roles['estudiantes']:
            print(i) # pase lo que pase, si tiene un objeto o el nombre se imprimirá i.
    
    def __str__(self):
        cadena = 'Asignatura: '+self.nombre+'\nCréditos: '+str(self.creditos)+'\nNº estudiantes: '+str(len(self.roles["estudiantes"]))+'\nProfesores: '
        if len(self.roles["profesor"]) == 0:
            cadena += "No hay ningún profesor a cargo de esta asignatura aún."
        else:
            for i in range(len(self.roles["profesor"])):
                if i == len(self.roles["profesor"])-1:
                    cadena += self.roles["profesor"][i].nombre
                else:
                    cadena += self.roles["profesor"][i].nombre + ', '
        cadena += "\n"
        return cadena



class Investigador(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self.area = area
        self.miembro  = Miembro_departamento(departamento) # Composición.
    

    def __str__(self):
        return self.devuelveDatos() +'\nArea de investigación: '+self.area+'\nDepartamento:'+str(self.miembro.get_dep())+'\n'


class ProfesorTitular(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area_inv, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = []
        self.rol_inv = Investigador(nombre, DNI ,direccion , sexo, area_inv, departamento)
        self.miembro  = Miembro_departamento(departamento)

    def add_asig(self,asig): # se implementará en la clase Universidad porque ahí estará la lista de asignaturas
        self.listaAsig.append(asig)
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def mostrar_asig(self):
        print(f"El profesor titular {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: # sup que son objetos
           print(i,"\n") # se imprime el objeto Asignatura.

    def __str__(self):
        return self.devuelveDatos() + '\nDepartamento:'+str(self.miembro.get_dep())+'\n'
       
            
class ProfesorAsociado(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = []
        self.miembro  = Miembro_departamento(departamento)

    def add_asig(self,asig):
        self.listaAsig.append(asig) # se mete el nombre de la asignatura
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def mostrar_asig(self):
        print(f"El profesor asociado {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: # sup que son objetos
            print(i)

    def __str__(self):
        return self.devuelveDatos() + '\nDepartamento:'+str(self.miembro.get_dep())


class Estudiante(Persona):
    def __init__(self, nombre, DNI, direccion, sexo):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = []
    
    def add_asig(self,asig):
        self.listaAsig.append(asig) 
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def mostrar_asig(self):
        if self.sexo == 'M':
            print("El estudiante",self.nombre,"tiene la siguientes asignaturas: ")
        else:
            print("La estudiante",self.nombre,"tiene la siguientes asignaturas: ")
        for i in self.listaAsig:
            print(i)
    
    def __str__(self):
        return self.devuelveDatos()


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
        self._departamentos = {}  
    
    def _buscaasig(self,nombre): # se hace un método para encontrar por el nombre de la asignatura el objeto.
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
    
    
    def add_estudiante(self,nombre,DNI,direccion,sexo):
        est = Estudiante(nombre,DNI,direccion,sexo)
        self._lista_est.append(est)
    
    def add_prof_titular(self,nombre,DNI,direccion,sexo,area_inv,departamento):
        prof_tit = ProfesorTitular(nombre,DNI,direccion,sexo,area_inv,departamento)
        self._lista_prof_tit.append(prof_tit)
        self._lista_inves.append(prof_tit) # el profesor titular deberá estar, a su vez, en las dos listas. 
        if departamento in self._departamentos: 
            self._departamentos[str(departamento)].append(prof_tit) 
        else:
            self._departamentos[str(departamento)] = [prof_tit]
    
    def add_prof_asoc(self,nombre,DNI,direccion,sexo,departamento):
        prof_asoc = ProfesorAsociado(nombre,DNI,direccion,sexo,departamento)
        self._lista_prof_asoc.append(prof_asoc)
        if departamento in self._departamentos: 
            self._departamentos[str(departamento)].append(prof_asoc) 
        else:
            self._departamentos[str(departamento)] = [prof_asoc]
    
    def add_investigador(self,nombre,DNI,direccion,sexo,area,departamento):
        invest = Investigador(nombre,DNI,direccion,sexo,area,departamento)
        self._lista_inves.append(invest)
        if departamento in self._departamentos: 
            self._departamentos[str(departamento)].append(invest) 
        else:
            self._departamentos[str(departamento)] = [invest]
    
    def add_asig(self,nombre,creditos):
        for i in self._lista_asig:
            if i.nombre == nombre:
                raise Repeated('Error. Ya hay una asignatura con este nombre.')
        asig = Asignatura(nombre,creditos) # ya se ha creado una nueva instancia de asignatura.
        self._lista_asig.append(asig)

    def del_estudiante(self,estudiante):
        est = self._buscaestud(estudiante)
        self._lista_est.remove(est) # se elimina de la lista de estudiantes.
        for i in est.listaAsig: # en la lista de asignaturas de estudiante estará almacenado los objetos asignaturas.
            i.del_estudiante(est) # habrá que eliminar de las asig que tenga el estudiante a este mismo.
        
    
    def del_profesor(self,profesor):
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos') # ese nombre no corresponde a ningún profesor.
            else: # signfica que profesor es un profesor titular.
                prof = self._buscaprofTitular(profesor)
                dep_ant = prof.miembro.get_dep()
                self._departamentos[str(dep_ant)].remove(prof)
                self._lista_prof_tit.remove(prof)
                self._lista_inves.remove(prof) # al ser una composición también se elimina.
                for i in prof.listaAsig:
                    i.del_profesor(prof)
        else: # es un profesor asociado
            prof = self._buscaprofAsoc(profesor)
            dep_ant = prof.miembro.get_dep()
            self._departamentos[str(dep_ant)].remove(prof)
            self._lista_prof_asoc.remove(prof)
            for i in prof.listaAsig:
                i.del_profesor(prof)
        
    def del_investigador(self,investigador):
        try:
            invest = self._buscainvest(investigador)
            self._lista_inves.remove(invest)
            dep_ant = invest.miembro.get_dep()
            self._departamentos[str(dep_ant)].remove(invest)
            if invest in self._lista_prof_tit:
                self._lista_prof_tit.remove(invest) # se elimina también de la lista de profesores titulares.
        except:
            raise NotFound('Error. Este investigador no se encuentra en la base de datos.')
        

    def cambiar_dep(self,nombre, dep):
        assert dep == Departamento.DIIC or dep == Departamento.DIS or dep == Departamento.DITEC , 'Nombre de departamento inválido.'
        p = self._buscaprofAsoc(nombre)
        if p != None:
            dep_antiguo = p.miembro.get_dep()
            self._departamentos[str(dep_antiguo)].remove(p)
            p.miembro.cambiar_dep(dep)
            if str(dep) in self._departamentos:
                self._departamentos[str(dep)].append(p)
            else:
                self._departamentos[str(dep)] = [p]
        else:
            pt = self._buscaprofTitular(nombre)
            if pt != None:
                dep_antiguo = pt.miembro.get_dep()
                self._departamentos[str(dep_antiguo)].remove(pt)
                pt.miembro.cambiar_dep(dep)
                inv = self._buscainvest(nombre) 
                inv.miembro.cambiar_dep(dep)
                if str(dep) in self._departamentos:
                    self._departamentos[str(dep)].append(pt)
                else:
                    self._departamentos[str(dep)] = [pt]
            else:
                i = self._buscainvest(nombre)
                if self._buscainvest(nombre) != None:
                    dep_antiguo = i.miembro.get_dep()
                    self._departamentos[dep_antiguo].remove(i) 
                    i.miembro.cambiar_dep(dep)
                    if str(dep) in self._departamentos:
                        self._departamentos[str(dep)].append(i)
                    else:
                        self._departamentos[str(dep)] = [i]
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
            asig.del_profesot(prof_asoc)
        
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
    
    def mostrar_dep(self,dep):
        try:
            print(f"--MIEMBROS DEL DEPARTAMENTO {str(dep)} --")
            for i in self._departamentos[str(dep)]:
                print(i)
        except:
            raise NotFound('No se encuentra este departamento.')

    def mostrar_asignaturas(self):
        print("La Universidad",self.nombre,"imparte las siguientes asignaturas: ")
        for i in self._lista_asig:
            print(i,"\n")
    
    def mostrar_estudiantes_asign(self, nom_asig):
        a = uni._buscaasig(nom_asig)
        a.lista_estudiantes()
    
    def mostrar_profesores(self):
        print("--PROFESORES ASOCIADOS--")
        for asoc in self._lista_prof_asoc:
            print(asoc,"\n")
        print("--PROFESORES TITULARES--")
        for tit in self._lista_prof_tit:
            print(tit)
    
    def mostrar_estudiantes(self):
        print("--LISTADO ESTUDIANTES--")
        for est in self._lista_est:
            print(est,"\n")
    
    def mostrar_investigadores(self):
        print("--LISTADO INVESTIGADORES--")
        for inv in self._lista_inves:
            print(inv,"\n")
    
        
if __name__ == "__main__":
    uni = Universidad('UMU',30840,'Murcia')
    uni.add_asig('Matemáticas', 6)
    uni.add_asig('Física',4)
    #uni.add_asig('Matemáticas',8) # saldrá error por repetir una asignatura ya creada.
    uni.add_asig('Lengua',8)
    uni.add_asig('Historia',6)
    uni.mostrar_asignaturas()

    uni.add_prof_asoc('Ana Martínez','12345678A','Murcia','F',Departamento.DIIC)
    uni.asignar_asig_prof('Ana Martínez','Lengua')

    uni.add_prof_asoc('Juan Fernández','12121212B','Madrid','M',Departamento.DIS)
    uni.asignar_asig_prof('Juan Fernández','Física')
    uni.asignar_asig_prof('Juan Fernández','Matemáticas')

    uni.mostrar_asign_profesor('Juan Fernández')
    
    uni.add_prof_titular('Pepe Ruiz','90091234C','León','M','Área de Computadores',Departamento.DITEC)
    uni.asignar_asig_prof('Pepe Ruiz','Matemáticas')
    uni.asignar_asig_prof('Pepe Ruiz','Historia')
    
    uni.mostrar_profesores()

    uni.cambiar_dep('Pepe Ruiz',Departamento.DIIC)

    uni.mostrar_dep(Departamento.DIIC)

    uni.mostrar_investigadores()

    uni.mostrar_asignaturas()
    
    #uni.add_estudiante('Mar Soler', '571867890L', 'Valladolid', 'F') # tendrá un error de DNI por tener una longitud de 10, en vez de 9.

    uni.add_estudiante('Manuel Rodríguez', '87654321M', 'Valladolid', 'F')
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





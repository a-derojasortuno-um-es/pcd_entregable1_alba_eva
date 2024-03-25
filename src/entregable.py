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
    
    # def __str__(self):
    #     result = ""
    #     result = result + "Asignatura:" + self.nombre + "con" + str(self.creditos) + "créditos," + len(self.roles["estudiantes"])  + "estudiantes y que la imparten los siguientes profesores: "
    #     for i in self.roles["profesor"]:
    #         result += "\n" + "Profesor:" + i.nombre # ver si se pone todos los datos del profesor o solo el nombre.
    #     return result
            
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
        return self.devuelveDatos() +'\nArea de investigación: '+self.area+'\nDepartamento:'+str(self.miembro.departamento)+'\n'


class ProfesorTitular(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area_inv, departamento, listaAsig = []):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig
        self.rol_inv = Investigador(nombre, DNI ,direccion , sexo, area_inv, departamento)
        self.miembro  = Miembro_departamento(departamento)

    def add_asig(self,asig): # se implementará en la clase Universidad porque ahí estará la lista de asignaturas
        self.listaAsig.append(asig)

    def mostrar_asig(self):
        print(f"El profesor titular {self.nombre} imparte las siguientes asignaturas: ")
        for i in self.listaAsig: # sup que son objetos
           print(i,"\n") # se imprime el objeto Asignatura.

    def __str__(self):
        return self.devuelveDatos() + '\nDepartamento:'+str(self.miembro.departamento)+'\n'
       
            
class ProfesorAsociado(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, departamento, listaAsig = []):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig
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
        return self.devuelveDatos() + '\nDepartamento:'+str(self.miembro.departamento)


class Estudiante(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, listaAsig = []):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig
    
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

    # se va a diferenciar a la hora de asignar asignaturas a profesores entre su rol. --- nos ahorramos recorrer dos listas.
    # vale la pena?    
    
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
        self._lista_inves.append(prof_tit) # el profesor titular deberá estar, a su vez, en las dos listas. -- unificar variables.
    
    def add_prof_asoc(self,nombre,DNI,direccion,sexo,departamento):
        prof_asoc = ProfesorAsociado(nombre,DNI,direccion,sexo,departamento)
        self._lista_prof_asoc.append(prof_asoc)
    
    def add_investigador(self,nombre,DNI,direccion,sexo,area,departamento):
        invest = Investigador(nombre,DNI,direccion,sexo,area,departamento)
        self._lista_inves.append(invest)
    
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
                self._lista_prof_tit.remove(invest) # se elimina también de la lista de profesores titulares.
        except:
            raise NotFound('Error. Este investigador no se encuentra en la base de datos.')
        

    def cambiar_dep(self,nombre, dep):
        assert dep == Departamento.DIIC or dep == Departamento.DIS or dep == Departamento.DITEC , 'Nombre de departamento inválido.'
        try:
            p = self._buscaprofAsoc(nombre)
            if p != None:
                p.miembro.cambiar_dep(dep)
            else:
                pt = self._buscaprofTitular(nombre)
                if pt != None:
                    pt.miembro.cambiar_dep(dep)
                    inv = self._buscainvest(nombre) #todos los prof titulares son tmb investigadores
                    inv.miembro.cambiar_dep(dep)
                else:
                    i = self._buscainvest(nombre)
                    if self._buscainvest(nombre) != None: #investigadores q no son prof titulares
                        i.miembro.cambiar_dep(dep)
        except:
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
        if asig  not in est.listaAsig:
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
        
    def mostrar_lista_asig_est(self,estudiante): 
        est = self._buscaestud(estudiante)
        est.mostrar_asig()

    def mostrar_lista_asig_prof(self,profesor): 
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # signfica que profesor es un profesor titular.
                prof_titular.mostrar_asig()
        else: # es un profesor asociado
            prof_asoc.mostrar_asig()
    
    def mostrar_lista_asig_totales(self):
        print("La Universidad",self.nombre,"imparte las siguientes asignaturas: ")
        for i in self._lista_asig:
            print(i,"\n")
    
    def mostrar_lista_est_asig(self, nom_asig):
        a = uni._buscaasig(nom_asig)
        a.lista_estudiantes()

    def get_estudiantes(self):
        for est in self._lista_est:
            print(est)
    
    def get_prof_tit(self):
        for prof in self._lista_prof_tit:
            print(prof)
    
    def get_prof_asoc(self):
        for prof in self._lista_prof_asoc:
            print(prof)

    def get_inves(self):
        for i in self._lista_inves:
            print(i)
        
if __name__ == "__main__":
    uni = Universidad('UMU',30840,'Murcia')
    uni.add_asig('mates', 6)
    uni.add_asig('fisica',4)
    #uni.add_asig('mates',8)
    uni.add_asig('lengua',8)

    uni.add_prof_asoc('Ana','123456789','ygfadgu','F',Departamento.DIIC)
    uni.asignar_asig_prof('Ana','mates')
    
    pt = ProfesorTitular('Juan','162435678','hgvahgv','M','x',Departamento.DIIC)
    
    uni.add_estudiante('Mar', '571867890', 'fsgsh', 'F')
    uni.add_estudiante('Emma', '571867890', 'fsgsh', 'F')
    uni.add_estudiante('Sara', '571867890', 'fsgsh', 'F')


    uni.asignar_asig_est('Emma','mates')
    uni.asignar_asig_est('Mar','lengua')
    uni.mostrar_lista_asig_est('Emma')
    uni.mostrar_lista_est_asig('lengua')
    uni.mostrar_lista_est_asig('fisica')

    uni.del_asig_est('Emma','mates')
    #uni.asignar_asig_est('Eva','fisica')
    uni.mostrar_lista_est_asig('mates')

    uni.add_prof_asoc('pepe','123456789','bhsb','M',Departamento.DIIC)
    #uni.add_prof_asoc('jose','gsh','hsg','b',Departamento.DITEC)
    uni.add_prof_titular('rosa','896754145','bvsj','F','hhs',Departamento.DIS)
    uni.add_prof_titular('jose','871956432','hgca','M','bjwh',Departamento.DIIC)
    uni.cambiar_dep('rosa',Departamento.DITEC)
    
    #uni.get_prof_asoc()
    #uni.get_prof_tit()
    uni.mostrar_lista_asig_totales()
    uni.mostrar_lista_est_asig('lengua')



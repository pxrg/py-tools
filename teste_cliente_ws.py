#!usr/bin/env python
#-*- encoding:latin1-*-

# Required Suds
try:
    from suds.client import Client
except:
    print "Required suds: \n try pip install suds"
    exit(1)
    
from datetime import datetime

#from _main_teste_ import *

# especificar o endereco do wsdl
##wsdl_address = 'http://localhost:8080/Teste?wsdl'

soap = Client(wsdl_address)

print soap

def createSoapTypeClass(soap):
    """ Percorrendo os schemas do wsdl e armazenando suas estruturas """
    attr = {}
    for name in soap.factory.resolver.schema.types:
        attr[name[0]] = soap.factory.create(name[0])
    return attr

class MetaClassEcgSoap(type):
    """
        Criacao dos tipos utilizando meta classes
        Artigo muito bom sobre o assunto:
        http://www.tocadoelfo.com.br/2011/08/metaclasses-em-python.html
    """
    def __new__(self, nomeDaClasse, classesPai, atributosDaClasse):
        soap = Client(wsdl_address)
        new_attr = {}
        for _class, _obj in createSoapTypeClass(soap).items():
            aux = {}
            for e in _obj.__keylist__:
                aux[e] = _obj.__getitem__(e)
            new_attr[_class] = type(str(_class), (), aux)
        return super(MetaClassEcgSoap, self).__new__(self, nomeDaClasse, classesPai, new_attr)
        

class FactoryServer(object):
    __metaclass__ = MetaClassEcgSoap
    pass

#Utilizando....
# classe = FactoryServer.nome_da_classe()
    

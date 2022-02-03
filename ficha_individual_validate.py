import xmlschema
import json
from xml.etree.ElementTree import ElementTree

my_schema = xmlschema.XMLSchema('XSD/dadotransporte.xsd')


is_valid = my_schema.is_valid('xml_examples/Atendimento_individual.esus.xml')


print(f"Schema válido: {is_valid}")

if not is_valid:
    print(f"Erros de validação do Schema \n")
    print(my_schema.validate('xml_examples/Cadastro_Domiciliar.esus.xml'))


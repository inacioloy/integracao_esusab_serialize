import xmlschema
import json
from xml.etree.ElementTree import ElementTree

# Medicamento
schema = xmlschema.XMLSchema('XSD/medicamento.xsd')
xml = "xml_examples/Atendimento_individual.esus.xml"


is_valid = schema.is_valid(xml)
print(f"Schema válido: {is_valid}")

if not is_valid:
    print(f"Erros de validação do Schema \n")
    print(schema.validate('xml_examples/Atendimento_individual.esus.xml'))


#Exportando para arquivo XML
# ElementTree(xml).write('D:\workspace\Inacio_Labs\inaciolabs\my_xml.esus.xml')


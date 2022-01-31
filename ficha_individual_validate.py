import xmlschema
import json
from xml.etree.ElementTree import ElementTree

my_schema = xmlschema.XMLSchema('XSD/fichaatendimentoindividualmaster.xsd')
# my_schema = xmlschema.XMLSchema('https://github.com/laboratoriobridge/esusab-integracao/blob/0c16a48ebda2ae65ccc0bbdca506f3ad5e2ea6c1/XSD/fichaatendimentoindividualmaster.xsd')


is_valid = my_schema.is_valid('xml_examples/Atendimento_individual.esus.xml')


print(f"Schema válido: {is_valid}")

if not is_valid:
    print(f"Erros de validação do Schema \n")
    print(my_schema.validate('xml_examples/Atendimento_individual.esus.xml'))


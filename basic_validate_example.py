import xmlschema
import json
from xml.etree.ElementTree import ElementTree

#Exemplo de um schema XSD básico
my_xsd = '<?xml version="1.0"?> <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"> <xs:element name="note" type="xs:string"/> </xs:schema>'

#Instancia schema
schema = xmlschema.XMLSchema(my_xsd)

#1 - Validando XML em schema XSD
my_xml = '<note>Teste</note>'

#Validando XML
my_xml_is_valid = schema.is_valid(my_xml)
print(f"XML válido: {my_xml_is_valid}")


#2 - Serializando a partir de um JSON
json_data = json.dumps({"note": "teste"})

#Convertendo JSON para XML baseado no schema a partir de JSON
xml_from_json = xmlschema.from_json(json_data, schema=schema, preserve_root=True)

#Validando XML gerado a partir do JSON
my_xml_is_valid = schema.is_valid(xml_from_json)
print(f"XML válido: {my_xml_is_valid}")

#Exportando para arquivo XML
# ElementTree(xml).write('D:\workspace\Inacio_Labs\inaciolabs\my_xml.esus.xml')
print("FIM!")
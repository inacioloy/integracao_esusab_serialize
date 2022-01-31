import xmlschema
import json
from xml.etree.ElementTree import ElementTree

# Medicamento
schema = xmlschema.XMLSchema('XSD/medicamento.xsd')

xml = '''
            <medicamentos>
                <codigoCatmat>BR0387985</codigoCatmat>
                <viaAdministracao>11</viaAdministracao>
                <dose>1 aplicação</dose>
                <doseUnica>false</doseUnica>
                <usoContinuo>false</usoContinuo>
                <doseFrequenciaTipo>1</doseFrequenciaTipo>
                <doseFrequencia>manhã</doseFrequencia>
                <doseFrequenciaQuantidade>2</doseFrequenciaQuantidade>
                <doseFrequenciaUnidadeMedida>3</doseFrequenciaUnidadeMedida>
                <dtInicioTratamento>1586095200000</dtInicioTratamento>
                <duracaoTratamento>12</duracaoTratamento>
                <duracaoTratamentoMedida>3</duracaoTratamentoMedida>
                <quantidadeReceitada>12</quantidadeReceitada>
            </medicamentos>
'''




#Gerando XML e validando a partir do JSON
# data = json.dumps({"codigoCatmat": "teste",
#                    "viaAdministracao": "0",
#                    "dose": "1 comprimido",
#                    "doseUnica": "false",
#                    "usoContinuo": "true",
#                    "doseFrequenciaTipo": "2",
#                    "doseFrequencia": "3",
#                    "doseFrequenciaQuantidade": "1",
#                    "doseFrequenciaUnidadeMedida": "1",
#                    "dtInicioTratamento": "1586095200000",
#                    "duracaoTratamento": "7",
#                    "duracaoTratamentoMedida": "1",
#                    "quantidadeReceitada": "8"
#                    })


#Convertendo JSON para XML baseado no schema a partir de JSON
# xml = xmlschema.from_json(data, schema=schema, preserve_root=True)

#Validando XML

is_valid = schema.is_valid(xml)
print(f"Schema válido: {is_valid}")

if not is_valid:
    print(f"Erros de validação do Schema \n")
    print(schema.validate('xml_examples/Atendimento_individual.esus.xml'))


#Exportando para arquivo XML
# ElementTree(xml).write('D:\workspace\Inacio_Labs\inaciolabs\my_xml.esus.xml')


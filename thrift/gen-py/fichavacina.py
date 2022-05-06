import time
import uuid
from io import BytesIO
from zipfile import ZipFile

from br.gov.saude.esusab.ras.vacinacao.ttypes import FichaVacinacaoMasterThrift, FichaVacinacaoChildThrift, VacinaRowThrift
from br.gov.saude.esusab.ras.common.ttypes import UnicaLotacaoHeaderThrift
from br.gov.saude.esusab.dadotransp.ttypes import DadoTransporteThrift, DadoInstalacaoThrift, VersaoThrift
from serializador import Serializador


class ExemploFichaVacina:
    EXTENSAO_EXPORT = ".esus"
    TIPO_DADO_SERIALIZADO_FICHA_PROCEDIMENTO = 14

    def __init__(self):
        thrift_ficha_vacina = self._get_ficha()
        dado_transporte = self._get_dado_transporte(thrift_ficha_vacina)
        serializador = Serializador()
        dado_transporte.tipoDadoSerializado = self.TIPO_DADO_SERIALIZADO_FICHA_PROCEDIMENTO
        dado_transporte.dadoSerializado = serializador.serializar(thrift_ficha_vacina)
        dado_transporte.versao = VersaoThrift(3, 2, 3)
        self.dado_transporte = dado_transporte

    def gerar_arquivo(self):
        try:
            arquivo = BytesIO()
            with ZipFile(arquivo, 'w') as zip_archive:
                # Create three files on zip archive
                entryName = self.dado_transporte.uuidDadoSerializado + self.EXTENSAO_EXPORT
                serializador = Serializador()
                dado_transporte_serializado = serializador.serializar(self.dado_transporte)

                with zip_archive.open(entryName, 'w') as file1:
                    file1.write(dado_transporte_serializado)

            with open('exemploThrift.zip', 'wb') as f:
                f.write(arquivo.getvalue())

            arquivo.close()
        except Exception as e:
            print(e)

    def _get_dado_transporte(self, ficha):
        remetente = DadoInstalacaoThrift(
            contraChave='123456',
            uuidInstalacao='UUIDUNICO111',
            cpfOuCnpj='11111111111',
            nomeOuRazaoSocial='Nome ou Razao Social Remetente',
            fone='999999999',
            email='a@b.com'
        )
        originadora = DadoInstalacaoThrift(
            contraChave='789010',
            uuidInstalacao='UUIDUNICO222',
            cpfOuCnpj='11111111111',
            nomeOuRazaoSocial='Nome ou Razao Social Originadora',
            fone='98888888',
            email='b@a.com'
        )
        return DadoTransporteThrift(
            uuidDadoSerializado=ficha.uuidFicha,
            cnesDadoSerializado=ficha.headerTransport.cnes,
            codIbge=ficha.headerTransport.codigoIbgeMunicipio,
            ineDadoSerializado=ficha.headerTransport.ine,
            numLote=123123,
            remetente=remetente,
            originadora=originadora,
        )

    def _get_ficha(self):
        uuid_ficha = str(uuid.uuid4())
        return FichaVacinacaoMasterThrift(
            uuidFicha=uuid_ficha,
            tpCdsOrigem=3,
            headerTransport=self._get_header(),
            vacinacoes=self._get_vacinacoes(),
        )

    def _get_header(self):
        return UnicaLotacaoHeaderThrift(
            profissionalCNS='898001160660761',
            cboCodigo_2002='223212',
            cnes='7381123',
            # Opcional ine='0000406465',
            dataAtendimento=round(time.time() * 1000),
            codigoIbgeMunicipio='4205407'
        )

    def _get_vacinacoes(self):
        vacinacoes = []

        vacina = FichaVacinacaoChildThrift(
            turno=1,
            #Opcional numProntuario='41413'
            #Não pode preencher se cpf for preenchido cnsCidadao=,
            dtNascimento=round(time.time() * 1000),
            sexo=1,
            localAtendimento=1,
            viajante=False,
            #Obrigatório se vacina é BCG comunicanteHanseniase
            gestante=False,
            puerpera=False,
            vacinas=self._get_vacinas(),
            dataHoraInicialAtendimento=round(time.time() * 1000),
            dataHoraFinalAtendimento=round(time.time() * 1000),
            cpfCidadao='80487483391',
        )

        vacinacoes.append(vacina)
        return vacinacoes

    def _get_vacinas(self):
        vacinas = []
        vacina = VacinaRowThrift(
            imunobiologico=28,
            estrategiaVacinacao=1,
            dose=1,
            lote='3571',
            fabricante='Fabricante',
            #Condicional grupoAtendimento=,
            stRegistroAnterior=False,
            #Condicional dataRegistroAnterior,
            #Condicional stAplicadoExterior,
        )
        vacinas.append(vacina)
        vacina = VacinaRowThrift(
            imunobiologico=65,
            estrategiaVacinacao=1,
            dose=1,
            lote='3572',
            fabricante='Fabricante 2',
            #Condicional grupoAtendimento=,
            stRegistroAnterior=False,
            #Condicional dataRegistroAnterior,
            #Condicional stAplicadoExterior,
        )
        vacinas.append(vacina)
        return vacinas

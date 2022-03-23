import time
import uuid
from io import BytesIO
from zipfile import ZipFile

from br.gov.saude.esusab.ras.atendprocedimentos.ttypes import FichaProcedimentoMasterThrift, FichaProcedimentoChildThrift
from br.gov.saude.esusab.ras.common.ttypes import UnicaLotacaoHeaderThrift
from br.gov.saude.esusab.dadotransp.ttypes import DadoTransporteThrift, DadoInstalacaoThrift, VersaoThrift
from serializador import Serializador


class ExemploFichaProcedimento:
    EXTENSAO_EXPORT = ".esus"
    TIPO_DADO_SERIALIZADO_FICHA_PROCEDIMENTO = 7

    def __init__(self):
        thrift_ficha_procedimento = self._get_ficha()
        dado_transporte = self._get_dado_transporte(thrift_ficha_procedimento)
        serializador = Serializador()
        dado_transporte.tipoDadoSerializado = self.TIPO_DADO_SERIALIZADO_FICHA_PROCEDIMENTO
        dado_transporte.dadoSerializado = serializador.serializar(thrift_ficha_procedimento)
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
        return FichaProcedimentoMasterThrift(
            uuidFicha=uuid_ficha,
            tpCdsOrigem=3,
            headerTransport=self._get_header(),
            atendProcedimentos=self._get_atendimentos(),
            numTotalAfericaoPa=1,
            numTotalAfericaoTemperatura=1,
            numTotalColetaMaterialParaExameLaboratorial=1,
            numTotalCurativoSimples=1,
            numTotalGlicemiaCapilar=1,
            numTotalMedicaoAltura=1,
            numTotalMedicaoPeso=1
        )

    def _get_header(self):
        return UnicaLotacaoHeaderThrift(
            profissionalCNS='898001160660761',
            cboCodigo_2002='223212',
            cnes='7381123',
            ine='0000406465',
            dataAtendimento=round(time.time() * 1000),
            codigoIbgeMunicipio='4205407'
        )

    def _get_atendimentos(self):
        procedimentos_atendimento = []

        for i in range(3):
            procedimentos = self._get_procedimentos_sia() + self._get_procedimentos()
            procedimento_atendimento = FichaProcedimentoChildThrift(
                numProntuario='43143',
                dtNascimento=round(time.time() * 1000),
                sexo=1,
                localAtendimento=1,
                turno=1,
                procedimentos=procedimentos,
                cpfCidadao='80487483391'
            )
            procedimentos_atendimento.append(procedimento_atendimento)

        return procedimentos_atendimento

    def _get_procedimentos_sia(self):
        sia = []
        sia.append("ABEX010")  # MAMOGRAFIA BILATERAL
        sia.append("ABEX007")  # HDL
        sia.append("ABEX009")  # LDL
        return sia

    def _get_procedimentos(self):
        procedimentos = []
        procedimentos.append("ABPG019")  # SUTURA SIMPLES
        procedimentos.append("ABEX004")  # ELETROCARDIOGRAMA
        return procedimentos

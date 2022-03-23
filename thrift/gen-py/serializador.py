from thrift.Thrift import TException
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport


class Serializador:

    def serializar(self, ficha_thrift):
        try:
            transport = TTransport.TMemoryBuffer()
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            ficha_thrift.write(protocol)
            return transport.getvalue()
        except TException as e:
            print(e)

        return None

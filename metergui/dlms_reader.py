from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_dlms.enums import InterfaceType
from gurux_dlms.GXDLMSReader import GXDLMSReader
from gurux_common.enums import TraceLevel
from gurux_serial.GXSerial import GXSerial
import datetime

def read_dlms_meter(settings):
    try:
        port = settings['comPortName']
        baud = settings['baudRate']
        stop_bits = int(settings['stopBits'])
        parity = settings['parity']
        client_address = settings['clientAddress']
        server_address = settings['serverAddress']
        client = GXDLMSClient(
            useLogicalNameReferencing=True,
            clientAddress=client_address,
            serverAddress=server_address,
            interfaceType=InterfaceType.HDLC
        )

        connection = GXSerial()
        connection.port = port
        connection.baudRate = baud
        connection.dataBits = 8
        connection.stopBits = stop_bits
        connection.parity = parity.upper()
        connection.open()

        reader = GXDLMSReader(connection, client, TraceLevel.INFO)

        reader.initializeConnection()

        result = {}
        result["energy"] = reader.readValue("1.0.1.8.0")
        result["voltage"] = reader.readValue("1.0.32.7.0")
        result["current"] = reader.readValue("1.0.31.7.0")

        reader.close()

        return result

    except Exception as e:
        return {"error": str(e)}

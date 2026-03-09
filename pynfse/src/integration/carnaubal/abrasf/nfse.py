

from pathlib import Path
from pynfse.src.common.api import NFSeBase
from pynfse.src.common.xml import XMLBase
from pynfse.schemas.nfse import InfoRPS
from pynfse.schemas.lote import LoteRps



#
#
#https://notanacional.speedgov.com.br/

class CarnaubalNFSe(NFSeBase):

    def get_xml_base(self) -> XMLBase:
        return XMLBase(templates=self.get_templates(__file__))
    
    def create_rps_nfse(self, rps: InfoRPS, lote: LoteRps = None) -> str:
        """
        Cria XML de RPS usando estrutura LoteRps conforme NFS-e Nacional.
        
        Se lote não for fornecido, cria um lote automático com um único RPS.
        """
        xml_base = self.get_xml_base()
        
        if lote is None:
            # Cria lote automático com um único RPS
            lote = LoteRps(
                numero_lote=1,
                cnpj=rps.provider.cnpj,
                inscricao_municipal=str(rps.provider.municipal_registration),
                quantidade_rps=1,
                lista_rps=[rps],
                id=f"lote_{rps.identification.number}"
            )
        
        return xml_base.create_rps_nfse(rps=rps, lote=lote)
    
    def create_cancel_nfse(self, nfse) -> str:
        """Cria XML para cancelamento de NFSE."""
        xml_base = self.get_xml_base()
        return xml_base.create_cancel_nfse(nfse)
    
    def create_consult_nfse(self, nfse) -> str:
        """Cria XML para consulta de NFSE."""
        xml_base = self.get_xml_base()
        return xml_base.create_consult_nfse(nfse)
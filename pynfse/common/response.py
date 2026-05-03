from httpx import Response


class ResponseNFSE:
    def __init__(self, xml: str, response: Response):

        self.xml = xml
        self.response = response

    def get_status_code(self)->int:
        return self.response.status_code

    def get_json(self)->dict:
        try:
            return self.response.json() 
        except Exception as e:
            return {}
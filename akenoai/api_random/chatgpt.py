import requests  # type: ignore


class ApiRandom:
    def __init__(self):
        self.loveyou = "https://akmoviedl.vercel.app"

    def _iloveyou(self, method=None):
        return f"{self.loveyou}/api/{method}"

    async def _chatgpt(self, **payload):
        """
        payload: userPrompt
        example:
        from akenoai.api_random import ApiRandom

        api = ApiRandom()
        get_response_json = await api._chatgpt(userPrompt="hello world")
        print(get_response_json)
        """
        headers = {
            "Content-Type": "application/json"
        }
        url = self._iloveyou("chessgpt")
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )
            return response.json()
        except Exception:
            raise Exception("Error connecting")

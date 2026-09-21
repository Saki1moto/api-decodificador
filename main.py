from fastapi import FastAPI
from pydantic import BaseModel
from googlenewsdecoder import gnewsdecoder

app = FastAPI()

# Estrutura do dado que vamos receber da planilha
class LinkRequest(BaseModel):
    url: str

@app.post("/decode")
def decode_link(request: LinkRequest):
    try:
        # Usa a sua biblioteca para decodificar
        resultado = gnewsdecoder(request.url, interval=1)
        
        if resultado.get("status"):
            return {"success": True, "decoded_url": resultado["decoded_url"]}
        else:
            return {"success": False, "error": resultado.get("message")}
    except Exception as e:
        return {"success": False, "error": str(e)}

from fastapi import FastAPI
from pydantic import BaseModel
from googlenewsdecoder import gnewsdecoder
import time

app = FastAPI()

class BatchLinkRequest(BaseModel):
    urls: list[str]

@app.post("/decode-batch")
def decode_batch(request: BatchLinkRequest):
    results = []
    for url in request.urls:
        if not url or url.strip() == "":
            results.append("")
            continue
            
        url_limpa = url.replace("'", "").replace('"', '').strip()
        try:
            res = gnewsdecoder(url_limpa, interval=1)
            if res.get("status"):
                results.append(res["decoded_url"])
            else:
                results.append(f"Erro: {res.get('message')}")
        except Exception as e:
            results.append(f"Erro: {str(e)}")
            
        time.sleep(0.5)
        
    return {"success": True, "decoded_urls": results}

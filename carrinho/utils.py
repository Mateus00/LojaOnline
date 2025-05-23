# carrinho/utils.py
import qrcode
from io import BytesIO
import base64

def gerar_payload_pix(chave, nome_recebedor, cidade, valor, info_adicional='Pedido via loja virtual'):
    payload = f"""000201
26440014BR.GOV.BCB.PIX
01{len(chave):02d}{chave}
52040000
5303986
540{len(f'{valor:.2f}'):02d}{valor:.2f}
5802BR
5913{nome_recebedor[:13]}
6009{cidade[:9]}
62070503***"""
    payload = payload.replace("\n", "")  # remove quebras de linha

    return payload


def gerar_qr_code_base64(payload):
    qr = qrcode.make(payload)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

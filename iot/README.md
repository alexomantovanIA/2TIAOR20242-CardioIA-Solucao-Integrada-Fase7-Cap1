# CardioIA IoT - Wokwi

Projeto MicroPython para simular o fluxo da Fase 7:

Sensor simulado -> ESP32/MicroPython -> Backend Python `/api/iot/ingest` -> IA -> Web/Mobile.

## Como rodar no Wokwi

1. Crie um novo projeto ESP32 MicroPython no Wokwi.
2. Copie `main.py` e `diagram.json` deste diretorio para o projeto.
3. Execute a simulacao.
4. Observe o console com `heart_rate`, `temperature`, `spo2` e `status`.
5. Observe o LED RGB:
   - Verde: normal.
   - Amarelo: atencao.
   - Vermelho: critico.

## Envio opcional ao backend

Preencha no topo de `main.py`:

```python
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
API_URL = "http://SEU_IP_LOCAL:5000/api/iot/ingest"
```

No Wokwi, use `Wokwi-GUEST` sem senha. Para backend local, use o IP da maquina na rede, nao `localhost`.

## Link Wokwi

Preencher apos publicar:

- https://wokwi.com/projects/SEU_PROJETO

## Prints esperados

- Console com leituras simuladas e status.
- LED verde para leituras normais.
- LED amarelo para status de atencao.
- LED vermelho para status critico.

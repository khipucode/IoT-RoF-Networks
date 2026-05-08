# Resumo dos scripts Python gerados para configuração e teste dos módulos XBee S2C

Este documento resume os arquivos `.py` criados durante a configuração e teste de dois módulos **XBee S2C** em modo ponto a ponto.

## Configuração geral usada

| Item | Valor |
|---|---|
| Coordinator | `/dev/ttyUSB0` |
| Router | `/dev/ttyUSB1` |
| Baud rate | `57600 bps` |
| API mode | `AP = 1` |
| PAN ID | `1234` |
| Canal final | `CH = 0C` |
| Coordinator address | `0013A20041839DB1` |
| Router address | `0013A20041839DCA` |

---

# 1. `configurar_coordinator.py`

## Função

Configura o módulo conectado em `/dev/ttyUSB0` como **Coordinator**.

## Principais parâmetros configurados

```text
CE = 01
AP = 01
ID = 1234
SC = 0200
BD = 06
NI = COORDINATOR
```

## Observação

O comando `JV` não foi usado porque o firmware retornou:

```text
Invalid command
```

---

# 2. `configurar_router.py`

## Função

Configura o módulo conectado em `/dev/ttyUSB1` como **Router**.

## Principais parâmetros configurados

```text
CE = 00
AP = 01
ID = 1234
SC = 0200
BD = 06
SM = 00
NI = ROUTER
```

## Observação

A primeira versão do script usava `JV = 1`, mas o firmware do módulo não aceita esse comando. Por isso, a versão final removeu o parâmetro `JV`.

---

# 3. `diagnosticar_router.py`

## Função

Lê os principais parâmetros do Router em `/dev/ttyUSB1`.

## Parâmetros verificados

```text
VR
HV
AP
BD
ID
SC
CE
SM
JV
NI
SH
SL
DH
DL
```

## Resultado importante obtido

```text
VR = 2003
AP = 01
BD = 00000006
ID = 1234
SC = 0200
CE = 00
SM = 00
NI = Sink 2
SH = 0013A200
SL = 41839DCA
```

Endereço completo do Router:

```text
0013A20041839DCA
```

---

# 4. `diagnosticar_coordinator.py`

## Função

Lê os principais parâmetros do Coordinator em `/dev/ttyUSB0`.

## Parâmetros verificados

```text
VR
HV
AP
BD
ID
SC
CE
SM
JV
NI
SH
SL
DH
DL
```

## Resultado importante obtido

```text
VR = 2003
AP = 01
BD = 00000006
ID = 1234
SC = 0200
CE = 01
SM = 00
NI = COORDINATOR
SH = 0013A200
SL = 41839DB1
```

Endereço completo do Coordinator:

```text
0013A20041839DB1
```

---

# 5. `configurar_destinos_ponto_a_ponto.py`

## Função

Configura os endereços de destino entre os dois módulos.

## Configuração aplicada

No Coordinator:

```text
DH = 0013A200
DL = 41839DCA
```

No Router:

```text
DH = 0013A200
DL = 41839DB1
```

## Objetivo

Fazer com que:

```text
Coordinator -> Router
Router      -> Coordinator
```

---

# 6. `listar_parametros.py`

## Função

Lista os principais parâmetros dos dois módulos.

## Módulos lidos

```text
/dev/ttyUSB0 -> Coordinator
/dev/ttyUSB1 -> Router
```

## Parâmetros listados

```text
CE
AP
ID
SC
BD
SM
JV
NI
SH
SL
DH
DL
```

## Uso

Serve para verificar rapidamente se os módulos continuam configurados corretamente.

---

# 7. `verificar_rede.py`

## Função

Verifica o estado da rede e associação dos módulos.

## Parâmetros verificados

```text
AI
OP
OI
CH
ID
SC
CE
AP
BD
SH
SL
DH
DL
```

## Resultado final obtido

Coordinator:

```text
AI = 00
CH = 0C
ID = 1234
SC = 0200
CE = 01
AP = 01
BD = 00000006
SH = 0013A200
SL = 41839DB1
DH = 0013A200
DL = 41839DCA
```

Router:

```text
AI = 00
CH = 0C
ID = 1234
SC = 0200
CE = 00
AP = 01
BD = 00000006
SH = 0013A200
SL = 41839DCA
DH = 0013A200
DL = 41839DB1
```

## Diagnóstico importante

Inicialmente os módulos estavam em canais diferentes:

```text
Coordinator CH = 0C
Router CH = 0D
```

Depois foi corrigido para:

```text
Coordinator CH = 0C
Router CH = 0C
```

---

# 8. `resetar_xbees.py`

## Função

Reinicia os dois módulos via comando AT `FR`.

## Ordem usada

```text
1. Resetar Coordinator
2. Esperar alguns segundos
3. Resetar Router
```

## Objetivo

Forçar a reformação/reassociação da rede após mudanças de parâmetros.

---

# 9. `forcar_canal_0C.py`

## Função

Força os dois módulos a trabalharem no mesmo canal operacional:

```text
CH = 0C
```

## Problema resolvido

Antes da execução, os módulos estavam em canais diferentes:

```text
Coordinator CH = 0C
Router CH = 0D
```

Depois da execução:

```text
Coordinator CH = 0C
Router CH = 0C
```

Esse foi um passo essencial para estabilizar o link.

---

# 10. `receptor_api_router.py`

## Função

Abre o Router em `/dev/ttyUSB1` como receptor em modo API.

## Configuração

```text
PORT = /dev/ttyUSB1
BAUD_RATE = 57600
```

## Saída esperada

```text
Abrindo Router em /dev/ttyUSB1...
Endereço local deste módulo:
0013A20041839DCA

Router escutando...
```

## Resultado obtido

Recebeu corretamente pacotes do Coordinator:

```text
Recebido de 0013A20041839DCA: Unicast 0 do Coordinator
Recebido de 0013A20041839DCA: Unicast 1 do Coordinator
Recebido de 0013A20041839DCA: Unicast 2 do Coordinator
```

## Observação

O receptor mostrou o endereço local do próprio Router como origem. Apesar disso, os pacotes chegaram corretamente.

---

# 11. `transmissor_api_coordinator.py`

## Função

Envia pacotes do Coordinator para o Router usando endereço fixo.

## Configuração

```text
PORT = /dev/ttyUSB0
BAUD_RATE = 57600
ROUTER_64BIT_ADDR = 0013A20041839DCA
```

## Problema encontrado

Este script inicialmente falhou com:

```text
There was a problem with a transmitted packet response (status not ok)
```

## Conclusão

O envio usando endereço criado manualmente apresentou problema. Depois foi substituído por um teste usando descoberta automática de nós.

---

# 12. `receptor_api_coordinator.py`

## Função

Abre o Coordinator em `/dev/ttyUSB0` como receptor em modo API.

## Configuração

```text
PORT = /dev/ttyUSB0
BAUD_RATE = 57600
```

## Uso

Serve para testar o sentido inverso:

```text
Router -> Coordinator
```

---

# 13. `transmissor_api_router.py`

## Função

Envia pacotes do Router para o Coordinator.

## Configuração

```text
PORT = /dev/ttyUSB1
BAUD_RATE = 57600
COORDINATOR_64BIT_ADDR = 0013A20041839DB1
```

## Uso

Serve para testar o sentido:

```text
Router -> Coordinator
```

---

# 14. `transmissor_broadcast_coordinator.py`

## Função

Envia pacotes broadcast a partir do Coordinator.

## Configuração

```text
PORT = /dev/ttyUSB0
BAUD_RATE = 57600
```

## Resultado obtido

O broadcast funcionou corretamente.

Transmissor:

```text
Enviado: Broadcast 0 do Coordinator
Enviado: Broadcast 1 do Coordinator
Enviado: Broadcast 2 do Coordinator
```

Receptor:

```text
Recebido de 0013A20041839DCA: Broadcast 0 do Coordinator
Recebido de 0013A20041839DCA: Broadcast 1 do Coordinator
Recebido de 0013A20041839DCA: Broadcast 2 do Coordinator
```

## Conclusão

O link RF estava funcionando. O problema estava apenas no envio unicast manual.

---

# 15. `descobrir_nos_coordinator.py`

## Função

Executa descoberta de nós a partir do Coordinator.

## Resultado obtido

```text
Endereço local do Coordinator:
0013A20041839DB1

Nós encontrados:
64-bit: 0013A20041839DCA
16-bit: 0000
NI: ROUTER
```

## Conclusão

O Coordinator conseguiu descobrir corretamente o Router.

---

# 16. `transmissor_unicast_descoberto.py`

## Função

Faz descoberta automática de nós e envia pacotes unicast para o Router encontrado.

## Configuração

```text
PORT = /dev/ttyUSB0
BAUD_RATE = 57600
```

## Funcionamento

1. Abre o Coordinator.
2. Executa descoberta de nós.
3. Encontra o Router pelo endereço ou pelo `NI`.
4. Envia pacotes usando o objeto remoto descoberto pela biblioteca.

## Resultado obtido

Transmissor:

```text
Nó encontrado: 0013A20041839DCA | NI=ROUTER

Router selecionado:
0013A20041839DCA

Enviado com sucesso: Unicast 0 do Coordinator
Enviado com sucesso: Unicast 1 do Coordinator
Enviado com sucesso: Unicast 2 do Coordinator
```

Receptor:

```text
Recebido de 0013A20041839DCA: Unicast 0 do Coordinator
Recebido de 0013A20041839DCA: Unicast 1 do Coordinator
Recebido de 0013A20041839DCA: Unicast 2 do Coordinator
```

## Conclusão

Este foi o script que confirmou o funcionamento do unicast.

---

# Estado final do sistema

O link ponto a ponto está funcionando no sentido:

```text
Coordinator -> Router
```

Configuração final:

```text
Coordinator:
PORT = /dev/ttyUSB0
Address = 0013A20041839DB1
CE = 01
AP = 01
BD = 06
ID = 1234
CH = 0C
DH/DL = 0013A20041839DCA

Router:
PORT = /dev/ttyUSB1
Address = 0013A20041839DCA
CE = 00
AP = 01
BD = 06
ID = 1234
CH = 0C
DH/DL = 0013A20041839DB1
```

---

# Scripts mais importantes para continuar usando

Para diagnóstico:

```text
verificar_rede.py
diagnosticar_coordinator.py
diagnosticar_router.py
```

Para corrigir canal:

```text
forcar_canal_0C.py
```

Para descobrir nós:

```text
descobrir_nos_coordinator.py
```

Para teste funcional recomendado:

```text
receptor_api_router.py
transmissor_unicast_descoberto.py
```

Para teste broadcast:

```text
transmissor_broadcast_coordinator.py
receptor_api_router.py
```

---

# Próximos passos recomendados

1. Testar o sentido inverso:

```text
Router -> Coordinator
```

usando:

```text
receptor_api_coordinator.py
transmissor_api_router.py
```

2. Criar um script de teste de PDR com:
   - contador de pacotes;
   - timestamp;
   - intervalo configurável;
   - payload configurável;
   - arquivo `.csv`.

3. Criar um receptor que salve:
   - número do pacote;
   - tempo de chegada;
   - endereço do nó;
   - payload recebido;
   - RSSI, se disponível.

4. Usar estes scripts como base para experimentos com RoF/IoT.

---

# Lista de arquivos Python citados

```text
configurar_coordinator.py
configurar_router.py
diagnosticar_router.py
diagnosticar_coordinator.py
configurar_destinos_ponto_a_ponto.py
listar_parametros.py
verificar_rede.py
resetar_xbees.py
forcar_canal_0C.py
receptor_api_router.py
transmissor_api_coordinator.py
receptor_api_coordinator.py
transmissor_api_router.py
transmissor_broadcast_coordinator.py
descobrir_nos_coordinator.py
transmissor_unicast_descoberto.py
```

# Diagnosi VETRO27-PC e GPO RDP dedicata — 5 novembre 2026

Raccolta documentale del **6 novembre 2026**, su attività svolte il **5 novembre 2026**.
Le verifiche descritte risalgono al 05/11/2026 (ultimo test TCP intorno alle **15:00**) e **non descrivono lo stato attuale**.

## 1. Identità del computer

| Elemento | Valore | Fonte |
|---|---|---|
| Computer | `VETRO27-PC` | output operativo 05/11/2026 |
| FQDN | `VETRO27-PC.Vetrodom.local` | idem |
| IP risolto durante il test del 05/11/2026 | `192.168.24.111` | idem — **non statico né riconfermato al 06/11** |
| Account computer | `VETRO27-PC$` | idem |
| SID | `S-1-5-21-2102961270-20425018-2847913122-1254` | idem |
| Percorso AD | `CN=VETRO27-PC,OU=Computer,OU=Vetronaviglio,DC=Vetrodom,DC=local` | `Inventario-Nable-Utenti-20261104-152954.csv` |

## 2. Operazioni eseguite durante la diagnosi (05/11/2026)

| Operazione | Esito |
|---|---|
| Accesso SMB amministrativo | verificato |
| Avvio del servizio `TermService` | eseguito durante la diagnosi |
| Servizio `RemoteRegistry` | ripristinato a **fermo** e **disabilitato** al termine delle verifiche |
| Test TCP porta RDP 3389 (ultimo, ~15:00 del 05/11) | `TcpTestSucceeded = False` |
| Modifiche a firewall | **nessuna** |
| Modifiche a NLA | **nessuna** |
| Riavvio del computer | **nessuno** come parte di questi passaggi |

La mancata raggiungibilità di RDP **non dimostra da sola** che il firewall ne sia la causa.

## 3. GPO dedicata

| Campo | Valore |
|---|---|
| Nome | `CMP - RDP - Solo VETRO27-PC` |
| GUID | `cf7918f0-92e4-4854-bcd8-79396dc9440a` |
| Collegamento | `OU=Computer,OU=Vetronaviglio,DC=Vetrodom,DC=local` |
| Collegamento abilitato | sì |
| Impostazione | `fDenyTSConnections = 0` |
| Filtro di applicazione | `VETRO27-PC$` con `GpoApply` |
| `Authenticated Users` | `GpoRead`, non `GpoApply` |
| `Domain Admins`, `Enterprise Admins`, `SYSTEM` | `GpoEditDeleteModifySecurity` |
| Controller di dominio dell'organizzazione (SID `S-1-5-9`) | `GpoRead` |
| Firewall / NLA | non modificati |

Fonte: output operativo su DC01 (05/11/2026). Percorso del report indicato dall'output: `C:\Users\administrator.VETRODOM\Desktop\GPO-RDP-VETRO27-20261105-145820` — **riferimento a file esterno**, non presumere che sia disponibile localmente.

**Stato da mantenere:** GPO **creata e collegata**; **applicazione effettiva sul client non ancora verificata**.

## 4. Cronologia e ruoto del file di diagnosi

| Data/ora | Evento |
|---|---|
| 05/11/2026 14:41 | timestamp di modifica di `Diagnosi-RDP-VETRO27.csv` sulla condivisione (riferimento esterno, non portabile) |
| 05/11/2026 ~14:58 | creazione della GPO `CMP - RDP - Solo VETRO27-PC` |

Il file di diagnosi contiene 8 oggetti GPO distinti (32 righe, 4 per GPO) e in nessuna riga un valore per `fDenyTSConnections`. **Il file non riporta un'intestazione che identifichi il computer oggetto né se rappresenti criteri applicati al client oppure configurazioni/link individuati**: il metodo di raccolta **non è determinabile dal file**.

Poiché il file è **precedente** alla creazione della GPO, la sua assenza **non costituisce evidenza** di mancata applicazione: è una fotografia di un momento precedente. Lo stato applicativo resta **non verificato**.

## 5. Tentativo di refresh remoto

Comando tentato il 05/11/2026:

```
Invoke-GPUpdate -Computer VETRO27-PC.Vetrodom.local -Target Computer -Force -RandomDelayInMinutes 0
```

Esito: **richiesta non riuscita** — il computer non risponde oppure le regole firewall di Gestione remota attività pianificate non consentono l'operazione.

Interpretazione corretta:

- il tentativo **non ha confermato** la programmazione del refresh remoto;
- **non dimostra** che il computer fosse spento;
- la GPO **resta collegata**;
- **non** è stato verificato il successivo aggiornamento autonomo dei criteri;
- **non ripetere tentativi RPC** senza nuove evidenze.

## 6. Passo successivo proposto (NON eseguito)

Se esiste un agente RMM già autorizzato e operativo, eseguire localmente sul client:

```
gpupdate.exe /target:computer /force /wait:120
```

Poi verificare, nell'ordine:

1. esito dell'aggiornamento;
2. presenza della GPO nei criteri effettivamente applicati;
3. valore effettivo della policy RDP;
4. stato del listener RDP;
5. raggiungibilità TCP 3389;
6. eventuali regole firewall pertinenti — **solo dopo aver raccolto evidenze**.

Questo è un **passo proposto, non un'attività completata**. Non è stato eseguito durante questa sincronizzazione documentale.

## 7. Riepilogo: fatto / non fatto / da fare

**Fatto (05/11/2026)**
- Identificazione del computer, dell'account e del SID.
- Accesso SMB amministrativo verificato; avvio di `TermService`; `RemoteRegistry` ripristinato a fermo e disabilitato.
- Test TCP 3389: `TcpTestSucceeded = False` (ultimo test ~15:00).
- Creazione e collegamento della GPO `CMP - RDP - Solo VETRO27-PC` con filtro su `VETRO27-PC$`.

**Non fatto / non verificato**
- Applicazione effettiva della GPO su VETRO27-PC.
- Refresh remoto riuscito; aggiornamento autonomo dei criteri.
- Modifiche a firewall e NLA; riavvio del computer.
- Causa dell'assenza di raggiungibilità RDP.
- Verifica di listener RDP e regole firewall.

**Da fare**
- Eseguire il passo locale `gpupdate.exe /target:computer /force /wait:120` (proposto, in attesa di esecuzione su un canale autorizzato).
- Raccogliere i criteri applicati **successivi** alla creazione della GPO e determinare il metodo di raccolta (applicati vs link individuati).
- Verificare listener RDP e firewall solo dopo le evidenze di cui sopra.

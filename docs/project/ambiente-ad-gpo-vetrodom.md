# Ambiente Active Directory e GPO — Vetrodom.local

Raccolta documentale del **6 novembre 2026**, su attività svolte il **4–5 novembre 2026**.
Le verifiche descritte in questo documento risalgono al 4–5/11/2026 e **non descrivono lo stato odierno**: la data della sincronizzazione documentale è il 06/11/2026, la data delle verifiche è sempre diversa e indicata.

## 1. Identificativi del dominio

| Elemento | Valore | Fonte |
|---|---|---|
| Dominio AD | `Vetrodom.local` | output operativo DC01/DC02 (4–5/11/2026) |
| Nome NetBIOS | `VETRODOM` | idem |
| Controller di dominio citati | `DC01-VN`, `DC02-VN` | idem |
| OU interessata | `OU=Computer,OU=Vetronaviglio,DC=Vetrodom,DC=local` | idem |
| Percorso oggetto computer | `CN=<nome>,OU=Computer,OU=Vetronaviglio,DC=Vetrodom,DC=local` | `Inventario-Nable-Utenti-20261104-152954.csv` |

## 2. Elenco dei criteri di gruppo incontrati nel materiale del 05/11/2026

Elenco ricavato dal file `Diagnosi-RDP-VETRO27.csv` (8 oggetti GPO distinti, 32 righe: 4 righe per GPO, una per ciascuna combinazione di tipo/chiave).

**Avvertenza di metodo (importante):** il file non contiene un'intestazione che identifichi il computer oggetto né il tipo di criteri rappresentati (criteri **applicati** al client oppure soltanto **configurazioni/link individuati**). Il metodo di raccolta **non è determinabile dal file stesso**. La datazione è ricavata dal timestamp di modifica del file sulla condivisione (`2026-11-05 14:41`), che è un indicatore e non un'intestazione di raccolta.

| GPO | Contesto noto nel progetto |
|---|---|
| `PC - Deploy Microsoft 365 Business` | distribuzione M365 (cfr. `inventario-m365-2026-10-12.md`) |
| `CMP - Workstation - Gestione remota` | gestione remota / apertura WinRM (cfr. `specifiche-tecniche-parco.md` §2-ter, 12/10/2026) |
| `ZBN - Hardware Inventory - Deploy Collector` | installazione del collettore hardware via GPO (cfr. `specifiche-tecniche-parco.md` §2-bis) |
| `TEST - Nable - VETRO71-PC` | GPO pilota N-able del 29/10/2026 (cfr. `deploy-nable-pilot-2026-10-29.md`) |
| `Default Domain Policy` | — |
| `USR - Tutti - Common L` | — |
| `Computer-AdminPC (Rimuovi Domain Admin)` | — |
| `USR - Tutti - Disco S` | — |

Nessuna delle righe del file contiene una impostazione `fDenyTSConnections` valorizzata: per tutte le coppie GPO/chiave l'esito è "impossibile trovare l'impostazione".

## 3. Cronologia: GPO RDP dedicata e file di diagnosi

| Data/ora | Evento |
|---|---|
| 05/11/2026 14:41 | timestamp di modifica di `Diagnosi-RDP-VETRO27.csv` sulla condivisione (riferimento esterno, non portabile) |
| 05/11/2026 ~14:58 | creazione della GPO `CMP - RDP - Solo VETRO27-PC` (output operativo su DC01) |

**Conseguenza documentale:** il file di diagnosi è **precedente** alla creazione della GPO dedicata. La sua assenza dal file **non è evidenza** di mancata applicazione della GPO: è semplicemente una fotografia precedente alla creazione. Lo stato corretto da mantenere è:

> **GPO creata e collegata; applicazione effettiva sul client non ancora verificata.**

Il perimetro e i dettagli della GPO dedicata sono in `diagnosi-vetro27-rdp-2026-11-05.md`.

## 4. Accesso remoto: stato documentato

- WinRM era risultato aperto su **0 host dei 114** rilevati nella scansione storica; dal 12/10/2026 la porta risulta aperta via GPO (`specifiche-tecniche-parco.md` §2-ter).
- Le raccolte del 04/11/2026 hanno però prodotto numerosi errori di connessione remota (WinRM/firewall "Gestione remota Windows"), per cui **48 computer su 63 non sono risultati verificabili** (cfr. `inventario-nable-2026-11-04.md`).
- Kerberos: `~/.config/krb5.conf` configurato il 30/09/2026 per il realm `VETRODOM.LOCAL`; l'accesso SMB a SYSVOL è operativo con la credenziale dedicata (`PROJECT_AI_NOTES.md`, sessione 08/10 e 30/09).
- Il client `smbclient` di questa build non usa il ccache di sistema: per letture continue il percorso previsto è il mount CIFS `sec=krb5`.

## 5. Limiti e fonti

- Nessuna verifica eseguita il 06/11/2026: nessun comando verso dominio, controller, client o RMM.
- Le evidenze citate restano sulla condivisione operativa (`\\SRVFS-VN\...`, montata in `/mnt/vetrodom-temporanea-stefano` sulla macchina di lavoro): **percorso esterno, non portabile** e non versionato in questo repository.
- Il percorso indicato dall'output su DC01 (`C:\Users\administrator.VETRODOM\Desktop\GPO-RDP-VETRO27-20261105-145820`) è un riferimento a un file esterno: non presumere che sia disponibile localmente.

## 6. Attività aperte su questo documento

1. Determinare il metodo di raccolta di `Diagnosi-RDP-VETRO27.csv` (applicati vs link individuati) e produrre un report successivo alla creazione della GPO.
2. Verificare l'applicazione effettiva di `CMP - RDP - Solo VETRO27-PC` su VETRO27-PC (criteri applicati + valore effettivo della policy).
3. Riconciliare il perimetro dichiarato delle GPO (pilota N-able limitata a 2 postazioni) con lo stato osservato degli agenti al 04/11/2026, senza dedurre la provenienza delle installazioni.

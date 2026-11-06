# Inventario agente N-able sui computer di dominio — 4 novembre 2026

Raccolta documentale del **6 novembre 2026**, su verifiche eseguite il **4 novembre 2026**.
Le verifiche descritte risalgono al 04/11/2026 (raccolta per computer fra le **15:13:15** e le **15:29:32**) e **non descrivono lo stato attuale**: la data della sincronizzazione documentale è il 06/11/2026.

## 1. Fonte e metodo

| Elemento | Valore |
|---|---|
| File di evidenza (non versionato) | `Inventario-Nable-Utenti-20261104-152954.csv` |
| Percorso operativo esterno | condivisione interna montata in `/mnt/vetrodom-temporanea-stefano` — **riferimento non portabile** |
| Timestamp di modifica del file | 2026-11-04 15:29:54 |
| Metodo | interrogazione remota per computer del servizio Windows di monitoraggio (`Advanced Monitoring Agent`), con raccolta di stato servizio, avvio, percorso del binario, ultime righe di log e sessione console |
| Computer esaminati | 63 (unici) |
| Copertura | computer di dominio `Vetrodom.local`; i controller di dominio non risultano fra i 63 |

## 2. Conteggi verificati sul file

| Esito | Computer | Significato |
|---|---|---|
| Agente presente, servizio `Running` | **12** | servizio attivo al momento del controllo |
| `Servizio agente assente` | **3** | servizio non presente sulla macchina (rilevazione positiva di assenza) |
| `Non verificabile` | **48** | **connessione remota non riuscita**: stato dell'agente **ignoto**, non assente |

Attenzione: la riga "non verificabile" **non equivale** a "agente assente". Tutti i 48 hanno una riga di errore di connessione remota (Gestione remota Windows / firewall / raggiungibilità).

## 3. Computer con agente presente e servizio Running (12)

| Computer | Ultima riga di log | Note |
|---|---|---|
| `BETTINADUE` | 02/11/2026 10:33:05 — verifica locale OK | |
| `VETRO09-PC` | 04/11/2026 10:26:09 | |
| `VETRO29-PC` | 02/11/2026 10:00:47 | |
| `VETRO33-PC` | 04/11/2026 08:16:37 | |
| `VETRO38-PC` | 04/11/2026 11:18:17 | |
| `VETRO43-PC` | 02/11/2026 09:40:11 | |
| `VETRO45-PC` | 02/11/2026 09:56:34 | |
| `VETRO54-PC` | 04/11/2026 13:40:03 | |
| `VETRO71-PC` | 04/11/2026 12:41:52 | pilota N-able di ZBN (`deploy-nable-pilot-2026-10-29.md`) |
| `VETRO79-PC` | 02/11/2026 10:10:02 | |
| `VETRO80-PC` | 02/11/2026 13:04:22 | |
| `VETRO82-PC` | 02/11/2026 09:53:05 | |

Sistemi operativi rilevati fra i 63 computer: Windows 10 Pro, Windows 11 Pro, Windows 7 Professional.

## 4. Computer con servizio agente assente (3)

`VETRO06-PC`, `VETRO07-PC`, `VETRO32-PC` — servizio assente rilevato; nessun errore di connessione (la macchina ha risposto al metodo remoto).

## 5. Non verificabili (48)

Suoi casi noti e rilevanti:

- `VETRO27-PC` — connessione remota non riuscita (stato agente ignoto; cfr. `diagnosi-vetro27-rdp-2026-11-05.md`).
- `VETRO53-PC` — connessione remota non riuscita. **Non è un agent-assente**: al 29/10/2026 il servizio era `Running / Automatic` (documento pilota). Al 04/11 lo stato è **indeterminato**.

L'elenco completo dei 48 resta nel CSV di origine sulla condivisione.

## 6. Perimetro dichiarato vs stato osservato

**Due fatti distinti, senza dedurre la provenienza delle installazioni:**

1. **Perimetro dichiarato (29/10/2026):** la distribuzione N-able di ZBN era limitata a due postazioni pilota (`VETRO71-PC`, `VETRO53-PC`), con GPO `TEST - Nable - VETRO71-PC` e nessuna estensione generale autorizzata (`deploy-nable-pilot-2026-10-29.md`, `agente-deploy-tracker.csv`).
2. **Stato osservato (04/11/2026):** 12 computer con servizio `Running`.

La presenza di 12 servizi attivi **non dimostra** chi li abbia installati, con quale metodo, né se installazioni e perimetro dichiarato si sovrappongano: **la sovrapposizione effettiva tra i due elenchi non è stata verificata** e non viene affermata. Il documento storico del pilota e `agente-deploy-tracker.csv` **non sono stati modificati**.

## 7. Limiti

- Rilevazione **puntuale** del 04/11/2026 via metodo remoto: non distingue agenti obsoleti, disinstallati o reinstallati.
- 48 computer su 63 non raggiungibili con il metodo usato: copertura reale **non nota**.
- Nessuna verifica di registrazione o attività in console presso il fornitore.
- Il file di origine non è stato copiato in questo repository (fase documentale senza import di CSV).

## 8. Attività aperte

1. Secondo inventario dopo il ripristino dell'accesso remoto, per coprire i 48 non verificabili e i 3 senza servizio.
2. Chiarire, con il fornitore/Agis Lab, l'origine degli agenti presenti sui computer fuori pilota e la loro effettiva copertura in console.
3. Risolvere i problemi di accesso remoto WinRM/firewall che rendono non verificabile più del 75% del parco.
4. Conferma del fornitore su presenza e attività di `VETRO53-PC` in console (aperto dal 29/10/2026).

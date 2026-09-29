# Changelog — Agis Lab

## 2026-09-16 — Bootstrap

- Apertura progetto da template `triathlon-starter`.
- Creazione repo GitHub `StefanoBonfanti66/agis-lab` (privato).
- Profilo MCP: `minimal`.
- Struttura `docs/` canonica inizializzata.
- In attesa di collocazione del PDF questionario Agis Lab.

## 2026-09-16 — Analisi documenti e prima traccia di risposta

- Collocato e analizzato `Relazione_preliminare_IT_Vetronaviglio.pdf` (Agis Lab, 10 pagine); sintesi in `docs/project/agis-lab-sintesi.md`.
- Estratto e analizzati i file `.msg`: richiesta/risposta IT Impresa (10/09/2026, credenziali dietro richiesta dell'amministratore) e ticket Microsoft #2609161420000280 (M365, elevazione account, 16/09/2026).
- Acquisito inventario rete `app/lan_inventory` (scansione 192.168.24.0/24, ~90 host, 15–16/09/2026).
- Redatta bozza di risposta ad Agis Lab con stato fornitori + evidenze + domande di chiarimento: `docs/leads/agis-lab-risposte.md` (da validare con CEO prima di ogni invio).
- Aggiornata risposta con integrazioni (IT Impresa ⇒ anche firewall WatchGuard; SAPI ⇒ accessi stampanti; centralino ⇒ fornitore Alascom in verifica contratto; allarme/videosorveglianza ⇒ Abbiati) e con le risposte di Stefano alle 9 domande di chiarimento (canale: invio diretto di Stefano; percorso progressivo confermato; formato consegna Excel; NDA da predisporre per la direzione).
- Predisposta bozza accordo di riservatezza (NDA) Vetronaviglio–Agis Lab: `docs/project/accordo-riservatezza-agis-lab.md` (da validare con direzione e legale).
- Generati file condivisibili da markdown: `leads/agis-lab-risposte.html` + `.pdf` (6 pagine) e `project/accordo-riservatezza-agis-lab.html` + `.pdf`, via pandoc + Chrome headless.
- **Branding rimosso (regola «nessun ZBN»):** eliminati riferimenti a ZBN/ZetaByteNexus da documenti, sintesi e dati inventario (hostname `zbn-srv01.local` → `lan-scan01.local` in CSV/HTML/XML/log/DB/XLSX). Verifica repo pulita.

## 2026-09-16 — Invio NDA alla direzione

- Redatta bozza email per Bettina Solito de Solis con richiesta di valutazione dell'accordo di riservatezza (e passaggio a un legale): `docs/leads/email-bettina-nda-agis-lab.md`.
- Allegato: `docs/project/accordo-riservatezza-agis-lab.pdf`.
- Da confermare prima dell'invio: indirizzo email di Bettina e completamento placeholder NDA.

## 2026-09-16 — Pulizia e reframing `lan_inventory` come strumento aziendale

- Verifica architettura `lan_monitor.py` (pipeline: nmap → inventario → classificazione → snapshot → sicurezza → report) e sintassi dei 7 moduli attivi OK.
- Rimossi script morti/duplicati/versionati (12 file) e DB/cifre di test (6 DB, 3 scan XML datati) → archiviati in `_archive_old/` per riferimento, non eliminati.
- README riscritto: focus non invasivo (nessuna credenziale/agente) e uso come biglietto da visita pre-engagement in aziende nuove.
- Evoluzioni previste tracciate: raccolta autenticata a privilegi minimi, identità MAC, classificatori VoIP/allarmi/BMS, notifiche variazioni.

## 2026-09-16 — `lan_inventory`: piano di evoluzione punti 1-5

- **Identità MAC + DHCP** (`inventory.py`): upsert che risolve l'identità dal MAC con ricaduta sull'IP, indice univoco parziale su `devices(mac)`, gestione scambio IP tra dispositivi (`swap_ips`) e collisioni su IP riusato; comparazione snapshot stabile via MAC (`inventory_report_v160.py` `device_key`).
- **Raccolta autenticata opzionale a privilegi minimi** (`windows_inventory.py`): refactor config-driven — rimossi riferimenti Vetronaviglio hardcoded (`SERVERS`), identità da `windows_servers.json` (IP/nome/account), password solo in memoria via `getpass`; eseguito solo se configurato.
- **Classificatori ampliati** (`auto_classify_and_report.py`, `inventory.py`): firme HIGH per allarmi/antifurto (Ksenia), biometrici/access control (Anviz/ZKTeco/Suprema), BMS (BACnet/Modbus/KNX/Schneider), reti (IP-COM/Netis/Tenda), VoIP/centralini (Alcatel/ALE/OmniPCX); port-based MEDIUM per telefonia (5100/5102/7070, H.323 1719/1720).
- **Report esecutivo** (`executive_report.py`, nuovo): sheet monofoglio per riunioni con KPI, trend tra snapshot, alert per severità, distribuzione ruoli e top 20 dispositivi a rischio.
- **Multi-cliente** (`lan_monitor.py` v1.8.0): flag `--client <nome>` con registry `clients.json` (etichetta, target nmap, sottocartella output); output/DB/log in `lan_inventory_output/<cliente>/`; report esecutivo integrato nella pipeline.
- README aggiornato (componenti, clienti, limiti, evoluzioni implementate).

## 2026-09-16 — `lan_inventory`: bugfix dal primo run su database vergine

- **`security_monitor_v152.py`**: la tabella `security_alerts` veniva data per scontata (nasceva dagli script archiviati in `_archive_old/`); ora `ensure_columns` esegue prima `CREATE TABLE IF NOT EXISTS security_alerts` con lo schema base, poi le migrazioni ALTER per le colonne successive. Senza questo il primo run su DB nuovo crashava con `no such table: security_alerts`.
- **`auto_classify_and_report.py`**: la CLI ora accetta `--db` e `--out` (prima leggeva/scriveva sempre i path di default della cartella base, ignorando i DB per-cliente). La fase CLASSIFY di `lan_monitor.py` passa i path corretti → la colonna `role` viene scritta sul DB giusto.
- **`auto_classify_and_report.py`**: query sulle tabelle `windows_inventory`/`windows_disks`/`windows_network` ora guardate con `table_exists` — su DB senza collector WinRM crashava con `no such table`.
- **`windows_inventory.py`**: `import winrm` in cima al modulo faceva fallire il probe `--help` dei collector (log fuorviante «CLI non espone --db»). Import reso opzionale: senza `pywinrm` la fase si salta con messaggio esplicito (exit 0), la collezione resta possibile dove la libreria è installata.
- Verificato end-to-end su rete reale: pipeline v1.8.0 completa (100 dispositivi, snapshot #2, 327 servizi aperti, 64 alert di cui 5 HIGH) con i 3 report Excel per-cliente generati.

## 2026-09-16 — NDA completato e email ad Agis Lab

- **NDA completo con dati di entrambe le società:** Agis Lab da relazione preliminare p.1 (Via Carnevali 48, 20158 Milano, P.Iva 07088660969, REA MI-1935058, cap. soc. €10.000,00) e Vetronaviglio forniti da Stefano (Via Don Severino Fracassi 31/39, Bareggio MI, P.Iva IT03366120271, CEO Bettina Solito de Solis).
- Decisioni registrate: **nessun riferimento alla vertenza Abbiati**; canale consegna credenziali **da decidere successivamente**; **Parte Divulgante = solo Vetronaviglio**.
- Rigenerati HTML + PDF del NDA (`accordo-riservatezza-agis-lab.pdf`, 63 KB) — verifica art.1 con dati completi di entrambe le parti. Nota: usato `/usr/bin/google-chrome-stable` (lo wrapper `/home/sbonfanti/bin/google-chrome` ha shebang rotto e snap chromium non installato).
- Redatta e **confermata da Stefano** la bozza email ad Alessandro Viviano con allegato NDA: `docs/leads/email-agis-nda.md`. Indirizzo email di Viviano **da inserire manualmente da Stefano** prima dell'invio.
## 2026-09-29 — `lan_inventory`: raccolta hardware automatica (share + GPO), verificata e corretta

- Analisi del metodo "Livello 1-bis" (`docs/project/specifiche-tecniche-parco.md` §2-bis) e verifica end-to-end dei 3 script su dati di prova costruiti nella forma reale di Windows PowerShell 5.1 (BOM UTF-8, date CIM `/Date(...)/`, adattatore Hyper-V davanti a quello fisso). La verifica ha trovato **3 difetti reali nel codice di produzione** che rendevano l'Excel inutilizzabile pur con exit 0.

### Difetti corretti

- **`import_hardware.py` — colonne sfalsate di una (critico).** I valori erano allineati per posizione con l'elenco delle colonne, ma la lista partiva da `collected_at`, che nelle colonne è **ultimo**: nell'Excel finiva `Hostname` = data di raccolta, `RAM GB` = numero di slot usati, `Installato il` = build dell'OS, `Raccolto il` = vuoto. Riscritta la costruzione del record per **chiave** (`{key: record.get(key, "") for key, _ in COLUMNS}`): ogni colonna prende il proprio campo per nome, quindi un ordine diverso non sposta più nulla.
- **`import_hardware.py` / `collect_hardware.ps1` — date grezze.** PowerShell 5.1 serializza le date CIM come `/Date(1640995200000)/` e finivano così nell'Excel. Introdotto `ps_date()` in import e `Get-IsoDate()` in raccolta (le date escono già ISO dal PC).
- **`import_hardware.py` / `collect_hardware.ps1` — IP sbagliato.** Veniva scelto il primo IP non di loopback, che con Hyper-V/WSL/VPN è l'adattatore virtuale (es. `192.168.137.1` invece di `192.168.24.31`): avrebbe prodotto falsi "IP cambiati" nella riconciliazione con `inventory.db` su tutto il parco. Il collettore ora marca `virtual` sulle schede non fisiche (join `Win32_NetworkAdapterConfiguration` ↔ `Win32_NetworkAdapter` su `Index`) e `pick_ip()` le scarta.

### Affidabilità e GDPR

- **`install_task_hardware.ps1` — rotto via GPO.** Il default `-Script "$PSScriptRoot\collect_hardware.ps1"` non funziona: la Startup folder della GPO riceve il solo installer, quindi il `Copy-Item` del collettore falliva su ogni PC. Ora risolve in ordine: `-Script` esplicito → fratello in `$PSScriptRoot` → fratello nella stessa share UNC da cui è lanciato; se non trova nulla, errore esplicito invece di installazione a metà. Istruzione con il percorso SYSVOL aggiunta in §2-bis e §7.
- **Share non scrivibile = falso "funziona".** Con `SilentlyContinue` una share non scrivibile non scriveva nulla e usciva comunque 0: si sarebbe creduto alla raccolta partita. Ora l'installer **verifica la scrivibilità** prima di installare (probe + `throw`), il collettore controlla l'uguaglianza del file scritto, scrive `collect.log` in locale ed **esce 1**.
- **Dati personali fuori dalla raccolta.** `asset_tag` era valorizzato con `$cs.UserName` (non è un asset tag, è dato personale, ed è vuoto perché il task gira come SYSTEM) e `logged_user` finiva nel JSON sulla share. Rimossi entrambi; `asset_tag` del template resta da assegnare a mano.
- **`-CsvOnly` era invertito** (disattivava il CSV) e il task GPO passava proprio quel flag: `hardware.csv` non sarebbe mai stato prodotto e l'installazione avrebbe fallito con parametro sconosciuto. Flag rinominato `-NoCsv`; il `-Weekly` ora usa `-RandomDelay` al posto dell'assegnazione a mano di `.Delay` (114 PC non si svegliano nello stesso secondo).
- **`-Uninstall`** su `install_task_hardware.ps1`: elimina task, script e log in un comando, come promesso in §2-bis.
- Estese le colonne con **`Tipo` (Fisso/Notebook da `PCSystemType`)**, **`Scheda video`** (`Win32_VideoController`) e **`Slot RAM totali`**: §4 elencava come "da aprire fisicamente" / "da aggiungere" dati che WMI conosce già. Rimane solo il *tipo* di modulo a vista, e serve solo per scegliere il KIT di espansione. Aggiunta la riga `Fisso / Notebook` al foglio `Riepilogo`.
- Documentazione allineata: §2-bis (tabella dei 3 file, parametro GPO, reversibilità, colonne apicali, **blocco "Test eseguito" riscritto con i 3 difetti trovati e il risultato verificato**), §4 (tabella e convenzioni), §6 (vincolo GDPR), §7 (parametro `-Script`), `app/lan_inventory/README.md` (i 3 file nella tabella "Componenti attivi" + nota sulle due vie di raccolta, rete vs macchina).
- **Entrambi gli script validati sintatticamente** con il parser di PowerShell 7.6.5; l'esecuzione reale non è possibile da Linux (CIM è Windows-only).
- **Attivato su 1 PC pilota il 29/09/2026 (~12:25 CEST):** share creata con l'ACL già risolta sul gruppo AD dedicato `VETRODOM\SG-HardwareInventory-Writers` (*Change* sulla condivisione `TEMP-STEFANO`, *Modify* sull'ACL NTFS di `inventory-hardware`), task installato ed eseguito come `NT AUTHORITY\SYSTEM`, `VETRO33-PC.json` prodotto e valido (`schema_version: 1`). Nessun rollout: 1 PC su 114, nessuna GPO creata, nessun altro PC aggiunto al gruppo. Il pilota ha usato il **template generico di `opencode-config`** distribuito dalla SYSVOL (`\\dc01-vn.vetrodom.local\SYSVOL\Vetrodom.local\scripts\hardware-inventory\`), non la copia locale in `app/lan_inventory/`.
- **Difetto emerso dal pilota, non ancora corretto:** nel template il join dei dischi usa `DeviceID`, ma `Win32_DiskDrive.DeviceID` vale `\\.\PHYSICALDRIVE0` e `Win32_LogicalDisk.DeviceID` vale `C:` → la corrispondenza non avviene e **modello e seriale del disco arrivano vuoti nel JSON**. Corretta la catena richiesta: `Win32_LogicalDiskToPartition` → `Win32_DiskDriveToDiskPartition`. Da correggere prima di estendere la raccolta a tutto il parco.

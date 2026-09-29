# LAN Asset Inventory — strumento di rilevamento rete

Strumento di inventario e monitoraggio del parco installato basato su scansione non invasiva.
Crea uno storico versionato e dei report condivisibili **senza richiedere credenziali, agenti o accessi** ai dispositivi:
un modo immediato per mostrare come si lavora quando si entra in un'azienda nuova.

## Cosa fa

Lettura dell'XML prodotto da Nmap (scansione non autenticata) con generazione di:

- **SQLite** — base dati con storico a snapshot immutabili (hash SHA-256 per rilevare cambi identici)
- **CSV** — inventario semplice
- **XLSX** — inventario filtrabile e report di sicurezza
- **HTML** — report consultabile dal browser

Nmap non vede RAM, CPU, numero di modulo o seriale. Per le **specifiche hardware** dei PC in
dominio esiste una seconda via, in **push** sul PC (CIM/WMI in locale, nessuna porta
aperta): `collect_hardware.ps1` → share → `import_hardware.py`. Le due vie non si sovrappongono,
la prima fotografa la rete, la seconda le macchine.

## Componenti attivi

| File | Ruolo |
|---|---|
| `lan_monitor.py` | Orchestratore: nmap → inventario → classificazione → snapshot → sicurezza → report |
| `inventory.py` | Import XML nmap in SQLite (dispositivi + servizi), identità MAC con gestione DHCP |
| `auto_classify_and_report.py` | Classificazione automatica dei dispositivi |
| `security_monitor_v152.py` | Rilevazione alert di sicurezza |
| `inventory_report_v160.py` | Report inventario (XLSX/HTML) |
| `security_report_v152.py` | Report sicurezza |
| `executive_report.py` | Report esecutivo monofoglio per riunioni (KPI, trend, rischi) |
| `windows_inventory.py` | Collector opzionale a privilegi minimi (WinRM/CIM) — seriale/modello/componenti, solo se configurato |
| `collect_hardware.ps1` | Raccolta hardware **push** sul PC (CIM/WMI, nessuna porta aperta): JSON per macchina sulla share. Task pianificato, `-NoCsv` per non scrivere il CSV cumulativo |
| `install_task_hardware.ps1` | Installer del task "Vetrodom HW Inventory" (SYSTEM, all'avvio + settimanale): verifica la scrivibilità della share, log locale, `-Uninstall` per la rimozione. Via GPO va lanciato con `-Script \\SERVER\share\collect_hardware.ps1` |
| `import_hardware.py` | Importa i JSON raccolti e genera l'Excel `Specifiche parco` (20 colonne) + foglio `Riepilogo`; normalizza le date, scarta gli adattatori virtuali, fallback CSV. Con `--workbook` riempie invece i fogli `Windows Inventory` / `Disks` / `Network` di un inventario di rete già esistente, scrivendo una copia e lasciando l'originale intatto; in quel caso il join avviene sul **MAC** (l'hostname fa solo da ripiego, perché l'IP ruota sulle macchine in leasing) e l'IP scritto è quello osservato sul PC: se differisce da quello dell'inventario la differenza resta tracciata nella colonna `Status` del foglio `Windows Inventory` |
| `clients.json` | Registry clienti (etichetta, target nmap, sottocartella output) |
| `requirements.txt` | Dipendenze |

File storici/superati spostati in `_archive_old/` (mantenuti per riferimento, non usati dal pipeline).

## Installazione e avvio

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Avvio completo (richiede permessi per nmap):

```bash
python3 lan_monitor.py --target 192.168.24.0/24
```

Per un cliente registrato in `clients.json` (target e output dedicati):

```bash
python3 lan_monitor.py --client vetronaviglio
```

`--client` instrada target, DB e output in `lan_inventory_output/<cliente>/`; `--target` resta disponibile per sovrascrivere il target del cliente. Aggiungere un nuovo cliente = aggiungere una voce in `clients.json`.

Si può eseguire solo l'analisi dei dati già scanati:

```bash
python3 lan_monitor.py --skip-nmap --target 192.168.24.0/24
```

Altri flag utili: `--skip-reports`, `--dry-run`, `--keep-nmap`, `--nmap-extra`.

Output in `lan_inventory_output/` (con `--client` in `lan_inventory_output/<cliente>/`):

```text
lan_inventory_output/
├── inventory.db                 # base dati con storico snapshot
├── inventory.csv                # inventario semplice
├── inventory.xlsx               # inventario filtrabile
├── inventory.html               # report browser
├── LAN_Inventory_Professional.xlsx
├── LAN_Security_Report.xlsx
├── LAN_Executive_Report.xlsx    # sintesi per riunioni/management
├── nmap_latest.xml              # ultima scansione
└── logs/                        # log di esecuzione
```

## Evoluzioni implementate (v1.8)

1. **Raccolta autenticata opzionale a privilegi minimi** — `windows_inventory.py` via WinRM/CIM legge ComputerName, seriale, modello, hardware e software con un solo account dedicato (in `windows_servers.json`, mai password nel codice); viene eseguito solo se configurato.
2. **Identità MAC + DHCP** — l'upsert in `inventory.py` risolve l'identità dal MAC (ricadendo sull'IP senza MAC) e gestisce lo scambio di IP tra dispositivi (DHCP) preservando `first_seen`; i confronti tra snapshot sono stabili via MAC.
3. **Classificatori ampliati** — aggiunti apparati VoIP/centralini (Alcatel/ALE, porte 5100/5102/7070, H.323), allarmi/antifurto (Ksenia), biometrici/access control (Anviz, ZKTeco), BMS (BACnet/Modbus/KNX), reti (IP-COM/Netis/Tenda…).
4. **Report esecutivo** — sheet monofoglio con KPI, trend tra snapshot, distribuzione per ruolo, alert aperti per severità e dispositivi a rischio, pronto per riunioni con il management.

## Robustezza su database nuovo (verificato su rete reale)

- `security_monitor_v152.py` crea da sé la tabella `security_alerts` se assente, poi applica le migrazioni delle colonne successive.
- `auto_classify_and_report.py` accetta `--db`/`--out` (usa il DB per-cliente corretto) e non assume più l'esistenza delle tabelle `windows_*` del collector opzionale.
- `windows_inventory.py` salta con un messaggio esplicito quando `pywinrm` non è installato (il probe `--help` del pipeline resta funzionante).

## Limiti noti (v1)

- Nmap non autenticato identifica IP, MAC/vendor, hostname, OS (quando la detection è sufficiente) e servizi esposti; seriale/modello/componenti arrivano solo dal collector Windows opzionale con autorizzazione del cliente.
- Con DHCP dinamico il confronto tra scan successivi è stabile grazie al MAC, ma un host senza MAC viene ancora inseguito via IP.
- La classificazione è euristica (hostname/vendor/servizi): può non riconoscere apparati particolari se non presentano firme note.

## Evoluzioni previste

1. Notifiche di variazione (eventi new/missing/changed su dispositivi e servizi).
2. Collector Linux (SSH) e rete (SNMPv3/API) oltre a quello Windows già disponibile.
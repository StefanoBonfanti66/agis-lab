# Runbook — Agis Lab

## Convenzione documenti

- **PDF questionario originale** → salvarlo in `docs/project/` con nome `agis-lab-questionario.pdf` (se il tema è il progetto) oppure in `docs/leads/` se è un questionario di qualifica convendenda. La decisione dipende dalla natura del PDF.

## Flusso di lavoro previsto

1. Ricezione PDF questionario da Agis Lab.
2. Collocazione del file in `docs/project/` o `docs/leads/`.
3. Estrazione delle domande → file di lavoro `docs/leads/agis-lab-risposte.md` (in attesa di conferma nomenclatura).
4. Bozza di risposta per ciascuna domanda.
5. Validazione CEO (umana) prima di qualsiasi invio.
6. Invio e tracciamento della risposta in `docs/changelog.md`.

## Regole

- Nessun invio senza approvazione umana.
- Mai rete/segreti nel documento di risposta.
- Aggiornare `docs/changelog.md` a ogni milestone.

---

## Procedure — completamento della risposta ad Agis Lab (08/10/2026)

Ordine di esecuzione: **A** = eseguibile oggi dal PC Ubuntu; **B** = serve un accesso che
abbiamo già (credenziali in `Vetronviglio.docx`); **C** = dipende da altre persone, da una
visita in sede o da una decisione della direzione. Niente in questa sezione autorizza invii:
ogni documento esce solo dopo validazione umana.

### 0 — Materiali già pronti (non rigenerare se non cambiano i JSON)

| Cosa | Dove | Punto della risposta |
|---|---|---|
| Specifiche parco, 22 postazioni | `app/lan_inventory/lan_inventory_output/Specifiche_parco_2026-10-12.xlsx` (9,0 KB) | 2, 4.1 |
| Postazioni **+ 5 server** nei fogli hardware | `app/lan_inventory/lan_inventory_output/LAN_Inventory_Professional_hardware.xlsx` (`Windows Inventory` 27, `Disks` 43, `Network` 28) | 2, 4.1, 4.2 |
| Elenco VM, stato accessi, gap | `docs/project/fornitori-contratti.md` (§1 matrice, §2 gap, §3 azioni) | 4.2, 4.3, 4.4, 4.8, 4.9 |
| Credenziali apparati e tenant | `docs/project/Vetronviglio.docx` — **consegnato ad Agis Lab 08/10/2026 via WeTransfer protetto da password** (ricevuto da Viviano); **mai riprodotte in email o in altri documenti** | 4.2, 4.4, 4.6 |
| Checklist EXO + script sola lettura | `docs/project/email-deliverability-checklist.md` §4, `app/email-diagnostics/check_caso_bettina.ps1` | 4.6 (e residuo caso A) |
| Bozza di risposta in lavorazione | `docs/leads/email-viviano-riscontro-censimento.md` | — |

Rigenerazione (da root del repo; l'import è un **merge per host**: i server già inventariati
restano nei fogli):

```bash
python3 app/lan_inventory/import_hardware.py \
  --input-dir /mnt/vetrodom-temporanea-stefano/inventory-hardware \
  --workbook app/lan_inventory/lan_inventory_output/LAN_Inventory_Professional.xlsx
python3 app/lan_inventory/import_hardware.py \
  --input-dir /mnt/vetrodom-temporanea-stefano/inventory-hardware \
  --out "app/lan_inventory/lan_inventory_output/Specifiche_parco_$(date +%F).xlsx"
```

**Attenzione alla lettura del foglio:** le colonne `Monitor` e `Antivirus` restano vuote
perché il collector deployato non le legge — non vanno riportate ad Agis Lab come
«postazione senza antivirus». Stessa cosa per `Inventory`/`Servers` del workbook di rete:
sono classificazioni automatiche (256 / 74), non conteggi.

### A1 — Postazioni: chiudere i dati mancanti (punti 2 e 4.1)

1. Rieseguire i due comandi qui sopra e allegare il file delle specifiche (9,0 KB, nessun
   problema di peso verso `agislab.it`). Verifica dopo la rigenerazione: `Specifiche parco`
   = **22 righe**, `Riepilogo` = «Macchine raccolte 22», «Fisso / Notebook 11 / 11»;
   `Windows Inventory` = **27** (5 server + 22 PC), `Disks` = **43**, `Network` = **28**.
2. **Utilizzatore e collocazione non esistono nello scanner** (dato personale, escluso per
   scelta): si ricavano solo dal registro assegnazioni dell'azienda. Chiedere a Federico o
   Bettina il foglio postazione ↔ utente ↔ stanza e unirlo in colonna su una copia del
   foglio `Specifiche parco` — **non** aggiungerlo al file che gira sui PC.
3. Le macchine fuori dalla `192.168.24.0/24` della sede al 12/10: `ACQUISTI` (.6) e
   `VETRO51-PC` (.24) su `192.168.1.0/24`, `VETRO21-PC` (.30) su `192.168.0.0/24`.
   * **`ACQUISTI` — CHIUSA:** è **a casa di un dipendente e si collega via VPN**
     (confermato il 12/10). Non è una postazione fuori rete da investigare. Conseguenza
     operativa: non usarne l'IP (`192.168.1.6` è la LAN domestica, non routingabile dal
     server) ma il nome host, e i test remoti dipendono dalla VPN attiva.
   * Restano da chiarire **`VETRO51-PC`** (stessa fascia `192.168.1.0/24`: stesso caso di
     smart working?) e **`VETRO21-PC`** (terza sottorete, ancora non spiegata). Se
     rispondono: `nmblookup -A <ip>` e `nmap -sV -p 445,139 <ip>`, altrimenti chiedere a
     Federico.
   **Attenzione:** al 08/10 la seconda macchina era `VETRO83-PC` (.111), ma gli IP DHCP
   sono ruotati e oggi `VETRO83-PC` è su `192.168.24.108` → **rileggere i JSON prima di
   citare un IP**.
4. I 4 host raccolti ma assenti dall'inventario di rete (`VETRO01-PC`, `VETRO21-PC`,
   `VETRO42-PC`, `VETRO46-PC`): sono macchine nuove o mai viste dalla scansione → vanno
   confermati a mano, sono comunque da inserire nell'elenco.

### A2 — Windows 10: valutazione delle 3 macchine (punto 3) — **CONCLUSA il 12/10/2026**

**WinRM è ora raggiungibile** (GPO) → il test si fa **da remoto**, senza RDP né sessione
locale. Pre-passo obbligato:

```powershell
# sul server, come admin di dominio
Test-WSMan -ComputerName VETRO32-PC   # deve rispondere prima di procedere

$check = {
  $os=Get-CimInstance Win32_OperatingSystem; $cs=Get-CimInstance Win32_ComputerSystem
  $cpu=Get-CimInstance Win32_Processor|Select-Object -First 1
  $c=Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
  $disk=Get-Partition -DriveLetter C -EA SilentlyContinue|Get-Disk -EA SilentlyContinue
  $gpu=Get-CimInstance Win32_VideoController|Select-Object -First 1
  $tpm=try{Get-Tpm -EA Stop}catch{$null}
  $sb=try{if(Confirm-SecureBootUEFI){'ATTIVO'}else{'DISATTIVO'}}catch{'NON DISPONIBILE (Legacy BIOS?)'}
  $fw=try{(Get-ComputerInfo -Property BiosFirmwareType -EA Stop).BiosFirmwareType}catch{'N/D'}
  $lic=try{(Get-CimInstance SoftwareLicensingProduct|Where-Object{$_.PartialProductKey -and $_.LicenseStatus -eq 1}|Select-Object -First 1).Description}catch{'N/D'}
  [pscustomobject]@{Host=$env:COMPUTERNAME; OS="$($os.Caption) build $($os.BuildNumber)"; CPU=$cpu.Name
    RAM_GB=[math]::Round($cs.TotalPhysicalMemory/1GB,1); Firmware=$fw
    DiskStyle=if($disk){$disk.PartitionStyle}else{'N/D'}; SecureBoot=$sb
    TPM=if($tpm -and $tpm.TpmPresent){"SI Ready=$($tpm.TpmReady) Enabled=$($tpm.TpmEnabled) Ver=$($tpm.ManufacturerVersionTxt)"}else{'NO'}
    GPU="$($gpu.Name)  drv=$($gpu.DriverVersion)"; SpaceC_GB=[math]::Round($c.FreeSpace/1GB,1); Licenza=$lic}
}
Invoke-Command -ComputerName VETRO32-PC,VETRO53-PC -ScriptBlock $check | Format-List
```

**Attenzione a due trappole** (capite facendo): (a) `$check` vive nella sessione del
server — se si apre una `Enter-PSSession` e poi si incolla lì, `$check` è **null** e
`Invoke-Command` fallisce con *«L'argomento è null»*: ridefinirlo nella sessione in uso, oppure
dentro la PSSession incollare direttamente il contenuto dello script block (senza
`Invoke-Command`); (b) `ACQUISTI` va raggiunta **per nome host**, non per IP (vedi A1.3).

**Esito — registrato in `specifiche-tecniche-parco.md` §2-ter:**

| Host | Esito |
|---|---|
| `VETRO32-PC` | ❌ **non aggiornabile** — Legacy BIOS/MBR, **nessun TPM 2.0**, i5-650 fuori lista, iGPU non WDDM 2.0/DX12. Licenza `VOLUME_MAK`. |
| `VETRO53-PC` | ❌ **non aggiornabile** — stessi 4 blocchi hardware. Licenza `RETAIL`. |
| `ACQUISTI` | ❌ **dedotto** (stesso modello/BIOS/CPU), **non misurata**: a casa del dipendente, VPN. |

⇒ **Sostituzione, non aggiornamento.** Un'unica fornitura per le tre. Da valutare con il
VAR la copertura **ESU** di Windows 10 in attesa del rinnovo. Resta aperto, per la bozza
email, il punto (3): **data EOL Windows 10 da verificare con fonte Microsoft**.

### B1 — Server fisici e virtuali (punto 4.2)

1. Aprire le credenziali in `Vetronviglio.docx` (Syneto/ESXi/IPMI) ed elencare le VM:
   l'elenco **già pronto** è in [`inventario-syneto-2026-10-12.md`](./inventario-syneto-2026-10-12.md)
   (integrato il 12/10 dai due PDF del 09/10: 9 VM del principale, 5 del secondario,
   `syneto-os-02`) — **non ricrearlo**. La discrepanza IP di Veeam è **chiusa**:
   `.135` = Veeam (PDF §4 + OUI VMware in scan), `.227` = Axtrax (hostname in scan).
   Qui vanno solo le **conferme in console**: IP/state di Axtrax, SynetoOS,
   SynetoFileRecovery, le 5 VM del secondario, e identità di `.127`.
2. Stato di supporto e licenze dei server Windows: i 5 server sono già nel foglio
   `Windows Inventory` del workbook (`Windows Server 2019 Standard` ⇒ supporto fino a
   09/2029, da confermare per edizione/licenza) — nessuna raccolta nuova.
3. Compilare la colonna «Stato / azione» della matrice con funzione, configurazione,
   stato supporto, licenza e chi ne è titolare.

### B2 — Backup e ripristino (punto 4.3) — solo con finestra concordata

1. Concordanza con Agis Lab (o con la direzione) della finestra: un ripristino di prova
   tocca dati reali.
2. In console Veeam: elenco job, frequenza, retention, repository, ultimo job riuscito →
   riportare **RPO dichiarato vs RPO reale**.
3. Eseguire un ripristino **livello file** su una cartella non critica, cronometrarlo e
   fotografare l'esito: è la prova che serve per rispondere su «effettiva possibilità di
   ripristinare».
4. NAS QNAP: l'admin non funziona e il reset è **distruttivo** → non fare nulla in
   autonomia, richiedere la risoluzione a IT Impresa insieme agli altri residui (B4).
5. Aggiornare la riga *Backup* di `docs/project/fornitori-contratti.md` (§2) da 🔴 a 🟡/🟢
   con data ed esito del test.

### B3 — Firewall WatchGuard (punto 4.4)

**Rilievo eseguito il 12/10/2026 (~12:00 CEST) in sola lettura da console web** → esito
completo in [`rilievo-watchguard-2026-10-12.md`](./rilievo-watchguard-2026-10-12.md)
(**rilievo operativo e licenze, non audit di sicurezza**). In sintesi: 2× Firebox M290 in
FireCluster active-passive (cluster ID 50; master `M290-2-Vetronaviglio` `C0390AFD27527`,
backup `M290-1-Vetronaviglio` `C0390AEECC116`), entrambi Online e Synchronized, salute 100,
Fireware **12.12.B733447** con «Upgrade Available», licenze **Enabled fino al 29/06/2028**
(627 giorni), firme/database aggiornati. **Nessuna modifica eseguita.**

Stato dei passi:

1. Licenze e sottoscrizioni → **✅ lette dalla Feature Key sul dispositivo** (17 feature
   abilitate, scadenza 29/06/2028; FireCluster/OSPF-BGP/Multi-WAN/WAN Failover/Link
   Aggregation = *Never*). **Limiti:** una sola tabella letta, scadenze **non verificate
   per seriale**, `Enabled` ≠ servizio applicato. Resta l'estrazione **dal portale** e la
   conferma per ciascun seriale.
2. Stato operativo → **✅ rilevato**: stato cluster, heartbeat, interfacce, porte
   monitorate, indici di salute, memoria (master 93,3% / backup 68,8%), uptime ~49 gg,
   connessioni 908–1.250. **Manca**: tunnel VPN attivi, interfacce WAN e indirizzi
   pubblici, e il **test di failover** (mai eseguito: lo stato corrente non certifica il
   subentro).
3. Esportare la configurazione e salvarla sulla condivisione interna → **⏳ ancora da
   fare** (residuo #12). Il rilievo è stato di sola lettura.
4. Registrazione del residuo già noto (config solo da export manuale, manca
   archiviazione automatica) → **✅ confermato e aggravato**: `Log Server: Not Connected`,
   `Dimension: Not Connected`, `WatchGuard Cloud Management: Disabled` → **nessuna
   centralizzazione log visibile**, da confrontare con l'architettura prevista
   (destinazioni alternative, storico e retention **non verificati**).

**Punti aperti** (elenco completo nel documento di rilievo): memoria master ~93,3%;
`Hostile Sites and Ports: Unmatched` (WatchGuard documenta un problema noto di
visualizzazione senza interruzione del filtraggio, ma la corrispondenza non è verificata);
aggiornamento Fireware da valutare; conferma firmware/scadenze per ciascun seriale;
copertura dei servizi sulle singole policy e ispezione HTTPS/TLS; motivo di `spamBlocker`
**licenziato ma disabilitato**; log/retention; failover da collaudare.

### C1 — Mappa della rete fisica (punto 4.5) — visita in sede

Non risolvibile da remoto. Checklist da portare in sede: armadi e posizione, switch (modello,
porte occupate, uplink), patch panel ed etichette dei cablaggi, punti di accesso Wi-Fi,
gruppi di continuità (modello, carico, autonomia), provenienza dei collegamenti Internet
(modem/router, indirizzi pubblici), planimetria con distanza armadio↔postazione.
Output: `docs/project/mappa-rete-fisica.md` — **non esiste un documento equivalente**, si
crea alla visita, non prima. Da concordare con Agis Lab come primo impegno congiunto.

### A3 — Tenant Microsoft 365 (punto 4.6)

**Perimetro e stato delle conoscenze:** [`inventario-m365-2026-10-12.md`](./inventario-m365-2026-10-12.md).

> **Aggiornamento 12/10 — raccolta EXO e portale fatti in sola lettura** (tre sessioni `-Device` da
> Ubuntu, `app/email-diagnostics/inventory_tenant_m365.ps1` + `_part2.ps1` + `_part3.ps1`, più
> browser `admin.microsoft.com`/Entra con admin di Stefano): **tenant ID, domini, dimensione,
> regole con valori, policy antispam, quarantena, connector (IP), DKIM, matrice licenze,
> abbonamenti/rinnovi, ruoli (Global Admin), MFA/accesso condizionale ed export utenti sono
> misurati** (§1-bis del modulo). **Restano dal portale solo i residui di decisione** (stato
> security defaults, spiegazione del +8, abbonamento EXO Plan 2 scaduto) più **`Boxafe`** e la
> **domanda sui membri del gruppo** di regola blocco. **Sola lettura**, nessuna modifica al tenant.

**Portale `admin.microsoft.com` (browser, admin di Stefano):**

1. **✅ Fatturazione → Licenze — letto il 12/10** (risultati in §1-bis del modulo): Business
   Standard **26/26**, Business Basic **9/2**, Exchange Online Plan 1 **5/3**, Plan 2 **2/3**.
   **26 + 9 = 35** = cross-check esatto con le 35 caselle `SKUAssigned` misurate via EXO.
   **42 assegnazioni su 34 licenze pagate ⇒ +8** (banner Microsoft) da spiegare.
2. **✅ Fatturazione → I tuoi prodotti — letto il 12/10:** 2 conti (MCA/**Esprinet SpA** + MOSA
   VETRONAVIGLIO SRL); rinnovi **Basic 10/08/2027**, **Standard 08/03/2027**; abbonamento
   **Exchange Online Plan 2 SCADUTO il 14/09/2026**. Resta `Storico ordini` per il fornitore
   commerciale (risultato già noto: SB Italia + acquisti diretti dal portale).
3. **✅ Ruoli → Assegnazioni dei ruoli — letto il 12/10** (export CSV): **5 Global Admin** —
   `administrator@`, Stefano Bonfanti, **`admin-itimpresa@`**, **`Admin-Abbiati@`**,
   **`a.viviano@`** ⇒ **3 dei 5 sono account fornitori** (§1-bis del modulo).
4. **✅ MFA / accesso condizionale — letto il 12/10** (Entra): **0 criteri CA** (banner
   «licenze insufficienti» ⇒ niente Entra ID P1/P2), **solo OTP via email** abilitato come
   metodo secondario, MFA non forzata. Resta **`[?]` stato delle security defaults**.
5. **✅ Utenti → Esporta utenti — letto il 12/10:** CSV **83 utenti** (78 attivi, 5 bloccati),
   **cloud-only** (0 `DirSyncEnabled`), password never expires **83/83** (§1-bis).

Da terminale — **residui EXO ✅ tutti eseguiti il 12/10** (`…_part3.ps1`, comandi **già corretti** per questa build; risultati in §1-bis del modulo):

| Residuo | Esito |
|---|---|
| Mappa DKIM → dominio | `vetronaviglio.it` = **`Disabled`/`CnameMissing`**; `.eu` e `.onmicrosoft.com` = `Valid` → **dominio primario non firmato DKIM** |
| Valori condizioni regole | blocco = `NotInOrganization` + gruppo **`deny_outbound_emailsDeny_Outbound_Emails@…`** (testo: *«…il destinatario non è un membro del dominio vetronaviglio.it»*); altre due = reindirizzamenti (Antje→Bettina, silos→f.olivieri) |
| IP relay | `Get-InboundConnector` → **`109.115.188.114`** (un solo IP; diverso dal `109.168.111.201` in SPF) |

**Ancora aperto da EXO:** `Get-DistributionGroupMember -Identity deny_outbound_emailsDeny_Outbound_Emails`
→ **chi è nel gruppo** che non può scrivere all'esterno (utenti reali o solo caselle funzionali?).

**6. Backup del tenant:** `Boxafe` (prodotto Syneto, prodotto nella riga *Backup* di
`fornitori-contratti.md`) è il candidato naturale per il backup Microsoft 365 — **copertura,
retention ed esito dell'ultimo job sono ignoti** e il test di restore è mai fatto.
Chiarirlo con Syneto/IT Impresa: un tenant senza backup verificato è un blocco in offerta.

Per message trace della **mail di prova** del caso A riusare:
`pwsh -NoProfile -File app/email-diagnostics/check_caso_bettina.ps1 -Da <data> -A <data>`.
Risultati → colonna *Licenze* e *Accessi* della riga Microsoft in `fornitori-contratti.md`.

### A4 — Telefonia, stampanti, videosorveglianza, controllo accessi (punto 4.7)

1. **Centralino Alascom:** gli accessi al software di gestione sono disponibili dal 23/09 →
   esportare postazioni, licenze e stato. La manutenzione è terminata: preparare alla
   direzione **due opzioni** (ricontratto di manutenzione vs migrazione/dismissione) con i
   relativi costi — è una decisione loro, non nostra.
2. **Stampanti di rete (4):** per ciascuna aprire la pagina web (`http://<ip>`, credenziali
   da SAPI già in nostro possesso) → modello, seriale, contatore pagine, stato toner. Gli
   IP si leggono dal foglio `Inventory` filtrando `Type = Printer / peripheral`.
3. **Videosorveglianza Hikvision:** dalla console NVR → elenco canali/telecamere, stato
   disco, retention effettiva, errori di registrazione.
4. **Controllo accessi:** il server Axtrax è **spento dal 26/06/2026** su richiesta di
   Abbiati. In autonomia si verifica solo lo stato fisico (alimentazione lettori, cavi);
   la riaccensione o la sostituzione è decisione della direzione → inserirla nelle decisioni
   richieste, non farla.

### A5 — Contratti, scadenze e responsabilità (punto 4.8)

Parte da `docs/project/fornitori-contratti.md` (matrice già impostata, righe 🟡/🔴).
Per ciascun fornitore con contratto mancante: cercare la fattura/passivo in Gmail
(`fattura <fornitore>`) oppure chiedere ad Amministrazione il registro scadenze, e riempire
intestatario, canone, durata, scadenza, rinnovo. Non si inventano valori: se il dato non
c'è, resta «da verificare».

### A6 — Residui con IT Impresa (punto 4.9)

Le credenziali sono già state consegnate il 21/09: la mail serve solo per i tre residui
(1. account amministrativo del NAS non funzionante, 2. backup delle configurazioni degli
switch mai creato, 3. export ricorrente delle configurazioni firewall). Stile e destinatari
da `docs/leads/email-it-impresa-followup.md` (messaggio del 16/09 inviato **a nome di
Bettina**, come richiesto da IT Impresa) — il file storico non va modificato, il nuovo
testo va in un file separato.

### A7 — Credenziali (punto 5)

> Aggiornato 09/10: Bitwarden **non è più previsto**. Canale operativo = file credenziali
> compatto + WeTransfer con link protetto da password, password comunicata telefonicamente
> (stesso schema della consegna dell'08/10, vedi `canale-sicuro-proposta.md`).

1. Aggiornare il file credenziali compatto (`Vetronviglio.docx` o successore) con le
   voci nuove, indicando per ciascun sistema **Titolare** e **Autorizzati**.
2. Comprimere/trasmettere via **WeTransfer con link protetto da password**.
3. Comunicare la password **telefonicamente** al referente nominativo, mai per email.
4. Registrare la consegna in `docs/changelog.md` (data, contenuto, destinatario, canale).
5. Gli aggiornamenti documentali non sensibili (elenco postazioni, matrice fornitori,
   matrice licenze) restano vietati in allegato email: solo canale protetto.

### Chiusura di ogni passo

- Esito e data → `docs/changelog.md`.
- Stato del documento di risposta → `docs/leads/index.md` e `PROJECT_AI_NOTES.md`.
- Invio solo dopo validazione umana (regola della sezione sopra).
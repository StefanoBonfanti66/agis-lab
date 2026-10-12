# Vetronaviglio — Matrice fornitori, contratti, licenze e accessi (Fase 1)

> **Stato:** bozza di lavoro (23/09/2026).
> **Scopo:** censire ciò che lan_inventory NON copre (parco macchine/rete/telefonia/sicurezza già rilevato) — fornitori, contratti, licenze M365, accessi e procedure, oggetto della Fase 1 «Perimetro e recupero» del percorso Agis Lab.
> **Fonte dati di partenza:** Relazione preliminare Agis Lab (04/09/2026); risposte fornitori 16/09 (`docs/leads/agis-lab-risposte.md`); evidenze `.msg` (IT Impresa, Microsoft); contratto Vodafone; **consegna credenziali IT Impresa 17–21/09 (`docs/project/Vetronviglio.docx`, Davide Sala, 14 pp, rev 22)**.
> **Regola:** nessun contatto diretto di Agis Lab con fornitori in uscita/in contenzioso prima dell'handover formalizzato da Vetronaviglio.
> **Sicurezza:** il file Vetronviglio.docx contiene credenziali reali — non riprodurre segreti in altri documenti/email; consegna ad Agis Lab solo tramite canale sicuro concordato.

---

## 1. Matrice perimetro per fornitore

Scheda compilata secondo il modello della Relazione Agis Lab §4 (servizi / contratto / licenze / accessi / responsabilità / referenti / consegne).

| Fornitore | Ambito / servizi | Contratto (intestatario, canone, scadenza, rinnovo) | Licenze (prodotti, q.tà, assegnazioni, portale) | Accessi (account admin, remoti, credenziali) | Stato / azione |
|---|---|---|---|---|---|
| **Abbiati Engineering** | Servizi IT storici; **allarme; videosorveglianza** | IN USCITA — contenzioso legale in corso, non contattabile | Da ricostruire (gestione impianti) | Credenziali da recuperare dai materiali Bonfanti | 🔴 Bloccato: documentazione solo da materiali storici, da validare con posizione legale |
| **IT Impresa** | Server Syneto (2), virtualizzazione VMware, firewall WatchGuard (cluster), switch, QNAP, VM dominio | In uscita — **contratto disponibile, da allegare al riscontro Agis Lab** (23/09); canone/scadenza/SLA in contratto | Portali accessibili ("licenze consultabili dai portali forniti") — **estrarre matrice licenze** | **Consegna ricevuta 21/09** (credenziali apparati, VM, Syneto/ESXi/IPMI, Veeam, switching, hosting, VPN, tenant M365) | 🟢 Accessi consegnati + contratto disponibile. 🔴 Residui: QNAP admin non funzionante; backup config switch **inesistente**; config firewall solo export manuale |
| **Microsoft** | Tenant M365 (configurazione mista: Office perpetue + canone) | **Canali confermati: acquisto da SB Italia + direttamente dal portale** (23/09) — **rinnovi letti 12/10: Basic 10/08/2027, Standard 08/03/2027; EXO Plan 2 SCADUTO 14/09/2026** | **Estratto dal portale 12/10** | **Risolto: Stefano è amministratore** (ticket #2609161420000280) | 🟢 Canale licenze, accesso admin, portale ed EXO **tutti letti**: [`inventario-m365-2026-10-12.md`](./inventario-m365-2026-10-12.md) — Tenant ID `5ce8afa1-…`, 3 domini, 89 destinatari, 35 caselle licenziate, policy `MoveToJmf`, relay on-prem, matrice licenze (42 su 34), **5 Global Admin (3 fornitori)**, **0 criteri CA / solo OTP email**, export 83 utenti cloud-only. Restano: security defaults, spiegazione +8, **`Boxafe`**, membri gruppo blocco |
| **Vodafone** | Connettività (fibra + backup 4G) | Contratto **già trasmesso ad Agis Lab** | — | — | 🟢 Chiuso |
| **SAPI** | Stampanti e consumabili (4 stampanti di rete) | Regolare, in mappa complessiva da inserire | — | Accessi user/password alle stampanti **già disponibili** | 🟢 Operativo |
| **Elabora** | Gestionale Prodware (2 VM, TS Plus palmari) | Da documentare (ruoli e modalità assistenza) | Licenze Prodware da verificare | **Gestione confermata ok** | 🟢 Coordinamento ok. Da verificare solo licenze Prodware |
| **Alcatel / Alascom** | Centralino telefonico fisico | **Manutenzione TERMINATA (non più attiva)** | Stato licenze da verificare | **Accessi al centralino + software di gestione disponibili (23/09)** | 🟡 Accessi risolti; 🔴 resta decisione: ricontratto manutenzione/licenze o dismissione/migrazione |
| **ServerPlan / CMSHigh** | **Hosting web dominio vetronaviglio.eu (cPanel, webmail)** | Contratto/canone/scadenza **da verificare** (nuovo fornitore emerso dalla consegna) | Piano hosting incluso; **webmail @vetronaviglio.eu** | cPanel/FTP/Webmail ricevuti | 🟡 Accessi ricevuti — verificare proprietà/intestatario e canone |
| — (esclusa) | 1 stampante Samsung obsoleta; W2003srv02 / W2008TS01 (dismessi); 1 NAS Buffalo TS-RXL256 (dismesso) | esclusi | — | — | Nota: driver stampante sul server; macchine spente/dismesse |

---

## 2. Gap — informazioni mancanti che lan_inventory non fornisce

| Area | Dato mancante | Fonte prevista | Stato |
|---|---|---|---|
| Contratti fornitori | Intestatario, canone, durata, scadenza, rinnovo per ciascun fornitore | Amministrazione/acquisti (fatture+database) | 🟡 Solo Vodafone disponibile; IT Impresa + hosting + M365 commerciale **da richiedere** |
| Licenze | Matrice prodotti/q.tà/assegnazioni/portale (Windows, Office, M365, Prodware, Syneto, Veeam, WatchGuard) | **Portali ora accessibili** (WatchGuard, Syneto, Veeam, M365, cPanel) | 🟡 Accessi ok — **estrazione non ancora fatta**, salvo **WatchGuard**: lette dalla Feature Key sul dispositivo il 12/10 (**17 feature Enabled, scadenza 29/06/2028, 627 gg residui**) → resta la verifica **per ciascun seriale** e dal portale |
| M365 | Fornitore commerciale, intestatario, scadenza, portale di gestione | **SB Italia (fornitore acquisti) o acquisto diretto portale** + amministrazione | 🟢 Admin risolto (ticket 16/09); canale **confermato** 23/09 (SB Italia + portale); **portale letto 12/10**: **2 conti di fatturazione** (MCA/**Esprinet SpA** per gli EXO + **MOSA VETRONAVIGLIO SRL** per i Business), **rinnovi Basic 10/08/2027 e Standard 08/03/2027**, **abbonamento EXO Plan 2 scaduto 14/09/2026** ⚠. **Matrice licenze 12/10:** **26 Business Standard + 9 Business Basic** (= le 35 caselle misurate via EXO) + **7 licenze Exchange aggiuntive** (Plan 1 ×5, Plan 2 ×2) = **42 assegnazioni su 34 pagate → banner «più assegnate che disponibili»**, da confermare riga per riga in `I tuoi prodotti`. Configurazione mista: M365 dichiarato su tutte le postazioni + Office perpetue preesistenti (1 portatile con Office 2019 da migrare). Vedi [`inventario-m365-2026-10-12.md`](./inventario-m365-2026-10-12.md) |
| Accessi | Elenco admin servizi + modalità consegna credenziali (account nominativi, MFA, tracciamento) | IT Impresa + Microsoft + direzione | 🟡 Ampia parte consegnata (IT Impresa + M365 + **centralino + Wi-Fi/AP 23/09**). Residui: **QNAP admin, allarme/videosorv (Abbiati)** |
| Documentazione tecnica | Syneto, Veeam, QNAP, WatchGuard, VPN, rete, **Wi-Fi/AP**; procedure di ripristino | Materiali Bonfanti (**accesso autorizzato 23/09**) + consegna IT Impresa | 🟡 Convergenza parziale: **mappa VLAN + server + apparati + doc/password Wi-Fi ricevuti**; mancano **procedure ripristino** e dettaglio centralino. **WatchGuard: rilievo console 12/10** (`rilievo-watchguard-2026-10-12.md`) — stato, licenze, servizi e firme noti; mancano **export config**, **test failover** e verifica **log/retention** (`Log Server` e `Dimension` = *Not Connected*) |
| VM e applicazioni | Elenco VM, dipendenze, licenze, applicazioni essenziali | Syneto/ESXi + IT Impresa | 🟢 **Elenco ricevuto e integrato il 12/10** nel modulo [`inventario-syneto-2026-10-12.md`](./inventario-syneto-2026-10-12.md): 9 VM del principale + **5 VM del secondario** (`APP-DEV-01`, `APP-DB-01`, `apps_DISMESSO`, `w2003srv02_DISMESSO`, `W2008TS01_DISMESSO`) + `syneto-os-02`. **IP Veeam chiuso:** `.135` (PDF Bareggio §4 + OUI VMware in scan), `.227` = Axtrax (hostname in scan) → resta solo la conferma in console. |
| Backup | Test restore Veeam/Boxafe mai eseguito; QNAP admin non funzionante (punto singolo) | Veeam (utente backup) + QNAP | 🔴 Test restore mai fatto; **QNAP recupero solo con reset distruttivo**. ⚠ **`Boxafe` è il candidato per il backup Microsoft 365**: copertura del tenant `vetronaviglio.it`, retention ed esito job **ignoti** → da chiarire con Syneto (runbook **A3**, punto 6) |
| Controllo accessi (badge) | Server Axtrax **SPENTO su richiesta Abbiati (26/06/26)** | Da verificare con direzione | 🔴 Badge/controllo accessi non gestito — decidere riaccensione/alternativa |
| Aree non presidiate | Regia complessiva, responsabile servizi per servizio | Direzione | 🔴 In fase di definizione (mandato Fase 0) |

---

## 3. Azioni in corso / da avviare (tracciato)

| # | Azione | Proprietario | Stato |
|---|---|---|---|
| 1 | **Consegna credenziali IT Impresa** (sollecito amministratore) | IT Impresa (Davide Sala) → Stefano | ✅ Ricevuta 21/09 (Vetronviglio.docx) |
| 2 | **Estrarre matrice licenze dai portali** (WatchGuard, Syneto, Veeam, M365, cPanel) | Stefano | ✅ **M365: fatto 12/10** (26 Standard + 9 Basic = 35 caselle; 42 assegnazioni su 34 pagate, banner su over-assignment → spiegato da molteplici abbonamenti sommati: MCA Esprinet + MOSA). **WatchGuard:** Feature Key letta dal dispositivo il 12/10 (17 feature, scadenza 29/06/2028), verifica per seriale e dal portale **da fare**. Syneto, Veeam, cPanel ⏳ (accessi disponibili) |
| 3 | **Ticket Microsoft M365 recupero admin** (#2609161420000280) | Stefano / supporto MS | ✅ Risolto — Stefano amministratore |
| 3b | **Canale licenze M365**: acquisto da **SB Italia** + **direttamente dal portale** (23/09) | Stefano ↔ SB Italia | ✅ Confermato |
| 4 | **Verifica contratto centralino Alascom** | Stefano | ✅ Esito: manutenzione NON attiva. **Accessi centralino + software di gestione ora disponibili (23/09)** |
| 4b | **Gestire centralino scoperto**: ricontrattiare manutenzione/licenze o pianificare dismissione/migrazione | Direzione + Agis Lab | 🔴 Da decidere |
| 5 | Coordinamento Elabora/Prodware (accesso admin gestionale) | Da definire con direzione | ✅ Risolto (Elabora/Prodware ok) |
| 6 | **Recupero materiali storici Bonfanti** da dispositivi/servizi (autorizzazione + perimetro con vertenza) | Direzione → Stefano | ✅ **Autorizzato 23/09** — accesso ai materiali storici ottenuto; da recuperare e inventariare |
| 7 | Modello censimento licenze: chiedere se Agis Lab dispone di un modulo standard | Stefano → Agis Lab | ⏳ Da chiedere (domanda 9 risposte) |
| 8 | **Canale consegna credenziali ad Agis Lab** (documento cifrato, password su canale separato; custode) — il doc IT Impresa va trasferito in sicurezza, MAI via email in chiaro | Stefano → Agis Lab | ✅ **Consegna 08/10/2026** — `Vetronviglio.docx` via **WeTransfer con link protetto da password**, password comunicata **telefonicamente**; ricezione + visualizzazione confermate da Alessandro Viviano. Canale valido per le consegne successive. Bitwarden non è più previsto |
| 9 | Raccordo amministrazione: contratti e fatture per tutti i fornitori (**incluso hosting ServerPlan**; **contratto IT Impresa disponibile da allegare**) | Amministrazione/acquisti | 🔴 Da avviare |
| 10 | Definizione referenti e poteri autorizzativi (Bettina autorizza, Federico coordina) | Direzione | ⏳ Da formalizzare in Fase 0 |
| 11 | **Verifica discrepanze IP consegna IT Impresa** (~~Veeam-VN .227 vs .135~~; Axtrax-VN; host .247/.249 inattivi) | Stefano | 🟡 **Veeam risolto il 12/10** con doppia fonte (PDF Bareggio §4 + scan: `.135` OUI VMware, `.227` hostname `AXTRAX-VN`) → vedi [`inventario-syneto-2026-10-12.md`](./inventario-syneto-2026-10-12.md) §6. Restano **Axtrax-VN** (IP da confermare, VM spenta) e gli **host .247/.249 inattivi**, da verificare con gli accessi |
| 12 | **Backup configurazioni**: avviare export regolare config firewall per file; creare backup config switch (oggi inesistente) | Stefano | ⏳ Da organizzare con Agis Lab — **confermato aperto dal rilievo 12/10** (nessun export automatico; `Log Server`/`Dimension` *Not Connected*, Cloud Management *Disabled*) |
| 13 | **Test restore Veeam/Boxafe** (mai eseguito) | Da pianificare con Agis Lab | 🔴 Da pianificare (Fase 2/3) |
| 14 | **Raccogliere documentazione e password Wi-Fi/AP** (accesso disponibile 23/09) nella matrice | Stefano | 🟡 Accesso ok — da consolidare nel fascicolo consegna |
| 15 | **WatchGuard — punti aperti del rilievo 12/10** (`rilievo-watchguard-2026-10-12.md`): (a) **test di failover** (mai eseguito), (b) **valutazione upgrade Fireware** («Upgrade Available», destinazione non verificata), (c) **memoria master ~93,3%**, (d) `spamBlocker` **licenziato ma disabilitato** (motivo), (e) `Hostile Sites and Ports: Unmatched`, (f) copertura policy + ispezione HTTPS/TLS, (g) conferma firmware/scadenze **per seriale**, (h) archiviazione log/retention | Stefano + Agis Lab | ⏳ Da pianificare (rilievo in sola lettura, nessuna modifica eseguita) |

---

## 4. Open point / rischi

- **Vertenza Abbiati:** nessuno scambio informativo diretto; allarme e videosorveglianza (sicurezza fisica) senza gestione fino a recupero accessi dai materiali storici.
- **Centralino:** contratto Alascom non attivo, ma **accessi al centralino + software di gestione ora disponibili (23/09)** → resta da decidere ricontratto manutenzione/licenze o migrazione/dismissione.
- **QNAP punto singolo:** credenziali admin non funzionanti, solo account backup Veeam; recupero richiederebbe reset distruttivo perdendo la configurazione backup. Dispositivo critico non presidiato a livello amministrativo.
- **Backup mai testati:** nessun restore test su Veeam/Boxafe — da pianificare con priorità.
- **Controllo accessi (badge):** server Axtrax spento su richiesta Abbiati (26/06/26) — impianto non gestito.
- **M365:** accesso admin e **canale licenze risolti (SB Italia + acquisto diretto dal portale, 23/09)** — da monitorare scadenza/rinnovo; da estrarre matrice licenze.
- **WatchGuard (rilievo 12/10/2026, sola lettura):** 2× M290 in FireCluster **operativi e sincronizzati**, licenze **Enabled fino al 29/06/2028**, firme aggiornati. Restano: **test di failover mai eseguito**, **upgrade Fireware da valutare**, **memoria master ~93,3%**, `spamBlocker` **licenziato ma disabilitato**, `Hostile Sites and Ports: Unmatched`, **nessuna centralizzazione log visibile** (`Log Server`/`Dimension` *Not Connected*, Cloud Management *Disabled*). Dettaglio e limiti del rilievo in `rilievo-watchguard-2026-10-12.md`. **Classificazione: rilievo operativo e licenze, non audit di sicurezza.**
- **Documentazione storica:** accesso ai materiali Bonfanti **autorizzato (23/09)** — recupero da pianificare con prioritizzazione (prima server/backup, poi rete, poi storica) e nel rispetto della posizione legale.
- **Smistamento: relay SMTP senza auth sul server Veeam** (per allarmi/stampanti) — verificare esposizione/open relay e restrizione.
- **Inventario non autenticato:** seriali/OS/ruolo applicativo confermabili nella fase autenticata (2/3) — la consegna IT Impresa ora fornisce l'accesso per farlo.

---

## 5. Nota

Questa matrice è l'elenco di lavoro della **Fase 1 — Perimetro e recupero**. La NDA firmata (23/09/2026) sblocca lo scambio di contratti, licenze e credenziali; **la consegna delle credenziali ad Agis Lab avviene esclusivamente da Vetronaviglio via canale sicuro (file protetto, password su canale secondario, no password in chiaro via email)**. **Consegna compiuta l'08/10/2026**: `Vetronviglio.docx` consegnato ad Alessandro Viviano via **WeTransfer con link protetto da password**, password comunicata telefonicamente (ricezione + visualizzazione confermate). In allegato al riscontro: contratto IT Impresa. Prossimo step: validare la matrice in contraddittorio con Agis Lab e chiudere le azioni bloccanti (QNAP, Abbiati, centralino decisione).
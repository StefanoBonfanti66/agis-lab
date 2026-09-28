# Agent rules

- Read PROJECT_AI_NOTES.md before doing major work.
- Prefer small diffs.
- Ask before touching secrets, .env, deployment, infra, auth, billing.
- Follow existing code style.
- Update PROJECT_AI_NOTES.md at meaningful checkpoints.

## OpenCode usage in this template
- Treat this repository as a project-scoped OpenCode workspace.
- Personalize `AGENTS.md` after cloning so the rules match the new project.
- Use `PROJECT_AI_NOTES.md` to track decisions, checkpoints, and pending items across sessions.
- If you use custom commands in your OpenCode setup, document project-specific ones here or in the repository docs.

## Current Focus — 2026-09-28

### Completato
- **NDA Agis Lab sottoscritta da entrambe le Parti.** Copia firmata ricevuta 23/09 e verificata: `docs/project/Accordo_riservatezza_Vetronaviglio_Agis_Lab_firmato.pdf` (scansione TOSHIBA e-STUDIO2525AC, 3 pagine, firme olografe — non è firma digitale). NDA in vigore → si procede con Fase 0/1.
- **Email riscontro NDA inviata a Agis Lab** (bozza su `docs/leads/email-agis-nda-firmato.md`, inviata da Stefano): conferma ricezione/archiviazione NDA, avvio Fase 0/1, allegati LAN Inventory (LAN_Executive_Report.xlsx + LAN_Inventory_Professional.xlsx da `app/lan_inventory/lan_inventory_output/vetronaviglio/`, dati 16/09/2026, 100 host) e reminder modalità consegna credenziali (solo da Vetronaviglio, account nominativi, MFA, tracciamento).
- `docs/leads/index.md` aggiornato con riga `email-agis-nda-firmato.md`.
- Verifica NDA firmata: nessuna email col PDF firmato in Gmail (ricevuto localmente); analisi forense PDF (no firme digitali, solo olografe).
- Lan_inventory analizzato vs esigenze operative Agis Lab: copre inventario parco macchine/rete/telefonia/sicurezza; NON copre contratti fornitori, licenze M365, mappe/config, procedure e credenziali = oggetto Fase 0/1.

### Da fare / ancora aperto
- **In attesa riscontro da Agis Lab** all'email di riscontro NDA (inviata).
- Lan_inventory v1.8.0 + docs + opencode.json committati su `main` il 28/09/2026 dopo revisione (il working tree era rimasto uncommitted dal 16/09). Dati di scansione LAN (NMAP XML, .xlsx, .db) esclusi via `.gitignore`.
- Canale consegna credenziali da concordare con Agis Lab (account nominativi, MFA, tracciamento, no password in chiaro).
- IT Impresa: in attesa riscontro al sollecito (lavoro in corso o blocco).

### Prossimo step concreto
Attendere riscontro Agis Lab; in parallelo preparare la Fase 0/1 (mappatura processi e credenziali) in attesa della conferma di avvio.
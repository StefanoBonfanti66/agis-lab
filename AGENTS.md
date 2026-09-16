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

## Current Focus — 2026-05-25

### Completato
- Diagnosi e fix CI: `@vitejs/plugin-react` aggiornato da `^4.3.4` a `^5.2.0` per compatibilità con Vite 8.x
- Aggiunto header template a `PROJECT_AI_NOTES.md`
- Merge di `fix/template-onboarding-ci` in `main` e push

### Da fare / miglioramenti futuri
- Aggiungere ESLint configurato (segnalato in README come mancante)
- Aggiungere test framework (Vitest/Jest) — segnalato in README come mancante
- Valutare se serve `dependabot.yml` e CodeQL workflow già presente

### Prossimo step concreto
Prima di una nuova sessione: pullare `main`, aprire `PROJECT_AI_NOTES.md`, compilare Obiettivo e Risultato atteso della sessione.

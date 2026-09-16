# Triathlon Starter

Starter repository personale per avviare rapidamente nuovi progetti web con una base moderna già pronta.

## Quando usarlo
Usa questo repository quando vuoi iniziare un nuovo progetto con:
- React 19
- TypeScript
- Vite
- TailwindCSS v4
- Supabase
- Vercel

## Cosa include già
- Bootstrap frontend Vite + React + TypeScript
- Supabase client setup
- GitHub Actions per CI, Deploy, CodeQL e notifiche Telegram
- Guida di bootstrap e file di supporto per sessioni OpenCode

## Cosa non include ancora di default
- ESLint configurato
- Test framework (Vitest/Jest)
- Branding finale del progetto, da personalizzare dopo il clone

## Struttura
- `app/` → applicazione frontend
- `.env.example` → variabili ambiente di esempio
- `AGENTS.md` → istruzioni operative per sessioni AI/OpenCode
- `PROJECT_AI_NOTES.md` → note progetto

## Setup

```bash
cd app
cp ../.env.example .env
npm install
npm run dev
```

## Checklist nuovo progetto
- Rinominare la repo GitHub
- Aggiornare `app/package.json`
- Configurare Supabase
- Configurare Vercel
- Aggiornare `.env`
- Personalizzare `AGENTS.md`
- Aggiornare `PROJECT_AI_NOTES.md`

## Required GitHub Secrets

Questo starter si aspetta i seguenti secret a livello repository per i workflow GitHub Actions inclusi di default:

- `TELEGRAM_BOT_TOKEN`  
  Token del bot Telegram usato per inviare notifiche CI e Deploy.

- `TELEGRAM_CHAT_ID`  
  Chat o canale che riceverà le notifiche Telegram.

- `VERCEL_TOKEN`  
  Token di accesso Vercel usato dal workflow `Deploy`.

- `VERCEL_ORG_ID`  
  Organization id Vercel del progetto di destinazione.

- `VERCEL_PROJECT_ID`  
  Project id Vercel associato alla repo.

Se questi secret mancano, il comportamento dipende dal contesto:
- **Telegram**: i workflow di notifica falliscono (i secret sono dichiarati `required` nel reusable).
- **Vercel**: il workflow `Deploy` salta gli step di produzione senza fallire.
- **CI**: non richiede alcun secret.

## GitHub Actions workflow naming conventions

Questo template riserva i seguenti nomi workflow:

- `CI`  
  Pipeline principale di continuous integration. Triggerata su push (main, develop, feat/*, fix/*) e su tutte le PR.

- `Deploy`  
  Pipeline di deploy production via Vercel CLI. Triggerata su push su main e manualmente via `workflow_dispatch`.

Altri workflow reagiscono a questi nomi tramite `workflow_run`:

- `Telegram CI Notify`  
  Invia un messaggio Telegram quando il workflow `CI` termina.

- `Telegram Deploy Notify`  
  Invia un messaggio Telegram quando il workflow `Deploy` termina.

Se rinomini `CI` o `Deploy`, devi aggiornare anche l'array `workflows` nei workflow Telegram relativi.

## Default GitHub Actions included

Questo starter include di default i seguenti workflow:

- `CI`  
  Pipeline CI Node-aware. Rileva automaticamente la presenza di `package.json` e salta gli step Node se il file non esiste ancora.

- `Deploy`  
  Pipeline di deploy production su Vercel. Parte solo quando:
  - la repo contiene un `package.json`
  - i secret Vercel richiesti sono presenti

- `Telegram CI Notify`  
  Ascolta gli eventi `workflow_run` del workflow `CI` e invia una notifica Telegram al completamento.

- `Telegram Deploy Notify`  
  Ascolta gli eventi `workflow_run` del workflow `Deploy` e invia una notifica Telegram al completamento.

- `Telegram Notify Reusable`  
  Workflow riutilizzabile che centralizza la logica di invio Telegram.

- `CodeQL`  
  Analisi di sicurezza CodeQL di GitHub. Eseguita su push/PR su main e settimanalmente (lunedì 04:00).

- `Lint workflows`  
  Esegue `yamllint` sui file in `.github/workflows` su push, pull request e `workflow_dispatch`.

- `Telegram Test` / `Telegram Test Reusable`  
  Workflow interni usati per validare l'integrazione Telegram.

## Convenzioni
- Branch `main` protetto
- Usare feature branch e PR
- Aprire una sessione con `opencode` e seguire `AGENTS.md`

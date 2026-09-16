# Bootstrap guide

Step-by-step guide to initialize a new project from this starter.

## 1. GitHub — rename the repository

Create the new repo on GitHub (private or public). Clone it locally, then pull the starter:

```bash
git remote add starter https://github.com/StefanoBonfanti66/triathlon-starter.git
git pull starter main --allow-unrelated-histories
git remote remove starter
git push origin main
```

## 2. Local — update package metadata

Edit `app/package.json`:

| Field | Change |
|---|---|
| `name` | `"your-project-name"` |
| `version` | `"0.1.0"` |
| *(optional)* `description` | Short description |

```bash
cd app
cp ../.env.example .env
npm install
npm run dev        # verify it starts
```

## 3. Supabase — create project

1. Go to [supabase.com](https://supabase.com) → **New project**
2. Choose a strong database password, save it in a password manager
3. Once created, go to **Project Settings → API**
4. Copy **Project URL** and **anon public key**
5. Update `app/.env`:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

6. *(optional)* Enable Row Level Security (RLS) on each table you create in the Supabase SQL editor.

## 4. Vercel — connect project

1. Go to [vercel.com](https://vercel.com) → **Add New → Project**
2. Import the GitHub repository
3. Framework preset: **Vite**
4. Root directory: `app`
5. Environment variables (add the same values as `app/.env`):
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
6. Click **Deploy** — Vercel will build and publish the site.

### Vercel project JSON

After the first deploy, link locally (optional — needed only if you want `vercel env pull` locally):

```bash
cd app
npx vercel link
```

The `.vercel/project.json` file is **not committed** (it's in `.gitignore`). The CI workflow reads the project ID and org ID from GitHub Secrets instead.

## 5. GitHub Secrets — configure CI/CD

Go to **Settings → Secrets and variables → Actions → Repository secrets** and add:

| Secret | Value |
|---|---|
| `VERCEL_TOKEN` | From [Vercel Account → Tokens](https://vercel.com/account/tokens) |
| `VERCEL_ORG_ID` | From `.vercel/project.json` after `npx vercel link`, or from Vercel dashboard URL (`team_...`) |
| `VERCEL_PROJECT_ID` | From `.vercel/project.json` after `npx vercel link`, or from Vercel project dashboard URL (`prj_...`) |
| `TELEGRAM_BOT_TOKEN` | Bot token from [@BotFather](https://t.me/botfather) |
| `TELEGRAM_CHAT_ID` | Chat ID where notifications are sent |

**To get `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`:**
```bash
cd app
npx vercel link      # follow prompts
cat .vercel/project.json
```

Or extract from the Vercel project URL: `https://vercel.com/<org-slug>/<project-slug>/...` — but linking locally is more reliable.

## 6. Workflow naming conventions

The workflows follow a naming convention used by `telegram-ci-notify.yml` and `telegram-deploy-notify.yml` in their `workflows:` trigger:

| Workflow file | `name:` value | Referenced by |
|---|---|---|
| `ci.yml` | `CI` | `Telegram CI Notify` |
| `deploy.yml` | `Deploy` | `Telegram Deploy Notify` |
| `codeql.yml` | `CodeQL` | — |
| `telegram-ci-notify.yml` | `Telegram CI Notify` | — |
| `telegram-deploy-notify.yml` | `Telegram Deploy Notify` | — |
| `telegram-notify-reusable.yml` | `Telegram Notify Reusable` | Called by CI/Deploy notify |
| `telegram-test.yml` | `Telegram Test` | — |
| `telegram-test-reusable.yml` | `Telegram Test Reusable` | — |

> If you rename a workflow, update the `workflows: ["..."]` reference in the corresponding `telegram-*-notify.yml`.

## 7. First CI / Deploy — verify

### CI

```bash
git checkout -b feat/init
git add -A
git commit -m "chore: bootstrap from triathlon-starter"
git push origin feat/init
```

1. Open the repo on GitHub → a **CI** run should trigger on the push
2. Wait for CI to complete → **Telegram CI Notify** should fire (if Telegram secrets are set)
3. Open a PR from `feat/init` to `main` → CI runs again on the PR

### Deploy

Merge the PR (or push directly to `main`):

```bash
git checkout main
git merge feat/init
git push origin main
```

1. **CI** runs again on `main`
2. **Deploy** workflow runs → deploys to Vercel
3. **CodeQL** runs (scheduled also weekly)
4. **Telegram Deploy Notify** sends the result

Check the Vercel deployment URL in the workflow logs, or find it in the Vercel dashboard.

## 8. Optional — customize project metadata

| File | What to change |
|---|---|
| `app/index.html` | `<title>`, `<html lang="...">` |
| `app/src/App.tsx` | App content, routes |
| `app/public/favicon.svg` | Favicon |
| `AGENTS.md` | Agent rules for your project |
| `PROJECT_AI_NOTES.md` | Fill out the template |
| `.env.example` | Remove example values, keep variable names |

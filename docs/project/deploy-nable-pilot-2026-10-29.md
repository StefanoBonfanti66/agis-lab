# Deployment agente N-able tramite GPO — test pilota (29/10/2026)

## 1. Obiettivo e perimetro

Distribuire l'agente N-able (servizio Windows: **Advanced Monitoring Agent**) su un ristretto gruppo di piloti tramite Group Policy Object (GPO), con verifica della corretta installazione e del servizio in esecuzione al riavvio del computer.

**Perimetro del pilota:**
- Dominio: `Vetrodom.local`
- Controller di dominio: `DC01-VN.Vetrodom.local`
- GPO: `TEST - Nable - VETRO71-PC`
- Postazioni pilota previste: `VETRO71-PC`, `VETRO53-PC`
- Limite: la distribuzione resta limitata ai due piloti. Non è stata autorizzata né documentata un'estensione generale.

**Fuori scope (documentato per chiarezza):**
- L'antivirus verrà installato in una fase successiva e **non fa parte di questa fase**.
- La presenza dell'agente di monitoraggio non va confusa con la presenza di protezione antivirus.
- Non è stata verificata la registrazione o la connettività alla console del fornitore.

## 2. Ambiente e componenti

| Elemento | Dettaglio |
|---|---|
| Percorso cartella Startup della GPO | `\\DC01-VN.Vetrodom.local\SYSVOL\Vetrodom.local\Policies\{GUID-GPO}\Machine\Scripts\Startup` |
| GUID della GPO | Segnaposto esplicito: non disponibile nelle evidenze fornite (recuperarlo solo se già documentato nel repository) |
| File nella cartella Startup | `InstallaNable.cmd` (176 byte), `InstallaNable.ps1` (2118 byte), `NableAgent.exe` (4.429.368 byte) |
| Percorso di lavoro locale sul client | `C:\ProgramData\DeployNable` |
| Log locale | `C:\ProgramData\DeployNable\install.log` |
| Backup GPO | `Backup-GPO` eseguito con destinazione `C:\BackupGPO` sul controller prima dell'aggiornamento degli script. ID o percorso della singola istanza di backup non disponibili in questa conversazione. |
| Impostazione GPO applicata | Chiave `HKLM\Software\Policies\Microsoft\Windows NT\CurrentVersion\Winlogon`, valore `SyncForegroundPolicy`, tipo `DWORD`, valore `1` |

**Nota:** nessuna altra impostazione GPO, filtro di sicurezza o collegamento a OU è dichiarata configurata se non verificabile nel repository. La limitazione ai nomi computer è implementata nello script, non in un filtro di sicurezza GPO (non documentato).

## 3. Cronologia delle attività (29/10/2026)

Tutte le evidenze sotto riguardano `VETRO53-PC`. Non attribuire a `VETRO71-PC` risultati che non sono documentati.

| Ora | Evento |
|---|---|
| 29/10/2026 15:19:24 | Ultimo avvio di `VETRO53-PC` |
| 15:19:38,74 | Avvio distribuzione (primo test dopo riavvio) |
| 15:19:41,02 | `ExitCode=0`, 1 file copiato |
| (15:19:xx) | Servizio presente con `StartType Automatic`, ma `Status Stopped` |
| (successivo, manuale) | Avvio manuale del servizio da PowerShell remoto → `Status Running`, `StartType Automatic` |
| (post-avvio manuale) | Aggiornata la logica dello script per gestire automaticamente il servizio dopo l'installazione |
| 29/10/2026 15:23:54 | Ultimo avvio di `VETRO53-PC` (test con agente già presente) |
| 15:24:10 | `Agente gia presente: installazione saltata.` |
| 15:24:20 | `VERIFICA LOCALE OK: servizio Running, avvio Automatic.` |
| (controllo successivo) | `Running / Automatic` |
| (precedente, metodo non documentato) | Disinstallazione dell'agente da `VETRO53-PC` per testare la reinstallazione |
| (prima del riavvio) | Controllo remoto: `Servizio agente assente: pronto per il test di reinstallazione.` |
| 29/10/2026 15:42:04 | Ultimo avvio di `VETRO53-PC` (test completo di reinstallazione automatica) |
| 15:42:20 | `Avvio distribuzione.` |
| 15:42:38 | `ExitCode installer=0` |
| 15:42:48 | `VERIFICA LOCALE OK: servizio Running, avvio Automatic.` |
| (controllo successivo) | `Running / Automatic` |

Il flusso locale ha raggiunto la verifica positiva circa 44 secondi dopo l'avvio del PC, senza avvio manuale del servizio.

## 4. Architettura del flusso

`GPO (Startup)` → `InstallaNable.cmd` → `InstallaNable.ps1` → `NableAgent.exe` → verifica servizio `Advanced Monitoring Agent`

### 4.1 Wrapper CMD (`InstallaNable.cmd`)

Già registrato come script di avvio della GPO. Contenuto:

```
@echo off
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0InstallaNable.ps1"
exit /b %ERRORLEVEL%
```

La registrazione preesistente del CMD come script di avvio è stata mantenuta; non è stato necessario modificare nuovamente `scripts.ini` (contenuto non ricostruito perché non disponibile).

### 4.2 Script PowerShell (`InstallaNable.ps1`)

Comportamento effettivamente implementato (descrizione, non dichiarazione di copia esatta del file):

- `$ErrorActionPreference = "Stop"`.
- Esce con codice 0 sui computer diversi da `VETRO71-PC` e `VETRO53-PC`.
- Crea `C:\ProgramData\DeployNable` se necessario.
- Scrive messaggi con timestamp nel file `install.log`.
- Cerca il servizio `"Advanced Monitoring Agent"`.
- Se il servizio esiste → salta l'installazione.
- Se il servizio manca:
  1. registra `"Avvio distribuzione."`;
  2. copia `NableAgent.exe` da `$PSScriptRoot` nella cartella locale `C:\ProgramData\DeployNable`;
  3. esegue `Start-Process -FilePath $Exe -Wait -PassThru`, senza argomenti aggiuntivi;
  4. registra l'`ExitCode` dell'installer;
  5. attende fino a circa 120 secondi la comparsa del servizio, controllando ogni 5 secondi;
  6. genera un errore se il servizio non compare.
- Imposta il servizio con `Set-Service -StartupType Automatic`.
- Se lo stato è `Stopped`:
  - registra `"Avvio del servizio agente."`;
  - esegue `Start-Service`.
- Attende `Running` con `WaitForStatus` e timeout di 60 secondi.
- Attende altri 10 secondi, aggiorna lo stato e verifica che sia ancora `Running`.
- Registra `"VERIFICA LOCALE OK: servizio Running, avvio Automatic."` ed esce con 0.
- Nel `catch` registra il messaggio di errore ed esce con 1.

### 4.3 Log consolidato (da conservare come evidenza)

```
[29/10/2026 15:19:38,74] Avvio distribuzione
        1 file copiati.
[29/10/2026 15:19:41,02] ExitCode=0
[2026-10-29 15:24:10] Agente gia presente: installazione saltata.
[2026-10-29 15:24:20] VERIFICA LOCALE OK: servizio Running, avvio Automatic.
[2026-10-29 15:42:20] Avvio distribuzione.
[2026-10-29 15:42:38] ExitCode installer=0
[2026-10-29 15:42:48] VERIFICA LOCALE OK: servizio Running, avvio Automatic.
```

## 5. Runbook di verifica

### 5.1 Riavvio del pilota (Windows PowerShell sul controller)

La variabile `$Cred` contiene credenziali già predisposte nella sessione; non includere credenziali reali.

```powershell
Restart-Computer -ComputerName "VETRO53-PC" `
    -Credential $Cred `
    -Protocol WSMan `
    -Wait -For PowerShell `
    -Timeout 300 -Delay 5 `
    -ErrorAction Stop
```

**Nota:** il ritorno della disponibilità PowerShell non certifica il completamento dell'installer. Prima di un riavvio, verificare che non ci siano lavori aperti sul pilota.

### 5.2 Verifica remota

```powershell
Invoke-Command -ComputerName "VETRO53-PC" -Credential $Cred -ScriptBlock {
    "--- ULTIMO AVVIO ---"
    Get-CimInstance Win32_OperatingSystem |
        Select-Object CSName, LastBootUpTime

    "--- LOG INSTALLAZIONE ---"
    Get-Content "C:\ProgramData\DeployNable\install.log" -Tail 25

    "--- SERVIZIO AGENTE ---"
    $Servizio = Get-Service -Name "Advanced Monitoring Agent" `
        -ErrorAction SilentlyContinue

    if ($Servizio) {
        $Servizio | Select-Object Name, Status, StartType
    }
    else {
        "Servizio agente ancora assente."
    }
}
```

Esito atteso: `Name = Advanced Monitoring Agent`, `Status = Running`, `StartType = Automatic`.

## 6. Evidenze e risultati

### Test superati
1. Primo test dopo riavvio: `ExitCode=0`, servizio installato con `StartType Automatic` (inizialmente `Stopped`, poi avviato manualmente).
2. Test al riavvio con agente già presente: installazione saltata, servizio `Running / Automatic`.
3. Test completo di reinstallazione automatica (dopo disinstallazione): `ExitCode installer=0`, servizio `Running / Automatic` raggiunto senza avvio manuale, circa 44 secondi dopo l'avvio del PC.

### Stato all'ultima verifica
- `VETRO53-PC`: servizio `Advanced Monitoring Agent` → `Running / Automatic`.
- Test locale di reinstallazione automatica: **superato**.
- Test al riavvio con agente già presente: **superato**.
- Verifica del fornitore sulla presenza e attività di `VETRO53-PC` in console: **richiesta e in attesa di conferma**.

### Non verificato in questa fase
- Registrazione o connettività alla console del fornitore.
- Installazione antivirus (fuori scope).
- Ramificazione correttiva `Start-Service` dello script aggiornato (non esercitata nei test automatici positivi; il servizio era già avviato al momento del controllo).
- Il controllo che evita la reinstallazione si basa sulla presenza del servizio, non su verifica di versione o integrità.

## 7. Limiti e aspetti non verificati

- Il controllo che evita la reinstallazione si basa sulla presenza del servizio, non su una verifica di versione o integrità dell'agente.
- L'`ExitCode` dell'installer viene registrato, ma lo script descritto non interrompe esplicitamente il flusso sulla base di un `ExitCode` diverso da zero.
- `Start-Process -Wait` non ha un timeout esplicito: se l'installer resta bloccato, la verifica successiva non viene raggiunta.
- Nei due test automatici positivi non compare la riga `"Avvio del servizio agente."`: il servizio era già avviato al momento del controllo.
- È verificato il risultato automatico complessivo, ma non risulta esercitato in questi test il ramo correttivo `Start-Service` del nuovo script.
- L'avvio manuale precedente ha funzionato, ma non equivale a un test del ramo correttivo del nuovo script.
- La verifica locale non dimostra la registrazione o la connettività alla console del fornitore.
- Non è stata verificata in questa fase alcuna installazione antivirus.

## 8. Stato attuale e prossimi passi

**Stato attuale:**
- Test pilota su `VETRO53-PC` completato con esito positivo (reinstallazione automatica al riavvio).
- Servizio all'ultima verifica: `Running / Automatic`.
- Distribuzione limitata ai due piloti (`VETRO71-PC`, `VETRO53-PC`); nessuna estensione generale autorizzata.

**Prossimi passi:**
1. Attendere la conferma del fornitore sulla presenza e attività di `VETRO53-PC` in console.
2. Valutare, solo dopo tale conferma, un'estensione oltre i due piloti (non ancora autorizzata).
3. Registrare l'esito in `docs/changelog.md` e `PROJECT_AI_NOTES.md` al completamento di ogni milestone.
4. Nessuna modifica a GPO, servizi o configurazioni remote è stata eseguita in questa fase di documentazione.

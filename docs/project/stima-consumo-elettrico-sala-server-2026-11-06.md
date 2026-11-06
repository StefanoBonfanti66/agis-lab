# Stima del consumo elettrico della sala server — 06/11/2026

**Stato:** stima documentale **ricalibrata con una misurazione reale** (IPMI del server primario) e con dati di carico letti in console.
**Scopo:** dimensionare l'ordine di grandezza del consumo elettrico della sala server che ospita l'infrastruttura Syneto/ESXi/Veeam/QNAP.
**Metodo:** (1) stima per classe di apparato dalle specifiche documentate; (2) **misura reale** del consumo elettrico del server ESXi primario via IPMI/BMC; (3) lettura in sola lettura della console SynetoOS per il carico; (4) stima residua per gli altri apparati, con PUE ipotizzato.
**Data:** 06/11/2026 · **Evidenze:** `[M]` misurato in console/IPMI · `[D]` documentale · `[S]` stima.

> ⚠ Restano **non misurati**: server secondario, NAS QNAP, WatchGuard, switch e il PUE reale della sala. I valori residui sono stime con incertezza ±40–50%. Questo documento **non** sostituisce una misura ai fini di fatturazione o di dimensionamento UPS.

---

## 1. Perimetro considerato

| ID | Apparato | Identificazione | Collocazione | Evidenza |
|---|---|---|---|---|
| A1 | **Server ESXi primario** (chassis completo: CPU, RAM, dischi, SynetoOS, VM ospitate) | `HYPER 3000-G3`, ser. `SY2000000281`, Xeon 4210R, ~191 GB RAM, 13 dischi | `192.168.24.125` (BMC `192.168.24.127`) | `[M]` consumo misurato via IPMI |
| A2 | Server ESXi secondario (chassis completo) | `HYPER 2000-G3`, ser. `SY2000000282`, ~128 GB RAM, pool `hybrid` degradato | `192.168.24.128` | `[S]` stima |
| A3 | SynetoOS (primario) | Appliance/VM Hyper 4.7.9.4550 su hypervisor locale | `192.168.24.126` | `[M]` **conta dentro A1** |
| A4 | SynetoFileRecovery (secondario) | Servizio recovery su hypervisor secondario | `192.168.24.129` | `[M]` **conta dentro A2** |
| A5 | NAS QNAP (repository Veeam) | QNAP, `\\192.168.24.244\veeambk`, ~2,3 TB | `192.168.24.244` | `[S]` stima |
| A6 | Server di backup Veeam | `VEEAM-VN`, VBR 12.2.0.334, WS2019 (macchina virtuale su hypervisor VMware) | `192.168.24.135` | `[M]` **conta dentro A1/A2** |
| A7 | Firewall | 2× WatchGuard Firebox M290 in FireCluster | `192.168.24.254` | `[S]` stima |
| A8 | Switch di rete | HP + Enterasys | `.247`, `.249` | `[S]` stima |
| A9 | Accessori / rack / cablaggio | PDU, cavi, patch panel | sala server | `[S]` stima |
| A10 | BMC/IPMI dei server | SuperMicro/ATEN su A1; secondario non raggiungibile | `.127` / secondario sconosciuto | `[M]`/`[S]` |
| — | DC01-VN / DC02-VN | domain controller: **2 VM VMware ospitate sul chassis Syneto primario** (OUI VMware; `inventario-syneto` §3, §11.3) | dentro A1 | `[M]` **conta dentro A1** |

**Correzione rispetto alla prima stima (06/11):** SynetoOS/SynetoFileRecovery, il server Veeam e i domain controller **DC01-VN/DC02-VN** **non sono apparati separati a scaffale**: sono funzioni/VM ospitate sui due chassis ESXi. Il loro consumo è **già dentro A1 e A2** → sono state eliminate dal totale per evitare doppio conteggio. In sala server restano quindi, come apparati fisici, **i due chassis Syneto, il QNAP, i due firewall, i due switch e accessori/rack**; i domain controller non sono un carico aggiuntivo e non hanno una collocazione fisica separata.

---

## 2. Tabella di stima per apparato (ricalibrata)

| ID | Apparato | Potenza IT (min) | Potenza IT (max) | Base |
|---|---|---|---|---|
| A1 | **Server ESXi primario (misurato)** | **0,185 kW** | **0,222 kW** | `[M]` IPMI: media 7 gg **194 W**, media 24 h 194 W, media 1 h 197 W; min 7 gg 179 W, max 7 gg 222 W; corrente 201 W; storico max 280 W (24/08/2026) |
| A2 | Server ESXi secondario | 0,10 kW | 0,16 kW | `[S]` stessa famiglia di A1, RAM 128 GB (≈2/3), storage ridotto e pool degradato (3,6 TB rimossa → lavoro sufficiente a far salire il consumo dischi) |
| A3/A4 | SynetoOS + SynetoFileRecovery | — | — | `[M]` **non sommati**: già dentro A1/A2 |
| A5 | NAS QNAP (repository Veeam) | 0,12 kW | 0,25 kW | `[S]` dischi in scrittura continua (job Veeam + copia offsite giornaliera); 4–6 unità con ridondanza |
| A6 | VEEAM-VN | — | — | `[M]` **non sommato**: VM su hypervisor VMware → dentro A1/A2 |
| A7 | 2× WatchGuard M290 | 0,08 kW | 0,15 kW | `[S]` throughput non critico (908–1.250 connessioni dichiarate) |
| A8 | 2× switch (HP + Enterasys) | 0,10 kW | 0,18 kW | `[S]` access layer 48 porte 10 Gb + core 24 porte |
| A9 | Accessori/rack/cablaggio | 0,03 kW | 0,08 kW | `[S]` PDU, cavi, patch panel, illuminazione rack |
| A10 | BMC/IPMI | — | — | `[M]` **non sommato**: il consumo del BMC è già dentro la misura A1; per A2 resta `[S]` ≈ 0,02–0,04 kW |

### Totale carico IT

```
min = 0,185 (A1) + 0,10 (A2) + 0,12 (A5) + 0,08 (A7) + 0,10 (A8) + 0,03 (A9) = 0,615 kW
max = 0,222 (A1) + 0,16  (A2) + 0,25 (A5) + 0,15 (A7) + 0,18 (A8) + 0,08 (A9) = 1,042 kW
```

**Carico IT: 0,615 – 1,042 kW** (scenario medio ≈ 0,83 kW).

Confronto con la stima preliminare (1,15–2,05 kW): la revisione al ribasso deriva da (a) eliminazione del doppio conteggio delle VM/appliance, (b) misura reale del server primario (194 W, contro 300–500 W stimati).

---

## 3. Dal carico IT alla potenza prelevata (PUE)

```
Potenza prelevata = Potenza IT × PUE
```

| PUE | min (0,615 kW) | medio (0,83 kW) | max (1,042 kW) |
|---|---|---|---|
| 1,20 | 0,74 kW | 1,00 kW | 1,25 kW |
| **1,40 (assunto)** | **0,86 kW** | **1,16 kW** | **1,46 kW** |
| 1,60 | 0,98 kW | 1,33 kW | 1,67 kW |

**Intervallo complessivo: 0,74 – 1,67 kW prelevati dalla rete** (scenario centrale ≈ 1,16 kW).

Il PUE resta il fattore più incerto: con la sola misura del server primario non è possibile separare il consumo di climatizzazione/illuminazione della sala.

---

## 4. Calcolo annuo e costo

```
Energia annua (kWh) = Potenza media (kW) × 8.760 h/anno
Costo annuo (€) = Energia annua (kWh) × tariffa (€/kWh)
```

| Scenario | P media | Energia annua | @0,20 €/kWh | @0,25 €/kWh | @0,30 €/kWh |
|---|---|---|---|---|---|
| Minimo (IT 0,615 kW × PUE 1,20) | 0,74 kW | 6.465 kWh ≈ 6,5 MWh | ≈ 1.290 € | ≈ 1.620 € | ≈ 1.940 € |
| **Centrale (IT 0,83 kW × PUE 1,40)** | **1,16 kW** | **10.174 kWh ≈ 10,2 MWh** | **≈ 2.030 €** | **≈ 2.540 €** | **≈ 3.050 €** |
| Massimo (IT 1,042 kW × PUE 1,60) | 1,67 kW | 14.603 kWh ≈ 14,6 MWh | ≈ 2.920 € | ≈ 3.650 € | ≈ 4.380 € |

**Sintesi:** **6,5 – 14,6 MWh/anno**, circa **1.300 – 4.400 €/anno** a 0,20–0,30 €/kWh; scenario centrale **≈ 10,2 MWh/anno e ≈ 2.540 €/anno a 0,25 €/kWh**.

I domain controller **DC01-VN/DC02-VN sono VM ospitate sul chassis primario** → nessun carico aggiuntivo in sala (già dentro A1). Non è previsto alcun addizionamento per DC.

**Correzione con dati futuri:**

```
E_annuale_reale = E_annuale_stimata × (Potenza_media_reale / 0,83 kW) × (PUE_reale / 1,40)
```

---

## 5. Sensibilità

| Variabile | Effetto | Stato |
|---|---|---|
| Consumo del server secondario (A2) | ±0,06 kW → ±6% | da misurare (BMC secondario non raggiungibile) |
| NAS QNAP (A5) | ±0,13 kW → ±15% | da misurare (SNMP 161 chiuso, serve abilitazione o misura al banco) |
| PUE reale | 1,20 → 1,60 = **+33%** | incognita principale |
| DC01/DC02 | nessun impatto: sono VM dentro A1 | risolto 06/11 |
| Climatizzazione | determina il PUE | — |
| Pool `hybrid` degradato (disco guasto) | consumo dischi sul secondario | da misurare |

---

## 6. Dati reali raccolti il 06/11/2026 `[M]`

### 6.1 IPMI/BMC del server primario — `192.168.24.127` (IPMI-SYNETO01, Supermicro/ATEN)

Accesso in sola lettura (sessione `ADMIN`), pagine **Power Consumption**, **Power Source**, **Sensor Readings**.

| Metrica | Valore |
|---|---|
| **Current Power Consumption** | **201 W** |
| Media ultima ora | 197 W |
| Media ultime 24 h | 194 W |
| Media ultimi 7 giorni | **194 W** |
| Minimo 1 h / 24 h / 7 gg | 190 W (06/11 10:47:03) / 185 W (06/11 10:31:19) / 179 W (02/11 20:04:08) |
| Massimo 1 h / 24 h / 7 gg | 205 W (06/11 10:56:53) / 203 W (06/11 10:00:50) / 222 W (04/11 01:13:31) |
| Highest Peak storico | 280 W (24/08/2026 10:05:57) |
| Lowest Peak storico | 0 W (24/08/2026 09:45:15) → coerente con un riavvio |
| Batteria (BBP) | **assente** → runtime residuo 0 s |

Alimentatori (coerenza con la misura: 109 W + 92 W = **201 W**):

| Slot | Stato | AC input | DC output | Temperature | Fan | Seriale |
|---|---|---|---|---|---|---|
| 1 | PS OK | 236 V, 0,515 A → **109 W** | 12 V, 7,25 A → 87 W | 35 °C / 48 °C | 2496 / 3360 RPM | `P9212CJ04TT2373` |
| 2 | PS OK | 238 V, 0,421 A → **92 W** | 12 V, 5,625 A → 68 W | 33 °C / 52 °C | 2432 / 3360 RPM | `P9212CJ04TT2372` |

Sensori: CPU1 45 °C · PCH 42 °C · System 28 °C · Peripheral 48 °C · MB_10G 55 °C · VRM CPU1 41 °C · VRM P1ABC/P1DEF 38 °C · DIMM A1 37 °C, B1 38 °C, C1 38 °C · ventole 2900 / 2900 / 3000 RPM · tensioni (12V, 5V, 3,3V, Vcpu1, VDIMM) normali · entrambi gli alimentatori presenti · Chassis Intrusion OK. CPU2, VRM2 e il banco DIMM P2 risultano **non presenti** (server a singolo socket con 3 moduli).

### 6.2 Console SynetoOS primario — `192.168.24.126` (Hyper 4.7.9.4550, ESXi 8.0.3.24784735)

| Metrica | Valore |
|---|---|
| CPU (hypervisor locale) | **28,08%** usato (6,739 GHz su 24 GHz) |
| Memoria | **85,01%** usata (174,04 GB su 204,72 GB) |
| Pool `hybrid` | 7,72 TB totali, **40,4%** usati (3,12 TB), ridondanza mirror, ONLINE, scrub concluso 31/10/2026 con 0 errori, prossimo 27/11/2026 |
| Dischi | **13 green**, 0 fault, 0 warning |
| Prestazioni storage | 182 IOPS (20 read / 162 write), 6,52 MB/s (2,08 read / 4,14 write), latenza media 1,1 ms |
| Cache | 30,7 GB, hit rate 94,9% |
| Dati | snapshot 751,4 GB · repliche 173,6 GB · primary data 1,9 TB |
| VM ospitate | 7 (6 ON, 1 OFF), 992,3 GB di spazio risparmiato · 9 VM/36 vhost green |

**La console SynetoOS non espone watt, corrente o tensione**: verificato su dashboard, `/cake/system/details.json` e nella pagina Analytics (le categorie disponibili sono System / Network / Drive / Pool / Dataset; nessuna metrica energetica). Pertanto **l'unico dato elettrico reale disponibile** è quello IPMI di A1.

### 6.3 Dati non disponibili (verificati il 06/11)

| Oggetto | Esito |
|---|---|
| BMC del server secondario | Il banner di `192.168.24.128` dichiara IPMI `192.168.24.130`. Il conflitto ARP con la VM `APP-DB-01` (che aveva `.130` hardcoded) è **risolto il 06/11/2026**: la VM è stata spostata a `192.168.24.132` (stack Supabase ricreato e verificato: 8000/5432 open, `/storage/v1/status` 200). **`.130` ora è libero ma non risponde**: nessuna ARP, ping 100% loss, tutte le porte (22/80/443/5900/8080/8443) filtered; la scansione TCP 443 dell'intera `192.168.24.0/24` non mostra altri dispositivi con login IPMI ATEN oltre `.127` (BMC del primario) → **probabile problema di cablaggio/porta o IP del BMC su altra VLAN: IP reale sconosciuto**, da risolvere con verifica fisica in sala |
| SNMP sul QNAP `.244` | porta 161 **chiusa** (443 e 8080 aperte, web con login) → telemetria non disponibile senza abilitazione SNMP |
| ESXi (entrambi) | espone solo stato di alimentazione delle VM, **nessun watt** |
| UPS / PDU | **non censiti** (nessun dato); "No Battery in the system" sul server primario ⇒ nessuna batteria di backup a livello server |
| PUE della sala | non misurabile senza misura del circuito di climatizzazione/illuminazione |

---

## 7. Piano per completare la misura

| Priorità | Azione | Dato | Stato |
|---|---|---|---|
| 1 | **Misura del server secondario** (BMC non raggiungibile: `.130` libero e muto dopo lo spostamento di APP-DB-01 a `.132` → verifica fisica di cavi/porta in sala, poi IP reale con Agis/Syneto) | watt medi | aperto |
| 2 | **Misura del QNAP** (abilitare SNMP 161 o wattmetro) | watt per banco dischi | aperto |
| 3 | **Censimento UPS/PDU e schema di distribuzione** (con elettricista) | continuità + PUE + presenza DC (nel senso di alimentazione) | aperto |
| 4 | **Wattmetro/PDU al banco** su 24–72 h | potenza reale per rack | aperto |
| 5 | Misura di WatchGuard/switch (bassa priorità: ≤0,33 kW stimati) | watt | opzionale |

> ⚠ Il rilievo dell'impianto elettrico richiede un professionista abilitato. Nessuna attività su UPS, PDU o quadro elettrico senza presenza e responsabilità dell'elettricista. Segnalato inoltre (13/10) un **impianto elettrico modificato a insaputa** → da verificare.

---

## 8. Limiti

1. **Una sola misura reale** (server primario): il 58% del carico IT stimato resta non misurato.
2. **PUE ipotizzato (1,40)**: la sola sala server può avere PUE più basso (climatizzazione dedicata) o più alto (carico condiviso).
3. **Collocazione fisica non confermata** per WatchGuard e switch; UPS/PDU non censiti. I domain controller **DC01-VN/DC02-VN sono VM** ospitate sul chassis primario (dentro A1) e non costituiscono un carico né una collocazione separata.
4. **Consumo medio ≠ consumo di picco**: per UPS e dimensionamento elettrico servono i picchi (max 7 gg sul primario: 222 W; picco storico 280 W).
5. **Tariffa ipotizzata** (0,20–0,30 €/kWh), senza fasce orarie né oneri di potenza.
6. **Carichi variabili**: job Veeam, repliche Syneto, snapshot e scrub del pool fanno oscillare il consumo.
7. La misura IPMI riflette il **chassis completo** del server primario: non è possibile attribuirla a singole VM.

---

## 9. Riferimenti

- `docs/project/inventario-syneto-2026-10-12.md` — host ESXi, SynetoOS, VM ospitate, pool degradato (§10–§11)
- `docs/project/inventario-veeam-2026-10-13.md` — server VBR, repository QNAP, job e copy offsite
- `docs/project/rilievo-watchguard-2026-10-12.md` — 2× Firebox M290 in FireCluster
- `docs/project/runbook.md` — B1 (server/Syneto), B2 (backup/restore), B3 (WatchGuard)
- `docs/project/fornitori-contratti.md` — fornitori, licenze, azioni aperte

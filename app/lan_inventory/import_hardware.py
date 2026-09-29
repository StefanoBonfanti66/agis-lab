#!/usr/bin/env python3
"""Importa i JSON raccolti da collect_hardware.ps1 e produce il
foglio Excel con le specifiche del parco (PC + notebook).

Non richiede alcuna credenziale: legge solo la cartella sulla share.
"""

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

PS_DATE = re.compile(r"Date\((-?\d+)\)")

COLUMNS = [
    ("computer_name", "Hostname"),
    ("device_type", "Tipo"),
    ("ip", "IP"),
    ("manufacturer", "Produttore"),
    ("model", "Modello"),
    ("serial_number", "Numero seriale"),
    ("cpu_name", "Processore"),
    ("cpu_cores", "Core"),
    ("cpu_threads", "Thread"),
    ("ram_total_gb", "RAM GB"),
    ("ram_slots_used", "Slot RAM usati"),
    ("ram_slots_total", "Slot RAM totali"),
    ("ram_modules_gb", "Moduli RAM"),
    ("video_controllers", "Scheda video"),
    ("os_caption", "Sistema operativo"),
    ("os_build", "Build"),
    ("os_install_date", "Installato il"),
    ("monitors", "Monitor"),
    ("antivirus", "Antivirus"),
    ("collected_at", "Raccolto il"),
]


def ps_date(value) -> str:
    """Le date CIM serializzate da PowerShell 5.1 arrivano come /Date(...)/."""
    if not isinstance(value, str):
        return value or ""
    match = PS_DATE.search(value)
    if not match:
        return value
    return datetime.fromtimestamp(int(match.group(1)) / 1000).strftime("%Y-%m-%d")


def nic_ips(nic: dict) -> list:
    """Il collector del progetto usa IPAddress, il template generico IPv4."""
    return nic.get("IPAddress") or nic.get("IPv4") or []


def nic_mac(nic: dict) -> str:
    return nic.get("MACAddress") or ""


def pick_ip(nics: list) -> str:
    """Prima IPv4 utilizzabile, evitando adattatori virtuali e link-local."""
    fallback = ""
    for nic in nics:
        for ip in nic_ips(nic):
            if not isinstance(ip, str):
                continue
            if ip.startswith("127.") or ip.startswith("169.254.") or ":" in ip:
                continue
            if nic.get("virtual") or nic.get("Virtual"):
                fallback = fallback or ip
                continue
            return ip
    return fallback


def read_payloads(input_dir: Path) -> list[dict]:
    payloads = []
    for path in sorted(input_dir.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8-sig")))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  ! {path.name}: {exc}")
    return payloads


def read_records(input_dir: Path) -> list[dict]:
    return [to_record(data) for data in read_payloads(input_dir)]


def to_record(data: dict) -> dict:
    """Un record per JSON. Accetta sia il collector del progetto sia il
    template generico, che nominano i campi in modo leggermente diverso."""
    record = {
        "computer_name": data.get("computer_name", ""),
        "device_type": data.get("device_type", ""),
        "ip": pick_ip(data.get("network") or []),
        "manufacturer": data.get("manufacturer", ""),
        "model": data.get("model", ""),
        "serial_number": data.get("serial_number", ""),
        "cpu_name": (data.get("cpu_name") or "").strip(),
        "cpu_cores": data.get("cpu_cores", ""),
        "cpu_threads": data.get("cpu_threads", ""),
        "ram_total_gb": data.get("ram_total_gb", ""),
        "ram_slots_used": data.get("ram_slots_used", ""),
        "ram_slots_total": data.get("ram_slots_total", ""),
        "ram_modules_gb": data.get("ram_modules_gb", ""),
        "video_controllers": " | ".join(data.get("video_controllers") or []),
        "os_caption": data.get("os_caption", ""),
        "os_build": data.get("os_build", ""),
        "os_install_date": ps_date(data.get("os_install_date")),
        "monitors": " | ".join(data.get("monitors") or []),
        "antivirus": " | ".join(
            a.get("displayName", "") for a in (data.get("antivirus") or [])
        ),
        "collected_at": ps_date(
            data.get("collected_at") or data.get("collected_at_utc")
        ),
    }
    return {key: record.get(key, "") for key, _ in COLUMNS}


WORKBOOK_SHEETS = {
    "Windows Inventory": [
        "IP", "Hostname", "Computer name", "Domain", "Manufacturer", "Model",
        "Serial", "BIOS", "OS", "Version", "Build", "CPU", "Cores", "Threads",
        "RAM GB", "Install date", "Last boot", "Status", "Error", "Collected at",
    ],
    "Disks": [
        "IP", "Hostname", "Model", "Serial", "Size GB", "Interface",
        "Collected at",
    ],
    "Network": [
        "IP", "Hostname", "Description", "MAC", "IP addresses", "Collected at",
    ],
}


def host_key(name: str) -> str:
    """Chiave di join fra inventario di rete e collector.

    Nell'inventario l'host e' spesso nel formato FQDN (es. HOST.dominio.local),
    mentre il collector riporta il nome NetBIOS corto: senza normalizzare il
    join non troverebbe nulla.
    """
    return str(name or "").strip().split(".")[0].strip().upper()


def mac_key(mac: str) -> str:
    return str(mac or "").strip().upper()


def inventory_index(workbook) -> tuple[dict, dict]:
    """Indice dell'inventario di rete, per hostname e per MAC.

    L'IP non e' un'identita': sulle macchine in leasing ruota (stesso MAC,
    .43 -> .41 -> .40 in due settimane), quindi il join avviene sul MAC quando
    c'e' e l'hostname fa solo da ripiego. L'IP letto sul PC e' piu' fresco di
    quello dichiarato nell'inventario, quindi finisce nella colonna IP e
    l'eventuale valore diverso dell'inventario viene segnalato in Status.
    """
    empty = ({}, {})
    if "Inventory" not in workbook.sheetnames:
        return empty
    ws = workbook["Inventory"]
    header = [str(c.value or "").strip().lower() for c in ws[1]]
    if "ip" not in header:
        return empty
    ip_col = header.index("ip")
    host_col = header.index("hostname") if "hostname" in header else None
    mac_col = header.index("mac") if "mac" in header else None
    by_host, by_mac = {}, {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        ip = str(row[ip_col] or "") if ip_col < len(row) else ""
        host = row[host_col] if host_col is not None and host_col < len(row) else None
        mac = row[mac_col] if mac_col is not None and mac_col < len(row) else None
        entry = {"ip": ip, "mac": str(mac or "").strip().upper()}
        if host:
            by_host[host_key(host)] = entry
        if entry["mac"]:
            by_mac[entry["mac"]] = entry
    return by_host, by_mac


def write_sheet(workbook, name: str, rows: list[list]) -> int:
    from openpyxl.styles import Font

    ws = workbook[name] if name in workbook.sheetnames else workbook.create_sheet(name)
    existing = [str(c.value or "").strip() for c in ws[1]] if ws.max_row else []
    columns = existing if any(existing) else WORKBOOK_SHEETS[name]
    if not any(existing):
        ws.append(columns)
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for values in rows:
        mapping = dict(zip(columns, values))
        ws.append([mapping.get(c, "") for c in columns])
    ws.freeze_panes = "A2"
    return len(rows)


def fill_workbook(workbook, payloads: list[dict], index: tuple) -> dict:
    hardware, disks, networks = [], [], []
    for data in payloads:
        host = str(data.get("computer_name", ""))
        collected = data.get("collected_at_utc") or data.get("collected_at") or ""
        collected = ps_date(collected) or collected
        nics = data.get("network") or []
        observed = pick_ip(nics)
        mac = next((nic_mac(n) for n in nics if nic_mac(n)), "")
        inv_by_host, inv_by_mac = index
        entry = inv_by_mac.get(mac_key(mac)) or inv_by_host.get(host_key(host)) or {}
        inv_ip = entry.get("ip", "")
        ip = observed or inv_ip
        status = "OK"
        if observed and inv_ip and observed != inv_ip:
            status = f"IP differente (inventario {inv_ip})"
        hardware.append([
            ip, host, host, data.get("domain", ""), data.get("manufacturer", ""),
            data.get("model", ""), data.get("serial_number", ""),
            data.get("bios_version", ""), data.get("os_caption", ""),
            data.get("os_version", ""), data.get("os_build", ""),
            (data.get("cpu_name") or "").strip(), data.get("cpu_cores", ""),
            data.get("cpu_threads", ""), data.get("ram_total_gb", ""),
            ps_date(data.get("os_install_date")),
            data.get("os_last_boot") or data.get("os_last_boot_utc", ""),
            status, "", collected,
        ])
        for disk in data.get("disks") or []:
            disks.append([
                ip, host, (disk.get("model") or "").strip(),
                (disk.get("serial") or "").strip(), disk.get("size_gb", ""),
                disk.get("device_id", ""), collected,
            ])
        for nic in data.get("network") or []:
            addresses = nic_ips(nic)
            if not addresses and not nic_mac(nic):
                continue
            networks.append([
                ip, host, nic.get("Description", ""), nic_mac(nic),
                " | ".join(addresses), collected,
            ])
    return {
        "Windows Inventory": write_sheet(workbook, "Windows Inventory", hardware),
        "Disks": write_sheet(workbook, "Disks", disks),
        "Network": write_sheet(workbook, "Network", networks),
    }


def fill_existing(workbook_path: Path, out: Path, payloads: list[dict]) -> int:
    """Riempie i fogli hardware di un inventario di rete gia' esistente.

    L'IP scritto e' quello osservato sul PC, che e' piu' fresco di quello
    nell'inventario: l'IP ruota sulle macchine in leasing, quindi non puo'
    essere trattato come un'identita'. Se i due valori differiscono, la
    differenza resta tracciata nella colonna Status. Il file originale non
    viene mai toccato, si scrive una copia.
    """
    try:
        from openpyxl import load_workbook
    except ModuleNotFoundError:
        print("openpyxl non installato: serve per aggiornare il workbook.")
        return 1

    if not workbook_path.is_file():
        print(f"Workbook non trovato: {workbook_path}")
        return 1

    workbook = load_workbook(workbook_path)
    index = inventory_index(workbook)
    written = fill_workbook(workbook, payloads, index)
    out.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(out)
    print(f"Workbook aggiornato: {out}")
    for name, count in written.items():
        print(f"  {name}: {count} righe")
    if not index[0] and not index[1]:
        print("  ! foglio 'Inventory' assente o senza hostname/MAC: "
              "l'IP arriva dal collector e non puo' essere confrontato.")
    raccolti = {host_key(d.get("computer_name", "")) for d in payloads}
    fuori = sorted(h for h in raccolti - set(index[0]) if h)
    if fuori:
        print(f"  host raccolti ma assenti dall'inventario di rete: {len(fuori)}")
        for host in fuori:
            print(f"    {host}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Importa i JSON hardware e genera il foglio Excel "
                    "delle specifiche del parco."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Cartella sulla share con i JSON (default d'obbligo: "
             "//SRVFS-VN/TEMP-STEFANO/inventory-hardware)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="File Excel di uscita (default: hardware_specifiche.xlsx, oppure "
             "<workbook>_hardware.xlsx se --workbook e' indicato)",
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        help="Inventario di rete esistente da arrichchire: riempie i fogli "
             "'Windows Inventory', 'Disks' e 'Network' con i dati hardware "
             "raccolti. L'originale non viene mai modificato, si scrive una "
             "copia su --out.",
    )
    args = parser.parse_args()

    if args.workbook:
        out = args.out or args.workbook.with_name(
            args.workbook.stem + "_hardware.xlsx"
        )
    else:
        out = args.out or Path("hardware_specifiche.xlsx")

    if not args.input_dir.is_dir():
        print(f"Cartella non trovata: {args.input_dir}")
        return 1

    payloads = read_payloads(args.input_dir)
    print(f"JSON letti: {len(payloads)}")

    if not payloads:
        print("Nessun JSON valido: la raccolta non e' ancora partita.")
        return 1

    if args.workbook:
        return fill_existing(args.workbook, out, payloads)

    records = [to_record(payload) for payload in payloads]

    records.sort(key=lambda r: str(r.get("computer_name", "")))

    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ModuleNotFoundError:
        print("openpyxl non installato: genero il CSV equivalente.")
        csv_path = out.with_suffix(".csv")
        with csv_path.open("w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.DictWriter(fh, fieldnames=[c[1] for c in COLUMNS])
            writer.writeheader()
            for r in records:
                writer.writerow({c[1]: r.get(c[0], "") for c in COLUMNS})
        print(f"CSV scritto: {csv_path}")
        return 0

    wb = Workbook()
    ws = wb.active
    ws.title = "Specifiche parco"
    ws.append([c[1] for c in COLUMNS])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for r in records:
        ws.append([r.get(c[0], "") for c in COLUMNS])
    widths = {1: 18, 2: 10, 3: 15, 4: 14, 5: 22, 6: 18, 7: 34, 8: 7, 9: 8,
              10: 9, 11: 14, 12: 16, 13: 26, 14: 30, 15: 30, 16: 9, 17: 14,
              18: 30, 19: 24, 20: 20}
    for idx, width in widths.items():
        ws.column_dimensions[ws.cell(row=1, column=idx).column_letter].width = width
    ws.freeze_panes = "A2"

    ws2 = wb.create_sheet("Riepilogo")
    ws2.append(["Generato il", datetime.now().strftime("%Y-%m-%d %H:%M")])
    ws2.append(["Macchine raccolte", len(records)])
    rams = sorted({r.get("ram_total_gb") for r in records if r.get("ram_total_gb")})
    ws2.append(["RAM distinti (GB)", ", ".join(str(x) for x in rams)])
    ws2.append(["Host senza seriale", sum(
        1 for r in records if not r.get("serial_number")
    )])
    ws2.append(["Host senza antivirus", sum(
        1 for r in records if not r.get("antivirus")
    )])
    fissi = sum(1 for r in records if r.get("device_type") == "Fisso")
    ws2.append(["Fisso / Notebook", f"{fissi} / {len(records) - fissi}"])

    wb.save(out)
    print(f"Excel scritto: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

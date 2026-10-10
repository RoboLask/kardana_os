# beepeew.py — Kardana Package Manager
import os, sys, requests, platform, colorama
from colorama import Fore, Style
colorama.init()

IS_WINDOWS = platform.system().lower() == "windows"

BEEPEEW_DIR    = os.path.dirname(os.path.abspath(__file__))
SYS_DIR        = os.path.dirname(BEEPEEW_DIR)
ROOT_DIR       = os.path.dirname(SYS_DIR)
DATA_DIR       = os.path.join(SYS_DIR, "data")
PACKET_DIR     = os.path.join(BEEPEEW_DIR, "packet")
PACLIST_FILE   = os.path.join(DATA_DIR, "beepeew_paclist.txt")
INSTALLED_FILE = os.path.join(DATA_DIR, "installed.txt")
APPS_FILE      = os.path.join(DATA_DIR, "installed_apps.txt")
CONF_ACTIVE    = os.path.join(DATA_DIR, "sys-config.active")

def T(s, **kw):   # translator is injected by kardana_pro_3.py
    return s.format(**kw) if kw else s

os.makedirs(PACKET_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def _rel(p):   # paths are stored relative to the system folder
    return os.path.relpath(p, ROOT_DIR).replace("\\", "/")

def _abs(p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(ROOT_DIR, p))

_PACK_KEY = "KARDANA_BEEPEEW_31_SECRET"

# ── Encryption ───────────────────────────────────────────
def _xor_bytes(data, key):
    kb = (key * ((len(data) // len(key)) + 1)).encode("utf-8")
    return bytes(a ^ b for a, b in zip(data, kb))

def _is_kpkg(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for _ in range(3):
                if f.readline().strip() == "#kpkg":
                    return True
    except Exception:
        pass
    return False

def _run_kpkg(filepath):
    import base64
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    payload = ""
    for line in lines:
        line = line.strip()
        if not line or line.startswith("# __KARDANA_SNKS__") or line == "#kpkg":
            continue
        payload = line
        break
    if not payload:
        print(Fore.RED + T("[beepeew] Corrupted package.") + Fore.RESET)
        return
    try:
        code = _xor_bytes(base64.b64decode(payload.encode()), _PACK_KEY).decode("utf-8")
    except Exception as e:
        print(Fore.RED + T("[beepeew] Decryption error: {e}", e=e) + Fore.RESET)
        return
    exec(compile(code, filepath, "exec"), {"__file__": filepath, "__name__": "__main__"})

# ── Repositories ─────────────────────────────────────────
def _load_repos():          # repositories come from sys-config ("repo = ..." lines)
    repos = []
    if not os.path.exists(CONF_ACTIVE):
        return repos
    with open(CONF_ACTIVE, "r", encoding="utf-8") as f:
        for line in f:
            k, _, v = line.split(" #")[0].strip().partition("=")
            v = v.strip()
            if k.strip().lower() == "repo" and v:
                name, url = v.split("|", 1) if "|" in v else ("repo", v)
                repos.append((name.strip(), _github_to_raw(url.strip())))
    return repos

def _github_to_raw(url):
    url = url.rstrip("/")
    if "raw.githubusercontent.com" in url:
        return url
    if "github.com" in url:
        raw = url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        for p in ["/blob/main", "/tree/main", "/blob/master", "/tree/master"]:
            raw = raw.replace(p, "")
        return raw + "/main"
    return url

# ── Package list ─────────────────────────────────────────
def _fetch_remote_paclist(raw_base):
    url = raw_base.rstrip("/") + "/beepeew_paclist.txt"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(Fore.YELLOW + T("[beepeew] Could not load paclist: {e}", e=e) + Fore.RESET)
        return ""

def _parse_paclist(text):
    packages, current = [], {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            if current.get("name"):
                packages.append(current)
            current = {"name": line[1:-1].strip()}
        elif "=" in line and current:
            k, _, v = line.partition("=")
            current[k.strip()] = v.strip()
    if current.get("name"):
        packages.append(current)
    return packages

def _load_local_paclist():
    if not os.path.exists(PACLIST_FILE):
        return []
    with open(PACLIST_FILE, "r", encoding="utf-8") as f:
        return _parse_paclist(f.read())

def _find_pkg(name):
    for p in _load_local_paclist():
        if p.get("name", "").lower() == name.lower():
            return p
    return None

# ── Installed ────────────────────────────────────────────
def _unlock_file(path):
    if os.name == "nt" and os.path.exists(path):
        try:
            import subprocess
            subprocess.run(["attrib", "-h", "-s", path], capture_output=True)
        except Exception:
            pass

def _load_installed():
    installed = {}
    if os.path.exists(INSTALLED_FILE):
        with open(INSTALLED_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, _, v = line.partition("=")
                    installed[k.strip()] = v.strip()
    return installed

def _save_installed(installed):
    _unlock_file(INSTALLED_FILE)
    with open(INSTALLED_FILE, "w", encoding="utf-8") as f:
        for name, fpath in installed.items():
            f.write(f"{name} = {fpath}\n")

# ── Installation ─────────────────────────────────────────
def _fix_url(url):
    if "github.com" in url and "raw.githubusercontent.com" not in url:
        url = url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        url = url.replace("/blob/", "/")
    return url

def _install_dependencies(depends_str):
    if not depends_str:
        return
    for dep in [d.strip() for d in depends_str.split(",") if d.strip()]:
        print(T("[beepeew] Dependency: {dep}", dep=dep))
        os.system(f"{sys.executable} -m pip install {dep} --quiet")

def _register(name, app_name, dest):
    installed = _load_installed()
    installed[name] = _rel(dest)
    _save_installed(installed)
    _unlock_file(APPS_FILE)
    existing = {}
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, "r") as f:
            for line in f:
                if " = " in line:
                    k, _, v = line.partition(" = ")
                    existing[k.strip()] = v.strip()
    existing[app_name] = _rel(dest)
    with open(APPS_FILE, "w") as f:
        for k, v in existing.items():
            f.write(f"{k} = {v}\n")

def _do_install(pkg, snks=None):
    name     = pkg.get("name", "unknown")
    url      = _fix_url(pkg.get("url", ""))
    filename = pkg.get("filename", name + ".py")
    pkg_type = pkg.get("type", "python")
    depends  = pkg.get("depends", "")

    if not url:
        print(Fore.RED + T("[beepeew] No URL for package {name}", name=name) + Fore.RESET)
        return None

    _install_dependencies(depends)

    print(T("[beepeew] Downloading {name} ...", name=name))
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(Fore.RED + T("[beepeew] Download error: {e}", e=e) + Fore.RESET)
        return None

    dest = os.path.join(PACKET_DIR, filename)
    with open(dest, "wb") as f:
        f.write(r.content)

    if not IS_WINDOWS and pkg_type in ("sh", "exe"):
        os.chmod(dest, 0o755)

    _register(name, pkg.get("app_name", name), dest)

    print(Fore.GREEN + T("[beepeew] {name} installed → sys/beepeew/packet/{filename}", name=name, filename=filename) + Fore.RESET)
    return dest

def _confirm_and_install(pkg):
    name     = pkg.get("name", "?")
    pkg_plat = pkg.get("platform", "any").lower()
    cur_plat = "windows" if IS_WINDOWS else "linux"

    if pkg_plat not in ("any", cur_plat):
        labels = {"linux": "Linux", "windows": "Windows"}
        print(Fore.YELLOW + T("[beepeew] Package '{name}' is for {target}, but you have {cur}.", name=name, target=labels.get(pkg_plat, pkg_plat), cur=cur_plat.capitalize()) + Fore.RESET)
        if input(T("Install anyway? (y/n): ")).strip().lower() != "y":
            print(T("[beepeew] Cancelled."))
            return
    else:
        if input(T("[beepeew] Install '{name}'? (y/n): ", name=name)).strip().lower() != "y":
            print(T("[beepeew] Cancelled."))
            return

    _do_install(pkg)

# ── Commands ─────────────────────────────────────────────
def cmd_update():   # bpw -su : repositories only
    repos = _load_repos()
    if not repos:
        print(T("[beepeew] No repositories. Add one in sys-config (repo = ...) and run: sys-config update"))
        return
    combined = ""
    for repo_name, raw_base in repos:
        print(T("[beepeew] Updating list from {repo} ...", repo=repo_name))
        text = _fetch_remote_paclist(raw_base)
        if text:
            combined += f"\n# === {repo_name} ===\n" + text
    if combined:
        with open(PACLIST_FILE, "w", encoding="utf-8") as f:
            f.write(combined)
        print(Fore.GREEN + T("[beepeew] List updated ({n} packages)", n=len(_parse_paclist(combined))) + Fore.RESET)

def cmd_upgrade():  # bpw -sup : installed packages only
    installed = _load_installed()
    if not installed:
        print(T("[beepeew] No installed packages."))
        return
    print(T("[beepeew] Updating installed packages..."))
    for pkg_name in list(installed.keys()):
        pkg = _find_pkg(pkg_name)
        if pkg:
            print(f"  -> {pkg_name}")
            _do_install(pkg)
        else:
            print(Fore.YELLOW + T("  ? {name} not found in repo (local)", name=pkg_name) + Fore.RESET)

def _is_gui(p):
    return p.get("gui", "").lower() in ("1", "true", "yes", "y") or p.get("type", "").lower() == "gui"

def cmd_search(query="", filtered=True):
    platform_filter = ("windows" if IS_WINDOWS else "linux") if filtered else None
    pkgs = _load_local_paclist()
    if not pkgs:
        print(T("[beepeew] List is empty. Run: bpw -su"))
        return
    if filtered:
        pkgs = [p for p in pkgs if p.get("platform","any").lower() in (platform_filter,"any") and not _is_gui(p)]
    if query:
        q = query.lower()
        pkgs = [p for p in pkgs if q in p.get("name","").lower() or q in p.get("description","").lower()]
    if not pkgs:
        print(T("[beepeew] Nothing found."))
        return
    print(f"\n  {T('No'):<4} {T('Name'):<22} {T('Version'):<8} {T('Platform'):<10} {T('Description')}")
    print("  " + "-" * 68)
    for i, p in enumerate(pkgs, 1):
        print(f"  {i:<4} {p.get('name','?'):<22} {p.get('version','-'):<8}"
              f" {p.get('platform','any'):<10} {p.get('description','')}")
    print("\n" + T("Install: bpw -s <name>"))

def cmd_list():
    installed = _load_installed()
    if not installed:
        print(T("[beepeew] No installed packages."))
        return
    print(f"\n  {T('Package'):<25} {T('File')}")
    print("  " + "-" * 55)
    for name, fpath in installed.items():
        mark = "+" if os.path.exists(_abs(fpath)) else "!"
        print(f"  {mark} {name:<23} {fpath}")
    print()

def cmd_install(pkg_name):
    pkg = _find_pkg(pkg_name)
    if not pkg:
        print(T("[beepeew] Package '{name}' not found. Try: bpw -su", name=pkg_name))
        return
    _confirm_and_install(pkg)

def _install_data(fname, data):
    default = os.path.splitext(fname)[0]
    app_name = input(T("App name (Enter = {d}): ", d=default)).strip() or default
    dest = os.path.join(PACKET_DIR, fname)
    with open(dest, "wb") as f:
        f.write(data)
    if not IS_WINDOWS and fname.endswith(".sh"):
        os.chmod(dest, 0o755)
    _register(app_name, app_name, dest)
    print(Fore.GREEN + T("[beepeew] {name} installed. Remove: bpw -r {name}", name=app_name) + Fore.RESET)

def install_file(path):
    with open(path, "rb") as f:
        _install_data(os.path.basename(path), f.read())

def _find_local(src):      # path from system root, then search by name (excluding /home)
    p = os.path.join(ROOT_DIR, src)
    if os.path.isfile(p):
        return p
    name = os.path.basename(src)
    for d, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [x for x in dirs if x not in ("home", "packet", "__pycache__")]
        if name in files:
            return os.path.join(d, name)

def cmd_install_app(src):
    pkg = _find_pkg(src)
    if pkg:                                   # name from repo
        _confirm_and_install(pkg); return
    if src.startswith(("http://", "https://")):
        fname = os.path.basename(src.split("?")[0].rstrip("/")) or "app.py"
        print(T("[beepeew] Downloading {name} ...", name=fname))
        try:
            r = requests.get(_fix_url(src), timeout=30); r.raise_for_status()
        except Exception as e:
            print(Fore.RED + T("[beepeew] Download error: {e}", e=e) + Fore.RESET); return
        _install_data(fname, r.content)
        return
    p = _find_local(src)
    if p:
        install_file(p)
    else:
        print(Fore.RED + T("[beepeew] '{src}' is not a repo package, link or file.", src=src) + Fore.RESET)

def cmd_remove(pkg_name):
    installed = _load_installed()
    if pkg_name not in installed:
        print(T("[beepeew] '{name}' is not installed.", name=pkg_name))
        return
    fpath = installed.pop(pkg_name)
    if os.path.exists(_abs(fpath)):
        os.remove(_abs(fpath))
    _save_installed(installed)
    if os.path.exists(APPS_FILE):
        _unlock_file(APPS_FILE)
        with open(APPS_FILE, "r") as f:
            lines = f.readlines()
        with open(APPS_FILE, "w") as f:
            for line in lines:
                if " = " in line and _abs(line.partition(" = ")[2].strip()) == _abs(fpath):
                    continue
                f.write(line)
    print(Fore.GREEN + T("[beepeew] {name} removed.", name=pkg_name) + Fore.RESET)

def launch_package(filepath):
    if not os.path.exists(filepath):
        print(Fore.RED + T("[beepeew] File not found: {path}", path=filepath) + Fore.RESET)
        return
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".py" and _is_kpkg(filepath):
        _run_kpkg(filepath)
        return
    if ext == ".py":
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                code = f.read()
            exec(compile(code, filepath, "exec"), {"__file__": filepath, "__name__": "__main__"})
        except Exception as e:
            print(Fore.RED + T("[beepeew] Launch error: {e}", e=e) + Fore.RESET)
    elif ext == ".sh" and not IS_WINDOWS:
        os.system(f"bash \"{filepath}\"")
    elif ext == ".bat" and IS_WINDOWS:
        os.system(f"\"{filepath}\"")
    elif ext == ".exe" and IS_WINDOWS:
        os.system(f"\"{filepath}\"")
    elif not IS_WINDOWS:
        os.system(f"\"{filepath}\"")

# ── Dispatcher ───────────────────────────────────────────
def beepeew_command(args_str):
    parts = args_str.strip().split()
    if not parts:
        _help(); return
    flag, rest = parts[0], parts[1:]
    if   flag == "-su":                        cmd_update()
    elif flag == "-sup":                       cmd_upgrade()
    elif flag == "-s"  and rest:               cmd_install(rest[0])
    elif flag == "-i"  and rest:               cmd_install_app(" ".join(rest))
    elif flag == "-g":                         cmd_search(rest[0] if rest else "", True)
    elif flag == "-ga":                        cmd_search(rest[0] if rest else "", False)
    elif flag == "-l":                         cmd_list()
    elif flag == "-r"  and rest:               cmd_remove(" ".join(rest))
    else:                                      _help()

def _help():
    print("\n" + Style.BRIGHT + "bpw" + Style.RESET_ALL + " — " + T("Kardana package manager (beepeew)") + "\n")
    rows = [("bpw -s  <name>", "install a package"), ("bpw -su", "update repositories (package list)"),
            ("bpw -sup", "update installed packages"), ("bpw -sus", "full update: system + repos + packages"),
            ("bpw -g  [query]", "search (your OS only, no GUI)"), ("bpw -ga [query]", "all packages from all repos"),
            ("bpw -i  <link|file>", "install an app (replaces kardana_install)"),
            ("bpw -r  <name>", "remove a package / app"), ("bpw -l", "list installed")]
    for c, d in rows:
        print(f"  {Fore.CYAN}{c:<22}{Fore.RESET}{T(d)}")
    print()

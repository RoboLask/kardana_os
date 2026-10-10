import time
import random
import os
import sys
import hashlib
import uuid
import colorama
from colorama import Fore, Back, Style
import datetime
import requests
import platform
import importlib.util
import re, shutil, posixpath, shlex, getpass, hmac, subprocess

colorama.init()

IS_WINDOWS = platform.system().lower() == "windows"

def clr():
    os.system("cls" if IS_WINDOWS else "clear")

# SNKS - bound to the machine hardware
def _generate_snks():
    raw    = f"{platform.node()}{platform.machine()}{platform.processor()}{platform.system()}"
    digest = hashlib.sha256(raw.encode()).hexdigest().upper()
    return "SNKS-" + "-".join([digest[i:i+4] for i in range(0, 16, 4)])

SNKS_SERIAL = _generate_snks()
os.environ["KARDANA_SNKS"] = SNKS_SERIAL

# beepeew import
_kardana_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _kardana_dir)

# Layout: kardana_pro_3.py | sys/ (data, beepeew, music) | home/
SYS_DIR  = os.path.join(_kardana_dir, "sys")
DATA_DIR = os.path.join(SYS_DIR, "data")
HOME_DIR = os.path.join(_kardana_dir, "home")
APPS_FILE = os.path.join(DATA_DIR, "installed_apps.txt")
for _d in (DATA_DIR, HOME_DIR):
    os.makedirs(_d, exist_ok=True)

BEEPEEW_OK = False
try:
    _bp   = os.path.join(SYS_DIR, "beepeew", "beepeew.py")
    _spec = importlib.util.spec_from_file_location("beepeew_mod", _bp)
    _mod  = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    beepeew_command = _mod.beepeew_command
    launch_package  = _mod.launch_package
    BEEPEEW_OK = True
except Exception as _e:
    print(f"[beepeew] Error: {_e}")

# Self-update (URL comes from sys-config: update_url)

def kardana_update():
    print(T("[Kardana] Checking for updates..."))
    try:
        r = requests.get(CONF["update_url"], timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(Fore.RED + T("[Kardana] Error: {e}", e=e) + Fore.RESET)
        return
    with open(os.path.abspath(__file__), "wb") as f:
        f.write(r.content)
    print(Fore.GREEN + T("[Kardana] Update downloaded! Restart Kardana.") + Fore.RESET)

VERSION_TAG            = "KARDANA_PRO_3.11"
calculator             = "Calculator"
kardana_play           = "Kardana Play"
Weather                = "Weather"
text                   = "Kardana Pro 3.11"
Watch                  = "Watch"
Secret_box             = "Secret_box"
Toss_a_Coin            = "Toss a Coin"
Guess_the_number       = "Guess the number"
Password_Generator_Pro = "Password Generator Pro"
kardana_radio          = "Kardana Radio v1"
kardana_music          = "Kardana Music v1"
box = ["Nothing","Junk","Key","License for the free version",
       "Ball","Scooter","Boat","Bottle"]

colored_text      = text.replace("3.11", f"{Fore.RED}3.11{Fore.RESET}")
bold_colored_text = f"{Style.BRIGHT}{colored_text}{Style.RESET_ALL}"

def run_application(app_name, installed_apps):
    if app_name not in installed_apps:
        print(f"{app_name} is not installed.")
        return
    filepath = os.path.normpath(os.path.join(_kardana_dir, installed_apps[app_name]))
    if BEEPEEW_OK and "beepeew" + os.sep + "packet" in filepath:
        launch_package(filepath)
        return
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}. Removing from list.")
        del installed_apps[app_name]
        with open(APPS_FILE, "w") as f:
            for app, fn in installed_apps.items():
                f.write(f"{app} = {fn}\n")
        return
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".py":
        os.system(f"{sys.executable} \"{filepath}\"")
    elif ext == ".sh" and not IS_WINDOWS:
        os.system(f"bash \"{filepath}\"")
    elif ext == ".bat" and IS_WINDOWS:
        os.system(f"\"{filepath}\"")
    elif ext == ".exe" and IS_WINDOWS:
        os.system(f"\"{filepath}\"")
    else:
        if not IS_WINDOWS:
            os.system(f"\"{filepath}\"")
        else:
            print(f"Cannot run {filepath} on this OS.")

# ══════════════════════════════════════════════════════════
#  Language and sys-config
# ══════════════════════════════════════════════════════════
LANG = "en"
LANGS = ("en", "ua")
_TR = {
    '[Kardana] Checking for updates...': '[Kardana] Перевіряємо оновлення...',
    '[Kardana] Error: {e}': '[Kardana] Помилка: {e}',
    '[Kardana] Update downloaded! Restart Kardana.': '[Kardana] Оновлення завантажено! Перезапусти Kardana.',
    'first run': 'перший запуск',
    'Create an administrator account.': 'Створи акаунт адміністратора.',
    'Wrong login or password': 'Невірний логін або пароль',
    'Password: ': 'Пароль: ',
    'Repeat password: ': 'Повтор пароля: ',
    'Login: 2-16 chars, a-z 0-9 _ -, must start with a letter': 'Логін: 2-16 символів, a-z 0-9 _ -, починається з літери',
    'User already exists': 'Користувач вже існує',
    'Password must be at least 4 characters': 'Пароль мінімум 4 символи',
    'Passwords do not match': 'Паролі не збігаються',
    'Binary file — cannot edit.': 'Бінарний файл — редагувати не можна.',
    'N = edit line': 'N — редагувати рядок',
    'a text = add': 'a текст — додати',
    'i N text = insert': 'i N текст — вставити',
    'd N = delete': 'd N — видалити',
    's = save': 's — зберегти',
    'q = quit': 'q — вихід',
    'Save changes? (y/n): ': 'Зберегти зміни? (y/n): ',
    "opd: '{t}' is disabled": "opd: '{t}' вимкнено",
    'opd: no such folder: {v}': 'opd: немає такої папки: {v}',
    'opd: permission denied: {v}': 'opd: доступ заборонено: {v}',
    'ls: no such folder': 'ls: немає такої папки',
    'ls: permission denied: {v}': 'ls: доступ заборонено: {v}',
    '(empty)': '(порожньо)',
    '{c}: specify a name': "{c}: вкажи ім'я",
    '{c}: already exists: {v}': '{c}: вже існує: {v}',
    '{c}: no folder {par}': '{c}: немає папки {par}',
    '{c}: permission denied: {par}': '{c}: доступ заборонено: {par}',
    'opf [-r] <file>': 'opf [-r] <файл>',
    'opf: it is a folder': 'opf: це папка',
    'opf: permission denied: {v}': 'opf: доступ заборонено: {v}',
    'opf: no such file: {v}': 'opf: немає файлу: {v}',
    'opf: permission denied: {par}': 'opf: доступ заборонено: {par}',
    'opf: binary file': 'opf: бінарний файл',
    'opf: binary file — cannot edit': 'opf: бінарний файл — редагувати не можна',
    'rmd: specify a path': 'rmd: вкажи шлях',
    'rmd: no such path: {v}': 'rmd: немає такого шляху: {v}',
    'rmd: system/home folders cannot be removed (for accounts: mu -r)': 'rmd: системну/домашню папку видаляти не можна (для акаунта: mu -r)',
    'rmd: permission denied: {v}': 'rmd: доступ заборонено: {v}',
    "Folder '{v}' is not empty. Delete everything inside? (y/n): ": "Папка '{v}' не порожня. Видалити все всередині? (y/n): ",
    'al <755> <path>': 'al <755> <шлях>',
    'al: no such path': 'al: немає такого шляху',
    'al: only the owner can change permissions': 'al: змінювати права може лише власник',
    'mu: administrators only': 'mu: лише для адміністратора',
    'mu <login> [-a]  |  mu -l  |  mu -r <login>': 'mu <логін> [-a]  |  mu -l  |  mu -r <логін>',
    'mu: no such user': 'mu: немає такого користувача',
    'mu: you cannot delete yourself': 'mu: не можна видалити себе',
    "Delete account '{n}'? (y/n): ": "Видалити акаунт '{n}'? (y/n): ",
    'Also delete home folder? (y/n): ': 'Видалити і домашню папку? (y/n): ',
    'User {n} created': 'Користувача {n} створено',
    'ka_terminal: administrators only': 'ka_terminal: лише для адміністратора',
    '[beepeew] Module not found. Make sure sys/beepeew/beepeew.py exists': '[beepeew] Модуль не знайдено. Перевір, що є sys/beepeew/beepeew.py',
    'sys-config: administrators only': 'sys-config: лише для адміністратора',
    "Run 'sys-config update' to apply the changes.": "Виконай 'sys-config update', щоб застосувати зміни.",
    "sys-config: line {n}: unknown language '{v}' (en / ua)": "sys-config: рядок {n}: невідома мова '{v}' (en / ua)",
    "sys-config: line {n}: unknown option '{k}'": "sys-config: рядок {n}: невідома опція '{k}'",
    "Nothing applied — fix the errors and run 'sys-config update' again.": "Нічого не застосовано — виправ помилки і повтори 'sys-config update'.",
    'Settings applied.': 'Налаштування застосовано.',
    '[beepeew] Corrupted package.': '[beepeew] Пошкоджений пакет.',
    '[beepeew] Decryption error: {e}': '[beepeew] Помилка розшифрування: {e}',
    '[beepeew] Could not load paclist: {e}': '[beepeew] Не вдалося завантажити paclist: {e}',
    '[beepeew] Dependency: {dep}': '[beepeew] Залежність: {dep}',
    '[beepeew] No URL for package {name}': '[beepeew] Немає URL для пакета {name}',
    '[beepeew] Downloading {name} ...': '[beepeew] Завантажуємо {name} ...',
    '[beepeew] Download error: {e}': '[beepeew] Помилка завантаження: {e}',
    '[beepeew] {name} installed → sys/beepeew/packet/{filename}': '[beepeew] {name} встановлено → sys/beepeew/packet/{filename}',
    "[beepeew] Package '{name}' is for {target}, but you have {cur}.": "[beepeew] Пакет '{name}' призначений для {target}, а в тебе {cur}.",
    'Install anyway? (y/n): ': 'Все одно встановити? (y/n): ',
    '[beepeew] Cancelled.': '[beepeew] Скасовано.',
    "[beepeew] Install '{name}'? (y/n): ": "[beepeew] Встановити '{name}'? (y/n): ",
    '[beepeew] No repositories. Add one in sys-config (repo = ...) and run: sys-config update': '[beepeew] Немає репозиторіїв. Додай у sys-config (repo = ...) і виконай: sys-config update',
    '[beepeew] Updating list from {repo} ...': '[beepeew] Оновлюємо список з {repo} ...',
    '[beepeew] List updated ({n} packages)': '[beepeew] Список оновлено ({n} пакетів)',
    '[beepeew] No installed packages.': '[beepeew] Немає встановлених пакетів.',
    '[beepeew] Updating installed packages...': '[beepeew] Оновлюємо встановлені пакети...',
    '  ? {name} not found in repo (local)': '  ? {name} не знайдено в репо (локальний)',
    '[beepeew] List is empty. Run: bpw -su': '[beepeew] Список порожній. Запусти: bpw -su',
    '[beepeew] Nothing found.': '[beepeew] Нічого не знайдено.',
    'No': '№',
    'Name': "Ім'я",
    'Version': 'Версія',
    'Platform': 'Платформа',
    'Description': 'Опис',
    'Install: bpw -s <name>': "Встановлення: bpw -s <ім'я>",
    'Package': 'Пакет',
    'File': 'Файл',
    "[beepeew] Package '{name}' not found. Try: bpw -su": "[beepeew] Пакет '{name}' не знайдено. Спробуй: bpw -su",
    "[beepeew] '{src}' is not a repo package, link or file.": "[beepeew] '{src}' — не пакет з репо, не посилання і не файл.",
    'App name (Enter = {d}): ': 'Назва застосунку (Enter = {d}): ',
    '[beepeew] {name} installed. Remove: bpw -r {name}': '[beepeew] {name} встановлено. Видалити: bpw -r {name}',
    "[beepeew] '{name}' is not installed.": "[beepeew] '{name}' не встановлено.",
    '[beepeew] {name} removed.': '[beepeew] {name} видалено.',
    '[beepeew] File not found: {path}': '[beepeew] Файл не знайдено: {path}',
    '[beepeew] Launch error: {e}': '[beepeew] Помилка запуску: {e}',
    'Kardana package manager (beepeew)': 'пакетний менеджер Kardana (beepeew)',
    'install a package': 'встановити пакет',
    'update repositories (package list)': 'оновити репозиторії (список пакетів)',
    'update installed packages': 'оновити встановлені пакети',
    'full update: system + repos + packages': 'повне оновлення: система + репо + пакети',
    'search (your OS only, no GUI)': 'пошук (лише під твою ОС, без GUI)',
    'all packages from all repos': 'усі пакети з усіх репо',
    'install an app (replaces kardana_install)': 'встановити застосунок (заміна kardana_install)',
    'remove a package / app': 'видалити пакет / застосунок',
    'list installed': 'список встановлених',
    "sys-config: line {n}: invalid value '{v}' for '{k}' (on / off)": "sys-config: рядок {n}: невірне значення '{v}' для '{k}' (on / off)",
    'sys-config: line {n}: country must be a 2-letter code (PL, UA, ...)': 'sys-config: рядок {n}: країна — це 2 літери (PL, UA, ...)',
}

def T(s, **kw):
    if LANG == "ua" and s in _TR:
        s = _TR[s]
    return s.format(**kw) if kw else s

CONF_FILE   = os.path.join(DATA_DIR, "sys-config.txt")
CONF_ACTIVE = os.path.join(DATA_DIR, "sys-config.active")
DEFAULT_UPDATE_URL = "https://raw.githubusercontent.com/RoboLask/kardana_os/main/kardana_pro_3.py"
DEFAULT_CONF = """# Kardana system config
# Edit this file, then run:  sys-config update
language = en            # en / ua
loading_window = on      # on / off  - startup splash and "Loading..."
city =                   # city for Weather, e.g. Warsaw
country =                # 2-letter country code for Weather, e.g. PL
prompt = {user}@kardana:{path}$     # placeholders: {user} {path}
music_dir =              # music folder (empty = sys/kardana_music)
update_url = """ + DEFAULT_UPDATE_URL + """
repo = beepeew_repo|https://raw.githubusercontent.com/RoboLask/beepeew_repo/main
"""

CONF_DEFAULTS = {"language": "en", "loading_window": True, "city": "", "country": "",
                 "prompt": "{user}@kardana:{path}$", "music_dir": "", "update_url": DEFAULT_UPDATE_URL}
CONF = dict(CONF_DEFAULTS)

def parse_conf(text):
    cfg, errors = dict(CONF_DEFAULTS), []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.split(" #")[0].strip()
        if not line or line.startswith("#"):
            continue
        k, _, v = line.partition("=")
        k, v = k.strip().lower(), v.strip()
        if k == "language":
            if v in LANGS: cfg["language"] = v
            else: errors.append(T("sys-config: line {n}: unknown language '{v}' (en / ua)", n=n, v=v))
        elif k == "loading_window":
            if v.lower() in ("on", "off"): cfg[k] = v.lower() == "on"
            else: errors.append(T("sys-config: line {n}: invalid value '{v}' for '{k}' (on / off)", n=n, v=v, k=k))
        elif k == "country":
            if not v or re.fullmatch(r"[A-Za-z]{2}", v): cfg[k] = v.upper()
            else: errors.append(T("sys-config: line {n}: country must be a 2-letter code (PL, UA, ...)", n=n))
        elif k in ("city", "prompt", "music_dir", "update_url"):
            if v or k in ("city", "music_dir"): cfg[k] = v
        elif k != "repo":
            errors.append(T("sys-config: line {n}: unknown option '{k}'", n=n, k=k))
    return cfg, errors

def load_active_conf():
    global LANG, CONF
    if not os.path.exists(CONF_FILE):
        open(CONF_FILE, "w", encoding="utf-8").write(DEFAULT_CONF)
    if not os.path.exists(CONF_ACTIVE):
        shutil.copy(CONF_FILE, CONF_ACTIVE)
    CONF = parse_conf(open(CONF_ACTIVE, encoding="utf-8").read())[0]
    LANG = CONF["language"]

load_active_conf()
if BEEPEEW_OK:
    _mod.T = T



# Startup splash
if CONF["loading_window"]:
    clr()
    print(r'''
  _  __             _                     _____             ____  
 | |/ /            | |                   |  __ \           |___ \ 
 | ' / __ _ _ __ __| | __ _ _ __   __ _  | |__) | __ ___     __) |
 |  < / _` | '__/ _` |/ _` | '_ \ / _` | |  ___/ '__/ _ \   |__ < 
 | . \ (_| | | | (_| | (_| | | | | (_| | | |   | | | (_) |  ___) |
 |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|   |_|  \___/  |____/ 
''')
    print(f"  {Fore.CYAN}SNKS: {SNKS_SERIAL}{Fore.RESET}")
    print(f"  Version: {VERSION_TAG}  |  OS: {platform.system()}")
    time.sleep(2)
    clr()
    print("Loading...")
    time.sleep(1)
    clr()
else:
    clr()

# ══════════════════════════════════════════════════════════
#  Accounts, virtual FS, permissions
# ══════════════════════════════════════════════════════════
# Options of the opd (cd) command and extra commands - set False to disable
OPD_OPTS = {"..": True, "~": True, "-": True}
EXTRA_CMDS = {"ls": True, "pwd": True}

ACC_FILE  = os.path.join(DATA_DIR, "accounts.txt")
PERM_FILE = os.path.join(DATA_DIR, "perms.txt")
_NAME_RE  = re.compile(r"^[a-z][a-z0-9_-]{1,15}$")
_ITER     = 200_000
USER = CWD = OLDPWD = ""
_printed = [False]
_redraw = [False]

def _say(msg):
    _printed[0] = True
    print(msg)

def _err(msg):
    _say(f"{Fore.RED}{msg}{Fore.RESET}")

# ── passwords: salt + PBKDF2-SHA256 (one-way hashing) ──
def _hash(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, _ITER).hex()

def load_users():
    users = {}
    if os.path.exists(ACC_FILE):
        with open(ACC_FILE, encoding="utf-8") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 4:
                    users[p[0]] = {"admin": p[1] == "1", "salt": p[2], "hash": p[3]}
    return users

def save_users(users):
    with open(ACC_FILE, "w", encoding="utf-8") as f:
        for n, u in users.items():
            f.write(f"{n}|{int(u['admin'])}|{u['salt']}|{u['hash']}\n")

def is_admin():
    return load_users().get(USER, {}).get("admin", False)

def ask_password(prompt):
    try:
        return getpass.getpass(prompt)
    except Exception:
        return input(prompt)

# ── permissions: perms.txt file  "/path|owner|755" ──
def load_perms():
    perms = {}
    if os.path.exists(PERM_FILE):
        with open(PERM_FILE, encoding="utf-8") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 3:
                    perms[p[0]] = (p[1], int(p[2], 8))
    return perms

def save_perms(perms):
    with open(PERM_FILE, "w", encoding="utf-8") as f:
        for k, (o, m) in perms.items():
            f.write(f"{k}|{o}|{m:o}\n")

def set_meta(vp, owner, mode):
    perms = load_perms()
    perms[vp] = (owner, mode)
    save_perms(perms)

def real_path(vp):
    return os.path.join(_kardana_dir, *[x for x in vp.split("/") if x])

def vpath(p):
    p = p.replace("\\", "/")
    if p == "~" or p.startswith("~/"):
        p = "/home/" + USER + p[1:]
    if not p.startswith("/"):
        p = CWD + "/" + p
    return "/" + posixpath.normpath(p).lstrip("/")

def _allow(user, vp, bit, perms):
    owner, mode = perms.get(vp, ("root", 0o755 if os.path.isdir(real_path(vp)) else 0o644))
    return bool(((mode >> 6) if owner == user else mode) & 7 & bit)

def can(user, vp, bit):          # bit: 4=read 2=write 1=enter/run
    if load_users().get(user, {}).get("admin"):
        return True
    perms = load_perms()
    parts = [x for x in vp.split("/") if x]
    for a in ["/"] + ["/" + "/".join(parts[:i]) for i in range(1, len(parts))]:
        if not _allow(user, a, 1, perms):
            return False
    return _allow(user, vp, bit, perms)

def ensure_system():
    for d in (SYS_DIR, DATA_DIR, HOME_DIR):
        os.makedirs(d, exist_ok=True)
    perms = load_perms()
    perms.setdefault("/sys", ("root", 0o700))
    perms.setdefault("/home", ("root", 0o755))
    save_perms(perms)

def make_home(name):
    base = "/home/" + name
    for sub in ("", "/Documents", "/Downloads", "/Desktop"):
        os.makedirs(real_path(base + sub), exist_ok=True)
        set_meta(base + sub, name, 0o700)

def create_user(name, admin=False):
    users = load_users()
    if not _NAME_RE.match(name):
        print(Fore.RED + T("Login: 2-16 chars, a-z 0-9 _ -, must start with a letter") + Fore.RESET); return False
    if name in users:
        print(Fore.RED + T("User already exists") + Fore.RESET); return False
    p1 = ask_password(T("Password: "))
    if len(p1) < 4:
        print(Fore.RED + T("Password must be at least 4 characters") + Fore.RESET); return False
    if p1 != ask_password(T("Repeat password: ")):
        print(Fore.RED + T("Passwords do not match") + Fore.RESET); return False
    salt = os.urandom(16)
    users[name] = {"admin": admin, "salt": salt.hex(), "hash": _hash(p1, salt)}
    save_users(users)
    make_home(name)
    return True

def login():
    global USER, CWD, OLDPWD
    clr()
    users = load_users()
    if not users:
        print(f"{bold_colored_text} — " + T("first run") + "\n" + T("Create an administrator account.") + "\n")
        while True:
            name = input("Login: ").strip().lower()
            if create_user(name, admin=True):
                break
        USER = name
    else:
        print(f"{bold_colored_text}  {Fore.CYAN}{SNKS_SERIAL}{Fore.RESET}\n")
        while True:
            name = input("login: ").strip().lower()
            pw = ask_password("password: ")
            u = users.get(name)
            salt = bytes.fromhex(u["salt"]) if u else bytes(16)
            good = hmac.compare_digest(_hash(pw, salt), u["hash"] if u else "0" * 64)
            if u and good:
                USER = name
                break
            time.sleep(1.5)
            print(Fore.RED + T("Wrong login or password") + Fore.RESET + "\n")
    make_home(USER) if not os.path.isdir(real_path("/home/" + USER)) else None
    CWD = OLDPWD = "/home/" + USER
    clr()

# ── editor for opf ──
def _read_text(r):
    try:
        with open(r, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return None

def _mini_edit(r):
    text = _read_text(r) if os.path.exists(r) else ""
    if text is None:
        _err(T("Binary file — cannot edit.")); return
    lines, dirty = text.splitlines() or [""], False
    while True:
        clr()
        print(f"{Fore.CYAN}opf: {os.path.basename(r)}{Fore.RESET}{' *' if dirty else ''}\n")
        for i, l in enumerate(lines, 1):
            print(f"{i:>3} | {l}")
        print("\n" + Fore.YELLOW + "   ".join(T(x) for x in ("N = edit line", "a text = add", "i N text = insert", "d N = delete", "s = save", "q = quit")) + Fore.RESET)
        cmd = input(">> ")
        w = cmd.split(None, 2)
        if cmd.strip().isdigit() and 1 <= int(cmd) <= len(lines):
            n = int(cmd) - 1
            print(f"{n+1} | {lines[n]}")
            new = input(f"{n+1} | ")
            if new != "":
                lines[n], dirty = new, True
        elif w[:1] == ["a"]:
            lines.append(cmd[2:]); dirty = True
        elif w[:1] == ["i"] and len(w) >= 2 and w[1].isdigit():
            lines.insert(max(0, int(w[1]) - 1), w[2] if len(w) > 2 else ""); dirty = True
        elif w[:1] == ["d"] and len(w) == 2 and w[1].isdigit() and 1 <= int(w[1]) <= len(lines):
            del lines[int(w[1]) - 1]; dirty = True
        elif cmd.strip() == "s":
            with open(r, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            dirty = False
        elif cmd.strip() == "q":
            if dirty and input(T("Save changes? (y/n): ")).strip().lower() == "y":
                with open(r, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
            break

def _edit(r):
    nano = shutil.which("nano")
    if nano:
        subprocess.call([nano, "-R", r])      # -R: restricted mode (no shell, no access to other files)
    else:
        _mini_edit(r)
    clr(); _redraw[0] = True

def _perm_str(owner, mode, isdir):
    s = "d" if isdir else "-"
    for sh in (6, 3, 0):
        b = (mode >> sh) & 7
        s += ("r" if b & 4 else "-") + ("w" if b & 2 else "-") + ("x" if b & 1 else "-")
    return s

def _protected(v):
    parts = [x for x in v.split("/") if x]
    return len(parts) == 0 or v in ("/sys", "/home") or (len(parts) == 2 and parts[0] == "home")

# ── file commands ──
FS_CMDS = {"opf", "opd", "md", "mf", "rmd", "mu", "al", "logout", "cls", "sys-config"} | {k for k, v in EXTRA_CMDS.items() if v}

def fs_command(line):
    """Runs a command. True = there was output to read (pause needed)."""
    global CWD, OLDPWD, USER, LANG, CONF
    _printed[0] = False
    try:
        a = shlex.split(line)
    except ValueError:
        a = line.split()
    c, args = a[0], a[1:]

    if c == "opd":
        t = args[0] if args else "~"
        if (t == ".." and not OPD_OPTS[".."]) or (t.startswith("~") and not OPD_OPTS["~"]) or (t == "-" and not OPD_OPTS["-"]):
            _err(T("opd: '{t}' is disabled", t=t)); return True
        v = vpath(OLDPWD if t == "-" else t)
        if not os.path.isdir(real_path(v)):   _err(T("opd: no such folder: {v}", v=v))
        elif not can(USER, v, 1):             _err(T("opd: permission denied: {v}", v=v))
        else:                                 OLDPWD, CWD = CWD, v

    elif c == "cls":
        clr(); _redraw[0] = True

    elif c == "sys-config":
        if not is_admin():
            _err(T("sys-config: administrators only")); return True
        if args[:1] == ["update"]:
            cfg, errs = parse_conf(open(CONF_FILE, encoding="utf-8").read())
            if errs:
                for m in errs: _err(m)
                _err(T("Nothing applied — fix the errors and run 'sys-config update' again."))
            else:
                shutil.copy(CONF_FILE, CONF_ACTIVE); CONF = cfg; LANG = cfg["language"]
                _say(Fore.GREEN + T("Settings applied.") + Fore.RESET)
        else:
            _edit(CONF_FILE)
            if open(CONF_FILE, encoding="utf-8").read() != open(CONF_ACTIVE, encoding="utf-8").read():
                _say(T("Run 'sys-config update' to apply the changes."))

    elif c == "pwd":
        _say(CWD)

    elif c == "ls":
        v = vpath(args[0] if args else ".")
        if not os.path.isdir(real_path(v)):   _err(T("ls: no such folder"))
        elif not can(USER, v, 4):             _err(T("ls: permission denied: {v}", v=v))
        else:
            perms = load_perms()
            for n in sorted(os.listdir(real_path(v))):
                p = (v.rstrip("/") + "/" + n)
                d = os.path.isdir(real_path(p))
                o, m = perms.get(p, ("root", 0o755 if d else 0o644))
                _say(f"{_perm_str(o, m, d)} {o:<10} " + (f"{Fore.CYAN}/{n}{Fore.RESET}" if d else n))
            if not os.listdir(real_path(v)):
                _say(T("(empty)"))

    elif c in ("md", "mf"):
        if not args:
            _err(T("{c}: specify a name", c=c)); return True
        for t in args:
            v = vpath(t); par = posixpath.dirname(v)
            if os.path.exists(real_path(v)):                 _err(T("{c}: already exists: {v}", c=c, v=v))
            elif not os.path.isdir(real_path(par)):          _err(T("{c}: no folder {par}", c=c, par=par))
            elif not (can(USER, par, 2) and can(USER, par, 1)): _err(T("{c}: permission denied: {par}", c=c, par=par))
            elif c == "md":
                os.mkdir(real_path(v)); set_meta(v, USER, 0o755)
            else:
                open(real_path(v), "a").close(); set_meta(v, USER, 0o644)

    elif c == "opf":
        ro = bool(args) and args[0] == "-r"
        if ro: args = args[1:]
        if not args:
            _err(T("opf [-r] <file>")); return True
        v = vpath(args[0]); r = real_path(v)
        if os.path.isdir(r):
            _err(T("opf: it is a folder")); return True
        if os.path.exists(r):
            if not can(USER, v, 4 if ro else 6):
                _err(T("opf: permission denied: {v}", v=v)); return True
        else:
            par = posixpath.dirname(v)
            if ro or not os.path.isdir(real_path(par)):
                _err(T("opf: no such file: {v}", v=v)); return True
            if not (can(USER, par, 2) and can(USER, par, 1)):
                _err(T("opf: permission denied: {par}", par=par)); return True
            open(r, "a").close(); set_meta(v, USER, 0o644)
        if ro:
            t = _read_text(r)
            _say(t if t is not None else Fore.RED + T("opf: binary file") + Fore.RESET)
        else:
            if _read_text(r) is None:
                _err(T("opf: binary file — cannot edit")); return True
            _edit(r)

    elif c == "rmd":
        if not args:
            _err(T("rmd: specify a path")); return True
        v = vpath(args[0]); r = real_path(v); par = posixpath.dirname(v)
        if not os.path.exists(r):                          _err(T("rmd: no such path: {v}", v=v))
        elif _protected(v):                                _err(T("rmd: system/home folders cannot be removed (for accounts: mu -r)"))
        elif not (can(USER, par, 2) and can(USER, par, 1)): _err(T("rmd: permission denied: {v}", v=v))
        else:
            if os.path.isdir(r):
                if os.listdir(r) and input(T("Folder '{v}' is not empty. Delete everything inside? (y/n): ", v=v)).strip().lower() != "y":
                    return _printed[0]
                shutil.rmtree(r)
            else:
                os.remove(r)
            save_perms({k: m for k, m in load_perms().items() if not (k == v or k.startswith(v + "/"))})
            if CWD == v or CWD.startswith(v + "/"):
                CWD = par

    elif c == "al":
        if len(args) != 2 or not re.fullmatch(r"[0-7]{3}", args[0]):
            _err(T("al <755> <path>")); return True
        v = vpath(args[1])
        if not os.path.exists(real_path(v)):  _err(T("al: no such path"))
        else:
            owner = load_perms().get(v, ("root", 0))[0]
            if owner != USER and not is_admin(): _err(T("al: only the owner can change permissions"))
            else:                                set_meta(v, owner, int(args[0], 8))

    elif c == "mu":
        if not is_admin():
            _err(T("mu: administrators only")); return True
        users = load_users()
        if not args:
            _err(T("mu <login> [-a]  |  mu -l  |  mu -r <login>"))
        elif args[0] == "-l":
            for n, u in users.items():
                _say(f"  {n:<16}" + (f"{Fore.YELLOW}admin{Fore.RESET}" if u["admin"] else "user"))
        elif args[0] == "-r":
            n = args[1] if len(args) > 1 else ""
            if n not in users:     _err(T("mu: no such user"))
            elif n == USER:        _err(T("mu: you cannot delete yourself"))
            elif input(T("Delete account '{n}'? (y/n): ", n=n)).strip().lower() == "y":
                del users[n]; save_users(users)
                if input(T("Also delete home folder? (y/n): ")).strip().lower() == "y":
                    shutil.rmtree(real_path("/home/" + n), ignore_errors=True)
                    save_perms({k: m for k, m in load_perms().items() if not k.startswith("/home/" + n)})
        else:
            if create_user(args[0].lower(), admin="-a" in args[1:]):
                _say(Fore.GREEN + T("User {n} created", n=args[0].lower()) + Fore.RESET)

    elif c == "logout":
        login(); _redraw[0] = True

    return _printed[0]

def bpw_command(args):
    if not BEEPEEW_OK:
        print(Fore.RED + T("[beepeew] Module not found. Make sure sys/beepeew/beepeew.py exists") + Fore.RESET)
    elif args.split()[:1] == ["-sus"]:
        kardana_update(); beepeew_command("-su"); beepeew_command("-sup")
    elif args.split()[:1] == ["-i"] and len(args.split()) > 1 and not args.split()[1].startswith(("http://", "https://")) \
            and os.path.isfile(real_path(vpath(" ".join(args.split()[1:])))):
        v = vpath(" ".join(args.split()[1:]))
        if can(USER, v, 4): _mod.install_file(real_path(v))
        else: _err(T("opf: permission denied: {v}", v=v))
    else:
        beepeew_command(args)

ensure_system()
login()

# Main loop
_quiet = False
while True:
    installed_apps = {}
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, "r") as _f:
            for _line in _f:
                _parts = _line.split(" = ")
                if len(_parts) == 2:
                    installed_apps[_parts[0].strip()] = _parts[1].strip()

    if not _quiet:
        print(bold_colored_text)
        print('Applications:\n'+calculator+'[write 1 to open]\n'+kardana_play+"[write 2 to open]")
        for index, (app_name, _) in enumerate(installed_apps.items(), start=3):
            print(f"{app_name}[write {index} to open]")
    _quiet = False
    _cd = CWD.replace("/home/" + USER, "~", 1) if CWD.startswith("/home/" + USER) else CWD
    _prompt = CONF["prompt"].replace("{user}", f"{Fore.GREEN}{USER}{Fore.RESET}").replace("{path}", f"{Fore.CYAN}{_cd}{Fore.RESET}") + " "
    menu = input(_prompt)

    if menu == "1":
        print('Loading...')
        time.sleep(1)
        print(r'''Welcome to the calculator
        Operators + - * / %
        Write your example''')
        try:
            p = input()
            result = eval(p)
            print("Solution:")
            print(result)
            time.sleep(2)
            clr()
        except Exception as e:
            print("Error:", e)
            time.sleep(1)
            print("Please enter a valid expression and try again.")

    elif menu == "2":
        print("Loading...")
        time.sleep(1)
        clr()
        print('Applications:\n'+Weather+'[write 1 to open]\n'+Watch+"[write 2 to open]\n"+Password_Generator_Pro+"[write 3 to open]\n"+kardana_radio+"[write 4 to open]")
        print('Games:\n'+Secret_box+'[write 5 to open]\n'+Guess_the_number+"[write 6 to open]\n"+Toss_a_Coin+"[write 7 to open]\n"+kardana_music+"[write 8 to open]")
        kp = input()

        if kp == "1":
            def get_weather(city):
                q = f"{city},{CONF['country']}" if CONF["country"] else city
                url = (f"https://api.openweathermap.org/data/2.5/weather"
                       f"?q={q}&units=metric&lang={'ua' if LANG == 'ua' else 'en'}"
                       f"&appid=79d1ca96933b0328e1c7e3e7a26cb347")
                r = requests.get(url)
                return r.json() if r.status_code == 200 else None
            settings_file = os.path.join(DATA_DIR, "settings_kardana.txt")
            city = CONF["city"] or None
            if not city and os.path.exists(settings_file):
                with open(settings_file) as f:
                    for line in f:
                        if line.startswith("City"):
                            city = line.split("=")[1].strip()
            if not city:
                city = input("Enter your city: ")
                with open(settings_file, "w") as f:
                    f.write(f"City = {city}\n")
            data = get_weather(city)
            if data:
                print(f"  {city}: {round(data['main']['temp'])} C  (feels {round(data['main']['feels_like'])} C), {data['weather'][0]['description']}")
            else:
                print("City not found.")
            time.sleep(2)
            clr()

        elif kp == "2":
            print("Current time:", datetime.datetime.now().strftime("%H:%M:%S"))
            time.sleep(2)
            clr()

        elif kp == "3":
            chars = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            try:
                n = int(input("Number of passwords: "))
                l = int(input("Length: "))
                for _ in range(n):
                    print("".join(random.choice(chars) for _ in range(l)))
            except ValueError:
                print("Invalid input.")
            time.sleep(2)
            clr()

        elif kp == "4":
            try:
                from PyQt5.QtCore import QUrl
                from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
                class ConsoleMediaPlayer:
                    def __init__(self, url):
                        self.player   = QMediaPlayer()
                        self.playlist = QMediaPlaylist()
                        self.playlist.addMedia(QMediaContent(QUrl(url)))
                        self.player.setPlaylist(self.playlist)
                        self.player.setVolume(100)
                    def play(self):  self.player.play()
                    def stop(self):  self.player.stop()
                cmp = ConsoleMediaPlayer("https://online.hitfm.ua/HitFM")
                while True:
                    cmp.play()
                    clr()
                    print("Kardana Radio v1 - HitFM\nCommands: stop / exit")
                    cmd = input(">> ").lower()
                    if cmd == "stop":
                        cmp.stop()
                        if input("(play/exit) >> ").lower() == "exit":
                            break
                    elif cmd == "exit":
                        cmp.stop()
                        break
            except ImportError:
                print("PyQt5 not installed. Run: pip install PyQt5")
                time.sleep(2)
            clr()

        elif kp == "5":
            print("You got:", random.choice(box))
            time.sleep(2)
            clr()

        elif kp == "6":
            c = random.randrange(1, 10)
            print("Guess 1-10:")
            while True:
                try:
                    v = int(input())
                    if v == c:   print("You won!"); time.sleep(1); clr(); break
                    elif v > c:  print("Too high")
                    else:        print("Too low")
                except ValueError:
                    print("Enter a number.")

        elif kp == "7":
            print("You got:", random.choice(["Heads", "Tails"]))
            time.sleep(1)
            clr()

        elif kp == "8":
            clr()
            try:
                import pygame
            except ImportError:
                print("pygame not installed. Run: pip install pygame")
                time.sleep(2)
                clr()
                continue
            music_folder = os.path.join(SYS_DIR, "kardana_music")
            if CONF["music_dir"]:
                music_folder = os.path.normpath(os.path.join(_kardana_dir, os.path.expanduser(CONF["music_dir"])))
            def list_music(directory):
                if not os.path.exists(directory):
                    print(f"Folder '{directory}' not found.")
                    if input("Create it? (y/n) >> ").strip().lower() == "y":
                        os.makedirs(directory)
                        print(f"Created '{directory}'. Add .mp3 or .wav files there.")
                    return []
                files = [f for f in os.listdir(directory) if f.endswith((".mp3", ".wav"))]
                if not files:
                    print("No music files in folder.")
                else:
                    for i, mf in enumerate(files, 1):
                        print(f"  {i}. {mf}")
                return files
            while True:
                files = list_music(music_folder)
                if not files:
                    time.sleep(2)
                    clr()
                    break
                try:
                    choice = int(input("Track number (0 = exit): "))
                    if choice == 0:
                        clr()
                        break
                    elif 1 <= choice <= len(files):
                        pygame.mixer.init()
                        pygame.mixer.music.load(os.path.join(music_folder, files[choice-1]))
                        pygame.mixer.music.play()
                        while True:
                            ctrl = input("pause / resume / exit: ").strip().lower()
                            if ctrl == "pause":   pygame.mixer.music.pause()
                            elif ctrl == "resume": pygame.mixer.music.unpause()
                            elif ctrl == "exit":
                                pygame.mixer.music.stop()
                                clr()
                                break
                    else:
                        print("Invalid number.")
                        time.sleep(1)
                        clr()
                except ValueError:
                    print("Enter a number.")
                    time.sleep(1)
                    clr()
        else:
            clr()

    elif menu == "dota 2":
        print(r'''
  _____   ____ _______         ___  
 |  __ \ / __ \__   __|/\     |__ \ 
 | |  | | |  | | | |  /  \       ) |
 | |  | | |  | | | | / /\ \     / / 
 | |__| | |__| | | |/ ____ \   / /_ 
 |_____/ \____/  |_/_/    \_\ |____|
''')
        time.sleep(2)
        clr()

    elif menu.split()[:1] and menu.split()[0] in FS_CMDS:
        _redraw[0] = False
        fs_command(menu)
        _quiet = not _redraw[0]

    elif menu.split()[:1] == ["bpw"]:
        bpw_command(menu[3:].strip())
        _quiet = True

    elif menu == "kardana_update":
        kardana_update()
        time.sleep(2)

    elif menu == "about":
        clr()
        print(r'''
  _  __             _                     _____             ____  
 | |/ /            | |                   |  __ \           |___ \ 
 | ' / __ _ _ __ __| | __ _ _ __   __ _  | |__) | __ ___     __) |
 |  < / _` | '__/ _` |/ _` | '_ \ / _` | |  ___/ '__/ _ \   |__ < 
 | . \ (_| | | | (_| | (_| | | | | (_| | | |   | | | (_) |  ___) |
 |_|\_\__,_|_|  \__,_|\__,_|_| |_|\__,_| |_|   |_|  \___/  |____/ 
''')
        print(f"  Version : {Fore.GREEN}{VERSION_TAG}{Fore.RESET}")
        print(f"  SNKS    : {Fore.CYAN}{SNKS_SERIAL}{Fore.RESET}")
        print(f"  OS      : {platform.system()} {platform.version()}")
        print(f"  Arch    : {platform.architecture()[0]}")
        print(f"  Machine : {platform.machine()}")
        print(f"  Node    : {platform.node()}")
        print(f"  CPU     : {platform.processor()}")
        time.sleep(5)
        clr()

    elif menu == "ka_terminal" and not is_admin():
        print(Fore.RED + T("ka_terminal: administrators only") + Fore.RESET)
        time.sleep(1)
        clr()

    elif menu == "ka_terminal":
        print("Welcome to Kardana Terminal! (type 'exit' to quit)")
        while True:
            cmd = input(f"[ {USER}@Kardana ] >> ").strip()
            if cmd == "exit":
                clr()
                break
            os.system(cmd)

    elif menu.isdigit() and 3 <= int(menu) <= len(installed_apps) + 2:
        idx      = int(menu) - 3
        app_name = list(installed_apps.keys())[idx]
        run_application(app_name, installed_apps)
        time.sleep(2)
        clr()

    elif menu.strip() == "":
        _quiet = True   # empty Enter: do not clear or redraw anything

    else:
        clr()

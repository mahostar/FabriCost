import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import json
import sqlite3
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
import io


def get_settings_path():
    """Return a writable settings path (works for PyInstaller onefile too)."""
    # Prefer Windows roaming AppData; fallback to user home.
    appdata = os.environ.get("APPDATA")
    base_dir = Path(appdata) if appdata else Path.home()
    settings_dir = base_dir / "3dPrix"
    try:
        settings_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return settings_dir / "settings.json"


SETTINGS_PATH = get_settings_path()
SETTINGS_DB_PATH = SETTINGS_PATH.with_suffix(".db")

APP_BRAND_NAME = "FabriCost"


def get_asset_path(name: str) -> Path:
    """
    Resolve an asset path that works both in a normal Python environment and
    when bundled with PyInstaller (onefile/onedir).
    """
    base_dir = getattr(sys, "_MEIPASS", None)
    if base_dir:
        return Path(base_dir) / name
    return Path(__file__).resolve().parent / name


def _copy_image_to_clipboard(img: Image.Image) -> bool:
    """
    Try to copy a PIL image to the Windows clipboard so it can be pasted
    directly into chat applications (WhatsApp, etc.).

    Returns True on success, False if the operation is not available.
    """
    try:
        from io import BytesIO
        import win32clipboard

        # Convert the image to DIB format (BMP without the 14‑byte file header).
        output = BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        finally:
            win32clipboard.CloseClipboard()
        return True
    except Exception:
        # pywin32 not installed or clipboard operation failed.
        return False

I18N = {
    "fr": {
        "app_title": "FabriCost",
        "language": "Langue",
        "input_title": "Calculateur de prix - Ajouter des pièces",
        "rules_title": "Règles de tarification",
        "add_piece_section": "Ajouter une nouvelle pièce",
        "grams": "Grammes :",
        "hours": "Heures :",
        "minutes": "Minutes :",
        "add_piece": "Ajouter",
        "update_piece": "Modifier la pièce {id}",
        "added_pieces": "Pièces ajoutées",
        "no_pieces": "Aucune pièce ajoutée",
        "calculate_all": "Calculer toutes les pièces",
        "results_title": "Résultats du calcul",
        "back": "Retour",
        "menu": "Menu",
        "pdf_detailed": "Générer PDF détaillé",
        "pdf_simple": "Générer PDF simple (prix seulement)",
        "copy": "Copier",
        "receipt_image": "Reçu (image)",
        "summary": "TOTAL : {total:.2f} DT    TEMPS : {time}",
        "piece": "Pièce",
        "weight": "Poids",
        "time": "Temps",
        "gram_price": "Prix du filament",
        "time_price": "Prix du temps",
        "exceeded_suffix": " (dépassement)",
        "subtotal": "Sous-total",
        "markup": "Marge",
        "final_price": "Prix final",
        "final_price_label": "Prix final :",
        "rule_gram_price": "Prix par gramme (DT) :",
        "rule_normal_hour": "Prix horaire normal (DT) :",
        "rule_exceed_hour": "Prix horaire (après seuil) (DT) :",
        "rule_threshold": "Seuil (heures) :",
        "rule_markup": "Marge (%) :",
        "error": "Erreur",
        "warning": "Avertissement",
        "confirm": "Confirmation",
        "invalid_numbers": "Veuillez saisir des nombres valides !",
        "need_piece": "Veuillez ajouter au moins une pièce !",
        "confirm_delete": "Supprimer la pièce {id} ?",
        "copied": "Copié",
        "copied_msg": "Les détails de la pièce {id} ont été copiés dans le presse-papiers.",
        "success": "Succès",
        "calc_first": "Veuillez d'abord calculer les pièces !",
        "img_saved": "Image enregistrée dans :\n{path}",
        "img_copied": "Image copiée dans le presse-papiers.",
        "img_copy_failed": "Impossible de copier l'image dans le presse-papiers. Elle sera enregistrée dans un fichier.",
        "pdf_saved": "PDF enregistré dans :\n{path}",
        "unexpected_error": "Erreur inattendue",
        "unexpected_error_msg": "Une erreur inattendue est survenue :\n{err}\n\nConsultez la console pour le détail.",
        "quote_title": "Devis impression 3D",
        "quote_title_laser": "Devis découpe laser",
        "pricing_rules": "Règles de tarification :",
        "total": "TOTAL",
        "restore_defaults": "Restaurer les valeurs par défaut",
        "brand_tagline": "Calculateur 3D & Laser",
        "about_title": "À propos de FabriCost",
        "about_body": "FabriCost\nAuteur : Mahou\n\nCalculateur de prix pour impression 3D et découpe laser.",
    },
    "en": {
        "app_title": "FabriCost",
        "language": "Language",
        "input_title": "Price Calculator - Add Pieces",
        "rules_title": "Pricing Rules",
        "add_piece_section": "Add New Piece",
        "grams": "Grams:",
        "hours": "Hours:",
        "minutes": "Minutes:",
        "add_piece": "Add",
        "update_piece": "Update Piece {id}",
        "added_pieces": "Added Pieces",
        "no_pieces": "No pieces added yet",
        "calculate_all": "Calculate All Pieces",
        "results_title": "Calculation Results",
        "back": "Back",
        "menu": "Menu",
        "pdf_detailed": "Generate Detailed PDF",
        "pdf_simple": "Generate Simple PDF (Prices Only)",
        "copy": "Copy",
        "receipt_image": "Receipt Image",
        "summary": "TOTAL: {total:.2f} DT    TIME: {time}",
        "piece": "Piece",
        "weight": "Weight",
        "time": "Time",
        "gram_price": "Gramage Price",
        "time_price": "Time Price",
        "exceeded_suffix": " (exceeded)",
        "subtotal": "Subtotal",
        "markup": "Markup",
        "final_price": "Final Price",
        "final_price_label": "Final Price:",
        "rule_gram_price": "Gram Price (DT):",
        "rule_normal_hour": "Normal Hour Price (DT):",
        "rule_exceed_hour": "Exceed Hour Price (DT):",
        "rule_threshold": "Hour Threshold:",
        "rule_markup": "Markup (%):",
        "error": "Error",
        "warning": "Warning",
        "confirm": "Confirm",
        "invalid_numbers": "Please enter valid numbers!",
        "need_piece": "Please add at least one piece!",
        "confirm_delete": "Delete Piece {id}?",
        "copied": "Copied",
        "copied_msg": "Piece {id} details copied to clipboard!",
        "success": "Success",
        "calc_first": "Please calculate pieces first!",
        "img_saved": "Image saved to:\n{path}",
        "img_copied": "Image copied to clipboard.",
        "img_copy_failed": "Could not copy image to clipboard. It will be saved to a file instead.",
        "pdf_saved": "PDF saved to:\n{path}",
        "unexpected_error": "Unexpected error",
        "unexpected_error_msg": "An unexpected error occurred:\n{err}\n\nCheck the console for the full traceback.",
        "quote_title": "3D Print Price Quote",
        "quote_title_laser": "Laser Cutting Quote",
        "pricing_rules": "Pricing Rules:",
        "total": "TOTAL",
        "restore_defaults": "Restore Defaults",
        "brand_tagline": "3D & Laser Calculator",
        "about_title": "About FabriCost",
        "about_body": "FabriCost\nAuthor: Mahou\n\nPrice calculator for 3D printing and laser cutting.",
    },
}

LANG_DISPLAY = {"fr": "Français", "en": "English"}
LANG_CODE = {"Français": "fr", "English": "en"}


def load_settings():
    """Load settings from a local SQLite database (with JSON fallback for legacy data)."""
    data = {}
    try:
        conn = sqlite3.connect(SETTINGS_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        conn.commit()

        # If the DB is empty but a legacy JSON file exists, migrate it once.
        cur.execute("SELECT COUNT(*) FROM settings")
        count = cur.fetchone()[0]
        if count == 0 and SETTINGS_PATH.exists():
            try:
                legacy = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
                for k, v in legacy.items():
                    cur.execute(
                        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                        (k, json.dumps(v, ensure_ascii=False)),
                    )
                conn.commit()
            except Exception:
                # Ignore migration errors and continue with an empty DB.
                pass

        cur.execute("SELECT key, value FROM settings")
        rows = cur.fetchall()
        for key, raw in rows:
            try:
                data[key] = json.loads(raw)
            except Exception:
                data[key] = raw
    except Exception:
        # Non-fatal: fall back to empty settings.
        data = {}
    finally:
        try:
            conn.close()
        except Exception:
            pass
    return data


def save_settings(data):
    """Persist the full settings dict into the local SQLite DB."""
    try:
        conn = sqlite3.connect(SETTINGS_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        for key, value in data.items():
            cur.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, json.dumps(value, ensure_ascii=False)),
            )
        conn.commit()
    except Exception:
        # Non-fatal: app can still run without persistence.
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


# Factory defaults for calculators (used on first run and for 'restore defaults').
FACTORY_3D_RULES = {
    "gram_price": 0.1,
    "normal_hour_price": 3.0,
    "exceed_hour_price": 2.0,
    "exceed_threshold": 10.0,
    "markup_percent": 20.0,
}

FACTORY_LASER_RULES = {
    "normal_hour_price": 30.0,
    "markup_percent": 5.0,
}


class PrintCalculatorApp:
    def __init__(self, root):
        self.root = root

        self.settings = load_settings()
        default_lang = self.settings.get("language", "fr")
        if default_lang not in I18N:
            default_lang = "fr"
        self.lang_var = tk.StringVar(value=default_lang)

        self.root.title(self.t("app_title"))
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f4f8")

        # App mode: "3d" or "laser"
        self.mode = None

        # Default rules for calculators, loaded from settings with factory fallbacks.
        self.default_3d_rules = {
            "gram_price": float(self.settings.get("3d_gram_price", FACTORY_3D_RULES["gram_price"])),
            "normal_hour_price": float(
                self.settings.get("3d_normal_hour_price", FACTORY_3D_RULES["normal_hour_price"])
            ),
            "exceed_hour_price": float(
                self.settings.get("3d_exceed_hour_price", FACTORY_3D_RULES["exceed_hour_price"])
            ),
            "exceed_threshold": float(
                self.settings.get("3d_exceed_threshold", FACTORY_3D_RULES["exceed_threshold"])
            ),
            "markup_percent": float(self.settings.get("3d_markup_percent", FACTORY_3D_RULES["markup_percent"])),
        }

        self.default_laser_rules = {
            "normal_hour_price": float(
                self.settings.get("laser_normal_hour_price", FACTORY_LASER_RULES["normal_hour_price"])
            ),
            "markup_percent": float(
                self.settings.get("laser_markup_percent", FACTORY_LASER_RULES["markup_percent"])
            ),
        }

        # Rule variables (configured per mode)
        self.gram_price = tk.DoubleVar(value=self.default_3d_rules["gram_price"])
        self.normal_hour_price = tk.DoubleVar(value=self.default_3d_rules["normal_hour_price"])
        self.exceed_hour_price = tk.DoubleVar(value=self.default_3d_rules["exceed_hour_price"])
        self.exceed_threshold = tk.DoubleVar(value=self.default_3d_rules["exceed_threshold"])
        self.markup_percent = tk.DoubleVar(value=self.default_3d_rules["markup_percent"])
        
        # Pieces list
        self.pieces = []

        # Editing state (input page)
        self.editing_piece = None

        # Results UI state
        self.result_cards = []
        self.summary_var = tk.StringVar(value="")
        self._layout_job = None
        
        # Current page inside calculator ("input" or "results")
        self.current_page = None

        # Main container that will host splash, menu, and calculator pages
        self.main_container = tk.Frame(self.root, bg="#f0f4f8")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Branding assets (logo for splash/menu, icon for window/taskbar)
        self.logo_large = None
        self.logo_small = None
        self._icon_image = None
        self._load_branding_assets()

        # Start with splash screen
        self.show_splash_screen()

    def _load_branding_assets(self):
        """Load logo image in different sizes and set the window icon if possible."""
        # --- Window icon (taskbar / alt-tab / title bar) ---
        # Prefer the .ico file for best Windows integration.
        try:
            ico_path = get_asset_path("FabriCost_Icon.ico")
            if ico_path.exists():
                self.root.iconbitmap(default=str(ico_path))
        except Exception:
            pass

        # --- Logo images for splash / menu ---
        try:
            logo_path = get_asset_path("FabriCost_Logo.png")
            img = Image.open(logo_path).convert("RGBA")

            # Large logo for splash / menu
            self.logo_large = ImageTk.PhotoImage(img.resize((160, 160), Image.LANCZOS))
            # Small logo (kept for possible future use)
            self.logo_small = ImageTk.PhotoImage(img.resize((36, 36), Image.LANCZOS))

            # Fallback icon via iconphoto (in case .ico was not available)
            self._icon_image = tk.PhotoImage(file=str(logo_path))
            try:
                self.root.iconphoto(True, self._icon_image)
            except Exception:
                pass
        except Exception:
            # If logo cannot be loaded, just continue without it.
            self.logo_large = None
            self.logo_small = None
            self._icon_image = None

    def t(self, key, **kwargs):
        lang = self.lang_var.get() if hasattr(self, "lang_var") else "fr"
        text = I18N.get(lang, I18N["fr"]).get(key, I18N["en"].get(key, key))
        try:
            return text.format(**kwargs)
        except Exception:
            return text

    def set_language(self, lang_code):
        if lang_code not in I18N:
            lang_code = "fr"
        if self.lang_var.get() == lang_code:
            return
        self.lang_var.set(lang_code)
        self.save_current_settings()
        self.apply_language()

    def apply_language(self):
        """Rebuild UI using the currently selected language."""
        self.root.title(self.t("app_title"))

        # If we are not in a calculator yet (splash / menu), nothing to rebuild.
        if self.mode not in ("3d", "laser"):
            return

        previous_page = self.current_page
        had_results = any(p.get("result") for p in self.pieces)

        # Rebuild calculator widgets so we don't have to update every label manually.
        self.create_ui()
        self.update_pieces_list()

        if previous_page == "results" and had_results:
            self.calculate_and_show_results()
        else:
            self.show_page("input")

    def reset_calculator_state(self):
        """Reset state when switching between 3D and Laser calculators."""
        self.pieces = []
        self.editing_piece = None
        self.result_cards = []
        self.summary_var.set("")
        self.current_page = "input"

    def save_current_settings(self):
        """Persist language and current calculator rules into the settings DB."""
        # Always store current language
        self.settings["language"] = self.lang_var.get()

        # Update defaults from the currently active calculator UI
        if self.mode == "3d":
            self.default_3d_rules["gram_price"] = float(self.gram_price.get())
            self.default_3d_rules["normal_hour_price"] = float(self.normal_hour_price.get())
            self.default_3d_rules["exceed_hour_price"] = float(self.exceed_hour_price.get())
            self.default_3d_rules["exceed_threshold"] = float(self.exceed_threshold.get())
            self.default_3d_rules["markup_percent"] = float(self.markup_percent.get())
        elif self.mode == "laser":
            self.default_laser_rules["normal_hour_price"] = float(self.normal_hour_price.get())
            self.default_laser_rules["markup_percent"] = float(self.markup_percent.get())

        # Mirror both calculators' defaults into the flat settings dict
        self.settings["3d_gram_price"] = self.default_3d_rules["gram_price"]
        self.settings["3d_normal_hour_price"] = self.default_3d_rules["normal_hour_price"]
        self.settings["3d_exceed_hour_price"] = self.default_3d_rules["exceed_hour_price"]
        self.settings["3d_exceed_threshold"] = self.default_3d_rules["exceed_threshold"]
        self.settings["3d_markup_percent"] = self.default_3d_rules["markup_percent"]

        self.settings["laser_normal_hour_price"] = self.default_laser_rules["normal_hour_price"]
        self.settings["laser_markup_percent"] = self.default_laser_rules["markup_percent"]

        save_settings(self.settings)

    def restore_defaults(self):
        """Reset pricing rules to factory defaults for the current calculator mode."""
        if self.mode == "3d":
            self.default_3d_rules = FACTORY_3D_RULES.copy()
            self.gram_price.set(self.default_3d_rules["gram_price"])
            self.normal_hour_price.set(self.default_3d_rules["normal_hour_price"])
            self.exceed_hour_price.set(self.default_3d_rules["exceed_hour_price"])
            self.exceed_threshold.set(self.default_3d_rules["exceed_threshold"])
            self.markup_percent.set(self.default_3d_rules["markup_percent"])
        elif self.mode == "laser":
            self.default_laser_rules = FACTORY_LASER_RULES.copy()
            # Laser mode ignores grams; only hour price and margin matter.
            self.normal_hour_price.set(self.default_laser_rules["normal_hour_price"])
            self.markup_percent.set(self.default_laser_rules["markup_percent"])

        self.save_current_settings()

    def back_to_menu(self):
        """Return from any calculator page back to the main mode selection menu."""
        # Persist any current settings before leaving the calculator.
        self.save_current_settings()
        self.reset_calculator_state()
        self.mode = None
        self.show_mode_selection()

    def show_splash_screen(self):
        """Initial splash screen with branding."""
        for child in self.main_container.winfo_children():
            child.destroy()

        self.mode = None
        self.current_page = None

        splash = tk.Frame(self.main_container, bg="#111827")
        splash.pack(fill=tk.BOTH, expand=True)

        # Logo (if available)
        if self.logo_large is not None:
            logo_label = tk.Label(splash, image=self.logo_large, bg="#111827")
            logo_label.place(relx=0.5, rely=0.4, anchor="center")
            title_y = 0.65
        else:
            title_y = 0.5

        title = tk.Label(
            splash,
            text=self.t("app_title"),
            font=("Helvetica", 32, "bold"),
            bg="#111827",
            fg="white",
        )
        title.place(relx=0.5, rely=title_y, anchor="center")

        subtitle = tk.Label(
            splash,
            text=self.t("brand_tagline"),
            font=("Helvetica", 16),
            bg="#111827",
            fg="#e5e7eb",
        )
        subtitle.place(relx=0.5, rely=title_y + 0.08, anchor="center")

        # After a short delay, move to the mode selection screen.
        self.root.after(1500, self.show_mode_selection)

    def show_mode_selection(self):
        """Second screen with buttons to choose 3D or Laser calculator."""
        for child in self.main_container.winfo_children():
            child.destroy()

        self.current_page = None

        menu = tk.Frame(self.main_container, bg="#f0f4f8")
        menu.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(menu, bg="white", bd=1, relief=tk.RAISED)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Brand area (logo + name)
        brand_frame = tk.Frame(card, bg="white")
        brand_frame.pack(padx=60, pady=(40, 10))

        if self.logo_large is not None:
            logo_label = tk.Label(brand_frame, image=self.logo_large, bg="white")
            logo_label.pack()

        title = tk.Label(
            brand_frame,
            text=self.t("app_title"),
            font=("Helvetica", 24, "bold"),
            bg="white",
            fg="#111827",
        )
        title.pack(pady=(10, 0))

        tagline = tk.Label(
            brand_frame,
            text=self.t("brand_tagline"),
            font=("Helvetica", 11),
            bg="white",
            fg="#6b7280",
        )
        tagline.pack()

        subtitle = tk.Label(
            card,
            text="Choose a calculator",
            font=("Helvetica", 12),
            bg="white",
            fg="#6b7280",
        )
        subtitle.pack(padx=60, pady=(0, 20))

        buttons_frame = tk.Frame(card, bg="white")
        buttons_frame.pack(padx=60, pady=(0, 30), fill=tk.X)

        btn_3d = tk.Button(
            buttons_frame,
            text="3D calculator",
            command=self.start_3d_calculator,
            bg="#4f46e5",
            fg="white",
            font=("Helvetica", 13, "bold"),
            relief=tk.FLAT,
            padx=40,
            pady=14,
            cursor="hand2",
        )
        btn_3d.pack(fill=tk.X, pady=(0, 10))

        btn_laser = tk.Button(
            buttons_frame,
            text="Laser calculator",
            command=self.start_laser_calculator,
            bg="#10b981",
            fg="white",
            font=("Helvetica", 13, "bold"),
            relief=tk.FLAT,
            padx=40,
            pady=14,
            cursor="hand2",
        )
        btn_laser.pack(fill=tk.X)

        # About button (shows author / app info)
        about_btn = tk.Button(
            card,
            text=self.t("about_title"),
            command=self.show_about,
            bg="#e5e7eb",
            fg="#111827",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
        )
        about_btn.pack(pady=(0, 20))

    def show_about(self):
        """Display a simple About dialog with author information."""
        messagebox.showinfo(self.t("about_title"), self.t("about_body"))

    def start_3d_calculator(self):
        """Launch the original 3D print price calculator."""
        self.mode = "3d"
        # Restore 3D defaults
        self.gram_price.set(self.default_3d_rules["gram_price"])
        self.normal_hour_price.set(self.default_3d_rules["normal_hour_price"])
        self.exceed_hour_price.set(self.default_3d_rules["exceed_hour_price"])
        self.exceed_threshold.set(self.default_3d_rules["exceed_threshold"])
        self.markup_percent.set(self.default_3d_rules["markup_percent"])

        self.reset_calculator_state()
        self.create_ui()

    def start_laser_calculator(self):
        """Launch the Laser calculator (time-based only)."""
        self.mode = "laser"
        # Restore Laser defaults (time-based only).
        self.gram_price.set(0.0)
        self.normal_hour_price.set(self.default_laser_rules["normal_hour_price"])
        self.exceed_hour_price.set(self.default_laser_rules["normal_hour_price"])
        self.exceed_threshold.set(9999.0)
        self.markup_percent.set(self.default_laser_rules["markup_percent"])

        self.reset_calculator_state()
        self.create_ui()

    def create_ui(self):
        # Clear anything currently shown (e.g., splash/menu or previous calculator)
        for child in self.main_container.winfo_children():
            child.destroy()

        # Create both pages
        self.create_input_page()
        self.create_results_page()
        
        # Show input page first
        self.show_page("input")
        
    def create_input_page(self):
        self.input_page = tk.Frame(self.main_container, bg="#f0f4f8")
        
        # Header
        header_frame = tk.Frame(self.input_page, bg="#4f46e5", height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Button to go back to main menu (mode selection)
        menu_btn = tk.Button(
            header_frame,
            text=self.t("menu"),
            command=self.back_to_menu,
            bg="#6366f1",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        menu_btn.pack(side=tk.LEFT, padx=20, pady=20)

        title = tk.Label(
            header_frame,
            text=self.t("input_title"),
            font=("Helvetica", 24, "bold"),
            bg="#4f46e5",
            fg="white",
        )
        title.place(relx=0.5, rely=0.5, anchor="center")

        lang_frame = tk.Frame(header_frame, bg="#4f46e5")
        lang_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        tk.Label(lang_frame, text=self.t("language"), bg="#4f46e5", fg="white", font=("Helvetica", 11, "bold")).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        lang_combo = ttk.Combobox(lang_frame, state="readonly", width=10, values=list(LANG_CODE.keys()))
        lang_combo.set(LANG_DISPLAY.get(self.lang_var.get(), "Français"))
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.set_language(LANG_CODE.get(lang_combo.get(), "fr")))
        lang_combo.pack(side=tk.LEFT)
        
        # Content area
        content_frame = tk.Frame(self.input_page, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Left side - Rules
        left_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20), expand=True)
        
        rules_label = tk.Label(left_frame, text=self.t("rules_title"), 
                              font=("Helvetica", 18, "bold"), bg="white", fg="#1f2937")
        rules_label.pack(pady=(30, 20), padx=30, anchor=tk.W)
        
        rules_frame = tk.Frame(left_frame, bg="white")
        rules_frame.pack(fill=tk.X, padx=30, pady=10)

        if self.mode == "laser":
            # Laser mode: only hourly price and margin, both editable (defaults set when mode starts).
            tk.Label(
                rules_frame,
                text=self.t("rule_normal_hour"),
                font=("Helvetica", 12),
                bg="white",
            ).grid(row=0, column=0, sticky=tk.W, pady=10)
            hour_entry = tk.Entry(
                rules_frame,
                textvariable=self.normal_hour_price,
                font=("Helvetica", 12),
                width=20,
            )
            hour_entry.grid(row=0, column=1, pady=10, padx=(15, 0))

            tk.Label(
                rules_frame,
                text=self.t("rule_markup"),
                font=("Helvetica", 12),
                bg="white",
            ).grid(row=1, column=0, sticky=tk.W, pady=10)
            markup_entry = tk.Entry(
                rules_frame,
                textvariable=self.markup_percent,
                font=("Helvetica", 12),
                width=20,
            )
            markup_entry.grid(row=1, column=1, pady=10, padx=(15, 0))
        else:
            # 3D mode: full pricing rules.
            self.create_rule_input(rules_frame, self.t("rule_gram_price"), self.gram_price, 0)
            self.create_rule_input(rules_frame, self.t("rule_normal_hour"), self.normal_hour_price, 1)
            self.create_rule_input(rules_frame, self.t("rule_exceed_hour"), self.exceed_hour_price, 2)
            self.create_rule_input(rules_frame, self.t("rule_threshold"), self.exceed_threshold, 3)
            self.create_rule_input(rules_frame, self.t("rule_markup"), self.markup_percent, 4)

        # Rules actions (e.g. restore defaults)
        actions_frame = tk.Frame(left_frame, bg="white")
        actions_frame.pack(fill=tk.X, padx=30, pady=(0, 10))

        restore_btn = tk.Button(
            actions_frame,
            text=self.t("restore_defaults"),
            command=self.restore_defaults,
            bg="#e5e7eb",
            fg="#111827",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2",
        )
        restore_btn.pack(anchor=tk.W)

        # Add Piece Section
        separator = tk.Frame(left_frame, height=2, bg="#e5e7eb")
        separator.pack(fill=tk.X, padx=30, pady=30)
        
        add_label = tk.Label(left_frame, text=self.t("add_piece_section"), 
                            font=("Helvetica", 18, "bold"), bg="white", fg="#1f2937")
        add_label.pack(pady=(10, 20), padx=30, anchor=tk.W)
        
        add_frame = tk.Frame(left_frame, bg="white")
        add_frame.pack(fill=tk.X, padx=30, pady=10)

        # Build piece inputs; in laser mode we hide grams entirely.
        row_idx = 0
        if self.mode != "laser":
            tk.Label(add_frame, text=self.t("grams"), font=("Helvetica", 12), bg="white").grid(
                row=row_idx, column=0, sticky=tk.W, pady=8
            )
            self.gram_entry = tk.Entry(add_frame, font=("Helvetica", 12), width=25)
            self.gram_entry.grid(row=row_idx, column=1, pady=8, padx=(15, 0))
            row_idx += 1
        else:
            self.gram_entry = None

        tk.Label(add_frame, text=self.t("hours"), font=("Helvetica", 12), bg="white").grid(
            row=row_idx, column=0, sticky=tk.W, pady=8
        )
        self.hours_entry = tk.Entry(add_frame, font=("Helvetica", 12), width=25)
        self.hours_entry.grid(row=row_idx, column=1, pady=8, padx=(15, 0))
        row_idx += 1

        tk.Label(add_frame, text=self.t("minutes"), font=("Helvetica", 12), bg="white").grid(
            row=row_idx, column=0, sticky=tk.W, pady=8
        )
        self.minutes_entry = tk.Entry(add_frame, font=("Helvetica", 12), width=25)
        self.minutes_entry.grid(row=row_idx, column=1, pady=8, padx=(15, 0))
        row_idx += 1

        self.add_piece_btn = tk.Button(
            add_frame,
            text=self.t("add_piece"),
            command=self.add_or_update_piece,
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
        )
        self.add_piece_btn.grid(row=row_idx, column=0, columnspan=2, pady=20)
        
        # Right side - Pieces list
        right_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        pieces_label = tk.Label(right_frame, text=self.t("added_pieces"), 
                               font=("Helvetica", 18, "bold"), bg="white", fg="#1f2937")
        pieces_label.pack(pady=(30, 20), padx=30, anchor=tk.W)
        
        # Scrollable list
        list_container = tk.Frame(right_frame, bg="white")
        list_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.pieces_canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)
        pieces_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.pieces_canvas.yview)
        self.pieces_list_frame = tk.Frame(self.pieces_canvas, bg="white")
        
        self.pieces_list_frame.bind(
            "<Configure>",
            lambda e: self.pieces_canvas.configure(scrollregion=self.pieces_canvas.bbox("all"))
        )
        
        self.pieces_canvas.create_window((0, 0), window=self.pieces_list_frame, anchor="nw")
        self.pieces_canvas.configure(yscrollcommand=pieces_scrollbar.set)
        
        self.pieces_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pieces_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Calculate button at bottom
        calc_frame = tk.Frame(right_frame, bg="white")
        calc_frame.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        calc_btn = tk.Button(calc_frame, text=self.t("calculate_all"), command=self.calculate_and_show_results,
                            bg="#4f46e5", fg="white", font=("Helvetica", 14, "bold"),
                            relief=tk.FLAT, padx=40, pady=15, cursor="hand2")
        calc_btn.pack(fill=tk.X)
        
    def create_results_page(self):
        self.results_page = tk.Frame(self.main_container, bg="#f0f4f8")
        
        # Header with back button
        header_frame = tk.Frame(self.results_page, bg="#4f46e5", height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Button to go back to main menu (mode selection)
        menu_btn = tk.Button(
            header_frame,
            text=self.t("menu"),
            command=self.back_to_menu,
            bg="#6366f1",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        menu_btn.pack(side=tk.LEFT, padx=(20, 5), pady=20)

        back_btn = tk.Button(header_frame, text=self.t("back"), command=lambda: self.show_page("input"),
                            bg="#6366f1", fg="white", font=("Helvetica", 11, "bold"),
                            relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=5, pady=20)
        
        title = tk.Label(header_frame, text=self.t("results_title"), 
                        font=("Helvetica", 24, "bold"), bg="#4f46e5", fg="white")
        title.pack(side=tk.LEFT, padx=20, pady=20)

        summary_label = tk.Label(
            header_frame,
            textvariable=self.summary_var,
            font=("Helvetica", 16, "bold"),
            bg="#4f46e5",
            fg="white",
            justify=tk.RIGHT,
        )
        summary_label.pack(side=tk.RIGHT, padx=25, pady=20)

        lang_frame = tk.Frame(header_frame, bg="#4f46e5")
        lang_frame.pack(side=tk.RIGHT, padx=15, pady=20)
        tk.Label(lang_frame, text=self.t("language"), bg="#4f46e5", fg="white", font=("Helvetica", 11, "bold")).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        lang_combo = ttk.Combobox(lang_frame, state="readonly", width=10, values=list(LANG_CODE.keys()))
        lang_combo.set(LANG_DISPLAY.get(self.lang_var.get(), "Français"))
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.set_language(LANG_CODE.get(lang_combo.get(), "fr")))
        lang_combo.pack(side=tk.LEFT)
        
        # Content
        content_frame = tk.Frame(self.results_page, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Action buttons
        action_frame = tk.Frame(content_frame, bg="#f0f4f8")
        action_frame.pack(fill=tk.X, pady=(0, 20))
        
        pdf_detailed_btn = tk.Button(action_frame, text=self.t("pdf_detailed"), command=self.generate_detailed_pdf,
                           bg="#8b5cf6", fg="white", font=("Helvetica", 12, "bold"),
                           relief=tk.FLAT, padx=30, pady=12, cursor="hand2")
        pdf_detailed_btn.pack(side=tk.LEFT, padx=5)
        
        pdf_simple_btn = tk.Button(action_frame, text=self.t("pdf_simple"), command=self.generate_simple_pdf,
                           bg="#06b6d4", fg="white", font=("Helvetica", 12, "bold"),
                           relief=tk.FLAT, padx=30, pady=12, cursor="hand2")
        pdf_simple_btn.pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_container = tk.Frame(content_frame, bg="#f0f4f8")
        results_container.pack(fill=tk.BOTH, expand=True)
        
        self.results_canvas = tk.Canvas(results_container, bg="#f0f4f8", highlightthickness=0)
        results_scrollbar = tk.Scrollbar(results_container, orient="vertical", command=self.results_canvas.yview)
        self.results_scrollable_frame = tk.Frame(self.results_canvas, bg="#f0f4f8")
        
        self.results_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mousewheel
        self.results_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Responsive grid layout for cards
        self.results_canvas.bind("<Configure>", self._schedule_layout_results)
        
    def _on_mousewheel(self, event):
        self.results_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def show_page(self, page_name):
        if page_name == "input":
            self.results_page.pack_forget()
            self.input_page.pack(fill=tk.BOTH, expand=True)
            self.current_page = "input"
        else:
            self.input_page.pack_forget()
            self.results_page.pack(fill=tk.BOTH, expand=True)
            self.current_page = "results"
            
    def create_rule_input(self, parent, label, variable, row):
        tk.Label(parent, text=label, font=("Helvetica", 12), bg="white").grid(row=row, column=0, sticky=tk.W, pady=10)
        entry = tk.Entry(parent, textvariable=variable, font=("Helvetica", 12), width=20)
        entry.grid(row=row, column=1, pady=10, padx=(15, 0))
        
    def add_or_update_piece(self):
        try:
            if self.mode == "laser":
                grams = 0.0
            else:
                grams = float(self.gram_entry.get())

            hours_text = self.hours_entry.get().strip()
            minutes_text = self.minutes_entry.get().strip()

            # If user leaves one of the fields empty, treat it as 0.
            # Only error if BOTH hours and minutes are empty.
            if hours_text == "" and minutes_text == "":
                raise ValueError

            hours = float(hours_text) if hours_text else 0.0
            minutes = float(minutes_text) if minutes_text else 0.0

            if self.editing_piece is None:
                piece = {
                    'id': len(self.pieces) + 1,
                    'grams': grams,
                    'hours': hours,
                    'minutes': minutes,
                    'result': None,
                }
                self.pieces.append(piece)
            else:
                # Update existing piece
                self.editing_piece['grams'] = grams
                self.editing_piece['hours'] = hours
                self.editing_piece['minutes'] = minutes
                self.editing_piece['result'] = None

                self.editing_piece = None
                self.add_piece_btn.configure(text=self.t("add_piece"), bg="#10b981", activebackground="#059669")

            # Clear entries
            if self.mode != "laser" and self.gram_entry is not None:
                self.gram_entry.delete(0, tk.END)
            self.hours_entry.delete(0, tk.END)
            self.minutes_entry.delete(0, tk.END)

            self.update_pieces_list()

        except ValueError:
            messagebox.showerror(self.t("error"), self.t("invalid_numbers"))

    def start_edit_piece(self, piece):
        """Load an existing piece into the inputs for editing."""
        self.editing_piece = piece
        if self.mode != "laser" and self.gram_entry is not None:
            self.gram_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        if self.mode != "laser" and self.gram_entry is not None:
            self.gram_entry.insert(0, str(piece['grams']))
        self.hours_entry.insert(0, str(piece['hours']))
        self.minutes_entry.insert(0, str(piece['minutes']))
        self.add_piece_btn.configure(text=self.t("update_piece", id=piece['id']), bg="#f59e0b", activebackground="#d97706")

    def _format_time_h_min(self, total_hours):
        """Format decimal hours as `50h8min`."""
        total_minutes = int(round(float(total_hours) * 60))
        h, m = divmod(total_minutes, 60)
        return f"{h}h{m}min"
            
    def update_pieces_list(self):
        # Clear existing list
        for widget in self.pieces_list_frame.winfo_children():
            widget.destroy()
            
        if not self.pieces:
            no_pieces_label = tk.Label(self.pieces_list_frame, text=self.t("no_pieces"), 
                                       font=("Helvetica", 12), bg="white", fg="#9ca3af")
            no_pieces_label.pack(pady=20)
            return
            
        for piece in self.pieces:
            piece_frame = tk.Frame(self.pieces_list_frame, bg="#f9fafb", relief=tk.FLAT, bd=1)
            piece_frame.pack(fill=tk.X, pady=5, padx=5)
            
            info_frame = tk.Frame(piece_frame, bg="#f9fafb")
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
            
            tk.Label(info_frame, text=f"{self.t('piece')} {piece['id']}", font=("Helvetica", 11, "bold"),
                    bg="#f9fafb", fg="#1f2937").pack(anchor=tk.W)
            if self.mode == "laser":
                summary_text = f"{piece['hours']}h {piece['minutes']}min"
            else:
                summary_text = f"{piece['grams']}g | {piece['hours']}h {piece['minutes']}min"
            tk.Label(
                info_frame,
                text=summary_text,
                font=("Helvetica", 10),
                bg="#f9fafb",
                fg="#6b7280",
            ).pack(anchor=tk.W)

            edit_btn = tk.Button(
                piece_frame,
                text="Edit",
                command=lambda p=piece: self.start_edit_piece(p),
                bg="#3b82f6",
                activebackground="#2563eb",
                fg="white",
                activeforeground="white",
                font=("Helvetica", 10, "bold"),
                relief=tk.FLAT,
                padx=8,
                pady=2,
                cursor="hand2",
            )
            edit_btn.pack(side=tk.RIGHT, padx=(0, 8))
            
            delete_btn = tk.Button(
                piece_frame,
                text="Delete",
                command=lambda p=piece: self.delete_piece(p),
                bg="#ef4444",
                activebackground="#dc2626",
                fg="white",
                activeforeground="white",
                font=("Helvetica", 10, "bold"),
                relief=tk.FLAT,
                padx=8,
                pady=2,
                cursor="hand2",
            )
            delete_btn.pack(side=tk.RIGHT, padx=10)
            
    def delete_piece(self, piece):
        if messagebox.askyesno(self.t("confirm"), self.t("confirm_delete", id=piece['id'])):
            if self.editing_piece is piece:
                self.editing_piece = None
                self.add_piece_btn.configure(text=self.t("add_piece"), bg="#10b981", activebackground="#059669")
            self.pieces.remove(piece)
            # Renumber pieces
            for i, p in enumerate(self.pieces):
                p['id'] = i + 1
            self.update_pieces_list()
            
    def calculate_and_show_results(self):
        if not self.pieces:
            messagebox.showwarning(self.t("warning"), self.t("need_piece"))
            return

        # Persist current settings (language + rules) when user runs a calculation.
        self.save_current_settings()

        # Calculate all pieces
        for piece in self.pieces:
            result = self.calculate_price(piece['grams'], piece['hours'], piece['minutes'])
            piece['result'] = result

        # Header summary (total price + total time)
        total_price = sum(p['result']['final_price'] for p in self.pieces if p.get('result'))
        total_hours = sum(p['result']['total_hours'] for p in self.pieces if p.get('result'))
        self.summary_var.set(self.t("summary", total=total_price, time=self._format_time_h_min(total_hours)))
             
        # Clear previous results
        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()

        self.result_cards.clear()
             
        # Display results
        for piece in self.pieces:
            card = self.create_piece_card(piece, piece['result'])
            self.result_cards.append(card)

        self._layout_result_cards()
             
        # Show results page
        self.show_page("results")

    def _schedule_layout_results(self, event=None):
        # Throttle relayout while resizing.
        if self.current_page != "results":
            return
        if self._layout_job is not None:
            try:
                self.root.after_cancel(self._layout_job)
            except Exception:
                pass
        self._layout_job = self.root.after(60, self._layout_result_cards)

    def _layout_result_cards(self):
        self._layout_job = None
        if not self.result_cards:
            return

        # Available width inside the canvas viewport.
        width = self.results_canvas.winfo_width()
        if width <= 1:
            width = self.root.winfo_width()

        # Responsive columns: up to 3 cards per row (as requested).
        card_min_width = 420
        padding = 20
        cols = max(1, min(3, max(1, (width - padding) // (card_min_width + padding))))

        # Configure grid columns.
        for i in range(3):
            self.results_scrollable_frame.grid_columnconfigure(i, weight=1 if i < cols else 0, uniform="cards")

        # Place cards.
        for idx, card in enumerate(self.result_cards):
            card.grid_forget()
            r, c = divmod(idx, cols)
            card.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
        
    def calculate_price(self, grams, hours, minutes):
        total_hours = hours + (minutes / 60)

        if self.mode == "laser":
            # Laser: ignore grams, single hourly rate.
            gram_price = 0.0
            time_price = total_hours * self.normal_hour_price.get()
            exceeded = False
            subtotal = time_price
        else:
            gram_price = grams * self.gram_price.get()

            if total_hours > self.exceed_threshold.get():
                time_price = total_hours * self.exceed_hour_price.get()
                exceeded = True
            else:
                time_price = total_hours * self.normal_hour_price.get()
                exceeded = False

            subtotal = gram_price + time_price

        markup_amount = subtotal * (self.markup_percent.get() / 100)
        final_price = subtotal + markup_amount
        
        return {
            'total_hours': total_hours,
            'gram_price': gram_price,
            'time_price': time_price,
            'exceeded': exceeded,
            'subtotal': subtotal,
            'markup_amount': markup_amount,
            'final_price': final_price
        }
        
    def create_piece_card(self, piece, result):
        card = tk.Frame(self.results_scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        
        # Header
        header = tk.Frame(card, bg="#4f46e5", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"{self.t('piece')} {piece['id']}", font=("Helvetica", 14, "bold"),
                bg="#4f46e5", fg="white").pack(side=tk.LEFT, padx=20, pady=10)
        
        # Content
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Input info
        input_frame = tk.Frame(content, bg="#f9fafb", relief=tk.FLAT, bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        if self.mode == "laser":
            info_text = (
                f"{self.t('time')}: {piece['hours']}h {piece['minutes']}min "
                f"({self._format_time_h_min(result['total_hours'])})"
            )
        else:
            info_text = (
                f"{self.t('weight')}: {piece['grams']}g  |  {self.t('time')}: {piece['hours']}h {piece['minutes']}min "
                f"({self._format_time_h_min(result['total_hours'])})"
            )
        tk.Label(input_frame, text=info_text, font=("Helvetica", 11), bg="#f9fafb", fg="#6b7280").pack(pady=10)
        
        # Calculation details
        if self.mode == "laser":
            details = [
                (
                    f"{self.t('time_price')}:",
                    f"{self._format_time_h_min(result['total_hours'])} × {self.normal_hour_price.get()} DT = {result['time_price']:.2f} DT",
                ),
                (f"{self.t('subtotal')}:", f"{result['subtotal']:.2f} DT"),
                (f"{self.t('markup')} (+{self.markup_percent.get():.0f}%):", f"+{result['markup_amount']:.2f} DT"),
            ]
        else:
            details = [
                (
                    f"{self.t('gram_price')} :",
                    f"{piece['grams']}g × {self.gram_price.get()} DT = {result['gram_price']:.2f} DT",
                ),
                (
                    self.t('time_price') + (self.t('exceeded_suffix') if result['exceeded'] else ":"),
                    f"{self._format_time_h_min(result['total_hours'])} × "
                    f"{self.exceed_hour_price.get() if result['exceeded'] else self.normal_hour_price.get()} DT = "
                    f"{result['time_price']:.2f} DT",
                ),
                (f"{self.t('subtotal')}:", f"{result['subtotal']:.2f} DT"),
                (f"{self.t('markup')} (+{self.markup_percent.get():.0f}%):", f"+{result['markup_amount']:.2f} DT"),
            ]
        
        for label, value in details:
            row = tk.Frame(content, bg="white")
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=label, font=("Helvetica", 10), bg="white", fg="#374151").pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Helvetica", 10, "bold"), bg="white", fg="#1f2937").pack(side=tk.RIGHT)
        
        # Final price
        final_frame = tk.Frame(content, bg="#ecfdf5", relief=tk.FLAT, bd=1)
        final_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(final_frame, text=self.t("final_price_label"), font=("Helvetica", 12, "bold"),
                bg="#ecfdf5", fg="#065f46").pack(side=tk.LEFT, padx=10, pady=12)
        tk.Label(final_frame, text=f"{result['final_price']:.2f} DT", font=("Helvetica", 16, "bold"),
                bg="#ecfdf5", fg="#10b981").pack(side=tk.RIGHT, padx=10, pady=12)
        
        # Buttons
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        copy_btn = tk.Button(btn_frame, text=self.t("copy"), command=lambda p=piece: self.copy_text(p),
                            bg="#3b82f6", fg="white", font=("Helvetica", 10, "bold"),
                            relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        recu_btn = tk.Button(btn_frame, text=self.t("receipt_image"), command=lambda p=piece: self.generate_image(p),
                            bg="#8b5cf6", fg="white", font=("Helvetica", 10, "bold"),
                            relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        recu_btn.pack(side=tk.LEFT, padx=5)

        return card
        
    def copy_text(self, piece):
        result = piece['result']
        if self.mode == "laser":
            text = f"""Piece {piece['id']}
Time: {piece['hours']}h {piece['minutes']}min

Time Price: {result['time_price']:.2f} DT
Subtotal: {result['subtotal']:.2f} DT
Markup (+{self.markup_percent.get():.0f}%): {result['markup_amount']:.2f} DT

Final Price: {result['final_price']:.2f} DT"""
        else:
            text = f"""Piece {piece['id']}
Weight: {piece['grams']}g
Time: {piece['hours']}h {piece['minutes']}min

Gramage Price: {result['gram_price']:.2f} DT
Time Price: {result['time_price']:.2f} DT
Subtotal: {result['subtotal']:.2f} DT
Markup (+{self.markup_percent.get():.0f}%): {result['markup_amount']:.2f} DT

Final Price: {result['final_price']:.2f} DT"""
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo(self.t("copied"), self.t("copied_msg", id=piece['id']))
        
    def generate_image(self, piece):
        result = piece['result']
        
        # Create image with larger size
        img_width, img_height = 700, 550
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 36)
            header_font = ImageFont.truetype("arialbd.ttf", 22)
            normal_font = ImageFont.truetype("arialbd.ttf", 20)
            bold_font = ImageFont.truetype("arialbd.ttf", 28)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            bold_font = ImageFont.load_default()
        
        # Header background
        draw.rectangle([0, 0, img_width, 90], fill='#4f46e5')
        draw.text((350, 45), f"Piece {piece['id']}", font=title_font, fill='white', anchor='mm')
        
        y = 140
        
        # Content with bold fonts
        if self.mode == "laser":
            lines = [
                (f"Time: {piece['hours']}h {piece['minutes']}min", normal_font, '#6b7280'),
                ("", normal_font, 'black'),
                (f"Time Price: {result['time_price']:.2f} DT", normal_font, 'black'),
                (f"Subtotal: {result['subtotal']:.2f} DT", normal_font, 'black'),
                (f"Markup (+{self.markup_percent.get():.0f}%): +{result['markup_amount']:.2f} DT", normal_font, 'black'),
                ("", normal_font, 'black'),
                (f"Final Price: {result['final_price']:.2f} DT", bold_font, '#10b981'),
            ]
        else:
            lines = [
                (f"Weight: {piece['grams']}g  |  Time: {piece['hours']}h {piece['minutes']}min", normal_font, '#6b7280'),
                ("", normal_font, 'black'),
                (f"Gramage Price: {result['gram_price']:.2f} DT", normal_font, 'black'),
                (f"Time Price: {result['time_price']:.2f} DT", normal_font, 'black'),
                (f"Subtotal: {result['subtotal']:.2f} DT", normal_font, 'black'),
                (f"Markup (+{self.markup_percent.get():.0f}%): +{result['markup_amount']:.2f} DT", normal_font, 'black'),
                ("", normal_font, 'black'),
                (f"Final Price: {result['final_price']:.2f} DT", bold_font, '#10b981'),
            ]
        
        for text, font, color in lines:
            draw.text((60, y), text, font=font, fill=color)
            y += 50
        
        # First, try to put the image directly into the system clipboard
        if _copy_image_to_clipboard(img):
            messagebox.showinfo(self.t("success"), self.t("img_copied"))
            return

        # Fallback: if clipboard copy fails (e.g. pywin32 not available), ask user to save the file.
        messagebox.showwarning(self.t("warning"), self.t("img_copy_failed"))
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=f"piece_{piece['id']}_recu.png"
        )

        if file_path:
            img.save(file_path)
            messagebox.showinfo(self.t("success"), self.t("img_saved", path=file_path))
            
    def generate_detailed_pdf(self):
        if not self.pieces or not any(p['result'] for p in self.pieces):
            messagebox.showwarning(self.t("warning"), self.t("calc_first"))
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="detailed_quote.pdf"
        )
        
        if not file_path:
            return
            
        doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()
        
        # Title (3D vs Laser)
        quote_key = "quote_title_laser" if self.mode == "laser" else "quote_title"
        title = Paragraph(f"<b>{self.t(quote_key)}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Rules summary
        if self.mode == "laser":
            rules_text = f"""
            <b>{self.t('pricing_rules')}</b><br/>
            {self.t('rule_normal_hour')} {self.normal_hour_price.get()} DT/h<br/>
            {self.t('rule_markup')} {self.markup_percent.get()}%
            """
        else:
            rules_text = f"""
            <b>{self.t('pricing_rules')}</b><br/>
            {self.t('rule_gram_price')} {self.gram_price.get()} DT/g<br/>
            {self.t('rule_normal_hour')} {self.normal_hour_price.get()} DT/h<br/>
            {self.t('rule_exceed_hour')} {self.exceed_hour_price.get()} DT/h ({self.t('rule_threshold')} {self.exceed_threshold.get()}h)<br/>
            {self.t('rule_markup')} {self.markup_percent.get()}%
            """
        story.append(Paragraph(rules_text, styles['Normal']))
        story.append(Spacer(1, 0.8*cm))
        
        # Each piece
        total = 0
        for piece in self.pieces:
            if piece['result']:
                result = piece['result']
                
                if self.mode == "laser":
                    data = [
                        ['Item', 'Value'],
                        [f"Piece {piece['id']}", ''],
                        ['Time', f"{piece['hours']}h {piece['minutes']}min"],
                        ['Time Price', f"{result['time_price']:.2f} DT"],
                        ['Subtotal', f"{result['subtotal']:.2f} DT"],
                        ['Markup', f"{result['markup_amount']:.2f} DT"],
                        ['Final Price', f"{result['final_price']:.2f} DT"],
                    ]
                else:
                    data = [
                        ['Item', 'Value'],
                        [f"Piece {piece['id']}", ''],
                        ['Weight', f"{piece['grams']}g"],
                        ['Time', f"{piece['hours']}h {piece['minutes']}min"],
                        ['Gramage Price', f"{result['gram_price']:.2f} DT"],
                        ['Time Price', f"{result['time_price']:.2f} DT"],
                        ['Subtotal', f"{result['subtotal']:.2f} DT"],
                        ['Markup', f"{result['markup_amount']:.2f} DT"],
                        ['Final Price', f"{result['final_price']:.2f} DT"],
                    ]
                
                table = Table(data, colWidths=[10*cm, 6*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e0e7ff')),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecfdf5')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('TOPPADDING', (0, -1), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 0.8*cm))
                
                total += result['final_price']
        
        # Total with proper padding
        total_data = [['TOTAL', f"{total:.2f} DT"]]
        total_table = Table(total_data, colWidths=[10*cm, 6*cm])
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(total_table)
        
        doc.build(story)
        messagebox.showinfo(self.t("success"), self.t("pdf_saved", path=file_path))
        
    def generate_simple_pdf(self):
        if not self.pieces or not any(p['result'] for p in self.pieces):
            messagebox.showwarning(self.t("warning"), self.t("calc_first"))
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="simple_quote.pdf"
        )
        
        if not file_path:
            return
            
        doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()
        
        # Title (3D vs Laser)
        quote_key = "quote_title_laser" if self.mode == "laser" else "quote_title"
        title = Paragraph(f"<b>{self.t(quote_key)}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 1*cm))
        
        # Simple table with only prices
        data = [['Piece', 'Final Price']]
        
        total = 0
        for piece in self.pieces:
            if piece['result']:
                result = piece['result']
                data.append([f"Piece {piece['id']}", f"{result['final_price']:.2f} DT"])
                total += result['final_price']
        
        table = Table(data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 1*cm))
        
        # Total with proper padding
        total_data = [['TOTAL', f"{total:.2f} DT"]]
        total_table = Table(total_data, colWidths=[10*cm, 6*cm])
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(total_table)
        
        doc.build(story)
        messagebox.showinfo(self.t("success"), self.t("pdf_saved", path=file_path))


def _tk_report_callback_exception(exc, val, tb):
    """Surface Tkinter callback exceptions instead of failing silently."""
    import traceback

    traceback.print_exception(exc, val, tb)
    try:
        lang = load_settings().get("language", "fr")
        strings = I18N.get(lang, I18N["fr"])
        messagebox.showerror(
            strings.get("unexpected_error", "Unexpected error"),
            strings.get("unexpected_error_msg", "An unexpected error occurred:\n{err}").format(err=val),
        )
    except Exception:
        # If Tk isn't fully initialized yet, at least keep the traceback in the console.
        pass


def main():
    # NOTE: Without creating a Tk root and starting the mainloop, the script exits immediately.
    print("[startup] Launching 3D & Laser Calculator...")
    root = tk.Tk()
    # Start maximized (Windows). Fallback to fullscreen on other platforms.
    try:
        root.state("zoomed")
    except Exception:
        try:
            root.attributes("-fullscreen", True)
        except Exception:
            pass
    root.report_callback_exception = _tk_report_callback_exception
    app = PrintCalculatorApp(root)

    # Ensure settings are flushed to disk when the window is closed.
    def _on_close():
        try:
            app.save_current_settings()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _on_close)
    root.mainloop()


if __name__ == "__main__":
    main()

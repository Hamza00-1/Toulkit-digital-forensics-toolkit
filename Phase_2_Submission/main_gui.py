import customtkinter as ctk
from tkinter import filedialog
import json

# Phase 1
from metadata_module import extract_metadata
# Phase 2
from log_module import parse_auth_log
from recovery_module import carve_files

# Basic Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AegisPhaseTwo(ctk.CTk):
    """Phase 2: Integrating Log Analytics & File Recovery Engines"""
    
    def __init__(self):
        super().__init__()
        self.title("Aegis Forensics Suite - Phase 2 Milestone")
        self.geometry("1400x900")
        
        self.bg_color = ("#f1f5f9", "#0b0d10")
        self.card_color = ("#ffffff", "#14161a")
        self.border_color = ("#cbd5e1", "#1f2228")
        self.accent = ("#3b82f6", "#3b82f6")
        
        self.configure(fg_color=self.bg_color)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ----------------------------------------------------
        # TOP RIBBON
        # ----------------------------------------------------
        self.ribbon = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color=self.card_color)
        self.ribbon.grid(row=0, column=0, sticky="ew")
        
        title_label = ctk.CTkLabel(self.ribbon, text="AEGIS FORENSICS: PHASE 2", font=ctk.CTkFont(family="Orbitron", size=14, weight="bold"), text_color=self.accent)
        title_label.pack(side="left", padx=15, pady=10)
        
        self._create_btn("📁 Extract Metadata (Phase 1)", self.run_metadata, is_active=True)
        self._create_btn("🔑 Parse Syslog (Phase 2)", self.run_syslog, is_active=True)
        self._create_btn("💾 Carve Raw Hex (Phase 2)", self.run_carving, is_active=True)
        self._create_btn("🔐 Compute Hashes (Phase 3)", self.run_phase_three)
        self._create_btn("📊 MySQL Dashboard (Phase 4)", self.run_phase_four)

        # ----------------------------------------------------
        # MULTI-PANE LAYOUT
        # ----------------------------------------------------
        self.paned_frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.paned_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        
        self.paned_frame.grid_rowconfigure(0, weight=1)
        self.paned_frame.grid_columnconfigure(0, weight=1) 
        self.paned_frame.grid_columnconfigure(1, weight=4) 
        
        # Left Panel (Evidence Explorer Skeleton)
        self.left_pane = ctk.CTkFrame(self.paned_frame, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.left_pane.grid(row=0, column=0, sticky="nsew", padx=2)
        
        ctk.CTkLabel(self.left_pane, text="Evidence Explorer", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self.left_pane, text="[+] Log Analytics Online\n[+] Carving Engine Online\n\nModules load evidence\nvia OS-level Dialogs.", font=ctk.CTkFont(size=11), text_color="gray").pack()

        # Right Panels
        self.right_region = ctk.CTkFrame(self.paned_frame, fg_color="transparent")
        self.right_region.grid(row=0, column=1, sticky="nsew")
        self.right_region.grid_rowconfigure(0, weight=3)
        self.right_region.grid_rowconfigure(1, weight=2)
        self.right_region.grid_columnconfigure(0, weight=1)
        
        # Top Right (Grid Output)
        self.grid_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.grid_pane.grid(row=0, column=0, sticky="nsew", pady=2)
        self.grid_label = ctk.CTkLabel(self.grid_pane, text="Data Grid (Phase 2 Ready)", font=ctk.CTkFont(size=12, weight="bold"))
        self.grid_label.pack(anchor="w", padx=10, pady=5)
        
        self.grid_output = ctk.CTkScrollableFrame(self.grid_pane, fg_color="transparent")
        self.grid_output.pack(fill="both", expand=True)
        self.active_widgets = []

        # Bottom Right (Viewer)
        self.viewer_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.viewer_pane.grid(row=1, column=0, sticky="nsew", pady=2)
        
        self.viewer_text = ctk.CTkTextbox(self.viewer_pane, font=ctk.CTkFont(family="Consolas", size=12), fg_color="#040506", text_color="#10b981")
        self.viewer_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.viewer_text.insert("0.0", "[SYSTEM] Aegis Phase 2 Architecture loaded.\n[SYSTEM] RegEx Log Analyzer Active.\n[SYSTEM] Hexadecimal Byte Carver Active.\n[SYSTEM] Awaiting Evidence ingestion...")

    def _create_btn(self, text, command, is_active=False):
        color = self.accent if is_active else ("#64748b", "#334155")
        btn = ctk.CTkButton(self.ribbon, text=text, command=command, fg_color=color, height=26, font=ctk.CTkFont(size=11, weight="bold"))
        btn.pack(side="left", padx=5)

    def _clear_grid(self):
        for widget in self.active_widgets:
            widget.destroy()
        self.active_widgets.clear()
        self.viewer_text.delete("0.0", "end")

    # ----------------------------------------------------
    # ACTIVE MODULES
    # ----------------------------------------------------
    def run_metadata(self):
        file_path = filedialog.askopenfilename(title="Select Evidence File (Image/PDF)")
        if file_path:
            self._clear_grid()
            self.grid_label.configure(text="Data Grid: EXIF & Document Metadata")
            result = extract_metadata(file_path)
            
            if "Error" in result:
                self.viewer_text.insert("end", f"\n[ERROR] Failed to extract headers: {result['Error']}")
                return

            for key, val in result.items():
                row = ctk.CTkFrame(self.grid_output, fg_color="transparent")
                row.pack(fill="x", padx=10, pady=2)
                
                k_lbl = ctk.CTkLabel(row, text=str(key), width=250, anchor="w", text_color="#94a3b8", font=ctk.CTkFont(size=11, weight="bold"))
                k_lbl.pack(side="left")
                
                v_lbl = ctk.CTkLabel(row, text=str(val)[:80] + "..." if len(str(val)) > 80 else str(val), anchor="w", font=ctk.CTkFont(family="Consolas", size=11))
                v_lbl.pack(side="left", padx=10)
                
                self.active_widgets.extend([row, k_lbl, v_lbl])
                
            self.viewer_text.insert("end", "\n[SUCCESS] Extracted Phase 1 Metadata from target.")

    def run_syslog(self):
        file_path = filedialog.askopenfilename(title="Select Syslog Evidence (.log)")
        if file_path:
            self._clear_grid()
            self.grid_label.configure(text="Data Grid: Syslog Regex Analyzer")
            
            df, anomalies_count = parse_auth_log(file_path)
            
            if df.empty:
                self.viewer_text.insert("end", "\n[WARNING] No recognized syslog patterns found in file.")
                return
                
            stats = ctk.CTkLabel(self.grid_output, text=f"Total Events: {len(df)} | Anomalies Detected: {anomalies_count}", text_color="#ef4444" if anomalies_count > 0 else "#10b981", font=ctk.CTkFont(weight="bold"))
            stats.pack(pady=10)
            self.active_widgets.append(stats)
            
            for index, row_data in df.head(50).iterrows():
                text = f"[{row_data['timestamp']}] {row_data['hostname']} {row_data['process']}: {row_data['message']}"
                lbl = ctk.CTkLabel(self.grid_output, text=text, anchor="w", font=ctk.CTkFont(family="Consolas", size=11))
                lbl.pack(fill="x", padx=10)
                self.active_widgets.append(lbl)
                
            self.viewer_text.insert("end", f"\n[SUCCESS] Syslog parsed into Dataframe. Rendered Top 50 recent events. Found {anomalies_count} brute-force anomalies.")

    def run_carving(self):
        file_path = filedialog.askopenfilename(title="Select Raw Binary Stream or Corruption")
        if file_path:
            self._clear_grid()
            self.grid_label.configure(text="Data Grid: Raw File Carving Target")
            
            self.viewer_text.insert("end", f"\n[SYSTEM] Initiating Hexadecimal Regex search on {file_path}...\n")
            
            # The recovery module naturally dumps carved output to its own folder.
            files_found = carve_files(file_path)
            
            if not files_found:
                self.viewer_text.insert("end", "[WARNING] No Magic Numbers (JPEG/PDF) identified in the raw binary.")
                return
                
            for sf in files_found:
                lbl = ctk.CTkLabel(self.grid_output, text=f"CARVED: {sf}", text_color="#10b981", font=ctk.CTkFont(weight="bold"))
                lbl.pack(pady=2)
                self.active_widgets.append(lbl)
                
            self.viewer_text.insert("end", f"\n[SUCCESS] Recovered {len(files_found)} deleted files traversing hexadecimal streams.")

    # ----------------------------------------------------
    # FUTURE PHASE MOCKUPS
    # ----------------------------------------------------
    def run_phase_three(self):
        self._clear_grid()
        self.viewer_text.insert("0.0", "[UNDER CONSTRUCTION]\n\nPhase 3 Feature: The Cryptographic Hashing Engine (MD5/SHA/Base64 Decoder) and VirusTotal API routing are scheduled for the next milestone.")

    def run_phase_four(self):
        self._clear_grid()
        self.viewer_text.insert("0.0", "[UNDER CONSTRUCTION]\n\nPhase 4 Feature: The MySQL Database Integration and Flask Web Application dashboard will be the final milestone submitted for this project.")

if __name__ == "__main__":
    app = AegisPhaseTwo()
    app.mainloop()

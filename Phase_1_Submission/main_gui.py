import customtkinter as ctk
from tkinter import filedialog
import json

# Phase 1: Only the Metadata module is integrated into the core architecture so far.
from metadata_module import extract_metadata

# Basic Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AegisPhaseOne(ctk.CTk):
    """Phase 1: Architecture Foundation & EXIF/Metadata Extraction"""
    
    def __init__(self):
        super().__init__()
        self.title("Aegis Forensics Suite - Phase 1 Milestone")
        self.geometry("1400x900")
        
        self.bg_color = ("#f1f5f9", "#0b0d10")
        self.card_color = ("#ffffff", "#14161a")
        self.border_color = ("#cbd5e1", "#1f2228")
        self.accent = ("#3b82f6", "#3b82f6")
        
        self.configure(fg_color=self.bg_color)
        
        # Base Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ----------------------------------------------------
        # TOP RIBBON
        # ----------------------------------------------------
        self.ribbon = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color=self.card_color)
        self.ribbon.grid(row=0, column=0, sticky="ew")
        
        title_label = ctk.CTkLabel(self.ribbon, text="AEGIS FORENSICS: PHASE 1", font=ctk.CTkFont(family="Orbitron", size=14, weight="bold"), text_color=self.accent)
        title_label.pack(side="left", padx=15, pady=10)
        
        self._create_btn("📁 Extract Metadata (Active)", self.run_metadata, is_active=True)
        self._create_btn("🔑 Parse Syslog (Phase 2)", self.run_phase_two)
        self._create_btn("🔐 Compute Hashes (Phase 3)", self.run_phase_three)
        self._create_btn("📊 MySQL Dashboard (Phase 4)", self.run_phase_four)

        # ----------------------------------------------------
        # MULTI-PANE LAYOUT
        # ----------------------------------------------------
        self.paned_frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.paned_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        
        self.paned_frame.grid_rowconfigure(0, weight=1)
        self.paned_frame.grid_columnconfigure(0, weight=1) # Evidence
        self.paned_frame.grid_columnconfigure(1, weight=4) # Data
        
        # Left Panel (Evidence Explorer Skeleton)
        self.left_pane = ctk.CTkFrame(self.paned_frame, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.left_pane.grid(row=0, column=0, sticky="nsew", padx=2)
        
        ctk.CTkLabel(self.left_pane, text="Evidence Explorer", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self.left_pane, text="[+] Architecture Setup Complete\n\nModules load evidence\nvia OS-level Dialogs in Phase 1.", font=ctk.CTkFont(size=11), text_color="gray").pack()

        # Right Panels
        self.right_region = ctk.CTkFrame(self.paned_frame, fg_color="transparent")
        self.right_region.grid(row=0, column=1, sticky="nsew")
        self.right_region.grid_rowconfigure(0, weight=3)
        self.right_region.grid_rowconfigure(1, weight=2)
        self.right_region.grid_columnconfigure(0, weight=1)
        
        # Top Right (Grid Output)
        self.grid_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.grid_pane.grid(row=0, column=0, sticky="nsew", pady=2)
        self.grid_label = ctk.CTkLabel(self.grid_pane, text="Data Grid (Phase 1 Ready)", font=ctk.CTkFont(size=12, weight="bold"))
        self.grid_label.pack(anchor="w", padx=10, pady=5)
        
        self.grid_output = ctk.CTkScrollableFrame(self.grid_pane, fg_color="transparent")
        self.grid_output.pack(fill="both", expand=True)
        self.active_widgets = []

        # Bottom Right (Viewer)
        self.viewer_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_color=self.border_color, border_width=1)
        self.viewer_pane.grid(row=1, column=0, sticky="nsew", pady=2)
        
        self.viewer_text = ctk.CTkTextbox(self.viewer_pane, font=ctk.CTkFont(family="Consolas", size=12), fg_color="#040506", text_color="#10b981")
        self.viewer_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.viewer_text.insert("0.0", "[SYSTEM] Aegis Phase 1 Architecture loaded.\n[SYSTEM] CustomTkinter structural UI active.\n[SYSTEM] Awaiting Evidence ingestion...")

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
    # PHASE 1 ACTIVE MODULES
    # ----------------------------------------------------
    def run_metadata(self):
        file_path = filedialog.askopenfilename(title="Select Evidence File (Image/PDF)")
        if file_path:
            self._clear_grid()
            self.grid_label.configure(text="Data Grid: EXIF & Document Metadata")
            
            # Execute Phase 1 Core Engine
            result = extract_metadata(file_path)
            
            if "Error" in result:
                lbl = ctk.CTkLabel(self.grid_output, text=result["Error"], text_color="#ef4444", font=ctk.CTkFont(weight="bold"))
                lbl.pack(pady=20)
                self.active_widgets.append(lbl)
                self.viewer_text.insert("0.0", f"[ERROR] Failed to extract headers: {result['Error']}")
                return

            # Display Tabular Data
            for key, val in result.items():
                row = ctk.CTkFrame(self.grid_output, fg_color="transparent")
                row.pack(fill="x", padx=10, pady=2)
                
                k_lbl = ctk.CTkLabel(row, text=str(key), width=250, anchor="w", text_color="#94a3b8", font=ctk.CTkFont(size=11, weight="bold"))
                k_lbl.pack(side="left")
                
                v_lbl = ctk.CTkLabel(row, text=str(val)[:80] + "..." if len(str(val)) > 80 else str(val), anchor="w", font=ctk.CTkFont(family="Consolas", size=11))
                v_lbl.pack(side="left", padx=10)
                
                self.active_widgets.extend([row, k_lbl, v_lbl])
                
            self.viewer_text.insert("0.0", f"[SUCCESS] Extracted Phase 1 Metadata from target.\n\nRAW DICTIONARY DUMP:\n{json.dumps(result, indent=2)}")

    # ----------------------------------------------------
    # FUTURE PHASE MOCKUPS
    # ----------------------------------------------------
    def run_phase_two(self):
        self._clear_grid()
        self.viewer_text.insert("0.0", "[UNDER CONSTRUCTION]\n\nPhase 2 Feature: The Syslog Regex parser and Hexadecimal Carver engines are currently under development. They will be integrated in the next milestone submission.")

    def run_phase_three(self):
        self._clear_grid()
        self.viewer_text.insert("0.0", "[UNDER CONSTRUCTION]\n\nPhase 3 Feature: The Cryptographic Hashing Engine (MD5/SHA) and VirusTotal API routing are scheduled for the third milestone.")

    def run_phase_four(self):
        self._clear_grid()
        self.viewer_text.insert("0.0", "[UNDER CONSTRUCTION]\n\nPhase 4 Feature: The MySQL Database Integration and Flask Web Application dashboard will be the final milestone submitted for this project.")

if __name__ == "__main__":
    app = AegisPhaseOne()
    app.mainloop()

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, Scrollbar, Canvas
from PIL import Image
import json
import os
import platform

# Matplotlib for professional inner dashboard graphs
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Toolkit Modules
from metadata_module import extract_metadata
from log_module import parse_auth_log
from recovery_module import carve_files
from hash_module import compute_hashes, check_virustotal
from decoding_module import decode_message
import activity_tracker

# Initial Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ToolkitApp(ctk.CTk):
    """Main GUI application class for Aegis Forensics Suite - FTK Edition."""
    
    def __init__(self):
        super().__init__()
        self.title("🛡️ Aegis Forensics Suite: Enterprise Analytics (FTK Layout)")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # --- Dual-Tone Enterprise Color Palette ---
        self.bg_color = ("#f1f5f9", "#0b0d10")          # Real Dark Background
        self.card_color = ("#ffffff", "#14161a")        # Elevated Dark Card
        self.pane_border = ("#cbd5e1", "#1f2228")       # Subtle Panel Borders
        self.accent_primary = ("#3b82f6", "#3b82f6")    # Bright Steel Blue for contrast
        self.accent_warning = ("#ef4444", "#ef4444")    # Bright Red
        self.text_primary = ("#0f172a", "#f8fafc")      # Pure White text
        self.text_secondary = ("#64748b", "#94a3b8")    # Muted Gray text

        self.vt_api_key = ""
        self.loaded_workspace_files = []

        self.configure(fg_color=self.bg_color)
        
        # Base Grid: Row 0 Toolbar, Row 1 Window Content
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ==========================================
        # TOP RIBBON / TOOLBAR
        # ==========================================
        self.ribbon_frame = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color=self.card_color)
        self.ribbon_frame.grid(row=0, column=0, sticky="ew")
        self.ribbon_frame.grid_propagate(False) # Keep height fixed
        
        # Tools in Ribbon
        self._create_ribbon_btn("📊 Dashboard", self.show_dashboard, 0)
        self._create_ribbon_btn("📁 Load Evidence (EXIF)", self._run_metadata, 1)
        self._create_ribbon_btn("🔑 Parse Syslog", self._run_syslog, 2)
        self._create_ribbon_btn("🔐 Compute Hashes", self._run_hasher, 3)
        self._create_ribbon_btn("🧩 Decode String", self._run_decoder, 4)
        self._create_ribbon_btn("🔍 Carve Hex (Raw)", self._run_carving, 5)

        # Theme switch on far right of ribbon
        self.appearance_var = ctk.StringVar(value="Dark")
        self.theme_switch = ctk.CTkSwitch(
            self.ribbon_frame, text="Night Ops", command=self.toggle_theme,
            variable=self.appearance_var, onvalue="Dark", offvalue="Light",
            font=ctk.CTkFont(family="Inter", size=11), text_color=self.text_primary, progress_color=self.accent_primary
        )
        self.theme_switch.pack(side="right", padx=15, pady=10)

        # ==========================================
        # MULTI-PANE STRUCTURAL LAYOUT
        # ==========================================
        self.paned_frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.paned_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        
        # 2 Columns: Evidence Tree (Left), Data Region (Right)
        self.paned_frame.grid_rowconfigure(0, weight=1)
        self.paned_frame.grid_columnconfigure(1, weight=4) # Right is much wider
        
        # --- LEFT PANE (Evidence Tree Simulator) ---
        self.left_pane = ctk.CTkFrame(self.paned_frame, fg_color=self.card_color, corner_radius=0, border_width=1, border_color=self.pane_border)
        self.left_pane.grid(row=0, column=0, sticky="nsew", padx=(0,2))
        
        self.tree_label_frame = ctk.CTkFrame(self.left_pane, fg_color="transparent")
        self.tree_label_frame.pack(fill="x", padx=8, pady=(5,0))
        
        self.tree_label = ctk.CTkLabel(self.tree_label_frame, text="Evidence Explorer", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color=self.text_primary, anchor="w")
        self.tree_label.pack(side="left")
        
        self.add_folder_btn = ctk.CTkButton(self.tree_label_frame, text="+ Folder", width=50, height=20, font=ctk.CTkFont(size=10, weight="bold"), command=self._load_workspace_folder, fg_color=self.pane_border, text_color=self.text_primary, hover_color=self.accent_primary)
        self.add_folder_btn.pack(side="right")
        
        # Mock tree structure but interactive
        self.tree_area = ctk.CTkScrollableFrame(self.left_pane, fg_color="transparent", corner_radius=0)
        self.tree_area.pack(fill="both", expand=True, padx=4, pady=4)
        self.tree_widgets = []
        self._update_evidence_tree()

        # --- RIGHT REGION (Data Grid over Detail Viewer) ---
        self.right_region = ctk.CTkFrame(self.paned_frame, fg_color="transparent")
        self.right_region.grid(row=0, column=1, sticky="nsew", padx=(2,0))
        self.right_region.grid_columnconfigure(0, weight=1)
        self.right_region.grid_rowconfigure(0, weight=3) # Top Data pane is taller
        self.right_region.grid_rowconfigure(1, weight=2) # Bottom Viewer is shorter

        # Top Right (Data Grid View)
        self.top_right_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_width=1, border_color=self.pane_border)
        self.top_right_pane.grid(row=0, column=0, sticky="nsew", pady=(0,2))
        
        self.grid_label = ctk.CTkLabel(self.top_right_pane, text="Data Grid Viewer", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color=self.text_primary, anchor="w")
        self.grid_label.pack(fill="x", padx=8, pady=(5,0))
        
        # Central generic output area (Scrollable)
        self.grid_output = ctk.CTkScrollableFrame(self.top_right_pane, fg_color=self.card_color)
        self.grid_output.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Keep references to the custom drawn data inside grid_output
        self.active_grid_widgets = []

        # Bottom Right (Raw Detail / Hex / Log Viewer)
        self.bottom_right_pane = ctk.CTkFrame(self.right_region, fg_color=self.card_color, corner_radius=0, border_width=1, border_color=self.pane_border)
        self.bottom_right_pane.grid(row=1, column=0, sticky="nsew", pady=(2,0))
        
        self.viewer_label = ctk.CTkLabel(self.bottom_right_pane, text="Properties / Hex / Raw View", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color=self.text_primary, anchor="w")
        self.viewer_label.pack(fill="x", padx=8, pady=(5,0))
        
        self.viewer_text = ctk.CTkTextbox(self.bottom_right_pane, font=ctk.CTkFont(family="Consolas", size=12), fg_color="#040506", text_color="#34d399") # Real dark BG, green text for hacker feel
        self.viewer_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize Dashboard view into the grids
        self.show_dashboard()

    def _create_ribbon_btn(self, text, command, col):
        btn = ctk.CTkButton(
            self.ribbon_frame, text=text, command=command,
            fg_color="transparent", text_color=self.text_primary,
            hover_color=self.pane_border, anchor="center",
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            height=30, corner_radius=4, width=120
        )
        btn.pack(side="left", padx=5, pady=5)

    def toggle_theme(self):
        new_mode = self.appearance_var.get()
        ctk.set_appearance_mode(new_mode)
        # Update extreme terminal colors
        if new_mode == "Light":
            self.viewer_text.configure(fg_color="#f8fafc", text_color="#0f172a")
        else:
            self.viewer_text.configure(fg_color="#040506", text_color="#34d399")
            
        self.after(50, self.show_dashboard)

    def _clear_grid(self):
        for widget in self.active_grid_widgets:
            widget.destroy()
        self.active_grid_widgets.clear()
        
    def _write_viewer(self, content):
        self.viewer_text.configure(state="normal")
        self.viewer_text.delete("0.0", "end")
        self.viewer_text.insert("end", content)

    def _update_evidence_tree(self):
        """Simulates an FTK-style expanding evidence tree taking data from Activity Tracker."""
        for w in self.tree_widgets:
            w.destroy()
        self.tree_widgets.clear()
        
        stats = activity_tracker.get_dashboard_stats()
        events = stats.get('raw_events', [])
        
        if not hasattr(self, 'tree_state'):
            self.tree_state = {"loaded": True, "processed": True}
            
        def show_context_menu(path):
            menu = tk.Menu(self, tearoff=0, 
                           bg=self.card_color[0] if ctk.get_appearance_mode()=="Light" else self.card_color[1],
                           fg=self.text_primary[0] if ctk.get_appearance_mode()=="Light" else self.text_primary[1])
            menu.add_command(label="Send to: Metadata Extractor", command=lambda p=path: self._execute_metadata(p))
            menu.add_command(label="Send to: Cryptographic Hasher", command=lambda p=path: self._execute_hasher(p))
            menu.add_command(label="Send to: Syslog Abstractor", command=lambda p=path: self._execute_syslog(p))
            menu.add_command(label="Send to: Hexadecimal Carving", command=lambda p=path: self._execute_carving(p))
            
            x, y = self.winfo_pointerxy()
            menu.tk_popup(x, y)
            
        lbl_ws = ctk.CTkLabel(self.tree_area, text="▾ Local Workspace", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=self.accent_primary, anchor="w")
        lbl_ws.pack(fill="x", pady=(0, 2))
        self.tree_widgets.append(lbl_ws)
        
        # --- Loaded Directory Files ---
        def toggle_loaded():
            self.tree_state["loaded"] = not self.tree_state["loaded"]
            self._update_evidence_tree()
            
        arrow_ld = "▾" if self.tree_state["loaded"] else "▸"
        lbl_wf = ctk.CTkButton(self.tree_area, text=f"  {arrow_ld} Loaded Directory Files", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=self.text_secondary, anchor="w", fg_color="transparent", hover_color=self.pane_border, height=22, command=toggle_loaded)
        lbl_wf.pack(fill="x", pady=(2, 2))
        self.tree_widgets.append(lbl_wf)
        
        if self.tree_state["loaded"]:
            if not hasattr(self, 'loaded_workspace_files') or not self.loaded_workspace_files:
                empty_wf = ctk.CTkLabel(self.tree_area, text="    (No folder loaded)", font=ctk.CTkFont(family="Consolas", size=11, slant="italic"), text_color=self.text_secondary, anchor="w")
                empty_wf.pack(fill="x")
                self.tree_widgets.append(empty_wf)
            else:
                hint_wf = ctk.CTkLabel(self.tree_area, text="    [Click a file to open Send To... Menu]", font=ctk.CTkFont(size=9, slant="italic"), text_color=self.text_secondary, anchor="w")
                hint_wf.pack(fill="x", pady=(0, 2))
                self.tree_widgets.append(hint_wf)
                
                for f in sorted(self.loaded_workspace_files)[:30]:
                    f_name = os.path.basename(f)
                    if len(f_name) > 23: f_name = f_name[:20] + "..."
                    
                    btn_wf = ctk.CTkButton(self.tree_area, text=f"    📁 {f_name}", command=lambda p=f: show_context_menu(p), fg_color="transparent", text_color=self.text_secondary, hover_color=self.pane_border, anchor="w", font=ctk.CTkFont(family="Consolas", size=10), height=22)
                    btn_wf.pack(fill="x", pady=1)
                    self.tree_widgets.append(btn_wf)
        
        # --- Processed Targets ---
        def toggle_processed():
            self.tree_state["processed"] = not self.tree_state["processed"]
            self._update_evidence_tree()
            
        arrow_pt = "▾" if self.tree_state["processed"] else "▸"
        lbl_pt = ctk.CTkButton(self.tree_area, text=f"\n  {arrow_pt} Processed Targets", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=self.text_secondary, anchor="w", fg_color="transparent", hover_color=self.pane_border, height=35, command=toggle_processed)
        lbl_pt.pack(fill="x", pady=(2, 2))
        self.tree_widgets.append(lbl_pt)
        
        if self.tree_state["processed"]:
            unique_files = list(set([e['file'] for e in events if e['file'] != 'N/A' and e['file'] != 'Raw String Input']))
            
            if not unique_files:
                empty = ctk.CTkLabel(self.tree_area, text="    (No evidence loaded)", font=ctk.CTkFont(family="Consolas", size=11, slant="italic"), text_color=self.text_secondary, anchor="w")
                empty.pack(fill="x")
                self.tree_widgets.append(empty)
            else:
                hint = ctk.CTkLabel(self.tree_area, text="    [Click a file to open Send To... Menu]", font=ctk.CTkFont(size=9, slant="italic"), text_color=self.text_secondary, anchor="w")
                hint.pack(fill="x", pady=(0, 2))
                self.tree_widgets.append(hint)
                
                for f in sorted(unique_files)[:20]:
                    f_name = os.path.basename(f)
                    if len(f_name) > 23: f_name = f_name[:20] + "..."
                    
                    btn = ctk.CTkButton(self.tree_area, text=f"    📄 {f_name}", command=lambda p=f: show_context_menu(p), fg_color="transparent", text_color=self.text_secondary, hover_color=self.pane_border, anchor="w", font=ctk.CTkFont(family="Consolas", size=10), height=22)
                    btn.pack(fill="x", pady=1)
                    self.tree_widgets.append(btn)
                    
        lbl_op = ctk.CTkLabel(self.tree_area, text="\n  ▾ Operations Executed", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=self.text_secondary, anchor="w")
        lbl_op.pack(fill="x", pady=(5, 2))
        self.tree_widgets.append(lbl_op)
        
        for mod, count in stats.get('module_counts', {}).items():
            mlbl = ctk.CTkLabel(self.tree_area, text=f"    ⚙️ {mod} ({count})", font=ctk.CTkFont(family="Consolas", size=11), text_color=self.text_secondary, anchor="w")
            mlbl.pack(fill="x", pady=1)
            self.tree_widgets.append(mlbl)

    def _load_workspace_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Add to Workspace")
        if folder_path:
            self._write_viewer(f"[SYSTEM] Crawling directory: {folder_path} ...\n")
            self.update()
            
            files_found = []
            for root, _, filenames in os.walk(folder_path):
                for f in filenames:
                    files_found.append(os.path.join(root, f))
                    if len(files_found) >= 50: # Limit to 50 to prevent UI freezing
                        break
                if len(files_found) >= 50:
                    break
                    
            if not files_found:
                self._write_viewer("[WARNING] Selected directory contains zero files.\n")
                return
                
            self.loaded_workspace_files.extend(files_found)
            # Deduplicate
            self.loaded_workspace_files = list(set(self.loaded_workspace_files))
            self._update_evidence_tree()
            self._write_viewer(f"[SUCCESS] Loaded {len(files_found)} files into the Workspace Evidence Tree.\nClick them in the left pane to instantly process them.")

    # ==============================
    # MODULE INTEGRATIONS (FTK STYLE)
    # ==============================
    
    def show_dashboard(self):
        self.grid_label.configure(text="Data Grid: Global Executive Analytics")
        self._clear_grid()
        
        stats = activity_tracker.get_dashboard_stats()
        events = list(reversed(stats.get('raw_events', [])))
        
        # Write events to raw viewer
        viewer_text = "[AEGIS GLOBAL LOGS]\n======================================================\nSystem online. Connected to Local Activity Database.\n======================================================\n"
        for e in events:
            viewer_text += f"[{e['timestamp']}] TRIGGERED: {e['module']} | FLAG: {e['status']} | Target: {e['file']}\n"
        self._write_viewer(viewer_text)
        
        # KPI Table Framework
        kpi_frame = ctk.CTkFrame(self.grid_output, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=10, pady=5)
        self.active_grid_widgets.append(kpi_frame)
        
        ctk.CTkLabel(kpi_frame, text="Metric Name", width=250, anchor="w", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.text_secondary).grid(row=0, column=0, pady=2, sticky="w")
        ctk.CTkLabel(kpi_frame, text="Value", width=250, anchor="w", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.text_secondary).grid(row=0, column=1, pady=2, sticky="w")
        
        ctk.CTkLabel(kpi_frame, text="Database State", width=250, anchor="w", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.accent_primary).grid(row=1, column=0, pady=2, sticky="w")
        ctk.CTkLabel(kpi_frame, text="ONLINE / SYNCED", text_color="#10b981", font=ctk.CTkFont(size=11, weight="bold")).grid(row=1, column=1, pady=2, sticky="w")
        
        ctk.CTkLabel(kpi_frame, text="Gross Processed Artifacts", width=250, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).grid(row=2, column=0, pady=2, sticky="w")
        ctk.CTkLabel(kpi_frame, text=str(stats['total_files']), font=ctk.CTkFont(family="Consolas", size=11)).grid(row=2, column=1, pady=2, sticky="w")
        
        anom_color = self.accent_warning if stats['anomalies'] > 0 else ("#10b981", "#10b981")
        ctk.CTkLabel(kpi_frame, text="Threat Vectors Flagged", width=250, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).grid(row=3, column=0, pady=2, sticky="w")
        ctk.CTkLabel(kpi_frame, text=str(stats['anomalies']), text_color=anom_color, font=ctk.CTkFont(family="Consolas", size=11, weight="bold")).grid(row=3, column=1, pady=2, sticky="w")
        
        ctk.CTkLabel(kpi_frame, text="Note: Select a module from the top ribbon to load evidence. Dashboard auto-syncs.", text_color=self.text_secondary, font=ctk.CTkFont(size=10, slant="italic")).grid(row=4, column=0, columnspan=2, pady=(15,0), sticky="w")
        
        # Detailed Execution Log Table
        log_frame = ctk.CTkFrame(self.grid_output, fg_color=self.card_color, corner_radius=0, border_width=1, border_color=self.pane_border)
        log_frame.pack(fill="x", padx=10, pady=10)
        self.active_grid_widgets.append(log_frame)
        
        # Headers
        ctk.CTkLabel(log_frame, text="Timestamp", font=ctk.CTkFont(size=11, weight="bold"), width=150, anchor="w").grid(row=0, column=0, padx=5, pady=2)
        ctk.CTkLabel(log_frame, text="Target Module", font=ctk.CTkFont(size=11, weight="bold"), width=150, anchor="w").grid(row=0, column=1, padx=5, pady=2)
        ctk.CTkLabel(log_frame, text="Result State", font=ctk.CTkFont(size=11, weight="bold"), width=150, anchor="w").grid(row=0, column=2, padx=5, pady=2)
        
        r = 1
        for e in events[:15]: # Show top 15 in UI grid
            ctk.CTkLabel(log_frame, text=e['timestamp'], font=ctk.CTkFont(family="Consolas", size=10), width=150, anchor="w").grid(row=r, column=0, padx=5, pady=1)
            ctk.CTkLabel(log_frame, text=e['module'], font=ctk.CTkFont(size=10), width=150, anchor="w").grid(row=r, column=1, padx=5, pady=1)
            
            is_danger = "Danger" in e['status'] or "Anomalies" in e['status']
            c = self.accent_warning if is_danger else self.text_primary
            ctk.CTkLabel(log_frame, text=e['status'], text_color=c, font=ctk.CTkFont(size=10, weight="bold" if is_danger else "normal"), width=150, anchor="w").grid(row=r, column=2, padx=5, pady=1)
            r += 1

    def _run_metadata(self):
        self.grid_label.configure(text="Data Grid: EXIF Properties Extractor")
        self._clear_grid()
        self._write_viewer("[SYSTEM] AEGIS Metadata Extractor ready.\nAwaiting manual image or PDF allocation...\n")
        
        lbl_inst = ctk.CTkLabel(self.grid_output, text="Target Evidence Base (Images / PDF):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_inst.pack(pady=(15, 5), anchor="w", padx=15)
        
        lbl_desc = ctk.CTkLabel(self.grid_output, text="Select a file to extract hidden document properties, GPS coords, and author tags.", font=ctk.CTkFont(size=11), text_color=self.text_secondary)
        lbl_desc.pack(pady=(0, 15), anchor="w", padx=15)
        
        btn = ctk.CTkButton(self.grid_output, text="Select File & Extract", command=self._execute_metadata, fg_color=self.accent_primary)
        btn.pack(pady=5, anchor="w", padx=15)
        self.active_grid_widgets.extend([lbl_inst, lbl_desc, btn])

    def _execute_metadata(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(title="Add Evidence to Case", filetypes=[("Doc/IMG", "*.jpg *.png *.pdf"), ("All", "*.*")])
            
        if file_path:
            self.grid_label.configure(text=f"Data Grid: EXIF Properties - {os.path.basename(file_path)}")
            self._clear_grid()
            self._write_viewer(f"[SYSTEM] Extracting properties from {file_path}...\n")
            
            metadata = extract_metadata(file_path)
            activity_tracker.log_activity("Metadata Extr.", file_path, "Error" if "Error" in metadata else "Success")
            self._update_evidence_tree()
            
            # Show Raw JSON in bottom viewer
            self._write_viewer(json.dumps(metadata, indent=4))
            
            # Show Table in Top Grid
            tbl = ctk.CTkFrame(self.grid_output, fg_color="transparent")
            tbl.pack(fill="x", padx=5, pady=5)
            self.active_grid_widgets.append(tbl)
            
            r = 0
            for k, v in metadata.items():
                if k == "Error": continue
                # Truncate very long values for the grid
                v_str = str(v)
                if len(v_str) > 60: v_str = v_str[:57] + "..."
                
                ctk.CTkLabel(tbl, text=str(k), width=150, anchor="w", font=ctk.CTkFont(family="Inter", size=11, weight="bold")).grid(row=r, column=0, padx=5, pady=2, sticky="w")
                ctk.CTkLabel(tbl, text=v_str, anchor="w", font=ctk.CTkFont(family="Inter", size=11)).grid(row=r, column=1, padx=5, pady=2, sticky="w")
                r += 1

    def _run_hasher(self):
        self.grid_label.configure(text="Data Grid: Cryptographic Integrity Validation")
        self._clear_grid()
        self._write_viewer("[SYSTEM] Cryptographic bounds ready.\nLoad file and optional API key to process arrays...\n")
        
        lbl_inst = ctk.CTkLabel(self.grid_output, text="Target Payload:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_inst.pack(pady=(15, 5), anchor="w", padx=15)
        
        lbl_desc = ctk.CTkLabel(self.grid_output, text="Compute MD5, SHA-1, and SHA-256 constants for any file.", font=ctk.CTkFont(size=11), text_color=self.text_secondary)
        lbl_desc.pack(pady=(0, 15), anchor="w", padx=15)
        
        btn = ctk.CTkButton(self.grid_output, text="Select File & Compute", command=self._execute_hasher, fg_color=self.accent_primary)
        btn.pack(pady=5, anchor="w", padx=15)
        self.active_grid_widgets.extend([lbl_inst, lbl_desc, btn])

    def _execute_hasher(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(title="Target Payload")
        if file_path:
            self.grid_label.configure(text=f"Data Grid: Cryptographic Integrity - {os.path.basename(file_path)}")
            self._clear_grid()
            
            hashes = compute_hashes(file_path)
            
            tbl = ctk.CTkFrame(self.grid_output, fg_color="transparent")
            tbl.pack(fill="x", padx=5, pady=5)
            self.active_grid_widgets.append(tbl)
            
            r=0
            for algo, hval in hashes.items():
                ctk.CTkLabel(tbl, text=algo, width=100, anchor="w", font=ctk.CTkFont(weight="bold", size=11)).grid(row=r, column=0, pady=2)
                ctk.CTkLabel(tbl, text=str(hval), anchor="w", font=ctk.CTkFont(family="Consolas", size=11)).grid(row=r, column=1, pady=2)
                r += 1
                
            self._write_viewer(f"[SYSTEM] Computed hashes for: {file_path}\n" + "-"*50 + "\n")
            activity_tracker.log_activity("Hasher", file_path, "Success")
            self._update_evidence_tree()

            # Optional VT API check button in the grid
            vt_btn = ctk.CTkButton(self.grid_output, text="Query VirusTotal Global DB", font=ctk.CTkFont(size=11), height=25, command=lambda: self._execute_vt(hashes.get("SHA-256")))
            vt_btn.pack(pady=10, anchor="w", padx=10)
            self.active_grid_widgets.append(vt_btn)

    def _execute_vt(self, sha256):
        if not self.vt_api_key:
            self.vt_api_key = simpledialog.askstring("Auth", "Provide VT API Key:")
            if not self.vt_api_key: return
            
        result = check_virustotal(sha256, self.vt_api_key)
        self._write_viewer(f"[VIRUSTOTAL QUERY]\nHash: {sha256}\n\n" + json.dumps(result, indent=4))

    def _run_syslog(self):
        self.grid_label.configure(text="Data Grid: Sentinel Syslog Abstractor")
        self._clear_grid()
        self._write_viewer("[SYSTEM] AEGIS Syslog abstractor initialized.\nAwaiting manual .log / .txt pipeline connection...\n")
        
        lbl_inst = ctk.CTkLabel(self.grid_output, text="Target Syslog File (.log / .txt):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_inst.pack(pady=(15, 5), anchor="w", padx=15)
        
        lbl_desc = ctk.CTkLabel(self.grid_output, text="Ingest authentication server logs. The Engine will map the file into a Pandas DataFrame\nand trigger critical Regex alerts for Brute Force activity.", font=ctk.CTkFont(size=11), text_color=self.text_secondary, justify="left")
        lbl_desc.pack(pady=(0, 15), anchor="w", padx=15)
        
        btn = ctk.CTkButton(self.grid_output, text="Load Syslog & Analyze", command=self._execute_syslog, fg_color=self.accent_primary)
        btn.pack(pady=5, anchor="w", padx=15)
        self.active_grid_widgets.extend([lbl_inst, lbl_desc, btn])

    def _execute_syslog(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(title="Load Syslog")
        if file_path:
            self.grid_label.configure(text=f"Data Grid: Sentinel Abstractor - {os.path.basename(file_path)}")
            self._clear_grid()
            
            df, anomalies = parse_auth_log(file_path)
            
            if anomalies:
                self._write_viewer("[!] CRITICAL ALERTS GENERATED\n" + "-"*50 + "\n" + "\n".join(anomalies))
            else:
                self._write_viewer("[*] Log parsed successfully. No known anomaly signatures found.")
                
            activity_tracker.log_activity("Syslog Auth Target", file_path, "Anomalies Found" if anomalies else "Success")
            self._update_evidence_tree()
            
            if df.empty: return
            
            # Primitive Dataframe Grid Renderer
            cols = list(df.columns)
            hdr_frame = ctk.CTkFrame(self.grid_output, fg_color="transparent")
            hdr_frame.pack(fill="x", padx=5)
            self.active_grid_widgets.append(hdr_frame)
            
            for i, c in enumerate(cols):
                ctk.CTkLabel(hdr_frame, text=str(c), font=ctk.CTkFont(weight="bold", size=10), width=100, anchor="w").grid(row=0, column=i)
                
            for index, row in df.head(50).iterrows(): # Show top 50 in GUI
                row_frame = ctk.CTkFrame(self.grid_output, fg_color="transparent")
                row_frame.pack(fill="x", padx=5)
                self.active_grid_widgets.append(row_frame)
                
                for i, c in enumerate(cols):
                    v = str(row[c])
                    if len(v) > 20: v = v[:17]+"..."
                    ctk.CTkLabel(row_frame, text=v, font=ctk.CTkFont(size=10), width=100, anchor="w").grid(row=0, column=i)

    def _run_decoder(self):
        self.grid_label.configure(text="Data Grid: Message Decoder Engine")
        self._clear_grid()
        self._write_viewer("[SYSTEM] Decoder matrix active.\nAwaiting manual string transmission...\n")
        
        lbl_inst = ctk.CTkLabel(self.grid_output, text="Input Hex / Base64 / Binary:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_inst.pack(pady=(15, 5), anchor="w", padx=15)
        
        txt_in = ctk.CTkTextbox(self.grid_output, height=100, border_width=1, border_color=self.pane_border)
        txt_in.pack(fill="x", padx=15, pady=5)
        
        enc_var = ctk.StringVar(value="Base64")
        opt = ctk.CTkOptionMenu(self.grid_output, variable=enc_var, values=["Base64", "Hex", "Binary"])
        opt.pack(pady=10, anchor="w", padx=15)
        
        def execute():
            result = decode_message(txt_in.get("0.0", "end"), enc_var.get())
            self.grid_label.configure(text=f"Data Grid: Decode ({enc_var.get()})")
            self._clear_grid()
            
            lbl = ctk.CTkLabel(self.grid_output, text="Translated Output Payload:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.pack(pady=15, anchor="w", padx=15)
            self.active_grid_widgets.append(lbl)
            
            out = ctk.CTkTextbox(self.grid_output, height=200, font=ctk.CTkFont(family="Consolas"), fg_color="transparent")
            out.insert("0.0", result)
            out.pack(fill="x", padx=15)
            self.active_grid_widgets.append(out)
            
            self._write_viewer(f"Action: Decoder string translation.\nType: {enc_var.get()}\nStatus: Finished.")
            activity_tracker.log_activity(f"Decoder", "Raw String Input", "Success")
            self._update_evidence_tree()
            
        btn = ctk.CTkButton(self.grid_output, text="Translate Payload", command=execute, fg_color=self.accent_primary)
        btn.pack(pady=5, anchor="w", padx=15)
        
        self.active_grid_widgets.extend([lbl_inst, txt_in, opt, btn])

    def _run_carving(self):
        self.grid_label.configure(text="Data Grid: Hexadecimal Data Carving")
        self._clear_grid()
        self._write_viewer("[SYSTEM] Carving engine initialized.\nAwaiting raw drive image or RAM dump...\n")
        
        lbl_inst = ctk.CTkLabel(self.grid_output, text="Select Raw Magic Pattern Target:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_inst.pack(pady=(15, 5), anchor="w", padx=15)
        
        lbl_desc = ctk.CTkLabel(self.grid_output, text="Isolate hard-coded Magic Number bounds directly from a raw Byte Stream.\nIdeal for memory forensics or unformatted volumes.", font=ctk.CTkFont(size=11), text_color=self.text_secondary, justify="left")
        lbl_desc.pack(pady=(0, 15), anchor="w", padx=15)
        
        btn = ctk.CTkButton(self.grid_output, text="Select Target & Output Path", command=self._execute_carving, fg_color=self.accent_primary)
        btn.pack(pady=5, anchor="w", padx=15)
        self.active_grid_widgets.extend([lbl_inst, lbl_desc, btn])

    def _execute_carving(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(title="Select Raw Magic Pattern Target")
        if file_path:
            out_dir = filedialog.askdirectory(title="Establish Target Output Directory")
            if out_dir:
                self.grid_label.configure(text=f"Data Grid: Carved Hex Artifacts - {os.path.basename(file_path)}")
                self._clear_grid()
                self._write_viewer("[SYSTEM] Analyzing raw byte stream for explicit signature blocks...")
                self.update()
                
                recovered = carve_files(file_path, out_dir)
                activity_tracker.log_activity("Data Carving", file_path, f"Recovered {len(recovered)}")
                self._update_evidence_tree()
                
                tbl = ctk.CTkFrame(self.grid_output, fg_color="transparent")
                tbl.pack(fill="x", padx=5, pady=5)
                self.active_grid_widgets.append(tbl)
                
                if recovered and not recovered[0].startswith("Error"):
                    ctk.CTkLabel(tbl, text="Loc", font=ctk.CTkFont(weight="bold", size=11), width=50).grid(row=0, column=0)
                    ctk.CTkLabel(tbl, text="Offset / Signature Mapped File", font=ctk.CTkFont(weight="bold", size=11), width=400, anchor="w").grid(row=0, column=1)
                    
                    r=1
                    for idx, f in enumerate(recovered):
                        ctk.CTkLabel(tbl, text=f"[{idx+1}]", width=50).grid(row=r, column=0)
                        ctk.CTkLabel(tbl, text=f, width=400, anchor="w", font=ctk.CTkFont(family="Consolas", size=10)).grid(row=r, column=1)
                        r+=1
                        
                    self._write_viewer(f"[SUCCESS] Isolated {len(recovered)} artifacts mapped via Header/Footer magic constants.\nData written to: {out_dir}")
                else:
                    self._write_viewer(f"[WARNING] 0 bytes isolated from stream. No valid heuristic magic blocks located.")

if __name__ == "__main__":
    app = ToolkitApp()
    app.mainloop()

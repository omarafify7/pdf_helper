import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime

# --------------------------
# PDF Concatenation Function
# --------------------------
def merge_pdfs(file_paths, output_path):
    """Merge multiple PDF files into one."""
    try:
        merger = PdfMerger()
        
        for path in file_paths:
            # Validate PDF before merging
            with open(path, 'rb') as f:
                reader = PdfReader(f)
                if len(reader.pages) == 0:
                    raise ValueError(f"File {os.path.basename(path)} is empty")
                
            merger.append(path)
        
        merger.write(output_path)
        merger.close()
        return True, f"Successfully created merged PDF: {output_path}"
    except Exception as e:
        return False, str(e)

# ----------------------
# GUI Related Functions
# ----------------------
class PDFMergerGUI:
    def __init__(self, master):
        self.master = master
        master.title("PDF Merger")
        
        # Configure grid
        master.columnconfigure(1, weight=1)
        
        # File list storage
        self.file_paths = []
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # File selection controls
        lbl_instructions = tk.Label(
            self.master, 
            text="Select PDFs to merge (order matters):"
        )
        lbl_instructions.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        
        # Listbox for PDF files
        self.listbox = tk.Listbox(
            self.master, 
            width=60, 
            height=8, 
            selectmode=tk.SINGLE
        )
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Control buttons
        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.btn_add = tk.Button(
            btn_frame, 
            text="Add PDFs", 
            command=self.add_files,
            width=12
        )
        self.btn_add.pack(side=tk.LEFT, padx=2)
        
        self.btn_remove = tk.Button(
            btn_frame, 
            text="Remove Selected", 
            command=self.remove_file,
            width=12
        )
        self.btn_remove.pack(side=tk.LEFT, padx=2)
        
        self.btn_move_up = tk.Button(
            btn_frame, 
            text="Move Up", 
            command=lambda: self.move_item(-1),
            width=12
        )
        self.btn_move_up.pack(side=tk.LEFT, padx=2)
        
        self.btn_move_down = tk.Button(
            btn_frame, 
            text="Move Down", 
            command=lambda: self.move_item(1),
            width=12
        )
        self.btn_move_down.pack(side=tk.LEFT, padx=2)
        
        # Merge button
        self.btn_merge = tk.Button(
            self.master, 
            text="Merge PDFs", 
            command=self.start_merge,
            width=20,
            height=2
        )
        self.btn_merge.grid(row=3, column=0, columnspan=3, pady=10)

    # ----------------------
    # Button Handlers
    # ----------------------
    def add_files(self):
        new_files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if new_files:
            self.file_paths.extend(new_files)
            self.update_listbox()
            
    def remove_file(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            del self.file_paths[index]
            self.update_listbox()
            
    def move_item(self, direction):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            new_index = index + direction
            if 0 <= new_index < len(self.file_paths):
                # Swap items in list
                self.file_paths[index], self.file_paths[new_index] = \
                    self.file_paths[new_index], self.file_paths[index]
                self.update_listbox()
                self.listbox.select_set(new_index)
                
    def start_merge(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No PDF files selected!")
            return
            
        # Create output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_{timestamp}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Perform merge
        success, message = merge_pdfs(self.file_paths, output_path)
        
        if success:
            messagebox.showinfo("Success", message)
            # Reset after successful merge
            self.file_paths = []
            self.update_listbox()
        else:
            messagebox.showerror("Merge Failed", message)
            
    # ----------------------
    # Helper Functions
    # ----------------------
    def update_listbox(self):
        """Update listbox with current file paths"""
        self.listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.listbox.insert(tk.END, os.path.basename(path))

# ----------------------
# Main Execution
# ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()
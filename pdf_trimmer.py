import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def trim_pdf(input_pdf, output_pdf, start_page, end_page):
    """
    Extracts pages from start_page to end_page (inclusive)
    from input_pdf and writes them to output_pdf.
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # PyPDF2 uses zero-based indices for pages
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

        with open(output_pdf, "wb") as f_out:
            writer.write(f_out)

        return True, f"Successfully created {output_pdf} with pages {start_page}-{end_page}."
    except Exception as e:
        return False, str(e)

def select_input_file():
    """Open a file dialog to select the input PDF."""
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        input_file_var.set(file_path)

def on_trim_clicked():
    """Handle the Trim button click."""
    input_file = input_file_var.get().strip()
    if not input_file:
        messagebox.showerror("Error", "No input file selected.")
        return

    # Read start and end page from the entries
    try:
        start_page = int(start_page_var.get().strip())
        end_page = int(end_page_var.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid page numbers.")
        return

    if start_page <= 0 or end_page <= 0:
        messagebox.showerror("Error", "Page numbers must be greater than 0.")
        return

    if end_page < start_page:
        messagebox.showerror("Error", "End page cannot be less than start page.")
        return

    # Generate output filename based on input file + range
    # Example: somePDF_trimmed_25_70.pdf
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = "output"  # <-- Added this line
    output_filename = f"{base_name}_trimmed_{start_page}_{end_page}.pdf"

    output_pdf = os.path.join(output_dir, output_filename)  # <-- Changed to use output directory

    success, msg = trim_pdf(input_file, output_pdf, start_page, end_page)
    if success:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", f"Error occurred: {msg}")

def create_gui():
    """Create and run the Tkinter GUI."""
    window = tk.Tk()
    window.title("PDF Trimmer")

    # Initialize StringVar variables after Tk() is created
    global input_file_var, start_page_var, end_page_var
    input_file_var = tk.StringVar()
    start_page_var = tk.StringVar()
    end_page_var = tk.StringVar()

    # 1. Input file selection
    lbl_input = tk.Label(window, text="Select PDF:")
    lbl_input.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_input = tk.Entry(window, textvariable=input_file_var, width=50)
    entry_input.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    btn_browse = tk.Button(window, text="Browse", command=select_input_file)
    btn_browse.grid(row=0, column=2, padx=10, pady=10)

    # 2. Start page
    lbl_start = tk.Label(window, text="Start Page:")
    lbl_start.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    entry_start = tk.Entry(window, textvariable=start_page_var, width=10)
    entry_start.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # 3. End page
    lbl_end = tk.Label(window, text="End Page:")
    lbl_end.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    entry_end = tk.Entry(window, textvariable=end_page_var, width=10)
    entry_end.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # 4. Trim button
    btn_trim = tk.Button(window, text="Trim PDF", command=on_trim_clicked, width=15)
    btn_trim.grid(row=3, column=0, columnspan=3, pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_gui()

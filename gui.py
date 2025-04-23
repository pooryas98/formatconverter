import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from converter import convert_html_to_txt # Import the conversion function

class HtmlToTxtConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("HTML to TXT Converter")
        master.geometry("600x450") # Adjusted size

        self.input_files = []
        self.output_dir = tk.StringVar(value=os.getcwd()) # Default to current dir
        self.same_dir_var = tk.BooleanVar(value=False)

        # --- Input File Selection ---
        self.input_frame = ttk.LabelFrame(master, text="Input HTML Files")
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.select_files_button = ttk.Button(self.input_frame, text="Select Files...", command=self.select_input_files)
        self.select_files_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_list_label = ttk.Label(self.input_frame, text="Selected Files:")
        self.file_list_label.pack(side=tk.LEFT, padx=5)

        # Use a Listbox to show selected files
        self.file_listbox = tk.Listbox(self.input_frame, height=5, width=60)
        self.file_listbox.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)
        # Add scrollbar to listbox
        self.scrollbar = ttk.Scrollbar(self.input_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)


        # --- Output Options ---
        self.output_frame = ttk.LabelFrame(master, text="Output Options")
        self.output_frame.pack(padx=10, pady=5, fill="x")

        self.same_dir_check = ttk.Checkbutton(
            self.output_frame,
            text="Save output in the same folder as input",
            variable=self.same_dir_var,
            command=self.toggle_output_dir_selection
        )
        self.same_dir_check.pack(anchor=tk.W, padx=5, pady=5)

        self.output_dir_frame = ttk.Frame(self.output_frame) # Frame to hold dir selection
        self.output_dir_frame.pack(fill="x", padx=5, pady=5)

        self.select_output_button = ttk.Button(self.output_dir_frame, text="Select Output Folder...", command=self.select_output_dir)
        self.select_output_button.pack(side=tk.LEFT, padx=5)

        self.output_dir_entry = ttk.Entry(self.output_dir_frame, textvariable=self.output_dir, width=50, state="readonly")
        self.output_dir_entry.pack(side=tk.LEFT, fill="x", expand=True)

        # --- Conversion & Status ---
        self.action_frame = ttk.Frame(master)
        self.action_frame.pack(padx=10, pady=10, fill="x")

        self.convert_button = ttk.Button(self.action_frame, text="Convert", command=self.start_conversion)
        self.convert_button.pack(pady=5)

        self.status_label = ttk.Label(self.action_frame, text="Status:")
        self.status_label.pack(anchor=tk.W, pady=(5,0))

        self.status_text = tk.Text(self.action_frame, height=8, width=70, state="disabled", wrap=tk.WORD)
        self.status_text.pack(fill="both", expand=True)
        # Add scrollbar to status text
        self.status_scrollbar = ttk.Scrollbar(self.action_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, before=self.status_text) # Place scrollbar correctly
        self.status_text.config(yscrollcommand=self.status_scrollbar.set)


        # Initial state update
        self.toggle_output_dir_selection()

    def select_input_files(self):
        files = filedialog.askopenfilenames(
            title="Select HTML Files",
            filetypes=[("HTML files", "*.html *.htm"), ("All files", "*.*")]
        )
        if files:
            self.input_files = list(files)
            self.file_listbox.delete(0, tk.END) # Clear previous list
            for f in self.input_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))
            self.update_status(f"{len(self.input_files)} file(s) selected.")

    def toggle_output_dir_selection(self):
        if self.same_dir_var.get():
            self.select_output_button.config(state="disabled")
            self.output_dir_entry.config(state="disabled")
        else:
            self.select_output_button.config(state="normal")
            self.output_dir_entry.config(state="readonly") # Keep readonly, but enable button

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Folder")
        if directory:
            self.output_dir.set(directory)
            self.update_status(f"Output folder set to: {directory}")

    def update_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END) # Scroll to the bottom
        self.status_text.config(state="disabled")
        self.master.update_idletasks() # Ensure UI updates

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("No Input Files", "Please select one or more HTML files first.")
            return

        self.convert_button.config(state="disabled")
        self.update_status("Starting conversion...")

        success_count = 0
        fail_count = 0

        for html_file in self.input_files:
            base_name = os.path.basename(html_file)
            name_without_ext = os.path.splitext(base_name)[0]
            txt_filename = f"{name_without_ext}.txt"

            if self.same_dir_var.get():
                output_path = os.path.join(os.path.dirname(html_file), txt_filename)
            else:
                selected_output_dir = self.output_dir.get()
                if not selected_output_dir or not os.path.isdir(selected_output_dir):
                     messagebox.showerror("Invalid Output Folder", f"The selected output folder is invalid or does not exist:\n{selected_output_dir}")
                     self.update_status("Conversion aborted due to invalid output folder.")
                     self.convert_button.config(state="normal")
                     return
                output_path = os.path.join(selected_output_dir, txt_filename)

            self.update_status(f"Converting '{base_name}'...")
            success, message = convert_html_to_txt(html_file, output_path)
            self.update_status(message)

            if success:
                success_count += 1
            else:
                fail_count += 1

        final_message = f"Conversion finished. {success_count} successful, {fail_count} failed."
        self.update_status(final_message)
        messagebox.showinfo("Conversion Complete", final_message)
        self.convert_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = HtmlToTxtConverterApp(root)
    root.mainloop()

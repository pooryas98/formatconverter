import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from converter import convert_html_to_txt # Import the conversion function

class HtmlToTxtConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("HTML to TXT Converter")
        master.geometry("600x450") # Adjusted size

        self.input_files = [] # List of full paths
        self.output_dir = tk.StringVar(value=os.getcwd()) # Default to current dir
        self.same_dir_var = tk.BooleanVar(value=False)
        self.single_file_var = tk.BooleanVar(value=False) # Variable for the new checkbox

        # --- Input File Selection ---
        self.input_frame = ttk.LabelFrame(master, text="Input HTML Files")
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.select_files_button = ttk.Button(self.input_frame, text="Select Files...", command=self.select_input_files)
        self.select_files_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_list_label = ttk.Label(self.input_frame, text="Selected Files:")
        self.file_list_label.pack(side=tk.LEFT, padx=5)

        # Use a Listbox to show selected files
        # Frame for listbox and reorder buttons
        self.listbox_frame = ttk.Frame(self.input_frame)
        self.listbox_frame.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

        self.file_listbox = tk.Listbox(self.listbox_frame, height=5, width=55) # Adjusted width
        self.file_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        # Add scrollbar to listbox
        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        # Reorder buttons frame
        self.reorder_frame = ttk.Frame(self.input_frame)
        self.reorder_frame.pack(side=tk.LEFT, padx=(0, 5), fill="y")

        self.move_up_button = ttk.Button(self.reorder_frame, text="↑", command=self.move_file_up, width=2)
        self.move_up_button.pack(pady=2)

        self.move_down_button = ttk.Button(self.reorder_frame, text="↓", command=self.move_file_down, width=2)
        self.move_down_button.pack(pady=2)


        # --- Output Options ---
        self.output_frame = ttk.LabelFrame(master, text="Output Options")
        self.output_frame.pack(padx=10, pady=5, fill="x")

        self.same_dir_check = ttk.Checkbutton(
            self.output_frame,
            text="Save output in the same folder as input",
            variable=self.same_dir_var,
            command=self.toggle_output_options # Corrected command
        )
        self.same_dir_check.pack(anchor=tk.W, padx=5, pady=2) # Reduced pady

        # Add the new checkbox for single file export
        self.single_file_check = ttk.Checkbutton(
            self.output_frame,
            text="Export to single file",
            variable=self.single_file_var,
            command=self.toggle_output_options # Add command to potentially disable other options
        )
        self.single_file_check.pack(anchor=tk.W, padx=5, pady=2)

        self.output_dir_frame = ttk.Frame(self.output_frame) # Frame to hold dir selection
        self.output_dir_frame.pack(fill="x", padx=5, pady=2)

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
        self.toggle_output_options() # Call the combined toggle function

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

    def move_file_up(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        if index > 0:
            # Move item in the listbox
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index - 1, text)
            self.file_listbox.selection_set(index - 1)
            # Move item in the underlying data list (self.input_files)
            self.input_files.insert(index - 1, self.input_files.pop(index))

    def move_file_down(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        if index < self.file_listbox.size() - 1:
            # Move item in the listbox
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index + 1, text)
            self.file_listbox.selection_set(index + 1)
            # Move item in the underlying data list (self.input_files)
            self.input_files.insert(index + 1, self.input_files.pop(index))

    def toggle_output_options(self):
        # Handles enabling/disabling based on BOTH checkboxes
        if self.single_file_var.get():
            # Single file mode: disable individual dir options
            self.same_dir_check.config(state="disabled")
            self.select_output_button.config(state="disabled")
            self.output_dir_entry.config(state="disabled")
            self.same_dir_var.set(False) # Uncheck same dir if single file is checked
        else:
            # Multi-file mode: re-enable individual dir options
            self.same_dir_check.config(state="normal")
            # Enable/disable output dir based on 'same dir' checkbox
            if self.same_dir_var.get():
                self.select_output_button.config(state="disabled")
                self.output_dir_entry.config(state="disabled")
            else:
                self.select_output_button.config(state="normal")
                self.output_dir_entry.config(state="readonly") # Keep readonly

    def select_output_dir(self):
        # This is only relevant if not in single file mode and not same dir
        if self.single_file_var.get() or self.same_dir_var.get():
             return # Should not be callable, but good practice
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
        final_message = ""

        # --- Single File Export Logic ---
        if self.single_file_var.get():
            # Ask user for the output file name and location
            single_output_path = filedialog.asksaveasfilename(
                title="Save Combined Text File As...",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if not single_output_path:
                self.update_status("Conversion cancelled by user (no output file selected).")
                self.convert_button.config(state="normal")
                return

            combined_content = []
            self.update_status(f"Combining files into: {os.path.basename(single_output_path)}")

            # Use the potentially reordered self.input_files
            for html_file in self.input_files:
                base_name = os.path.basename(html_file)
                self.update_status(f"Processing '{base_name}'...")
                # Call converter to get content
                success, content_or_error = convert_html_to_txt(html_file, return_content=True)

                if success:
                    combined_content.append(content_or_error)
                    success_count += 1
                    self.update_status(f" -> Added content from '{base_name}'.")
                else:
                    fail_count += 1
                    self.update_status(f" -> Failed to process '{base_name}': {content_or_error}") # content_or_error is error msg here

            # Write the combined content to the single file
            try:
                with open(single_output_path, 'w', encoding='utf-8') as f_out:
                    # Add a separator between files for clarity
                    f_out.write("\n\n--- File Separator ---\n\n".join(combined_content))
                self.update_status(f"Successfully saved combined output to: {single_output_path}")
                final_message = f"Conversion finished. Combined {success_count} file(s) into '{os.path.basename(single_output_path)}'. {fail_count} file(s) failed processing."
            except Exception as e:
                final_message = f"Error writing combined file: {e}"
                self.update_status(final_message)
                messagebox.showerror("File Write Error", final_message)
                self.convert_button.config(state="normal")
                return

        # --- Multiple File Export Logic (Original logic, but uses reordered list) ---
        else:
            # Use the potentially reordered self.input_files
            for html_file in self.input_files:
                base_name = os.path.basename(html_file)
                name_without_ext = os.path.splitext(base_name)[0]
                txt_filename = f"{name_without_ext}.txt"

                output_path = ""
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
                # Call converter to write file directly
                success, message = convert_html_to_txt(html_file, txt_filepath=output_path, return_content=False)
                self.update_status(message)

                if success:
                    success_count += 1
                else:
                    fail_count += 1

            final_message = f"Conversion finished. {success_count} successful, {fail_count} failed."

        # --- Final Status Update and Cleanup ---
        self.update_status(final_message)
        messagebox.showinfo("Conversion Complete", final_message)
        self.convert_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = HtmlToTxtConverterApp(root)
    root.mainloop()

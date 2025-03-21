import tkinter as tk
from tkinter import filedialog, messagebox
import os

class NotePad:
    def  __init__(self, root):
        self.root = root
        self.root.title("NotePad")
        self.file_path = None
        
        # Text Widget
        self.text_area = tk.Text(root, undo=True, wrap='word')
        self.text_area.pack(expand=1, fill='both')
        
        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find and Replace", command=self.find_and_replace_dialog)

        self.file_path = None
        
    def new_file(self):
        if self.confirm_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.file_path = None
            self.root.title("NotePad - New File")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END) 
                self.text_area.insert(tk.END, content)  
                self.file_path = file_path  
                self.root.title(f"Simple Notepad - {file_path}")  
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
                    
    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_as_file()
    
    def save_as_file(self): 
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Save As")
        
        if file_path: 
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.file_path = file_path
                self.root.title(f"Simple Notepad - {file_path}")
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def write_to_file(self, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'r') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_path = file_path
            self.root.title(f"NotePad - {file_path}")
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    
    def exit_app(self):
        if self.confirm_unsaved_changes():
            self.root.destroy()
        
    def confirm_unsaved_changes(self):
        if self.text_area.edit_modified():
            res = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if res:
                self.save_file()
                return True
            elif res is False:
                return True
            else:
                return False
        return True
    
    def find_and_replace_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Find and Replace")
        dialog.geometry("300x150")

        tk.Label(dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        find_entry = tk.Entry(dialog, width=25)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Replace:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        replace_entry = tk.Entry(dialog, width=25)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(dialog, text="Replace All", command=lambda: self.find_and_replace(find_entry.get(), replace_entry.get(), dialog)).grid(row=2, column=0, columnspan=2, pady=10)

    def find_and_replace(self, target, replacement, dialog):
        text = self.text_area.get(1.0, tk.END)
        
        result = self.find_and_replace_logic(text, target, replacement)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)

        dialog.destroy()
        messagebox.showinfo("Find and Replace", f"All occurrences of '{target}' replaced with '{replacement}'.")
    
    @staticmethod
    def find_and_replace_logic(text, target, replacement):
        res = []
        i = 0
        
        while i < len(text):
            if text[i:i+len(target)] == target:
                res.append(replacement)
                i += len(target)
            else:
                res.append(text[i])
                i += 1
        return ''.join(res)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = NotePad(root)
    root.mainloop()
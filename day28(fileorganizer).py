import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import datetime

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Set color scheme - dark mode with accent colors
        self.bg_color = "#1E1E1E"
        self.text_color = "#FFFFFF"
        self.accent_color = "#007BFF"
        self.secondary_color = "#2D2D2D"
        self.success_color = "#28A745"
        self.warning_color = "#FFC107"
        
        self.root.configure(bg=self.bg_color)
        
        # File type categories
        self.file_types = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".java", ".html", ".css", ".js", ".cpp", ".c", ".php", ".json", ".xml"]
        }
        
        # Selected directory and custom categories
        self.selected_directory = tk.StringVar()
        self.custom_categories = {}
        self.is_organizing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Smart File Organizer", 
            font=("Helvetica", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Directory selection frame
        dir_frame = tk.Frame(main_frame, bg=self.secondary_color, padx=15, pady=15)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        dir_label = tk.Label(
            dir_frame,
            text="Select Directory to Organize:",
            font=("Helvetica", 12),
            fg=self.text_color,
            bg=self.secondary_color
        )
        dir_label.pack(anchor="w", pady=(0, 10))
        
        dir_selection_frame = tk.Frame(dir_frame, bg=self.secondary_color)
        dir_selection_frame.pack(fill=tk.X)
        
        self.dir_entry = tk.Entry(
            dir_selection_frame,
            textvariable=self.selected_directory,
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.text_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.accent_color,
            insertbackground=self.text_color
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(
            dir_selection_frame,
            text="Browse",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg=self.text_color,
            bd=0,
            padx=15,
            pady=5,
            activebackground=self.accent_color,
            activeforeground=self.text_color,
            cursor="hand2",
            command=self.browse_directory
        )
        browse_button.pack(side=tk.RIGHT)
        
        # Categories frame
        categories_frame = tk.Frame(main_frame, bg=self.secondary_color, padx=15, pady=15)
        categories_frame.pack(fill=tk.BOTH, expand=True)
        
        categories_label = tk.Label(
            categories_frame,
            text="File Categories:",
            font=("Helvetica", 12),
            fg=self.text_color,
            bg=self.secondary_color
        )
        categories_label.pack(anchor="w", pady=(0, 10))
        
        # Create a canvas for scrolling
        canvas = tk.Canvas(categories_frame, bg=self.secondary_color, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(categories_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.secondary_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add default categories as checkboxes
        self.category_vars = {}
        for idx, (category, extensions) in enumerate(self.file_types.items()):
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            
            category_frame = tk.Frame(scrollable_frame, bg=self.secondary_color, pady=5)
            category_frame.pack(fill=tk.X)
            
            checkbox = tk.Checkbutton(
                category_frame,
                text=f"{category} ({', '.join(extensions)})",
                variable=var,
                font=("Helvetica", 11),
                fg=self.text_color,
                bg=self.secondary_color,
                selectcolor=self.bg_color,
                activebackground=self.secondary_color,
                activeforeground=self.text_color
            )
            checkbox.pack(side=tk.LEFT)
        
        # Custom category section
        custom_label = tk.Label(
            scrollable_frame,
            text="Add Custom Category:",
            font=("Helvetica", 12),
            fg=self.accent_color,
            bg=self.secondary_color,
            pady=10
        )
        custom_label.pack(anchor="w", pady=(15, 5))
        
        custom_frame = tk.Frame(scrollable_frame, bg=self.secondary_color)
        custom_frame.pack(fill=tk.X, pady=(0, 10))
        
        category_name_frame = tk.Frame(custom_frame, bg=self.secondary_color)
        category_name_frame.pack(fill=tk.X, pady=(0, 5))
        
        category_label = tk.Label(
            category_name_frame,
            text="Category Name:",
            font=("Helvetica", 10),
            fg=self.text_color,
            bg=self.secondary_color,
            width=15,
            anchor="w"
        )
        category_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_entry = tk.Entry(
            category_name_frame,
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.text_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.accent_color,
            insertbackground=self.text_color
        )
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        extensions_frame = tk.Frame(custom_frame, bg=self.secondary_color)
        extensions_frame.pack(fill=tk.X, pady=(0, 5))
        
        extensions_label = tk.Label(
            extensions_frame,
            text="Extensions:",
            font=("Helvetica", 10),
            fg=self.text_color,
            bg=self.secondary_color,
            width=15,
            anchor="w"
        )
        extensions_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.extensions_entry = tk.Entry(
            extensions_frame,
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.text_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.accent_color,
            insertbackground=self.text_color
        )
        self.extensions_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        add_category_button = tk.Button(
            custom_frame,
            text="Add Category",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg=self.text_color,
            bd=0,
            padx=15,
            pady=5,
            activebackground=self.accent_color,
            activeforeground=self.text_color,
            cursor="hand2",
            command=self.add_custom_category
        )
        add_category_button.pack(pady=(5, 0))
        
        # Bottom frame for status and organize button
        bottom_frame = tk.Frame(main_frame, bg=self.bg_color, pady=15)
        bottom_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            bottom_frame,
            text="Ready to organize files.",
            font=("Helvetica", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.organize_button = tk.Button(
            bottom_frame,
            text="Organize Files",
            font=("Helvetica", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            bd=0,
            padx=20,
            pady=10,
            activebackground=self.accent_color,
            activeforeground=self.text_color,
            cursor="hand2",
            command=self.start_organizing
        )
        self.organize_button.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            orient=tk.HORIZONTAL, 
            mode='indeterminate',
            style="Accent.Horizontal.TProgressbar"
        )
        
        # Configure ttk style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Accent.Horizontal.TProgressbar", 
            background=self.accent_color,
            troughcolor=self.secondary_color
        )
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)
    
    def add_custom_category(self):
        category_name = self.category_entry.get().strip()
        extensions_text = self.extensions_entry.get().strip()
        
        if not category_name or not extensions_text:
            self.status_label.config(text="Please provide both category name and extensions.", fg=self.warning_color)
            return
        
        # Parse extensions
        extensions = [ext.strip() for ext in extensions_text.split(",")]
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        # Add to custom categories
        self.custom_categories[category_name] = extensions
        
        # Add checkbox for the new category
        var = tk.BooleanVar(value=True)
        self.category_vars[category_name] = var
        
        # Create a new checkbox in the scrollable frame
        scrollable_frame = self.root.nametowidget(self.root.nametowidget(".!frame.!frame3.!canvas").create_window()[1])
        
        category_frame = tk.Frame(scrollable_frame, bg=self.secondary_color, pady=5)
        category_frame.pack(fill=tk.X, before=scrollable_frame.winfo_children()[-3])  # Insert before custom category section
        
        checkbox = tk.Checkbutton(
            category_frame,
            text=f"{category_name} ({', '.join(extensions)})",
            variable=var,
            font=("Helvetica", 11),
            fg=self.text_color,
            bg=self.secondary_color,
            selectcolor=self.bg_color,
            activebackground=self.secondary_color,
            activeforeground=self.text_color
        )
        checkbox.pack(side=tk.LEFT)
        
        # Clear entries
        self.category_entry.delete(0, tk.END)
        self.extensions_entry.delete(0, tk.END)
        
        self.status_label.config(text=f"Custom category '{category_name}' added successfully.", fg=self.success_color)
    
    def start_organizing(self):
        if self.is_organizing:
            return
        
        directory = self.selected_directory.get()
        if not directory or not os.path.isdir(directory):
            self.status_label.config(text="Please select a valid directory.", fg=self.warning_color)
            return
        
        # Collect active categories
        active_categories = {}
        for category, var in self.category_vars.items():
            if var.get():
                if category in self.file_types:
                    active_categories[category] = self.file_types[category]
                else:
                    active_categories[category] = self.custom_categories[category]
        
        if not active_categories:
            self.status_label.config(text="Please select at least one category to organize.", fg=self.warning_color)
            return
        
        # Start organizing in a separate thread
        self.is_organizing = True
        self.organize_button.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X, pady=(15, 0))
        self.progress.start()
        self.status_label.config(text="Organizing files...", fg=self.text_color)
        
        organize_thread = threading.Thread(target=self.organize_files, args=(directory, active_categories))
        organize_thread.daemon = True
        organize_thread.start()
    
    def organize_files(self, directory, categories):
        try:
            # Create a log file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(directory, f"file_organizer_log_{timestamp}.txt")
            log_content = [f"File Organization Log - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
            log_content.append(f"Directory: {directory}\n")
            log_content.append("Categories:\n")
            
            for category, extensions in categories.items():
                log_content.append(f"- {category}: {', '.join(extensions)}\n")
            
            log_content.append("\nMoved Files:\n")
            
            # Count files
            all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            processed_count = 0
            moved_count = 0
            
            # Process files
            for filename in all_files:
                file_path = os.path.join(directory, filename)
                
                # Skip log files
                if filename.startswith("file_organizer_log_"):
                    continue
                
                processed_count += 1
                
                # Get file extension
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension.lower()
                
                # Find matching category
                target_category = "Other"
                for category, extensions in categories.items():
                    if file_extension in extensions:
                        target_category = category
                        break
                
                # Create category folder if it doesn't exist
                category_folder = os.path.join(directory, target_category)
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                
                # Move file to category folder
                new_path = os.path.join(category_folder, filename)
                
                # Handle duplicate file names
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(new_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    new_path = os.path.join(category_folder, new_filename)
                    counter += 1
                
                try:
                    shutil.move(file_path, new_path)
                    moved_count += 1
                    log_content.append(f"- {filename} -> {target_category}/{os.path.basename(new_path)}\n")
                except Exception as e:
                    log_content.append(f"- ERROR: Failed to move {filename}: {str(e)}\n")
            
            # Create "Other" folder for uncategorized files if needed
            if "Other" not in categories:
                other_folder = os.path.join(directory, "Other")
                if os.path.exists(other_folder) and not os.listdir(other_folder):
                    os.rmdir(other_folder)
            
            # Summary
            log_content.append("\nSummary:\n")
            log_content.append(f"- Files processed: {processed_count}\n")
            log_content.append(f"- Files moved: {moved_count}\n")
            
            # Write log file
            with open(log_path, 'w') as log_file:
                log_file.writelines(log_content)
            
            # Update UI on the main thread
            self.root.after(0, self.organize_completed, moved_count, processed_count, log_path)
            
        except Exception as e:
            self.root.after(0, self.organize_failed, str(e))
    
    def organize_completed(self, moved_count, processed_count, log_path):
        self.progress.stop()
        self.progress.pack_forget()
        self.is_organizing = False
        self.organize_button.config(state=tk.NORMAL)
        
        success_message = f"Organization complete! {moved_count} of {processed_count} files organized. Details in log file."
        self.status_label.config(text=success_message, fg=self.success_color)
    
    def organize_failed(self, error_message):
        self.progress.stop()
        self.progress.pack_forget()
        self.is_organizing = False
        self.organize_button.config(state=tk.NORMAL)
        
        self.status_label.config(text=f"Error during organization: {error_message}", fg=self.warning_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()
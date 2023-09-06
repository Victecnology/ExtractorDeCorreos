import tkinter as tk
import re
import tkinter.filedialog as filedialog
import json

def extract_emails(text):
  """
  Extracts all emails from a given text string.

  Args:
    text: The text string to extract emails from.

  Returns:
    A list of all emails found in the text string.
  """

  emails = []
  for match in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
    emails.append(match.group(0))
  return emails


class EmailExtractorGUI(tk.Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()

    self.text_input = tk.Text(self, height=10, width=50)
    self.text_input.pack(side=tk.TOP)

    self.extract_button = tk.Button(self, text="Extract Emails", command=self.extract_emails)
    self.extract_button.pack(side=tk.BOTTOM)

    self.results_label = tk.Label(self, text="Results:")
    self.results_label.pack(side=tk.TOP)

    self.results_listbox = tk.Listbox(self)
    self.results_listbox.pack(side=tk.BOTTOM)

    self.save_button = tk.Button(self, text="Save Results", command=self.save_results)
    self.save_button.pack(side=tk.BOTTOM)

    self.export_file_type_var = tk.StringVar(value="CSV")
    self.export_file_type_label = tk.Label(self, text="Export file type:")
    self.export_file_type_label.pack(side=tk.TOP)
    self.export_file_type_menu = tk.OptionMenu(self, self.export_file_type_var, "CSV", "JSON")
    self.export_file_type_menu.pack(side=tk.TOP)

  def extract_emails(self):
    text = self.text_input.get("1.0", "end-1c")
    emails = extract_emails(text)
    self.results_listbox.delete(0, tk.END)
    for email in emails:
      self.results_listbox.insert(tk.END, email)

  def save_results(self):
    filename = filedialog.asksaveasfilename(title="Save Results", filetypes=[("Text files", "*.txt")])
    if filename:
      file_type = self.export_file_type_var.get()
      if file_type == "CSV":
        with open(filename, "w") as f:
          for email in self.results_listbox.get(0, tk.END):
            f.write(email + "\n")
      elif file_type == "JSON":
        with open(filename, "w") as f:
          f.write(json.dumps(list(self.results_listbox.get(0, tk.END))))


if __name__ == "__main__":
  root = tk.Tk()
  EmailExtractorGUI(root).pack()
  root.mainloop()
import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from plyer import notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurar tus credenciales de correo electrónico
email_address = 'guerreroh335@gmail.com'
email_password = 'TICOdrawinghacker'


class TodoListApp:
    def __init__(self, master):
        self.master = master
        master.title("Lista de Tareas")

        # Colores y estilos
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.button_hover_color = "#45a049"
        self.text_color = "#333333"
        self.entry_color = "#ffffff"
        self.entry_border_color = "#cccccc"
        self.listbox_color = "#ffffff"
        self.listbox_border_color = "#cccccc"

        self.master.configure(bg=self.bg_color)
        self.master.geometry("400x500")

        # Frame para los botones
        self.button_frame = tk.Frame(master, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        # Inicialización de la lista de tareas
        self.task_listbox = tk.Listbox(
            master, selectmode=tk.SINGLE, bg=self.listbox_color, bd=2, relief=tk.FLAT, font=('Arial', 12))
        self.task_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.tasks = []  # Lista de tareas

        self.load_tasks()  # Cargar tareas al iniciar la aplicación

        # Etiqueta y campo de entrada
        self.task_label = tk.Label(master, text="Ingrese la tarea:",
                                   bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.task_label.pack()

        self.task_entry = tk.Entry(
            master, bg=self.entry_color, bd=2, relief=tk.FLAT, font=('Arial', 12))
        self.task_entry.pack(padx=10, pady=5, fill=tk.BOTH)

        # Prioridades
        self.priority_label = tk.Label(
            master, text="Prioridad:", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.priority_label.pack()

        self.priority_var = tk.StringVar(master)
        self.priority_var.set("Alta")
        self.priority_menu = tk.OptionMenu(
            master, self.priority_var, "Alta", "Media", "Baja")
        self.priority_menu.config(bg=self.bg_color, bd=2, relief=tk.FLAT)
        self.priority_menu.pack(padx=10, pady=5, fill=tk.BOTH)

        # Etiquetas y categorías
        self.tags_label = tk.Label(
            master, text="Etiquetas:", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.tags_label.pack()

        self.tags_entry = tk.Entry(
            master, bg=self.entry_color, bd=2, relief=tk.FLAT, font=('Arial', 12))
        self.tags_entry.pack(padx=10, pady=5, fill=tk.BOTH)

        # Duración de la tarea
        self.duration_label = tk.Label(
            master, text="Duración (minutos):", bg=self.bg_color, fg=self.text_color, font=('Arial', 12))
        self.duration_label.pack()

        self.duration_entry = tk.Entry(
            master, bg=self.entry_color, bd=2, relief=tk.FLAT, font=('Arial', 12))
        self.duration_entry.pack(padx=10, pady=5, fill=tk.BOTH)

        # Botón de agregar tarea
        self.add_button = tk.Button(self.button_frame, text="Agregar tarea", bg=self.button_color, fg="white",
                                    activebackground=self.button_hover_color, bd=0, relief=tk.FLAT,
                                    command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        # Botón de eliminar tarea
        self.remove_button = tk.Button(self.button_frame, text="Eliminar tarea", bg=self.button_color, fg="white",
                                       activebackground=self.button_hover_color, bd=0, relief=tk.FLAT,
                                       command=self.remove_task)
        self.remove_button.grid(row=0, column=1, padx=5)

        # Botón de mostrar tareas
        self.show_button = tk.Button(self.button_frame, text="Mostrar tareas", bg=self.button_color, fg="white",
                                     activebackground=self.button_hover_color, bd=0, relief=tk.FLAT,
                                     command=self.display_tasks)
        self.show_button.grid(row=0, column=2, padx=5)

        # Botón de salir
        self.quit_button = tk.Button(self.button_frame, text="Salir", bg=self.button_color, fg="white",
                                     activebackground=self.button_hover_color, bd=0, relief=tk.FLAT,
                                     command=self.save_and_quit)
        self.quit_button.grid(row=0, column=3, padx=5)

        # Llamar save_and_quit al cerrar la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

        # Verificar tareas al iniciar la aplicación
        self.check_task_duration()

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        tags = self.tags_entry.get()
        duration = self.duration_entry.get()
        # Verificar si la duración es un número válido y mayor que cero
        if task and duration.isdigit() and int(duration) > 0:
            duration = int(duration)
            self.tasks.append({"task": task, "priority": priority, "tags": tags,
                               "duration": duration, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Tarea agregada exitosamente.")
            notification.notify(
                title="Tarea agregada",
                message=f"Se ha agregado la tarea: {task}",
                app_name="TodoListApp"
            )
        else:
            messagebox.showwarning(
                "Advertencia", "Ingrese una tarea válida y una duración válida (en minutos).")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            removed_task = self.tasks.pop(task_index)
            self.task_listbox.delete(task_index)
            messagebox.showinfo("Éxito", f"Tarea '{
                                removed_task['task']}' eliminada exitosamente.")

            notification.notify(
                title="Tarea eliminada",
                message=f"Se ha eliminado la tarea: {removed_task['task']}",
                app_name="TodoListApp")

        else:
            messagebox.showwarning(
                "Advertencia", "Seleccione una tarea para eliminar.")

    def display_tasks(self):
        if self.tasks:
            task_info = ""
            for index, task in enumerate(self.tasks):
                task_info += f"{index+1}. Tarea: {task['task']}\n"
                task_info += f"   - Prioridad: {task['priority']}\n"
                task_info += f"   - Etiquetas: {task['tags']}\n"
                task_info += f"   - Duración: {task['duration']} minutos\n"
                task_info += f"   - Fecha: {task['timestamp']}\n\n"

            messagebox.showinfo("Lista de Tareas", task_info)
        else:
            messagebox.showinfo("Lista de Tareas",
                                "La lista de tareas está vacía.")

    def save_and_quit(self):
        self.save_tasks()
        self.master.destroy()

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, task['task'])
        except FileNotFoundError:
            self.tasks = []

    def check_task_duration(self):
        current_time = datetime.now()
        for task in self.tasks:
            task_time = datetime.strptime(
                task["timestamp"], "%Y-%m-%d %H:%M:%S")
            time_diff = current_time - task_time
            if time_diff.seconds >= task["duration"] * 60:
                # Tarea vencida, notificar al usuario
                notification.notify(
                    title="Tarea Vencida",
                    message=f"La tarea '{task['task']}' ha expirado.",
                    app_name="TodoListApp"
                )
                # Opcional: eliminar la tarea automáticamente
                self.tasks.remove(task)
                self.save_tasks()

    def send_email(self, task):
        # Configurar el servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)

        # Construir el mensaje
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = email_address
        msg['Subject'] = "Tarea Vencida"
        body = f"La tarea '{task['task']}' ha expirado."
        msg.attach(MIMEText(body, 'plain'))

        # Enviar el mensaje de correo electrónico
        server.send_message(msg)
        del msg

        # Cerrar la conexión SMTP
        server.quit()


def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

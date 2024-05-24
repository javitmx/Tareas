class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print("Tarea eliminada exitosamente.")
        else:
            print("La tarea no existe en la lista.")

    def display_tasks(self):
        if self.tasks:
            print("Lista de tareas:")
            for index, task in enumerate(self.tasks, start=1):
                print(f"{index}. {task}")
        else:
            print("La lista de tareas está vacía.")


def main():
    todo_list = TodoList()

    while True:
        print("\n--- Menú ---")
        print("1. Agregar tarea")
        print("2. Eliminar tarea")
        print("3. Mostrar tareas")
        print("4. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            task = input("Ingrese la tarea: ")
            todo_list.add_task(task)
            print("Tarea agregada exitosamente.")

        elif choice == "2":
            if todo_list.tasks:
                todo_list.display_tasks()
                task_index = int(
                    input("Ingrese el número de tarea a eliminar: "))
                if 1 <= task_index <= len(todo_list.tasks):
                    todo_list.remove_task(todo_list.tasks[task_index - 1])
                else:
                    print("Número de tarea inválido.")
            else:
                print("No hay tareas para eliminar.")

        elif choice == "3":
            todo_list.display_tasks()

        elif choice == "4":
            print("¡Adiós!")
            break

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()

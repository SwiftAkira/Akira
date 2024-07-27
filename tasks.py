from memory import load_memory, save_memory

def manage_tasks():
    tasks = load_memory()
    while True:
        command = input("Task command (add/view/exit): ").lower()
        if command == "add":
            task = input("Enter the task: ")
            tasks.append(task)
            save_memory(tasks)
            print("Task added.")
        elif command == "view":
            if tasks:
                print("Your tasks:")
                for idx, task in enumerate(tasks, 1):
                    print(f"{idx}. {task}")
            else:
                print("No tasks added.")
        elif command == "exit":
            break
        else:
            print("Invalid command. Please enter 'add', 'view', or 'exit'.")
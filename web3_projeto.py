import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import mysql.connector
from mysql.connector import Error


class LoginForm:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Register a client")

        self.username_label = ttk.Label(self.window, text="Name:")
        self.password_label = ttk.Label(self.window, text="Code:")
        self.update_label = ttk.Label(
            self.window, text="Double Click to update client name"
        )

        self.username_entry = ttk.Entry(self.window)
        self.password_entry = ttk.Entry(self.window, show="*")

        self.register_button = ttk.Button(
            self.window, text="Register", command=self.register
        )
        self.login_button = ttk.Button(
            self.window, text="Validate client", command=self.login
        )

        self.user_listbox = tk.Listbox(self.window)
        self.edit_button = ttk.Button(
            self.window, text="Edit client", command=self.edit_username
        )
        self.delete_button = ttk.Button(
            self.window, text="Delete client", command=self.delete_user
        )

        self.username_label.grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label.grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.register_button.grid(row=2, column=0, padx=10, pady=10)
        self.login_button.grid(row=2, column=1, padx=10, pady=10)
        self.update_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.user_listbox.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )
        self.edit_button.grid(row=5, column=0, padx=10, pady=10)
        self.delete_button.grid(row=5, column=1, padx=10, pady=10)

        
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(4, weight=1)

        self.conn = self.connect()
        self.create_tables()

        self.update_user_listbox()

        self.user_listbox.bind("<Double-Button-1>", self.edit_username)

    def delete_user(self):
        selected_username = self.user_listbox.get(
            self.user_listbox.curselection())

        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "DELETE FROM tkinter.users WHERE username = %s",
                    (selected_username,),
                )
                self.conn.commit()
                messagebox.showinfo(
                    "User Deletion", "User deleted successfully")

                self.update_user_listbox()

            except Error as e:
                print(e)
                messagebox.showerror("User Deletion", "User deletion failed")

            finally:
                cursor.close()

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="")
            if conn.is_connected():
                print("Connected to MySQL server")
                return conn

        except Error as e:
            print(e)

        return None

    def create_tables(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS tkinter")
            cursor.execute("USE tkinter")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, "
                "username VARCHAR(255) NOT NULL, client VARCHAR(255) NOT NULL)"
            )
            print("Table 'users' created successfully")

            conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tkinter.users (username, password) VALUES (%s, %s)",
                (username, password),
            )
            self.conn.commit()
            messagebox.showinfo("Registration", "Registered successfully")

            self.update_user_listbox()

        except Error as e:
            print(e)
            messagebox.showerror("Registration", "Registration failed")

        finally:
            cursor.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT * FROM tkinter.users WHERE username = %s AND password = %s",
                    (username, password),
                )
                result = cursor.fetchone()

                if result is not None:
                    messagebox.showinfo(
                        "Client Validation", "Client validation successful"
                    )
                else:
                    messagebox.showerror(
                        "Client Validation", "Invalid client info")

            except Error as e:
                print(e)
                messagebox.showerror("Client Validation", "Validation Failed")

            finally:
                cursor.close()

    def update_user_listbox(self):
        self.user_listbox.delete(0, tk.END)

        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT username FROM tkinter.users")
                results = cursor.fetchall()

                for result in results:
                    username = result[0]
                    self.user_listbox.insert(tk.END, username)

            except Error as e:
                print(e)

            finally:
                cursor.close()

    def edit_username(self, event=None):
        selected_username = self.user_listbox.get(
            self.user_listbox.curselection())

        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT * FROM tkinter.users WHERE username = %s",
                    (selected_username,),
                )
                result = cursor.fetchone()

                if result is not None:
                    edit_window = tk.Toplevel(self.window)
                    edit_window.title("Edit Username")

                    new_username_label = tk.Label(
                        edit_window, text="New Username:")
                    new_username_entry = tk.Entry(edit_window)
                    new_username_entry.insert(
                        tk.END, result[1])  
                    password_label = tk.Label(edit_window, text="Password:")
                    password_entry = tk.Entry(edit_window, show="*")
                    password_entry.insert(tk.END, result[2])  
                    save_button = tk.Button(
                        edit_window,
                        text="Save",
                        command=lambda: self.save_username(
                            edit_window,
                            selected_username,
                            new_username_entry.get(),
                            password_entry.get(),
                        ),
                    )

                    new_username_label.grid(row=0, column=0, padx=10, pady=10)
                    new_username_entry.grid(row=0, column=1, padx=10, pady=10)
                    password_label.grid(row=1, column=0, padx=10, pady=10)
                    password_entry.grid(row=1, column=1, padx=10, pady=10)
                    save_button.grid(
                        row=2, column=0, columnspan=2, padx=10, pady=10)

                else:
                    messagebox.showerror("Username Update", "Invalid username")

            except Error as e:
                print(e)
                messagebox.showerror(
                    "Username Update", "Failed to fetch user data")

            finally:
                cursor.close()

    def save_username(self, edit_window, old_username, new_username, password):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT * FROM tkinter.users WHERE username = %s AND password = %s",
                    (old_username, password),
                )
                result = cursor.fetchone()

                if result is not None:
                    cursor.execute(
                        "UPDATE tkinter.users SET username = %s WHERE username = %s",
                        (new_username, old_username),
                    )
                    self.conn.commit()
                    messagebox.showinfo(
                        "Username Update", "Username updated successfully"
                    )

                    self.update_user_listbox()

                    edit_window.destroy()

                else:
                    messagebox.showerror("Username Update", "Invalid password")

            except Error as e:
                print(e)
                messagebox.showerror(
                    "Username Update", "Username update failed")

            finally:
                cursor.close()

    def run(self):
        self.create_tables()
        self.window.mainloop()


def main():
    login_form = LoginForm()
    login_form.run()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import pickle
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the Event class to store event details and manage tickets
class Event:
    def __init__(self, eventID, eventName, eventDate, location, totalCapacity, soldTickets=0):
        self.setEventID(eventID)
        self.setEventName(eventName)
        self.setEventDate(eventDate)
        self.setLocation(location)
        self.setTotalCapacity(totalCapacity)
        self.setSoldTickets(soldTickets)

    def setEventID(self, eventID):
        self.__eventID = eventID

    def getEventID(self):
        return self.__eventID

    def setEventName(self, eventName):
        self.__eventName = eventName

    def getEventName(self):
        return self.__eventName

    def setEventDate(self, eventDate):
        self.__eventDate = eventDate

    def getEventDate(self):
        return self.__eventDate

    def setLocation(self, location):
        self.__location = location

    def getLocation(self):
        return self.__location

    def setTotalCapacity(self, totalCapacity):
        self.__totalCapacity = totalCapacity

    def getTotalCapacity(self):
        return self.__totalCapacity

    def setSoldTickets(self, soldTickets):
        self.__soldTickets = soldTickets

    def getSoldTickets(self):
        return self.__soldTickets

    def getAvailableTickets(self):
        return self.getTotalCapacity() - self.getSoldTickets()

    def updateSoldTickets(self, count):
        if self.getSoldTickets() + count <= self.getTotalCapacity():
            self.setSoldTickets(self.getSoldTickets() + count)
        else:
            print("Not enough tickets available.")
        return self.getSoldTickets()

    def getEventDetails(self):
        return {
            "Event ID": self.getEventID(),
            "Event Name": self.getEventName(),
            "Event Date": self.getEventDate().strftime('%Y-%m-%d'),
            "Location": self.getLocation(),
            "Total Capacity": self.getTotalCapacity(),
            "Sold Tickets": self.getSoldTickets(),
            "Available Tickets": self.getAvailableTickets()
        }

class GrandPrixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grand Prix Ticket Booking System")
        self.geometry("900x600")
        self.resizable(False, False)

        self.events = self.load_events()
        self.current_user = None

        self.discounts = {
            "Single Race": 0,
            "Weekend Pass": 0,
            "Group Pack (5)": 0
        }

        self.tabs = ttk.Notebook(self)

        self.customer_frame = ttk.Frame(self.tabs)
        self.purchase_frame = ttk.Frame(self.tabs)
        self.admin_frame = ttk.Frame(self.tabs)

        self.tabs.add(self.customer_frame, text='Customer Portal')
        self.tabs.add(self.purchase_frame, text='Buy Tickets')
        self.tabs.add(self.admin_frame, text='Admin Dashboard')
        self.tabs.pack(expand=1, fill='both')

        self.init_customer_portal()
        self.init_ticket_interface()
        self.init_admin_dashboard()

    def init_customer_portal(self):
        tk.Label(self.customer_frame, text="Customer Management", font=('Arial', 16)).pack(pady=10)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(self.customer_frame, text="Name:").pack()
        tk.Entry(self.customer_frame, textvariable=self.name_var).pack()

        tk.Label(self.customer_frame, text="Email:").pack()
        tk.Entry(self.customer_frame, textvariable=self.email_var).pack()

        tk.Button(self.customer_frame, text="Create Account", command=self.create_account).pack(pady=5)
        tk.Button(self.customer_frame, text="Display Account", command=self.display_account).pack(pady=5)

    def create_account(self):
        name = self.name_var.get()
        email = self.email_var.get()
        if name and email:
            self.current_user = {"name": name, "email": email}
            messagebox.showinfo("Success", f"Account created for {name}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def display_account(self):
        if self.current_user:
            user = self.current_user
            messagebox.showinfo("Account Info", f"Name: {user['name']}\nEmail: {user['email']}")
        else:
            messagebox.showwarning("No Account", "No user account found.")

    def init_ticket_interface(self):
        tk.Label(self.purchase_frame, text="Buy Tickets", font=('Arial', 16)).pack(pady=10)

        self.ticket_type = tk.StringVar()
        self.ticket_type.set("Single Race")

        self.ticket_menu = ttk.Combobox(
            self.purchase_frame,
            textvariable=self.ticket_type,
            values=[
                "Single Race - $ 100",
                "Weekend Pass - $ 250",
                "Group Pack (5) - $ 1400"
            ],
            state="readonly"
        )
        self.ticket_menu.pack(pady=10)

        tk.Button(self.purchase_frame, text="Purchase Ticket", command=self.purchase_ticket).pack(pady=10)

    def purchase_ticket(self):
        if not self.current_user:
            messagebox.showwarning("Login Required", "Please create an account first.")
            return

        selected = self.ticket_type.get().split(" - ")[0]
        prices = {
            "Single Race": 100,
            "Weekend Pass": 250,
            "Group Pack (5)": 400
        }

        price = prices[selected]
        discount = self.discounts.get(selected, 0)
        discounted_price = price * (1 - discount / 100)

        if self.events:
            self.events[0].updateSoldTickets(1)
            self.save_events(self.events)
            messagebox.showinfo("Purchase Successful", f"{self.current_user['name']} bought: {selected} for AED {discounted_price:.2f}")
            self.refresh_admin_chart()
        else:
            messagebox.showerror("Error", "No event data found.")

    def init_admin_dashboard(self):
        tk.Label(self.admin_frame, text="Admin Dashboard", font=('Arial', 16)).pack(pady=10)

        tk.Button(self.admin_frame, text="View Ticket Sales", command=self.show_sales_data).pack(pady=5)
        tk.Button(self.admin_frame, text="Modify Discounts", command=self.modify_discounts).pack(pady=5)

        self.chart_frame = tk.Frame(self.admin_frame)
        self.chart_frame.pack(pady=10, fill="both", expand=True)

        self.refresh_admin_chart()

    def refresh_admin_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if self.events:
            event = self.events[0]
            sold = event.getSoldTickets()
            available = event.getAvailableTickets()

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.pie([sold, available], labels=["Sold", "Available"], autopct='%1.1f%%', startangle=140)
            ax.set_title("Ticket Sales Percentage")

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_sales_data(self):
        if self.events:
            e = self.events[0]
            info = e.getEventDetails()
            summary = "\n".join([f"{k}: {v}" for k, v in info.items()])
            messagebox.showinfo("Ticket Sales Summary", summary)
        else:
            messagebox.showerror("No Data", "No events available.")

    def modify_discounts(self):
        discount_window = tk.Toplevel(self)
        discount_window.title("Modify Discounts")
        discount_window.geometry("300x200")

        tk.Label(discount_window, text="Set Discounts (%)", font=("Arial", 14)).pack(pady=10)

        entries = {}
        for ticket in self.discounts:
            frame = tk.Frame(discount_window)
            frame.pack(pady=5)
            tk.Label(frame, text=ticket).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=5)
            entry.insert(0, str(self.discounts[ticket]))
            entry.pack(side=tk.LEFT)
            entries[ticket] = entry

        def save():
            for ticket, entry in entries.items():
                try:
                    self.discounts[ticket] = float(entry.get())
                except ValueError:
                    self.discounts[ticket] = 0
            messagebox.showinfo("Saved", "Discounts updated successfully.")
            discount_window.destroy()

        tk.Button(discount_window, text="Save", command=save).pack(pady=10)

    def save_events(self, events, filename='events.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(events, file)

    def load_events(self, filename='events.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        else:
            default_event = Event(
                eventID=301,
                eventName="Formula One Racing",
                eventDate=date(2025, 11, 15),
                location="Yas Marina",
                totalCapacity=5000,
                soldTickets=0
            )
            self.save_events([default_event], filename)
            return [default_event]

if __name__ == "__main__":
    app = GrandPrixApp()
    app.mainloop()

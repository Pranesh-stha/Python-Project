import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import calendar
import os

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Calendar App")
        self.root.geometry("500x800")
        self.root.configure(bg="#121212")

        # Predefined events dictionary (month: {day: event})
        self.predefined_events = {
            1: {
               1: "New Year's Day",
               24: "International Day of Education"
            },
            2: {
                4: "World Cancer Day",
               13: "World Radio Day",
               20: "World Day of Social Justice"
            },
            3: {
                8: "International Women's Day",
                20: "International Day of Happiness",
                21: "International Day for the Elimination of Racial Discrimination",
                22: "World Water Day"
            },
            4: {
                7: "World Health Day",
                22: "Earth Day"
            },
            5: {
                1: "Labor Day",
                3: "World Press Freedom Day",
                15: "International Day of Families"
            },
            6: {
                5: "World Environment Day",
                12: "World Day Against Child Labour",
                20: "World Refugee Day"
            },
            7: {
                11: "World Population Day"
            },
            8: {
                12: "International Youth Day",
                19: "World Humanitarian Day"
            },
            9: {
                8: "International Literacy Day",
                21: "International Day of Peace"
            },
            10: {
                1: "International Day of Older Persons",
                2: "International Day of Non-Violence",
                10: "World Mental Health Day",
                16: "World Food Day"
            },
            11: {
                14: "World Diabetes Day",
                16: "International Day for Tolerance",
                20: "Universal Children's Day"
            },
            12: {
                1: "World AIDS Day",
                3: "International Day of Persons with Disabilities",
                10: "Human Rights Day"
            }
        }

        # User-defined events dictionary (month: {day: event})
        self.user_events = {}
        self.load_user_events()  # Load user events from file

        # Current date
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.selected_date = None

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#121212")
        self.header_frame.pack(pady=10)
        self.prev_button = tk.Button(self.header_frame, text="❮", font=("Helvetica Neue", 14), command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.month_label = tk.Label(self.header_frame, text=self.get_month_name(), font=("Helvetica Neue", 16, "bold"), fg="white", bg="#121212")
        self.month_label.pack(side=tk.LEFT, padx=10)
        self.year_label = tk.Label(self.header_frame, text=str(self.current_year), font=("Helvetica Neue", 16, "bold"), fg="white", bg="#121212")
        self.year_label.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(self.header_frame, text="❯", font=("Helvetica Neue", 14), command=self.next_month)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Weekday Headers
        self.weekdays = ["SUN", "MON", "TUE", "WED", "THUR", "FRI", "SAT"]
        self.weekday_frame = tk.Frame(self.root, bg="#121212")
        self.weekday_frame.pack()
        for day in self.weekdays:
            label = tk.Label(self.weekday_frame, text=day, font=("Helvetica Neue", 12, "bold"), fg="white", bg="#121212", width=5, relief=tk.RIDGE)
            label.pack(side=tk.LEFT, padx=2, pady=2)

        # Calendar Grid
        self.calendar_frame = tk.Frame(self.root, bg="#121212")
        self.calendar_frame.pack(pady=10)
        self.create_calendar_grid()

        # Event Details Section
        self.event_details_frame = tk.Frame(self.root, bg="#121212")
        self.event_details_frame.pack(pady=10)
        self.date_label = tk.Label(self.event_details_frame, text="", font=("Helvetica Neue", 24, "bold"), fg="white", bg="#121212")
        self.date_label.pack(pady=5)
        self.day_label = tk.Label(self.event_details_frame, text="", font=("Helvetica Neue", 12), fg="white", bg="#121212")
        self.day_label.pack(pady=5)
        self.event_label = tk.Label(self.event_details_frame, text="", font=("Helvetica Neue", 14), fg="white", bg="#121212")
        self.event_label.pack(pady=5)

        # Buttons
        self.add_event_button = tk.Button(self.root, text="+ Add Event", font=("Helvetica Neue", 12), command=self.add_event_window, bg="#28a745", fg="white")
        self.add_event_button.pack(pady=5)

        self.delete_event_button = tk.Button(self.root, text="🗑 Delete Selected Event", font=("Helvetica Neue", 12), command=self.delete_selected_event, bg="#dc3545", fg="white")
        self.delete_event_button.pack(pady=5)

    def load_user_events(self):
        """Loads user events from 'events.txt' into self.user_events."""
        if not os.path.exists("events.txt"):
            open("events.txt", "w").close()
        with open("events.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    month_str, day_str, event = line.split(",", 2)
                    month = int(month_str.strip())
                    day = int(day_str.strip())
                    if month not in self.user_events:
                        self.user_events[month] = {}
                    self.user_events[month][day] = event.strip()
                except ValueError:
                    continue

    def save_event_to_file(self, month, day, event):
        """Appends a new event to 'events.txt'."""
        with open("events.txt", "a") as f:
            f.write(f"{month}, {day}, {event}\n")

    def update_events_file(self):
        ##"""Rewrites the entire 'events.txt' file from self.user_events."""
        with open("events.txt", "w") as f:
            for month in self.user_events:
                for day in self.user_events[month]:
                    f.write(f"{month}, {day}, {self.user_events[month][day]}\n")

    def get_month_name(self):
        return calendar.month_name[self.current_month]

    def create_calendar_grid(self):
        # Clear existing grid
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        num_days = calendar.monthrange(self.current_year, self.current_month)[1]
        ## first_day = datetime(self.current_year, self.current_month, 1).weekday()  # Monday=0
        # Adjust Sunday logic
        first_day_sunday_aware = datetime(self.current_year, self.current_month, 1).toordinal() % 7  # SUN=0
        for i in range(6):  # Max 6 rows
            for j in range(7):  # 7 columns
                day = (i * 7 + j - first_day_sunday_aware) + 1
                if 1 <= day <= num_days:
                    button = tk.Button(
                        self.calendar_frame,
                        text=str(day),
                        font=("Helvetica Neue", 12),
                        width=5,
                        height=2,
                        bg="#2c3e50",
                        fg="white",
                        relief=tk.RIDGE,
                        borderwidth=2
                    )
                    button.grid(row=i, column=j, padx=2, pady=2)
                    button.bind("<Button-1>", lambda e, d=day: self.select_date(d))
                    if day == datetime.now().day and self.current_month == datetime.now().month:
                        button.config(bg="#28a745")  # Highlight today
                else:
                    tk.Button(self.calendar_frame, text="", state=tk.DISABLED, bg="#121212", fg="#121212").grid(
                        row=i, column=j, padx=2, pady=2
                    )

    def select_date(self, day):
        self.selected_date = day
        self.update_event_details()

    def update_event_details(self):
        if self.selected_date is None:
            return
        selected_full_date = datetime(self.current_year, self.current_month, self.selected_date)
        day_of_week = selected_full_date.strftime("%A")
        self.date_label.config(text=f"{self.selected_date}")
        self.day_label.config(text=f"{selected_full_date.strftime('%B %d, %Y')}\n{day_of_week}")
        events = self.get_events_for_date(self.current_month, self.selected_date)
        if events:
            self.event_label.config(text="\n".join(events))
        else:
            self.event_label.config(text="No events for this date.")

    def get_events_for_date(self, month, day):
        events = []
        if month in self.predefined_events and day in self.predefined_events.get(month, {}):
            events.append(self.predefined_events[month][day])
        if month in self.user_events and day in self.user_events.get(month, {}):
            events.append(self.user_events[month][day])
        return events

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

    def update_calendar(self):
        self.month_label.config(text=self.get_month_name())
        self.year_label.config(text=str(self.current_year))
        self.create_calendar_grid()
        self.update_event_details()

    def add_event_window(self):
        add_event_window = tk.Toplevel(self.root)
        add_event_window.title("Add Event")
        add_event_window.geometry("400x280")
        add_event_window.configure(bg="#121212")

        tk.Label(add_event_window, text="Enter Month (1-12):", font=("Helvetica Neue", 12), fg="white", bg="#121212").pack(pady=5)
        month_entry = tk.Entry(add_event_window, font=("Helvetica Neue", 12))
        month_entry.pack(pady=5)

        tk.Label(add_event_window, text="Enter Day:", font=("Helvetica Neue", 12), fg="white", bg="#121212").pack(pady=5)
        day_entry = tk.Entry(add_event_window, font=("Helvetica Neue", 12))
        day_entry.pack(pady=5)

        tk.Label(add_event_window, text="Enter Event Description:", font=("Helvetica Neue", 12), fg="white", bg="#121212").pack(pady=5)
        event_entry = tk.Entry(add_event_window, font=("Helvetica Neue", 12))
        event_entry.pack(pady=5)

        def save_event():
            try:
                month = int(month_entry.get())
                day = int(day_entry.get())
                event = event_entry.get().strip()
                if not (1 <= month <= 12):
                    messagebox.showerror("Invalid Input", "Month must be between 1 and 12.")
                    return
                if not event:
                    messagebox.showerror("Invalid Input", "Event description cannot be empty.")
                    return
                if month not in self.user_events:
                    self.user_events[month] = {}
                self.user_events[month][day] = event
                self.save_event_to_file(month, day, event)
                messagebox.showinfo("Success", "Event added successfully!")
                add_event_window.destroy()
                self.update_calendar()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integers for month and day.")

        tk.Button(add_event_window, text="Save Event", font=("Helvetica Neue", 12), command=save_event, bg="#28a745", fg="white").pack(pady=10)

    def delete_selected_event(self):
        if self.selected_date is None:
            messagebox.showwarning("No Date Selected", "Please select a date first.")
            return
        if self.current_month not in self.user_events or self.selected_date not in self.user_events[self.current_month]:
            messagebox.showinfo("No Event", "There is no user-defined event for the selected date.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this event?")
        if confirm:
            del self.user_events[self.current_month][self.selected_date]
            if not self.user_events[self.current_month]:  # Remove month if empty
                del self.user_events[self.current_month]
            self.update_events_file()
            messagebox.showinfo("Deleted", "Event deleted successfully!")
            self.update_calendar()

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
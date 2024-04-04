from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import Tk, Label, Button
from tkcalendar import DateEntry
import datetime
#import tkinter as tk
#from PIL import Image, ImageTk
import subprocess
from pdf2image import convert_from_path
from PIL import Image, ImageTk



#Create global Window
root = Tk()
root.title('This is a test')
root.geometry("600x600")




#create pages directory
home_frame = Frame(root)
page_one_frame = Frame(root)
page_client_details_frame = Frame(root)
page_two_frame = Frame(root)
page_two_a_frame = Frame(root)
page_three_frame = Frame(root)
page_three_a_frame = Frame(root)
page_three_b_frame = Frame(root)
page_three_c_frame = Frame(root)
# Create a frame to hold the Treeview widgets
client_display_frame = Frame(page_client_details_frame)
venue_list_frame = Frame(page_two_frame)
future_bookings_frame = Frame(page_three_b_frame)


# Include only the frames that have been defined
pages = [home_frame, page_one_frame, page_client_details_frame, page_two_frame, page_two_a_frame, page_three_frame, page_three_a_frame,page_three_b_frame, page_three_c_frame] 


# Create Treeview widgets
client_treeview = ttk.Treeview(client_display_frame, columns=("client_id", "client_name", "client_company"), show="headings")
client_treeview.heading("client_id", text="ID")
client_treeview.heading("client_name", text="Name")
client_treeview.heading("client_company", text="Company")
client_treeview.column("client_id", width=20)
client_treeview.column("client_name", width=120)
client_treeview.column("client_company", width=150)
client_treeview.pack()

venue_treeview = ttk.Treeview(venue_list_frame, columns=("venue_id", "Attr1", "Attr2", "Attr3", "AttrNo"), show="headings")
venue_treeview.heading("venue_id", text="ID")
venue_treeview.heading("Attr1", text="Venue Name")
venue_treeview.heading("Attr2", text="Address")
venue_treeview.heading("Attr3", text="Suburb")
venue_treeview.heading("AttrNo", text="Rate($)")
venue_treeview.column("venue_id", width=20)  # Adjust the width of column "Attr1" to 100 pixels
venue_treeview.column("Attr1", width=80)  # Adjust the width of column "Attr1" to 100 pixels
venue_treeview.column("Attr2", width=80)  # Adjust the width of column "Attr2" to 100 pixels
venue_treeview.column("Attr3", width=80)  # Adjust the width of column "Attr3" to 100 pixels
venue_treeview.column("AttrNo", width=80) # Adjust the width of column "AttrNo" to 100 pixels
venue_treeview.pack()

bookings_treeview = ttk.Treeview(future_bookings_frame, columns=("Booking Date", "Venue Name", "Suburb", "Start Time"), show="headings")
bookings_treeview.heading("Booking Date", text="Booking Date")
bookings_treeview.heading("Venue Name", text="Venue Name")
bookings_treeview.heading("Suburb", text="Suburb")
bookings_treeview.heading("Start Time", text="Start Time")
bookings_treeview.column("Booking Date", width=100)
bookings_treeview.column("Venue Name", width=140)
bookings_treeview.column("Suburb", width=80)
bookings_treeview.column("Start Time", width=80)
bookings_treeview.pack(fill="both", expand=True)


# Create/connect to DB
conn = sqlite3.connect('Gig_Bookings.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")


# Create TABLES
c.execute("""CREATE TABLE IF NOT EXISTS performer (
          perf_id integer PRIMARY KEY AUTOINCREMENT,
          perf_f_name text,
          perf_l_name text,
          perf_phn text,
          perf_email text,
          perf_st_address text,
          perf_suburb text,
          perf_state text,
          perf_post_code integer,
          perf_abn integer,
          perf_bank_name text,
          perf_acc_name text,
          perf_bsb integer,
          perf_acc_no integer
)""")

c.execute("""CREATE TABLE IF NOT EXISTS client (
          client_id integer PRIMARY KEY AUTOINCREMENT,
          client_name text,
          client_company text
)""")

c.execute("""CREATE TABLE IF NOT EXISTS venue (
          venue_id integer PRIMARY KEY AUTOINCREMENT,
          venue_name text,
          venue_st_address text,
          venue_suburb text,
          venue_rate integer
)""")

c.execute("""CREATE TABLE IF NOT EXISTS booking (
          booking_id integer PRIMARY KEY AUTOINCREMENT,
          booking_date DATE,
          venue_id INTEGER,
          perf_id INTEGER,
          client_id INTEGER,
          booking_sta_time text,
          booking_fin_time text,
          FOREIGN KEY (venue_id) REFERENCES venue (venue_id),
          FOREIGN KEY (perf_id) REFERENCES performer (perf_id),
          FOREIGN KEY (client_id) REFERENCES client (client_id)

)""")

c.execute("""CREATE TABLE IF NOT EXISTS invoice (
          invoice_id integer PRIMARY KEY AUTOINCREMENT,
          booking_id INTEGER,
          FOREIGN KEY (booking_id) REFERENCES booking (booking_id)

)""")



#DEFINE FUNCTIONS REQUIRED FOR PROGRAM


def show_page(target_frame):
    for page in pages:
        if page == target_frame:
            page.pack()  # Show the target frame
        else:
            page.pack_forget()  # Hide all other frames

def wipe_database():
    c.execute("PRAGMA foreign_keys=off;")
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table in tables:
        c.execute(f"DELETE FROM {table[0]};")
    c.execute("PRAGMA foreign_keys=on;")
    conn.commit()
    



#Page 1 Functions
def update_perf_f_name():
    global perf_f_name_entry
    perf_f_name_value = perf_f_name_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_f_name) VALUES (?)", (perf_f_name_value,))
    else:   
        c.execute("UPDATE performer SET perf_f_name = ? WHERE perf_id = 1", (perf_f_name_value,))
    conn.commit()
    perf_f_name_entry.delete(0, END)
    perf_f_name_curr.config(text=get_perf_f_name_value())

def update_perf_l_name():
    global perf_l_name_entry
    perf_l_name_value = perf_l_name_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_l_name) VALUES (?)", (perf_l_name_value,))
    else:   
        c.execute("UPDATE performer SET perf_l_name = ? WHERE perf_id = 1", (perf_l_name_value,))
    conn.commit()
    perf_l_name_entry.delete(0, END)
    perf_l_name_curr.config(text=get_perf_l_name_value())

def update_perf_bank_name():
    global perf_bank_name_entry
    perf_bank_name_value = perf_bank_name_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_bank_name) VALUES (?)", (perf_bank_name_value,))
    else:   
        c.execute("UPDATE performer SET perf_bank_name = ? WHERE perf_id = 1", (perf_bank_name_value,))
    conn.commit()
    perf_bank_name_entry.delete(0, END)
    perf_bank_name_curr.config(text=get_perf_bank_name_value())

def update_perf_abn():
    global perf_abn_entry
    perf_abn_value = perf_abn_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_abn) VALUES (?)", (perf_abn_value,))
    else:   
        c.execute("UPDATE performer SET perf_abn = ? WHERE perf_id = 1", (perf_abn_value,))
    conn.commit()
    perf_abn_entry.delete(0, END)
    perf_abn_curr.config(text=get_perf_abn_value())

def update_perf_phn():
    global perf_phn_entry
    perf_phn_value = perf_phn_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_phn) VALUES (?)", (perf_phn_value,))
    else:   
        c.execute("UPDATE performer SET perf_phn = ? WHERE perf_id = 1", (perf_phn_value,))
    conn.commit()
    perf_phn_entry.delete(0, END)
    perf_phn_curr.config(text=get_perf_phn_value())

def update_perf_email():
    global perf_email_entry
    perf_email_value = perf_email_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_email) VALUES (?)", (perf_email_value,))
    else:   
        c.execute("UPDATE performer SET perf_email = ? WHERE perf_id = 1", (perf_email_value,))
    conn.commit()
    perf_email_entry.delete(0, END)
    perf_email_curr.config(text=get_perf_email_value())

def update_perf_st_address():
    global perf_st_address_entry
    perf_st_address_value = perf_st_address_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_st_address) VALUES (?)", (perf_st_address_value,))
    else:   
        c.execute("UPDATE performer SET perf_st_address = ? WHERE perf_id = 1", (perf_st_address_value,))
    conn.commit()
    perf_st_address_entry.delete(0, END)
    perf_st_address_curr.config(text=get_perf_st_address_value())

def update_perf_suburb():
    global perf_suburb_entry
    perf_suburb_value = perf_suburb_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_suburb) VALUES (?)", (perf_suburb_value,))
    else:   
        c.execute("UPDATE performer SET perf_suburb = ? WHERE perf_id = 1", (perf_suburb_value,))
    conn.commit()
    perf_suburb_entry.delete(0, END)
    perf_suburb_curr.config(text=get_perf_suburb_value())

def update_perf_state():
    global perf_state_entry
    perf_state_value = perf_state_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_state) VALUES (?)", (perf_state_value,))
    else:   
        c.execute("UPDATE performer SET perf_state = ? WHERE perf_id = 1", (perf_state_value,))
    conn.commit()
    perf_state_entry.delete(0, END)
    perf_state_curr.config(text=get_perf_state_value())

def update_perf_post_code():
    global perf_post_code_entry
    perf_post_code_value = perf_post_code_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_post_code) VALUES (?)", (perf_post_code_value,))
    else:   
        c.execute("UPDATE performer SET perf_post_code = ? WHERE perf_id = 1", (perf_post_code_value,))
    conn.commit()
    perf_post_code_entry.delete(0, END)
    perf_post_code_curr.config(text=get_perf_post_code_value())

def update_perf_acc_name():
    global perf_acc_name_entry
    perf_acc_name_value = perf_acc_name_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_acc_name) VALUES (?)", (perf_acc_name_value,))
    else:   
        c.execute("UPDATE performer SET perf_acc_name = ? WHERE perf_id = 1", (perf_acc_name_value,))
    conn.commit()
    perf_acc_name_entry.delete(0, END)
    perf_acc_name_curr.config(text=get_perf_acc_name_value())

def update_perf_bsb():
    global perf_bsb_entry
    perf_bsb_value = perf_bsb_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_bsb) VALUES (?)", (perf_bsb_value,))
    else:   
        c.execute("UPDATE performer SET perf_bsb = ? WHERE perf_id = 1", (perf_bsb_value,))
    conn.commit()
    perf_bsb_entry.delete(0, END)
    perf_bsb_curr.config(text=get_perf_bsb_value())

def update_perf_acc_no():
    global perf_acc_no_entry
    perf_acc_no_value = perf_acc_no_entry.get()
    c.execute("SELECT COUNT(*) FROM performer")
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute("INSERT INTO performer (perf_acc_no) VALUES (?)", (perf_acc_no_value,))
    else:   
        c.execute("UPDATE performer SET perf_acc_no = ? WHERE perf_id = 1", (perf_acc_no_value,))
    conn.commit()
    perf_acc_no_entry.delete(0, END)
    perf_acc_no_curr.config(text=get_perf_acc_no_value())

##########################################

def get_perf_f_name_value():
    c.execute("SELECT perf_f_name FROM performer")
    perf_f_name_data = c.fetchone()
    return perf_f_name_data[0] if perf_f_name_data else "No data"

def get_perf_l_name_value():
    c.execute("SELECT perf_l_name FROM performer")
    perf_l_name_data = c.fetchone()
    return perf_l_name_data[0] if perf_l_name_data else "No data"

def get_perf_bank_name_value():
    c.execute("SELECT perf_bank_name FROM performer")
    perf_bank_name_data = c.fetchone()
    return perf_bank_name_data[0] if perf_bank_name_data else "No data"

def get_perf_abn_value():
    c.execute("SELECT perf_abn FROM performer")
    perf_abn_data = c.fetchone()
    return perf_abn_data[0] if perf_abn_data else "No data"

def get_perf_phn_value():
    c.execute("SELECT perf_phn FROM performer")
    perf_phn_data = c.fetchone()
    return perf_phn_data[0] if perf_phn_data else "No data"

def get_perf_email_value():
    c.execute("SELECT perf_email FROM performer")
    perf_email_data = c.fetchone()
    return perf_email_data[0] if perf_email_data else "No data"

def get_perf_st_address_value():
    c.execute("SELECT perf_st_address FROM performer")
    perf_st_address_data = c.fetchone()
    return perf_st_address_data[0] if perf_st_address_data else "No data"

def get_perf_suburb_value():
    c.execute("SELECT perf_suburb FROM performer")
    perf_suburb_data = c.fetchone()
    return perf_suburb_data[0] if perf_suburb_data else "No data"

def get_perf_state_value():
    c.execute("SELECT perf_state FROM performer")
    perf_state_data = c.fetchone()
    return perf_state_data[0] if perf_state_data else "No data"

def get_perf_post_code_value():
    c.execute("SELECT perf_post_code FROM performer")
    perf_post_code_data = c.fetchone()
    return perf_post_code_data[0] if perf_post_code_data else "No data"

def get_perf_acc_name_value():
    c.execute("SELECT perf_acc_name FROM performer")
    perf_acc_name_data = c.fetchone()
    return perf_acc_name_data[0] if perf_acc_name_data else "No data"

def get_perf_bsb_value():
    c.execute("SELECT perf_bsb FROM performer")
    perf_bsb_data = c.fetchone()
    return perf_bsb_data[0] if perf_bsb_data else "No data"

def get_perf_acc_no_value():
    c.execute("SELECT perf_acc_no FROM performer")
    perf_acc_no_data = c.fetchone()
    return perf_acc_no_data[0] if perf_acc_no_data else "No data"


#Page 2 Function

# Define a function to update the display of venue table
def update_client_display(client_display_label):
    client_table_data = display_client()
    client_display_label.config(text=client_table_data)

def add_client():
    global client_name_entry, client_company_entry
    c.execute("INSERT INTO client (client_name, client_company) VALUES (?, ?)",
              (client_name_entry.get(),
               client_company_entry.get()))
    conn.commit()
    client_name_entry.delete(0, END)
    client_company_entry.delete(0, END)
    update_client_display(client_display_label)
    client_list_dropdown['values'] = get_client_options()
    select_client_dropdown['values'] = get_client_options()


def display_client():
    c.execute("SELECT * FROM client")
    client_table_data = c.fetchall()
    for row in client_treeview.get_children():
        client_treeview.delete(row)
    for row in client_table_data:
        client_treeview.insert("", "end", values=row)

def get_client_options():
    global client_data
    c.execute("SELECT client_id, client_name, client_company FROM client")
    client_data = c.fetchall()
    client_options = [f"{item[1]} {item[2]}" for item in client_data]
    return client_options

#def get_selected_client_id():
    selected_venue_name = booking_venue_dropdown.get()
    for data in venue_data:
        if data[1] == selected_venue_name:
            return data[0]
    return None  # Handle if venue_id is not found

def delete_client_entry():
    selected_client = get_selected_client_id()
    c.execute("DELETE FROM client WHERE client_id = ?", (selected_client,))
    conn.commit()
    client_list_dropdown['values'] = get_client_options()
    select_client_dropdown['values'] = get_client_options()
    #booking_venue_dropdown['values'] = get_venue_options()
    update_client_display(client_display_label)

#Page 2 Function

def update_venue_display(venue_label):
    table_data = display_venue()
    venue_label.config(text=table_data)

def add_venue():
    global attr2_1_entry, attr2_2_entry, attr2_3_entry, attr2_no_entry
    c.execute("INSERT INTO venue (venue_name, venue_st_address, venue_suburb, venue_rate) VALUES (:venue_name, :venue_st_address, :venue_suburb, :venue_rate)",
    {
        'venue_name': attr2_1_entry.get(),
        'venue_st_address': attr2_2_entry.get(),
        'venue_suburb': attr2_3_entry.get(),
        'venue_rate': attr2_no_entry.get()
    })
    conn.commit()
    attr2_1_entry.delete(0, END)
    attr2_2_entry.delete(0, END)
    attr2_3_entry.delete(0, END)
    attr2_no_entry.delete(0, END)
    attr2_1_dropdown['values'] = get_venue_options()
    booking_venue_dropdown['values'] = get_venue_options()
    update_venue_display(venue_label)


def display_venue():
    c.execute("SELECT * FROM venue")
    venue_table_data = c.fetchall()
    #return venue_table_data if venue_table_data else "No data"
    # Clear previous data
    for row in venue_treeview.get_children():
        venue_treeview.delete(row)
    # Insert new data
    for row in venue_table_data:
        venue_treeview.insert("", "end", values=row)

def get_venue_options():
    global venue_data
    c.execute("SELECT venue_id, venue_name FROM venue")
    venue_data = c.fetchall()
    venue_names = [item[1] for item in venue_data]
    return venue_names


def delete_venue_entry():
    selected_attr = attr2_1_dropdown.get()
    c.execute("DELETE FROM venue WHERE venue_name = ?", (selected_attr,))
    conn.commit()
    attr2_1_dropdown['values'] = get_venue_options()
    booking_venue_dropdown['values'] = get_venue_options()
    update_venue_display(venue_label)

### PAGE 3 FUNCTIONS:
def get_selected_venue_id():
    selected_venue_name = booking_venue_dropdown.get()
    for data in venue_data:
        if data[1] == selected_venue_name:
            return data[0]
    return None  # Handle if venue_id is not found

def get_selected_client_id():
    selected_client_data = select_client_dropdown.get() or client_list_dropdown.get()
    for item in client_data:
        if f"{item[1]} {item[2]}" == selected_client_data:
            return item[0]
    return None  # Handle if venue_id is not found

def get_booking_start_time():
    hour = int(booking_start_hour_spinbox.get())
    minute = int(booking_start_minute_spinbox.get())
    if booking_start_am_pm_spinbox.get() == "PM":
        hour += 12
    hour %= 24  # Ensure hour is within 24-hour format
    sta_time_str = f"{hour:02d}:{minute:02d}"
    return sta_time_str

def get_booking_end_time():
    hour = int(booking_fin_hour_spinbox.get())
    minute = int(booking_fin_minute_spinbox.get())
    if booking_fin_am_pm_spinbox.get() == "PM":
        hour += 12
    hour %= 24  # Ensure hour is within 24-hour format
    fin_time_str = f"{hour:02d}:{minute:02d}"
    return fin_time_str


def create_booking():
    global venue_data  # Access the global variable venue_data
    c.execute("INSERT INTO booking (booking_date, venue_id, booking_sta_time, booking_fin_time, perf_id, client_id) VALUES (?, ?, ?, ?, ?, ?)",
              (booking_date_entry.get(),
               get_selected_venue_id(),
               get_booking_start_time(),
               get_booking_end_time(),
               1,
               get_selected_client_id()))
    conn.commit()
    booking_date_entry.delete(0, END)
    booking_venue_dropdown.set('')
    display_future_bookings()
    create_invoice_dropdown['values'] = get_possible_invoices()




def display_future_bookings():
    # Clear previous data
    for row in bookings_treeview.get_children():
        bookings_treeview.delete(row)
    # Query the database for future bookings
    today = datetime.date.today()
    c.execute("SELECT booking_date, venue_name, venue_suburb, booking_sta_time FROM booking JOIN venue ON booking.venue_id = venue.venue_id WHERE booking_date >= DATE('now')")
    future_bookings = c.fetchall()
    # Insert new data into the table
    for booking in future_bookings:
        bookings_treeview.insert("", "end", values=booking)


### Invoice Functions:
        
def get_possible_invoices():
    global possible_invoice_data
    c.execute('''
    SELECT booking.booking_id, venue.venue_name, booking.booking_date
    FROM booking
    LEFT JOIN venue ON booking.venue_id = venue.venue_id
    LEFT JOIN invoice ON booking.booking_id = invoice.booking_id
    WHERE invoice.booking_id IS NULL
    ''')
    possible_invoice_data = c.fetchall()
    create_invoice_options = [f"{item[1]} {item[2]}" for item in possible_invoice_data]
    return create_invoice_options

def get_selected_booking_id():
    selected_booking_data = create_invoice_dropdown.get()
    for item in possible_invoice_data:
        if f"{item[1]} {item[2]}" == selected_booking_data:
            return item[0]
    return None  # Handle if venue_id is not found

def create_invoice():
    global possible_invoice_data
    selected_booking_id = get_selected_booking_id()
    c.execute("INSERT INTO invoice (booking_id) VALUES (?)", (selected_booking_id,))
    conn.commit()
    create_invoice_dropdown.set('')
    create_invoice_dropdown['values'] = get_possible_invoices()



def get_existing_invoices():
    global existing_invoice_data
    c.execute('''
    SELECT invoice.invoice_id, venue.venue_name, booking.booking_date
    FROM booking
    LEFT JOIN venue ON booking.venue_id = venue.venue_id
    LEFT JOIN invoice ON booking.booking_id = invoice.booking_id
    WHERE invoice.booking_id
    ''')
    existing_invoice_data = c.fetchall()
    create_existing_invoice_options = [f"{item[1]} {item[2]}" for item in existing_invoice_data]
    return create_existing_invoice_options

def get_selected_invoice_id():
    selected_invoice_data = display_invoice_dropdown.get()
    for item in existing_invoice_data:
        if f"{item[1]} {item[2]}" == selected_invoice_data:
            return item[0]
    return None
    

def get_invoice_details(invoice_id):
    c.execute('''
    SELECT invoice.invoice_id, performer.perf_f_name, performer.perf_l_name, client.client_name, client.client_company, performer.perf_phn, performer.perf_email, booking.booking_date, venue.venue_name, venue.venue_rate, performer.perf_st_address, performer.perf_suburb, performer.perf_state, performer.perf_post_code, performer.perf_abn, performer.perf_bank_name, performer.perf_acc_name, performer.perf_bsb, performer.perf_acc_no
    FROM invoice
    INNER JOIN booking ON invoice.booking_id = booking.booking_id
    INNER JOIN venue ON booking.venue_id = venue.venue_id
    INNER JOIN performer ON booking.perf_id = performer.perf_id
    INNER JOIN client ON booking.client_id = client.client_id

    WHERE invoice.invoice_id = ?
    ''', (invoice_id,))
    invoice_details = c.fetchone()
    invoice_id = invoice_details[0]
    perf_name = invoice_details[1] + " " + invoice_details[2]
    client_name = invoice_details[3]
    client_company = invoice_details[4]
    perf_phn = invoice_details[5]
    perf_email = invoice_details[6]
    booking_date = invoice_details[7]
    venue_name = invoice_details[8]
    venue_rate = invoice_details[9]
    perf_st_address = invoice_details[10]
    perf_suburb = invoice_details[11]
    perf_state = invoice_details[12]
    perf_post_code = invoice_details[13]
    perf_abn = invoice_details[14]
    perf_bank_name = invoice_details[15]
    perf_acc_name = invoice_details[16]
    perf_bsb = invoice_details[17]
    perf_acc_no = invoice_details[18]
    return invoice_id, perf_name, client_name, client_company, perf_phn, perf_email, booking_date, venue_name, venue_rate, perf_st_address, perf_suburb, perf_state, perf_post_code, perf_abn, perf_bank_name, perf_acc_name, perf_bsb, perf_acc_no


def update_invoice():
    invoice_id = get_selected_invoice_id()
    invoice_details = get_invoice_details(invoice_id)
    lines = open("invoice_template.tex").readlines()
    lines[91] = (invoice_details[1]) #perf Name
    lines[26] = (invoice_details[2]) #CLient Name
    lines[29] = (invoice_details[3]) # Client Company
    lines[32] = str(invoice_details[4]) #phn
    lines[36] = (invoice_details[5]).split('@')[0] # Email handle i.e. mathewjonathmusic
    lines[40] = "@" + (invoice_details[5]).split('@')[1] # Email host i.e. @gmail.com
    lines[34] = datetime.date.today().strftime("%A, %d %B, %Y")
    lines[38] = datetime.datetime.strptime(invoice_details[6], '%Y-%m-%d').strftime('%Y %m%d')# BOOKING DATE -> INV NUMBER = YYYY MMDD
    lines[54] = datetime.datetime.strptime(invoice_details[6], '%Y-%m-%d').strftime('%d %b %Y') # Booking date in itemized billing table DD/MM/YY
    lines[56] = str(invoice_details[7]) #venue Name
    lines[58] = "\$" + str(invoice_details[8]) #venue rate
    lines[67] = "\$" + str(invoice_details[8]) #invoice total
    lines[43] = str(invoice_details[9]) #Perf street
    lines[73] = str(invoice_details[10]) #perf Sub
    lines[75] = str(invoice_details[11]) #perf State
    lines[76] = str(invoice_details[12]) #Perf Postcode
    lines[81] = str(invoice_details[13]) #perf ABN
    lines[101] = str(invoice_details[14]) # bank Name
    lines[104] = str(invoice_details[15]) #acc name
    lines[107] = str(invoice_details[16]) #bsb
    lines[110] = str(invoice_details[17]) #acc
    open("new_invoice.tex", "w").writelines(lines)
   


def compile_tex_to_pdf():
    tex_file = 'new_invoice.tex'
    subprocess.run(['pdflatex', tex_file])

def convert_to_png():
    images = convert_from_path('new_invoice.pdf')
    for i, image in enumerate(images):
        image.save(f'Output_{i}.png', 'PNG')

def display_png():
    try:
        image_path = 'Output_0.png'
        img = Image.open(image_path)
        img = img.resize((500, 707), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        popup_window = Toplevel(root)
        popup_window.title("Display Image")

        label = Label(popup_window, image=img_tk)
        label.image = img_tk
        label.pack()

    except FileNotFoundError:
        print("Output image not found.")

def display_invoice():
    update_invoice()
    compile_tex_to_pdf()
    convert_to_png()
    display_png()

    




















###HOME PAGE LAYOUT
# Home Title
home_title = Label(home_frame, text="Home", font=('Helvetica', 18))
home_title.pack(pady=20)
# Button to navigate to Page One
goto_page_one_button = Button(home_frame, text="User Details", command=lambda: show_page(page_one_frame))
goto_page_one_button.pack(pady=10)
# Button to navigate to Page One
goto_page_client_details_button = Button(home_frame, text="Client Details", command=lambda: show_page(page_client_details_frame))
goto_page_client_details_button.pack(pady=10)
# Button to navigate to Page two
goto_page_two_button = Button(home_frame, text="Manage Venues", command=lambda: show_page(page_two_frame))
goto_page_two_button.pack(pady=10)
# Button to navigate to Page three
goto_page_three_button = Button(home_frame, text="Manage Bookings", command=lambda: show_page(page_three_frame))
goto_page_three_button.pack(pady=10)
wipe_button = Button(home_frame, text="Wipe Database", command= wipe_database)
wipe_button.pack(pady=10)
home_frame.pack(fill='both', expand=True)



# Page One LAYOUT
#heading
Page_one_heading = Label(page_one_frame, text="User Details")
Page_one_heading.grid(row=0, column=0, columnspan=5)
#row 1:
perf_f_name_label = Label(page_one_frame, text="First Name:")
perf_f_name_label.grid(row=1, column=0)
perf_f_name_curr = Label(page_one_frame, text=get_perf_f_name_value())
perf_f_name_curr.grid(row=1, column=2)
perf_f_name_entry = Entry(page_one_frame, width=30)
perf_f_name_entry.grid(row=1, column=3, padx=5)
update_perf_f_name_btn = Button(page_one_frame, text="Update", command=update_perf_f_name)
update_perf_f_name_btn.grid(row=1, column=4, padx=5, pady=2)
#row 2:
perf_l_name_label = Label(page_one_frame, text="Last Name:")
perf_l_name_label.grid(row=2, column=0)
perf_l_name_curr = Label(page_one_frame, text=get_perf_l_name_value())
perf_l_name_curr.grid(row=2, column=2)
perf_l_name_entry = Entry(page_one_frame, width=30)
perf_l_name_entry.grid(row=2, column=3, padx=5)
update_perf_l_name_btn = Button(page_one_frame, text="Update", command=update_perf_l_name)
update_perf_l_name_btn.grid(row=2, column=4, padx=5, pady=2)
#row 3: perf_phn4:
perf_phn_label = Label(page_one_frame, text="Phone:")
perf_phn_label.grid(row=3, column=0)
perf_phn_curr = Label(page_one_frame, text=get_perf_phn_value())
perf_phn_curr.grid(row=3, column=2)
perf_phn_entry = Entry(page_one_frame, width=30)
perf_phn_entry.grid(row=3, column=3, padx=5)
update_perf_phn_btn = Button(page_one_frame, text="Update", command=update_perf_phn)
update_perf_phn_btn.grid(row=3, column=4, padx=5, pady=2)
#row 4: perf_email:
perf_email_label = Label(page_one_frame, text="Email:")
perf_email_label.grid(row=4, column=0)
perf_email_curr = Label(page_one_frame, text=get_perf_email_value())
perf_email_curr.grid(row=4, column=2)
perf_email_entry = Entry(page_one_frame, width=30)
perf_email_entry.grid(row=4, column=3, padx=5)
update_perf_email_btn = Button(page_one_frame, text="Update", command=update_perf_email)
update_perf_email_btn.grid(row=4, column=4, padx=5, pady=2)
#row 5:perf_st_address:
perf_st_address_label = Label(page_one_frame, text="Street Address:")
perf_st_address_label.grid(row=5, column=0)
perf_st_address_curr = Label(page_one_frame, text=get_perf_st_address_value())
perf_st_address_curr.grid(row=5, column=2)
perf_st_address_entry = Entry(page_one_frame, width=30)
perf_st_address_entry.grid(row=5, column=3, padx=5)
update_perf_st_address_btn = Button(page_one_frame, text="Update", command=update_perf_st_address)
update_perf_st_address_btn.grid(row=5, column=4, padx=5, pady=2)
#row 6: perf_suburb:
perf_suburb_label = Label(page_one_frame, text="Suburb:")
perf_suburb_label.grid(row=6, column=0)
perf_suburb_curr = Label(page_one_frame, text=get_perf_suburb_value())
perf_suburb_curr.grid(row=6, column=2)
perf_suburb_entry = Entry(page_one_frame, width=30)
perf_suburb_entry.grid(row=6, column=3, padx=5)
update_perf_suburb_btn = Button(page_one_frame, text="Update", command=update_perf_suburb)
update_perf_suburb_btn.grid(row=6, column=4, padx=5, pady=2)
#row 7:perf_state:
perf_state_label = Label(page_one_frame, text="State:")
perf_state_label.grid(row=7, column=0)
perf_state_curr = Label(page_one_frame, text=get_perf_state_value())
perf_state_curr.grid(row=7, column=2)
perf_state_entry = Entry(page_one_frame, width=30)
perf_state_entry.grid(row=7, column=3, padx=5)
update_perf_state_btn = Button(page_one_frame, text="Update", command=update_perf_state)
update_perf_state_btn.grid(row=7, column=4, padx=5, pady=2)
#row 8:perf_post_code:
perf_post_code_label = Label(page_one_frame, text="Post Code:")
perf_post_code_label.grid(row=8, column=0)
perf_post_code_curr = Label(page_one_frame, text=get_perf_post_code_value())
perf_post_code_curr.grid(row=8, column=2)
perf_post_code_entry = Entry(page_one_frame, width=30)
perf_post_code_entry.grid(row=8, column=3, padx=5)
update_perf_post_code_btn = Button(page_one_frame, text="Update", command=update_perf_post_code)
update_perf_post_code_btn.grid(row=8, column=4, padx=5, pady=2)
#row 9: perf abn: :
perf_abn_label = Label(page_one_frame, text="ABN:")
perf_abn_label.grid(row=9, column=0)
perf_abn_curr = Label(page_one_frame, text=get_perf_abn_value())
perf_abn_curr.grid(row=9, column=2)
perf_abn_entry = Entry(page_one_frame, width=30)
perf_abn_entry.grid(row=9, column=3, padx=5)
update_perf_abn_btn = Button(page_one_frame, text="Update", command=update_perf_abn)
update_perf_abn_btn.grid(row=9, column=4, padx=5, pady=2)
#row 10: bank name:
perf_bank_name_label = Label(page_one_frame, text="Bank Name:")
perf_bank_name_label.grid(row=10, column=0)
perf_bank_name_curr = Label(page_one_frame, text=get_perf_bank_name_value())
perf_bank_name_curr.grid(row=10, column=2)
perf_bank_name_entry = Entry(page_one_frame, width=30)
perf_bank_name_entry.grid(row=10, column=3, padx=5)
update_perf_bank_name_btn = Button(page_one_frame, text="Update", command=update_perf_bank_name)
update_perf_bank_name_btn.grid(row=10, column=4, padx=5, pady=2)
#row 11 acc name:
perf_acc_name_label = Label(page_one_frame, text="Acc Name:")
perf_acc_name_label.grid(row=11, column=0)
perf_acc_name_curr = Label(page_one_frame, text=get_perf_acc_name_value())
perf_acc_name_curr.grid(row=11, column=2)
perf_acc_name_entry = Entry(page_one_frame, width=30)
perf_acc_name_entry.grid(row=11, column=3, padx=5)
update_perf_acc_name_btn = Button(page_one_frame, text="Update", command=update_perf_acc_name)
update_perf_acc_name_btn.grid(row=11, column=4, padx=5, pady=2)
#row 12 bsb:
perf_bsb_label = Label(page_one_frame, text="BSB:")
perf_bsb_label.grid(row=12, column=0)
perf_bsb_curr = Label(page_one_frame, text=get_perf_bsb_value())
perf_bsb_curr.grid(row=12, column=2)
perf_bsb_entry = Entry(page_one_frame, width=30)
perf_bsb_entry.grid(row=12, column=3, padx=5)
update_perf_bsb_btn = Button(page_one_frame, text="Update", command=update_perf_bsb)
update_perf_bsb_btn.grid(row=12, column=4, padx=5, pady=2)
#row 13:acc no :
perf_acc_no_label = Label(page_one_frame, text="Acc No:")
perf_acc_no_label.grid(row=13, column=0)
perf_acc_no_curr = Label(page_one_frame, text=get_perf_acc_no_value())
perf_acc_no_curr.grid(row=13, column=2)
perf_acc_no_entry = Entry(page_one_frame, width=30)
perf_acc_no_entry.grid(row=13, column=3, padx=5)
update_perf_acc_no_btn = Button(page_one_frame, text="Update", command=update_perf_acc_no)
update_perf_acc_no_btn.grid(row=13, column=4, padx=5, pady=2)
#BACK BUTTON
back_button = Button(page_one_frame, text="Back", command=lambda: show_page(home_frame))
back_button.grid(row=15, column=0, columnspan=5, pady=10)



#CLIENT PAGE LAYOUT
#heading
client_page_heading = Label(page_client_details_frame, text="Client Details")
client_page_heading.grid(row=0, column=0, columnspan=2)

#row 1:
client_name_label = Label(page_client_details_frame, text="Client Name")
client_name_label.grid(row=1, column=0)
client_name_entry = Entry(page_client_details_frame, width=30)
client_name_entry.grid(row=1, column=1)
#row 2:
client_company_label = Label(page_client_details_frame, text="Client Company")
client_company_label.grid(row=2, column=0)
client_company_entry = Entry(page_client_details_frame, width=30)
client_company_entry.grid(row=2, column=1)
#Submit BUTTON
submit_button = Button(page_client_details_frame, text="Add Client", command= add_client)
submit_button.grid(row=5, column=0, columnspan=2, pady=10)
#Table
client_display_frame.grid(row=7, column=0, columnspan=2, pady=20)
client_display_label = Label(page_two_frame, text="")
update_client_display(client_display_label)
#delete Client Label
del_client_label = Label(page_client_details_frame, text="Delete Client")
del_client_label.grid(row=9, column=0)
#create Dropdown widget
client_list_dropdown = ttk.Combobox(page_client_details_frame)
client_list_dropdown['values'] = get_client_options()
client_list_dropdown.grid(row=9, column=1, columnspan=2, pady=5)
#DELETE BUTTON
del_button = Button(page_client_details_frame, text="Delete", command= delete_client_entry)
del_button.grid(row=10, column=0, columnspan=2, pady=5)
#BACK BUTTON
back_button = Button(page_client_details_frame, text="Back", command=lambda: show_page(home_frame))
back_button.grid(row=12, column=0, columnspan=2, pady=10)


#PAGE 2 LAYOUT
#heading
page_two_heading = Label(page_two_frame, text="Manage Venues")
page_two_heading.grid(row=0, column=0, columnspan=2)

#row 1:
attr2_1_label = Label(page_two_frame, text="Venue Name")
attr2_1_label.grid(row=1, column=0)
attr2_1_entry = Entry(page_two_frame, width=30)
attr2_1_entry.grid(row=1, column=1)
#row 2:
attr2_2_label = Label(page_two_frame, text="Street Address")
attr2_2_label.grid(row=2, column=0)
attr2_2_entry = Entry(page_two_frame, width=30)
attr2_2_entry.grid(row=2, column=1)
#row 3:
attr2_3_label = Label(page_two_frame, text="Suburb")
attr2_3_label.grid(row=3, column=0)
attr2_3_entry = Entry(page_two_frame, width=30)
attr2_3_entry.grid(row=3, column=1)
#row 4:
attr2_no_label = Label(page_two_frame, text="Rate")
attr2_no_label.grid(row=4, column=0)
attr2_no_entry = Entry(page_two_frame, width=30)
attr2_no_entry.grid(row=4, column=1)
#Submit BUTTON
submit_button = Button(page_two_frame, text="Add Venue", command= add_venue)
submit_button.grid(row=5, column=0, columnspan=2, pady=10)

#Table
venue_list_frame.grid(row=7, column=0, columnspan=2, pady=20)

#display Table
venue_label = Label(page_two_frame, text="")
#venue_label.grid(row=7, column=0, columnspan=2)
update_venue_display(venue_label)
#delete Venue Label
del_venue_label = Label(page_two_frame, text="Delete Venue")
del_venue_label.grid(row=9, column=0)
#create Dropdown widget
attr2_1_dropdown = ttk.Combobox(page_two_frame)
attr2_1_dropdown['values'] = get_venue_options()
attr2_1_dropdown.grid(row=9, column=1, columnspan=2, pady=5)

#DELETE BUTTON
del_button = Button(page_two_frame, text="Delete", command= delete_venue_entry)
del_button.grid(row=10, column=0, columnspan=2, pady=5)


#BACK BUTTON
back_button = Button(page_two_frame, text="Back", command=lambda: show_page(home_frame))
back_button.grid(row=12, column=0, columnspan=2, pady=10)



#PAGE 3 LAYOUT
#heading
page_three_heading = Label(page_three_frame, text="Manage Bookings")
page_three_heading.grid(row=0, column=0, columnspan=5)

#NAV Button to add entries to table_3
page_3a_button = Button(page_three_frame, text="Add New Booking", command=lambda: show_page(page_three_a_frame))
page_3a_button.grid(row=1, column=0, columnspan=5)
#NAV Button to display entries to table_3
page_3b_button = Button(page_three_frame, text="View Upcoming", command=lambda: show_page(page_three_b_frame))
page_3b_button.grid(row=2, column=0, columnspan=5)
#NAV Button to create document from table_3
page_3c_button = Button(page_three_frame, text="Create Invoice", command=lambda: show_page(page_three_c_frame))
page_3c_button.grid(row=3, column=0, columnspan=5)

#BACK BUTTON
back_button = Button(page_three_frame, text="Back", command=lambda: show_page(home_frame))
back_button.grid(row=4, column=0, columnspan=5, pady=10)



#PAGE 3a LAYOUT
#heading
page_3a_heading = Label(page_three_a_frame, text="New Booking")
page_3a_heading.grid(row=0, column=0, columnspan=5)

#row 1:
booking_date_label = Label(page_three_a_frame, text="Booking Date")
booking_date_label.grid(row=1, column=0)
booking_date_entry = DateEntry(page_three_a_frame, date_pattern="yyyy-mm-dd")
booking_date_entry.grid(row=1, column=1, columnspan=6)
#row 2
booking_venue_label = Label(page_three_a_frame, text="Venue Name")
booking_venue_label.grid(row=2, column=0)
#create Dropdown widget (Replaces ENTRY)
booking_venue_dropdown = ttk.Combobox(page_three_a_frame)
booking_venue_dropdown['values'] = get_venue_options()
booking_venue_dropdown.grid(row=2, column=1, columnspan=6, pady=5)
#row 3:
booking_start_label = ttk.Label(page_three_a_frame, text="Start Time:")
booking_start_label.grid(row=3, column=0)
booking_start_hour_spinbox = ttk.Spinbox(page_three_a_frame, from_=1, to=12, width=5, wrap=True)
booking_start_hour_spinbox.grid(row=3, column=1)
booking_start_hour_spinbox.set(12)
booking_hh_mm_label = ttk.Label(page_three_a_frame, text=" : ")
booking_hh_mm_label.grid(row=3, column=2)
booking_start_minute_spinbox = ttk.Spinbox(page_three_a_frame, from_=0, to=59, width=5, wrap=True)
booking_start_minute_spinbox.grid(row=3, column=3)
booking_start_minute_spinbox.set(0)
booking_start_am_pm_spinbox = ttk.Spinbox(page_three_a_frame, values=("PM", "AM"), width=5, wrap=True)
booking_start_am_pm_spinbox.grid(row=3, column=4, padx=5)
booking_start_am_pm_spinbox.set("AM")
#row 4:
booking_fin_label = ttk.Label(page_three_a_frame, text="Finish Time:")
booking_fin_label.grid(row=4, column=0)
booking_fin_hour_spinbox = ttk.Spinbox(page_three_a_frame, from_=1, to=12, width=5, wrap=True)
booking_fin_hour_spinbox.grid(row=4, column=1)
booking_fin_hour_spinbox.set(12)
booking_hh_mm_label.grid(row=4, column=2)
booking_fin_minute_spinbox = ttk.Spinbox(page_three_a_frame, from_=0, to=59, width=5, wrap=True)
booking_fin_minute_spinbox.grid(row=4, column=3)
booking_fin_minute_spinbox.set(0)
booking_fin_am_pm_spinbox = ttk.Spinbox(page_three_a_frame, values=("PM", "AM"), width=5, wrap=True)
booking_fin_am_pm_spinbox.grid(row=4, column=4, padx=5)
booking_fin_am_pm_spinbox.set("AM")
#row 5:
select_client_label = ttk.Label(page_three_a_frame, text="Client")
select_client_label.grid(row=5, column=0)
select_client_dropdown = ttk.Combobox(page_three_a_frame)
select_client_dropdown['values'] = get_client_options()
select_client_dropdown.grid(row=5, column=1, columnspan=5, pady=5)
#Submit Button
create_booking_button = Button(page_three_a_frame, text="Submit", command=create_booking)
create_booking_button.grid(row=6, column=0, columnspan=5, pady=10)
#BACK BUTTON
back_button = Button(page_three_a_frame, text="Back", command=lambda: show_page(page_three_frame))
back_button.grid(row=7, column=0, columnspan=5, pady=10)


#PAGE 3b LAYOUT
#heading
page_3b_heading = Label(page_three_b_frame, text="Upcoming")
page_3b_heading.grid(row=0, column=0, columnspan=5)

future_bookings_frame.grid(row=2, column=0, columnspan=5, pady=10)

# Call the function to display future bookings
display_future_bookings()

#BACK BUTTON
back_button = Button(page_three_b_frame, text="Back", command=lambda: show_page(page_three_frame))
back_button.grid(row=4, column=0, columnspan=5, pady=10)


#PAGE 3c LAYOUT
#heading
page_3c_heading = Label(page_three_c_frame, text="Manage Invoices")
page_3c_heading.grid(row=0, column=0, columnspan=5)

select_booking_label = ttk.Label(page_three_c_frame, text="Select Booking for New Invoice:")
select_booking_label.grid(row=1, column=0)
create_invoice_dropdown = ttk.Combobox(page_three_c_frame)
create_invoice_dropdown['values'] = get_possible_invoices()
create_invoice_dropdown.grid(row=1, column=2, columnspan=4, pady=5)
create_invoice_button = Button(page_three_c_frame, text="Create Invoice", command=create_invoice)
create_invoice_button.grid(row=2, column=0, columnspan=5, pady=10)

select_invoice_label = ttk.Label(page_three_c_frame, text="Select Existing Invoice:")
select_invoice_label.grid(row=3, column=0)
display_invoice_dropdown = ttk.Combobox(page_three_c_frame)
display_invoice_dropdown['values'] = get_existing_invoices()
display_invoice_dropdown.grid(row=3, column=2, columnspan=4, pady=5)
display_invoice_button = Button(page_three_c_frame, text="Display Invoice", command=display_invoice)
display_invoice_button.grid(row=4, column=0, columnspan=5, pady=10)

#BACK BUTTON
back_button = Button(page_three_c_frame, text="Back", command=lambda: show_page(page_three_frame))
back_button.grid(row=5, column=0, columnspan=5, pady=10)






show_page(home_frame)  # Start with home screen visible

root.mainloop()

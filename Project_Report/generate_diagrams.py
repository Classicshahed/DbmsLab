import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = r"C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project\Project_Report\Project_Diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

# Common styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def save_fig(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Generated {filename}")

# 1. System Architecture Diagram
def make_architecture():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(6, 9.5, "Blood Bank Management System - 4-Tier System Architecture", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1a365d')

    layers = [
        ("Presentation Layer (Client Browser)", 7.8, 1.4, "#ebf8ff", "#3182ce", 
         ["Responsive UI (HTML5, CSS3, JavaScript)", "Jinja2 Dynamic Server-Side Rendering", "Client-Side UX & Dynamic Form Helpers"]),
        ("Application & Web Layer (Flask Web Framework)", 5.6, 1.8, "#f0fff4", "#38a169", 
         ["Route Controllers & HTTP Dispatcher (app.py)", "Session-Based CSRF Protection & Input Sanitization", 
          "Admin Authentication Guard & Sliding-Window Rate Limiting", "Transaction Flow & Business Rules Engine"]),
        ("Data Access & Connection Layer (db.py)", 3.4, 1.4, "#fffaf0", "#dd6b20", 
         ["mysql-connector-python Pure-Python Driver (Direct SQL, No ORM)", 
          "Thread-Local Dedicated Session Management", "Pre-Flight Ping (COM_PING) & Stale Socket Auto-Recovery", "Atomic Transaction Context Managers (db.transaction)"]),
        ("Database & Persistence Layer (MySQL 8.0 / MariaDB)", 1.2, 1.4, "#faf5ff", "#805ad5", 
         ["InnoDB ACID Storage Engine with Row-Level Locking (FOR UPDATE)", 
          "Relational Tables: Blood_Group, Donor, Donation, Hospital, Blood_Request, Blood_Stock", 
          "Referential Integrity: FK RESTRICT (Audit Preservation), UNIQUE & CHECK Constraints", "Admin Audit Trail (Admin_Audit_Log)"])
    ]

    for title, y, h, bg, border, items in layers:
        rect = patches.FancyBboxPatch((0.5, y), 11, h, boxstyle="round,pad=0.2", 
                                      facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(0.8, y + h - 0.3, title, fontsize=12, fontweight='bold', color=border)
        
        # Sub-items
        cols = len(items)
        col_w = 10.4 / cols
        for i, item in enumerate(items):
            box = patches.FancyBboxPatch((0.8 + i * col_w, y + 0.15), col_w - 0.2, h - 0.6,
                                         boxstyle="round,pad=0.1", facecolor="white", edgecolor="#cbd5e0", linewidth=1)
            ax.add_patch(box)
            ax.text(0.8 + i * col_w + (col_w - 0.2)/2, y + 0.15 + (h - 0.6)/2, item,
                    ha='center', va='center', fontsize=8.5, color='#2d3748', wrap=True)

    # Inter-layer arrows
    for y_arr in [7.7, 5.5, 3.3]:
        ax.annotate('', xy=(6, y_arr - 0.25), xytext=(6, y_arr + 0.05),
                    arrowprops=dict(arrowstyle="<->", color="#4a5568", lw=2))

    save_fig(fig, "system_architecture.png")

# 2. Use Case Diagram
def make_use_case():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(6.5, 9.6, "UML Use Case Diagram - Blood Bank Management System", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1a365d')

    # System boundary
    boundary = patches.FancyBboxPatch((3.2, 0.4), 6.6, 8.8, boxstyle="round,pad=0.1", 
                                      facecolor="#f7fafc", edgecolor="#4a5568", linewidth=2, linestyle='--')
    ax.add_patch(boundary)
    ax.text(6.5, 8.9, "Blood Bank System Boundary", ha='center', fontsize=12, fontweight='bold', color='#4a5568')

    # Actors
    def draw_actor(x, y, label):
        # Head
        ax.add_patch(patches.Circle((x, y), 0.25, facecolor="#e2e8f0", edgecolor="#2b6cb0", lw=2))
        # Body
        ax.plot([x, x], [y - 0.25, y - 0.9], color="#2b6cb0", lw=2)
        # Arms
        ax.plot([x - 0.4, x + 0.4], [y - 0.5, y - 0.5], color="#2b6cb0", lw=2)
        # Legs
        ax.plot([x, x - 0.3], [y - 0.9, y - 1.4], color="#2b6cb0", lw=2)
        ax.plot([x, x + 0.3], [y - 0.9, y - 1.4], color="#2b6cb0", lw=2)
        ax.text(x, y - 1.7, label, ha='center', fontsize=10, fontweight='bold', color='#1a365d')

    draw_actor(1.5, 5.5, "Donor / Hospital User\n(Public Operator)")
    draw_actor(11.5, 5.5, "System Administrator\n(Privileged Role)")

    use_cases = [
        (6.5, 8.1, "View Live Dashboard & Stock", ["public", "admin"]),
        (6.5, 7.2, "Register & Manage Donors", ["public"]),
        (6.5, 6.3, "Record Blood Donation (Units)", ["public"]),
        (6.5, 5.4, "Register Hospital & Raise Blood Request", ["public"]),
        (6.5, 4.5, "Atomic Request Fulfilment (Stock Deduction)", ["public"]),
        (6.5, 3.6, "View SQL Analytical Reports", ["public", "admin"]),
        (6.5, 2.7, "Secure Admin Login (Rate-Limited)", ["admin"]),
        (6.5, 1.8, "Approve / Reject Pending Requests", ["admin"]),
        (6.5, 0.9, "View Audit Trail & Manage Profile", ["admin"]),
    ]

    for x, y, title, roles in use_cases:
        ellipse = patches.Ellipse((x, y), 4.2, 0.65, facecolor="#ebf8ff", edgecolor="#3182ce", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, title, ha='center', va='center', fontsize=9, fontweight='medium', color='#2b6cb0')

        if "public" in roles:
            ax.plot([1.9, x - 2.1], [5.5, y], color="#4a5568", lw=1.2, linestyle='-')
        if "admin" in roles:
            ax.plot([11.1, x + 2.1], [5.5, y], color="#805ad5", lw=1.2, linestyle='-')

    save_fig(fig, "use_case_diagram.png")

# 3. DFD Level 0 (Context Diagram)
def make_dfd_0():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.5, "Data Flow Diagram (Level 0) - Context Diagram", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1a365d')

    # Central Process
    circ = patches.Circle((5.5, 4.0), 1.5, facecolor="#ebf8ff", edgecolor="#2b6cb0", lw=2.5)
    ax.add_patch(circ)
    ax.text(5.5, 4.2, "0.0", ha='center', va='center', fontsize=13, fontweight='bold', color="#2b6cb0")
    ax.text(5.5, 3.8, "Blood Bank\nManagement\nSystem", ha='center', va='center', fontsize=11, fontweight='bold', color="#1a202c")

    # Entities
    def draw_entity(x, y, text):
        rect = patches.Rectangle((x-1.2, y-0.6), 2.4, 1.2, facecolor="#edf2f7", edgecolor="#4a5568", lw=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold', color="#2d3748")

    draw_entity(1.6, 5.8, "Blood Donor")
    draw_entity(1.6, 2.2, "Hospital")
    draw_entity(9.4, 4.0, "Administrator")

    # Arrows
    def arrow(x1, y1, x2, y2, label, offset_y=0.15):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#2c5282", lw=1.5, shrinkA=5, shrinkB=5))
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        ax.text(mid_x, mid_y + offset_y, label, ha='center', va='center', fontsize=8.5, color='#1a365d', fontweight='medium',
                bbox=dict(boxstyle='square,pad=0.1', facecolor='white', edgecolor='none', alpha=0.8))

    arrow(2.8, 6.0, 4.3, 4.8, "Donor Details & Donations", 0.15)
    arrow(4.3, 4.6, 2.8, 5.6, "Donation History & Acknowledgement", -0.2)

    arrow(2.8, 2.4, 4.3, 3.4, "Blood Requests & Hospital Details", 0.15)
    arrow(4.3, 3.2, 2.8, 2.0, "Fulfillment Status & Availability", -0.2)

    arrow(8.2, 4.3, 7.0, 4.3, "Admin Credentials & Approvals", 0.2)
    arrow(7.0, 3.7, 8.2, 3.7, "Audit Log & Pending Proposals", -0.25)

    save_fig(fig, "dfd_level_0.png")

# 4. DFD Level 1
def make_dfd_1():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.6, "Data Flow Diagram (Level 1) - Detailed System Processes", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1a365d')

    processes = [
        (4.0, 7.8, "1.0", "Donor & Donation\nManagement"),
        (9.5, 7.8, "2.0", "Blood Inventory\n& Stock Control"),
        (4.0, 4.5, "3.0", "Hospital & Blood\nRequest Processing"),
        (9.5, 4.5, "4.0", "Admin Decision\n& Audit Control"),
        (6.8, 1.5, "5.0", "Reporting &\nSQL Analytics"),
    ]

    for x, y, num, title in processes:
        circ = patches.Circle((x, y), 0.9, facecolor="#ebf8ff", edgecolor="#3182ce", lw=2)
        ax.add_patch(circ)
        ax.text(x, y + 0.25, num, ha='center', va='center', fontsize=11, fontweight='bold', color="#2b6cb0")
        ax.text(x, y - 0.15, title, ha='center', va='center', fontsize=9, fontweight='medium', color="#1a202c")

    stores = [
        (1.2, 8.8, "D1", "Donor Table"),
        (6.8, 8.8, "D2", "Blood_Group Table"),
        (1.2, 6.8, "D3", "Donation Table"),
        (12.5, 7.8, "D4", "Blood_Stock Table"),
        (1.2, 3.5, "D5", "Hospital Table"),
        (6.8, 4.5, "D6", "Blood_Request Table"),
        (12.5, 4.5, "D7", "Admin_Audit_Log"),
    ]

    for x, y, code, name in stores:
        ax.plot([x - 0.9, x + 0.9], [y + 0.3, y + 0.3], color="#4a5568", lw=1.5)
        ax.plot([x - 0.9, x + 0.9], [y - 0.3, y - 0.3], color="#4a5568", lw=1.5)
        ax.plot([x - 0.9, x - 0.9], [y - 0.3, y + 0.3], color="#4a5568", lw=1.5)
        ax.text(x - 0.5, y, code, ha='center', va='center', fontsize=9, fontweight='bold', color="#2c5282")
        ax.text(x + 0.2, y, name, ha='center', va='center', fontsize=8.5, color="#2d3748")

    # Connectors
    ax.annotate("", xy=(3.1, 7.8), xytext=(2.1, 8.8), arrowprops=dict(arrowstyle="<->", color="#718096", lw=1))
    ax.annotate("", xy=(3.1, 7.4), xytext=(2.1, 6.8), arrowprops=dict(arrowstyle="<->", color="#718096", lw=1))
    ax.annotate("Stock Increments", xy=(8.6, 7.8), xytext=(4.9, 7.8), 
                arrowprops=dict(arrowstyle="->", color="#38a169", lw=1.5), ha='center', va='bottom', fontsize=8.5, color="#22543d")
    ax.annotate("", xy=(11.6, 7.8), xytext=(10.4, 7.8), arrowprops=dict(arrowstyle="<->", color="#718096", lw=1.5))
    ax.annotate("Atomic Stock Deduction", xy=(9.0, 7.0), xytext=(4.5, 5.3),
                arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=1.5), ha='center', va='center', fontsize=8.5, color="#742a2a")
    ax.annotate("", xy=(5.9, 4.5), xytext=(4.9, 4.5), arrowprops=dict(arrowstyle="<->", color="#718096", lw=1.5))
    ax.annotate("", xy=(8.6, 4.5), xytext=(7.7, 4.5), arrowprops=dict(arrowstyle="<->", color="#718096", lw=1.5))
    ax.annotate("", xy=(11.6, 4.5), xytext=(10.4, 4.5), arrowprops=dict(arrowstyle="->", color="#805ad5", lw=1.5))
    ax.annotate("Aggregate Queries", xy=(6.8, 2.4), xytext=(6.8, 3.8), arrowprops=dict(arrowstyle="<-", color="#3182ce", lw=1.5),
                ha='center', va='center', fontsize=8.5, color="#2b6cb0")

    save_fig(fig, "dfd_level_1.png")

# 5. ER Diagram (High-res PNG)
def make_er_diagram():
    fig, ax = plt.subplots(figsize=(15, 11))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis('off')

    ax.text(7.5, 10.5, "Entity-Relationship (ER) Diagram - Chen Notation", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1a365d')

    def entity(x, y, name):
        r = patches.Rectangle((x-1.1, y-0.45), 2.2, 0.9, facecolor="#ebf8ff", edgecolor="#2b6cb0", lw=2)
        ax.add_patch(r)
        ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold', color="#1a365d")

    def rel(x, y, name):
        p = patches.Polygon([[x, y+0.45], [x+0.85, y], [x, y-0.45], [x-0.85, y]], 
                            facecolor="#fefcbf", edgecolor="#b7791f", lw=1.5)
        ax.add_patch(p)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='medium', color="#744210")

    def attr(x, y, name, is_pk=False, is_fk=False):
        ls = '--' if is_fk else '-'
        el = patches.Ellipse((x, y), 1.4, 0.5, facecolor="white", edgecolor="#4a5568", lw=1.2, linestyle=ls)
        ax.add_patch(el)
        weight = 'bold' if is_pk else 'normal'
        t = ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight=weight, color="#2d3748")
        if is_pk:
            # Underline
            ax.plot([x - len(name)*0.045, x + len(name)*0.045], [y - 0.12, y - 0.12], color="#2d3748", lw=1)

    # Entities
    entity(3.0, 8.5, "Donor")
    entity(12.0, 8.5, "Donation")
    entity(7.5, 5.5, "Blood_Group")
    entity(3.0, 2.5, "Blood_Stock")
    entity(12.0, 2.5, "Blood_Request")
    entity(12.0, 0.5, "Hospital")
    entity(7.5, 2.5, "Admin_Audit_Log")

    # Relationships
    rel(7.5, 8.5, "makes")
    rel(4.5, 7.0, "classifies")
    rel(10.5, 7.0, "typed as")
    rel(4.5, 4.0, "tracked in")
    rel(10.5, 4.0, "needed for")
    rel(12.0, 1.5, "raises")
    rel(9.5, 2.5, "logged")

    # Connect entities and relationships with cardinalities
    def line_with_card(x1, y1, x2, y2, card, cx, cy):
        ax.plot([x1, x2], [y1, y2], color="#718096", lw=1.5)
        ax.text(cx, cy, card, fontsize=10, fontweight='bold', color="#c53030")

    line_with_card(4.1, 8.5, 6.65, 8.5, "1", 4.4, 8.7)
    line_with_card(8.35, 8.5, 10.9, 8.5, "N", 10.6, 8.7)

    line_with_card(3.0, 8.05, 4.5, 7.0, "N", 3.4, 7.5)
    line_with_card(4.5, 7.0, 6.4, 5.5, "1", 5.7, 6.0)

    line_with_card(12.0, 8.05, 10.5, 7.0, "N", 11.6, 7.5)
    line_with_card(10.5, 7.0, 8.6, 5.5, "1", 9.3, 6.0)

    line_with_card(6.4, 5.5, 4.5, 4.0, "1", 5.6, 4.8)
    line_with_card(4.5, 4.0, 3.0, 2.95, "1", 3.4, 3.6)

    line_with_card(8.6, 5.5, 10.5, 4.0, "1", 9.4, 4.8)
    line_with_card(10.5, 4.0, 12.0, 2.95, "N", 11.6, 3.6)

    line_with_card(12.0, 2.05, 12.0, 1.5, "N", 12.2, 1.8)
    line_with_card(12.0, 1.5, 12.0, 0.95, "1", 12.2, 1.2)

    line_with_card(10.9, 2.5, 9.5, 2.5, "1", 10.6, 2.7)
    line_with_card(9.5, 2.5, 8.6, 2.5, "N", 8.8, 2.7)

    # Attributes Donor
    attrs_donor = [("Donor_ID", True, False), ("Name", False, False), ("Age", False, False), 
                   ("Gender", False, False), ("Phone", False, False), ("Bg_ID", False, True)]
    for i, (a, pk, fk) in enumerate(attrs_donor):
        ax.plot([3.0, 1.0], [8.5, 9.5 - i*0.4], color="#a0aec0", lw=1)
        attr(1.0, 9.5 - i*0.4, a, pk, fk)

    # Attributes Donation
    attrs_donation = [("Donation_ID", True, False), ("Donor_ID", False, True), ("Bg_ID", False, True), 
                      ("Donation_Date", False, False), ("Units_Donated", False, False)]
    for i, (a, pk, fk) in enumerate(attrs_donation):
        ax.plot([12.0, 14.0], [8.5, 9.3 - i*0.4], color="#a0aec0", lw=1)
        attr(14.0, 9.3 - i*0.4, a, pk, fk)

    # Attributes Blood_Group
    ax.plot([7.5, 6.8], [5.5, 6.4], color="#a0aec0", lw=1)
    attr(6.8, 6.4, "Bg_ID", True, False)
    ax.plot([7.5, 8.2], [5.5, 6.4], color="#a0aec0", lw=1)
    attr(8.2, 6.4, "Blood_Type", False, False)

    # Attributes Blood_Stock
    attrs_stock = [("Stock_ID", True, False), ("Bg_ID", False, True), ("Total_Qty", False, False), ("Last_Updated", False, False)]
    for i, (a, pk, fk) in enumerate(attrs_stock):
        ax.plot([3.0, 1.0], [2.5, 3.2 - i*0.45], color="#a0aec0", lw=1)
        attr(1.0, 3.2 - i*0.45, a, pk, fk)

    # Attributes Blood_Request
    attrs_req = [("Request_ID", True, False), ("Hospital_ID", False, True), ("Bg_ID", False, True), 
                 ("Date", False, False), ("Qty", False, False), ("Status", False, False)]
    for i, (a, pk, fk) in enumerate(attrs_req):
        ax.plot([12.0, 14.0], [2.5, 3.5 - i*0.4], color="#a0aec0", lw=1)
        attr(14.0, 3.5 - i*0.4, a, pk, fk)

    # Attributes Hospital
    attrs_hosp = [("Hospital_ID", True, False), ("Name", False, False), ("Address", False, False), ("Phone", False, False)]
    for i, (a, pk, fk) in enumerate(attrs_hosp):
        ax.plot([12.0, 14.0], [0.5, 1.2 - i*0.45], color="#a0aec0", lw=1)
        attr(14.0, 1.2 - i*0.45, a, pk, fk)

    # Attributes Admin_Audit_Log
    attrs_audit = [("Audit_ID", True, False), ("Proposal_Type", False, False), ("Proposal_ID", False, False),
                   ("Action", False, False), ("Detail", False, False), ("Decided_At", False, False)]
    for i, (a, pk, fk) in enumerate(attrs_audit):
        ax.plot([7.5, 5.8 + i*0.7], [2.5, 1.2 if i%2==0 else 1.7], color="#a0aec0", lw=1)
        attr(5.8 + i*0.7, 1.2 if i%2==0 else 1.7, a, pk, fk)

    # Legend
    leg_box = patches.Rectangle((0.2, 0.2), 3.0, 1.3, facecolor="#edf2f7", edgecolor="#cbd5e0", lw=1)
    ax.add_patch(leg_box)
    ax.text(0.4, 1.2, "Legend:", fontweight='bold', fontsize=9, color="#2d3748")
    ax.text(0.4, 0.9, "— Underlined = Primary Key (PK)", fontsize=8, color="#2d3748")
    ax.text(0.4, 0.6, "-- Dashed Ellipse = Foreign Key (FK)", fontsize=8, color="#2d3748")
    ax.text(0.4, 0.35, "1 / N = Cardinality Ratio", fontsize=8, color="#c53030", fontweight='bold')

    save_fig(fig, "er_diagram.png")

# 6. Sequence Diagram for Donation
def make_donation_sequence():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.5, "UML Sequence Diagram: Atomic Donation Registration Workflow", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1a365d')

    participants = [
        (1.5, "Client / User"),
        (4.5, "Flask App Controller"),
        (7.5, "Database Driver (db.py)"),
        (9.8, "MySQL (InnoDB)"),
    ]

    for x, name in participants:
        box = patches.Rectangle((x-1.0, 6.7), 2.0, 0.5, facecolor="#ebf8ff", edgecolor="#3182ce", lw=1.5)
        ax.add_patch(box)
        ax.text(x, 6.95, name, ha='center', va='center', fontsize=9, fontweight='bold', color="#1a365d")
        ax.plot([x, x], [6.7, 0.8], color="#cbd5e0", lw=1.5, linestyle="--")

    steps = [
        (6.3, 1.5, 4.5, "1. POST /donations (donor_id, bg_id, units, csrf)", "->"),
        (5.8, 4.5, 7.5, "2. with db.transaction() context", "->"),
        (5.3, 7.5, 9.8, "3. START TRANSACTION", "->"),
        (4.8, 7.5, 9.8, "4. SELECT Donor_ID, Bg_ID FROM Donor WHERE Donor_ID = %s", "->"),
        (4.3, 9.8, 7.5, "5. Return donor row (verify Bg_ID matches)", "<-"),
        (3.8, 7.5, 9.8, "6. INSERT INTO Donation (Units_Donated = %s)", "->"),
        (3.3, 7.5, 9.8, "7. UPDATE Blood_Stock SET Total_Qty = Total_Qty + %s", "->"),
        (2.8, 7.5, 9.8, "8. Check rowcount == 1 -> COMMIT", "->"),
        (2.3, 9.8, 4.5, "9. Transaction Success Status", "<-"),
        (1.8, 4.5, 1.5, "10. Redirect (PRG) & Flash Success Message", "<-"),
    ]

    for y, x1, x2, msg, direction in steps:
        color = "#2b6cb0" if direction == "->" else "#2c5282"
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=color, lw=1.3))
        ax.text((x1 + x2)/2, y + 0.12, msg, ha='center', va='bottom', fontsize=8, color="#2d3748")

    save_fig(fig, "donation_sequence.png")

# 7. Sequence Diagram for Request Fulfillment
def make_fulfillment_sequence():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ax.text(5.5, 8.0, "UML Sequence Diagram: Atomic Request Fulfilment with Row Locking", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1a365d')

    participants = [
        (1.5, "Hospital / Staff"),
        (4.5, "Flask Controller"),
        (7.5, "db.py (Tx Manager)"),
        (9.8, "MySQL (InnoDB)"),
    ]

    for x, name in participants:
        box = patches.Rectangle((x-1.0, 7.2), 2.0, 0.5, facecolor="#fff5f5", edgecolor="#e53e3e", lw=1.5)
        ax.add_patch(box)
        ax.text(x, 7.45, name, ha='center', va='center', fontsize=9, fontweight='bold', color="#742a2a")
        ax.plot([x, x], [7.2, 0.6], color="#cbd5e0", lw=1.5, linestyle="--")

    steps = [
        (6.7, 1.5, 4.5, "1. POST /requests/<id>/fulfill (csrf_token)", "->"),
        (6.2, 4.5, 7.5, "2. with db.transaction() -> start_transaction()", "->"),
        (5.7, 7.5, 9.8, "3. SELECT ... FROM Blood_Request FOR UPDATE (Lock Request)", "->"),
        (5.1, 7.5, 9.8, "4. SELECT Total_Qty FROM Blood_Stock FOR UPDATE (Lock Stock)", "->"),
        (4.5, 9.8, 7.5, "5. Return locked row (Verify Total_Qty >= Qty)", "<-"),
        (3.9, 7.5, 9.8, "6. UPDATE Blood_Stock SET Total_Qty = Total_Qty - %s", "->"),
        (3.3, 7.5, 9.8, "7. UPDATE Blood_Request SET Status = 'Completed'", "->"),
        (2.7, 7.5, 9.8, "8. COMMIT (Atomic Stock Deduction & Completion)", "->"),
        (2.1, 9.8, 4.5, "9. Transaction Committed Successfully", "<-"),
        (1.5, 4.5, 1.5, "10. HTTP 302 Redirect with Flash Message", "<-"),
    ]

    for y, x1, x2, msg, direction in steps:
        color = "#c53030" if direction == "->" else "#2b6cb0"
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=color, lw=1.3))
        ax.text((x1 + x2)/2, y + 0.12, msg, ha='center', va='bottom', fontsize=8, color="#2d3748")

    save_fig(fig, "fulfillment_sequence.png")

if __name__ == "__main__":
    make_architecture()
    make_use_case()
    make_dfd_0()
    make_dfd_1()
    make_er_diagram()
    make_donation_sequence()
    make_fulfillment_sequence()
    print("All diagrams generated successfully.")


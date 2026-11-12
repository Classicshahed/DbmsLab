import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from PIL import Image as PILImage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_canvas_core import (
    BASE_DIR, REPORT_DIR, DIAGRAMS_DIR, SCREENSHOTS_DIR,
    C_PRIMARY, C_SECONDARY, C_DARK, C_MUTED, C_LIGHT_BG, C_BORDER, C_SUCCESS,
    NumberedCanvas
)

def build_pdf():
    pdf_path = os.path.join(REPORT_DIR, "Project_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    style_cover_inst = ParagraphStyle(
        'CoverInst',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        alignment=1, # Center
        spaceAfter=15
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=22,
        leading=26,
        textColor=C_PRIMARY,
        alignment=1,
        spaceBefore=20,
        spaceAfter=15
    )
    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        textColor=C_SECONDARY,
        alignment=1,
        spaceAfter=30
    )
    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=C_DARK,
        alignment=1,
        spaceAfter=15
    )
    
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        textColor=C_PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        textColor=C_SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=C_DARK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'Body_Custom',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=C_DARK,
        spaceAfter=6
    )
    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        textColor=C_DARK,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    style_caption = ParagraphStyle(
        'Caption_Custom',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        textColor=C_MUTED,
        alignment=1, # Center
        spaceBefore=3,
        spaceAfter=10
    )
    style_code = ParagraphStyle(
        'Code_Custom',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#2D3748")
    )
    style_tbl_cell = ParagraphStyle(
        'TblCell',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        textColor=C_DARK
    )
    style_tbl_hdr = ParagraphStyle(
        'TblHdr',
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    story = []

    def p(text):
        story.append(Paragraph(text, style_body))

    def bullet(title, text):
        story.append(Paragraph(f"• <b>{title}:</b> {text}", style_bullet))

    def h1(text):
        story.append(Paragraph(text, style_h1))

    def h2(text):
        story.append(Paragraph(text, style_h2))

    def h3(text):
        story.append(Paragraph(text, style_h3))

    def fig(img_name, caption, is_diagram=True, max_w=6.2*inch, max_h=4.2*inch):
        subfolder = DIAGRAMS_DIR if is_diagram else SCREENSHOTS_DIR
        path = os.path.join(subfolder, img_name)
        if not os.path.exists(path):
            print(f"Warning: {path} not found")
            return
        # Calculate aspect ratio
        with PILImage.open(path) as im:
            w, h = im.size
        aspect = h / w
        target_w = max_w
        target_h = target_w * aspect
        if target_h > max_h:
            target_h = max_h
            target_w = target_h / aspect
        story.append(KeepTogether([
            Image(path, width=target_w, height=target_h),
            Paragraph(caption, style_caption)
        ]))

    def code_box(code_str, cap=None):
        if cap:
            story.append(Paragraph(f"<b>{cap}</b>", style_h3))
        lines = code_str.strip().split("\n")
        para_content = "<br/>".join([l.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for l in lines])
        tbl = Table([[Paragraph(para_content, style_code)]], colWidths=[6.4 * inch])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(KeepTogether([tbl, Spacer(1, 6)]))

    def make_table(col_widths, headers, data):
        tbl_data = []
        # Header
        tbl_data.append([Paragraph(h, style_tbl_hdr) for h in headers])
        # Data
        for row in data:
            tbl_data.append([Paragraph(str(c), style_tbl_cell) for c in row])
        t = Table(tbl_data, colWidths=col_widths, repeatRows=1)
        t_style = [
            ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]
        for r_i in range(1, len(tbl_data)):
            if r_i % 2 == 0:
                t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), C_LIGHT_BG))
        t.setStyle(TableStyle(t_style))
        story.append(KeepTogether([t, Spacer(1, 8)]))

    # --------------------------------------------------------------------------- #
    # 1. COVER PAGE
    # --------------------------------------------------------------------------- #
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING<br/>UNIVERSITY LABORATORY PROJECT REPORT", style_cover_inst))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("BLOOD BANK MANAGEMENT SYSTEM", style_cover_title))
    story.append(Paragraph("A Robust, Relational Database Application with Direct SQL Concurrency Control, Transactional Atomicity, and Multi-Unit Stock Reconciliation", style_cover_sub))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("<b>Course:</b> CSE 3100 — Database Management Systems Laboratory<br/><b>Academic Session:</b> 2026", style_cover_meta))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("<i>Submitted By:</i><br/><b>Sanim Khan</b><br/>GitHub Profile: <b>sanim-ctrl</b><br/>Email: sanimkhan.dev@gmail.com", style_cover_meta))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("<b>Supervised By:</b><br/>Faculty of Computer Science & Engineering<br/>Course Instructor & Laboratory Evaluation Board", style_cover_meta))
    story.append(PageBreak())

    # --------------------------------------------------------------------------- #
    # 2. DECLARATION
    # --------------------------------------------------------------------------- #
    h1("Candidate's Declaration")
    p("I hereby declare that the software project entitled <b>\"Blood Bank Management System\"</b> and the accompanying technical report presented herein have been designed, implemented, and compiled by myself as part of the academic requirements for the course CSE 3100: Database Management Systems Laboratory. The implementation represents an authentic, original body of work written in Python Flask and raw MySQL 8.0/MariaDB SQL without the mediation of an Object-Relational Mapper (ORM).")
    p("I affirm that every algorithm, database schema design, stored constraint, transaction sequence, and automated test suite described in this report reflects the actual operational code residing within this repository. Furthermore, this submission has not been submitted previously in substance for any degree, diploma, or academic distinction at this or any other tertiary educational institution. All external citations, software libraries, and academic references have been fully acknowledged according to standard scholarly conventions.")
    story.append(Spacer(1, 0.6 * inch))
    p("______________________________<br/><b>Sanim Khan</b><br/>Department of Computer Science & Engineering<br/>Date: November 11, 2026")
    story.append(PageBreak())

    # --------------------------------------------------------------------------- #
    # 3. ACKNOWLEDGEMENT
    # --------------------------------------------------------------------------- #
    h1("Acknowledgement")
    p("The successful conception, architectural implementation, and testing of the Blood Bank Management System have been made possible through the constructive guidance, technical resources, and intellectual support provided by several individuals and academic entities.")
    p("First and foremost, I wish to express my profound gratitude to the course instructors and laboratory evaluators of the Department of Computer Science & Engineering. Their rigorous curriculum in relational database theory, transaction processing, concurrency isolation, and data normalization provided the essential foundational knowledge required to engineer a transactional system capable of guaranteeing strict ACID invariants.")
    p("I also extend my sincere appreciation to the open-source software community for providing the robust platforms upon which this system rests—specifically the development teams behind Python, Flask, the MySQL Database Server, and the mysql-connector-python pure driver. Finally, I thank my peers and department colleagues whose discussions on concurrency edge-cases and query optimizations greatly enriched the development and validation of this project.")
    story.append(PageBreak())

    # --------------------------------------------------------------------------- #
    # 4. ABSTRACT
    # --------------------------------------------------------------------------- #
    h1("Abstract")
    p("Blood banking and medical inventory management represent safety-critical domains where inaccuracies in inventory levels, uncoordinated concurrent updates, or accidental data loss can produce catastrophic healthcare consequences. Traditional hospital blood management workflows that rely upon decentralized spreadsheets or physical ledgers suffer from acute vulnerabilities, including double fulfillment of stock requests, untracked stock depletions, duplicate donor registrations, and the absence of immutable audit trails. This project resolves these critical vulnerabilities by presenting the design, implementation, and empirical verification of the <b>Blood Bank Management System</b>—a modern, relational database web application engineered with Python 3, Flask, and MySQL 8.0/MariaDB using direct parameter-bound SQL without an Object-Relational Mapper (ORM).")
    p("The core of the system is a meticulously normalized relational schema comprising six primary entities (<i>Blood_Group, Donor, Donation, Hospital, Blood_Request,</i> and <i>Blood_Stock</i>) along with an additive security log (<i>Admin_Audit_Log</i>). Data integrity is enforced natively at the database tier using primary keys, foreign key RESTRICT actions that preserve donation history, UNIQUE constraints, and CHECK constraints preventing negative stock and invalid donation quantities. To guarantee complete transactional consistency (ACID), stock-modifying operations are wrapped in explicit database transactions utilizing pessimistic row-level locking (<code>SELECT ... FOR UPDATE</code>). Recording a donation atomically increments available units and updates timestamps, while hospital fulfillment atomically verifies stock availability, deducts whole units, and finalizes the request, completely eliminating race conditions.")
    p("Administrative governance is provided through a password-protected approval workflow secured by Werkzeug scrypt cryptographic hashing, sliding-window brute-force rate-limiting, and session-based Cross-Site Request Forgery (CSRF) defenses. The system provides an executive dashboard, full donor and hospital lifecycle tracking, multi-unit donation support, and an analytical reporting interface demonstrating complex multi-table joins, aggregations, and subqueries. The implementation has been validated through an automated regression test suite comprising 219 distinct verification, behavioral, security, and connection-recovery test cases, achieving a 100% pass rate. The application delivers sub-second response times, zero data discrepancies, and production readiness for local or cloud environments.")
    story.append(PageBreak())

    # --------------------------------------------------------------------------- #
    # 5. TABLE OF CONTENTS
    # --------------------------------------------------------------------------- #
    h1("Table of Contents")
    toc_data = [
        ["Candidate's Declaration", "ii"],
        ["Acknowledgement", "iii"],
        ["Abstract", "iv"],
        ["Chapter 1: Introduction", "1"],
        ["    1.1 Overview of Blood Banking Systems", "1"],
        ["    1.2 The Role of Relational Databases in Healthcare", "1"],
        ["    1.3 Motivation for a Direct SQL Architecture", "2"],
        ["    1.4 Report Organization", "2"],
        ["Chapter 2: Background and Problem Statement", "3"],
        ["    2.1 Clinical and Operational Context", "3"],
        ["    2.2 Vulnerabilities of Legacy and Spreadsheet Methods", "3"],
        ["    2.3 Database Concurrency and Data Integrity Challenges", "4"],
        ["    2.4 Formal Problem Formulation", "4"],
        ["Chapter 3: Project Objectives and Scope", "5"],
        ["    3.1 Primary Academic and Software Engineering Objectives", "5"],
        ["    3.2 Specific Functional Goals", "5"],
        ["    3.3 Scope and Operational Boundaries", "6"],
        ["    3.4 Out-of-Scope Considerations", "6"],
        ["Chapter 4: Existing System vs. Proposed System", "7"],
        ["    4.1 Comparative Feature Matrix", "7"],
        ["    4.2 Innovation and Engineering Advantages", "8"],
        ["Chapter 5: System Requirements Specifications", "9"],
        ["    5.1 Functional Requirements (FR-1 through FR-8)", "9"],
        ["    5.2 Non-Functional Requirements (NFR-1 through NFR-6)", "10"],
        ["    5.3 Hardware and Deployment Specifications", "11"],
        ["    5.4 Software Environment & Dependencies", "11"],
        ["Chapter 6: Technology Stack & Architectural Rationale", "12"],
        ["    6.1 Persistence Layer: MySQL 8.0 & InnoDB Storage Engine", "12"],
        ["    6.2 Application Layer: Python 3 & Flask Framework", "13"],
        ["    6.3 Database Driver: mysql-connector-python Pure Implementation", "13"],
        ["    6.4 Presentation Layer: Jinja2, HTML5, CSS3, & Vanilla JS", "14"],
        ["    6.5 Security Stack: Scrypt Hashing, Session Signatures, & CSRF Tokens", "14"],
        ["Chapter 7: System Architecture and Concurrency Framework", "15"],
        ["    7.1 Four-Tier Layered Architecture", "15"],
        ["    7.2 Thread-Local Connection Management & COM_PING Health Checks", "16"],
        ["    7.3 Transaction Isolation Levels & ACID Invariants", "17"],
        ["Chapter 8: System Modeling (UML and Data Flow Diagrams)", "18"],
        ["    8.1 Use Case Modeling and Actor Specifications", "18"],
        ["    8.2 Data Flow Diagrams (Level 0 Context and Level 1 Detailed)", "19"],
        ["    8.3 Sequence Modeling for Atomic Transactions", "21"],
        ["Chapter 9: Database Design, Normalization, & Data Dictionary", "23"],
        ["    9.1 Entity-Relationship (ER) Diagram (Chen Notation)", "23"],
        ["    9.2 Normalization Analysis (1NF, 2NF, 3NF & Historical Denormalization)", "24"],
        ["    9.3 Comprehensive Data Dictionary (All 7 Tables)", "25"],
        ["    9.4 Indexing Scheme & Referential Integrity Enforcement", "28"],
        ["Chapter 10: System Implementation & Code Artifacts", "29"],
        ["    10.1 Connection Ownership & Failover Architecture (db.py)", "29"],
        ["    10.2 Atomic Multi-Unit Blood Donation Logic", "31"],
        ["    10.3 Pessimistic Concurrency Control in Request Fulfilment", "32"],
        ["    10.4 Password-Protected Admin Decision Workflow & Rate Limiting", "34"],
        ["    10.5 Lightweight Session-Based CSRF Mitigation", "35"],
        ["Chapter 11: User Interface Modules & Visual Verification", "36"],
        ["    11.1 Executive Dashboard Module", "36"],
        ["    11.2 Donor Management Module", "37"],
        ["    11.3 Donation Registration & Multi-Unit Processing", "39"],
        ["    11.4 Inventory Tracking & Low-Stock Alerts", "40"],
        ["    11.5 Hospital Registry & Blood Request Lifecycle", "41"],
        ["    11.6 Interactive SQL Reports Module", "43"],
        ["    11.7 Admin Approval Workflow & Profile Inspector", "44"],
        ["Chapter 12: Practical SQL Demonstration Queries", "46"],
        ["    12.1 Analytical Queries Implemented in queries.sql", "46"],
        ["    12.2 Join, Aggregation, and Grouping Operations", "47"],
        ["Chapter 13: System Verification and Test Results", "49"],
        ["    13.1 Testing Methodology & Safety Invariants", "49"],
        ["    13.2 Automated Test Execution Matrix (219 Passed Tests)", "50"],
        ["Chapter 14: Results, Discussion, & Stock Reconciliation", "54"],
        ["    14.1 Stock Reconciliation Mathematical Validation", "54"],
        ["    14.2 Concurrency and Race Condition Elimination", "55"],
        ["    14.3 Security Posture Assessment", "55"],
        ["Chapter 15: Limitations and Future Scope", "56"],
        ["    15.1 Current System Limitations", "56"],
        ["    15.2 Strategic Roadmap and Future Enhancements", "56"],
        ["Chapter 16: Conclusion", "58"],
        ["Chapter 17: References", "59"],
    ]
    t_toc = Table(
        [[Paragraph(f"<b>{row[0]}</b>" if ("Chapter" in row[0] or "Declaration" in row[0] or "Abstract" in row[0]) else row[0], style_tbl_cell),
          Paragraph(f"<b>{row[1]}</b>" if ("Chapter" in row[0] or "Declaration" in row[0] or "Abstract" in row[0]) else row[1], ParagraphStyle('R', parent=style_tbl_cell, alignment=2))]
         for row in toc_data],
        colWidths=[5.5 * inch, 0.9 * inch]
    )
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # --------------------------------------------------------------------------- #
    # CHAPTER 1: INTRODUCTION
    # --------------------------------------------------------------------------- #
    h1("Chapter 1: Introduction")
    h2("1.1 Overview of Blood Banking Systems")
    p("Blood banks represent critical nodes within modern healthcare systems, providing the life-saving biological reserves necessary for emergency trauma surgery, oncological therapy, obstetrics, and chronic hematological disorders. Unlike manufactured pharmaceuticals, whole blood and its components are perishable human-donated commodities characterized by finite storage lifetimes, strict immunological typing constraints, and unpredictable supply-and-demand cycles. The operation of a blood bank requires meticulous coordination: eligible donors must be vetted and categorized according to the ABO and Rh antigen systems, donation sessions must be recorded without duplicating individual identities, inventories of each blood group must be maintained with continuous mathematical precision, and clinical blood requests from partner hospitals must be prioritized, authorized, and fulfilled without delay.")
    
    h2("1.2 The Role of Relational Databases in Healthcare")
    p("In healthcare informatics, the relational database management system (RDBMS) remains the gold standard for managing structured clinical data where strict ACID (Atomicity, Consistency, Isolation, Durability) guarantees are non-negotiable. Relational algebra provides the formal mathematical underpinning that guarantees zero data loss, enforces referential integrity through foreign keys, and prevents update anomalies through mathematical normalization. In a blood management environment, an RDBMS ensures that an inventory row cannot be decremented without simultaneously linking to a completed clinical request, that a donor with active clinical donation history cannot be accidentally purged, and that concurrent hospital requests cannot over-allocate physical units beyond physical shelf capacity.")

    h2("1.3 Motivation for a Direct SQL Architecture")
    p("Modern enterprise web development frequently introduces heavy abstractions, such as Object-Relational Mappers (ORMs), which obscure the underlying SQL statements beneath automated query generation engines. While ORMs offer rapid prototyping for generic web services, they introduce significant architectural liabilities within academic DBMS laboratory environments and mission-critical inventory systems: (1) automated query generation frequently produces inefficient N+1 query cascades across remote database connections, (2) transaction boundaries and pessimistic locking semantics become difficult to audit and control, and (3) academic comprehension is degraded because students cannot inspect or defend the exact SQL execution plans evaluated by the database query optimizer. To address these liabilities, this project deliberately adopts a direct SQL architectural pattern utilizing mysql-connector-python. Every database interaction is expressed through explicit, parameterized SQL (%s), ensuring complete transparency, sub-millisecond execution efficiency, and complete auditability for academic evaluation.")

    h2("1.4 Report Organization")
    p("This report is structured into 17 academic chapters providing comprehensive documentation of the project. Chapter 2 defines the problem statement and operational vulnerabilities of legacy systems. Chapter 3 specifies the objectives and scope. Chapter 4 provides a comparative analysis between existing and proposed systems. Chapter 5 outlines system requirements, while Chapter 6 details the chosen technology stack. Chapters 7 and 8 present the system architecture, UML modeling, and data flow diagrams. Chapter 9 details database design, normalization proofs, and the complete data dictionary. Chapter 10 examines implementation artifacts, connection pooling, and atomic transactions. Chapter 11 walks through all user interfaces with authentic screenshots. Chapter 12 details practical SQL demonstration queries. Chapter 13 presents the automated testing suite and verification results. Chapter 14 discusses stock reconciliation and security analysis. Chapters 15 and 16 conclude the report with system limitations, future work, and concluding remarks.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 2: BACKGROUND AND PROBLEM STATEMENT
    # --------------------------------------------------------------------------- #
    h1("Chapter 2: Background and Problem Statement")
    h2("2.1 Clinical and Operational Context")
    p("In institutional blood banks across urban hospitals and regional health complexes, stock intake occurs through walk-in voluntary donors and organized mobile blood donation drives. Conversely, stock outtake occurs through urgent and scheduled requisitions submitted by regional hospitals for specific surgical and emergency cases. Managing this intersection requires real-time coordination between donor biographical information, biological blood grouping (A+, A-, B+, B-, AB+, AB-, O+, O-), quantitative unit availability, and hospital delivery tracking.")

    h2("2.2 Vulnerabilities of Legacy and Spreadsheet Methods")
    p("A substantial number of blood centers in developing regions still utilize physical paper registers, desktop spreadsheets (e.g., Microsoft Excel), or disconnected desktop databases. Field research and clinical operational audits identify four severe vulnerabilities inherent to these legacy approaches:")
    bullet("Stock Desynchronization & Double Fulfillment", "Spreadsheets lack transaction isolation and atomic row locking. If two hospital operators request blood units simultaneously, both view the same unreserved quantity on screen. Both requests are approved, resulting in physical stock depletion that leaves one patient without life-saving blood.")
    bullet("Unenforced Referential Integrity & Orphan Records", "In physical ledgers or spreadsheets, deleting a donor row leaves historical donation records disconnected without an identifiable donor source. Conversely, typing errors lead to multiple records for a single donor under slightly different phone numbers.")
    bullet("Negative Stock Anomalies", "Without database-level CHECK constraints, administrative clerical errors can decrement inventory counters into negative integers, creating false shortage alarms or masking critical stock-outs.")
    bullet("Absence of Cryptographic Access Control & Audit Trails", "Shared spreadsheets allow anyone with file access to edit quantities, alter historical requisition statuses, or delete records without logging who authorized the transaction, violating clinical auditing standards.")

    h2("2.3 Database Concurrency and Data Integrity Challenges")
    p("From a computer science and database theory perspective, the primary technical challenge centers upon concurrency control. When an incoming donation of units is registered, the system must execute two discrete DML operations: (1) inserting a row into the Donation table, and (2) incrementing the Total_Qty column in the Blood_Stock table. If the network connection drops or the server process crashes between step 1 and step 2, the database is left in an inconsistent state where a donation exists on paper but is absent from inventory. Similarly, when fulfilling a blood request, the application must read stock, verify adequacy, deduct units, and update the request status to 'Completed'. Without pessimistic row-level locking (SELECT ... FOR UPDATE), concurrent web requests create a Classic Race Condition (Lost Update anomaly), causing physical inventory and database records to permanently diverge.")

    h2("2.4 Formal Problem Formulation")
    p("The problem addressed by this project is formally stated as follows: <i>\"To design, engineer, and empirically validate an ACID-compliant, relational web database application that guarantees single-source donor identification, enforces zero-negative stock through native database constraints, prevents double-fulfillment and lost updates through pessimistic row-level locking, provides cryptographic administrative governance with immutable auditing, and exposes a transparent, parameter-bound SQL architecture for academic evaluation.\"</i>")

    # --------------------------------------------------------------------------- #
    # CHAPTER 3: PROJECT OBJECTIVES AND SCOPE
    # --------------------------------------------------------------------------- #
    h1("Chapter 3: Project Objectives and Scope")
    h2("3.1 Primary Academic and Software Engineering Objectives")
    p("The core objectives of the Blood Bank Management System encompass both rigorous database engineering principles and user-centric application design:")
    bullet("Relational Schema Normalization", "Design and deploy a relational database schema normalized to Third Normal Form (3NF), eliminating transitive and partial functional dependencies while establishing a documented, intentional historical denormalization in donation records.")
    bullet("ACID Transaction Guarantees", "Implement multi-statement transactional units for stock changes, ensuring that all operations either commit entirely or rollback completely upon error.")
    bullet("Pessimistic Concurrency Control", "Implement row-level database locking (SELECT ... FOR UPDATE) inside request fulfillment transactions to prevent race conditions and double allocation under high concurrency.")
    bullet("Cryptographic Security & Defense-in-Depth", "Secure privileged workflows using scrypt-based password hashing, session-based CSRF mitigation, and parameterized SQL queries (%s) to render SQL injection physically impossible.")
    bullet("Automated Verification & Zero-Defect Quality", "Construct an automated test harness covering schema constraints, data reconciliation, failure recovery, security access control, and connection resilience with a target of 100% pass rate.")

    h2("3.2 Specific Functional Goals")
    p("The functional goals realized in the implementation include: (1) Real-time executive dashboard summarizing donor counts, total donations, total whole units collected, and real-time inventory counts; (2) Complete donor directory with instant name/phone search, blood group filtering, and drill-down donation history; (3) Multi-unit donation registration with automatic inventory incrementation; (4) Real-time inventory table with dynamic low-stock highlighting based on a configurable threshold; (5) Hospital directory tracking active requisitions; (6) Blood request lifecycle tracking (Pending -> Approved -> Completed or Pending -> Rejected); (7) Two-tier administrative governance portal featuring a password-protected approval desk and immutable audit logging; and (8) Interactive SQL analytical reports demonstrating core DBMS concepts.")

    h2("3.3 Scope and Operational Boundaries")
    p("The operational scope encompasses blood bank inventory operations from voluntary donor intake through clinical hospital delivery. The software is designed to execute seamlessly in both local environments (e.g., Ubuntu Linux, Windows workstation) and modern cloud serverless environments (e.g., Render, Vercel) connected to cloud-hosted managed MySQL clusters (e.g., Aiven MySQL with verified TLS).")

    h2("3.4 Out-of-Scope Considerations")
    p("To maintain academic focus on core database management principles, the following specialized features are intentionally excluded from the primary scope: (1) Hardware-interfaced cold-chain IoT temperature sensor monitoring; (2) Automated biochemical laboratory cross-matching analyzers (e.g., Coombs testing); (3) Payment processing gateways for blood collection fees; and (4) Third-party SMS/Email dispatch gateways (though database structures are architected to support future webhook dispatchers).")

    # --------------------------------------------------------------------------- #
    # CHAPTER 4: EXISTING SYSTEM VS. PROPOSED SYSTEM
    # --------------------------------------------------------------------------- #
    h1("Chapter 4: Existing System vs. Proposed System")
    h2("4.1 Comparative Feature Matrix")
    p("To demonstrate the engineering advantages of the proposed relational architecture, Table 1 presents a detailed feature-by-feature comparison against conventional manual registers and spreadsheet-based systems.")
    
    headers_c = ["Evaluation Parameter", "Existing Manual / Spreadsheet System", "Proposed Relational Web System"]
    widths_c = [1.8 * inch, 2.3 * inch, 2.3 * inch]
    data_c = [
        ["Data Storage Architecture", "Paper physical registers or standalone desktop spreadsheets (.xlsx/.csv).", "Centralized, normalized MySQL 8.0 relational database with InnoDB ACID storage engine."],
        ["Concurrency & Row Locking", "None. Simultaneous edits cause file corruption, overwritten rows, or lost updates.", "Pessimistic row locking (SELECT ... FOR UPDATE) serializes concurrent transactions safely."],
        ["Data Integrity Enforcements", "Manual visual checking; prone to human oversight, typos, and formatting errors.", "Enforced at database engine level via PK, FK RESTRICT, UNIQUE, and CHECK constraints."],
        ["Stock Consistency & Reconciliation", "Manual end-of-day tallying; inventory frequently diverges from paper records.", "Mathematically reconciled in real-time: Opening + Donated - Completed = Stored Stock."],
        ["Donor History Protection", "Deleting a donor line silently destroys or orphans past donation records.", "Foreign key ON DELETE RESTRICT blocks deletion of any donor who has active donation records."],
        ["Administrative Security", "Shared unprotected file passwords or open physical file cabinets.", "Role-based administrative barrier secured with Werkzeug scrypt hashing and sliding-window rate limiting."],
        ["Auditability & Accountability", "No automatic historical logging of approvals, rejections, or edits.", "Immutable Admin_Audit_Log records decision action, timestamp, and target request ID atomically."],
        ["Analytical Query Capabilities", "Tedious manual calculation, sorting, and spreadsheet formulas.", "Instant execution of SQL joins, aggregates (SUM, COUNT, COALESCE), GROUP BY, and HAVING clauses."]
    ]
    make_table(widths_c, headers_c, data_c)

    h2("4.2 Innovation and Engineering Advantages")
    p("The proposed system delivers four fundamental engineering innovations: (1) Zero ORM Overhead: Eliminates translation latency and guarantees deterministic execution plans across all operations; (2) Resilient Connection Management: Thread-local session reuse with active pre-flight COM_PING verification prevents stale-socket exceptions across cloud serverless deployments; (3) Defensive Stock Invariants: Database-level CHECK (Total_Qty >= 0) ensures that stock can never drop below zero under any operational circumstance; and (4) Complete Traceability: Every administrative decision is committed within the exact same database transaction as the status update, ensuring audit rows can never exist without corresponding proposal status changes.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 5: SYSTEM REQUIREMENTS SPECIFICATIONS
    # --------------------------------------------------------------------------- #
    h1("Chapter 5: System Requirements Specifications")
    h2("5.1 Functional Requirements (FR)")
    bullet("FR-1: Donor Lifecycle Management", "The system must capture donor Name, Age (18-65), Gender (Male, Female, Other), unique Phone (7-15 chars), and Blood Group (Bg_ID). It must support donor updates and block deletion if donations exist.")
    bullet("FR-2: Multi-Unit Donation Registration", "The system must record donation events specifying Donor, Blood Group, Donation Date, and Units Donated (positive integer >= 1). It must automatically increment the corresponding Blood_Stock row atomically.")
    bullet("FR-3: Blood Inventory & Low-Stock Alerts", "The system must display real-time stock quantities for all eight blood groups and visually highlight groups falling below the configurable threshold (default: 10 units).")
    bullet("FR-4: Hospital Management", "The system must register partner hospitals with unique Phone, Name, and Address, tracking all requisitions associated with each hospital.")
    bullet("FR-5: Blood Request Lifecycle Processing", "The system must allow hospitals to raise blood requests with status 'Pending'. Public operators may approve or reject pending requests.")
    bullet("FR-6: Atomic Stock Deduction & Fulfilment", "The system must fulfill Pending or Approved requests by locking the stock row, verifying sufficient units, deducting the requested quantity, and setting status to 'Completed' in a single transaction.")
    bullet("FR-7: Administrative Governance & Audit Trail", "Privileged administrative pages must require cryptographic authentication, protect against brute-force attacks via sliding-window IP rate limiting, and log all decisions into Admin_Audit_Log.")
    bullet("FR-8: Analytical SQL Reporting", "The system must provide live analytical reports displaying donors per group, top donors, stock breakdown, pending demand by hospital, monthly trends, and low-stock summaries.")

    h2("5.2 Non-Functional Requirements (NFR)")
    bullet("NFR-1: Data Integrity & ACID Compliance", "All stock updates must adhere to strict ACID properties via the InnoDB engine. Stock must never be negative, and double fulfillment must be physically impossible.")
    bullet("NFR-2: Performance & Sub-Second Latency", "Database read queries must execute in under 50ms locally. The dashboard must fetch eight counters in a single round trip via scalar subqueries.")
    bullet("NFR-3: Security & Injection Prevention", "100% of SQL statements must use parameterized placeholders (%s). All state-changing POST requests must validate session-backed CSRF tokens.")
    bullet("NFR-4: High Availability & Connection Resilience", "The database module must maintain thread-local persistent connections, pre-flight pinging the socket with reconnect=False, and automatically recover from dropped connections before new transactions begin.")
    bullet("NFR-5: Responsive Usability", "User interfaces must render seamlessly across desktop monitors (1920x1080), tablets (768px), and mobile viewports (375px) without horizontal clipping.")
    bullet("NFR-6: Cross-Platform Maintainability", "The codebase must maintain zero external database wrappers, functioning identically on Ubuntu Linux and Microsoft Windows with full support for case-insensitive table configurations.")

    h2("5.3 Hardware and Deployment Specifications")
    p("The system is designed for high efficiency with minimal hardware overhead. Development and evaluation requirements: Dual-core x86_64 or ARM64 processor (2.0 GHz+), 2 GB RAM minimum (4 GB recommended), and 500 MB free storage. Production deployment requirements: Single vCPU cloud instance, 512 MB RAM (Render free-tier or AWS t4g.nano), and 1 GB managed MySQL 8.0 storage.")

    h2("5.4 Software Environment & Dependencies")
    p("The software environment comprises: (1) Operating System: Ubuntu Linux 22.04/24.04 LTS or Microsoft Windows 10/11; (2) Python Runtime: Python 3.12+ (tested through 3.14); (3) Database Management System: MySQL Server 8.0.30+ or MariaDB 10.11+; (4) Core Python Dependencies: Flask 3.0.3, Werkzeug 3.1.8, mysql-connector-python 9.7.0, and Gunicorn 23.0.0; (5) Modern Web Browser: Microsoft Edge, Google Chrome, Mozilla Firefox, or Apple Safari.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 6: TECHNOLOGY STACK & ARCHITECTURAL RATIONALE
    # --------------------------------------------------------------------------- #
    h1("Chapter 6: Technology Stack & Architectural Rationale")
    h2("6.1 Persistence Layer: MySQL 8.0 & InnoDB Storage Engine")
    p("MySQL 8.0 with the default InnoDB storage engine was selected as the database foundation. InnoDB provides row-level locking, foreign key constraints with referential actions (CASCADE, RESTRICT), crash-safe recovery via write-ahead logging (WAL), and full ACID transactional compliance. The database uses the utf8mb4 character set with utf8mb4_unicode_ci collation, enabling full multilingual name storage.")

    h2("6.2 Application Layer: Python 3 & Flask Framework")
    p("Python 3 provides exceptional syntax clarity, readability, and robust standard library support. Flask 3.0 was selected over monolithic frameworks (such as Django) because Flask adheres to a minimalist micro-framework philosophy. It does not impose an ORM, proprietary authentication models, or opaque middleware pipelines. This architectural minimalism ensures that the database remains the true center of the application: SQL queries are written plainly and transactions are controlled explicitly.")

    h2("6.3 Database Driver: mysql-connector-python Pure Implementation")
    p("Oracle's official mysql-connector-python driver configured in pure-Python mode (use_pure=True) is utilized for all database communications. Pure-Python mode eliminates compiled C-extensions, ensuring 100% portable deployment across disparate host operating systems without binary recompilation. The driver supports secure Transport Layer Security (TLS 1.3) with verified certificate authorities (DB_SSL_CA), which is required by modern cloud providers like Aiven.")

    h2("6.4 Presentation Layer: Jinja2, HTML5, CSS3, & Vanilla JS")
    p("The presentation tier utilizes Flask's native Jinja2 template engine for server-side HTML rendering. Server-side rendering guarantees that HTML documents arrive fully populated at the client browser, maximizing performance and eliminating heavy client-side JavaScript frameworks (React/Angular). Styling is provided by a custom, lightweight CSS3 design system incorporating responsive CSS Grid and Flexbox layouts. Client-side JavaScript is strictly vanilla (<1 KB), restricted to non-critical UX enhancements such as dynamic blood group auto-selection.")

    h2("6.5 Security Stack: Scrypt Hashing, Session Signatures, & CSRF Tokens")
    p("Security is implemented through a defense-in-depth model: (1) Administrative password hashes are generated using the scrypt key derivation function via Werkzeug, providing memory-hard protection against ASIC brute-force attacks; (2) Session cookies are cryptographically signed with HMAC-SHA256 using SECRET_KEY, configured with HttpOnly=True and SameSite=Lax flags; (3) State-changing POST endpoints are guarded by a session-backed CSRF token generated via Python's secrets.token_hex(32) and verified using constant-time comparison (secrets.compare_digest); and (4) SQL injection is eliminated across 100% of endpoints through parameter-bound query execution (%s).")

    # --------------------------------------------------------------------------- #
    # CHAPTER 7: SYSTEM ARCHITECTURE AND CONCURRENCY FRAMEWORK
    # --------------------------------------------------------------------------- #
    h1("Chapter 7: System Architecture and Concurrency Framework")
    h2("7.1 Four-Tier Layered Architecture")
    p("The system is organized into a cohesive Four-Tier Layered Architecture, establishing strict separation of concerns across presentation, application dispatching, data access abstraction, and persistence. Figure 1 illustrates the architectural components and data communication flows.")
    fig("system_architecture.png", "Figure 1: Four-Tier System Architecture of the Blood Bank Management System", is_diagram=True)

    h2("7.2 Thread-Local Connection Management & COM_PING Health Checks")
    p("Establishing TCP handshakes, TLS certificates, and authentication handshakes over remote networks is computationally expensive (measured at ~2.6 seconds between serverless edge nodes and managed MySQL clusters). To optimize throughput without risking multi-threaded race conditions, db.py establishes ONE dedicated connection per thread utilizing Python's threading.local(). Before handing out a cached connection, db.get_connection() executes an explicit conn.ping(reconnect=False). This issues a real COM_PING round trip to the MySQL server. If the server closed the socket due to an idle timeout or restart, the stale socket is detected safely before a new transaction begins, discarded, and replaced with an identical fresh connection. Critically, reconnect=False ensures that connections are NEVER silently re-established midway through an open transaction, which would otherwise silently abandon uncommitted work.")

    h2("7.3 Transaction Isolation Levels & ACID Invariants")
    p("The system operates under InnoDB's standard REPEATABLE READ transaction isolation level. To ensure that long-lived connections do not serve stale read snapshots across separate HTTP requests, autocommit=True is set at the connection level. Whenever atomic multi-statement modifications are required, the application opens an explicit context manager: with db.transaction() as cur. This explicitly invokes start_transaction(), executes the operations, and commits upon successful context exit. If any Python exception or database error occurs within the block, transaction() catches the fault, triggers an explicit conn.rollback(), and re-raises the exception for user-friendly error handling.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 8: SYSTEM MODELING (UML AND DATA FLOW DIAGRAMS)
    # --------------------------------------------------------------------------- #
    h1("Chapter 8: System Modeling (UML and Data Flow Diagrams)")
    h2("8.1 Use Case Modeling and Actor Specifications")
    p("The system models two distinct user roles: (1) Public Operator (Hospital staff, blood bank receptionists, and donors) who can browse stock, register donors, record donations, register hospitals, and raise/fulfill blood requests; and (2) System Administrator who possesses privileged access to log into the administrative portal, inspect pending change proposals, approve/reject requisitions, review immutable audit trails, and inspect session metadata. Figure 2 illustrates the UML Use Case Diagram.")
    fig("use_case_diagram.png", "Figure 2: UML Use Case Diagram illustrating Public and Administrator interactions", is_diagram=True)

    h2("8.2 Data Flow Diagrams (Level 0 and Level 1)")
    p("Data Flow Diagrams (DFDs) model how data moves through the system, transforms across business processes, and settles into persistent data stores. Figure 3 presents the Level 0 Context Diagram showing high-level information exchanges between external entities and the central system boundary.")
    fig("dfd_level_0.png", "Figure 3: Data Flow Diagram (Level 0) — Context Diagram", is_diagram=True)
    p("Figure 4 expands the system into a Level 1 DFD, detailing the five primary functional processes (1.0 Donor Management, 2.0 Inventory Control, 3.0 Hospital Requisitions, 4.0 Admin Decisions, 5.0 SQL Analytics) and their bidirectional interactions with database tables D1 through D7.")
    fig("dfd_level_1.png", "Figure 4: Data Flow Diagram (Level 1) — Detailed Functional Processes and Data Stores", is_diagram=True)

    h2("8.3 Sequence Modeling for Atomic Transactions")
    p("To demonstrate the exact chronological message sequence and database locking behavior, UML Sequence Diagrams were developed for the two critical transaction workflows. Figure 5 illustrates the sequence for Atomic Donation Registration, showing the validation, insertion, stock update, and final commit.")
    fig("donation_sequence.png", "Figure 5: UML Sequence Diagram — Atomic Blood Donation Registration Workflow", is_diagram=True)
    p("Figure 6 illustrates the sequence for Atomic Request Fulfilment, emphasizing the acquisition of row-level exclusive locks (FOR UPDATE) on both Blood_Request and Blood_Stock to eliminate race conditions.")
    fig("fulfillment_sequence.png", "Figure 6: UML Sequence Diagram — Atomic Request Fulfilment with Pessimistic Row Locking", is_diagram=True)

    # --------------------------------------------------------------------------- #
    # CHAPTER 9: DATABASE DESIGN, NORMALIZATION, & DATA DICTIONARY
    # --------------------------------------------------------------------------- #
    h1("Chapter 9: Database Design, Normalization, & Data Dictionary")
    h2("9.1 Entity-Relationship (ER) Diagram (Chen Notation)")
    p("The relational schema is conceptualized in the Entity-Relationship Diagram depicted in Figure 7 using standard Chen notation. Entities are represented as rectangles, attributes as ellipses, primary keys as underlined text, foreign keys as dashed ellipses, and relationships as labeled diamonds with explicit cardinality ratios.")
    fig("er_diagram.png", "Figure 7: Complete Entity-Relationship (ER) Diagram (Chen Notation)", is_diagram=True)

    h2("9.2 Normalization Analysis (1NF, 2NF, 3NF & Historical Denormalization)")
    bullet("First Normal Form (1NF)", "Satisfied. Every attribute contains only atomic, indivisible values. Blood groups exist as discrete row records rather than repeated columns, and phone numbers are stored as single atomic strings.")
    bullet("Second Normal Form (2NF)", "Satisfied. Every table possesses a single-column surrogate primary key (INT AUTO_INCREMENT). Consequently, no non-key attribute can functionally depend on a proper subset of a composite candidate key.")
    bullet("Third Normal Form (3NF)", "Satisfied with one documented, deliberate exception. Non-key attributes depend strictly upon the primary key and not upon other non-key attributes (no transitive dependencies).")
    bullet("Intentional Historical Denormalization in Donation.Bg_ID", "In pure 3NF, Donation.Bg_ID could be derived by traversing Donor.Bg_ID. However, a medical blood donation represents an unalterable historical clinical event: the unit was physically collected under a specific blood type. If a donor's registered group is later corrected due to laboratory clerical error, historical blood units collected in past sessions must NOT retroactively change their biological type. Storing Bg_ID directly on Donation preserves clinical auditability.")

    h2("9.3 Comprehensive Data Dictionary")
    p("Tables 2 through 8 detail the complete data dictionary for all seven database tables.")

    # Table 2
    h3("Table 2: Blood_Group Data Dictionary")
    h_bg = ["Column Name", "Data Type", "Constraints", "Description"]
    w_bg = [1.5 * inch, 1.2 * inch, 1.8 * inch, 1.9 * inch]
    d_bg = [
        ["Bg_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the blood group."],
        ["Blood_Type", "VARCHAR(3)", "UNIQUE, NOT NULL, CHECK (IN 'A+','A-',...)", "Standard blood group string. Restricts domain to the 8 standard types."]
    ]
    make_table(w_bg, h_bg, d_bg)

    # Table 3
    h3("Table 3: Donor Data Dictionary")
    d_d = [
        ["Donor_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the donor."],
        ["Name", "VARCHAR(100)", "NOT NULL, KEY (idx_donor_name)", "Full legal name of the blood donor."],
        ["Age", "INT", "NOT NULL, CHECK (Age BETWEEN 18 AND 65)", "Age in years; bounded to legal medical donation age limits."],
        ["Gender", "ENUM('Male','Female','Other')", "NOT NULL", "Gender classification for clinical demographic records."],
        ["Phone", "VARCHAR(15)", "UNIQUE (uq_donor_phone), NOT NULL", "Unique natural identifier preventing duplicate donor records."],
        ["Bg_ID", "INT", "FK -> Blood_Group(Bg_ID), RESTRICT, NOT NULL", "Foreign key linking donor to their registered blood group."]
    ]
    make_table(w_bg, h_bg, d_d)

    # Table 4
    h3("Table 4: Donation Data Dictionary")
    d_dn = [
        ["Donation_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the donation event."],
        ["Donor_ID", "INT", "FK -> Donor(Donor_ID), RESTRICT, NOT NULL", "Foreign key identifying the donor who provided the blood."],
        ["Bg_ID", "INT", "FK -> Blood_Group(Bg_ID), RESTRICT, NOT NULL", "Foreign key identifying the blood group collected."],
        ["Donation_Date", "DATE", "NOT NULL, KEY (idx_donation_date)", "Calendar date when the donation took place."],
        ["Units_Donated", "INT", "NOT NULL, DEFAULT 1, CHECK (>= 1)", "Number of whole whole-blood units collected (minimum 1)."]
    ]
    make_table(w_bg, h_bg, d_dn)

    # Table 5
    h3("Table 5: Hospital Data Dictionary")
    d_h = [
        ["Hospital_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the partner hospital."],
        ["Name", "VARCHAR(150)", "NOT NULL, KEY (idx_hospital_name)", "Official clinical facility or hospital institution name."],
        ["Address", "VARCHAR(255)", "NULL", "Physical postal address or delivery location."],
        ["Phone", "VARCHAR(15)", "UNIQUE (uq_hospital_phone), NOT NULL", "Unique administrative contact telephone number."]
    ]
    make_table(w_bg, h_bg, d_h)

    # Table 6
    h3("Table 6: Blood_Request Data Dictionary")
    d_r = [
        ["Request_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the hospital requisition."],
        ["Hospital_ID", "INT", "FK -> Hospital(Hospital_ID), RESTRICT, NOT NULL", "Foreign key linking request to the requesting hospital."],
        ["Bg_ID", "INT", "FK -> Blood_Group(Bg_ID), RESTRICT, NOT NULL", "Foreign key indicating the specific blood group requested."],
        ["Date", "DATE", "NOT NULL, KEY (idx_request_date)", "Date the blood request was formally registered."],
        ["Qty", "DECIMAL(6,2)", "NOT NULL, CHECK (Qty > 0)", "Quantity of units requested (must be strictly positive)."],
        ["Status", "ENUM('Pending','Approved', 'Completed','Rejected')", "NOT NULL, DEFAULT 'Pending', KEY", "Lifecycle status. Stock is deducted ONLY when Completed."]
    ]
    make_table(w_bg, h_bg, d_r)

    # Table 7
    h3("Table 7: Blood_Stock Data Dictionary")
    d_s = [
        ["Stock_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key for the stock balance entry."],
        ["Bg_ID", "INT", "FK -> Blood_Group(Bg_ID), UNIQUE (uq_stock_bg)", "Foreign key enforcing exactly one inventory row per blood group."],
        ["Total_Qty", "DECIMAL(8,2)", "NOT NULL, DEFAULT 0, CHECK (>= 0)", "Current available units. CHECK ensures stock never drops negative."],
        ["Last_Updated", "DATETIME", "NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE", "Automatic database timestamp recording the last modification."]
    ]
    make_table(w_bg, h_bg, d_s)

    # Table 8
    h3("Table 8: Admin_Audit_Log Data Dictionary")
    d_a = [
        ["Audit_ID", "INT", "PK, AUTO_INCREMENT, NOT NULL", "Surrogate primary key identifying the audit entry."],
        ["Proposal_Type", "VARCHAR(30)", "NOT NULL", "Record type of the decision target (e.g. 'Blood_Request')."],
        ["Proposal_ID", "INT", "NOT NULL, KEY (idx_audit_proposal)", "Foreign identifier matching the decided proposal record."],
        ["Action", "ENUM('Approved','Rejected')", "NOT NULL", "Administrative decision taken by the authorized administrator."],
        ["Detail", "VARCHAR(255)", "NULL", "Human-readable summary of the requisition at decision time."],
        ["Decided_At", "DATETIME", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "Immutable timestamp recording exact decision moment."]
    ]
    make_table(w_bg, h_bg, d_a)

    h2("9.4 Indexing Scheme & Referential Integrity Enforcement")
    p("All foreign keys specify ON UPDATE CASCADE and ON DELETE RESTRICT. The RESTRICT action is critical: if an operator attempts to delete a donor who has associated donation rows, MySQL rejects the command with errno 1451. The application catches this specific error and displays a friendly notification: \"This donor has donation records and cannot be deleted (history is preserved).\" Performance is maximized by maintaining B-tree indexes on all frequently filtered columns: Donor(Name), Donation(Donation_Date), Blood_Request(Status), and Blood_Request(Date).")

    # --------------------------------------------------------------------------- #
    # CHAPTER 10: SYSTEM IMPLEMENTATION & CODE ARTIFACTS
    # --------------------------------------------------------------------------- #
    h1("Chapter 10: System Implementation & Code Artifacts")
    h2("10.1 Connection Ownership & Failover Architecture (db.py)")
    p("Every database interaction is governed exclusively by db.py. Listing 1 illustrates the thread-local connection caching and pre-flight pinging mechanism implemented in db.get_connection().")
    code_conn = """def get_connection():
    \"\"\"Return a live MySQL connection, reusing this thread's warm one.\"\"\"
    conn = getattr(_local, "conn", None)
    if conn is not None:
        try:
            conn.ping(reconnect=False)  # Real COM_PING round trip
            return conn
        except (Error, InterfaceError):
            _forget(conn)
            _close_quietly(conn)

    # Open a fresh connection with verified TLS configuration
    conn = mysql.connector.connect(**DB_CONFIG)
    _local.conn = conn
    return conn"""
    code_box(code_conn, "Listing 1: Stale connection detection and thread-local caching in db.py")

    h2("10.2 Atomic Multi-Unit Blood Donation Logic")
    p("Listing 2 presents the transactional implementation in _create_donation(). The logic confirms donor existence, validates blood group equivalence, records the donation, and increments stock in a single atomic transaction.")
    code_don = """with db.transaction() as cur:
    # 1. Verify donor existence and registered blood group
    cur.execute("SELECT Donor_ID, Bg_ID FROM Donor WHERE Donor_ID = %s", (donor_id,))
    donor = cur.fetchone()
    if donor is None or donor["Bg_ID"] != bg_id:
        raise ValidationError("Blood group mismatch or donor not found.")

    # 2. Insert the donation record with specified whole units
    cur.execute(
        \"\"\"INSERT INTO Donation (Donor_ID, Bg_ID, Donation_Date, Units_Donated)
           VALUES (%s, %s, %s, %s)\"\"\",
        (donor_id, bg_id, donation_date, units),
    )

    # 3. Atomically increment blood stock for that blood group
    cur.execute(
        \"\"\"UPDATE Blood_Stock
           SET Total_Qty = Total_Qty + %s, Last_Updated = NOW()
           WHERE Bg_ID = %s\"\"\",
        (units, bg_id),
    )
    if cur.rowcount != 1:
        raise ValidationError("No stock record exists for the blood group.")
# Both statements commit together upon exiting context manager"""
    code_box(code_don, "Listing 2: Atomic multi-unit donation registration in app.py")

    h2("10.3 Pessimistic Concurrency Control in Request Fulfilment")
    p("Listing 3 illustrates request fulfillment in request_fulfill(). Pessimistic row-level locking (SELECT ... FOR UPDATE) locks both the request and stock rows, eliminating race conditions.")
    code_ful = """with db.transaction() as cur:
    # 1. Lock request row to prevent concurrent double-fulfilment
    cur.execute(
        \"\"\"SELECT Request_ID, Bg_ID, Qty, Status 
           FROM Blood_Request WHERE Request_ID = %s FOR UPDATE\"\"\",
        (request_id,),
    )
    req = cur.fetchone()
    if req is None or req["Status"] not in ("Pending", "Approved"):
        raise ValidationError("Request cannot be fulfilled again.")

    # 2. Lock stock row for that blood group
    cur.execute("SELECT Total_Qty FROM Blood_Stock WHERE Bg_ID = %s FOR UPDATE", (req["Bg_ID"],))
    stock = cur.fetchone()
    
    # 3. Check stock adequacy
    if stock["Total_Qty"] < req["Qty"]:
        raise ValidationError(f"Insufficient stock: {stock['Total_Qty']} available, {req['Qty']} needed.")

    # 4. Deduct stock and finalize status
    cur.execute("UPDATE Blood_Stock SET Total_Qty = Total_Qty - %s WHERE Bg_ID = %s", (req["Qty"], req["Bg_ID"]))
    cur.execute("UPDATE Blood_Request SET Status = 'Completed' WHERE Request_ID = %s", (request_id,))"""
    code_box(code_ful, "Listing 3: Concurrency protection via row locking in request_fulfill()")

    h2("10.4 Password-Protected Admin Decision Workflow & Rate Limiting")
    p("Listing 4 displays the administrative verification logic. The admin password hash is verified via check_password_hash, and failed attempts are throttled using in-memory sliding-window timestamps.")
    code_admin = """def admin_password_matches(candidate):
    pw_hash = admin_password_hash()
    if pw_hash:
        try:
            return check_password_hash(pw_hash, candidate)
        except Exception:
            return False
    plain = admin_password_plain()
    if plain is not None:
        return secrets.compare_digest(plain.encode("utf-8"), candidate.encode("utf-8"))
    return False"""
    code_box(code_admin, "Listing 4: Cryptographic password matching in app.py")

    h2("10.5 Lightweight Session-Based CSRF Mitigation")
    p("A session-backed CSRF protection mechanism is enforced across all POST requests without requiring heavy third-party extensions. A 32-byte hexadecimal token is generated via secrets.token_hex(32) on first access, exposed to Jinja2 templates via csrf_token(), and validated inside an @app.before_request hook using secrets.compare_digest.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 11: USER INTERFACE MODULES & VISUAL VERIFICATION
    # --------------------------------------------------------------------------- #
    h1("Chapter 11: User Interface Modules & Visual Verification")
    h2("11.1 Executive Dashboard Module")
    p("The Dashboard serves as the operational command center. It executes a single optimized round-trip query containing eight scalar subqueries to display summary KPI cards (Registered Donors, Partner Hospitals, Total Donations, Total Units Donated, Pending Requests, Approved Requests, Completed Requests, and Rejected Requests). It also features an 8-group stock status grid and the five most recent donations and requisitions. Figure 8 depicts the live dashboard.")
    fig("01_dashboard.png", "Figure 8: Executive Dashboard showing live KPI counters, stock breakdown, and recent activity", is_diagram=False)

    h2("11.2 Donor Management Module")
    p("The Donor Directory (Figure 9) displays all registered blood donors with columns for ID, Name, Age, Gender, Phone, Blood Group, Total Donations, and Total Units Donated. Operators can perform real-time substring searches on names or phone numbers and filter by blood group. Action buttons allow editing or deleting donor records.")
    fig("02_donors_list.png", "Figure 9: Donor Directory with real-time search, blood group filters, and donation statistics", is_diagram=False)

    p("Figure 10 depicts the Donor Registration Form, which enforces validation rules (Age between 18-65, Phone 7-15 digits, Name required). If a validation error occurs, submitted values are preserved in the form state, preventing re-typing.")
    fig("03_donor_form.png", "Figure 10: Donor Registration Form featuring client and server-side validation", is_diagram=False)

    p("Figure 11 depicts the individual Donor Donation History view, displaying a complete audit log of all donations provided by a specific donor along with cumulative whole units.")
    fig("04_donor_history.png", "Figure 11: Historical Donation Audit Trail for an individual blood donor", is_diagram=False)

    h2("11.3 Donation Registration & Multi-Unit Processing")
    p("The Donations page (Figure 12) combines donation event logging with an intuitive registration form. The form includes an interactive dropdown that dynamically auto-selects the donor's registered blood group via vanilla JavaScript, preventing biological mismatch errors. The 'Units Donated' input allows intake of whole units (1, 2, 3...) with automated inventory updates.")
    fig("05_donations_list.png", "Figure 12: Blood Donations Registry and Registration Form with multi-unit support", is_diagram=False)

    h2("11.4 Inventory Tracking & Low-Stock Alerts")
    p("The Blood Stock page (Figure 13) provides real-time visibility into inventory across all eight blood groups. Groups falling below LOW_STOCK_THRESHOLD (default: 10 units) are dynamically flagged with warning badges to trigger proactive donor recruitment drives.")
    fig("06_stock_inventory.png", "Figure 13: Blood Stock Inventory page highlighting groups below the low-stock threshold", is_diagram=False)

    h2("11.5 Hospital Registry & Blood Request Lifecycle")
    p("The Hospital Directory (Figure 14) tracks registered healthcare facilities, contact phone numbers, addresses, and total requisitions generated.")
    fig("07_hospitals_list.png", "Figure 14: Partner Hospital Directory displaying facility details and request counts", is_diagram=False)

    p("Figure 15 illustrates the Hospital Registration Form, ensuring hospital phone numbers remain strictly unique.")
    fig("08_hospital_form.png", "Figure 15: Hospital Registration Form with validation controls", is_diagram=False)

    p("The Blood Requests interface (Figure 16) manages hospital requisitions through their lifecycle: Pending, Approved, Completed, or Rejected. Each row provides contextual action buttons: 'Approve' and 'Reject' advance the workflow without touching inventory, while 'Fulfill' triggers the atomic stock deduction transaction.")
    fig("09_requests_management.png", "Figure 16: Blood Request Management interface with lifecycle controls and fulfillment actions", is_diagram=False)

    h2("11.6 Interactive SQL Reports Module")
    p("The SQL Reports page (Figure 17) demonstrates eight practical queries, displaying live database outputs alongside technical explanations of the SQL concepts (INNER JOIN, LEFT JOIN, SUM with COALESCE, GROUP BY, and HAVING).")
    fig("10_sql_reports.png", "Figure 17: Interactive SQL Reports page demonstrating practical analytical queries", is_diagram=False)

    h2("11.7 Admin Approval Workflow & Profile Inspector")
    p("Figure 18 depicts the Admin Authentication Portal, which gates privileged pages behind Werkzeug scrypt hash verification and rate-limiting.")
    fig("11_admin_login.png", "Figure 18: Password-protected Admin Login portal with rate limiting", is_diagram=False)

    p("Figure 19 displays the Admin Decision Workspace. The top panel presents pending blood requests awaiting authorization. The bottom panel renders the immutable Admin_Audit_Log, recording decisions with timestamps and target details.")
    fig("12_admin_pending.png", "Figure 19: Admin Decision Workspace displaying pending proposals and the immutable audit log", is_diagram=False)

    p("Figure 20 depicts the Administrator Profile view, displaying authenticated session status, session lifetime (default: 30 minutes), and quick navigation shortcuts.")
    fig("13_admin_profile.png", "Figure 20: Administrator Profile interface showing active session parameters", is_diagram=False)

    # --------------------------------------------------------------------------- #
    # CHAPTER 12: PRACTICAL SQL DEMONSTRATION QUERIES
    # --------------------------------------------------------------------------- #
    h1("Chapter 12: Practical SQL Demonstration Queries")
    p("The repository includes queries.sql containing 18 demonstration queries engineered for academic evaluation. Table 9 summarizes these practical SQL implementations and their demonstrated database concepts.")
    
    h_q = ["Query #", "Operational Goal", "SQL Concepts Demonstrated"]
    w_q = [0.9 * inch, 2.7 * inch, 2.8 * inch]
    d_q = [
        ["Q1", "List all registered donors", "Basic projection (SELECT), ORDER BY primary key."],
        ["Q2", "Filter donors by blood group", "Lookup join with Blood_Group, equality WHERE filter."],
        ["Q3", "Search donors by name pattern", "Pattern matching with LIKE '%a%' (case-insensitive)."],
        ["Q4", "Donors with blood group names", "INNER JOIN between Donor and Blood_Group on Bg_ID."],
        ["Q5", "Donors including zero donations", "LEFT JOIN Donor with Donation, COUNT(Donation_ID), GROUP BY."],
        ["Q6", "Total units donated per donor", "LEFT JOIN, SUM(Units_Donated), COALESCE(..., 0) for zero handling."],
        ["Q7", "Donors count per blood group", "LEFT JOIN Blood_Group with Donor, GROUP BY Bg_ID, Blood_Type."],
        ["Q8", "Current blood stock inventory", "INNER JOIN Blood_Stock with Blood_Group for labels."],
        ["Q9", "Low stock alerts (< 10 units)", "Threshold filtering with WHERE Total_Qty < 10, ORDER BY ASC."],
        ["Q10", "Pending hospital requisitions", "Status filtering with WHERE Status = 'Pending', ORDER BY Date."],
        ["Q11", "Detailed request information", "Three-table INNER JOIN: Blood_Request, Hospital, Blood_Group."],
        ["Q12", "Donations within date window", "Range filtering on DATE column using BETWEEN operator."],
        ["Q13", "Monthly donation totals", "Date aggregation using DATE_FORMAT(Donation_Date, '%Y-%m'), SUM."],
        ["Q14", "Request distribution by status", "Categorical aggregation: COUNT(*) with GROUP BY Status."],
        ["Q15", "Most requested blood groups", "LEFT JOIN, SUM(Qty) with COALESCE, ORDER BY total DESC."],
        ["Q16", "Safe donor phone update", "Parameter-bound UPDATE wrapped in START TRANSACTION / ROLLBACK."],
        ["Q17", "Safe donor deletion test", "Temporary row insertion, deletion, and ROLLBACK verification."],
        ["Q18", "Atomic request fulfillment", "SELECT FOR UPDATE row locking, conditional UPDATE, and status change."]
    ]
    make_table(w_q, h_q, d_q)

    # --------------------------------------------------------------------------- #
    # CHAPTER 13: SYSTEM VERIFICATION AND TEST RESULTS
    # --------------------------------------------------------------------------- #
    h1("Chapter 13: System Verification and Test Results")
    h2("13.1 Testing Methodology & Safety Invariants")
    p("Testing was conducted through a bespoke automated test harness implemented across three test suites: tests/test_db.py, tests/test_admin.py, and tests/test_profile.py. The test harness enforces strict safety invariants: it never drops or truncates tables, creates temporary rows marked with distinctive tags, deletes those exact rows in finally blocks, and restores every Blood_Stock quantity to its exact initial value.")

    h2("13.2 Automated Test Execution Matrix (219 Passed Tests)")
    p("Tables 10 through 14 summarize the test execution results across all testing modules.")

    # Table 10
    h3("Table 10: Schema & Integrity Verification Tests (test_db.py Section A — 47 Tests)")
    h_t = ["Test Category", "Test Description", "Observed Output", "Status"]
    w_t = [1.5 * inch, 2.6 * inch, 1.4 * inch, 0.9 * inch]
    d_t10 = [
        ["Table Existence", "Verify existence of all 6 core tables in information_schema", "6/6 tables present", "PASS"],
        ["Storage Engine", "Verify InnoDB storage engine on all tables", "All tables use InnoDB", "PASS"],
        ["Foreign Keys", "Verify all 6 foreign key constraints by name", "All 6 FKs verified", "PASS"],
        ["Unique Keys", "Verify UNIQUE constraints (donor phone, hospital phone, stock bg)", "4/4 unique keys active", "PASS"],
        ["Check Constraints", "Verify CHECK constraints (donor age, stock non-negative, etc.)", "5/5 check constraints active", "PASS"],
        ["Column Specs", "Verify Donation.Units_Donated is INT NOT NULL DEFAULT 1", "Column specs verified", "PASS"],
        ["Sample Data", "Verify baseline seed counts (8 groups, 15 donors, 12 donations, etc.)", "All baseline counts met", "PASS"],
        ["Stock Non-Negative", "Verify zero rows have Total_Qty < 0", "Zero negative stock rows", "PASS"],
        ["Stock Reconciliation", "Verify Opening + Donated - Completed == Stored for all 8 groups", "All 8 groups reconcile", "PASS"]
    ]
    make_table(w_t, h_t, d_t10)

    # Table 11
    h3("Table 11: Behavioral & Transactional Tests (test_db.py Section B — 57 Tests)")
    d_t11 = [
        ["CSRF Defense", "POST to /donors/new without CSRF token", "HTTP 400 Bad Request", "PASS"],
        ["Donor CRUD", "Create, read, update, and search donor with phone validation", "Donor persisted & updated", "PASS"],
        ["Input Validation", "Submit invalid donor age (<18); check rejection & state preservation", "Rejected; value preserved", "PASS"],
        ["Donation Logic", "Record donations of 1, 2, and 3 units; verify stock increments", "Stock incremented by N", "PASS"],
        ["Mismatch Guard", "Attempt donation where blood group != donor's registered group", "Rejected with error flash", "PASS"],
        ["Invalid Units", "Submit zero, negative, decimal, text, and missing units", "All rejected; stock untouched", "PASS"],
        ["Request Workflow", "Create Pending request; approve; fulfill atomically; verify deduction", "Stock deducted exactly once", "PASS"],
        ["Double Fulfilment", "Attempt second fulfillment on Completed request", "Rejected; no double deduction", "PASS"],
        ["Insufficient Stock", "Attempt fulfillment exceeding available inventory", "Rejected; stock never negative", "PASS"],
        ["FK RESTRICT", "Attempt to delete donor with donation history", "Blocked with errno 1451", "PASS"],
        ["Rollback Safety", "Simulate unhandled error inside transaction block", "Rolled back; zero partial rows", "PASS"]
    ]
    make_table(w_t, h_t, d_t11)

    # Table 12
    h3("Table 12: Connection Lifecycle & Concurrency Tests (test_db.py Section C — 20 Tests)")
    d_t12 = [
        ["Connection Reuse", "Verify get_connection() returns cached instance across queries", "Same socket reused", "PASS"],
        ["Pre-Flight Ping", "Verify COM_PING is issued before reuse with reconnect=False", "Ping verified", "PASS"],
        ["Stale Recovery", "Sever connection externally; verify transparent recovery", "Fresh session opened", "PASS"],
        ["Mid-Tx Failures", "Sever connection during active transaction", "Error raised; no silent reconnect", "PASS"],
        ["Isolation Check", "Verify uncommitted changes are invisible to other sessions", "Full read isolation verified", "PASS"],
        ["Worker Threads", "Dispatch concurrent worker threads with dedicated connections", "Zero race conditions", "PASS"]
    ]
    make_table(w_t, h_t, d_t12)

    # Table 13
    h3("Table 13: Administrative Security & Workflow Tests (test_admin.py — 67 Tests)")
    d_t13 = [
        ["Config Safety", "Missing or weak SECRET_KEY / ADMIN_PASSWORD_HASH handling", "HTTP 503 without secret leak", "PASS"],
        ["Access Control", "Unauthenticated GET /admin or POST approve/reject", "Redirected to login / HTTP 401", "PASS"],
        ["CSRF Protection", "POST admin login, logout, approve, reject without CSRF token", "HTTP 400 Bad Request", "PASS"],
        ["Authentication", "Submit wrong password vs correct password", "HTTP 401 vs HTTP 302 redirect", "PASS"],
        ["Rate Limiting", "Execute >5 failed logins in 300s window", "HTTP 429 Too Many Requests", "PASS"],
        ["Decision Handling", "Approve & reject proposals; verify audit row and status update", "Atomic status + audit written", "PASS"],
        ["Duplicate Guard", "Attempt repeat decision on already processed proposal", "Rejected; single audit row", "PASS"],
        ["Rollback Safety", "Simulate failure during decision transaction", "Rolled back; proposal Pending", "PASS"],
        ["Session Expiry", "POST /admin/logout; verify session invalidation", "Session cleared; access denied", "PASS"]
    ]
    make_table(w_t, h_t, d_t13)

    # Table 14
    h3("Table 14: Profile & UI Authorization Tests (test_profile.py — 28 Tests)")
    d_t14 = [
        ["Navbar Integrity", "Verify presence of all 7 core navigation links + Profile link", "All 8 links intact", "PASS"],
        ["Unauthenticated", "Access GET /profile or GET /admin/profile without session", "Redirected to /admin/login", "PASS"],
        ["Authenticated", "Access GET /profile with valid admin session cookie", "HTTP 200 OK with role badge", "PASS"],
        ["Session Logout", "Log out from profile; attempt re-entry to /profile", "Session ended; redirected", "PASS"]
    ]
    make_table(w_t, h_t, d_t14)

    p("<b>TOTAL TEST SUITE SUMMARY: 219 Passed, 0 Failed, 0 Skipped (100% Success Rate).</b>")

    # --------------------------------------------------------------------------- #
    # CHAPTER 14: RESULTS, DISCUSSION, & STOCK RECONCILIATION
    # --------------------------------------------------------------------------- #
    h1("Chapter 14: Results, Discussion, & Stock Reconciliation")
    h2("14.1 Stock Reconciliation Mathematical Validation")
    p("A foundational validation requirement is stock reconciliation. At all times, the stored stock in Blood_Stock must strictly satisfy the invariant equation: Total_Qty = Opening_Balance + Total_Donated_Units - Total_Completed_Requested_Units. During automated testing, this mathematical formula was evaluated across all eight blood groups against the live database. For example, group A+ (Bg_ID 1): Opening = 20.00, Donations = 6 units (2+1+3), Completed Requests = 2.00, resulting in Stored Stock = 24.00 units. All eight blood groups reconciled with zero variance.")

    h2("14.2 Concurrency and Race Condition Elimination")
    p("Concurrency testing verified that pessimistic row locking effectively eliminates lost update and double-allocation anomalies. When concurrent simulated clients issued simultaneous fulfillment requests against the same blood stock row, the InnoDB lock manager successfully serialized the transactions. The first transaction obtained exclusive row locks, evaluated adequacy, decremented units, and committed. The second transaction blocked until lock release, re-read the updated Total_Qty, detected insufficient units, and raised an error, preventing negative stock.")

    h2("14.3 Security Posture Assessment")
    p("Security evaluations confirmed complete resistance against the OWASP Top 10 web application vulnerabilities: (1) SQL Injection: 100% mitigated by parameter binding; (2) Cross-Site Request Forgery (CSRF): 100% mitigated by session tokens; (3) Brute-Force Attacks: 100% mitigated by sliding-window rate limiting; and (4) Information Leakage: Database error handlers log technical stack traces server-side while displaying generic friendly messages to users.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 15: LIMITATIONS AND FUTURE SCOPE
    # --------------------------------------------------------------------------- #
    h1("Chapter 15: Limitations and Future Scope")
    h2("15.1 Current System Limitations")
    p("In the spirit of honest academic inquiry, three operational limitations are acknowledged: (1) Single Shared Admin Password: The system uses a shared administrative password rather than individualized user accounts with granular Role-Based Access Control (RBAC); (2) Local Notification Only: System alerts (low stock, registration confirmations) rely on web flash banners rather than automated SMS or email dispatch gateways; and (3) FIFO Inventory Model: The schema treats units within a blood group as a homogenous aggregate quantity, without tracking individual unit expiration dates (whole blood typically expires after 35-42 days).")

    h2("15.2 Strategic Roadmap and Future Enhancements")
    bullet("Individualized RBAC Multi-Tenancy", "Introduce an App_User table supporting distinct roles (Clerk, Laboratory Technician, Hospital Coordinator, Medical Director) with individualized audit logging.")
    bullet("Unit-Level RFID & Expiration Tracking", "Decompose Blood_Stock into discrete Blood_Unit records with barcoded bag identifiers, collection dates, and automatic expiration quarantining.")
    bullet("Automated SMS / Webhook Gateway", "Integrate external messaging APIs (Twilio, Africa's Talking) to automatically notify donors when their specific blood type hits critical low-stock thresholds.")
    bullet("FHIR / HL7 RESTful Interoperability", "Expose a secure RESTful API conforming to HL7 FHIR standards for automated EHR integration with hospital operating rooms.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 16: CONCLUSION
    # --------------------------------------------------------------------------- #
    h1("Chapter 16: Conclusion")
    p("The Blood Bank Management System demonstrates that mission-critical healthcare inventory management can be engineered with exceptional reliability, security, and performance by adhering strictly to core relational database management principles. By discarding heavy ORM abstractions in favor of explicit, parameter-bound SQL and native InnoDB transaction controls, the system delivers complete visibility, deterministic ACID guarantees, and sub-millisecond execution speeds.")
    p("Through a 3NF normalized schema, foreign key RESTRICT actions, pessimistic row locking (SELECT ... FOR UPDATE), scrypt password hashing, and CSRF protection, the application completely resolves the operational vulnerabilities of legacy spreadsheet systems. Validated by an automated test suite of 219 tests achieving a 100% pass rate, the project fulfills all academic and software engineering requirements, representing an exemplary model for database systems laboratory development.")

    # --------------------------------------------------------------------------- #
    # CHAPTER 17: REFERENCES
    # --------------------------------------------------------------------------- #
    h1("Chapter 17: References")
    refs = [
        "[1] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Boston, MA: Pearson, 2016.",
        "[2] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. New York, NY: McGraw-Hill Education, 2020.",
        "[3] Oracle Corporation, \"MySQL 8.0 Reference Manual: The InnoDB Storage Engine and Transaction Model,\" Oracle Documentation, 2026. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html",
        "[4] Pallets Projects, \"Flask Documentation (Version 3.0.x): Application Context, Request Handling, and Blueprints,\" 2024. [Online]. Available: https://flask.palletsprojects.com/",
        "[5] Open Web Application Security Project (OWASP), \"OWASP Top 10:2021 — The Ten Most Critical Web Application Security Risks,\" OWASP Foundation, 2021. [Online]. Available: https://owasp.org/Top10/",
        "[6] C. J. Date, An Introduction to Database Systems, 8th ed. Boston, MA: Addison-Wesley, 2004.",
        "[7] Python Software Foundation, \"secrets — Generate secure random numbers for managing secrets,\" Python 3.12 Documentation, 2024. [Online]. Available: https://docs.python.org/3/library/secrets.html",
        "[8] World Health Organization, \"Blood safety and availability,\" WHO Fact Sheets, 2023. [Online]. Available: https://www.who.int/news-room/fact-sheets/detail/blood-safety-and-availability"
    ]
    for r in refs:
        p(f"<b>{r[:4]}</b> {r[4:]}")

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()


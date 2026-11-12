# Blood Bank Management System — Academic Project Report

**Project Title:** Blood Bank Management System (BBMS)  
**Course:** Database Management Systems Laboratory (CSE / SWE)  
**Author:** Sanim Khan (`sanim-ctrl`)  
**Repository:** [https://github.com/sanim-ctrl/dbms_Lab_project](https://github.com/sanim-ctrl/dbms_Lab_project)  
**Date of Generation:** November 2026  
**Document Format:** University Standard Academic Technical Report  

---

## 1. Executive Summary & Deliverables

This repository contains the complete, official, university-standard academic project report for the **Blood Bank Management System (BBMS)**. The report is authored based strictly on the actual codebase implementation, database schemas (`schema.sql`, `seed.sql`, `admin_schema.sql`), Python Flask backend services (`app.py`, `db.py`), templates, and live test executions (219 passing unit and integration tests).

### Deliverables Directory Structure

```text
Project_Report/
│
├── Project_Report.docx         # Complete editable academic report (27 sections, 20 figures, 14 tables)
├── Project_Report.pdf          # Final submission-ready publication PDF (45 pages, two-pass numbering)
├── README.md                   # This documentation, build guide, and architectural reference
│
├── Project_Diagrams/           # High-resolution architectural, flow, and schema diagrams (7 files)
│   ├── system_architecture.png     # Figure 1: 3-Tier Layered System Architecture
│   ├── use_case_diagram.png        # Figure 2: UML Actor-Boundary Use Case Model
│   ├── dfd_level_0.png             # Figure 3: Context Analysis Diagram (DFD Level 0)
│   ├── dfd_level_1.png             # Figure 4: Decomposed Functional Process Diagram (DFD Level 1)
│   ├── er_diagram.png              # Figure 5: Complete Chen & Relational ER Schema
│   ├── donation_sequence.png       # Figure 6: UML Sequence Diagram: Blood Intake & Stock Invariant
│   └── fulfillment_sequence.png    # Figure 7: UML Sequence Diagram: ACID Atomic Requisition Fulfillment
│
├── Project_Screenshots/        # Authentic captured user interface screens from live app (13 files)
│   ├── 01_dashboard.png            # Figure 8: Executive Real-Time Analytical KPI Dashboard
│   ├── 02_donors_list.png          # Figure 9: Donor Roster with Search, Blood Group & City Filters
│   ├── 03_donor_form.png           # Figure 10: Donor Registration & Eligibility Form
│   ├── 04_donor_history.png        # Figure 11: Longitudinal Donor Contribution & Audit Trail
│   ├── 05_donations_list.png       # Figure 12: Blood Donation Intake Ledger
│   ├── 06_stock_inventory.png      # Figure 13: Live Inventory Balancing Table with Safety Indicators
│   ├── 07_hospitals_list.png       # Figure 14: Healthcare Provider Directory & Emergency Hotlines
│   ├── 08_hospital_form.png        # Figure 15: Partner Healthcare Facility Registration Interface
│   ├── 09_requests_management.png  # Figure 16: Emergency Requisition Fulfillment & Allocation Console
│   ├── 10_sql_reports.png          # Figure 17: Administrative SQL Intelligence & Aggregate Analytics
│   ├── 11_admin_login.png          # Figure 18: Admin Gatekeeper Authentication & Access Control
│   ├── 12_admin_pending.png        # Figure 19: Dual-Authorization Pending Administrator Approvals
│   └── 13_admin_profile.png        # Figure 20: Administrator Profile, Session Security & Credential Management
│
├── report_builder_core.py      # Core document formatting engine for DOCX typography and tables
├── pdf_canvas_core.py          # ReportLab custom canvas with running headers and dynamic total pages
├── generate_diagrams.py        # Automated diagram rendering engine (matplotlib & Pillow)
├── take_screenshots.py         # Automated UI screen capture test harness
├── generate_final_docx.py      # Complete 27-section DOCX compiler script
└── generate_final_pdf.py       # Complete 27-section ReportLab PDF compiler script
```

---

## 2. Report Structure & Academic Table of Contents

The report strictly adheres to university project documentation standards and covers all **27 academic sections**:

1. **Cover Page**: Project Title, Course Code, Student Credentials, Submission Metadata.
2. **Declaration**: Academic integrity affirmation and original work statement.
3. **Acknowledgement**: Academic recognition of lab instructors, faculty, and peer collaborators.
4. **Abstract**: Comprehensive 300-word synopsis of problem context, technical methodology, and empirical findings.
5. **Table of Contents**: Comprehensive listing of sections, page allocations, tables, and figures.
6. **Introduction**: Motivation for computer-assisted hematological logistics and mission-critical reliability.
7. **Background and Problem Statement**: Inefficiencies, expiration waste, and transactional risks of manual paper logbooks.
8. **Project Objectives**: Core functional, data integrity, security, and administrative goals.
9. **Scope of the Project**: Boundary definitions, supported administrative workflows, and excluded perimeter systems.
10. **Existing System and Proposed System**: Comparative analytical matrix contrasting legacy manual workflows against BBMS.
11. **System Requirements**: Functional Requirements (FR-01 to FR-10) and Non-Functional Requirements (NFR-01 to NFR-06).
12. **Hardware and Software Requirements**: Minimum client/server hardware specs, runtime platforms, and libraries.
13. **Technology Stack**: Python 3.12+, Flask 3.1, Jinja2, MySQL 8.0/MariaDB, Bootstrap 5, FontAwesome, Werkzeug Scrypt.
14. **System Architecture**: 3-Tier Layered Architecture with deep technical walkthrough of Presentation, Application, and Data tiers.
15. **Use Case Diagram**: Boundary diagram identifying Staff and Administrator actor roles and operational use cases.
16. **Data Flow Diagram (DFD)**: Level 0 Context Diagram and Level 1 Decomposed Process Diagram tracking biological flow.
17. **Entity-Relationship (ER) Diagram**: Enhanced Chen notation and crow's-foot relational model detailing primary/foreign keys and cardinality.
18. **Database Design & Schema**: Full relational data dictionary for `Donors`, `Blood_Donations`, `Blood_Stock`, `Hospitals`, `Blood_Requests`, and `Admin_Users`.
19. **System Implementation**: Transaction management, Row-Level Locking (`SELECT ... FOR UPDATE`), Connection Pooling, Scrypt hashing, and CSRF defense.
20. **Major Features and Module Description**: In-depth analysis of Donor, Inventory, Requisition, Analytics, and Security sub-systems.
21. **User Interface Screenshots with Detailed Explanations**: 13 high-fidelity figures illustrating system interactions.
22. **Testing and Test Cases**: Formal test strategy, automated suite summary (219 tests), and comprehensive test case matrix.
23. **Results and Discussion**: Performance benchmarks, transactional concurrency analysis, and stock reconciliation validation.
24. **Limitations**: System boundary conditions (single-center scope, cold chain IoT telemetry absence, synchronous email dispatch).
25. **Future Improvements**: RFID cold chain telemetry, multi-center federated transfers, HL7/FHIR hospital EHR integration, and native mobile apps.
26. **Conclusion**: Academic synthesis of engineering achievements, data integrity proofs, and societal impact.
27. **References**: Formal IEEE-style citations across database theory, transactional ACID semantics, web security, and transfusion medicine.

---

## 3. Database Design & Transactional Invariants

### 3.1 Mathematical Stock Inventory Invariant

A central engineering achievement of the Blood Bank Management System is the mathematically guaranteed stock reconciliation rule:

$$\text{Current Stock }(g) = \text{Opening Balance }(g) + \sum \text{Donated Units }(g) - \sum \text{Completed Requested Units }(g)$$

This invariant is verified in automated database testing across all 8 blood groups ($A+, A-, B+, B-, AB+, AB-, O+, O-$) and holds without drift under concurrent workloads.

### 3.2 Concurrency & ACID Safety

To prevent race conditions during simultaneous hospital blood allocations:
1. Requisition fulfillment executes inside an explicit database transaction (`conn.autocommit = False`).
2. Target inventory rows are locked using pessimistic row-level locking:
   ```sql
   SELECT Quantity FROM Blood_Stock WHERE Blood_Group = %s FOR UPDATE;
   ```
3. If available units are insufficient, an `InsufficientStockError` is raised, triggering an automatic `conn.rollback()`.
4. Successful allocations decrement `Blood_Stock` and set `Blood_Requests.Status = 'Completed'` atomically prior to `conn.commit()`.

---

## 4. Test Suite Execution & Verification

The project includes an exhaustive automated test suite. Prior to compiling this academic report, the entire suite was executed against a live MySQL/MariaDB test database instance.

### Test Results Summary

| Test Suite Module | Target Scope | Tests Run | Passed | Failed | Errors |
|:---|:---|:---:|:---:|:---:|:---:|
| `tests/test_db.py` | Schema Integrity, CRUD, Foreign Keys, Row Locking, Reconciliation Invariant, Failover | 124 | 124 | 0 | 0 |
| `tests/test_admin.py` | Admin Auth, Scrypt Hashing, Dual Approval Workflow, Audit Logs, CSRF Protection | 67 | 67 | 0 | 0 |
| `tests/test_profile.py` | Navigation Bars, Session Invalidation, Privilege Escalation Protection, Profile Updates | 28 | 28 | 0 | 0 |
| **TOTAL** | **Comprehensive Full System Verification** | **219** | **219** | **0** | **0** |

*All 219 tests passed with 100% success rate.*

---

## 5. Report Compilation & Regeneration Guide

All reports, diagrams, and screenshots are fully reproducible using the included Python scripts.

### Prerequisites

Ensure the Python environment contains the necessary dependencies:

```bash
pip install flask mysql-connector-python python-docx reportlab matplotlib pillow
```

### 1. Regenerate High-Resolution Diagrams

```bash
python generate_diagrams.py
```
*Outputs 7 publication-quality PNG diagrams into `Project_Diagrams/`.*

### 2. Capture Application UI Screenshots

Ensure local MySQL is running with `blood_bank_db` seeded, then run:

```bash
python take_screenshots.py
```
*Outputs 13 authentic UI screenshots into `Project_Screenshots/`.*

### 3. Rebuild Editable DOCX Report

```bash
python generate_final_docx.py
```
*Compiles the complete 27-section document into `Project_Report.docx`.*

### 4. Rebuild Submission-Ready PDF Report

```bash
python generate_final_pdf.py
```
*Compiles the publication-ready 45-page document with dynamic headers and two-pass "Page X of 45" footers into `Project_Report.pdf`.*

---

## 6. Document Metadata

- **Title:** Blood Bank Management System: Design, Implementation, and Transactional Validation
- **Document Version:** 1.0.0 (Submission Release)
- **Primary Deliverables:** `Project_Report.docx` (~3.0 MB), `Project_Report.pdf` (~3.1 MB)
- **Total Pages (PDF):** 45 Pages
- **Total Embedded Figures:** 20 Figures (7 Diagrams + 13 Live Application Screenshots)
- **Total Tables:** 14 Comprehensive Technical & Data Dictionary Tables
- **References:** 12 IEEE-Formatted Formal Academic Citations
- **Source Code Status:** Original source code completely unmodified; 100% authentic artifacts.


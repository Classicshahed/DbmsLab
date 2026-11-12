"""
build_presentation.py
Professional Redesign of Blood Bank Management System University Presentation
Outputs: Professional_Presentation/Final_Professional_Presentation.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# CONSTANTS & PALETTE
# ---------------------------------------------------------
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette (Medical & Academic)
COLOR_CRIMSON = RGBColor(153, 0, 0)          # #990000 Primary Medical Crimson
COLOR_CRIMSON_DARK = RGBColor(128, 0, 0)     # #800000 Deep Burgundy
COLOR_CRIMSON_TINT = RGBColor(254, 242, 242) # #FEF2F2 Soft Crimson Tint
COLOR_CRIMSON_BORDER = RGBColor(254, 202, 202) # #FECACA

COLOR_NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A Slate 900
COLOR_NAVY_MID = RGBColor(30, 41, 59)        # #1E293B Slate 800
COLOR_NAVY_LIGHT = RGBColor(241, 245, 249)   # #F1F5F9 Slate 100
COLOR_NAVY_BORDER = RGBColor(203, 213, 225)  # #CBD5E1 Slate 300

COLOR_TEXT_PRIMARY = RGBColor(15, 23, 42)    # #0F172A Dark charcoal
COLOR_TEXT_SECONDARY = RGBColor(51, 65, 85)  # #334155 Slate 700
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate 500

COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BG = RGBColor(248, 250, 252)           # #F8FAFC Slate 50
COLOR_RULE = RGBColor(226, 232, 240)         # #E2E8F0

# Code Terminal Colors
COLOR_TERM_BG = RGBColor(15, 23, 42)         # #0F172A Dark IDE container
COLOR_TERM_TEXT = RGBColor(241, 245, 249)    # #F1F5F9
COLOR_KEYWORD = RGBColor(56, 189, 248)       # #38BDF8 Cyan
COLOR_COMMENT = RGBColor(148, 163, 184)      # #94A3B8 Slate 400
COLOR_STRING = RGBColor(52, 211, 153)        # #34D399 Mint
COLOR_FUNC = RGBColor(251, 191, 36)          # #FBBF24 Amber

# Directories
WORKSPACE = r"C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project"
RAW_IMG_DIR = os.path.join(WORKSPACE, "raw_extracted_slides")
SCREENSHOTS_DIR = os.path.join(WORKSPACE, "Project_Report", "Project_Screenshots")
OUT_DIR = os.path.join(WORKSPACE, "Professional_Presentation")
os.makedirs(OUT_DIR, exist_ok=True)


def create_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]
    return prs, blank_layout


def add_base_background(slide):
    """Adds a full-slide subtle off-white background."""
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background()
    return bg_shape


def add_header_footer(slide, kicker_text, title_text, subtitle_text, slide_num, total_slides=11):
    """Standard professional university editorial header and footer."""
    # Top decorative kicker pill
    kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.3))
    tf_k = kicker_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker_text.upper()
    p_k.font.name = "Arial"
    p_k.font.size = Pt(9.5)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_PRIMARY

    # Subtitle / context description
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.7), Inches(0.32))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.name = "Calibri"
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = COLOR_TEXT_MUTED

    # Top dividing line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.015))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = COLOR_RULE
    top_line.line.fill.background()

    # Bottom dividing line
    bot_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.015))
    bot_line.fill.solid()
    bot_line.fill.fore_color.rgb = COLOR_RULE
    bot_line.line.fill.background()

    # Footer left
    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(8.0), Inches(0.3))
    tf_fl = foot_left.text_frame
    tf_fl.margin_left = tf_fl.margin_right = tf_fl.margin_top = tf_fl.margin_bottom = 0
    p_fl = tf_fl.paragraphs[0]
    p_fl.text = "Blood Bank Management System | DBMS Laboratory Project (MySQL + Flask)"
    p_fl.font.name = "Calibri"
    p_fl.font.size = Pt(9.5)
    p_fl.font.color.rgb = COLOR_TEXT_MUTED

    # Footer right
    foot_right = slide.shapes.add_textbox(Inches(9.5), Inches(7.0), Inches(3.033), Inches(0.3))
    tf_fr = foot_right.text_frame
    tf_fr.margin_left = tf_fr.margin_right = tf_fr.margin_top = tf_fr.margin_bottom = 0
    p_fr = tf_fr.paragraphs[0]
    p_fr.alignment = PP_ALIGN.RIGHT
    p_fr.text = f"Slide {slide_num} of {total_slides}"
    p_fr.font.name = "Calibri"
    p_fr.font.size = Pt(9.5)
    p_fr.font.color.rgb = COLOR_TEXT_MUTED


def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_NAVY_BORDER, border_width=Pt(1)):
    """Creates a sleek container card with subtle border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = border_width
    else:
        card.line.fill.background()
    return card


# =========================================================================
# SLIDE BUILDERS
# =========================================================================

def build_slide_1(prs, layout):
    """Slide 1: Hero Editorial Title & Attribution Slide."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)

    # Left vertical accent line
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.08), Inches(2.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_CRIMSON
    bar.line.fill.background()

    # Kicker
    kicker = slide.shapes.add_textbox(Inches(1.05), Inches(1.25), Inches(9.0), Inches(0.35))
    tf_k = kicker.text_frame
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = "CSE 3100: DATABASE MANAGEMENT SYSTEMS LABORATORY • FINAL PROJECT"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(11)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON

    # Title
    title = slide.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(9.5), Inches(1.1))
    tf_t = title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = "Blood Bank Management System"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    # Subtitle
    sub = slide.shapes.add_textbox(Inches(1.05), Inches(2.82), Inches(9.5), Inches(0.65))
    tf_s = sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = "Relational Database Implementation, Concurrency Invariants, and Web Application\n(MySQL 8.0 Engine + Python Flask Web Framework)"
    p_s.font.name = "Calibri"
    p_s.font.size = Pt(15)
    p_s.font.color.rgb = COLOR_TEXT_SECONDARY

    # Right side graphic motif
    icon_path = os.path.join(RAW_IMG_DIR, "slide_11_img_6.png")
    if os.path.exists(icon_path):
        slide.shapes.add_picture(icon_path, Inches(10.6), Inches(1.3), Inches(1.9), Inches(2.3))

    # Divider line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.8), Inches(11.733), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_RULE
    div.line.fill.background()

    # Three Structured Cards for Presenters, Course, Instructor
    card_w = Inches(3.68)
    card_h = Inches(2.8)
    card_y = Inches(4.05)

    # Card 1: Presenters
    add_card(slide, Inches(0.8), card_y, card_w, card_h)
    # Header inside card
    tb1 = slide.shapes.add_textbox(Inches(1.0), card_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    
    p = tf1.paragraphs[0]
    p.text = "GROUP MEMBERS (PRESENTERS)"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(10)

    members = [
        ("Tahamina", "1003"),
        ("Md. Shifat Pramanik", "1035"),
        ("Shahed Ahmad", "1043"),
        ("Md. Rayhan", "1107"),
        ("Sanim Ahmed Khan", "1175")
    ]
    for name, s_id in members:
        p_m = tf1.add_paragraph()
        p_m.text = f"• {name}  (ID: {s_id})"
        p_m.font.name = "Calibri"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_after = Pt(3)

    # Card 2: Academic Department & Course
    add_card(slide, Inches(4.82), card_y, card_w, card_h)
    tb2 = slide.shapes.add_textbox(Inches(5.02), card_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    p.text = "COURSE SPECIFICATION"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(10)

    course_info = [
        ("Course:", "Database Management Systems"),
        ("Course Code:", "CSE 3100"),
        ("Department:", "Computer Science & Engineering"),
        ("Level/Term:", "3rd Year, Final Term"),
        ("Platform:", "MySQL Engine + Flask Framework")
    ]
    for label, val in course_info:
        p_c = tf2.add_paragraph()
        p_c.text = f"{label} {val}"
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = COLOR_TEXT_PRIMARY
        p_c.space_after = Pt(4)

    # Card 3: Course Instructor
    add_card(slide, Inches(8.85), card_y, card_w, card_h)
    tb3 = slide.shapes.add_textbox(Inches(9.05), card_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p = tf3.paragraphs[0]
    p.text = "COURSE INSTRUCTOR"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(10)

    p_i1 = tf3.add_paragraph()
    p_i1.text = "Ramisa Rahman"
    p_i1.font.name = "Arial"
    p_i1.font.size = Pt(14)
    p_i1.font.bold = True
    p_i1.font.color.rgb = COLOR_NAVY_DARK
    p_i1.space_after = Pt(4)

    p_i2 = tf3.add_paragraph()
    p_i2.text = "Lecturer, Department of CSE\nProject Defense & Evaluation Panel"
    p_i2.font.name = "Calibri"
    p_i2.font.size = Pt(11)
    p_i2.font.color.rgb = COLOR_TEXT_MUTED
    p_i2.space_after = Pt(16)

    p_badge = tf3.add_paragraph()
    p_badge.text = "✓ Final Laboratory Defense"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(10.5)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_CRIMSON


def build_slide_2(prs, layout):
    """Slide 2: Problem Statement & Project Objectives (Split Contrast Layout)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Project Motivation & Scope", "Problem Statement & Core Project Objectives",
                      "Overcoming manual record degradation through formal relational normalization and transactional invariants.", 2)

    col_w = Inches(5.72)
    col_h = Inches(4.95)
    col_y = Inches(1.8)

    # Left Column: Problem Statement (Warning / Alert Styling)
    add_card(slide, Inches(0.8), col_y, col_w, col_h, bg_color=COLOR_WHITE, border_color=COLOR_CRIMSON_BORDER)
    # Accent top border band
    top_band_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), col_y, col_w, Inches(0.06))
    top_band_l.fill.solid()
    top_band_l.fill.fore_color.rgb = COLOR_CRIMSON
    top_band_l.line.fill.background()

    tb_l = slide.shapes.add_textbox(Inches(1.05), col_y + Inches(0.2), col_w - Inches(0.5), col_h - Inches(0.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_k = tf_l.paragraphs[0]
    p_k.text = "THE PROBLEM DOMAIN"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON
    p_k.space_after = Pt(4)

    p_title = tf_l.add_paragraph()
    p_title.text = "Vulnerabilities of Manual & Spreadsheet Systems"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY_DARK
    p_title.space_after = Pt(8)

    p_desc = tf_l.add_paragraph()
    p_desc.text = "Paper logbooks and decentralized Excel sheets introduce severe operational failure points in critical emergency healthcare:"
    p_desc.font.name = "Calibri"
    p_desc.font.size = Pt(11)
    p_desc.font.color.rgb = COLOR_TEXT_SECONDARY
    p_desc.space_after = Pt(12)

    problems = [
        ("Duplicate Donor Records", "Absence of telephone unique constraints causes redundant registrations and split donation histories across drives."),
        ("Lost Longitudinal History", "Prior donation dates, deferral windows, and adverse screening histories cannot be reliably retrieved during emergencies."),
        ("Inaccurate Stock Counts", "Physical blood bags diverge from manual tallies, causing dangerous phantom availability or unexpected deficits."),
        ("Zero Emergency Visibility", "Hospitals and emergency trauma ICUs cannot query blood group availability in real time, causing life-threatening dispatch delays.")
    ]
    for title, desc in problems:
        p_pt = tf_l.add_paragraph()
        p_pt.text = f"•  {title}: {desc}"
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = COLOR_TEXT_PRIMARY
        p_pt.space_after = Pt(8)

    # Right Column: Objectives (Engineering Solution Styling)
    add_card(slide, Inches(6.8), col_y, col_w, col_h, bg_color=COLOR_WHITE, border_color=COLOR_NAVY_BORDER)
    top_band_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), col_y, col_w, Inches(0.06))
    top_band_r.fill.solid()
    top_band_r.fill.fore_color.rgb = COLOR_NAVY_DARK
    top_band_r.line.fill.background()

    tb_r = slide.shapes.add_textbox(Inches(7.05), col_y + Inches(0.2), col_w - Inches(0.5), col_h - Inches(0.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_kr = tf_r.paragraphs[0]
    p_kr.text = "CORE PROJECT OBJECTIVES"
    p_kr.font.name = "Arial"
    p_kr.font.size = Pt(10)
    p_kr.font.bold = True
    p_kr.font.color.rgb = COLOR_NAVY_DARK
    p_kr.space_after = Pt(4)

    p_titler = tf_r.add_paragraph()
    p_titler.text = "Relational Rigor & Transactional Database Goals"
    p_titler.font.name = "Arial"
    p_titler.font.size = Pt(15)
    p_titler.font.bold = True
    p_titler.font.color.rgb = COLOR_NAVY_DARK
    p_titler.space_after = Pt(8)

    p_descr = tf_r.add_paragraph()
    p_descr.text = "Engineered to satisfy comprehensive University DBMS Laboratory academic criteria:"
    p_descr.font.name = "Calibri"
    p_descr.font.size = Pt(11)
    p_descr.font.color.rgb = COLOR_TEXT_SECONDARY
    p_descr.space_after = Pt(12)

    objectives = [
        ("Normalized Relational Schema (3NF)", "6 core relational tables designed in Third Normal Form to eliminate insertion, update, and deletion anomalies."),
        ("Multi-Layer Integrity Constraints", "Enforced Primary Keys, Foreign Keys (ON DELETE RESTRICT), UNIQUE phone bounds, and CHECK donor age bounds (18–65)."),
        ("Realistic Sample Data Seeding", "Realistic dataset across 8 human blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-) modeling live clinic operations."),
        ("15+ Advanced SQL Queries", "Complex SQL analytics utilizing INNER/LEFT JOINs, GROUP BY aggregation, date formatting, and subquery filters."),
        ("ACID Safe Stock Balancing", "Atomic transaction updates with row-level locking (SELECT ... FOR UPDATE) preventing stock from dropping below zero.")
    ]
    for title, desc in objectives:
        p_pt = tf_r.add_paragraph()
        p_pt.text = f"✓  {title}: {desc}"
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = COLOR_TEXT_PRIMARY
        p_pt.space_after = Pt(6)


def build_slide_3(prs, layout):
    """Slide 3: Project Features & Live Web Application Dashboard."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "System Implementation & Capabilities", "Project Features & Real-Time Analytical Dashboard",
                      "Modular architecture spanning donor registration, inventory balancing, and hospital emergency requisitions.", 3)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Features Breakdown (Inches(4.8) wide)
    col_w_l = Inches(4.8)
    add_card(slide, Inches(0.8), col_y, col_w_l, col_h)

    tb_l = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.2), col_w_l - Inches(0.4), col_h - Inches(0.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_k = tf_l.paragraphs[0]
    p_k.text = "CORE FUNCTIONAL MODULES"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON
    p_k.space_after = Pt(6)

    features = [
        ("Donor Management Lifecycle", "Full CRUD operations (Add, Edit, Delete, Search by Blood Group & City) with strict clinical age validation (18–65)."),
        ("Blood Donation Intake", "Donation logging triggers automated stock increment for matched blood type, maintaining an immutable ledger."),
        ("Live Inventory & Low-Stock Alerts", "Real-time stock dashboard across all 8 blood groups with visual badge alerts when reserves drop below 10 units."),
        ("Hospital Emergency Requisitions", "3-stage transactional lifecycle (Pending → Approved → Completed) with atomic quantity reservation."),
        ("Administrative Governance & SQL Reports", "Dual-authorization admin approval, session audit logs, and on-demand SQL analytical query execution.")
    ]
    for idx, (f_title, f_desc) in enumerate(features):
        p_num = tf_l.add_paragraph()
        p_num.text = f"{idx+1}. {f_title}"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_NAVY_DARK
        p_num.space_after = Pt(1)

        p_desc = tf_l.add_paragraph()
        p_desc.text = f_desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.8)
        p_desc.font.color.rgb = COLOR_TEXT_SECONDARY
        p_desc.space_after = Pt(6)

    # Right Column: Screenshot Showcase (Inches(6.65) wide)
    col_w_r = Inches(6.65)
    col_x_r = Inches(5.88)
    add_card(slide, col_x_r, col_y, col_w_r, col_h)

    # Window header bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x_r, col_y, col_w_r, Inches(0.35))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY_DARK
    top_bar.line.fill.background()

    tb_bar = slide.shapes.add_textbox(col_x_r + Inches(0.2), col_y + Inches(0.06), col_w_r - Inches(0.4), Inches(0.25))
    tf_bar = tb_bar.text_frame
    tf_bar.margin_left = tf_bar.margin_right = tf_bar.margin_top = tf_bar.margin_bottom = 0
    p_b = tf_bar.paragraphs[0]
    p_b.text = "● ● ●  Blood Bank Management System — Live Production Dashboard"
    p_b.font.name = "Consolas"
    p_b.font.size = Pt(9.5)
    p_b.font.color.rgb = COLOR_NAVY_LIGHT

    # Image
    dash_img_path = os.path.join(SCREENSHOTS_DIR, "01_dashboard.png")
    if not os.path.exists(dash_img_path):
        dash_img_path = os.path.join(RAW_IMG_DIR, "slide_3_img_9.png")

    if os.path.exists(dash_img_path):
        slide.shapes.add_picture(dash_img_path, col_x_r + Inches(0.15), col_y + Inches(0.45), Inches(6.35), Inches(4.0))

    # Caption under image
    cap_box = slide.shapes.add_textbox(col_x_r + Inches(0.2), col_y + Inches(4.55), col_w_r - Inches(0.4), Inches(0.3))
    tf_cap = cap_box.text_frame
    tf_cap.word_wrap = True
    tf_cap.margin_left = tf_cap.margin_right = tf_cap.margin_top = tf_cap.margin_bottom = 0
    p_c = tf_cap.paragraphs[0]
    p_c.text = "Figure: Real-time KPI summary cards, live blood stock inventory table, and recent transaction audit stream."
    p_c.font.name = "Calibri"
    p_c.font.size = Pt(9.5)
    p_c.font.color.rgb = COLOR_TEXT_MUTED


def build_slide_4(prs, layout):
    """Slide 4: Conceptual Database Design (ER Diagram in Chen Notation)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Conceptual Database Architecture", "Entity-Relationship (ER) Diagram: Chen Notation",
                      "Formal conceptual model capturing 6 core entities, relationships, attributes, and administrative audit logging.", 4)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Notation Formalisms & Entities (Inches(4.4) wide)
    col_w_l = Inches(4.4)
    add_card(slide, Inches(0.8), col_y, col_w_l, col_h)

    tb_l = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.2), col_w_l - Inches(0.4), col_h - Inches(0.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_k = tf_l.paragraphs[0]
    p_k.text = "FORMAL CHEN NOTATION KEY"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON
    p_k.space_after = Pt(4)

    symbols = [
        ("Rectangles", "Entity Sets (Donor, Blood_Group, Donation, Blood_Stock, Hospital, Blood_Request)"),
        ("Diamonds", "Relationship Sets (makes, classifies, tracked in, typed as, needed for, raises, logged)"),
        ("Solid Ellipse (Underline)", "Primary Key (Donor_ID, Bg_ID, Donation_ID, Stock_ID, Hospital_ID, Request_ID, Audit_ID)"),
        ("Dashed Ellipse", "Foreign Key reference maintaining relational integrity (e.g., Bg_ID, Donor_ID)"),
        ("Cardinality (1 / N)", "Mapping constraints (1 Donor : N Donations, 1 Hospital : N Requests)")
    ]
    for sym, desc in symbols:
        p_s = tf_l.add_paragraph()
        p_s.text = f"•  {sym}: {desc}"
        p_s.font.name = "Calibri"
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = COLOR_TEXT_PRIMARY
        p_s.space_after = Pt(5)

    p_div = tf_l.add_paragraph()
    p_div.text = "CORE SYSTEM ENTITIES (6 + 1)"
    p_div.font.name = "Arial"
    p_div.font.size = Pt(10)
    p_div.font.bold = True
    p_div.font.color.rgb = COLOR_NAVY_DARK
    p_div.space_before = Pt(8)
    p_div.space_after = Pt(4)

    entities = [
        ("Donor & Blood_Group", "Volunteers classified into 1 of 8 standard blood types."),
        ("Donation & Blood_Stock", "Intake records updating the inventory balance pool."),
        ("Hospital & Blood_Request", "Partner clinical facilities requesting emergency units."),
        ("Admin_Audit_Log", "Administrative proposal tracking with approval trail.")
    ]
    for e_name, e_desc in entities:
        p_e = tf_l.add_paragraph()
        p_e.text = f"▸  {e_name}: {e_desc}"
        p_e.font.name = "Calibri"
        p_e.font.size = Pt(9.8)
        p_e.font.color.rgb = COLOR_TEXT_SECONDARY
        p_e.space_after = Pt(3)

    # Right Column: High-Resolution ER Diagram (Inches(7.05) wide)
    col_w_r = Inches(7.05)
    col_x_r = Inches(5.48)
    add_card(slide, col_x_r, col_y, col_w_r, col_h)

    er_img_path = os.path.join(RAW_IMG_DIR, "slide_4_img_5.png")
    if os.path.exists(er_img_path):
        slide.shapes.add_picture(er_img_path, col_x_r + Inches(0.15), col_y + Inches(0.15), Inches(6.75), Inches(4.65))


def build_slide_5(prs, layout):
    """Slide 5: Database Implementation & Physical Tables Overview."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Physical Schema Specification", "Database Implementation & Physical Tables Overview",
                      "Physical catalog structure and active relational tables within the blood_bank_db MySQL database.", 5)

    col_w = Inches(5.72)
    col_h = Inches(4.95)
    col_y = Inches(1.8)

    # Left Column: Catalog & Table Schema Verification
    add_card(slide, Inches(0.8), col_y, col_w, col_h)

    tb_l = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.15), col_w - Inches(0.4), Inches(1.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_k = tf_l.paragraphs[0]
    p_k.text = "1. CATALOG & SCHEMA VERIFICATION"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON
    p_k.space_after = Pt(2)

    p_desc = tf_l.add_paragraph()
    p_desc.text = "• SHOW TABLES: Confirms 6 normalized tables (blood_group, blood_request, blood_stock, donation, donor, hospital).\n• DESCRIBE Donor: Verifies types, NOT NULL, PRI, UNI, and MUL constraints."
    p_desc.font.name = "Calibri"
    p_desc.font.size = Pt(9.8)
    p_desc.font.color.rgb = COLOR_TEXT_SECONDARY

    # Left Image (slide_5_img_16.png)
    img_l = os.path.join(RAW_IMG_DIR, "slide_5_img_16.png")
    if os.path.exists(img_l):
        slide.shapes.add_picture(img_l, Inches(0.95), col_y + Inches(1.2), Inches(5.42), Inches(3.55))

    # Right Column: Active Tables Data Overview
    add_card(slide, Inches(6.8), col_y, col_w, col_h)

    tb_r = slide.shapes.add_textbox(Inches(7.0), col_y + Inches(0.15), col_w - Inches(0.4), Inches(1.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_kr = tf_r.paragraphs[0]
    p_kr.text = "2. ACTIVE INVENTORY & DONOR ROSTER DATA"
    p_kr.font.name = "Arial"
    p_kr.font.size = Pt(10)
    p_kr.font.bold = True
    p_kr.font.color.rgb = COLOR_NAVY_DARK
    p_kr.space_after = Pt(2)

    p_descr = tf_r.add_paragraph()
    p_descr.text = "• SELECT * FROM Blood_Stock: Displays real-time units across 8 blood groups.\n• SELECT * FROM Donor: Displays registered donor tuples with unique phones."
    p_descr.font.name = "Calibri"
    p_descr.font.size = Pt(9.8)
    p_descr.font.color.rgb = COLOR_TEXT_SECONDARY

    # Right Image (slide_5_img_18.png)
    img_r = os.path.join(RAW_IMG_DIR, "slide_5_img_18.png")
    if os.path.exists(img_r):
        slide.shapes.add_picture(img_r, Inches(6.95), col_y + Inches(1.2), Inches(5.42), Inches(3.55))


def build_slide_6(prs, layout):
    """Slide 6: SQL DDL & DML (CREATE TABLE and INSERT with Constraints)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "DDL & DML Specification", "SQL: Table Creation with Constraints & Verified Tuple Insertion",
                      "Enforcing domain, entity, and referential integrity via strict SQL schema definitions.", 6)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Monospace Dark IDE Code Terminal (Inches(5.72) wide)
    col_w_l = Inches(5.72)
    add_card(slide, Inches(0.8), col_y, col_w_l, col_h, bg_color=COLOR_TERM_BG, border_color=COLOR_NAVY_MID)

    # Terminal header bar
    term_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), col_y, col_w_l, Inches(0.35))
    term_bar.fill.solid()
    term_bar.fill.fore_color.rgb = COLOR_NAVY_MID
    term_bar.line.fill.background()

    tb_tb = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.06), col_w_l - Inches(0.4), Inches(0.25))
    tf_tb = tb_tb.text_frame
    tf_tb.margin_left = tf_tb.margin_right = tf_tb.margin_top = tf_tb.margin_bottom = 0
    p_tb = tf_tb.paragraphs[0]
    p_tb.text = "● ● ●  MySQL Console — DDL & DML Script"
    p_tb.font.name = "Consolas"
    p_tb.font.size = Pt(9.5)
    p_tb.font.color.rgb = COLOR_NAVY_LIGHT

    # Code Content
    tb_c = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.45), col_w_l - Inches(0.4), col_h - Inches(0.6))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    sql_lines = [
        ("-- 1. DDL: Create Donor Table with Constraints", COLOR_COMMENT),
        ("CREATE TABLE Donor (", COLOR_KEYWORD),
        ("  Donor_ID INT AUTO_INCREMENT PRIMARY KEY,", COLOR_TERM_TEXT),
        ("  Name VARCHAR(100) NOT NULL,", COLOR_TERM_TEXT),
        ("  Age INT CHECK (Age BETWEEN 18 AND 65),", COLOR_FUNC),
        ("  Gender ENUM('Male','Female','Other'),", COLOR_TERM_TEXT),
        ("  Phone VARCHAR(15) UNIQUE NOT NULL,", COLOR_FUNC),
        ("  Bg_ID INT NOT NULL,", COLOR_TERM_TEXT),
        ("  FOREIGN KEY (Bg_ID)", COLOR_KEYWORD),
        ("    REFERENCES Blood_Group(Bg_ID)", COLOR_KEYWORD),
        (");", COLOR_KEYWORD),
        ("", COLOR_TERM_TEXT),
        ("-- 2. DML: Verified Tuple Insertion", COLOR_COMMENT),
        ("INSERT INTO Donor", COLOR_KEYWORD),
        ("  (Name, Age, Gender, Phone, Bg_ID)", COLOR_TERM_TEXT),
        ("VALUES", COLOR_KEYWORD),
        ("  ('Test Donor', 25, 'Male', '9000000123', 1);", COLOR_STRING)
    ]
    for idx, (code_txt, color) in enumerate(sql_lines):
        p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
        p.text = code_txt
        p.font.name = "Consolas"
        p.font.size = Pt(10)
        p.font.color.rgb = color
        p.space_after = Pt(2)

    # Right Column: Two Workbench Verification Cards
    col_w_r = Inches(5.72)
    col_x_r = Inches(6.8)

    # Sub-card 1: CREATE TABLE Output (Top)
    add_card(slide, col_x_r, col_y, col_w_r, Inches(2.35))
    tb_r1 = slide.shapes.add_textbox(col_x_r + Inches(0.15), col_y + Inches(0.1), col_w_r - Inches(0.3), Inches(0.3))
    tf_r1 = tb_r1.text_frame
    tf_r1.margin_left = tf_r1.margin_right = tf_r1.margin_top = tf_r1.margin_bottom = 0
    p_r1 = tf_r1.paragraphs[0]
    p_r1.text = "DDL Execution: SHOW CREATE TABLE Donor"
    p_r1.font.name = "Arial"
    p_r1.font.size = Pt(9.5)
    p_r1.font.bold = True
    p_r1.font.color.rgb = COLOR_CRIMSON

    img_r1 = os.path.join(RAW_IMG_DIR, "slide_6_img_18.png")
    if os.path.exists(img_r1):
        slide.shapes.add_picture(img_r1, col_x_r + Inches(0.15), col_y + Inches(0.4), Inches(5.42), Inches(1.85))

    # Sub-card 2: INSERT & Query Output (Bottom)
    sub_y2 = col_y + Inches(2.55)
    add_card(slide, col_x_r, sub_y2, col_w_r, Inches(2.4))
    tb_r2 = slide.shapes.add_textbox(col_x_r + Inches(0.15), sub_y2 + Inches(0.1), col_w_r - Inches(0.3), Inches(0.3))
    tf_r2 = tb_r2.text_frame
    tf_r2.margin_left = tf_r2.margin_right = tf_r2.margin_top = tf_r2.margin_bottom = 0
    p_r2 = tf_r2.paragraphs[0]
    p_r2.text = "DML Verification: INSERT INTO & SELECT New Tuple"
    p_r2.font.name = "Arial"
    p_r2.font.size = Pt(9.5)
    p_r2.font.bold = True
    p_r2.font.color.rgb = COLOR_NAVY_DARK

    img_r2 = os.path.join(RAW_IMG_DIR, "slide_6_img_22.png")
    if os.path.exists(img_r2):
        slide.shapes.add_picture(img_r2, col_x_r + Inches(0.15), sub_y2 + Inches(0.4), Inches(5.42), Inches(1.9))


def build_slide_7(prs, layout):
    """Slide 7: Basic SQL Operations (SELECT, WHERE, ORDER BY, UPDATE, DELETE)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Data Manipulation Language", "Basic SQL Operations: SELECT, WHERE, UPDATE, and DELETE",
                      "Filtering, updating in-place, and safely deleting records with verified execution logs.", 7)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Three Modular Operation Cards (Inches(5.72) wide)
    col_w_l = Inches(5.72)

    # Card 1: SELECT & Filter
    add_card(slide, Inches(0.8), col_y, col_w_l, Inches(1.5))
    tb_1 = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.12), col_w_l - Inches(0.4), Inches(1.3))
    tf_1 = tb_1.text_frame
    tf_1.word_wrap = True
    tf_1.margin_left = tf_1.margin_right = tf_1.margin_top = tf_1.margin_bottom = 0
    p = tf_1.paragraphs[0]
    p.text = "1. Filtering & Sorting: SELECT ... WHERE ... ORDER BY"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(2)
    p_code = tf_1.add_paragraph()
    p_code.text = "SELECT Name, Age, Phone FROM Donor\nWHERE Age > 25 ORDER BY Name;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(2)
    p_note = tf_1.add_paragraph()
    p_note.text = "• Purpose: Extracts eligible adult donors sorted alphabetically for urgent notification."
    p_note.font.name = "Calibri"
    p_note.font.size = Pt(9)
    p_note.font.color.rgb = COLOR_TEXT_MUTED

    # Card 2: UPDATE
    c2_y = col_y + Inches(1.65)
    add_card(slide, Inches(0.8), c2_y, col_w_l, Inches(1.5))
    tb_2 = slide.shapes.add_textbox(Inches(1.0), c2_y + Inches(0.12), col_w_l - Inches(0.4), Inches(1.3))
    tf_2 = tb_2.text_frame
    tf_2.word_wrap = True
    tf_2.margin_left = tf_2.margin_right = tf_2.margin_top = tf_2.margin_bottom = 0
    p = tf_2.paragraphs[0]
    p.text = "2. In-Place Tuple Update: UPDATE ... SET ... WHERE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(2)
    p_code = tf_2.add_paragraph()
    p_code.text = "UPDATE Donor SET Phone = '9000000999'\nWHERE Donor_ID = 2;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(2)
    p_note = tf_2.add_paragraph()
    p_note.text = "• Purpose: Updates donor emergency contact targeting primary key; verified with SELECT."
    p_note.font.name = "Calibri"
    p_note.font.size = Pt(9)
    p_note.font.color.rgb = COLOR_TEXT_MUTED

    # Card 3: DELETE
    c3_y = col_y + Inches(3.3)
    add_card(slide, Inches(0.8), c3_y, col_w_l, Inches(1.65))
    tb_3 = slide.shapes.add_textbox(Inches(1.0), c3_y + Inches(0.12), col_w_l - Inches(0.4), Inches(1.4))
    tf_3 = tb_3.text_frame
    tf_3.word_wrap = True
    tf_3.margin_left = tf_3.margin_right = tf_3.margin_top = tf_3.margin_bottom = 0
    p = tf_3.paragraphs[0]
    p.text = "3. Referential Removal: DELETE FROM ... WHERE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(2)
    p_code = tf_3.add_paragraph()
    p_code.text = "DELETE FROM Donor WHERE Phone = '9000000123';\nSELECT COUNT(*) FROM Donor WHERE Phone = '9000000123';"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(2)
    p_note = tf_3.add_paragraph()
    p_note.text = "• Purpose: Safely deletes test records; verified COUNT(*) = 0 confirms deletion."
    p_note.font.name = "Calibri"
    p_note.font.size = Pt(9)
    p_note.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Sequential Execution Output (Inches(5.72) wide)
    col_w_r = Inches(5.72)
    col_x_r = Inches(6.8)
    add_card(slide, col_x_r, col_y, col_w_r, col_h)

    tb_rt = slide.shapes.add_textbox(col_x_r + Inches(0.2), col_y + Inches(0.1), col_w_r - Inches(0.4), Inches(0.3))
    tf_rt = tb_rt.text_frame
    tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_top = tf_rt.margin_bottom = 0
    p_rt = tf_rt.paragraphs[0]
    p_rt.text = "MySQL Workbench Execution Proof (Sequential Operations)"
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(9.5)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_NAVY_DARK

    img_r = os.path.join(RAW_IMG_DIR, "slide_7_img_18.jpg")
    if os.path.exists(img_r):
        slide.shapes.add_picture(img_r, col_x_r + Inches(0.15), col_y + Inches(0.4), Inches(5.42), Inches(4.4))


def build_slide_8(prs, layout):
    """Slide 8: SQL JOIN Operations (INNER JOIN & LEFT JOIN)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Relational Algebra & Multi-Table Queries", "SQL: INNER JOIN and LEFT OUTER JOIN Operations",
                      "Bridging normalized entities to produce human-readable reports and identify donor engagement.", 8)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Code & Relational Significance (Inches(5.72) wide)
    col_w_l = Inches(5.72)

    # Box 1: INNER JOIN
    add_card(slide, Inches(0.8), col_y, col_w_l, Inches(2.35))
    tb_1 = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.15), col_w_l - Inches(0.4), Inches(2.1))
    tf_1 = tb_1.text_frame
    tf_1.word_wrap = True
    tf_1.margin_left = tf_1.margin_right = tf_1.margin_top = tf_1.margin_bottom = 0
    p = tf_1.paragraphs[0]
    p.text = "1. INNER JOIN: Foreign Key Resolution"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(2)
    p_code = tf_1.add_paragraph()
    p_code.text = "SELECT d.Donor_ID, d.Name, bg.Blood_Type\nFROM Donor d\nINNER JOIN Blood_Group bg ON d.Bg_ID = bg.Bg_ID;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(4)
    p_exp = tf_1.add_paragraph()
    p_exp.text = "• Relational Purpose: Resolves surrogate integer key (Bg_ID) to standardized clinical blood types (e.g. 'A+', 'O-'). Filters out non-matching tuples."
    p_exp.font.name = "Calibri"
    p_exp.font.size = Pt(9)
    p_exp.font.color.rgb = COLOR_TEXT_SECONDARY

    # Box 2: LEFT JOIN
    c2_y = col_y + Inches(2.55)
    add_card(slide, Inches(0.8), c2_y, col_w_l, Inches(2.4))
    tb_2 = slide.shapes.add_textbox(Inches(1.0), c2_y + Inches(0.15), col_w_l - Inches(0.4), Inches(2.15))
    tf_2 = tb_2.text_frame
    tf_2.word_wrap = True
    tf_2.margin_left = tf_2.margin_right = tf_2.margin_top = tf_2.margin_bottom = 0
    p = tf_2.paragraphs[0]
    p.text = "2. LEFT OUTER JOIN: Preserving Inactive Entities"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(2)
    p_code = tf_2.add_paragraph()
    p_code.text = "SELECT d.Name, COUNT(dn.Donation_ID) AS total\nFROM Donor d\nLEFT JOIN Donation dn ON d.Donor_ID = dn.Donor_ID\nGROUP BY d.Donor_ID, d.Name;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(4)
    p_exp = tf_2.add_paragraph()
    p_exp.text = "• Relational Purpose: Preserves all donors, including those with zero donations (total = 0). Critical for recruitment campaigns and outreach audit."
    p_exp.font.name = "Calibri"
    p_exp.font.size = Pt(9)
    p_exp.font.color.rgb = COLOR_TEXT_SECONDARY

    # Right Column: Live Result Grids (Inches(5.72) wide)
    col_w_r = Inches(5.72)
    col_x_r = Inches(6.8)
    add_card(slide, col_x_r, col_y, col_w_r, col_h)

    tb_rt = slide.shapes.add_textbox(col_x_r + Inches(0.2), col_y + Inches(0.1), col_w_r - Inches(0.4), Inches(0.3))
    tf_rt = tb_rt.text_frame
    tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_top = tf_rt.margin_bottom = 0
    p_rt = tf_rt.paragraphs[0]
    p_rt.text = "MySQL Workbench Output Grids (LEFT JOIN & INNER JOIN)"
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(9.5)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_NAVY_DARK

    img_r = os.path.join(RAW_IMG_DIR, "slide_8_img_18.png")
    if os.path.exists(img_r):
        slide.shapes.add_picture(img_r, col_x_r + Inches(0.15), col_y + Inches(0.4), Inches(5.42), Inches(4.4))


def build_slide_9(prs, layout):
    """Slide 9: SQL Aggregate Functions and GROUP BY."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Analytical Intelligence & Aggregations", "SQL: Aggregate Functions and GROUP BY Analytics",
                      "Deriving actionable administrative intelligence and inventory trends from transactional data.", 9)

    col_y = Inches(1.8)
    col_h = Inches(4.95)

    # Left Column: Analytical Queries & Business Insight (Inches(5.72) wide)
    col_w_l = Inches(5.72)

    # Box 1: COUNT + GROUP BY
    add_card(slide, Inches(0.8), col_y, col_w_l, Inches(2.35))
    tb_1 = slide.shapes.add_textbox(Inches(1.0), col_y + Inches(0.15), col_w_l - Inches(0.4), Inches(2.1))
    tf_1 = tb_1.text_frame
    tf_1.word_wrap = True
    tf_1.margin_left = tf_1.margin_right = tf_1.margin_top = tf_1.margin_bottom = 0
    p = tf_1.paragraphs[0]
    p.text = "1. Donor Supply Base: COUNT + GROUP BY"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(2)
    p_code = tf_1.add_paragraph()
    p_code.text = "SELECT bg.Blood_Type, COUNT(d.Donor_ID) AS donors\nFROM Blood_Group bg\nLEFT JOIN Donor d ON bg.Bg_ID = d.Bg_ID\nGROUP BY bg.Bg_ID, bg.Blood_Type;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(4)
    p_exp = tf_1.add_paragraph()
    p_exp.text = "• Clinical Insight: Identifies demographic donor concentration per blood group. Pinpoints critical rare groups (e.g. AB-, O-) needing targeted drives."
    p_exp.font.name = "Calibri"
    p_exp.font.size = Pt(9)
    p_exp.font.color.rgb = COLOR_TEXT_SECONDARY

    # Box 2: SUM + GROUP BY
    c2_y = col_y + Inches(2.55)
    add_card(slide, Inches(0.8), c2_y, col_w_l, Inches(2.4))
    tb_2 = slide.shapes.add_textbox(Inches(1.0), c2_y + Inches(0.15), col_w_l - Inches(0.4), Inches(2.15))
    tf_2 = tb_2.text_frame
    tf_2.word_wrap = True
    tf_2.margin_left = tf_2.margin_right = tf_2.margin_top = tf_2.margin_bottom = 0
    p = tf_2.paragraphs[0]
    p.text = "2. Monthly Donation Volume: SUM + DATE_FORMAT"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(2)
    p_code = tf_2.add_paragraph()
    p_code.text = "SELECT DATE_FORMAT(Donation_Date,'%Y-%m') AS month,\n       SUM(Units_Donated) AS total_units\nFROM Donation\nGROUP BY month ORDER BY month;"
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_NAVY_DARK
    p_code.space_after = Pt(4)
    p_exp = tf_2.add_paragraph()
    p_exp.text = "• Clinical Insight: Tracks seasonal collection trends (Jan: 5, Feb: 4, Mar: 5, Apr: 4 units), allowing administrators to forecast clinical inventory."
    p_exp.font.name = "Calibri"
    p_exp.font.size = Pt(9)
    p_exp.font.color.rgb = COLOR_TEXT_SECONDARY

    # Right Column: MySQL Workbench Output Grids (Inches(5.72) wide)
    col_w_r = Inches(5.72)
    col_x_r = Inches(6.8)
    add_card(slide, col_x_r, col_y, col_w_r, col_h)

    tb_rt = slide.shapes.add_textbox(col_x_r + Inches(0.2), col_y + Inches(0.1), col_w_r - Inches(0.4), Inches(0.3))
    tf_rt = tb_rt.text_frame
    tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_top = tf_rt.margin_bottom = 0
    p_rt = tf_rt.paragraphs[0]
    p_rt.text = "MySQL Workbench Analytical Intelligence Grids"
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(9.5)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_NAVY_DARK

    img_r = os.path.join(RAW_IMG_DIR, "slide_9_img_17.png")
    if os.path.exists(img_r):
        slide.shapes.add_picture(img_r, col_x_r + Inches(0.15), col_y + Inches(0.4), Inches(5.42), Inches(4.4))


def build_slide_10(prs, layout):
    """Slide 10: Conclusion & Future Work (Key Technical Achievements & Roadmap)."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)
    add_header_footer(slide, "Synthesis & Strategic Roadmap", "Project Outcomes, Technical Achievements & Future Work",
                      "Evaluating accomplished DBMS laboratory benchmarks and outlining clinical scalability directions.", 10)

    col_w = Inches(5.72)
    col_h = Inches(4.95)
    col_y = Inches(1.8)

    # Left Column: What We Achieved (Success Accent Card)
    add_card(slide, Inches(0.8), col_y, col_w, col_h, bg_color=COLOR_WHITE, border_color=COLOR_NAVY_BORDER)
    top_band_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), col_y, col_w, Inches(0.06))
    top_band_l.fill.solid()
    top_band_l.fill.fore_color.rgb = COLOR_NAVY_DARK
    top_band_l.line.fill.background()

    tb_l = slide.shapes.add_textbox(Inches(1.05), col_y + Inches(0.2), col_w - Inches(0.5), col_h - Inches(0.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_k = tf_l.paragraphs[0]
    p_k.text = "PROJECT DELIVERABLES"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_NAVY_DARK
    p_k.space_after = Pt(4)

    p_title = tf_l.add_paragraph()
    p_title.text = "Key Engineering Achievements"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY_DARK
    p_title.space_after = Pt(10)

    achievements = [
        ("6 Normalized Tables in 3NF", "Completely eliminated partial and transitive functional dependencies, guaranteeing zero redundancy."),
        ("Multi-Layer Constraint Protection", "Domain CHECK age (18–65), telephone UNIQUE keys, and ON DELETE RESTRICT foreign keys safeguard data integrity."),
        ("Atomic Stock Transaction Safety", "Pessimistic row-locking (SELECT ... FOR UPDATE) ensures inventory stock can never drop below zero."),
        ("15+ Advanced Analytical Queries", "Multi-table JOINs, GROUP BY aggregations, and date formatting powering real-time administrative dashboards."),
        ("Production Flask + Bootstrap UI", "Responsive medical web portal with search, automated stock updates, and admin proposal authorization.")
    ]
    for title, desc in achievements:
        p_pt = tf_l.add_paragraph()
        p_pt.text = f"✓  {title}: {desc}"
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(10.2)
        p_pt.font.color.rgb = COLOR_TEXT_PRIMARY
        p_pt.space_after = Pt(6)

    # Right Column: Future Work (Roadmap Accent Card)
    add_card(slide, Inches(6.8), col_y, col_w, col_h, bg_color=COLOR_WHITE, border_color=COLOR_CRIMSON_BORDER)
    top_band_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), col_y, col_w, Inches(0.06))
    top_band_r.fill.solid()
    top_band_r.fill.fore_color.rgb = COLOR_CRIMSON
    top_band_r.line.fill.background()

    tb_r = slide.shapes.add_textbox(Inches(7.05), col_y + Inches(0.2), col_w - Inches(0.5), col_h - Inches(0.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_kr = tf_r.paragraphs[0]
    p_kr.text = "STRATEGIC EXPANSION"
    p_kr.font.name = "Arial"
    p_kr.font.size = Pt(10)
    p_kr.font.bold = True
    p_kr.font.color.rgb = COLOR_CRIMSON
    p_kr.space_after = Pt(4)

    p_titler = tf_r.add_paragraph()
    p_titler.text = "Future Technical Roadmap"
    p_titler.font.name = "Arial"
    p_titler.font.size = Pt(15)
    p_titler.font.bold = True
    p_titler.font.color.rgb = COLOR_NAVY_DARK
    p_titler.space_after = Pt(10)

    future_work = [
        ("Blood Bag Expiration Tracking", "Individual unit barcoding with shelf-life timers (Red Cells: 42 days, Platelets: 5 days) and FIFO dispatch algorithms."),
        ("Plasma & Platelet Sub-Inventories", "Extending schema to manage blood derivatives (Fresh Frozen Plasma, Cryoprecipitate) alongside whole blood."),
        ("Role-Based Access Control (RBAC)", "Fine-grained security tiers distinguishing Laboratory Phlebotomists, Inventory Clerks, and Hospital Physicians."),
        ("Automated Low-Stock Notifications", "Asynchronous SMS and email webhooks triggered whenever rare blood group balances breach safety thresholds."),
        ("HL7 / FHIR Clinical Interoperability", "Integrating hospital electronic health records (EHR) for automated real-time cross-match validation.")
    ]
    for title, desc in future_work:
        p_pt = tf_r.add_paragraph()
        p_pt.text = f"▸  {title}: {desc}"
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(10.2)
        p_pt.font.color.rgb = COLOR_TEXT_PRIMARY
        p_pt.space_after = Pt(6)


def build_slide_11(prs, layout):
    """Slide 11: Authoritative Closing & Q&A Slide."""
    slide = prs.slides.add_slide(layout)
    add_base_background(slide)

    # Large Center Card
    card_w = Inches(10.5)
    card_h = Inches(5.8)
    card_x = Inches(1.416)
    card_y = Inches(0.85)

    add_card(slide, card_x, card_y, card_w, card_h, bg_color=COLOR_WHITE, border_color=COLOR_NAVY_BORDER)

    # Accent top band
    top_band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_x, card_y, card_w, Inches(0.08))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = COLOR_CRIMSON
    top_band.line.fill.background()

    # Kicker
    kicker_box = slide.shapes.add_textbox(card_x + Inches(0.8), card_y + Inches(0.4), card_w - Inches(1.6), Inches(0.35))
    tf_k = kicker_box.text_frame
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = "CSE 3100: DATABASE MANAGEMENT SYSTEMS LABORATORY • FINAL EVALUATION"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(11)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_CRIMSON

    # Big Thank You
    title_box = slide.shapes.add_textbox(card_x + Inches(0.8), card_y + Inches(0.85), card_w - Inches(3.5), Inches(0.9))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = "Thank You for Your Time & Attention"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    # Subtitle / Questions prompt
    sub_box = slide.shapes.add_textbox(card_x + Inches(0.8), card_y + Inches(1.75), card_w - Inches(3.5), Inches(0.5))
    tf_s = sub_box.text_frame
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = "Any Questions or Discussion?"
    p_s.font.name = "Arial"
    p_s.font.size = Pt(20)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_CRIMSON

    # Right side graphic
    icon_path = os.path.join(RAW_IMG_DIR, "slide_11_img_6.png")
    if os.path.exists(icon_path):
        slide.shapes.add_picture(icon_path, card_x + Inches(7.5), card_y + Inches(0.6), Inches(2.2), Inches(2.8))

    # Divider line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_x + Inches(0.8), card_y + Inches(2.4), card_w - Inches(1.6), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_RULE
    div.line.fill.background()

    # Two metadata summary columns inside card
    meta_w = Inches(4.2)
    meta_y = card_y + Inches(2.65)

    # Left Meta: Team Presenters
    tb_m1 = slide.shapes.add_textbox(card_x + Inches(0.8), meta_y, meta_w, Inches(2.8))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = tf_m1.margin_bottom = 0

    p_h1 = tf_m1.paragraphs[0]
    p_h1.text = "PROJECT TEAM (PRESENTERS)"
    p_h1.font.name = "Arial"
    p_h1.font.size = Pt(10)
    p_h1.font.bold = True
    p_h1.font.color.rgb = COLOR_NAVY_DARK
    p_h1.space_after = Pt(6)

    members = [
        "Tahamina (ID: 1003)",
        "Md. Shifat Pramanik (ID: 1035)",
        "Shahed Ahmad (ID: 1043)",
        "Md. Rayhan (ID: 1107)",
        "Sanim Ahmed Khan (ID: 1175)"
    ]
    for m in members:
        p_m = tf_m1.add_paragraph()
        p_m.text = f"• {m}"
        p_m.font.name = "Calibri"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_after = Pt(2)

    # Right Meta: Course & Instructor
    tb_m2 = slide.shapes.add_textbox(card_x + Inches(5.3), meta_y, meta_w, Inches(2.8))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_right = tf_m2.margin_top = tf_m2.margin_bottom = 0

    p_h2 = tf_m2.paragraphs[0]
    p_h2.text = "EVALUATION SPECIFICATION"
    p_h2.font.name = "Arial"
    p_h2.font.size = Pt(10)
    p_h2.font.bold = True
    p_h2.font.color.rgb = COLOR_NAVY_DARK
    p_h2.space_after = Pt(6)

    meta_items = [
        ("Course:", "Database Management Systems (CSE 3100)"),
        ("Department:", "Computer Science & Engineering (CSE)"),
        ("Instructor:", "Ramisa Rahman, Lecturer"),
        ("Project Scope:", "Relational Database Design + Web Portal"),
        ("Technology:", "MySQL 8.0 • Python Flask • Bootstrap 5")
    ]
    for lbl, val in meta_items:
        p_item = tf_m2.add_paragraph()
        p_item.text = f"{lbl} {val}"
        p_item.font.name = "Calibri"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_TEXT_PRIMARY
        p_item.space_after = Pt(2)


# =========================================================================
# MAIN EXECUTION
# =========================================================================

def main():
    prs, layout = create_presentation()

    print("Building Slide 1: Hero Editorial Title & Attribution...")
    build_slide_1(prs, layout)

    print("Building Slide 2: Problem Statement & Project Objectives...")
    build_slide_2(prs, layout)

    print("Building Slide 3: Implemented Features & Web Dashboard...")
    build_slide_3(prs, layout)

    print("Building Slide 4: Conceptual Database Design (ER Diagram)...")
    build_slide_4(prs, layout)

    print("Building Slide 5: Database Implementation & Physical Tables...")
    build_slide_5(prs, layout)

    print("Building Slide 6: SQL DDL & DML (CREATE TABLE & INSERT)...")
    build_slide_6(prs, layout)

    print("Building Slide 7: Basic SQL Operations (SELECT, UPDATE, DELETE)...")
    build_slide_7(prs, layout)

    print("Building Slide 8: SQL JOIN Operations (INNER & LEFT JOIN)...")
    build_slide_8(prs, layout)

    print("Building Slide 9: SQL Aggregate Functions & GROUP BY...")
    build_slide_9(prs, layout)

    print("Building Slide 10: Outcomes, Technical Achievements & Roadmap...")
    build_slide_10(prs, layout)

    print("Building Slide 11: Authoritative Closing & Q&A...")
    build_slide_11(prs, layout)

    out_pptx = os.path.join(OUT_DIR, "Final_Professional_Presentation.pptx")
    prs.save(out_pptx)
    print(f"\nSUCCESS! Redesigned presentation saved to:\n  {out_pptx}")


if __name__ == "__main__":
    main()


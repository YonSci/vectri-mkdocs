# Assessments

How participants are evaluated and certified for the workshop.

---

## 📊 Assessment Overview

Your workshop performance is evaluated across three components:

| Component | Weight | Description |
|-----------|--------|-------------|
| **Lab Completion** | 40% | Hands-on exercises (Labs 1-13) |
| **Capstone Project** | 40% | Final team deliverable |
| **Participation** | 20% | Engagement, collaboration, discussions |

**Passing score:** 70% overall  
**Certificate requirement:** ≥85% attendance + passing score

---

## 🧪 Lab Assessments (40%)

### Structure

**13 Labs total** (Days 1-5)

Each lab is evaluated on:
- ✅ **Completion** (5 points): All tasks attempted
- ✅ **Correctness** (3 points): Outputs match expectations
- ✅ **Documentation** (2 points): Code comments, markdown explanations

**Total:** 10 points per lab × 13 labs = 130 points maximum  
**Scaled to 40%** of final grade

### Lab Checklist

#### Day 1 Labs
- [ ] **Lab 1:** Environment setup, repo cloned, dependencies installed
- [ ] **Lab 2:** CHIRPS/ERA5-Land data downloaded for study region
- [ ] **Lab 3:** Data preprocessed to VECTRI grid, EDA notebook completed

#### Day 2 Labs
- [ ] **Lab 4:** VECTRI compiled successfully, test run passes
- [ ] **Lab 5:** Single-location run, EIR time series plotted
- [ ] **Lab 6:** Gridded simulation, QC checks documented

#### Day 3 Labs
- [ ] **Lab 7:** HMIS/DHIS2 data aggregated and cleaned
- [ ] **Lab 8:** Calibration complete, optimal parameters identified
- [ ] **Lab 9:** Validation metrics calculated (R², RMSE, bias)

#### Day 4 Labs
- [ ] **Lab 10:** Seasonal forecast generated with uncertainty
- [ ] **Lab 11:** Climate scenario runs (RCP 4.5/8.5 or SSP)
- [ ] **Lab 12:** Ensemble forecast, probability maps created

#### Day 5 Lab
- [ ] **Lab 13:** Dashboard deployed (Streamlit), interactive maps functional

### Submission

**Format:** Jupyter notebooks (`.ipynb`) or Python scripts (`.py`)  
**Location:** Push to `participants/your-team/` in workshop repo  
**Deadline:** End of each day (17:30) for daily labs; Day 5 17:00 for Lab 13

**Submit via:**
```bash
git add participants/your-team/lab_X_solution.ipynb
git commit -m "Lab X completed - Team Name"
git push origin team-name/labs
```

---

## 🎯 Capstone Project (40%)

### Overview

**Team deliverable** presented on Day 5 (14:00-15:30)

**Components:**
1. **Interactive Dashboard** (Streamlit/Folium) — 15%
2. **2-Page Policy Brief** (PDF) — 10%
3. **Presentation** (15 minutes + 5 min Q&A) — 15%

### Rubric

#### 1. Interactive Dashboard (15 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Functionality** | 5 | Dashboard loads, widgets work, maps interactive |
| **Content** | 5 | Shows seasonal outlook, risk maps, time series |
| **Design** | 3 | Clean layout, intuitive navigation, visual appeal |
| **Documentation** | 2 | README with deployment instructions |

**Required elements:**
- [ ] Seasonal malaria risk map (next 3 months)
- [ ] Historical validation plot (observed vs. modeled)
- [ ] Climate scenario comparison (e.g., baseline vs. SSP5-8.5)
- [ ] Downloadable outputs (CSV, PNG)

#### 2. Policy Brief (10 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Framing** | 2 | Clear problem statement, policy relevance |
| **Methods** | 2 | VECTRI setup, data sources, calibration |
| **Results** | 3 | Key findings, validation metrics, forecasts |
| **Recommendations** | 2 | Actionable insights for decision-makers |
| **Clarity** | 1 | Concise, non-technical language, figures clear |

**Template:** [Download brief template](https://example.org/policy-brief-template.docx)

**Length:** Max 2 pages (A4), including 1-2 figures

#### 3. Presentation (15 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Content** | 5 | Context, methods, results, implications |
| **Clarity** | 4 | Logical flow, understandable to non-experts |
| **Visuals** | 3 | High-quality figures, maps, charts |
| **Delivery** | 2 | Time management, team coordination |
| **Q&A** | 1 | Responsive, demonstrates understanding |

**Format:**
- **Duration:** 15 minutes (strict)
- **Slides:** 10-15 slides recommended
- **Team:** All members present (divide speaking time)

**Suggested structure:**
1. Introduction & motivation (2 min)
2. Study area & data (2 min)
3. VECTRI setup & calibration (3 min)
4. Results: validation & forecasts (5 min)
5. Decision products & recommendations (2 min)
6. Challenges & next steps (1 min)

### Deliverable Checklist

Submit by **Friday, Dec 19, 17:00:**

- [ ] Dashboard URL (hosted on Streamlit Cloud, Heroku, or localhost instructions)
- [ ] Policy brief PDF (`team_name_brief.pdf`)
- [ ] Presentation slides (`team_name_slides.pptx` or `.pdf`)
- [ ] Code repository with `README.md`

**Submit to:** `participants/your-team/capstone/` in workshop repo

---

## 💬 Participation (20%)

### Evaluation Criteria

| Activity | Points | Description |
|----------|--------|-------------|
| **Attendance** | 8 | Present for all sessions (Days 1-5) |
| **Engagement** | 6 | Active in discussions, asks questions, helps peers |
| **Collaboration** | 4 | Team contributions, code reviews, shared insights |
| **Daily demos** | 2 | Volunteer to present findings (bonus) |

### Attendance Policy

- **Required:** ≥85% attendance (minimum 4 full days)
- **Excused absences:** Medical/emergency (notify in advance)
- **Unexcused absences:** >15% time → no certificate

**Tracked via:**
- Morning sign-in sheets
- Lab submission timestamps
- Slack activity logs

### Engagement Indicators

**Positive indicators:**
- Asking clarifying questions during lectures
- Helping teammates troubleshoot
- Sharing findings in `#results-showcase`
- Contributing to GitHub discussions
- Peer code reviews

---

## 🏆 Grading Scale

| Score | Grade | Outcome |
|-------|-------|---------|
| 90-100% | **A** (Excellent) | Certificate with Distinction |
| 80-89% | **B** (Very Good) | Certificate |
| 70-79% | **C** (Good) | Certificate |
| 60-69% | **D** (Pass) | Completion Letter (no certificate) |
| <60% | **F** (Fail) | No certificate |

---

## 📜 Certificate of Completion

### Requirements

To receive an official certificate:

1. **Attendance:** ≥85% (min. 4 full days)
2. **Grade:** ≥70% overall score
3. **Capstone:** Submitted and presented

### Certificate Details

**Issued by:** [Your Organization / ICTP / Partner Institution]  
**Signed by:** Lead Trainer + Program Director  
**Issued date:** January 31, 2026  
**Delivery:** Digital PDF via email + optional printed version

**Certificate includes:**
- Participant name
- Workshop title & dates
- Total hours (40 hours)
- Grade (optional, upon request)
- Skills acquired (climate data, VECTRI, forecasting, dashboards)

---

## 📝 Daily Quizzes (Formative, Not Graded)

### Purpose

Quick knowledge checks — **not graded**, used for learning reinforcement only.

**Format:**
- 5 questions, multiple choice
- 5 minutes at end of day
- Immediate feedback
- Optional review in morning

**Topics:**
- Day 1: Climate-malaria pathways, data formats
- Day 2: VECTRI parameters, model structure
- Day 3: Validation metrics, calibration methods
- Day 4: Forecast interpretation, uncertainty
- Day 5: Communication, stakeholder engagement

**Access:** [Menti.com/workshop-quizzes](https://menti.com) (code shared daily)

---

## 🆘 Support for Struggling Participants

If you're falling behind:

1. **Office hours:** Daily 17:30-18:30
2. **Slack help:** Post in `#technical-help`
3. **Catch-up sessions:** Lunchtime assistance available
4. **Instructor check-in:** We'll reach out proactively

!!! tip "Don't wait!"
    Notify instructors early if you're stuck. We're here to help!

---

## 🔄 Re-assessment Policy

**Failed capstone?**  
- One resubmission allowed (within 2 weeks, by Jan 15)
- Revised deliverables submitted via email
- Max grade after resubmission: 80%

**Missed labs:**
- Make-up labs possible if excused absence
- Must complete within 1 week

---

## ❓ Assessment FAQ

??? question "Can I work alone instead of a team?"
    Teams are required for capstone. Solo completion possible only with instructor approval (e.g., odd number of participants).

??? question "What if my team member isn't contributing?"
    Notify instructors. We'll address individually. Peer evaluations may adjust individual scores.

??? question "Are code errors penalized heavily?"
    No. Effort and documentation matter. Partial credit given if approach is sound.

??? question "Can I use external libraries (not in environment.yml)?"
    Yes, but document installation steps. Must not break reproducibility.

??? question "Is the dashboard required to be publicly deployed?"
    No. Localhost with clear README is acceptable. Deployment is a bonus.

---

!!! success "You've Got This!"
    The assessments are designed to reinforce learning, not trip you up. Focus on the process, collaborate, and enjoy building something impactful!

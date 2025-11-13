# Collaboration

Building a community of practice around climate-driven malaria modeling.

---

## 💬 Communication Channels

### Workshop Slack/Teams Workspace

**Primary hub for all workshop communication**

!!! info "Join the Workspace"
    **Invitation link:** Sent to registered participants via email  
    **Workspace:** `vectri-workshop-2025.slack.com`

**Channel Structure:**

| Channel | Purpose |
|---------|---------|
| `#general` | Announcements, daily schedule updates |
| `#technical-help` | Installation issues, code debugging |
| `#data-questions` | Data access, preprocessing queries |
| `#results-showcase` | Share plots, findings, dashboards |
| `#random` | Off-topic, networking, coffee chat |
| `#day1` to `#day5` | Daily discussion threads |

**Communication Guidelines:**
- **Response time:** Instructors active 08:30-18:00 UTC+3
- **Thread replies:** Keep discussions organized
- **Search first:** Check pinned messages and search history
- **Be respectful:** Follow code of conduct

---

## 📝 GitHub Collaboration

### Workshop Repository

**Main repo:** [github.com/your-org/vectri-workshop-2025](https://github.com/your-org/vectri-workshop-2025)

```bash
# Clone the repository
git clone https://github.com/your-org/vectri-workshop-2025.git
cd vectri-workshop-2025
```

### Repository Structure

```
vectri-workshop-2025/
├── notebooks/           # Jupyter notebooks for all labs
├── scripts/             # Python/bash automation scripts
├── configs/             # VECTRI configuration templates
├── data/                # Sample datasets (small files only)
├── docs/                # Additional documentation
├── participants/        # Individual/team workspaces
│   ├── team_1/
│   ├── team_2/
│   └── ...
└── environment.yml      # Conda environment
```

### Contributing Guidelines

**Submitting your work:**

1. **Fork or create branch:**
```bash
git checkout -b team-name/lab-X
```

2. **Add your notebooks/scripts:**
```bash
git add participants/your-team/lab_X_solution.ipynb
git commit -m "Add Lab X solution - Team Name"
```

3. **Push and create Pull Request:**
```bash
git push origin team-name/lab-X
```

!!! tip "Sharing is Caring"
    Share interesting findings, visualizations, or code optimizations via PR!

### Issue Tracking

**Report bugs or ask questions:**

- **Bug reports:** Use `bug` label
- **Questions:** Use `question` label
- **Feature requests:** Use `enhancement` label

**Template:**
```markdown
**Issue:** Brief description
**Lab:** Which lab/day
**Error message:** Copy-paste error (if applicable)
**Environment:** OS, Python version
**Steps to reproduce:** ...
```

---

## 👥 Team Structure

### Team Formation (Day 1)

- **Team size:** 3-4 participants
- **Mix backgrounds:** Combine climate scientists, health experts, programmers
- **Geographic diversity:** Cross-country teams encouraged

### Roles (Suggested)

| Role | Responsibilities |
|------|------------------|
| **Data Lead** | Manages data downloads, preprocessing |
| **Model Lead** | VECTRI configuration, runs, debugging |
| **Validation Lead** | Calibration, metrics, skill assessment |
| **Viz Lead** | Dashboard, maps, presentation graphics |

!!! info "Flexible Roles"
    Roles can overlap and rotate. Everyone should experience all components!

---

## 📊 Shared Resources

### Google Drive / Shared Folder

**Workshop folder:** [Link provided via email]

**Contents:**
- Presentation slides (daily)
- Supplementary reading materials
- Large datasets (shared storage)
- Recording links (after sessions)

**Organization:**
```
VECTRI Workshop 2025/
├── Slides/
│   ├── Day1_Foundations.pdf
│   ├── Day2_VECTRI_Config.pdf
│   └── ...
├── Recordings/
├── Papers/
├── Datasets/
│   ├── CHIRPS/
│   ├── ERA5/
│   └── Admin_Boundaries/
└── Team_Deliverables/
```

---

## 🤝 Code of Conduct

### Our Commitment

We are committed to providing a **welcoming, inclusive, and harassment-free** experience for everyone.

**Core principles:**
- **Respect:** Value diverse perspectives and experiences
- **Inclusivity:** Welcome participants of all backgrounds
- **Collaboration:** Support each other's learning
- **Professionalism:** Maintain constructive dialogue

### Expected Behavior

✅ **Do:**
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Give and gracefully accept constructive feedback
- Focus on what's best for the community
- Show empathy towards others

❌ **Don't:**
- Use sexualized language or imagery
- Make derogatory comments or personal attacks
- Engage in trolling or inflammatory behavior
- Publish others' private information without permission
- Conduct yourself unprofessionally

### Reporting Issues

**Contact:**
- **Workshop organizer:** Yonas Mersha ([email@example.org](mailto:email@example.org))
- **Anonymous reporting:** [Form link]

**Response:** All complaints will be reviewed and investigated promptly and fairly.

---

## 🔒 Data Governance & Ethics

### Health Data Handling

!!! warning "Sensitive Data"
    Malaria case data from HMIS/DHIS2 is **personal health information**. Handle responsibly!

**Guidelines:**

1. **Aggregation:** Use only aggregated data (no individual-level)
2. **Anonymization:** Remove identifiers before sharing
3. **Access control:** Keep data within secure environments
4. **Sharing:** Get explicit permission before publishing
5. **Retention:** Delete data after workshop (unless authorized to keep)

### DHIS2 / HMIS Data Protocol

**Before using health data:**

- [ ] Confirm data use agreement with Ministry of Health
- [ ] Aggregate to district/regional level minimum
- [ ] Remove patient identifiers
- [ ] Secure storage (encrypted drives)
- [ ] No public GitHub uploads of raw data

### Climate Data

**Public datasets (CHIRPS, ERA5):**
- Freely shareable
- Cite appropriately in publications
- Follow dataset-specific licenses

---

## 📅 Collaboration Calendar

### Key Dates

| Date | Event |
|------|-------|
| **Dec 12-14** | Pre-workshop office hours |
| **Dec 15-19** | Workshop week |
| **Dec 20-31** | Capstone project buffer (optional) |
| **Jan 15, 2026** | Final capstone submissions |
| **Jan 31, 2026** | Certificates issued |

### Post-Workshop Community

**Stay connected:**

- **Monthly meetups:** First Friday (virtual)
- **Slack stays open:** Ongoing support
- **LinkedIn group:** [VECTRI Practitioners](https://linkedin.com/groups/...)
- **Annual reunion:** Next workshop in 2026

---

## 🎓 Peer Learning

### Daily Demos (17:00-17:30)

**Volunteer to present:**
- Interesting finding from the day
- Creative visualization
- Troubleshooting tip
- 5 minutes per team

### Knowledge Sharing

**Wiki / Documentation:**

Contribute to workshop Wiki:
- [github.com/your-org/vectri-workshop-2025/wiki](https://github.com/your-org/vectri-workshop-2025/wiki)

**Topics to document:**
- Installation workarounds
- Optimization tricks
- Dataset tips
- Regional calibration notes

---

## 🌍 Regional Network

### East Africa Climate-Health Community

Building a regional community of practice:

**Organizations involved:**
- ICPAC (IGAD Climate Prediction Center)
- National Meteorological Services
- Ministries of Health (Kenya, Uganda, Tanzania, Ethiopia, Rwanda)
- Universities & research institutes
- WHO AFRO

**Future collaboration:**
- Operational malaria early warning systems
- Joint research publications
- Funding proposals
- Regional training initiatives

---

## 📧 Contact Information

### Workshop Team

| Name | Role | Email |
|------|------|-------|
| **Yonas Mersha** | | [yonas.mersha14@gmail.com](mailto:yonas.mersha14@gmail.com) |




---

!!! success "Let's Build Together!"
    This workshop is just the beginning. Together, we're building capacity for climate-informed malaria control across East Africa.

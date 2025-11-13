<div class="hero-banner" markdown>

# Climate-Driven Malaria Modeling with VECTRI

**One-Week Training Workshop**

<span class="workshop-date">📅 December 15–19, 2025</span>

</div>

## Overview

This training is designed to help participants understand how climate-driven malaria modeling using VECTRI can be used to enhance malaria early warning systems and support evidence-based public health interventions in Ethiopia. In particular, this training is prepared in collaboration between the **Swedish Meteorological and Hydrological Institute (SMHI)** and **Addis Ababa University (AAU)** to support participants from the **Ethiopian Meteorological Institute (EMI)**. 

It will cover both foundational concepts and hands-on practical applications using real-world data from the Amhara region. This training is financed by the **Swedish International Development Cooperation Agency (Sida)** as part of the **Water and Climate Change Services for Africa, Ethiopia (WACCA-E), phase 2** project.

---

## Workshop Details

| | |
|---|---|
| **Dates** | Monday–Friday, December 15–19, 2025 |
| **Time** | 09:00–17:00 daily (UTC+03:00, Addis Ababa) |
| **Duration** | 5 Days |
| **Format** | In-person (mix of lectures, practical exercises, and discussions) |
| **Participants** | Up to 15 participants |
| **Venue** | Addis Ababa, Ethiopia |

---

## Target Audience

- **EMI hydrology and meteorology team**
- **Masters and PhD students from AAU**
- Public health professionals
- Researchers and practitioners interested in applying climate-driven modeling techniques to malaria prediction and control

---

## Learning Outcomes

By the end of this training, participants will be able to:

1. Source, quality check, and preprocess ERA5/CHIRPS climate data into daily, VECTRI-ready NetCDF format (rainfall, 2-m temperature)
2. Compile and run VECTRI; interpret outputs (EIR - Entomological Inoculation Rate, HBR - Human Biting Rate, cases) and evaluate lags (EIR→cases)
3. Understand the biological basis of malaria transmission and how climate variables drive vector and parasite dynamics
4. Create environmental input files (population, land cover) for VECTRI modeling
5. Conduct spatial and temporal analysis of model outputs to identify malaria transmission hotspots and seasonal patterns
6. Prototype a simple early-warning workflow for Amhara's Kiremt/Belg seasonality
7. Communicate findings effectively for public health decision-making

---

## Daily Structure (Quick Glance)

- **Day 1:** Foundations and Setup - Malaria-climate link, VECTRI overview, Linux basics & installation
- **Day 2:** Climate Data Preparation - ERA5/CHIRPS data access, quality control, and NetCDF processing
- **Day 3:** Environmental Factors - Population data, land cover, and creating VECTRI environmental data files
- **Day 4:** Running and Evaluating VECTRI - Amhara case study simulation and model validation
- **Day 5:** Toward Operations - Early warning system prototype and participant presentations

---

## Requirements

!!! warning "Prerequisites"
    - **Basic Python programming** skills (Pandas, NumPy, Matplotlib)
    - **Basic Linux command-line** skills
    - **Personal laptop** (Linux preferred; Windows users must have WSL2 installed)

### Software & Tools
- Python 3.8+ (Jupyter Notebooks)
- VECTRI model (compiled from source)
- Linux/Unix environment (native or WSL2)
- NetCDF utilities (nco, cdo)

### Key Datasets
- **Climate:** ERA5/ERA5-Land (temperature, precipitation), CHIRPS (rainfall) for Amhara region (2013-2019)
- **Malaria:** EPHI confirmed case data by district (2013-2019)
- **Environmental:** WorldPop population density, land cover data
- **Geographic:** Amhara administrative boundaries (shapefiles)

---

## Facilitators

<div class="facilitators-grid">
  <div class="facilitator-card">
    <h3>Yonas Mersha</h3>
    <p class="affiliation">International Livestock Research Institute (ILRI)</p>
  </div>
  
  <div class="facilitator-card">
    <h3>Dr. Alemayehu Mengesha</h3>
    <p class="affiliation">Addis Ababa University (AAU)</p>
  </div>
  
  <div class="facilitator-card">
    <h3>Dr. Natei Ermias</h3>
    <p class="affiliation">Addis Ababa University (AAU)</p>
  </div>
  
  <div class="facilitator-card">
    <h3>Dr. Bode Gbobaniyi</h3>
    <p class="affiliation">Swedish Meteorological and Hydrological Institute (SMHI)</p>
  </div>
</div>

---

## Interactive Learning with Binder

Experience hands-on learning with our interactive Jupyter notebooks! No installation required - just click and start coding.

<div class="binder-section">
  <div class="binder-content">
    <a href="https://mybinder.org/v2/gh/your-org/vectri-workshop-2025/main" target="_blank" rel="noopener" class="binder-button">
      <img src="https://mybinder.org/badge_logo.svg" alt="Launch Binder" />
      <span>Launch Interactive Environment</span>
    </a>
    <p class="binder-description">
      Includes all lessons, sample climate data, and pre-configured Python environment.
    </p>
  </div>
  
  <div class="binder-info">
    <h4>💡 What is Binder?</h4>
    <p>
      A free service that turns our GitHub repository into a live, interactive Jupyter environment. 
      Perfect for following along with lessons or experimenting with code!
    </p>
  </div>
</div>

---

## 💬 Real-Time Collaboration

Join our dedicated real-time collaborative space for Q&A, notes, and discussions during training sessions:

<div class="collaboration-section">
    <!-- https://mensuel.framapad.org/p/sd4kzsefdk-ahvu
    https://etherpad.wikimedia.org/p/zUfnxQWMHmdzQZYnDI8I -->
   <!-- https://rustpad.io/#UsvH7I -->
  <a href="https://etherpad.wikimedia.org/p/zUfnxQWMHmdzQZYnDI8I" target="_blank" rel="noopener" class="collab-button">
    <span class="collab-icon">🚀</span>
    <span class="collab-text">Join Training Pad</span>
  </a>
</div>

For more collaboration options, visit our [full collaboration guide](collaboration.md).

---


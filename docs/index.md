<div class="hero-banner" markdown>

# Climate-Driven Malaria Modeling with VECTRI

**One-Week Training Workshop**

<span class="workshop-date">📅 December 8–12, 2025</span>

</div>

## Overview

This training is designed to help participants understand how climate-driven malaria modeling using VECTRI can be used to enhance malaria early warning systems and support evidence-based public health interventions in Ethiopia. In particular, this training is prepared in collaboration between the **Swedish Meteorological and Hydrological Institute (SMHI)** and **Addis Ababa University (AAU)** to support participants from the **Ethiopian Meteorological Institute (EMI)**. 

It will cover both foundational concepts and hands-on practical applications using real-world data from the Amhara region. This training is financed by the **Swedish International Development Cooperation Agency (Sida)** as part of the **Water and Climate Change Services for Africa, Ethiopia (WACCA-E), phase 2** project.

---

## Workshop Details

| | |
|---|---|
| **Dates** | Monday–Friday, December 8–12, 2025 |
| **Time** | 09:00–17:00 daily (UTC+03:00, Addis Ababa) |
| **Duration** | 5 Days |
| **Format** | In-person (mix of lectures, practical exercises, and discussions) |
| **Participants** | Up to 15 participants |
| **Venue** | Elilly Hotel, Addis Ababa, Ethiopia |

---

## Target Audience

- **EMI hydrology and meteorology team**
- **Masters and PhD students from AAU**

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

- **Climate:** 
    - Rainfall 
        - Historical: CHIRPS, ARC2, TAMSAT
        - Near-real-time: CHIRPS-GEFS, NCEP-GFS, ECMWF HRES
        - Sub-seasonal: ECMWF S2S (WMO S2S database)
        - Seasonal: ECMWF seasonal / extended-range (C3S)
        - Long-term projections: CMIP6, ISIMIP3b, CHC-CMIP6, Regional products (e.g. CORDEX, CHC-CMIP6)

    - Temperature:
        - Historical: ERA5/ERA5-Land
        - Near-real-time: NCEP-GFS, ECMWF HRES
        - Sub-seasonal: ECMWF S2S
        - Seasonal: ECMWF SEAS5, NCEP CFSv2, NMME
        - Long-term projections: ISIMIP3b (CMIP6-based)	

- **Population data:** 
    - AFRIPOP
    - GRUMP
    - WorldPop/HRSL
  
- **Geographic:** 
    - Administrative boundaries (shapefiles) GADM/FAO GAUL
    - Land cover data
    - Soil Type Map

- **Malaria:** EPHI confirmed case data

--- 

## Facilitators


<div class="facilitators-grid">
  <div class="facilitator-card">
    <h3>Dr. Addisu Gezahegn</h3>
    <p class="affiliation">NSF Science and Technology Center, Columbia University</p>
  </div>

  <div class="facilitator-card">
    <h3>Dr. Bode Gbobaniyi</h3>
    <p class="affiliation">Swedish Meteorological and Hydrological Institute (SMHI)</p>
  </div>

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
    <h3>Hailu Fentaw</h3>
    <p class="affiliation">Addis Ababa University (AAU)</p>
  </div>

  <div class="facilitator-card">
    <h3>Fitsum Bekele</h3>
    <p class="affiliation">Addis Ababa University (AAU)</p>
  </div>
  
  <div class="facilitator-card">
    <h3>Samson Warkaye</h3>
    <p class="affiliation">Addis Ababa University (AAU)</p>
  </div>
  
</div>

---

## Interactive Learning with Binder

Experience hands-on learning with our interactive Jupyter notebooks! No installation required - just click and start coding.

<div class="binder-section">
  <div class="binder-content">
    <a href="https://mybinder.org/v2/gh/YonSci/vectri-mkdocs/main" target="_blank" rel="noopener" class="binder-button">
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

## Participants List 

| No. | Name              | Department/Desk | Email                       |
|-----|-------------------|-----------------|-----------------------------|
| 1   | Tarekgn Abera     | ISOMS           | tatarish59@gmail.com        |
| 2   | Desalegn Tarekgn  | Health Met      | desalegntarekegn@gmail.com  |
| 3   | Ayalew Tassew     | HealthMet       | ayalewtasew8@gmail.com      |
| 4   | Tamirat Yohannes  | Hydromet        | yohannestamirat81@gmail.com |
| 5   | Alemu Gamini      | Hydro met       | alemugamini@gmail.com       |
| 6   | Kidus Belay       | Agromet         | kibe_302001@yahoo.com       |
| 7   | Yimer Assefa      | Agromet         | yimera649@gmail.com         |
| 8   | Gebremariam Adane | Healthmet       | gebremariamadane@gmail.com  |
| 9   | Sintayhu Tewabe   | Agomet          | santazewdu18@gmail.com      |
| 10  | Chaka Natai       | Halthmet        | chakanatae832@gmail.com     |
| 11  | Rahele Yirdaw     | MFEW            | rahelyirdaw21@gmail.com     |

---
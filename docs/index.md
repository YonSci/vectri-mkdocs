<div class="hero-banner" markdown>

# Climate-Driven Malaria Modeling with VECTRI

**One-Week Training Workshop**

<span class="workshop-date">📅 December 8–12, 2025</span>

</div>

<style>
.vectri-carousel {
  position: relative;
  max-width: 100%;
  margin: 2rem 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  overflow: hidden;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
}

.carousel-slide {
  display: none;
  width: 100%;
  height: 100%;
  position: absolute;
  opacity: 0;
  transition: opacity 0.6s ease-in-out;
}

.carousel-slide.active {
  display: block;
  opacity: 1;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #f8f9fa;
}

.carousel-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: white;
  padding: 2rem;
  text-align: center;
}

.carousel-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: white;
}

.carousel-content p {
  margin: 0;
  font-size: 1rem;
  opacity: 0.95;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  color: #1a237e;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.carousel-nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.carousel-nav.prev {
  left: 20px;
}

.carousel-nav.next {
  right: 20px;
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}

.carousel-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-indicator.active {
  background: white;
  transform: scale(1.2);
}

@media (max-width: 768px) {
  .carousel-container {
    height: 400px;
  }
  
  .carousel-nav {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .carousel-nav.prev {
    left: 10px;
  }
  
  .carousel-nav.next {
    right: 10px;
  }
  
  .carousel-content {
    padding: 1.5rem;
  }
  
  .carousel-content h4 {
    font-size: 1.2rem;
  }
  
  .carousel-content p {
    font-size: 0.9rem;
  }
}
</style>

<div class="vectri-carousel">
  <div class="carousel-container">
    <div class="carousel-slide active">
      <img src="assets/img/spatial_map_vector.png" alt="Mosquito Density Spatial Map" />
      <div class="carousel-content">
        <h4>Spatial Patterns</h4>
        <p>Time-averaged mosquito density showing transmission hotspots</p>
      </div>
    </div>
    <div class="carousel-slide">
      <img src="assets/img/temporal_series_vector.png" alt="Vector Density Time Series" />
      <div class="carousel-content">
        <h4>Temporal Dynamics</h4>
        <p>Seasonal cycles in vector populations over time</p>
      </div>
    </div>
    <div class="carousel-slide">
      <img src="assets/img/spatial_map_eir.png" alt="EIR Spatial Map" />
      <div class="carousel-content">
        <h4>Disease Metrics</h4>
        <p>Entomological Inoculation Rate (EIR) distribution</p>
      </div>
    </div>
    <div class="carousel-slide">
      <img src="assets/img/monthly_clim_vector_density.png" alt="Monthly Climatology" />
      <div class="carousel-content">
        <h4>Seasonal Analysis</h4>
        <p>Average seasonal cycle of vector density</p>
      </div>
    </div>
    <div class="carousel-slide">
      <img src="assets/img/seasonal_map_vector_density.png" alt="Seasonal Spatial Maps" />
      <div class="carousel-content">
        <h4>Seasonal Maps</h4>
        <p>Transmission patterns across different seasons</p>
      </div>
    </div>
    <div class="carousel-slide">
      <img src="assets/img/correlation_matrix.png" alt="Correlation Matrix" />
      <div class="carousel-content">
        <h4>Variable Relationships</h4>
        <p>Correlations between key VECTRI variables</p>
      </div>
    </div>
    
    <button class="carousel-nav prev" onclick="changeSlide(-1)">‹</button>
    <button class="carousel-nav next" onclick="changeSlide(1)">›</button>
    
    <div class="carousel-indicators" id="indicators"></div>
  </div>
</div>

<script>
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const totalSlides = slides.length;
let autoSlideInterval;

// Create indicators
const indicatorsContainer = document.getElementById('indicators');
for (let i = 0; i < totalSlides; i++) {
  const indicator = document.createElement('div');
  indicator.className = 'carousel-indicator' + (i === 0 ? ' active' : '');
  indicator.onclick = () => goToSlide(i);
  indicatorsContainer.appendChild(indicator);
}

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('active', i === index);
  });
  
  const indicators = document.querySelectorAll('.carousel-indicator');
  indicators.forEach((indicator, i) => {
    indicator.classList.toggle('active', i === index);
  });
}

function changeSlide(direction) {
  currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
  showSlide(currentSlide);
  resetAutoSlide();
}

function goToSlide(index) {
  currentSlide = index;
  showSlide(currentSlide);
  resetAutoSlide();
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
}

function resetAutoSlide() {
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
}

// Initialize auto-slide
resetAutoSlide();

// Pause on hover
const carousel = document.querySelector('.vectri-carousel');
carousel.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
carousel.addEventListener('mouseleave', resetAutoSlide);
</script>

<p style="text-align: center; margin-top: 1.5rem;">
  <a href="day5/07-vectri-analyzing-outputs-visualizations/" style="color: #1565c0; text-decoration: none; font-weight: 500; font-size: 1.1rem;">
  </a>
</p>

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

- **EMI health, hydrology and meteorology team**
- **Masters and PhD students from AAU**
- **Experts from Ethiopian Public Health Institute (EPHI)**

---

## Learning Outcomes

By the end of this training, participants will be able to:

1. Source, quality check, and preprocess ERA5/CHIRPS climate data into daily, VECTRI-ready NetCDF format (rainfall, 2-m temperature)
2. Compile and run VECTRI; interpret outputs (EIR - Entomological Inoculation Rate, HBR - Human Biting Rate, cases) and evaluate lags (EIR→cases)
3. Understand the biological basis of malaria transmission and how climate variables drive vector and parasite dynamics
4. Create environmental input files (population, soil type) for VECTRI modeling
5. Conduct spatial and temporal analysis of model outputs to identify malaria transmission hotspots and seasonal patterns

---

## Daily Structure (Quick Glance)

| Day | Theme | Lessons | Focus |
|-----|-------|---------|-------|
| **Day 1** | Foundations | 6 lessons | Theory, VECTRI introduction, model components |
| **Day 2** | Setup and Python Basics | 5 lessons | Environment setup, Linux, Python fundamentals, NumPy |
| **Day 3** | Advanced Python and Climate Data | 6 lessons | Data processing libraries, climate data access |
| **Day 4** | VECTRI Setup and Running | 5 lessons | VECTRI configuration, execution, output analysis |
| **Day 5** | Advanced Analysis | 2 lessons | Advanced visualizations, parameter sensitivity |

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
- NetCDF utilities 

### Key Datasets

- **Climate:** 
    - Rainfall 
        - Historical: **[CHIRPS](scripts/download_chirps.py)**, **[ARC2](scripts/download_arc2.py)**, **[TAMSAT](scripts/download_tamsat.py)**
        - Near-real-time: **[NCEP-GFS](scripts/download_gfs_precip_forecast.py)**, **[ECMWF HRES](scripts/download_ecmwf-hres_precip.py)**
        - Sub-seasonal: **[ECMWF S2S](scripts/download_ecmwf-s2s-precip.py)**, **[ECMWF S2S Ensemble](scripts/download_ecmwf_s2s_precip_daily_ensemble.py)**
        - Seasonal: **[ECMWF Seasonal (C3S)](scripts/download_c3s_seasonal_precip_ensmean_daily.py)** 
        - Long-term projections: **[CHC-CMIP6](scripts/download_chc_cmip6_precip_daily.py)**, CMIP6, ISIMIP3b, Regional products (e.g. CORDEX)

    - Temperature:
        - Historical: **[CHIRTS](scripts/download_chirts.py)**, **[ERA5-Land](scripts/download_era5-land-temp.py)**, **[ERA5](scripts/download_era5-temp.py)**  
        - Near-real-time: **[NCEP-GFS](scripts/download_gfs_temp_forecast.py)**, **[ECMWF HRES](scripts/download_ecmwf-hres_temp.py)**
        - Sub-seasonal: **[ECMWF S2S](scripts/download_ecmwf-s2s-temp.py)**, **[ECMWF S2S Ensemble](scripts/download_ecmwf_s2s_temp_daily_ensemble.py)**
        - Seasonal: **[ECMWF Seasonal (C3S)](scripts/download_c3s_seasonal_temp_ensmean_daily.py)**, NCEP CFSv2, NMME
        - Long-term projections: **[CHC-CMIP6](scripts/download_chc_cmip6_temp_daily.py)**, CMIP6, ISIMIP3b, Regional products (e.g. CORDEX)

- **Population data:** 
    - **[AfriPop (WorldPop)](scripts/download_afripop_worldpop.py)** 
    - **[WorldPop Projections](scripts/download_harmonized_world_soil_database.py)**


- **Soil Type/Soil Fraction:**
    - **[Harmonized World Soil Database (HWSD)](scripts/download_harmonized_world_soil_database.py)**
  
- **Geographic:** 
    - Administrative boundaries (shapefiles) GADM/FAO GAUL

- **Malaria:** EPHI confirmed case data

--- 

## Facilitators


<div class="facilitators-grid">
  <div class="facilitator-card">
    <h3><a href="https://youtu.be/yCuJHWiX3jo?si=K3ds-ZhjMYkHkZpm&t=2" target="_blank" rel="noopener" style="color: inherit; text-decoration: none;">Dr. Addisu Gezahegn</a></h3>
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

<div class="qr-code-section" style="text-align: center; margin: 1.5rem 0; padding: 1rem; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 8px; max-width: 400px; margin-left: auto; margin-right: auto;">
  <h4 style="margin-bottom: 0.75rem; color: #1a237e; font-size: 1rem;">📱 Scan to Access Workshop Materials</h4>
  <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://vectri-emi-smhi.netlify.app/&bgcolor=ffffff&color=1a237e&margin=8" alt="QR Code - VECTRI Workshop" style="border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />
  <p style="margin-top: 0.75rem; font-size: 0.8rem; color: #555; margin-bottom: 0.25rem;">
    <a href="https://vectri-emi-smhi.netlify.app/" target="_blank" style="color: #1565c0; text-decoration: none; font-weight: 500;">
      vectri-emi-smhi.netlify.app
    </a>
  </p>
  <p style="font-size: 0.75rem; color: #777; margin: 0;">
    Access on mobile device
  </p>
</div>

---

## Contact

<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-left: 4px solid #1a237e; border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <p style="margin: 0 0 1rem 0; color: #555; font-size: 0.95rem;">
    For inquiries about this workshop, please contact:
  </p>
  <div style="display: flex; align-items: flex-start; gap: 1.5rem; flex-wrap: wrap;">
    <div style="flex-shrink: 0;">
      <img src="assets/img/profile-photo.jpeg" alt="Yonas Mersha" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #1a237e; box-shadow: 0 2px 8px rgba(0,0,0,0.15);" />
    </div>
    <div style="flex: 1; min-width: 250px;">
      <h3 style="margin: 0 0 0.5rem 0; color: #1a237e; font-size: 1.25rem; font-weight: 600;">
        Yonas Mersha
      </h3>
      <p style="margin: 0 0 0.75rem 0; color: #666; font-size: 0.9rem; line-height: 1.5;">
        <strong>Hydro-Climate Modelling and ML/AI Expert</strong><br>
        International Livestock Research Institute (ILRI)
      </p>
      <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem;">
        <p style="margin: 0; font-size: 0.95rem;">
          <a href="mailto:yonas.mersha14@gmail.com" style="color: #1565c0; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.5rem;">
            <span>📧</span>
            <span>yonas.mersha14@gmail.com</span>
          </a>
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.5rem;">
          <a href="https://www.linkedin.com/in/yonas-mersha-baab561b5/" target="_blank" rel="noopener" style="color: #0077b5; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.9rem;">
            <span>💼</span>
            <span>LinkedIn</span>
          </a>
          <a href="https://github.com/YonSci" target="_blank" rel="noopener" style="color: #333; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.9rem;">
            <span>💻</span>
            <span>GitHub</span>
          </a>
          <a href="https://medium.com/@yonas.mersha14" target="_blank" rel="noopener" style="color: #00ab6c; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.9rem;">
            <span>✍️</span>
            <span>Medium</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---
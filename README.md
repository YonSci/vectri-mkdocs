# 🦟 Climate-Driven Malaria Modeling with VECTRI

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/YonSci/vectri-mkdocs)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://your-site.netlify.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the **Climate-Driven Malaria Modeling with VECTRI** workshop website! This comprehensive 5-day training program (December 15-19, 2025) teaches participants how to use the VECTRI model to enhance malaria early warning systems and support evidence-based public health interventions in Ethiopia.

## 🎯 Overview

This training is designed to help participants understand how climate-driven malaria modeling using VECTRI can be used to enhance malaria early warning systems. Prepared in collaboration between the **Swedish Meteorological and Hydrological Institute (SMHI)** and **Addis Ababa University (AAU)**, this workshop supports participants from the **Ethiopian Meteorological Institute (EMI)**.

**Training Period:** December 15-19, 2025  
**Mode:** In-person (mix of lectures, practical exercises, and discussions)  
**Participants:** Up to 15 participants

### 🤝 Partners

- **EMI** - Ethiopian Meteorological Institute
- **AAU** - Addis Ababa University
- **SMHI** - Swedish Meteorological and Hydrological Institute

### 💰 Funding

This training is financed by the **Swedish International Development Cooperation Agency (Sida)** as part of the **Water and Climate Change Services for Africa, Ethiopia (WACCA-E), phase 2** project.

## 📚 Learning Outcomes

By the end of this training, participants will be able to:

1. Source, quality check, and preprocess ERA5/CHIRPS climate data into VECTRI-ready NetCDF format
2. Compile and run VECTRI; interpret outputs (EIR, HBR, cases) and evaluate lags
3. Understand the biological basis of malaria transmission and climate drivers
4. Create environmental input files (population, land cover) for VECTRI modeling
5. Conduct spatial and temporal analysis to identify transmission hotspots
6. Prototype a simple early-warning workflow for Amhara's seasonality
7. Communicate findings effectively for public health decision-making

## 🛠️ Technologies Used

- **MkDocs** - Static site generator
- **Material for MkDocs** - Modern, responsive theme
- **Python 3.8+** - Programming language for data processing
- **VECTRI Model** - Climate-driven malaria transmission model
- **ERA5/CHIRPS** - Climate reanalysis datasets
- **Jupyter Notebooks** - Interactive computing
- **Binder** - Interactive online environment
- **Netlify** - Hosting and deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Text editor or IDE

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/YonSci/vectri-mkdocs.git
cd vectri-mkdocs
```

2. **Create a virtual environment:**

```bash
# Windows
python -m venv vec-env
vec-env\Scripts\activate

# Linux/Mac
python3 -m venv vec-env
source vec-env/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the development server:**

```bash
mkdocs serve
```

5. **Open your browser:**

Navigate to `http://127.0.0.1:8000`

## 📦 Building for Production

To build the static site:

```bash
mkdocs build
```

The built site will be in the `site/` directory.

## 🌐 Deployment

### Deploy to Netlify

1. Push your repository to GitHub
2. Log in to [Netlify](https://www.netlify.com/)
3. Click "New site from Git"
4. Select your repository
5. Set build command: `mkdocs build`
6. Set publish directory: `site`
7. Click "Deploy site"

### Continuous Deployment

Every push to the `main` branch will automatically trigger a new deployment on Netlify.

## 📖 Documentation Structure

```
vectri-mkdocs/
├── docs/
│   ├── index.md              # Home page
│   ├── prerequisites.md      # Prerequisites and requirements
│   ├── setup.md             # Setup instructions
│   ├── schedule.md          # Daily schedule
│   ├── lessons.md           # Hands-on labs
│   ├── assessments.md       # Evaluation and quizzes
│   ├── collaboration.md     # Collaboration hub
│   ├── resources.md         # Additional resources
│   ├── quizzes/             # Interactive quizzes
│   │   ├── xarray-interactive.md
│   │   └── README.md
│   ├── assets/
│   │   ├── css/
│   │   │   └── custom.css   # Custom styles
│   │   └── img/             # Images and logos
│   └── overrides/
│       └── partials/
│           └── footer.html  # Custom footer
├── mkdocs.yml               # MkDocs configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── LICENSE                 # MIT License
```

## 🎓 Training Modules

### Day 1: Foundations and Setup
- Malaria-climate link and Ethiopian context
- VECTRI model overview
- Linux basics and VECTRI installation

### Day 2: Climate Data Preparation
- ERA5/CHIRPS data access and processing
- Building VECTRI climate input files

### Day 3: Environmental Factors
- Population data processing
- Creating VECTRI environmental data files

### Day 4: Running VECTRI
- Model configuration and execution
- Output analysis and validation

### Day 5: Early Warning Systems
- Spatial and temporal analysis
- Prototyping operational workflows

## 🎯 Interactive Features

- **📊 Interactive Quizzes** - Test your knowledge with instant scoring
- **🚀 Binder Integration** - Launch interactive Jupyter environments
- **💬 Real-Time Collaboration** - Shared collaboration pad for Q&A
- **🎨 Modern UI** - Beautiful, responsive design with dark mode
- **📱 Mobile-Friendly** - Works seamlessly on all devices

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

### Development Guidelines

- Follow the existing code style
- Update documentation for any new features
- Test your changes locally before submitting
- Write clear commit messages

## 📧 Contact

**Yonas Mersha** - Training Coordinator  
📧 Email: [yonas.mersha14@gmail.com](mailto:yonas.mersha14@gmail.com)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sida** - Swedish International Development Cooperation Agency for funding
- **SMHI** - Swedish Meteorological and Hydrological Institute
- **AAU** - Addis Ababa University
- **EMI** - Ethiopian Meteorological Institute
- **EPHI** - Ethiopian Public Health Institute for malaria surveillance data
- All workshop participants and contributors

## 📚 Additional Resources

- **VECTRI Model:** [VECTRI Documentation](https://vectri.org)
- **ERA5 Data:** [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
- **CHIRPS Data:** [Climate Hazards Center](https://www.chc.ucsb.edu/data/chirps)
- **MkDocs:** [MkDocs Documentation](https://www.mkdocs.org/)
- **Material for MkDocs:** [Material Theme](https://squidfunk.github.io/mkdocs-material/)

## 🌟 Star History

If you find this project helpful, please consider giving it a star ⭐!

---

<div align="center">
  <p>Built with ❤️ for climate-informed malaria control in East Africa</p>
  <p>© 2025 VECTRI Workshop. All rights reserved.</p>
</div>


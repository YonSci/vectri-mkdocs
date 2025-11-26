# 🌡️ Malaria-Climate Link: Understanding the Connection

Welcome to the foundational theory behind climate-driven malaria modeling! This lecture explores how climate variables shape malaria transmission dynamics and why models like VECTRI are essential for forecasting and intervention planning.

---

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

!!! success "What You'll Master"
    
    **🌍 Climate-Biology Interactions**
    
    - Understand how climate variables (**temperature**, **rainfall**, **humidity**, and **hydrology**) control mosquito vector and *Plasmodium* parasite life cycles
    - Identify critical thresholds and optimal conditions for development and survival
    
    **📊 Epidemiological Metrics**
    
    - Grasp key rates and probabilities:
        - Development rates (larval, gonotrophic, sporogonic)
        - Survival probabilities (larvae, adults)
        - Biting rates and host interactions
        - Entomological Inoculation Rate (EIR)
        - Transmission probabilities (vector ↔ host)
    - Understand how these metrics respond dynamically to climate
    
    **🖥️ Modeling Framework**
    
    - Recognize the role of models like **VECTRI** in integrating climate data
    - Understand nonlinear responses and spatial dynamics in transmission forecasting

---

## 📚 Lecture Outline

This lecture is organized into six interconnected modules:

<div class="grid cards" markdown>

-   :material-thermometer-alert:{ .lg .middle } __1. Climate-Sensitive Transmission System__

    ---

    Explore the fundamental relationships between climate and malaria transmission
    
    [:octicons-arrow-right-24: Jump to Section](#1-malaria-as-a-climate-sensitive-transmission-system)

-   :material-bug:{ .lg .middle } __2. Vector Life Cycle__

    ---

    Understand mosquito development from larvae to adults and climate dependencies
    
    [:octicons-arrow-right-24: Jump to Section](#12-vector-life-cycle-components)

-   :material-bacteria:{ .lg .middle } __3. Parasite Development__

    ---

    Learn how *Plasmodium* parasites develop inside mosquito vectors
    
    [:octicons-arrow-right-24: Jump to Section](#13-parasite-development)

-   :material-account-group:{ .lg .middle } __4. Host Dynamics__

    ---

    Examine human population factors affecting transmission intensity
    
    [:octicons-arrow-right-24: Jump to Section](#14-host-dynamics)

-   :material-water:{ .lg .middle } __5. Environmental Factors__

    ---

    Discover how hydrology creates and sustains breeding habitats
    
    [:octicons-arrow-right-24: Jump to Section](#15-environmental-factors)

-   :material-chart-line:{ .lg .middle } __6. Modeling Approaches__

    ---

    Introduction to dynamical models for malaria transmission
    
    [:octicons-arrow-right-24: Jump to Section](#16-modeling-malaria-transmission)

</div>

---

## 1. Malaria as a Climate-Sensitive Transmission System

### 1.1 Climate and Health Relationship

Malaria is one of the most climate-sensitive diseases on Earth. Understanding this relationship is crucial for predicting transmission patterns and planning interventions.

#### 🌐 Overview of Climate-Health Links

!!! info "Core Concept"
    Malaria transmission is a complex system where climate factors simultaneously affect:
    
    - **Vectors** (mosquitoes): development, survival, behavior
    - **Parasites** (*Plasmodium*): maturation rates, infectivity
    - **Humans**: exposure patterns, immunity dynamics

The transmission cycle requires all three components to align within favorable climate conditions. A disruption in any component can halt transmission entirely.

---

#### 🌡️ Climate Drivers of Malaria

Climate affects malaria transmission through multiple pathways:

=== "Temperature"

    **Impact on Biology**
    
    - **Larval Development**: Higher temperatures accelerate development (within limits)
        - Minimum threshold: ~16°C for most *Anopheles* species
        - Optimal range: 25-28°C
        - Lethal threshold: >37°C
    
    - **Adult Survival**: Bell-shaped relationship
        - Too cold: metabolic shutdown
        - Optimal: 20-25°C
        - Too hot: desiccation and heat stress
    
    - **Parasite Development (EIP)**: Exponentially sensitive
        - Below 16°C: parasites cannot complete development
        - At 20°C: EIP ≈ 23 days
        - At 30°C: EIP ≈ 9 days
    
    !!! warning "Critical Threshold"
        For transmission to occur, mosquitoes must **survive longer than the EIP**. This creates a temperature-dependent transmission threshold around 18-20°C.

=== "Rainfall"

    **Impact on Breeding Habitat**
    
    - **Breeding Site Creation**: Rain creates temporary pools
        - Light rain (1-10 mm/day): maintains existing sites
        - Heavy rain (>30 mm/day): creates new sites but flushes larvae
    
    - **Habitat Persistence**: Balance between inflow and evaporation
        - Dry periods: breeding sites dry up → population collapse
        - Wet periods: abundant habitat → population expansion
    
    - **Seasonal Patterns**: Transmission often peaks 1-2 months after peak rainfall
    
    !!! tip "Regional Variation"
        - **Sahel**: Strong seasonal transmission follows monsoon rains
        - **Tropics**: Year-round transmission with wet season peaks
        - **Highlands**: Transmission limited to warm, wet periods

=== "Humidity"

    **Impact on Adult Survival**
    
    - **Desiccation Risk**: Low humidity shortens mosquito lifespan
        - <40% RH: severe survival penalty
        - 60-80% RH: optimal
        - >95% RH: little additional benefit
    
    - **Flight Behavior**: Humidity affects host-seeking
        - High humidity: increased flight activity
        - Low humidity: mosquitoes shelter, reducing biting
    
    - **Indoor vs Outdoor**: Houses often provide more stable humidity
    
    !!! example "Practical Implication"
        Desert-edge regions may have low transmission despite adequate rainfall due to low humidity limiting mosquito survival.

=== "Hydrology"

    **Impact on Breeding Sites**
    
    - **Temporary Pools**: Created by rainfall, evaporation, infiltration
        - Duration: 1-3 weeks typical
        - Productivity: high (fewer predators)
    
    - **Permanent Water Bodies**: Rivers, lakes, wetlands
        - Duration: year-round
        - Productivity: lower (more predators, competition)
    
    - **Irrigation Systems**: Human-managed water
        - Can create stable breeding habitat
        - Extends transmission seasons
    
    !!! danger "Development Impact"
        Irrigation and dam projects can dramatically increase malaria risk by creating stable breeding habitats year-round.

---

#### 📈 Typical Climate Sensitivities of Vector-Borne Diseases (VBDs)

Vector-borne diseases show **nonlinear** responses to climate variables. Small changes near critical thresholds can produce large changes in transmission.

!!! abstract "Key Nonlinearities"
    
    **1. Temperature Thresholds**
    
    - **Lower threshold**: Below this, development cannot occur
    - **Optimal range**: Rapid development, high transmission
    - **Upper threshold**: Above this, mortality increases rapidly
    
    **Example**: A shift from 18°C to 20°C can enable transmission. A shift from 25°C to 27°C may triple transmission intensity.
    
    **2. Rainfall Thresholds**
    
    - **Minimum**: Insufficient breeding habitat
    - **Optimal**: Maximum habitat without excessive flushing
    - **Maximum**: Heavy flushing reduces larval survival
    
    **Example**: 50 mm/month may produce little transmission. 150 mm/month may be highly favorable. 400 mm/month may reduce transmission due to flushing.
    
    **3. Seasonal Amplification**
    
    - Transmission is concentrated when **multiple** factors are simultaneously favorable
    - Even short favorable periods can produce epidemics
    
    **Example**: A single month of optimal conditions can sustain transmission for 2-3 months due to population momentum.

---

#### 🔗 Non-Climate Interactions

Climate doesn't act in isolation. Its impact on malaria is **modulated** by human and environmental factors:

=== "Land Use"

    **How It Modifies Climate Impact**
    
    - **Deforestation**: 
        - Increases temperature (loss of shade)
        - Creates sun-lit pools (favorable for *An. gambiae*)
        - Reduces humidity
    
    - **Urbanization**:
        - Urban heat island effect (higher temperatures)
        - Reduces breeding sites (paved surfaces)
        - Changes mosquito species composition
    
    - **Agriculture**:
        - Irrigation creates stable breeding sites
        - Rice paddies particularly favorable
        - Can override seasonal rainfall patterns

=== "Population Density"

    **How It Affects Transmission**
    
    - **Low Density** (<10 people/km²):
        - Mosquitoes feed on animals (zoophily)
        - Low human biting rate
        - Low transmission despite high vector density
    
    - **Intermediate Density** (10-500 people/km²):
        - Transition to human feeding (anthropophily)
        - Maximum per-person biting rate
        - Highest transmission risk
    
    - **High Density** (>500 people/km²):
        - Vector abundance limited
        - Per-person biting rate decreases
        - Transmission may decline

=== "Interventions"

    **How They Interact with Climate**
    
    - **Insecticide-Treated Nets (ITNs)**:
        - Reduce biting rates regardless of climate
        - Effectiveness may vary with mosquito behavior
        - Climate affects compliance (too hot → net usage drops)
    
    - **Indoor Residual Spraying (IRS)**:
        - Targets indoor-resting mosquitoes
        - Effectiveness depends on mosquito behavior
        - Climate affects spray persistence
    
    - **Larval Source Management**:
        - Reduces breeding sites
        - Effectiveness depends on hydrology
        - Rain can overwhelm control efforts
    
    !!! warning "Climate-Intervention Feedback"
        Climate change may shift mosquito behavior, potentially reducing effectiveness of indoor-targeted interventions like ITNs and IRS.

---

### 1.2 Vector Life Cycle Components

The mosquito vector undergoes several distinct life stages, each with unique climate sensitivities.

#### 🥚 Larval Cycle

The aquatic stages (egg → larvae → pupae → adult) are highly temperature-dependent.

!!! note "Development Stages"
    
    **1. Egg Stage** (1-3 days)
    
    - Eggs laid on water surface
    - Hatch within 2-3 days at 25°C
    - Can survive brief dry periods (some species)
    
    **2. Larval Stage** (5-14 days at 25-30°C)
    
    - Four instars (L1 → L2 → L3 → L4)
    - Feed on microorganisms
    - Most vulnerable to predation and environmental stress
    - **Temperature-driven development**:
    
    $$
    R_L = \frac{T_{wat} - T_{L,min}}{K_L}
    $$
    
    Where:
    
    - \(R_L\) = development rate (fraction per day)
    - \(T_{wat}\) = water temperature (°C)
    - \(T_{L,min}\) = minimum threshold (typically 16°C)
    - \(K_L\) = degree-days required (typically 90-100)
    
    **3. Pupal Stage** (1-2 days)
    
    - Non-feeding stage
    - Rapid metamorphosis to adult
    - Less vulnerable than larvae

**Climate Sensitivity**

| Temperature | Development Time | Notes |
|-------------|------------------|-------|
| 16°C | No development | Below threshold |
| 20°C | ~18 days | Slow development |
| 25°C | ~10 days | Optimal |
| 30°C | ~6 days | Fast but risky |
| 35°C | ~4 days | High mortality |
| >37°C | Lethal | Complete mortality |

---

#### ☠️ Larval Mortality

Larvae face multiple mortality sources, many climate-related:

=== "Predation"

    **Natural Enemies**
    
    - Fish (especially *Gambusia*)
    - Aquatic insects (dragonfly nymphs, beetles)
    - Tadpoles and frogs
    - Copepods (small crustaceans)
    
    **Climate Connection**:
    
    - Temporary pools (rain-created) → fewer predators
    - Permanent water → more predators
    - Temperature affects predator activity

=== "Crowding"

    **Density-Dependent Mortality**
    
    - Larvae compete for food
    - Waste products accumulate
    - Survival decreases as density increases
    
    **Mathematical Representation**:
    
    $$
    P_{L,surv} = P_{L,surv0} \times \left(1 - \frac{M_L}{w \times M_{L,max}}\right)
    $$
    
    Where:
    
    - \(M_L\) = larval biomass (mg/m²)
    - \(w\) = pond coverage fraction
    - \(M_{L,max}\) = carrying capacity
    
    **Climate Connection**:
    
    - Rain creates habitat → reduces crowding
    - Evaporation reduces habitat → increases crowding

=== "Rainfall Flushing"

    **Washout Effects**
    
    - Heavy rain washes larvae out of pools
    - Early instars (L1, L2) most vulnerable
    - Can cause sudden population crashes
    
    **Flushing Function**:
    
    $$
    K_{flush} = L_f + (1 - L_f) \times \left[(1 - K_{\infty}) e^{-R_d/\tau} + K_{\infty}\right]
    $$
    
    Where:
    
    - \(L_f\) = larval stage (0=early, 1=late)
    - \(R_d\) = daily rainfall (mm)
    - \(\tau\) = flushing scale (~50 mm/day)
    - \(K_{\infty}\) = survival under heavy rain (~0.4)
    
    **Implications**:
    
    - Moderate rain: beneficial (creates habitat)
    - Heavy rain: detrimental (flushes larvae)
    - Optimal: 5-15 mm/day with occasional heavier events

=== "Temperature Stress"

    **Direct Temperature Effects**
    
    - **Too Cold** (<16°C): development halts, starvation
    - **Too Hot** (>34°C): metabolic stress, hypoxia
    - **Lethal** (>37°C): protein denaturation, death
    
    - **Fluctuations**: Rapid changes more stressful than gradual
    
    **Climate Change Concern**:
    
    - More frequent heat waves → episodic die-offs
    - Warmer minimum temperatures → extended seasons

---

#### 🩸 Gonotrophic Cycle

The gonotrophic cycle is the time between blood meals and egg laying in adult female mosquitoes.

!!! info "Cycle Stages"
    
    **1. Host Seeking** (varies with hunger, temperature)
    
    - Peak activity: dusk and dawn
    - Lasts minutes to hours
    
    **2. Blood Feeding** (few minutes)
    
    - Female mosquitoes only
    - Required for egg development
    - Risk of parasite acquisition
    
    **3. Blood Digestion & Egg Maturation** (2-4 days at 25°C)
    
    - Temperature-dependent rate:
    
    $$
    R_{gono} = \frac{T_{eff} - T_{gono,min}}{K_{gono}}
    $$
    
    - \(T_{gono,min}\) ≈ 7.7°C
    - \(K_{gono}\) ≈ 37 degree-days
    
    **4. Oviposition** (egg laying)
    
    - Female seeks water body
    - Lays 50-200 eggs
    - Cycle repeats

**Temperature Impact on Gonotrophic Period**

| Temperature | Gonotrophic Period | Biting Frequency |
|-------------|-------------------|------------------|
| 15°C | ~5 days | Low |
| 20°C | ~3 days | Moderate |
| 25°C | ~2 days | High |
| 30°C | ~1.5 days | Very High |

!!! tip "Transmission Implication"
    Shorter gonotrophic cycles mean more frequent blood meals → higher transmission rates. Warmer temperatures increase biting pressure.

---

#### 💀 Vector Survival

Adult mosquito daily survival probability is **critical** for transmission because parasites require 8-30 days to develop inside the mosquito (EIP).

**Martens II Survival Model**

$$
P_{V,surv} = \exp\left(-\frac{1}{K_0 + K_1 T_{eff} + K_2 T_{eff}^2}\right)
$$

Where:

- \(K_0\) ≈ -4.4
- \(K_1\) ≈ 1.31
- \(K_2\) ≈ -0.03

This produces a **bell-shaped** relationship between temperature and survival.

**Expected Lifespan**

$$
\text{Lifespan} = \frac{1}{1 - P_{V,surv}} \text{ days}
$$

| Temperature | Daily Survival | Expected Lifespan |
|-------------|---------------|-------------------|
| 15°C | 0.70 | ~3 days |
| 20°C | 0.88 | ~8 days |
| 25°C | 0.92 | ~13 days |
| 28°C | 0.91 | ~11 days |
| 32°C | 0.85 | ~7 days |
| 35°C | 0.75 | ~4 days |

!!! danger "Transmission Threshold"
    **For malaria transmission:** Lifespan > EIP
    
    - At 20°C: EIP ≈ 23 days, Lifespan ≈ 8 days → **No transmission**
    - At 25°C: EIP ≈ 12 days, Lifespan ≈ 13 days → **Marginal transmission**
    - At 28°C: EIP ≈ 9 days, Lifespan ≈ 11 days → **Efficient transmission**

---

### 1.3 Parasite Development

#### 🦠 Sporogonic Cycle

The sporogonic cycle is the development of *Plasmodium* parasites inside the mosquito vector.

!!! abstract "Parasite Journey"
    
    **1. Gametocyte Ingestion** (during blood meal)
    
    - Mosquito ingests male and female gametocytes from human blood
    
    **2. Fertilization** (in mosquito gut, <1 day)
    
    - Gametocytes mature to gametes
    - Fertilization produces zygote
    
    **3. Ookinete Formation** (1-2 days)
    
    - Zygote develops into motile ookinete
    - Penetrates gut wall
    
    **4. Oocyst Development** (7-14 days)
    
    - Forms on outer gut wall
    - Produces thousands of sporozoites
    - **Most temperature-sensitive stage**
    
    **5. Sporozoite Migration** (1-2 days)
    
    - Oocyst ruptures
    - Sporozoites migrate to salivary glands
    - Mosquito now **infectious**

**Temperature-Dependent Development**

$$
R_{sporo} = \frac{T_{eff} - T_{sporo,min}}{K_{sporo}}
$$

Where:

- \(T_{sporo,min}\) ≈ 16°C (critical threshold)
- \(K_{sporo}\) ≈ 111 degree-days

**Extrinsic Incubation Period (EIP)**

$$
\text{EIP} = \frac{1}{R_{sporo}} = \frac{K_{sporo}}{T_{eff} - T_{sporo,min}} \text{ days}
$$

| Temperature | EIP Duration | Transmission Potential |
|-------------|--------------|------------------------|
| <16°C | Infinite | **No transmission** |
| 18°C | ~56 days | Very low |
| 20°C | ~28 days | Low |
| 25°C | ~12 days | Moderate |
| 28°C | ~9 days | High |
| 30°C | ~8 days | Very high |

!!! warning "Critical Temperature Threshold"
    **Below 16°C**: Parasites cannot complete development, regardless of time. This creates an absolute lower temperature limit for malaria transmission.

---

### 1.4 Host Dynamics

Human populations are not passive receivers of malaria; they are active components of the transmission system.

#### 👥 Host Community

**Population Density Effects**

The relationship between human population density and malaria risk is **non-monotonic** (not always increasing).

!!! example "Zoophily to Anthropophily Transition"
    
    **Low Density** (sparse rural, <10 people/km²)
    
    - Mosquitoes preferentially feed on animals (cattle, goats)
    - **Zoophilic** behavior dominant
    - Low human biting rate despite high vector abundance
    - **Result**: Low malaria risk
    
    **Intermediate Density** (rural villages, 10-500 people/km²)
    
    - Sufficient humans to attract mosquitoes
    - Livestock often present but humans preferred
    - **Anthropophilic** behavior increases
    - Maximum per-capita biting rate
    - **Result**: Highest malaria risk (per person)
    
    **High Density** (towns/cities, >500 people/km²)
    
    - Breeding sites scarce (less habitat)
    - Vectors per person decreases
    - Biting rate per person declines
    - **Result**: Lower malaria risk (per person)

**Human Biting Rate (HBR)**

$$
\text{HBR} = \frac{(1 - e^{-H/\tau_{zoo}}) \times V_{biting}}{H}
$$

Where:

- \(H\) = human population density
- \(\tau_{zoo}\) = zoophily scale (~50 people/km²)
- \(V_{biting}\) = biting mosquito density

**Entomological Inoculation Rate (EIR)**

$$
\text{EIR} = \text{HBR} \times \text{CSPR}
$$

Where CSPR = Circumsporozoite Protein Rate (fraction of infectious mosquitoes)

!!! tip "Regional Patterns"
    - **High EIR** (>100 infectious bites/person/year): Stable, endemic transmission
    - **Low EIR** (<10): Unstable, epidemic-prone transmission
    - **Climate modulates EIR** by affecting vector density and CSPR

---

#### 🛡️ Immunity

Malaria immunity is **complex**, **partial**, and **short-lived**.

!!! info "Types of Immunity"
    
    **1. Anti-Parasite Immunity**
    
    - Reduces parasite density
    - Develops slowly (years of exposure)
    - Never complete (can still be infected)
    
    **2. Anti-Disease Immunity**
    
    - Prevents severe symptoms
    - Develops faster than anti-parasite immunity
    - Adults in endemic areas often asymptomatic
    
    **3. Anti-Transmission Immunity**
    
    - Reduces gametocyte production
    - Limits mosquito infection
    - Least understood component

**Immunity Dynamics**

- **Acquisition**: Proportional to EIR (more exposure → faster acquisition)
- **Loss**: Decays with time (~1-3 years without exposure)
- **Age Patterns**:
  - Children: Low immunity → clinical malaria
  - Adults (endemic areas): Partial immunity → asymptomatic infections
  - Adults (epidemic areas): Low immunity → severe disease

!!! danger "Climate-Immunity Feedback"
    Changes in transmission intensity (climate-driven) affect immunity:
    
    - **Increased transmission** → Immunity builds faster → Fewer clinical cases (paradoxically)
    - **Decreased transmission** → Immunity wanes → More clinical cases when transmission resumes
    
    This can cause **epidemic rebound** after control efforts or climate fluctuations.

---

### 1.5 Environmental Factors

#### 💧 Surface Hydrology

Breeding sites are the foundation of mosquito populations. Their formation, persistence, and productivity depend on hydrology.

!!! abstract "Breeding Habitat Types"
    
    **Temporary Pools** (Rain-Dependent)
    
    - **Formation**: Rainfall creates pools in depressions
    - **Persistence**: Days to weeks (evaporation, infiltration)
    - **Productivity**: High (few predators, optimal conditions)
    - **Climate Sensitivity**: Very high
    - **Mosquito Species**: *An. gambiae s.s.* (Africa), *An. funestus* (when drying)
    
    **Permanent Water** (Rivers, Lakes, Wetlands)
    
    - **Formation**: Year-round water availability
    - **Persistence**: Months to permanent
    - **Productivity**: Lower (more predators, vegetation)
    - **Climate Sensitivity**: Moderate (flow and level vary)
    - **Mosquito Species**: *An. funestus*, *An. arabiensis*
    
    **Irrigation Systems** (Human-Managed)
    
    - **Formation**: Agriculture (rice, vegetables)
    - **Persistence**: Seasonal to year-round
    - **Productivity**: Very high (nutrient-rich, stable)
    - **Climate Sensitivity**: Low (managed)
    - **Mosquito Species**: All *Anopheles* species

**Pond Dynamics Model**

VECTRI represents breeding sites as a fractional pond coverage:

$$
\frac{dw}{dt} = K_w \times \left[R_d (w_{max} - w) - w(E + I)\right]
$$

Where:

- \(w\) = pond fraction (0-0.04 typically)
- \(R_d\) = daily rainfall (mm)
- \(E\) = evaporation rate (mm/day)
- \(I\) = infiltration rate (mm/day)
- \(w_{max}\) = maximum pond coverage (~4%)

!!! example "Seasonal Pattern"
    
    **Dry Season**:
    
    - Evaporation > Rainfall → \(dw/dt < 0\)
    - Ponds shrink and disappear
    - Vector populations collapse
    - Transmission ceases
    
    **Wet Season Onset**:
    
    - Rainfall > Evaporation → \(dw/dt > 0\)
    - Ponds form and expand
    - Vector populations explode (1-2 months lag)
    - Transmission intensifies
    
    **Peak Wet Season**:
    
    - Abundant habitat (high \(w\))
    - But heavy flushing reduces larval survival
    - Transmission moderate despite high rainfall
    
    **End of Wet Season**:
    
    - Moderate rainfall, low flushing
    - **Optimal conditions for transmission**
    - Often the **peak transmission period**

---

### 1.6 Modeling Malaria Transmission

#### 🖥️ Overview of Malaria Models

Mathematical models are essential for understanding malaria transmission dynamics and forecasting.

!!! quote "Why Model Malaria?"
    
    > "Malaria transmission is too complex to understand intuitively. Models provide a rigorous framework to integrate multiple processes, test hypotheses, and forecast under changing conditions."

**Model Categories**

=== "Statistical Models"

    **Characteristics**:
    
    - Based on observed patterns
    - Correlate climate with malaria cases
    - No explicit biology
    
    **Strengths**:
    
    - Simple, fast
    - Good for short-term forecasts
    - Data-driven
    
    **Weaknesses**:
    
    - Limited mechanistic understanding
    - Poor extrapolation outside training data
    - Cannot simulate interventions
    
    **Examples**:
    
    - Regression models (climate → cases)
    - Machine learning (random forests, neural nets)

=== "Compartmental Models"

    **Characteristics**:
    
    - People divided into compartments (S-E-I-R)
    - Differential equations for flows
    - Simplified vector dynamics
    
    **Strengths**:
    
    - Mechanistic insights
    - Can test interventions
    - Well-established theory
    
    **Weaknesses**:
    
    - Often spatially aggregated
    - Simplified vector biology
    - Difficult to parameterize
    
    **Examples**:
    
    - Ross-Macdonald model
    - SEIR models with vector compartments

=== "Dynamical Vector Models"

    **Characteristics**:
    
    - **Explicit vector life cycle** (larvae, adults)
    - **Climate-driven** rates and survival
    - **Spatially explicit** (gridded)
    - **Coupled to transmission** in humans
    
    **Strengths**:
    
    - Most realistic biology
    - Climate-responsive
    - Spatial dynamics captured
    - Can forecast under novel conditions
    
    **Weaknesses**:
    
    - Complex (many parameters)
    - Computationally intensive
    - Requires detailed climate data
    
    **Examples**:
    
    - **VECTRI** (our focus!)
    - Liverpool Malaria Model (LMM)
    - Hydrology-based models

**VECTRI Model Overview**

!!! success "What is VECTRI?"
    
    **VECTRI** = VECtor-borne disease community model of ICTP, TRIeste
    
    A **dynamical, climate-driven** model that simulates:
    
    1. **Breeding site hydrology** (rainfall, evaporation, infiltration)
    2. **Larval dynamics** (development, survival, crowding, flushing)
    3. **Adult mosquito populations** (emergence, survival, biting)
    4. **Parasite development** (sporogonic cycle, EIP)
    5. **Human infection dynamics** (susceptible, infected, immune)
    6. **Spatial spread** (adult dispersal, human movement)
    
    **Key Features**:
    
    - **Climate inputs**: Temperature, rainfall, humidity
    - **Resolution**: Typically 0.5° (~50 km) grid
    - **Time step**: Daily
    - **Outputs**: EIR, prevalence, clinical cases, vector density

**Model Applications**

- **Seasonal forecasting**: Predict transmission 1-6 months ahead
- **Climate change impacts**: Project future transmission zones
- **Intervention planning**: Optimize timing and targeting of control
- **Epidemic early warning**: Detect anomalous conditions

---

## 🎬 Summary

Congratulations! You've completed the theoretical foundation for climate-driven malaria modeling.

!!! success "Key Takeaways"
    
    ✅ **Climate-Transmission Links**
    
    - Temperature, rainfall, and humidity control vector and parasite biology
    - Nonlinear responses create critical thresholds
    - Transmission requires simultaneous favorable conditions
    
    ✅ **Vector Life Cycle**
    
    - Larvae: Temperature-dependent development, crowding, flushing
    - Adults: Temperature-dependent survival, gonotrophic cycle
    - Critical: Mosquito lifespan must exceed parasite EIP
    
    ✅ **Parasite Biology**
    
    - 16°C minimum threshold for development
    - EIP decreases exponentially with temperature
    - Long EIP at cooler temperatures limits transmission
    
    ✅ **Host Factors**
    
    - Population density affects biting rates (nonlinear)
    - Immunity builds with exposure, wanes without
    - Age patterns reflect cumulative exposure
    
    ✅ **Environmental Drivers**
    
    - Hydrology creates breeding habitat
    - Balance of rainfall, evaporation, infiltration
    - Seasonal patterns drive transmission cycles
    
    ✅ **Modeling Approaches**
    
    - Dynamical models like VECTRI capture climate-biology links
    - Essential for forecasting and intervention planning
    - Bridge climate science and public health

---

## 🔜 Next Steps

Now that you understand the theory, you're ready to explore VECTRI in action!

<div class="grid cards" markdown>

-   :material-telescope:{ .lg .middle } __Explore Use Cases__

    ---

    See how VECTRI is applied to real-world malaria forecasting
    
    [View Use Cases →](02-use-case.md){ .md-button }

-   :material-laptop:{ .lg .middle } __Get Started with VECTRI__

    ---

    Introduction to the VECTRI model structure and components
    
    [VECTRI Introduction →](03-vectri-intro.md){ .md-button .md-button--primary }

-   :material-book-open-variant:{ .lg .middle } __Deep Dive: Model Components__

    ---

    Detailed equations and implementations for all VECTRI components
    
    [Model Components →](06-vectri_model_components_larvae_to_hydrology.md){ .md-button }

</div>

---

## 📚 References and Further Reading

!!! quote "Foundational Papers"
    
    - **Ross, R.** (1911). *The Prevention of Malaria*. London: John Murray. (Original mathematical framework)
    - **Macdonald, G.** (1957). *The Epidemiology and Control of Malaria*. Oxford University Press. (Refined transmission model)
    - **Martens, W.J.M. et al.** (1995). Potential impact of global climate change on malaria risk. *Environmental Health Perspectives*, 103(5), 458-464. (Survival model)
    - **Bayoh, M.N. & Lindsay, S.W.** (2003). Effect of temperature on the development of the aquatic stages of *Anopheles gambiae* sensu stricto. *Bulletin of Entomological Research*, 93(5), 375-381. (Larval development)

!!! info "VECTRI-Specific"
    
    - **Tompkins, A.M. & Ermert, V.** (2013). A regional-scale, high resolution dynamical malaria model that accounts for population density, climate and surface hydrology. *Malaria Journal*, 12, 65. (Original VECTRI paper)
    - **Tompkins, A.M. & Thomson, M.C.** (2018). Uncertainty in malaria simulations in the highlands of Kenya: Relative contributions of model parameter setting, driving climate and initial condition errors. *PLOS ONE*, 13(9). (Uncertainty analysis)

!!! tip "Additional Resources"
    
    - [VECTRI GitLab Repository](https://gitlab.com/tompkins/vectri) - Model code and documentation
    - [WHO Malaria Reports](https://www.who.int/teams/global-malaria-programme/reports) - Global malaria data and trends
    - [Malaria Atlas Project](https://malariaatlas.org/) - Global maps and data
---

<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h3 style="color: white; margin-top: 0;">Ready to Build Your Understanding?</h3>
    <p style="font-size: 1.1rem;">Continue to the next lesson to see VECTRI applied to real-world scenarios!</p>
    <a href="02-use-case.md" style="display: inline-block; margin-top: 1rem; padding: 0.75rem 2rem; background: white; color: #667eea; text-decoration: none; border-radius: 5px; font-weight: bold;">Explore Use Cases →</a>
</div>

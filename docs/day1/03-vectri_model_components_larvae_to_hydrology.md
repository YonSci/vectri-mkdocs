# VECTRI Model Components: Larvae to Surface Hydrology

This note summarizes the main biological and physical components of the VECTRI malaria model from the **larval cycle** through **surface hydrology**.
---

## 1. Larval Cycle

### 1.1 Concept

The larval cycle describes the development of mosquito larvae from hatching to adult emergence. VECTRI represents this as a **fractional life-cycle** from 0 to 1 and advances larvae along this axis each day.

Development is assumed to depend primarily on **water temperature** via a degree-day relationship:

- Warmer water → faster development  
- No development below a minimum temperature  
- Death above a maximum (lethal) temperature

Egg and pupa stages are not explicitly temperature-dependent in VECTRI; they are each assigned a fixed duration of 1 day because the model time step (1 day) is too coarse to resolve shorter variations.

### 1.2 Larval development rate

The **larval development rate** \(R_L\) (fraction of full development per day) is:

$$
R_L = \frac{T_{\mathrm{wat}} - T_{L,\min}}{K_L}
$$

where:

- \(T_{\mathrm{wat}}\) is the water temperature in breeding pools (°C)  
- \(T_{L,\min}\) is the minimum temperature for larval development (°C)  
- \(K_L\) is the number of **degree-days** required to complete the larval stage  

Key points:

- If \(R_L = 0.1\), larvae complete 10% of their development per day → larval phase lasts about \(1/0.1 = 10\) days.
- If \(T_{\mathrm{wat}} \le T_{L,\min}\), then \(R_L \le 0\) and **no development** occurs.
- VECTRI supports several choices for \(K_L\) (e.g., based on Jepson 1947, Bayoh & Lindsay 2003, or a fixed 12-day larval period).
- Jepson (1947): \(K_L\) = 90.9 degree-days → fast development
- Bayoh & Lindsay (2003): \(K_L\) = 200 degree-days → slower development
- LMM-style option: fixed 12-day larval cycle independent of temperature

#### Example

Let:

- \(T_{\mathrm{wat}} = 26^\circ\mathrm{C}\)  
- \(T_{L,\min} = 16^\circ\mathrm{C}\)  
- Case 1: \(K_L = 90.9\) degree-days  
- Case 2: \(K_L = 200\) degree-days  

Then:

$$
T_{\mathrm{excess}} = T_{\mathrm{wat}} - T_{L,\min} = 26 - 16 = 10^\circ\mathrm{C}
$$

- Case 1:

$$
R_L = \frac{10}{90.9} \approx 0.11
\quad\Rightarrow\quad
\text{Larval duration} \approx \frac{1}{0.11} \approx 9.1\ \text{days}
$$

- Case 2:

$$
R_L = \frac{10}{200} = 0.05
\quad\Rightarrow\quad
\text{Larval duration} = \frac{1}{0.05} = 20\ \text{days}
$$

Thus, choosing different parameterizations for \(K_L\) can double the larval duration.

### 1.3 Advection along the life cycle

Let \(f \in [0,1]\) be the fractional larval development stage and \(L(f,t)\) the larval density at stage \(f\) and time \(t\). VECTRI advances larvae by solving an **advection equation**:

$$
\frac{\partial L}{\partial t} = R_L \frac{\partial L}{\partial f}
$$


- Each time step, larvae are “advected” forward along the development axis at speed \(R_L\).

with:

- Daily time step  
- Discrete bins in \(f\)  

Egg and pupa stages are both set to 1 day each (temperature-independent) because the daily time step is too coarse to resolve their true variation (they are typically O(1 day) in lab experiments).

An upper lethal temperature \(𝑇𝐿,max\) (≈ 37–38 °C) is imposed: above this, larvae die and do not develop.

### 1.4 Temperature limits

To represent lethal heat stress:

- If \(T_{\mathrm{wat}} > T_{L,\max}\), all larvae are assumed to **die** and no development occurs, regardless of other factors.

Biological assumptions

- Development depends only on water temperature, not food quality or density (those show up in the survival formulation, see below).

- All larvae in a cell see the same \(𝑇𝑤𝑎𝑡\) 

- Eggs and pupae have fixed durations, even though in reality they do vary with temperature.

---

## 2. Larval Mortality

### 2.1 Concept

Larval survival depends on:

1. A **base survival rate** in “good” conditions  
2. **Crowding** (resource limitation as biomass approaches pond carrying capacity)  
3. **Flushing** by heavy rainfall  
4. A **lethal temperature cutoff** at very high water temperatures  

### 2.2 Base survival and crowding

Base daily survival (without crowding or flushing):

$$
P_{L,\mathrm{surv},0} \approx 0.825
$$

Crowding is represented by a simple linear reduction:

$$
P_{L,\mathrm{surv,crowd}} =
\left(1 - \frac{M_L}{w\,M_{L,\max}}\right)
P_{L,\mathrm{surv},0}
$$

where:

- \(M_L\) is total larval biomass per unit water area (mg m\(^{-2}\))  
- \(w\) is the fraction of the grid cell covered by breeding pools  
- \(M_{L,\max}\) is the carrying capacity for larval biomass (e.g. 300 mg m\(^{-2}\))  

If \(M_L = w M_{L,\max}\), then crowding factor \(= 0\) and no larvae survive that day.

Assumption: individual larval mass increases linearly with stage, and \(M_{L,\max}\) corresponds to an order of hundreds of late-stage larvae per m².

### 2.3 Rainfall-driven flushing

Early larval stages can be washed out of ephemeral pools by heavy rainfall. VECTRI models this with a flushing factor \(K_{\mathrm{flush}}\) that multiplies survival:

$$
K_{\mathrm{flush}} =
L_f + (1 - L_f)
\left[
(1 - K_{\mathrm{flush,\infty}})\,e^{-R_d / \tau_{\mathrm{flush}}}
+ K_{\mathrm{flush,\infty}}
\right]
$$

where:

- \(L_f\) is the larval fractional stage (0 = very early, 1 = about to emerge)  
- \(R_d\) is daily rainfall (mm day\(^{-1}\))  
- \(\tau_{\mathrm{flush}}\) is a rainfall scale (mm day\(^{-1}\))  
- \(K_{\mathrm{flush,\infty}}\) is the survival fraction of early larvae under extremely heavy rain  

Properties:

- **Early larvae** (\(L_f \approx 0\)) are strongly affected by rainfall.
- **Late larvae** (\(L_f = 1\)) have \(K_{\mathrm{flush}} = 1\), i.e., no extra flushing mortality.
- For small \(R_d\), \(e^{-R_d/\tau_{\mathrm{flush}}} \approx 1\) → weak flushing.
- For large \(R_d\), \(e^{-R_d/\tau_{\mathrm{flush}}} \to 0\) → early larvae survival approaches \(K_{\mathrm{flush,\infty}}\).

#### Example

Let:

- \(L_f = 0\) (first-stage larvae)  
- \(\tau_{\mathrm{flush}} = 50\ \text{mm/day}\)  
- \(K_{\mathrm{flush,\infty}} = 0.4\)  

For \(R_d = 25\ \text{mm/day}\):

$$
e^{-R_d / \tau_{\mathrm{flush}}} = e^{-25/50} = e^{-0.5} \approx 0.61
$$

Then:

$$
K_{\mathrm{flush}} \approx 0.6 \times 0.61 + 0.4 \approx 0.76
$$

So rainfall of 25 mm/day reduces survival by ~24% relative to base.

For \(R_d \gg 50\ \text{mm/day}\), the factor approaches \(K_{\mathrm{flush,\infty}} = 0.4\), meaning roughly 60% of early larvae are lost to flushing.

### 2.4 Total larval survival

Total daily survival probability is:

$$
P_{L,\mathrm{surv}} =
\left(1 - \frac{M_L}{w\,M_{L,\max}}\right)
K_{\mathrm{flush}}\,
P_{L,\mathrm{surv},0}
$$

bounded between 0 and 1.

### 2.5 Temperature cutoff

If \(T_{\mathrm{wat}}\) exceeds a lethal threshold \(T_{L,\max}\):

- All larvae are assumed to **die**, regardless of crowding or flushing.

---

## 3. Gonotrophic Cycle

### 3.1 Concept

The gonotrophic cycle is the time from a mosquito’s **blood meal** to **egg laying** (oviposition). In VECTRI:

- Female mosquitoes in a “searching” stage attempt to feed each night.
- By default, all searching mosquitoes succeed in obtaining a blood meal unless interventions (e.g. bed nets) reduce this.

Egg development after feeding is modeled via degree-days, similar to larval development.

### 3.2 Egg development rate

The gonotrophic development rate \(R_{\mathrm{gono}}\) is:

$$
R_{\mathrm{gono}} = \frac{T_{\mathrm{eff}} - T_{\mathrm{gono,\min}}}{K_{\mathrm{gono}}}
$$

where:

- \(T_{\mathrm{eff}}\) is the effective temperature experienced by mosquitoes (possibly including indoor weighting)  
- \(T_{\mathrm{gono,\min}}\) is the minimum temperature for egg development  
- \(K_{\mathrm{gono}}\) is the gonotrophic degree-day requirement  

The gonotrophic period (days per cycle) is approximately:

$$
P_{\mathrm{gono}} = \frac{1}{R_{\mathrm{gono}}}
$$

#### Example

Let:

- \(T_{\mathrm{eff}} = 25^\circ\mathrm{C}\)  
- \(T_{\mathrm{gono,\min}} = 7.7^\circ\mathrm{C}\)  
- \(K_{\mathrm{gono}} = 37.1\) degree-days  

Then:

$$
R_{\mathrm{gono}} =
\frac{25 - 7.7}{37.1} =
\frac{17.3}{37.1} \approx 0.47\ \text{day}^{-1}
$$

$$
P_{\mathrm{gono}} \approx \frac{1}{0.47} \approx 2.1\ \text{days}
$$

At cooler temperatures (e.g. 20 °C), the cycle extends to ~3 days; at warmer temperatures (e.g. 28 °C), it shortens toward ~1.8 days.

### 3.3 Eggs per cycle

Each completed gonotrophic cycle produces \(N_{\mathrm{egg}}\) female eggs, typically parameterized around:

$$
N_{\mathrm{egg}} \approx 80\ \text{female eggs per cycle}
$$

(about 160 total eggs assuming a 50:50 sex ratio).

Assumption: the model ignores explicit size/body condition of females and uses a fixed batch size per cycle.

---

## 4. Sporogonic Cycle (Parasite in the Mosquito)

### 4.1 Concept

The sporogonic cycle describes the development of the malaria parasite (e.g., *Plasmodium falciparum*) inside the mosquito:

- From ingestion of gametocytes during a blood meal  
- To mature sporozoites in the salivary glands, making the mosquito infectious  

The duration of this **extrinsic incubation period** (EIP) depends strongly on temperature.

### 4.2 Host → vector infection probability

When a mosquito bites a human, the probability the mosquito becomes infected is:

$$
P_{h \to v} = \frac{H_{\mathrm{inf}}}{H} P_{hv}
$$

where:

- \(H_{\mathrm{inf}}\) is the number (or density) of infectious humans  
- \(H\) is the total human population  
- \(P_{hv}\) is the probability that a bite on an infectious human results in mosquito infection  

Assumption: mosquitoes do not preferentially bite infectious or non-infectious humans.

#### Example

If 10% of humans are infectious and \(P_{hv} = 0.2\):

$$
\frac{H_{\mathrm{inf}}}{H} = 0.1
\quad\Rightarrow\quad
P_{h \to v} = 0.1 \times 0.2 = 0.02
$$

So 2% of all blood meals infect the mosquito.

### 4.3 Temperature-dependent parasite development

The parasite development rate \(R_{\mathrm{sporo}}\) is:

$$
R_{\mathrm{sporo}} =
\frac{T_{\mathrm{eff}} - T_{\mathrm{sporo,\min}}}{K_{\mathrm{sporo}}}
$$

where:

- \(T_{\mathrm{sporo,\min}}\) is the minimum temperature for sporogonic development  
- \(K_{\mathrm{sporo}}\) is the sporogonic degree-day requirement  

The EIP (days) is:

$$
\mathrm{EIP} = \frac{1}{R_{\mathrm{sporo}}}
$$

if \(R_{\mathrm{sporo}} > 0\), otherwise it is effectively infinite (no development).

#### Example

Let:

- \(T_{\mathrm{eff}} = 25^\circ\mathrm{C}\)  
- \(T_{\mathrm{sporo,\min}} = 16^\circ\mathrm{C}\)  
- \(K_{\mathrm{sporo}} = 111\) degree-days  

Then:

$$
R_{\mathrm{sporo}} =
\frac{25 - 16}{111} =
\frac{9}{111} \approx 0.081\ \text{day}^{-1}
\quad\Rightarrow\quad
\mathrm{EIP} \approx \frac{1}{0.081} \approx 12.3\ \text{days}
$$

At 20 °C, \(R_{\mathrm{sporo}}\) is about 0.036 day\(^{-1}\), giving an EIP of ~28 days, much longer than typical mosquito lifespans in many settings.

---

## 5. Vector Survival

### 5.1 Concept

Adult mosquito daily survival probability depends on temperature. VECTRI includes two parameterizations from Martens et al.; the default is often referred to as “Martens II”.

### 5.2 Martens II formulation

The daily probability of survival \(P_{V,\mathrm{surv}}\) is given by:

$$
P_{V,\mathrm{surv}} =
\exp\left(
- \frac{1}{K_{0} + K_{1} T_{\mathrm{eff}} + K_{2} T_{\mathrm{eff}}^2}
\right)
$$

where \(K_0, K_1, K_2\) are constants.

This formulation:

- Produces a **bell-shaped** relationship with temperature.  
- Yields higher survival in a mid-temperature range (e.g. ~20–25 °C).  
- Reduces survival at low and high extremes.

### 5.3 Expected lifespan

If daily survival probability is \(P_{V,\mathrm{surv}}\), the approximate expected lifespan in days is:

$$
\mathrm{Lifespan} \approx \frac{1}{1 - P_{V,\mathrm{surv}}}
$$

#### Example

- If \(P_{V,\mathrm{surv}} = 0.9\), the expected lifespan is:

$$
\approx \frac{1}{1 - 0.9} = 10\ \text{days}
$$

- If \(P_{V,\mathrm{surv}} = 0.8\), the expected lifespan is ~5 days.

Assumption: survival is memoryless (like a geometric distribution), and other stressors (humidity, predators, insecticides) are captured implicitly via parameter choices.

---

## 6. Indoor Temperatures

### 6.1 Concept

Mosquitoes spend substantial time resting indoors, where temperatures can differ from outdoor air temperature. VECTRI includes a simple parameterization for indoor temperatures and a weighting for time spent indoors.

### 6.2 Indoor temperature parameterization

Indoor temperature is given by:

$$
T_{\mathrm{indoor}} = T_0 + K\,T_{2\mathrm{m}}
$$

where:

- \(T_{2\mathrm{m}}\) is the 2 m air temperature (outdoor)  
- \(T_0\) and \(K\) are empirical constants  

This implies:

- At cool outdoor temperatures, indoors tends to be **warmer** than outside.  
- At very hot outdoor temperatures, indoors can be **cooler** (e.g. thick walls, shading).

### 6.3 Effective temperature seen by mosquitoes

If mosquitoes spend a fraction \(\beta_{\mathrm{indoor}}\) of their time indoors, the effective temperature is:

$$
T_{\mathrm{eff}} =
\beta_{\mathrm{indoor}}\,T_{\mathrm{indoor}} +
(1 - \beta_{\mathrm{indoor}})\,T_{2\mathrm{m}}
$$

Special cases:

- \(\beta_{\mathrm{indoor}} = 0\): always outdoors → \(T_{\mathrm{eff}} = T_{2\mathrm{m}}\)  
- \(\beta_{\mathrm{indoor}} = 1\): always indoors → \(T_{\mathrm{eff}} = T_{\mathrm{indoor}}\)  

This \(T_{\mathrm{eff}}\) is then used in the **gonotrophic**, **sporogonic**, and **survival** equations.

---

## 7. Host Community and Biting

### 7.1 Concept

VECTRI explicitly models the **human population** and links it to:

- Biting rate per person  
- Entomological inoculation rate (EIR)  
- Human infection probability  

Human population density \(H\) comes from gridded datasets (e.g., AFRIPOP/WorldPop), aggregated to the model grid.

### 7.2 Human biting rate

Let:

- \(V_b\) be the number of biting mosquitoes (e.g., in the first gonotrophic bin, across all sporogonic stages).  
- \(H\) be the human population in the cell.  

The **mean** human biting rate (bites per person per day) is:

$$
\overline{\mathrm{hbr}} =
\left(1 - e^{-H / \tau_{\mathrm{zoo}}}\right)
\frac{V_b}{H}
$$

where:

- \(\tau_{\mathrm{zoo}}\) is a scale parameter controlling the switch from zoophilic to anthropophilic feeding.  

Interpretation:

- At low human densities (\(H \ll \tau_{\mathrm{zoo}}\)), the factor \(1 - e^{-H/\tau_{\mathrm{zoo}}}\) is small → many bites go to animals.  
- At high densities (\(H \gg \tau_{\mathrm{zoo}}\)), the factor approaches 1 → almost all bites are on humans.

In the model, the actual number of bites per person is drawn from a **Poisson** distribution with mean \(\overline{\mathrm{hbr}}\).

### 7.3 Daily EIR

The **daily entomological inoculation rate** (EIR) is:

$$
\mathrm{EIR}_d = \overline{\mathrm{hbr}} \times \mathrm{CSPR}
$$

where \(\mathrm{CSPR}\) is the circumsporozoite protein rate, i.e. the fraction of mosquitoes that are infectious.

### 7.4 Vector → host infection probability

Given the per-bite probability of infection from vector to human \(P_{vh}\), and a mean EIR \(\lambda = \mathrm{EIR}_d\), the daily probability that a **susceptible** host becomes infected is:

- Let the number of infectious bites \(N\) on that host be Poisson with mean \(\lambda\).
- Given \(N\) infectious bites, the probability of at least one successful infection is:

$$
P(\text{infection} \mid N) = 1 - (1 - P_{vh})^N
$$

- Averaging over the Poisson distribution leads to a closed form:

$$
P_{v \to h} =
1 - e^{-\lambda P_{vh}}
=
1 - e^{-\mathrm{EIR}_d\,P_{vh}}
$$

This is what VECTRI uses as the daily infection probability for susceptible hosts.

#### Example

If:

- \(\mathrm{EIR}_d = 0.1\) infectious bites per person per day (about 36 per year)  
- \(P_{vh} = 0.3\)  

Then:

$$
P_{v \to h} = 1 - e^{-0.1 \times 0.3} \approx 1 - e^{-0.03} \approx 0.0296
$$

So the daily infection probability is about 3% for a susceptible host.

---

## 8. Immunity

### 8.1 Concept

VECTRI includes a simplified **immunity module** to capture:

- Acquisition of immunity through repeated exposure (infectious bites)  
- Loss of immunity over time when exposure declines  
- Reduction in **clinical disease** and **transmission efficiency** for immune individuals  

The implementation follows Laneri et al. (2010) and related literature.

### 8.2 Acquisition and loss of immunity

Simplified description:

- Immunity level \(I\) increases with exposure rate (EIR) and decays toward zero with a certain timescale.
- Parameters are tuned so that:
  - At an annual EIR of ~100, about 95% of individuals become clinically immune.
  - In the absence of exposure, 95% of immunity is lost in roughly 3 years.

Mathematically, a commonly used simple form (conceptually) is:

$$
\frac{dI}{dt} = \alpha\,\mathrm{EIR} - \frac{I}{\tau}
$$

where:

- \(\alpha\) controls how fast immunity accumulates with exposure  
- \(\tau\) is the decay timescale for immunity (e.g. on the order of years)  

VECTRI uses a discrete implementation with parameters chosen to match the above qualitative behavior.

### 8.3 Effects of immunity

In the model, increasing immunity:

- Reduces the probability that an infection leads to **clinical disease**.  
- Reduces the probability that an infected host successfully infects a mosquito (i.e., lowers \(P_{hv}\) for immune individuals), representing **transmission-blocking immunity**.

This allows VECTRI to reproduce patterns where:

- High-transmission settings have high infection prevalence but relatively fewer clinical episodes among adults.  
- Low-transmission or unstable settings see more clinical disease when exposure varies.

---

## 9. Surface Hydrology

### 9.1 Concept

Surface hydrology links **rainfall** to **breeding habitat availability** and thus to larval carrying capacity. VECTRI distinguishes:

- **Permanent water bodies** (lakes, rivers)  
- **Temporary ponds/puddles** formed by rainfall

The total breeding area fraction \(w\) is:

$$
w = w_{\mathrm{perm}} + w_{\mathrm{pond}}
$$

where:

- \(w_{\mathrm{perm}}\) is the (time-independent) fraction with permanent water  
- \(w_{\mathrm{pond}}\) is the dynamic fraction covered by rainfall-driven ponds  

By default, \(w_{\mathrm{perm}}\) is often set to zero and all breeding comes from \(w_{\mathrm{pond}}\), unless specified by the user.

### 9.2 Water balance for temporary ponds (conceptual)

A simplified water balance for temporary ponds might be written as:

$$
\frac{dw_{\mathrm{pond}}}{dt} =
K_w \left[
P \left(w_{\max} - w_{\mathrm{pond}}\right)
- w_{\mathrm{pond}}(E + I)
\right]
$$

where:

- \(w_{\max}\) is the maximum possible pond coverage (e.g. 0.04 = 4% of cell area)  
- \(P\) is daily precipitation (mm day\(^{-1}\))  
- \(E\) is evaporation (mm day\(^{-1}\))  
- \(I\) is infiltration (mm day\(^{-1}\)), typically large (e.g. \(\sim\) 200–250 mm day\(^{-1}\))  
- \(K_w\) is a geometric factor converting volume changes to area changes  

Interpretation:

- When it rains, \(P (w_{\max} - w_{\mathrm{pond}})\) increases pond area, but once \(w_{\mathrm{pond}} \to w_{\max}\), this term saturates.
- When it is dry or ponds exist, \(w_{\mathrm{pond}}(E+I)\) shrinks ponds via evaporation and infiltration.
- \(K_w\) controls how rapidly area responds to the water balance.

### 9.3 Interaction with larvae

Surface hydrology affects larvae in three ways:

**1. Carrying capacity**

Larval survival includes a crowding term:

$$
1 - \frac{M_L}{w\,M_{L,\max}}
$$

If \(w\) is small (few ponds), the same biomass \(M_L\) means stronger crowding and lower survival. If \(w\) is large, crowding is weaker.

**2. Flushing**

Daily rainfall \(P\) enters the flushing factor \(K_{\mathrm{flush}}\): intense rain increases flushing mortality, especially for early-stage larvae.

**3. Water temperature**

Pond temperature is typically parameterized as:

$$
T_{\mathrm{wat}} = T_{2\mathrm{m}} + \Delta T
$$

where \(\Delta T\) is a user-defined offset (often positive, as shallow water can be warmer than air). This \(T_{\mathrm{wat}}\) drives larval development and temperature cutoffs.

### 9.4 Qualitative behavior

- In **semi-arid** regions, short intense rainstorms produce temporary ponds that may dry out before larvae can complete development, limiting transmission despite high rainfall intensity.
- In **humid** regions with frequent rainfall, \(w_{\mathrm{pond}}\) remains high, ponds persist, and larval habitats are abundant, supporting high vector densities and high EIR.

---

## 10. Summary

From larvae to surface hydrology, VECTRI integrates:

- **Temperature-driven development** (larval, gonotrophic, sporogonic)  
- **Mortality mechanisms** (crowding, flushing, lethal temperatures, temperature-dependent adult survival)  
- **Host community structure** and **biting dynamics**  
- **Immunity** that accumulates and decays with exposure  
- **Rainfall-driven hydrology** determining breeding habitat availability  

These components are tightly coupled:

- Rainfall and hydrology determine **where larvae can develop**.  
- Temperatures control **how fast larvae, mosquitoes, and parasites develop** and **how long adult vectors survive**.  
- Human population and immunity modulate **infection dynamics** and **clinical outcomes**.


Putting all these pieces together:
 - Rainfall and surface hydrology determine how many and how long ponds exist.
 
 - Pond temperature and air/indoor temperatures control larval development, adult survival, and parasite development via degree-day relationships.
 
 - Larval mortality balances base survival, crowding, and flushing from rainfall.
 
 - The gonotrophic cycle and egg production define how fast new vectors are generated.
 
 - The host community and biting process connect vector numbers to EIR and infection probabilities.
 
 - Immunity then modulates how many clinical cases occur for a given EIR.

This integrated framework allows VECTRI to simulate malaria transmission across diverse climates and population densities in a mechanistic and spatially explicit way.


## 📝 Test Your Knowledge

Ready to test your understanding of VECTRI model components? Take the interactive quiz to assess your knowledge of the biological and physical processes that drive malaria transmission in VECTRI.

[Take the VECTRI Model Components Quiz →](../quizzes/vectri-model-components-quiz.md){ .md-button .md-button--primary }

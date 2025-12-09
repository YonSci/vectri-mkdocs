# VECTRI Model: Theory, Equations, and Python Implementation

This comprehensive guide covers the main biological and physical components of the VECTRI malaria model, combining **theory**, **equations**, **examples**, and **Python code** for each concept.

---

## 📋 Outline

* [1. Introduction and Setup](#1-introduction-and-setup)
* [2. Larval Cycle](#2-larval-cycle)
* [3. Larval Mortality](#3-larval-mortality)
* [4. Gonotrophic Cycle](#4-gonotrophic-cycle)
* [5. Sporogonic Cycle](#5-sporogonic-cycle)
* [6. Vector Survival](#6-vector-survival)
* [7. Indoor Temperatures](#7-indoor-temperatures)
* [8. Host Community and Biting](#8-host-community-and-biting)
* [9. Immunity](#9-immunity)
* [10. Surface Hydrology](#10-surface-hydrology)
* [11. Complete Simulation Example](#11-complete-simulation-example)
* [12. Exercises](#12-exercises)
* [13. Summary](#13-summary)

---

## 1. Introduction and Setup

### 1.1 Required Libraries

```python
import math
```

```python
import numpy as np
```

```python
import pandas as pd
```

```python
import matplotlib.pyplot as plt
```

### 1.2 Overview

VECTRI integrates multiple biological and physical processes:

- **Temperature-driven development** (larval, gonotrophic, sporogonic)
- **Mortality mechanisms** (crowding, flushing, lethal temperatures, temperature-dependent adult survival)
- **Host community structure** and **biting dynamics**
- **Immunity** that accumulates and decays with exposure
- **Rainfall-driven hydrology** determining breeding habitat availability

---

## 2. Larval Cycle

### 2.1 Concept

The larval cycle describes the development of mosquito larvae from hatching to adult emergence. VECTRI represents this as a **fractional life-cycle** from 0 to 1 and advances larvae along this axis each day.

Development is assumed to depend primarily on **water temperature** via a degree-day relationship:

- Warmer water → faster development
- No development below a minimum temperature
- Death above a maximum (lethal) temperature

Egg and pupa stages are not explicitly temperature-dependent in VECTRI; they are each assigned a fixed duration of 1 day because the model time step (1 day) is too coarse to resolve shorter variations.

### 2.2 Equations

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
- VECTRI supports several choices for \(K_L\):
    - Jepson (1947): \(K_L\) = 90.9 degree-days → fast development
    - Bayoh & Lindsay (2003): \(K_L\) = 200 degree-days → slower development
    - LMM-style option: fixed 12-day larval cycle independent of temperature

### 2.3 Parameters

```python
T_L_min = 16.0   # [°C] Minimum water temperature for larval development
```

```python
K_L = 90.9       # [degree-days] Degree-days needed to complete larval stage
```

```python
T_L_max = 37.0   # [°C] Lethal upper water temperature (no larvae survive)
```

### 2.4 Python Implementation

```python
def calculate_larval_development(T_wat, T_L_min=16.0, K_L=90.9, T_L_max=37.0):
    """
    Calculate larval development rate and period.
    
    Parameters:
    -----------
    T_wat : float
        Water temperature in breeding pools (°C)
    T_L_min : float
        Minimum temperature for larval development (°C)
    K_L : float
        Degree-days required to complete larval stage
    T_L_max : float
        Lethal upper temperature (°C)
    
    Returns:
    --------
    R_L : float
        Development rate (fraction per day)
    larval_period : float
        Days to complete larval development
    """
    if T_wat <= T_L_min or T_wat >= T_L_max:
        R_L = 0.0
        larval_period = math.inf
    else:
        R_L = (T_wat - T_L_min) / K_L
        larval_period = 1.0 / R_L
    
    return R_L, larval_period
```

### 2.5 Example Calculation

Let:

- \(T_{\mathrm{wat}} = 26^\circ\mathrm{C}\)
- \(T_{L,\min} = 16^\circ\mathrm{C}\)
- Case 1: \(K_L = 90.9\) degree-days
- Case 2: \(K_L = 200\) degree-days

Then:

$$
T_{\mathrm{excess}} = T_{\mathrm{wat}} - T_{L,\min} = 26 - 16 = 10^\circ\mathrm{C}
$$

- Case 1: \(R_L = \frac{10}{90.9} \approx 0.11\) → Larval duration ≈ 9.1 days
- Case 2: \(R_L = \frac{10}{200} = 0.05\) → Larval duration = 20 days

```python
# Example: Calculate larval development at 26°C
T_wat = 26.0

# Case 1: Jepson parameterization
R_L_case1, period_case1 = calculate_larval_development(T_wat, K_L=90.9)
print(f"Case 1 (K_L=90.9): R_L = {R_L_case1:.3f}, Period = {period_case1:.1f} days")

# Case 2: Bayoh & Lindsay parameterization
R_L_case2, period_case2 = calculate_larval_development(T_wat, K_L=200.0)
print(f"Case 2 (K_L=200): R_L = {R_L_case2:.3f}, Period = {period_case2:.1f} days")
```

### 2.6 Visualization: Temperature Sensitivity

```python
# Temperature range for analysis
temps = np.arange(10, 41, 1)
R_L_values = []
period_values = []

for T in temps:
    R_L, period = calculate_larval_development(T)
    R_L_values.append(R_L)
    period_values.append(period if period < 100 else np.nan)

# Plot development rate vs temperature
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(temps, R_L_values, 'b-', linewidth=2)
axes[0].axvline(x=16, color='r', linestyle='--', label='T_L_min = 16°C')
axes[0].axvline(x=37, color='r', linestyle='--', label='T_L_max = 37°C')
axes[0].set_xlabel('Water Temperature (°C)')
axes[0].set_ylabel('Development Rate R_L (fraction/day)')
axes[0].set_title('Larval Development Rate vs Temperature')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(temps, period_values, 'g-', linewidth=2)
axes[1].axvline(x=16, color='r', linestyle='--', label='T_L_min = 16°C')
axes[1].axvline(x=37, color='r', linestyle='--', label='T_L_max = 37°C')
axes[1].set_xlabel('Water Temperature (°C)')
axes[1].set_ylabel('Larval Period (days)')
axes[1].set_title('Larval Development Period vs Temperature')
axes[1].set_ylim(0, 50)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2.7 Advection Along the Life Cycle

Let \(f \in [0,1]\) be the fractional larval development stage and \(L(f,t)\) the larval density at stage \(f\) and time \(t\). VECTRI advances larvae by solving an **advection equation**:

$$
\frac{\partial L}{\partial t} = R_L \frac{\partial L}{\partial f}
$$

- Each time step, larvae are "advected" forward along the development axis at speed \(R_L\).
- Daily time step with discrete bins in \(f\)
- An upper lethal temperature \(T_{L,\max}\) (≈ 37–38 °C) is imposed: above this, larvae die and do not develop.

---

## 3. Larval Mortality

### 3.1 Concept

Larval survival depends on:

1. A **base survival rate** in "good" conditions
2. **Crowding** (resource limitation as biomass approaches pond carrying capacity)
3. **Flushing** by heavy rainfall
4. A **lethal temperature cutoff** at very high water temperatures

### 3.2 Equations

#### Base Survival and Crowding

Base daily survival (without crowding or flushing):

$$
P_{L,\mathrm{surv},0} \approx 0.825
$$

Crowding is represented by a simple linear reduction:

$$
P_{L,\mathrm{surv,crowd}} = \left(1 - \frac{M_L}{w \cdot M_{L,\max}}\right) P_{L,\mathrm{surv},0}
$$

where:

- \(M_L\) is total larval biomass per unit water area (mg m⁻²)
- \(w\) is the fraction of the grid cell covered by breeding pools
- \(M_{L,\max}\) is the carrying capacity for larval biomass (e.g., 300 mg m⁻²)

#### Rainfall-Driven Flushing

Early larval stages can be washed out of ephemeral pools by heavy rainfall:

$$
K_{\mathrm{flush}} = L_f + (1 - L_f) \left[ (1 - K_{\mathrm{flush,\infty}}) e^{-R_d / \tau_{\mathrm{flush}}} + K_{\mathrm{flush,\infty}} \right]
$$

where:

- \(L_f\) is the larval fractional stage (0 = very early, 1 = about to emerge)
- \(R_d\) is daily rainfall (mm day⁻¹)
- \(\tau_{\mathrm{flush}}\) is a rainfall scale (mm day⁻¹)
- \(K_{\mathrm{flush,\infty}}\) is the survival fraction of early larvae under extremely heavy rain

#### Total Larval Survival

$$
P_{L,\mathrm{surv}} = \left(1 - \frac{M_L}{w \cdot M_{L,\max}}\right) K_{\mathrm{flush}} \cdot P_{L,\mathrm{surv},0}
$$

### 3.3 Parameters

```python
P_L_surv0 = 0.825    # Base daily larval survival (no crowding, no flushing)
```

```python
M_L_max = 300.0      # [mg m^-2] Larval biomass capacity (carrying capacity)
```

```python
tau_flush = 50.0     # [mm/day] Rainfall scale for flushing
```

```python
K_flush_inf = 0.4    # Survival of early larvae under very heavy rain (asymptote)
```

### 3.4 Python Implementation

```python
def calculate_flushing_factor(L_f, R_d, tau_flush=50.0, K_flush_inf=0.4):
    """
    Calculate flushing factor based on larval stage and rainfall.
    
    Parameters:
    -----------
    L_f : float
        Larval fractional stage (0 = very early, 1 = about to emerge)
    R_d : float
        Daily rainfall (mm/day)
    tau_flush : float
        Rainfall scale for flushing (mm/day)
    K_flush_inf : float
        Survival fraction under very heavy rain
    
    Returns:
    --------
    K_flush : float
        Flushing factor (0 to 1)
    """
    inner = (1.0 - K_flush_inf) * math.exp(-R_d / tau_flush) + K_flush_inf
    K_flush = L_f + (1.0 - L_f) * inner
    return K_flush
```

```python
def calculate_larval_survival(M_L, w, R_d, L_f, P_L_surv0=0.825, M_L_max=300.0, 
                               tau_flush=50.0, K_flush_inf=0.4):
    """
    Calculate total larval survival probability.
    
    Parameters:
    -----------
    M_L : float
        Larval biomass (mg m^-2)
    w : float
        Pond fraction (0 to 1)
    R_d : float
        Daily rainfall (mm/day)
    L_f : float
        Larval fractional stage (0 to 1)
    
    Returns:
    --------
    P_L_surv : float
        Total daily survival probability
    P_L_surv_crowd : float
        Crowding-only survival
    K_flush : float
        Flushing factor
    """
    if w <= 0.0:
        return 0.0, 0.0, 1.0
    
    # Crowding term
    crowd_term = 1.0 - M_L / (w * M_L_max)
    crowd_term = max(0.0, min(1.0, crowd_term))
    
    # Crowding-only survival
    P_L_surv_crowd = crowd_term * P_L_surv0
    
    # Flushing factor
    K_flush = calculate_flushing_factor(L_f, R_d, tau_flush, K_flush_inf)
    
    # Total survival
    P_L_surv = P_L_surv_crowd * K_flush
    P_L_surv = max(0.0, min(1.0, P_L_surv))
    
    return P_L_surv, P_L_surv_crowd, K_flush
```

### 3.5 Example Calculation

Let:

- \(L_f = 0\) (first-stage larvae)
- \(\tau_{\mathrm{flush}} = 50\) mm/day
- \(K_{\mathrm{flush,\infty}} = 0.4\)

For \(R_d = 25\) mm/day:

$$
e^{-R_d / \tau_{\mathrm{flush}}} = e^{-25/50} = e^{-0.5} \approx 0.61
$$

$$
K_{\mathrm{flush}} \approx 0.6 \times 0.61 + 0.4 \approx 0.76
$$

So rainfall of 25 mm/day reduces survival by ~24% relative to base.

```python
# Example: Flushing effect on early larvae
L_f = 0.0  # First-stage larvae
R_d = 25.0  # 25 mm/day rainfall

K_flush = calculate_flushing_factor(L_f, R_d)
print(f"Flushing factor at R_d={R_d} mm/day: K_flush = {K_flush:.3f}")
print(f"Survival reduction: {(1 - K_flush) * 100:.1f}%")
```

### 3.6 Visualization: Flushing Effect

```python
# Flushing factor vs rainfall for different larval stages
rainfall = np.linspace(0, 100, 100)
stages = [0.0, 0.25, 0.5, 0.75, 1.0]

plt.figure(figsize=(10, 5))

for L_f in stages:
    K_flush_values = [calculate_flushing_factor(L_f, R) for R in rainfall]
    plt.plot(rainfall, K_flush_values, label=f'L_f = {L_f}', linewidth=2)

plt.xlabel('Daily Rainfall (mm/day)')
plt.ylabel('Flushing Factor K_flush')
plt.title('Flushing Factor vs Rainfall for Different Larval Stages')
plt.legend(title='Larval Stage')
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()
```

---

## 4. Gonotrophic Cycle

### 4.1 Concept

The gonotrophic cycle is the time from a mosquito's **blood meal** to **egg laying** (oviposition). In VECTRI:

- Female mosquitoes in a "searching" stage attempt to feed each night.
- By default, all searching mosquitoes succeed in obtaining a blood meal unless interventions (e.g., bed nets) reduce this.

Egg development after feeding is modeled via degree-days, similar to larval development.

### 4.2 Equations

The gonotrophic development rate \(R_{\mathrm{gono}}\) is:

$$
R_{\mathrm{gono}} = \frac{T_{\mathrm{eff}} - T_{\mathrm{gono,\min}}}{K_{\mathrm{gono}}}
$$

where:

- \(T_{\mathrm{eff}}\) is the effective temperature experienced by mosquitoes (possibly including indoor weighting)
- \(T_{\mathrm{gono,\min}}\) is the minimum temperature for egg development
- \(K_{\mathrm{gono}}\) is the gonotrophic degree-day requirement

The gonotrophic period (days per cycle) is:

$$
P_{\mathrm{gono}} = \frac{1}{R_{\mathrm{gono}}}
$$

Each completed gonotrophic cycle produces approximately:

$$
N_{\mathrm{egg}} \approx 80 \text{ female eggs per cycle}
$$

(about 160 total eggs assuming a 50:50 sex ratio).

### 4.3 Parameters

```python
T_gono_min = 7.7    # [°C] Minimum temperature for egg development
```

```python
K_gono = 37.1       # [degree-days] Degree-days needed to complete gonotrophic cycle
```

### 4.4 Python Implementation

```python
def calculate_gonotrophic_cycle(T_eff, T_gono_min=7.7, K_gono=37.1):
    """
    Calculate gonotrophic development rate and period.
    
    Parameters:
    -----------
    T_eff : float
        Effective temperature (°C)
    T_gono_min : float
        Minimum temperature for egg development (°C)
    K_gono : float
        Degree-days for gonotrophic cycle
    
    Returns:
    --------
    R_gono : float
        Development rate (fraction per day)
    gono_period : float
        Days to complete gonotrophic cycle
    """
    if T_eff <= T_gono_min:
        R_gono = 0.0
        gono_period = math.inf
    else:
        R_gono = (T_eff - T_gono_min) / K_gono
        gono_period = 1.0 / R_gono
    
    return R_gono, gono_period
```

### 4.5 Example Calculation

Let:

- \(T_{\mathrm{eff}} = 25^\circ\mathrm{C}\)
- \(T_{\mathrm{gono,\min}} = 7.7^\circ\mathrm{C}\)
- \(K_{\mathrm{gono}} = 37.1\) degree-days

Then:

$$
R_{\mathrm{gono}} = \frac{25 - 7.7}{37.1} = \frac{17.3}{37.1} \approx 0.47 \text{ day}^{-1}
$$

$$
P_{\mathrm{gono}} \approx \frac{1}{0.47} \approx 2.1 \text{ days}
$$

```python
# Example: Gonotrophic cycle at different temperatures
temperatures = [20, 25, 28]

for T in temperatures:
    R_gono, period = calculate_gonotrophic_cycle(T)
    print(f"T_eff = {T}°C: R_gono = {R_gono:.3f}, Period = {period:.1f} days")
```

### 4.6 Visualization: Gonotrophic Period vs Temperature

```python
temps = np.arange(10, 36, 1)
gono_periods = []

for T in temps:
    _, period = calculate_gonotrophic_cycle(T)
    gono_periods.append(period if period < 20 else np.nan)

plt.figure(figsize=(8, 5))
plt.plot(temps, gono_periods, 'b-', linewidth=2)
plt.axvline(x=7.7, color='r', linestyle='--', label='T_gono_min = 7.7°C')
plt.xlabel('Effective Temperature (°C)')
plt.ylabel('Gonotrophic Period (days)')
plt.title('Gonotrophic Cycle Duration vs Temperature')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 15)
plt.tight_layout()
plt.show()
```

---

## 5. Sporogonic Cycle

### 5.1 Concept

The sporogonic cycle describes the development of the malaria parasite (e.g., *Plasmodium falciparum*) inside the mosquito:

- From ingestion of gametocytes during a blood meal
- To mature sporozoites in the salivary glands, making the mosquito infectious

The duration of this **extrinsic incubation period** (EIP) depends strongly on temperature.

### 5.2 Equations

#### Host → Vector Infection Probability

When a mosquito bites a human, the probability the mosquito becomes infected is:

$$
P_{h \to v} = \frac{H_{\mathrm{inf}}}{H} P_{hv}
$$

where:

- \(H_{\mathrm{inf}}\) is the number of infectious humans
- \(H\) is the total human population
- \(P_{hv}\) is the probability that a bite on an infectious human results in mosquito infection

#### Temperature-Dependent Parasite Development

The parasite development rate \(R_{\mathrm{sporo}}\) is:

$$
R_{\mathrm{sporo}} = \frac{T_{\mathrm{eff}} - T_{\mathrm{sporo,\min}}}{K_{\mathrm{sporo}}}
$$

The EIP (days) is:

$$
\mathrm{EIP} = \frac{1}{R_{\mathrm{sporo}}}
$$

### 5.3 Parameters

```python
T_sporo_min = 16.0  # [°C] Minimum temperature for parasite development
```

```python
K_sporo = 111.0     # [degree-days] Degree-days for sporogonic cycle (EIP)
```

```python
P_hv = 0.2          # P(mosquito infected | bite on infectious host)
```

### 5.4 Python Implementation

```python
def calculate_sporogonic_cycle(T_eff, T_sporo_min=16.0, K_sporo=111.0):
    """
    Calculate sporogonic development rate and EIP.
    
    Parameters:
    -----------
    T_eff : float
        Effective temperature (°C)
    T_sporo_min : float
        Minimum temperature for parasite development (°C)
    K_sporo : float
        Degree-days for sporogonic cycle
    
    Returns:
    --------
    R_sporo : float
        Development rate (fraction per day)
    EIP : float
        Extrinsic incubation period (days)
    """
    if T_eff <= T_sporo_min:
        R_sporo = 0.0
        EIP = math.inf
    else:
        R_sporo = (T_eff - T_sporo_min) / K_sporo
        EIP = 1.0 / R_sporo
    
    return R_sporo, EIP
```

```python
def calculate_host_to_vector_infection(H_inf, H, P_hv=0.2):
    """
    Calculate probability of mosquito infection from a blood meal.
    
    Parameters:
    -----------
    H_inf : float
        Number of infectious humans
    H : float
        Total human population
    P_hv : float
        Probability of infection given bite on infectious host
    
    Returns:
    --------
    P_h2v : float
        Probability mosquito becomes infected per blood meal
    """
    if H <= 0:
        return 0.0
    return (H_inf / H) * P_hv
```

### 5.5 Example Calculation

Let:

- \(T_{\mathrm{eff}} = 25^\circ\mathrm{C}\)
- \(T_{\mathrm{sporo,\min}} = 16^\circ\mathrm{C}\)
- \(K_{\mathrm{sporo}} = 111\) degree-days

Then:

$$
R_{\mathrm{sporo}} = \frac{25 - 16}{111} = \frac{9}{111} \approx 0.081 \text{ day}^{-1}
$$

$$
\mathrm{EIP} \approx \frac{1}{0.081} \approx 12.3 \text{ days}
$$

At 20°C, EIP ≈ 28 days, much longer than typical mosquito lifespans in many settings.

```python
# Example: EIP at different temperatures
temperatures = [18, 20, 25, 30]

for T in temperatures:
    R_sporo, EIP = calculate_sporogonic_cycle(T)
    print(f"T_eff = {T}°C: R_sporo = {R_sporo:.4f}, EIP = {EIP:.1f} days")
```

### 5.6 Visualization: EIP vs Temperature

```python
temps = np.arange(15, 36, 1)
EIP_values = []

for T in temps:
    _, EIP = calculate_sporogonic_cycle(T)
    EIP_values.append(EIP if EIP < 60 else np.nan)

plt.figure(figsize=(8, 5))
plt.plot(temps, EIP_values, 'r-', linewidth=2)
plt.axvline(x=16, color='gray', linestyle='--', label='T_sporo_min = 16°C')
plt.axhline(y=10, color='green', linestyle=':', label='Typical mosquito lifespan')
plt.xlabel('Effective Temperature (°C)')
plt.ylabel('Extrinsic Incubation Period (days)')
plt.title('Parasite Development Time (EIP) vs Temperature')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 50)
plt.tight_layout()
plt.show()
```

---

## 6. Vector Survival

### 6.1 Concept

Adult mosquito daily survival probability depends on temperature. VECTRI includes two parameterizations from Martens et al.; the default is often referred to as "Martens II".

This formulation:

- Produces a **bell-shaped** relationship with temperature
- Yields higher survival in a mid-temperature range (e.g., ~20–25°C)
- Reduces survival at low and high extremes

### 6.2 Equations

The daily probability of survival \(P_{V,\mathrm{surv}}\) is given by:

$$
P_{V,\mathrm{surv}} = \exp\left(- \frac{1}{K_{0} + K_{1} T_{\mathrm{eff}} + K_{2} T_{\mathrm{eff}}^2}\right)
$$

where \(K_0, K_1, K_2\) are constants.

If daily survival probability is \(P_{V,\mathrm{surv}}\), the approximate expected lifespan in days is:

$$
\mathrm{Lifespan} \approx \frac{1}{1 - P_{V,\mathrm{surv}}}
$$

### 6.3 Parameters

```python
K_mar2_0 = -4.4     # Martens II constant
```

```python
K_mar2_1 = 1.31     # Martens II constant
```

```python
K_mar2_2 = -0.03    # Martens II constant
```

### 6.4 Python Implementation

```python
def calculate_vector_survival(T_eff, K0=-4.4, K1=1.31, K2=-0.03):
    """
    Calculate adult vector daily survival probability and lifespan.
    
    Parameters:
    -----------
    T_eff : float
        Effective temperature (°C)
    K0, K1, K2 : float
        Martens II parameters
    
    Returns:
    --------
    P_V_surv : float
        Daily survival probability
    lifespan : float
        Expected lifespan (days)
    """
    den = K0 + K1 * T_eff + K2 * (T_eff ** 2)
    
    if den <= 0.0:
        P_V_surv = 0.0
        lifespan = 0.0
    else:
        P_V_surv = math.exp(-1.0 / den)
        P_V_surv = max(0.0, min(1.0, P_V_surv))
        
        if P_V_surv >= 0.999:
            lifespan = math.inf
        elif P_V_surv <= 0.0:
            lifespan = 0.0
        else:
            lifespan = 1.0 / (1.0 - P_V_surv)
    
    return P_V_surv, lifespan
```

### 6.5 Example Calculation

- If \(P_{V,\mathrm{surv}} = 0.9\), the expected lifespan is: \(\approx \frac{1}{1 - 0.9} = 10\) days
- If \(P_{V,\mathrm{surv}} = 0.8\), the expected lifespan is ~5 days

```python
# Example: Vector survival at different temperatures
temperatures = [15, 20, 25, 30, 35]

for T in temperatures:
    P_surv, lifespan = calculate_vector_survival(T)
    print(f"T_eff = {T}°C: P_V_surv = {P_surv:.3f}, Lifespan = {lifespan:.1f} days")
```

### 6.6 Visualization: Survival and Lifespan vs Temperature

```python
temps = np.arange(10, 40, 1)
P_surv_values = []
lifespan_values = []

for T in temps:
    P_surv, lifespan = calculate_vector_survival(T)
    P_surv_values.append(P_surv)
    lifespan_values.append(lifespan if lifespan < 50 else np.nan)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(temps, P_surv_values, 'b-', linewidth=2)
axes[0].set_xlabel('Effective Temperature (°C)')
axes[0].set_ylabel('Daily Survival Probability')
axes[0].set_title('Adult Vector Daily Survival vs Temperature')
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(0, 1)

axes[1].plot(temps, lifespan_values, 'g-', linewidth=2)
axes[1].set_xlabel('Effective Temperature (°C)')
axes[1].set_ylabel('Expected Lifespan (days)')
axes[1].set_title('Adult Vector Lifespan vs Temperature')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 7. Indoor Temperatures

### 7.1 Concept

Mosquitoes spend substantial time resting indoors, where temperatures can differ from outdoor air temperature. VECTRI includes a simple parameterization for indoor temperatures and a weighting for time spent indoors.

This implies:

- At cool outdoor temperatures, indoors tends to be **warmer** than outside
- At very hot outdoor temperatures, indoors can be **cooler** (e.g., thick walls, shading)

### 7.2 Equations

Indoor temperature is given by:

$$
T_{\mathrm{indoor}} = T_0 + K \cdot T_{2\mathrm{m}}
$$

where:

- \(T_{2\mathrm{m}}\) is the 2 m air temperature (outdoor)
- \(T_0\) and \(K\) are empirical constants

If mosquitoes spend a fraction \(\beta_{\mathrm{indoor}}\) of their time indoors, the effective temperature is:

$$
T_{\mathrm{eff}} = \beta_{\mathrm{indoor}} \cdot T_{\mathrm{indoor}} + (1 - \beta_{\mathrm{indoor}}) \cdot T_{2\mathrm{m}}
$$

### 7.3 Parameters

```python
T0_indoor = 10.33   # [°C] Intercept for indoor temperature
```

```python
K_indoor = 0.58     # [-] Slope relating outdoor T to indoor T
```

```python
beta_indoor = 0.5   # Fraction of time mosquitoes spend indoors
```

### 7.4 Python Implementation

```python
def calculate_temperatures(T2m, T0_indoor=10.33, K_indoor=0.58, beta_indoor=0.5, delta_Tw=1.5):
    """
    Calculate indoor, effective, and water temperatures.
    
    Parameters:
    -----------
    T2m : float
        Outdoor air temperature at 2m (°C)
    T0_indoor : float
        Indoor temperature intercept (°C)
    K_indoor : float
        Indoor temperature slope
    beta_indoor : float
        Fraction of time spent indoors
    delta_Tw : float
        Water temperature offset from air (°C)
    
    Returns:
    --------
    T_indoor : float
        Indoor temperature (°C)
    T_eff : float
        Effective temperature for mosquitoes (°C)
    T_wat : float
        Water temperature (°C)
    """
    T_indoor = T0_indoor + K_indoor * T2m
    T_eff = beta_indoor * T_indoor + (1.0 - beta_indoor) * T2m
    T_wat = T2m + delta_Tw
    
    return T_indoor, T_eff, T_wat
```

### 7.5 Example Calculation

```python
# Example: Temperature calculations at different outdoor temperatures
outdoor_temps = [15, 20, 25, 30, 35]

print("Outdoor | Indoor | Effective | Water")
print("-" * 45)
for T2m in outdoor_temps:
    T_indoor, T_eff, T_wat = calculate_temperatures(T2m)
    print(f"  {T2m}°C  |  {T_indoor:.1f}°C |   {T_eff:.1f}°C   | {T_wat:.1f}°C")
```

### 7.6 Visualization: Temperature Relationships

```python
T2m_range = np.linspace(10, 40, 100)
T_indoor_vals = []
T_eff_vals = []
T_wat_vals = []

for T2m in T2m_range:
    T_indoor, T_eff, T_wat = calculate_temperatures(T2m)
    T_indoor_vals.append(T_indoor)
    T_eff_vals.append(T_eff)
    T_wat_vals.append(T_wat)

plt.figure(figsize=(10, 5))
plt.plot(T2m_range, T2m_range, 'k-', label='T2m (outdoor)', linewidth=2)
plt.plot(T2m_range, T_indoor_vals, 'r-', label='T_indoor', linewidth=2)
plt.plot(T2m_range, T_eff_vals, 'g-', label='T_eff (50% indoor)', linewidth=2)
plt.plot(T2m_range, T_wat_vals, 'b--', label='T_wat (water)', linewidth=2)
plt.xlabel('Outdoor Air Temperature (°C)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Relationships in VECTRI')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 8. Host Community and Biting

### 8.1 Concept

VECTRI explicitly models the **human population** and links it to:

- Biting rate per person
- Entomological inoculation rate (EIR)
- Human infection probability

Human population density \(H\) comes from gridded datasets (e.g., AFRIPOP/WorldPop), aggregated to the model grid.

### 8.2 Equations

#### Human Biting Rate

Let:

- \(V_b\) be the number of biting mosquitoes
- \(H\) be the human population in the cell

The **mean** human biting rate (bites per person per day) is:

$$
\overline{\mathrm{hbr}} = \left(1 - e^{-H / \tau_{\mathrm{zoo}}}\right) \frac{V_b}{H}
$$

where \(\tau_{\mathrm{zoo}}\) is a scale parameter controlling the switch from zoophilic to anthropophilic feeding.

#### Daily EIR

The **daily entomological inoculation rate** (EIR) is:

$$
\mathrm{EIR}_d = \overline{\mathrm{hbr}} \times \mathrm{CSPR}
$$

where CSPR is the circumsporozoite protein rate (fraction of mosquitoes that are infectious).

#### Vector → Host Infection Probability

Given the per-bite probability of infection \(P_{vh}\), the daily probability that a susceptible host becomes infected is:

$$
P_{v \to h} = 1 - e^{-\mathrm{EIR}_d \cdot P_{vh}}
$$

### 8.3 Parameters

```python
tau_zoo = 50.0      # [people] Scale for zoophily/anthropophily
```

```python
P_vh = 0.3          # P(host infected | infectious bite)
```

### 8.4 Python Implementation

```python
def calculate_biting_rate(V_biting, H, tau_zoo=50.0):
    """
    Calculate mean human biting rate.
    
    Parameters:
    -----------
    V_biting : float
        Number of biting mosquitoes
    H : float
        Human population
    tau_zoo : float
        Zoophily scale parameter
    
    Returns:
    --------
    hbr : float
        Human biting rate (bites per person per day)
    """
    if H <= 0.0:
        return 0.0
    
    phi = 1.0 - math.exp(-H / tau_zoo)
    hbr = phi * V_biting / H
    return hbr
```

```python
def calculate_transmission(hbr, CSPR, P_vh=0.3):
    """
    Calculate daily EIR and vector-to-host infection probability.
    
    Parameters:
    -----------
    hbr : float
        Human biting rate (bites per person per day)
    CSPR : float
        Circumsporozoite protein rate (infectious fraction)
    P_vh : float
        Probability of infection per infectious bite
    
    Returns:
    --------
    EIR_d : float
        Daily EIR (infectious bites per person per day)
    P_v2h : float
        Daily vector-to-host infection probability
    """
    EIR_d = hbr * CSPR
    P_v2h = 1.0 - math.exp(-EIR_d * P_vh)
    return EIR_d, P_v2h
```

### 8.5 Example Calculation

If:

- \(\mathrm{EIR}_d = 0.1\) infectious bites per person per day (about 36 per year)
- \(P_{vh} = 0.3\)

Then:

$$
P_{v \to h} = 1 - e^{-0.1 \times 0.3} \approx 1 - e^{-0.03} \approx 0.0296
$$

So the daily infection probability is about 3% for a susceptible host.

```python
# Example: Transmission calculations
V_biting = 50
H = 200
CSPR = 0.10

hbr = calculate_biting_rate(V_biting, H)
EIR_d, P_v2h = calculate_transmission(hbr, CSPR)

print(f"Human biting rate: {hbr:.3f} bites/person/day")
print(f"Daily EIR: {EIR_d:.4f} infectious bites/person/day")
print(f"Annual EIR: {EIR_d * 365:.1f} infectious bites/person/year")
print(f"Daily infection probability: {P_v2h:.4f} ({P_v2h*100:.2f}%)")
```

### 8.6 Visualization: Biting Rate vs Population

```python
H_values = np.logspace(0, 4, 100)  # 1 to 10,000 people
V_biting = 50

hbr_values = [calculate_biting_rate(V_biting, H) for H in H_values]

plt.figure(figsize=(10, 5))
plt.semilogx(H_values, hbr_values, 'b-', linewidth=2)
plt.axvline(x=50, color='r', linestyle='--', label=f'tau_zoo = 50')
plt.xlabel('Human Population (H)')
plt.ylabel('Human Biting Rate (bites/person/day)')
plt.title('Human Biting Rate vs Population Density')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 9. Immunity

### 9.1 Concept

VECTRI includes a simplified **immunity module** to capture:

- Acquisition of immunity through repeated exposure (infectious bites)
- Loss of immunity over time when exposure declines
- Reduction in **clinical disease** and **transmission efficiency** for immune individuals

The implementation follows Laneri et al. (2010) and related literature.

### 9.2 Equations

Immunity level \(I\) increases with exposure rate (EIR) and decays toward zero with a certain timescale:

$$
\frac{dI}{dt} = \alpha \cdot \mathrm{EIR} - \frac{I}{\tau}
$$

where:

- \(\alpha\) controls how fast immunity accumulates with exposure
- \(\tau\) is the decay timescale for immunity (e.g., on the order of years)

Parameters are tuned so that:

- At an annual EIR of ~100, about 95% of individuals become clinically immune
- In the absence of exposure, 95% of immunity is lost in roughly 3 years

### 9.3 Effects of Immunity

In the model, increasing immunity:

- Reduces the probability that an infection leads to **clinical disease**
- Reduces the probability that an infected host successfully infects a mosquito (transmission-blocking immunity)

### 9.4 Python Implementation

```python
def update_immunity(I, EIR_annual, alpha=0.01, tau_years=3.0, dt=1.0):
    """
    Update immunity level based on exposure.
    
    Parameters:
    -----------
    I : float
        Current immunity level (0 to 1)
    EIR_annual : float
        Annual EIR (infectious bites per year)
    alpha : float
        Immunity acquisition rate
    tau_years : float
        Immunity decay timescale (years)
    dt : float
        Time step (days)
    
    Returns:
    --------
    I_new : float
        Updated immunity level
    """
    tau_days = tau_years * 365
    EIR_daily = EIR_annual / 365
    
    dI = (alpha * EIR_daily - I / tau_days) * dt
    I_new = I + dI
    I_new = max(0.0, min(1.0, I_new))
    
    return I_new
```

### 9.5 Visualization: Immunity Dynamics

```python
# Simulate immunity buildup and decay
days = 365 * 10  # 10 years
I = np.zeros(days)
EIR_pattern = np.zeros(days)

# High EIR for first 5 years, then zero
EIR_pattern[:365*5] = 100  # Annual EIR of 100

for d in range(1, days):
    I[d] = update_immunity(I[d-1], EIR_pattern[d])

years = np.arange(days) / 365

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axes[0].plot(years, EIR_pattern, 'b-', linewidth=2)
axes[0].set_ylabel('Annual EIR')
axes[0].set_title('Exposure Pattern')
axes[0].grid(True, alpha=0.3)

axes[1].plot(years, I, 'r-', linewidth=2)
axes[1].set_xlabel('Time (years)')
axes[1].set_ylabel('Immunity Level')
axes[1].set_title('Immunity Dynamics')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 10. Surface Hydrology

### 10.1 Concept

Surface hydrology links **rainfall** to **breeding habitat availability** and thus to larval carrying capacity. VECTRI distinguishes:

- **Permanent water bodies** (lakes, rivers)
- **Temporary ponds/puddles** formed by rainfall

The total breeding area fraction \(w\) is:

$$
w = w_{\mathrm{perm}} + w_{\mathrm{pond}}
$$

By default, \(w_{\mathrm{perm}}\) is often set to zero and all breeding comes from \(w_{\mathrm{pond}}\).

### 10.2 Equations

A simplified water balance for temporary ponds:

$$
\frac{dw_{\mathrm{pond}}}{dt} = K_w \left[ P (w_{\max} - w_{\mathrm{pond}}) - w_{\mathrm{pond}}(E + I) \right]
$$

where:

- \(w_{\max}\) is the maximum possible pond coverage (e.g., 0.04 = 4% of cell area)
- \(P\) is daily precipitation (mm day⁻¹)
- \(E\) is evaporation (mm day⁻¹)
- \(I\) is infiltration (mm day⁻¹), typically large (~200–250 mm day⁻¹)
- \(K_w\) is a geometric factor converting volume changes to area changes

### 10.3 Parameters

```python
w_max = 0.04        # Max fractional pond coverage (4% of grid cell)
```

```python
E = 5.0             # [mm/day] Evaporation
```

```python
I_infilt = 245.0    # [mm/day] Infiltration
```

```python
K_w = 0.001         # Geometry/scale factor
```

### 10.4 Python Implementation

```python
def update_pond_fraction(w_prev, rain, w_max=0.04, E=5.0, I_infilt=245.0, K_w=0.001):
    """
    Update pond fraction based on water balance.
    
    Parameters:
    -----------
    w_prev : float
        Previous pond fraction
    rain : float
        Daily rainfall (mm/day)
    w_max : float
        Maximum pond fraction
    E : float
        Evaporation (mm/day)
    I_infilt : float
        Infiltration (mm/day)
    K_w : float
        Geometry factor
    
    Returns:
    --------
    w_new : float
        New pond fraction
    inflow : float
        Water inflow term
    outflow : float
        Water outflow term
    """
    inflow = rain * (w_max - w_prev)
    outflow = w_prev * (E + I_infilt)
    
    dw = K_w * (inflow - outflow)
    w_new = w_prev + dw
    
    w_new = max(0.0, min(w_max, w_new))
    
    return w_new, inflow, outflow
```

### 10.5 Example: Pond Dynamics Under Different Rainfall

```python
# Simulate pond dynamics for 60 days
days = 60
w = np.zeros(days)
w[0] = 0.0  # Start dry

# Scenario 1: Constant moderate rain
rain_constant = np.full(days, 8.0)

# Scenario 2: Episodic heavy rain
rain_episodic = np.zeros(days)
rain_episodic[::7] = 30.0  # Heavy rain every 7 days

# Scenario 3: Dry spell
rain_dry = np.full(days, 1.0)

scenarios = {
    'Constant (8 mm/day)': rain_constant,
    'Episodic (30 mm/week)': rain_episodic,
    'Dry (1 mm/day)': rain_dry
}

plt.figure(figsize=(12, 5))

for name, rain in scenarios.items():
    w = np.zeros(days)
    w[0] = 0.01  # Start with small pond
    
    for d in range(1, days):
        w[d], _, _ = update_pond_fraction(w[d-1], rain[d])
    
    plt.plot(range(days), w * 100, label=name, linewidth=2)

plt.axhline(y=4, color='r', linestyle='--', label='w_max = 4%')
plt.xlabel('Day')
plt.ylabel('Pond Coverage (%)')
plt.title('Pond Dynamics Under Different Rainfall Scenarios')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 10.6 Interaction with Larvae

Surface hydrology affects larvae in three ways:

**1. Carrying Capacity**: If \(w\) is small (few ponds), the same biomass means stronger crowding and lower survival.

**2. Flushing**: Daily rainfall enters the flushing factor: intense rain increases flushing mortality.

**3. Water Temperature**: Pond temperature is typically:

$$
T_{\mathrm{wat}} = T_{2\mathrm{m}} + \Delta T
$$

where \(\Delta T\) is a user-defined offset (often positive, as shallow water can be warmer than air).

---

## 11. Complete Simulation Example

### 11.1 Create Climate Time Series

```python
# Time axis: 180 days
dates = pd.date_range("2025-01-01", periods=180, freq="D")
day_of_year = dates.dayofyear.values

# Synthetic air temperature [°C]: seasonal cycle around 24°C
T2m = 24.0 + 3.0 * np.sin(2 * np.pi * (day_of_year / 365.0))

# Synthetic rainfall [mm/day]: random Gamma distribution
rng = np.random.default_rng(42)
rain = rng.gamma(shape=2.0, scale=3.0, size=len(dates))

climate_df = pd.DataFrame({"T2m": T2m, "rain": rain}, index=dates)
```

### 11.2 Set Location Parameters

```python
# Larval state
M_L = 3.0           # [mg m^-2] Larval biomass
L_f = 0.25          # Larval fractional stage
delta_Tw = 1.5      # Water temperature offset

# Host & vector
H = 200.0           # Humans in the cell
H_inf_frac = 0.10   # Fraction infectious
V_biting = 50.0     # Biting mosquitoes
CSPR = 0.10         # Infectious fraction
beta_indoor = 0.5   # Fraction time indoors

H_inf = H * H_inf_frac
```

### 11.3 Run Day-by-Day Simulation

```python
n = len(climate_df)

# Initialize arrays
w = np.zeros(n)
Twat = np.zeros(n)
T_ind = np.zeros(n)
T_eff_arr = np.zeros(n)
R_L_arr = np.zeros(n)
larval_period = np.zeros(n)
P_L_surv_arr = np.zeros(n)
R_gono_arr = np.zeros(n)
gono_period_arr = np.zeros(n)
EIP_arr = np.zeros(n)
P_V_surv_arr = np.zeros(n)
lifespan_arr = np.zeros(n)
hbr_arr = np.zeros(n)
EIR_d_arr = np.zeros(n)
P_v2h_arr = np.zeros(n)

for i, (date, row) in enumerate(climate_df.iterrows()):
    T2 = row["T2m"]
    Rd = row["rain"]
    
    # Hydrology
    w_prev = w[i-1] if i > 0 else 0.0
    w[i], _, _ = update_pond_fraction(w_prev, Rd)
    
    # Temperatures
    T_indoor, T_eff, T_wat = calculate_temperatures(T2, beta_indoor=beta_indoor, delta_Tw=delta_Tw)
    Twat[i] = T_wat
    T_ind[i] = T_indoor
    T_eff_arr[i] = T_eff
    
    # Larval development
    R_L, period = calculate_larval_development(T_wat)
    R_L_arr[i] = R_L
    larval_period[i] = period if period < 100 else np.nan
    
    # Larval survival
    P_L_surv, _, _ = calculate_larval_survival(M_L, w[i], Rd, L_f)
    P_L_surv_arr[i] = P_L_surv
    
    # Gonotrophic cycle
    R_gono, gono_p = calculate_gonotrophic_cycle(T_eff)
    R_gono_arr[i] = R_gono
    gono_period_arr[i] = gono_p if gono_p < 20 else np.nan
    
    # Sporogonic cycle
    _, EIP = calculate_sporogonic_cycle(T_eff)
    EIP_arr[i] = EIP if EIP < 60 else np.nan
    
    # Vector survival
    P_V_surv, lifespan = calculate_vector_survival(T_eff)
    P_V_surv_arr[i] = P_V_surv
    lifespan_arr[i] = lifespan if lifespan < 50 else np.nan
    
    # Transmission
    hbr = calculate_biting_rate(V_biting, H)
    EIR_d, P_v2h = calculate_transmission(hbr, CSPR)
    hbr_arr[i] = hbr
    EIR_d_arr[i] = EIR_d
    P_v2h_arr[i] = P_v2h
```

### 11.4 Create Results DataFrame

```python
results_df = pd.DataFrame({
    "T2m": T2m,
    "rain": rain,
    "w": w,
    "Twat": Twat,
    "T_indoor": T_ind,
    "T_eff": T_eff_arr,
    "R_L": R_L_arr,
    "larval_period": larval_period,
    "P_L_surv": P_L_surv_arr,
    "gono_period": gono_period_arr,
    "EIP": EIP_arr,
    "P_V_surv": P_V_surv_arr,
    "lifespan": lifespan_arr,
    "hbr": hbr_arr,
    "EIR_d": EIR_d_arr,
    "P_v2h": P_v2h_arr
}, index=dates)

print(results_df.describe())
```

### 11.5 Comprehensive Visualization

```python
fig, axes = plt.subplots(4, 2, figsize=(14, 12))

# Temperature dynamics
axes[0, 0].plot(results_df.index, results_df["T2m"], label="T2m (air)")
axes[0, 0].plot(results_df.index, results_df["T_eff"], label="T_eff")
axes[0, 0].plot(results_df.index, results_df["Twat"], label="T_wat", linestyle="--")
axes[0, 0].set_ylabel("Temperature (°C)")
axes[0, 0].set_title("Temperature Dynamics")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Rainfall and ponds
ax1 = axes[0, 1]
ax2 = ax1.twinx()
ax1.bar(results_df.index, results_df["rain"], alpha=0.4, label="Rain")
ax2.plot(results_df.index, results_df["w"] * 100, 'r-', label="Pond %", linewidth=2)
ax1.set_ylabel("Rain (mm/day)")
ax2.set_ylabel("Pond Coverage (%)")
ax1.set_title("Rainfall and Breeding Habitat")
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Larval survival
axes[1, 0].plot(results_df.index, results_df["P_L_surv"])
axes[1, 0].set_ylabel("Survival Probability")
axes[1, 0].set_title("Larval Daily Survival")
axes[1, 0].set_ylim(0, 1)
axes[1, 0].grid(True, alpha=0.3)

# Development periods
axes[1, 1].plot(results_df.index, results_df["larval_period"], label="Larval")
axes[1, 1].plot(results_df.index, results_df["gono_period"], label="Gonotrophic")
axes[1, 1].plot(results_df.index, results_df["EIP"], label="EIP")
axes[1, 1].set_ylabel("Days")
axes[1, 1].set_title("Development Periods")
axes[1, 1].legend()
axes[1, 1].set_ylim(0, 30)
axes[1, 1].grid(True, alpha=0.3)

# Vector survival and lifespan
axes[2, 0].plot(results_df.index, results_df["P_V_surv"])
axes[2, 0].set_ylabel("Daily Survival")
axes[2, 0].set_title("Adult Vector Survival")
axes[2, 0].set_ylim(0, 1)
axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].plot(results_df.index, results_df["lifespan"])
axes[2, 1].set_ylabel("Days")
axes[2, 1].set_title("Expected Mosquito Lifespan")
axes[2, 1].grid(True, alpha=0.3)

# Transmission metrics
axes[3, 0].plot(results_df.index, results_df["EIR_d"])
axes[3, 0].set_ylabel("Infectious bites/person/day")
axes[3, 0].set_title("Daily EIR")
axes[3, 0].grid(True, alpha=0.3)

axes[3, 1].plot(results_df.index, results_df["P_v2h"] * 100)
axes[3, 1].set_ylabel("Probability (%)")
axes[3, 1].set_title("Daily Infection Probability")
axes[3, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 12. Exercises

### Exercise 1: Temperature Sensitivity Analysis

**Objective**: Explore how temperature affects larval development.

**Task**:

1. Calculate R_L for water temperatures from 10°C to 40°C
2. Plot R_L and larval period vs temperature
3. Compare Jepson (K_L=90.9) vs Bayoh & Lindsay (K_L=200) parameterizations

```python
# Your code here
temps = np.arange(10, 41, 1)

# Calculate for both parameterizations
# Plot comparison
```

---

### Exercise 2: EIP vs Mosquito Lifespan

**Objective**: Determine when parasites can complete development before mosquitoes die.

**Task**:

1. For temperatures 16°C to 32°C, calculate both EIP and lifespan
2. Find the "transmission threshold" - lowest temperature where EIP < lifespan
3. Create a visualization showing both curves

```python
# Your code here
temps = np.arange(16, 33, 1)

# Calculate EIP and lifespan for each temperature
# Find intersection point
```

---

### Exercise 3: Rainfall Scenarios

**Objective**: Understand how rainfall patterns affect breeding habitat.

**Task**:

1. Create three 60-day rainfall scenarios:
   - Constant: 5 mm/day
   - Episodic: 25 mm every 5 days
   - Dry: 0.5 mm/day
2. Simulate pond dynamics for each
3. Calculate mean larval survival for each scenario

```python
# Your code here
days = 60

# Create rainfall scenarios
# Simulate pond dynamics
# Calculate survival
```

---

### Exercise 4: Full Seasonal Cycle

**Objective**: Simulate a complete year and identify peak transmission.

**Task**:

1. Create 365 days of climate data with seasonal patterns
2. Run the full VECTRI calculation
3. Calculate monthly mean EIR
4. Identify peak transmission months

```python
# Your code here
# Create annual climate data
# Run simulation
# Analyze monthly patterns
```

---

## 13. Summary

This comprehensive guide covered VECTRI's main components:

| Component | Key Equation | Temperature Dependence |
|-----------|-------------|----------------------|
| Larval Development | \(R_L = (T_{wat} - T_{L,min}) / K_L\) | Degree-days in water |
| Larval Survival | Crowding × Flushing × Base | Lethal threshold |
| Gonotrophic Cycle | \(R_{gono} = (T_{eff} - T_{gono,min}) / K_{gono}\) | Effective temperature |
| Sporogonic Cycle | \(R_{sporo} = (T_{eff} - T_{sporo,min}) / K_{sporo}\) | Effective temperature |
| Vector Survival | Martens II formula | Bell-shaped curve |
| Hydrology | Water balance ODE | Evaporation |

**Key Insights**:

- Temperature controls development rates and survival
- Rainfall creates breeding habitat but can flush larvae
- The EIP must be shorter than mosquito lifespan for transmission
- Human population density affects biting rates
- Immunity modulates clinical outcomes

---

## 📝 Test Your Knowledge

Ready to test your understanding of VECTRI model components and equations?

[Take the VECTRI Model Quiz →](../quizzes/vectri-model-components-quiz.md){ .md-button .md-button--primary }

---

## 🔗 Additional Resources

- The VECTRI online documentation at [VECTRI](https://users.ictp.it/~tompkins/vectri/documentation/)
- The PDF manual `VECTRI_manual_v1.6.pdf` [VECTRI PDF manual](../pdfs/VECTRI_manual_v1.6.pdf)
- Tompkins & Ermert (2013) - A regional-scale, high resolution dynamical malaria model
- Bayoh & Lindsay (2003) - Effect of temperature on the development of the aquatic stages of Anopheles gambiae
- Martens et al. (1995) - Potential impact of global climate change on malaria risk


# VECTRI Core Equations – Single Location

This document computes key VECTRI quantities for a **single grid cell** using
**explicit parameters and formulas**, without classes or helper functions.

We include:

- Explicit parameter definitions with comments  
- Core equations written directly in code  
- A simple daily time series (180 days) for one location  
- Plots grouped by **physical meaning**, each with a short interpretation  

Main components covered:

- Water and air temperature, indoor and effective temperature  
- Temporary pond hydrology (water balance and pond fraction)  
- Larval development, crowding survival, flushing, and total survival  
- Gonotrophic and sporogonic development rates and periods (EIP)  
- Adult vector survival and approximate lifespan  
- Human biting rate, daily EIR, and vector → host infection probability  

---

## 1. Imports

```python
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

---

## 2. Parameter Definitions

We define each parameter explicitly and comment its meaning.

### 2.1 Larval development

```python
# ---------------------------
# Larval development
# ---------------------------

T_L_min = 16.0   # [°C] Minimum water temperature for larval development
K_L     = 90.9   # [degree-days] Degree-days needed to complete larval stage
T_L_max = 37.0   # [°C] Lethal upper water temperature (no larvae survive)

# Larval development equation:
#   R_L = (T_wat - T_L_min) / K_L    if T_L_min < T_wat < T_L_max, else 0
# where R_L is the fraction of the larval life cycle completed per day.
```

### 2.2 Larval survival, crowding, and flushing

```python
# ---------------------------
# Larval survival
# ---------------------------

P_L_surv0   = 0.825  # Base daily larval survival (no crowding, no flushing)
M_L_max     = 300.0  # [mg m^-2] Larval biomass capacity (carrying capacity)
tau_flush   = 50.0   # [mm/day] Rainfall scale for flushing
K_flush_inf = 0.4    # Survival of early larvae under very heavy rain (asymptote)

# We will compute:
#   crowd_term = 1 - M_L / (w * M_L_max)        (bounded to [0,1])
#   P_L_surv_crowd = crowd_term * P_L_surv0     (crowding-only survival)
#   K_flush = L_f + (1 - L_f) * [ (1 - K_flush_inf)*exp(-R_d/tau_flush) + K_flush_inf ]
#   P_L_surv = P_L_surv_crowd * K_flush         (total survival)
```

### 2.3 Gonotrophic cycle (egg development)

```python
# ---------------------------
# Gonotrophic cycle (egg development)
# ---------------------------

T_gono_min = 7.7    # [°C] Minimum temperature for egg development
K_gono     = 37.1   # [degree-days] Degree-days needed to complete gonotrophic cycle

# Gonotrophic rate:
#   R_gono = (T_eff - T_gono_min) / K_gono   if T_eff > T_gono_min, else 0
# Gonotrophic period (days) = 1 / R_gono
```

### 2.4 Sporogonic (parasite) cycle

```python
# ---------------------------
# Sporogonic (parasite) cycle
# ---------------------------

T_sporo_min = 16.0  # [°C] Minimum temperature for parasite development
K_sporo     = 111.0 # [degree-days] Degree-days for sporogonic cycle (EIP)

# Parasite development rate:
#   R_sporo = (T_eff - T_sporo_min) / K_sporo   if T_eff > T_sporo_min, else 0
# Extrinsic incubation period (EIP, days) = 1 / R_sporo
```

### 2.5 Adult vector survival (Martens II) and lifespan

```python
# ---------------------------
# Adult vector survival (Martens II)
# ---------------------------

K_mar2_0 = -4.4
K_mar2_1 =  1.31
K_mar2_2 = -0.03

# Daily survival probability:
#   den = K_mar2_0 + K_mar2_1 * T_eff + K_mar2_2 * T_eff^2
#   P_V_surv = exp(-1 / den)  if den > 0, else 0
#
# Approximate expected lifespan (days):
#   lifespan = 1 / (1 - P_V_surv)   if P_V_surv < 1, else infinite
```

### 2.6 Indoor temperature and effective mosquito temperature

```python
# ---------------------------
# Indoor temperature & effective temperature
# ---------------------------

T0_indoor = 10.33  # [°C] Intercept for indoor temperature
K_indoor  = 0.58   # [-]  Slope relating outdoor T to indoor T

# Indoor temperature:
#   T_indoor = T0_indoor + K_indoor * T2m
#
# Effective temperature (fraction of time indoors = beta_indoor):
#   T_eff = beta_indoor * T_indoor + (1 - beta_indoor) * T2m
```

### 2.7 Host–vector system & transmission

```python
# ---------------------------
# Host–vector system
# ---------------------------

tau_zoo = 50.0   # [people/km^2 or people] Scale for zoophily/anthropophily
P_hv    = 0.2    # P(mosquito infected | bite on infectious host)
P_vh    = 0.3    # P(host infected | infectious bite)

# Mean human biting rate:
#   hbr_bar = (1 - exp(-H / tau_zoo)) * V_biting / H
#
# Daily EIR:
#   EIR_d = hbr_bar * CSPR
#
# Vector -> host infection probability per day:
#   P_v_to_h = 1 - exp(-EIR_d * P_vh)
```

### 2.8 Simple pond hydrology (temporary ponds)

```python
# ---------------------------
# Simple pond hydrology parameters
# ---------------------------

w_max = 0.04  # Max fractional pond coverage (4% of grid cell)
E     = 5.0   # [mm/day] Evaporation
I     = 245.0 # [mm/day] Infiltration
K_w   = 0.001 # Geometry/scale factor

# Pond fraction evolution (conceptual ODE):
#   dw/dt = K_w * [ rain * (w_max - w) - w * (E + I) ]
#
# We will store:
#   pond_inflow  = rain * (w_max - w_prev)
#   pond_outflow = w_prev * (E + I)
#   pond_balance = pond_inflow - pond_outflow   (mm/day equivalent)
```

---

## 3. Climate Time Series (Single Location)

We create a synthetic 180-day series of daily temperature and rainfall,
roughly mimicking a warm tropical site with moderate rainfall variability.

```python
# Time axis: 180 days
dates = pd.date_range("2025-01-01", periods=180, freq="D")
day_of_year = dates.dayofyear.values

# Synthetic air temperature [°C]: seasonal cycle around 24 °C
T2m = 24.0 + 3.0 * np.sin(2 * np.pi * (day_of_year / 365.0))

# Synthetic rainfall [mm/day]: random Gamma distribution (episodic wet days)
rng = np.random.default_rng(42)
rain = rng.gamma(shape=2.0, scale=3.0, size=len(dates))  # mean ~6 mm/day

climate_df = pd.DataFrame({"T2m": T2m, "rain": rain}, index=dates)
climate_df.head()
```

---

## 4. Location-Specific Constants

We hold these fixed over time for this demo. In a full VECTRI run, many of
these are dynamic or spatially varying.

```python
# Larval & hydrological state
M_L      = 3.0   # [mg m^-2] Larval biomass (assumed constant for simplicity)
L_f      = 0.25  # [-] Early larval stage (0 = very early, 1 = about to emerge)
delta_Tw = 1.5   # [°C] Water temperature offset relative to air

# Ponds: initial fraction
w0 = 0.0         # start completely dry

# Host & vector
H            = 200.0  # Humans in the cell
H_inf_frac   = 0.10   # Fraction infectious
V_biting     = 50.0   # Biting mosquitoes (number)
CSPR         = 0.10   # Circumsporozoite protein rate (infectious fraction)
beta_indoor  = 0.5    # Fraction of time mosquitoes spend indoors

H_inf = H * H_inf_frac  # number of infectious humans
```

---

## 5. Core Equations Applied Day by Day

We loop through each day and compute all quantities using the equations
written explicitly above.

```python
n = len(climate_df)

# Hydrology
w = np.zeros(n)           # pond fraction
w[0] = w0
pond_inflow  = np.zeros(n)  # mm/day equivalent inflow
pond_outflow = np.zeros(n)  # mm/day equivalent outflow
pond_balance = np.zeros(n)  # inflow - outflow

# Temperatures
Twat   = np.zeros(n)  # water temperature
T_ind  = np.zeros(n)  # indoor temperature
T_eff  = np.zeros(n)  # effective mosquito temperature

# Larval development & survival
R_L                = np.zeros(n)
larval_period_days = np.zeros(n)
K_flush            = np.zeros(n)
P_L_surv_crowd     = np.zeros(n)
P_L_surv           = np.zeros(n)

# Adult & parasite
R_gono      = np.zeros(n)
gono_period = np.zeros(n)
R_sporo     = np.zeros(n)
EIP_days    = np.zeros(n)
P_V_surv    = np.zeros(n)
lifespan    = np.zeros(n)  # approximate expected lifespan (days)

# Host-vector
hbr_bar = np.zeros(n)
EIR_d   = np.zeros(n)
P_h2v   = np.zeros(n)   # host -> vector infection prob per bite
P_v2h   = np.zeros(n)   # vector -> host infection prob per day

for i, (date, row) in enumerate(climate_df.iterrows()):
    # --- Climate inputs ---
    T2  = row["T2m"]
    Rd  = row["rain"]
    
    # --- Hydrology: pond fraction and water balance ---
    if i == 0:
        w_prev = w0
    else:
        w_prev = w[i-1]
    
    # Components of the water balance (mm/day equivalent)
    inflow  = Rd * (w_max - w_prev)
    outflow = w_prev * (E + I)
    pond_inflow[i]  = inflow
    pond_outflow[i] = outflow
    pond_balance[i] = inflow - outflow
    
    # ODE for pond fraction: dw/dt = K_w * (inflow - outflow)
    dw = K_w * (inflow - outflow)
    w[i] = w_prev + dw
    if w[i] < 0.0:
        w[i] = 0.0
    if w[i] > w_max:
        w[i] = w_max
    
    # --- Temperatures ---
    # Water temperature: T_wat = T2m + delta_Tw
    Tw = T2 + delta_Tw
    Twat[i] = Tw
    
    # Indoor temperature: T_ind = T0_indoor + K_indoor * T2m
    Ti = T0_indoor + K_indoor * T2
    T_ind[i] = Ti
    
    # Effective temperature: T_eff = beta_indoor*T_ind + (1 - beta_indoor)*T2m
    Teff = beta_indoor * Ti + (1.0 - beta_indoor) * T2
    T_eff[i] = Teff
    
    # --- Larval development ---
    if Tw <= T_L_min or Tw >= T_L_max:
        RL = 0.0
    else:
        RL = (Tw - T_L_min) / K_L
    R_L[i] = RL
    if RL > 0.0:
        larval_period_days[i] = 1.0 / RL
    else:
        larval_period_days[i] = math.inf
    
    # --- Flushing factor ---
    # K_flush = L_f + (1 - L_f) * [ (1 - K_flush_inf)*exp(-Rd / tau_flush) + K_flush_inf ]
    inner = (1.0 - K_flush_inf) * math.exp(-Rd / tau_flush) + K_flush_inf
    Kf = L_f + (1.0 - L_f) * inner
    K_flush[i] = Kf
    
    # --- Larval survival components ---
    if w[i] <= 0.0:
        # No ponds: no larvae survive
        P_L_surv_crowd[i] = 0.0
        P_L_surv[i]       = 0.0
    else:
        # crowd_term = 1 - M_L / (w * M_L_max)
        crowd_term = 1.0 - M_L / (w[i] * M_L_max)
        if crowd_term < 0.0:
            crowd_term = 0.0
        if crowd_term > 1.0:
            crowd_term = 1.0
        
        # Crowding-only survival
        PL_crowd = crowd_term * P_L_surv0
        if PL_crowd < 0.0:
            PL_crowd = 0.0
        if PL_crowd > 1.0:
            PL_crowd = 1.0
        P_L_surv_crowd[i] = PL_crowd
        
        # Total survival including flushing
        PL = PL_crowd * Kf
        if PL < 0.0:
            PL = 0.0
        if PL > 1.0:
            PL = 1.0
        P_L_surv[i] = PL
    
    # --- Gonotrophic cycle ---
    if Teff <= T_gono_min:
        Rg = 0.0
    else:
        Rg = (Teff - T_gono_min) / K_gono
    R_gono[i] = Rg
    if Rg > 0.0:
        gono_period[i] = 1.0 / Rg
    else:
        gono_period[i] = math.inf
    
    # --- Sporogonic cycle (parasite) ---
    if Teff <= T_sporo_min:
        Rs = 0.0
    else:
        Rs = (Teff - T_sporo_min) / K_sporo
    R_sporo[i] = Rs
    if Rs > 0.0:
        EIP_days[i] = 1.0 / Rs
    else:
        EIP_days[i] = math.inf
    
    # --- Adult vector survival and lifespan ---
    den = K_mar2_0 + K_mar2_1 * Teff + K_mar2_2 * (Teff**2)
    if den <= 0.0:
        PV = 0.0
    else:
        PV = math.exp(-1.0 / den)
    if PV < 0.0:
        PV = 0.0
    if PV > 1.0:
        PV = 1.0
    P_V_surv[i] = PV
    
    # Approx expected lifespan
    if PV >= 0.999:
        lifespan[i] = math.inf
    elif PV <= 0.0:
        lifespan[i] = 0.0
    else:
        lifespan[i] = 1.0 / (1.0 - PV)
    
    # --- Host-vector interactions ---
    # Mean human biting rate:
    if H <= 0.0:
        hbr = 0.0
    else:
        phi = 1.0 - math.exp(-H / tau_zoo)
        hbr = phi * V_biting / H
    hbr_bar[i] = hbr
    
    # Daily EIR: EIR_d = hbr_bar * CSPR
    eir = hbr * CSPR
    EIR_d[i] = eir
    
    # Host -> vector infection probability per blood meal:
    if H <= 0.0:
        Ph2v = 0.0
    else:
        Ph2v = (H_inf / H) * P_hv
    P_h2v[i] = Ph2v
    
    # Vector -> host daily infection probability:
    #   P_v2h = 1 - exp(-EIR_d * P_vh)
    Pv2h = 1.0 - math.exp(-eir * P_vh)
    P_v2h[i] = Pv2h
```

---

## 6. Pack Results into a DataFrame

```python
ts_df = pd.DataFrame(
    {
        "T2m": T2m,
        "rain": rain,
        "w": w,
        "pond_inflow": pond_inflow,
        "pond_outflow": pond_outflow,
        "pond_balance": pond_balance,
        "Twat": Twat,
        "T_indoor": T_ind,
        "T_eff": T_eff,
        "R_L": R_L,
        "larval_period_days": larval_period_days,
        "K_flush": K_flush,
        "P_L_surv_crowd": P_L_surv_crowd,
        "P_L_surv": P_L_surv,
        "R_gono": R_gono,
        "gono_period_days": gono_period,
        "R_sporo": R_sporo,
        "EIP_days": EIP_days,
        "P_V_surv": P_V_surv,
        "lifespan_days": lifespan,
        "hbr": hbr_bar,
        "EIR_d": EIR_d,
        "P_h2v": P_h2v,
        "P_v2h": P_v2h,
    },
    index=dates,
)

ts_df.head()
```

---

## 7. Basic Summaries

```python
print("=== Basic summaries over the 180 days ===")
print(f"Mean T2m                : {ts_df['T2m'].mean():.2f} °C")
print(f"Mean Twat               : {ts_df['Twat'].mean():.2f} °C")
print(f"Mean T_indoor           : {ts_df['T_indoor'].mean():.2f} °C")
print(f"Mean larval R_L         : {ts_df['R_L'].mean():.4f} frac/day")
print(f"Mean larval survival    : {ts_df['P_L_surv'].mean():.3f}")
print(f"Mean EIP (finite only)  : {ts_df['EIP_days'].replace(math.inf, float('nan')).mean():.2f} days")
print(f"Mean P_V_surv           : {ts_df['P_V_surv'].mean():.3f}")
print(f"Mean lifespan (finite)  : {ts_df['lifespan_days'].replace(math.inf, float('nan')).mean():.2f} days")
print(f"Mean hbr                : {ts_df['hbr'].mean():.3f} bites/person/day")
print(f"Mean daily EIR          : {ts_df['EIR_d'].mean():.4f} inf. bites/person/day")
print(f"Mean P_v2h (per day)    : {ts_df['P_v2h'].mean():.4f}")
```

---

## 8. Plot Templates and Physical Interpretation

Below are the code snippets used in the notebook to make physically meaningful plots.
You can keep them here as templates or run them directly in a notebook.

### 8.1 Daily Temperatures (Air, Indoor, Effective, Water)

This figure shows how different temperatures relevant to VECTRI relate:

- **T2m**: outdoor air temperature.  
- **T_indoor**: parameterized indoor temperature.  
- **T_eff**: effective temperature seen by mosquitoes (here 50% time indoors).  
- **Twat**: water temperature in breeding sites (slightly warmer than air).

These temperatures drive larval development, adult survival, and parasite development.

```python
plt.figure(figsize=(11, 4))
plt.plot(ts_df.index, ts_df["T2m"], label="T2m (air)")
plt.plot(ts_df.index, ts_df["T_indoor"], label="T_indoor")
plt.plot(ts_df.index, ts_df["T_eff"], label="T_eff")
plt.plot(ts_df.index, ts_df["Twat"], label="Twat (water)", linestyle="--")
plt.ylabel("Temperature (°C)")
plt.xlabel("Date")
plt.title("Daily Temperature: Air, Indoor, Effective, and Water")
plt.legend()
plt.tight_layout()
plt.show()
```

### 8.2 Rainfall, Water Balance, and Pond Fraction (Breeding Habitat)

Here we show:

- **Rainfall (bars)**: incoming water from precipitation.  
- **Pond inflow / outflow (lines)**: conceptual water balance terms.  
- **Pond fraction w (line)**: fraction of the cell covered by temporary ponds.

Physically:

- On days with heavy rain, inflow dominates → pond fraction increases toward **w_max** (here 4%).  
- In dry spells, outflow (evaporation + infiltration) dominates → ponds shrink and may disappear, reducing breeding habitat and carrying capacity.

```python
fig, ax1 = plt.subplots(figsize=(11, 4))

ax1.bar(ts_df.index, ts_df["rain"], alpha=0.4, label="Rain (mm/day)")
ax1.set_ylabel("Rain (mm/day)")
ax1.set_xlabel("Date")

ax2 = ax1.twinx()
ax2.plot(ts_df.index, ts_df["pond_inflow"], label="Pond inflow", linestyle="-")
ax2.plot(ts_df.index, ts_df["pond_outflow"], label="Pond outflow", linestyle="--")
ax2.plot(ts_df.index, ts_df["w"], label="Pond fraction w", linewidth=2)
ax2.set_ylabel("Inflow/Outflow (mm/day) & w (fraction)")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.title("Rainfall, Water Balance, and Pond Fraction (Breeding Habitat)")
plt.tight_layout()
plt.show()
```

### 8.3 Larval Survival Components: Crowding, Flushing, and Total Survival

This figure shows:

- **P_L_surv_crowd**: survival due to crowding and base survival only.  
- **K_flush**: flushing factor (1 = no extra mortality; <1 = some larvae washed out).  
- **P_L_surv**: total larval daily survival (crowding × flushing).

Physical interpretation:

- When ponds are small or larval biomass is high, **crowding** reduces P_L_surv_crowd.  
- On heavy-rainfall days, **K_flush** drops, especially affecting early instars.  
- The combined effect **P_L_surv** determines how many larvae survive to the next day.

```python
plt.figure(figsize=(11, 4))
plt.plot(ts_df.index, ts_df["P_L_surv_crowd"], label="P_L_surv_crowd (crowding only)")
plt.plot(ts_df.index, ts_df["K_flush"], label="K_flush (flushing factor)")
plt.plot(ts_df.index, ts_df["P_L_surv"], label="P_L_surv (total)")
plt.ylabel("Probability / Factor")
plt.xlabel("Date")
plt.ylim(0, 1.05)
plt.title("Larval Survival: Crowding, Flushing, and Total Survival")
plt.legend()
plt.tight_layout()
plt.show()
```

### 8.4 Development Times: Larval Period, Gonotrophic Period, and EIP

Here we plot:

- **Larval period** (if finite): approximate days to complete larval development.  
- **Gonotrophic period**: days between blood meals and egg laying.  
- **EIP (sporogonic period)**: days for the parasite to develop inside the mosquito.

Physically:

- At warmer temperatures, **all three periods shorten**, increasing vector density and transmission potential.  
- In cooler conditions, the **EIP** can exceed typical mosquito lifespans, greatly reducing transmission.

```python
plt.figure(figsize=(11, 4))
plt.plot(ts_df.index, ts_df["larval_period_days"], label="Larval period (days)", alpha=0.7)
plt.plot(ts_df.index, ts_df["gono_period_days"], label="Gonotrophic period (days)")
plt.plot(ts_df.index, ts_df["EIP_days"], label="EIP (parasite, days)")
plt.ylabel("Days")
plt.xlabel("Date")
plt.ylim(0, 40)
plt.title("Larval, Gonotrophic, and Sporogonic (EIP) Periods")
plt.legend()
plt.tight_layout()
plt.show()
```

### 8.5 Adult Vector Survival and Approximate Lifespan

We plot:

- **P_V_surv**: daily survival probability of adult mosquitoes.  
- **lifespan_days**: approximate expected number of days an adult survives (\(1 / (1 - P_V_surv)\)).

Physical meaning:

- When **P_V_surv** is high (e.g. >0.9), typical lifespans are >10 days, allowing mosquitoes to complete multiple gonotrophic cycles and EIP.  
- If **P_V_surv** drops (e.g. due to unfavorable temperature or interventions), lifespans shorten and many mosquitoes die before becoming infectious.

```python
plt.figure(figsize=(11, 4))
plt.plot(ts_df.index, ts_df["P_V_surv"], label="P_V_surv (daily survival)")
plt.ylabel("Daily survival probability")
plt.xlabel("Date")
plt.ylim(0, 1.05)
plt.title("Adult Vector Daily Survival Probability")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(11, 4))
lifesp = ts_df["lifespan_days"].replace(math.inf, np.nan)
plt.plot(ts_df.index, lifesp)
plt.ylabel("Expected lifespan (days)")
plt.xlabel("Date")
plt.title("Approximate Adult Mosquito Lifespan")
plt.tight_layout()
plt.show()
```

### 8.6 Transmission Metrics: Human Biting Rate, Daily EIR, and Vector → Host Infection Probability

This final figure focuses on **transmission intensity**:

- **hbr**: mean human biting rate (bites per person per day).  
- **EIR_d**: daily entomological inoculation rate (infectious bites per person per day).  
- **P_v2h**: daily probability that a **susceptible human** is infected by mosquito bites.

Physical interpretation:

- As vector density or infectious fraction (CSPR) increases, **EIR_d** and **P_v2h** rise.  
- Even modest daily infection probabilities (a few percent) can lead to very high annual infection pressure.

```python
fig, ax1 = plt.subplots(figsize=(11, 4))

ax1.plot(ts_df.index, ts_df["hbr"], label="hbr (bites/person/day)")
ax1.set_ylabel("Bites / Infectious bites per person per day")
ax1.set_xlabel("Date")

ax2 = ax1.twinx()
ax2.plot(ts_df.index, ts_df["EIR_d"], label="EIR_d (infectious bites/person/day)", color="tab:orange")
ax2.plot(ts_df.index, ts_df["P_v2h"], label="P_v2h (vector→host infection prob)", color="tab:green")
ax2.set_ylabel("EIR / Infection probability")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.title("Human Biting Rate, Daily EIR, and Vector → Host Infection Probability")
plt.tight_layout()
plt.show()
```


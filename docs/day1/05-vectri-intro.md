---
hide:
  - toc
---


### 1.1 History

**VECTRI** was created when _Adrian Tompkins_, originally a tropical cloud/convection scientist, joined an EU project on climate impacts on health. 

- The main malaria model in that project (**LMM – Liverpool Malaria Model**) assumed a __fixed human population of 100 people per grid box__ and __distributed only an executable__, __not source code__.

After questioning how such a model could represent rural vs. urban differences – where population density is critical – Tompkins was told:

> "If you want a code you can play with, why don't you just write one yourself?"

With colleague __Volker Ermert__ providing literature guidance, Tompkins implemented process relationships for vector-borne disease transmission. After ~4 weeks of intense coding, **VECTRI v1.0** was born and released as an **open-source community model**.

### 1.2 What VECTRI *is*

From the docs:

- A **gridded**, climate-driven model that focuses on **mosquito life-cycle dynamics**.
- Supports multiple **Anopheles** and **Aedes** species (one vector at a time).
- Currently only **malaria** is represented as a disease (for Anopheles vectors).
- Can run from **continental** scales down to roughly **1 km** resolution.
- Designed to be **fast**: uses 1st-order accurate solvers, accepting some numerical approximation because **process and parameter uncertainties dominate**.
- Can also be run for **single locations (points)**.
- Fully **open source**: users are encouraged to read, modify and improve the code and to contribute back.

### 1.3 What VECTRI *is not*

Also from the docs:

- Not a fully supported "product", **research tool provided as-is** by a small team. It needs comprehensive calibration and validation.
- Interventions (bednets, SIT) are present but **not as extensively validated** as in dedicated operational tools like OpenMalaria.
- Simulates primarily **climate impacts** on malaria; therefore, predicted clinical case numbers can exceed observations because routine health system effects (treatment, health-seeking behaviour, many control measures) are not fully represented.
- Not a "point-and-click" GUI: it is a **Fortran90 + bash** tool that assumes **basic Linux familiarity**.
- Not guaranteed to be always up-to-date with a GUI or Python wrapper; those are aspirational, but core science developments take priority.

### 1.4 Further reading 

VECTRI documentation is evolving. The upstream manual (including the HTML docs) is stored **inside the same git repository** as the model. This training course builds on:

- The VECTRI online documentation at [VECTRI](https://users.ictp.it/~tompkins/vectri/documentation/) 

- The PDF manual `VECTRI_manual_v1.6.pdf` [VECTRI PDF manual](../pdfs/VECTRI_manual_v1.6.pdf): Introductory sections describing motivation and history.

---

## 📝 Test Your Knowledge

Ready to test your understanding of VECTRI? Take the interactive quiz to assess your knowledge of VECTRI's history, capabilities, and limitations.

<div style="text-align: center; margin: 2rem 0;">
  <a href="/quizzes/vectri-intro-quiz/" class="md-button md-button--primary" style="font-size: 1.2rem; padding: 1rem 2rem; text-decoration: none; display: inline-block;">
    📝 Take the Quiz
  </a>
</div>

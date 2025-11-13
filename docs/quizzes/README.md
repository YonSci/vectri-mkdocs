# Workshop Quizzes

Interactive quizzes to test your understanding of key concepts.

---

## Available Quizzes

### Python & Data Science Fundamentals

- [Xarray Basics](xarray-basics.md) - Working with multi-dimensional labeled arrays and NetCDF files

### Coming Soon

- **NumPy & Pandas** - Array operations and data manipulation
- **NetCDF Operations** - Working with climate data files
- **Linux Command Line** - Essential shell commands for data processing
- **Git & GitHub** - Version control basics
- **Climate Data** - ERA5, CHIRPS, and data quality control
- **VECTRI Model** - Model structure, inputs, and outputs
- **Malaria Biology** - Vector dynamics and transmission
- **Statistical Validation** - Correlation, RMSE, and model evaluation

---

## Quiz Format

Each quiz uses MkDocs Material's **admonitions** with collapsible answers:

### Example Format:

```markdown
## Question X: Topic

**Question text here?**

??? question "Select the correct answer"
    - [ ] Wrong option
    - [x] Correct option
    - [ ] Wrong option
    - [ ] Wrong option
    
    !!! success "Correct Answer"
        Explanation with code example if applicable.
```

---

## How to Use

1. **Read the question** carefully
2. **Think about your answer** before revealing
3. **Click to expand** the answer section
4. **Review the explanation** and code examples
5. **Practice** the concepts in the workshop labs

---

## Adding New Quizzes

To create a new quiz:

1. Create a new `.md` file in this directory
2. Use the format from `xarray-basics.md` as a template
3. Include 8-10 questions covering key concepts
4. Add code examples in the explanations
5. Update this README with the new quiz link

---

## Integration with Assessments

These quizzes complement the daily assessments:

- **Day 1**: Linux basics, Git, VECTRI installation
- **Day 2**: Xarray, NetCDF, climate data processing
- **Day 3**: Population data, environmental factors
- **Day 4**: VECTRI outputs, validation metrics
- **Day 5**: Early warning systems, visualization

---

!!! tip "Self-Assessment"
    These quizzes are for **self-assessment** and don't count toward your grade. Use them to:
    
    - Check your understanding before labs
    - Review concepts after lectures
    - Prepare for daily assessments
    - Identify areas needing more practice


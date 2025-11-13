# Xarray Basics Quiz

Test your understanding of Xarray fundamentals for climate data analysis.

---

## 📋 Assessment Guidelines

### How This Quiz Works

!!! tip "Interactive Format"
    - **Multiple choice** questions with 4 options
    - **Multiple select** questions (check all that apply)
    - **True/False** questions for quick concept checks
    - Click to reveal answers and explanations

!!! success "Instant Feedback"
    - Get immediate results with detailed explanations
    - Understand why answers are correct or incorrect
    - Learn best practices and common pitfalls

!!! example "Code Examples"
    - Questions include real Python code snippets
    - Analyze code behavior and outputs
    - Practice reading and understanding Xarray syntax

!!! question "Hints Available"
    - Look for 💡 hint sections if you get stuck
    - Hints guide you toward the answer without giving it away
    - Use hints to learn problem-solving strategies

!!! info "Retake Anytime"
    - Quiz results are **not saved** or graded
    - Retake as many times as you want to improve understanding
    - Perfect for review before workshop labs

---

## Question 1: Data Structure

**What is the primary data structure in Xarray for working with multi-dimensional labeled arrays?**

??? hint "💡 Need a hint?"
    Think about what "Array" structure would be suitable for multi-dimensional data with labels...

??? question "Select the correct answer"
    - [ ] DataFrame
    - [x] DataArray
    - [ ] Series
    - [ ] Matrix
    
    !!! success "Correct Answer"
        **DataArray** is the primary data structure in Xarray. It's like a pandas Series but for multi-dimensional arrays with labeled dimensions and coordinates.
        
        **Why others are wrong:**
        - DataFrame is pandas' 2D structure
        - Series is pandas' 1D structure
        - Matrix is a generic NumPy term

---

## Question 2: Opening NetCDF Files

**Which Xarray function is used to open a NetCDF file?**

??? question "Select the correct answer"
    - [ ] xr.read_netcdf()
    - [x] xr.open_dataset()
    - [ ] xr.load_netcdf()
    - [ ] xr.open_file()
    
    !!! success "Correct Answer"
        **xr.open_dataset()** is the standard function to open NetCDF files. For example:
        ```python
        import xarray as xr
        ds = xr.open_dataset('climate_data.nc')
        ```

---

## Question 3: Selecting Data

**How do you select data for a specific time period in Xarray?**

??? question "Select the correct answer"
    - [ ] ds.filter(time='2020')
    - [ ] ds.query(time='2020')
    - [x] ds.sel(time='2020')
    - [ ] ds.select(time='2020')
    
    !!! success "Correct Answer"
        **ds.sel()** (select) is used for label-based indexing. For example:
        ```python
        # Select a specific date
        ds.sel(time='2020-01-01')
        
        # Select a time slice
        ds.sel(time=slice('2020-01-01', '2020-12-31'))
        ```

---

## Question 4: Dimensions and Coordinates

**What's the difference between dimensions and coordinates in Xarray?**

??? question "Select the correct answer"
    - [ ] They are the same thing
    - [ ] Dimensions store data values, coordinates are labels
    - [x] Dimensions are axis names, coordinates are the labels along those axes
    - [ ] Coordinates are optional, dimensions are required
    
    !!! success "Correct Answer"
        **Dimensions are axis names** (like 'time', 'lat', 'lon'), while **coordinates are the actual labels** along those axes (like specific dates, latitude values, longitude values).
        
        Example:
        ```python
        ds = xr.Dataset({
            'temperature': (['time', 'lat', 'lon'], data)
        })
        # Dimensions: time, lat, lon
        # Coordinates: actual time values, lat values, lon values
        ```

---

## Question 5: Aggregation Operations

**Which method would you use to calculate the mean temperature across all time steps?**

??? question "Select the correct answer"
    - [ ] ds.temperature.average(dim='time')
    - [x] ds.temperature.mean(dim='time')
    - [ ] ds.temperature.avg(axis='time')
    - [ ] ds.temperature.reduce_mean('time')
    
    !!! success "Correct Answer"
        **mean(dim='time')** calculates the average along the time dimension:
        ```python
        # Calculate temporal mean
        temp_mean = ds.temperature.mean(dim='time')
        
        # Calculate spatial mean
        temp_spatial = ds.temperature.mean(dim=['lat', 'lon'])
        ```

---

## Question 6: Multiple Operations (Multiple Select)

**Which of the following are valid aggregation methods in Xarray? (Select all that apply)**

??? hint "💡 Need a hint?"
    Think about common statistical operations you'd perform on climate data...

??? question "Select ALL correct answers"
    - [x] mean()
    - [x] sum()
    - [ ] average()
    - [x] std()
    - [x] median()
    - [ ] avg()
    
    !!! success "Correct Answers"
        **Valid methods: mean(), sum(), std(), median()**
        
        These are all standard Xarray aggregation methods:
        ```python
        # All valid
        ds.temperature.mean(dim='time')
        ds.precipitation.sum(dim='time')
        ds.temperature.std(dim='time')
        ds.temperature.median(dim='time')
        ```
        
        **Invalid methods:**
        - `average()` - use `mean()` instead
        - `avg()` - use `mean()` instead

---

## Question 7: True or False

**True or False: Xarray automatically aligns data based on coordinate labels when performing operations between DataArrays.**

??? hint "💡 Need a hint?"
    Consider what happens when you add two DataArrays with different coordinate values...

??? question "Select True or False"
    - [x] True
    - [ ] False
    
    !!! success "Correct Answer"
        **True!** This is one of Xarray's most powerful features.
        
        **Automatic alignment** means:
        ```python
        # Even if coordinates don't match exactly
        da1 = xr.DataArray([1, 2, 3], coords=[('x', [1, 2, 3])])
        da2 = xr.DataArray([4, 5, 6], coords=[('x', [2, 3, 4])])
        
        result = da1 + da2
        # Xarray aligns on matching coordinates [2, 3]
        # Result: [6, 8] at x=[2, 3]
        ```
        
        This prevents many common data alignment errors!

---

## Question 8: Resampling Time Series

**How do you resample daily temperature data to monthly averages in Xarray?**

??? hint "💡 Need a hint?"
    The method name is `resample()` and you need to specify a frequency string like '1M' for monthly...

??? question "Select the correct answer"
    - [ ] ds.resample(time='M').average()
    - [x] ds.resample(time='1M').mean()
    - [ ] ds.groupby('time.month').mean()
    - [ ] ds.resample_time('monthly').mean()
    
    !!! success "Correct Answer"
        **resample(time='1M').mean()** resamples to monthly frequency and calculates the mean:
        ```python
        # Resample daily to monthly
        monthly = ds.resample(time='1M').mean()
        
        # Resample to seasonal (3-month)
        seasonal = ds.resample(time='3M').mean()
        ```
        
        **Why others are wrong:**
        - 'M' needs to be '1M' for proper frequency
        - `average()` should be `mean()`
        - `groupby('time.month')` groups by month across years (different purpose)
        - `resample_time()` is not a valid method

---

## Question 7: Masking Data

**How do you mask (filter) temperature values below 0°C in Xarray?**

??? question "Select the correct answer"
    - [ ] ds.temperature.filter(lambda x: x >= 0)
    - [ ] ds.temperature.mask(ds.temperature < 0)
    - [x] ds.temperature.where(ds.temperature >= 0)
    - [ ] ds.temperature.query('temperature >= 0')
    
    !!! success "Correct Answer"
        **where()** keeps values where the condition is True and replaces others with NaN:
        ```python
        # Keep only temperatures >= 0°C
        temp_positive = ds.temperature.where(ds.temperature >= 0)
        
        # Drop NaN values
        temp_positive_dropped = ds.temperature.where(ds.temperature >= 0, drop=True)
        ```

---

## Question 8: Working with Multiple Files

**Which function opens multiple NetCDF files at once along a new dimension?**

??? question "Select the correct answer"
    - [ ] xr.open_multiple()
    - [ ] xr.concat_datasets()
    - [x] xr.open_mfdataset()
    - [ ] xr.merge_files()
    
    !!! success "Correct Answer"
        **xr.open_mfdataset()** (multi-file dataset) opens and concatenates multiple files:
        ```python
        # Open all NetCDF files in a directory
        ds = xr.open_mfdataset('data/*.nc', combine='by_coords')
        
        # Open specific files
        ds = xr.open_mfdataset(['file1.nc', 'file2.nc', 'file3.nc'])
        ```

---

## Question 9: Regridding/Interpolation

**How do you interpolate data to a new set of coordinates in Xarray?**

??? question "Select the correct answer"
    - [ ] ds.regrid(new_coords)
    - [x] ds.interp(lat=new_lats, lon=new_lons)
    - [ ] ds.resample(lat=new_lats, lon=new_lons)
    - [ ] ds.interpolate(coords={'lat': new_lats, 'lon': new_lons})
    
    !!! success "Correct Answer"
        **interp()** performs interpolation to new coordinate values:
        ```python
        # Interpolate to new lat/lon grid
        new_lats = np.arange(-5, 15, 0.1)
        new_lons = np.arange(33, 42, 0.1)
        ds_regrid = ds.interp(lat=new_lats, lon=new_lons)
        
        # Can also use interp_like() to match another dataset's grid
        ds_regrid = ds.interp_like(target_ds)
        ```

---

## Question 10: Saving Data

**What's the correct way to save an Xarray Dataset to a NetCDF file?**

??? question "Select the correct answer"
    - [ ] ds.save('output.nc')
    - [ ] ds.write_netcdf('output.nc')
    - [x] ds.to_netcdf('output.nc')
    - [ ] ds.export('output.nc', format='netcdf')
    
    !!! success "Correct Answer"
        **to_netcdf()** writes the dataset to a NetCDF file:
        ```python
        # Basic save
        ds.to_netcdf('output.nc')
        
        # With compression
        ds.to_netcdf('output.nc', encoding={
            'temperature': {'zlib': True, 'complevel': 5}
        })
        
        # Specify format
        ds.to_netcdf('output.nc', format='NETCDF4')
        ```

---

## Question 11: Code Analysis

**What will be the output of this code?**

```python
import xarray as xr
import numpy as np

da = xr.DataArray(
    [[10, 20], [30, 40]], 
    coords=[('x', [0, 1]), ('y', [0, 1])]
)

result = da.sel(x=0).values
print(result)
```

??? hint "💡 Need a hint?"
    `.sel(x=0)` selects the data where x coordinate equals 0. What row is that?

??? question "Select the correct answer"
    - [x] [10 20]
    - [ ] [10 30]
    - [ ] 10
    - [ ] [[10 20] [30 40]]
    
    !!! success "Correct Answer"
        **[10 20]** is correct!
        
        **Step-by-step explanation:**
        ```python
        # Original array:
        #     y=0  y=1
        # x=0 [10,  20]  ← This row is selected
        # x=1 [30,  40]
        
        # .sel(x=0) selects the first row (where x=0)
        # .values extracts numpy array: [10 20]
        ```
        
        **Why others are wrong:**
        - `[10 30]` would be `.sel(y=0)`
        - `10` would be `.sel(x=0, y=0)`
        - Original array would be no selection

---

## Bonus Question: Performance

**What's the lazy loading feature in Xarray, and when is it useful?**

??? question "Think about it"
    !!! info "Answer"
        **Lazy loading** means Xarray doesn't load data into memory immediately when you open a file. Data is only loaded when you actually need it (e.g., when computing or plotting).
        
        **Benefits:**
        - Work with datasets larger than RAM
        - Faster initial file opening
        - Only load what you need
        
        **Example:**
        ```python
        # Open without loading data (lazy)
        ds = xr.open_dataset('large_file.nc')
        
        # Data loads only when needed
        result = ds.temperature.mean().compute()  # Now it loads and computes
        
        # Load entire dataset into memory
        ds_loaded = ds.load()
        ```

---

## 📊 Quiz Summary

### What You've Learned:

✅ **11 Questions** covering essential Xarray concepts  
✅ **3 Question Types**: Multiple choice, multiple select, true/false  
✅ **11 Code Examples** with real Python syntax  
✅ **8 Hints** to guide your problem-solving  
✅ **Instant Feedback** with detailed explanations

### Key Xarray Concepts Covered:

1. **DataArray & Dataset**: Core data structures
2. **Labeled dimensions**: time, lat, lon, etc.
3. **Selection**: `sel()`, `isel()`, `where()`
4. **Aggregation**: `mean()`, `sum()`, `std()`, etc.
5. **Resampling**: `resample()`, `groupby()`
6. **I/O**: `open_dataset()`, `to_netcdf()`
7. **Interpolation**: `interp()`, `interp_like()`
8. **Lazy loading**: Efficient memory usage
9. **Automatic alignment**: Label-based operations
10. **Code analysis**: Reading and understanding Xarray code

### Your Score

!!! question "How did you do?"
    - **9-11 correct**: Excellent! You're ready for the labs
    - **6-8 correct**: Good! Review missed topics before labs
    - **3-5 correct**: Keep practicing! Retake the quiz
    - **0-2 correct**: Review Xarray basics, then retake

### For More Practice:

- 📚 [Xarray Documentation](https://docs.xarray.dev/)
- 🎓 [Xarray Tutorial](https://tutorial.xarray.dev/)
- 💻 Workshop Lab exercises (Day 2 & 3)
- 🔄 **Retake this quiz** to improve your score!

---

!!! tip "Next Steps"
    1. **Retake this quiz** if needed to master concepts
    2. **Review explanations** for any questions you missed
    3. **Try the code examples** in Jupyter notebooks
    4. **Complete Day 2 labs** to apply your knowledge with real Amhara climate data
    
!!! success "Ready for More?"
    Check out other quizzes:
    
    - Coming soon: NumPy & Pandas
    - Coming soon: NetCDF Operations
    - Coming soon: Linux Command Line


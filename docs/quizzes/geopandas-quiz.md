# GeoPandas Quiz

Test your understanding of GeoPandas and geospatial data handling!

---

<style>
  .quiz-container {
    max-width: 900px;
    margin: 2rem auto;
    font-family: 'Roboto', sans-serif;
  }
  
  .question-block {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  
  .question-block h3 {
    color: white;
    margin-top: 0;
    font-size: 1.1rem;
    font-weight: 500;
  }
  
  .options {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
  }
  
  .option-label {
    display: block;
    padding: 0.75rem;
    margin: 0.5rem 0;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .option-label:hover {
    border-color: #43e97b;
    background-color: #f0fdf7;
  }
  
  .option-label input[type="radio"],
  .option-label input[type="checkbox"] {
    margin-right: 0.5rem;
  }
  
  .feedback {
    margin-top: 0.5rem;
    padding: 0.75rem;
    border-radius: 6px;
    display: none;
  }
  
  .feedback.correct {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
  }
  
  .feedback.incorrect {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
  }
  
  .quiz-controls {
    text-align: center;
    margin: 2rem 0;
  }
  
  .btn {
    padding: 0.75rem 2rem;
    font-size: 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin: 0.5rem;
    transition: all 0.3s ease;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    color: white;
  }
  
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(67, 233, 123, 0.4);
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
  }
  
  #quiz-results {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    display: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  
  #quiz-results h2 {
    color: #43e97b;
    margin-bottom: 1rem;
  }
  
  .score-display {
    font-size: 2.5rem;
    font-weight: bold;
    color: #38f9d7;
    margin: 1rem 0;
  }
  
  .note {
    background-color: #e7f9f5;
    border-left: 4px solid #43e97b;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
  }
</style>

<div class="quiz-container">
  <div class="note">
    <strong>📝 Note:</strong> This quiz contains 20 questions including multiple choice and multiple selection questions. Some questions may have more than one correct answer. Select all that apply for those questions.
  </div>

  <form id="geopandas-quiz">
    
    <!-- Question 1 -->
    <div class="question-block">
      <h3>1. What is the main difference between a Pandas DataFrame and a GeoPandas GeoDataFrame?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q1" value="wrong1">
          GeoDataFrame is faster than DataFrame
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="correct">
          GeoDataFrame has a geometry column and CRS metadata
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong2">
          GeoDataFrame can only handle spatial data
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong3">
          There is no difference
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 2 -->
    <div class="question-block">
      <h3>2. Which library provides the geometry objects (Point, Polygon, LineString) used in GeoPandas?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q2" value="wrong1">
          GeoPandas itself
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="correct">
          Shapely
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong2">
          PyProj
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong3">
          GDAL
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 3 -->
    <div class="question-block">
      <h3>3. What does CRS stand for in GeoPandas?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q3" value="wrong1">
          Cartographic Representation System
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="correct">
          Coordinate Reference System
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="wrong2">
          Coordinate Registration System
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="wrong3">
          Climate Reference System
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 4 -->
    <div class="question-block">
      <h3>4. Which method is used to change the CRS of a GeoDataFrame?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q4" value="wrong1">
          gdf.convert_crs()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="correct">
          gdf.to_crs()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong2">
          gdf.transform()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong3">
          gdf.reproject()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 5 -->
    <div class="question-block">
      <h3>5. What is the EPSG code for the WGS84 geographic coordinate system (latitude/longitude)?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q5" value="wrong1">
          EPSG:3857
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="correct">
          EPSG:4326
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong2">
          EPSG:32637
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong3">
          EPSG:2163
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 6 -->
    <div class="question-block">
      <h3>6. Which spatial operation creates a zone around geometries at a specified distance?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q6" value="wrong1">
          dissolve()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="correct">
          buffer()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong2">
          overlay()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong3">
          intersection()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 7 -->
    <div class="question-block">
      <h3>7. What does the dissolve() method do in GeoPandas?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q7" value="wrong1">
          Removes geometries from the GeoDataFrame
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="correct">
          Combines geometries based on an attribute (similar to groupby)
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong2">
          Splits geometries into smaller parts
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong3">
          Simplifies geometry vertices
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 8 -->
    <div class="question-block">
      <h3>8. Which GeoPandas methods perform spatial joins? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q8" value="correct1">
          sjoin()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="correct2">
          sjoin_nearest()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="wrong1">
          merge()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="wrong2">
          join_spatial()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 9 -->
    <div class="question-block">
      <h3>9. What is the purpose of the overlay() method in GeoPandas?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q9" value="wrong1">
          To plot one GeoDataFrame on top of another
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="correct">
          To perform spatial set operations (union, intersection, difference)
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong2">
          To merge two GeoDataFrames by index
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong3">
          To add transparency to geometries
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 10 -->
    <div class="question-block">
      <h3>10. Which file formats can GeoPandas read and write? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct1">
          Shapefile (.shp)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct2">
          GeoJSON (.geojson)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct3">
          GeoPackage (.gpkg)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="wrong1">
          NetCDF (.nc)
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 11 -->
    <div class="question-block">
      <h3>11. How do you create a Point geometry from coordinates in Shapely?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q11" value="correct">
          Point(longitude, latitude)
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong1">
          Point(latitude, longitude)
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong2">
          Point([longitude, latitude])
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong3">
          Point(x=longitude, y=latitude)
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 12 -->
    <div class="question-block">
      <h3>12. What is the purpose of rioxarray in climate data processing?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q12" value="wrong1">
          To create vector geometries
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="correct">
          To add geospatial raster capabilities to xarray
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong2">
          To convert NetCDF to shapefile
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong3">
          To visualize climate data
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 13 -->
    <div class="question-block">
      <h3>13. Which library is commonly used to mask NetCDF data with shapefiles in climate science?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q13" value="wrong1">
          Shapely
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="correct">
          Salem
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong2">
          Cartopy
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong3">
          Rasterio
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 14 -->
    <div class="question-block">
      <h3>14. What does the .plot() method do on a GeoDataFrame?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q14" value="wrong1">
          Creates a time series plot
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="correct">
          Creates a map visualization of the geometries
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong2">
          Exports the data to a file
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong3">
          Prints summary statistics
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 15 -->
    <div class="question-block">
      <h3>15. When performing distance calculations or buffers, why is it important to use a projected CRS?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q15" value="wrong1">
          Projected CRS looks better on maps
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="correct">
          Geographic CRS (lat/lon) uses degrees, not meters, leading to inaccurate distances
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong2">
          Projected CRS is faster to compute
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong3">
          It's not important, any CRS works the same
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 16 -->
    <div class="question-block">
      <h3>16. What does the box() function from Shapely create?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q16" value="wrong1">
          A 3D cube geometry
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="correct">
          A rectangular polygon from min/max coordinates
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong2">
          A boxplot visualization
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong3">
          A bounding box without geometry
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 17 -->
    <div class="question-block">
      <h3>17. Which operations can be performed with GeoPandas? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct1">
          Spatial aggregation
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct2">
          Calculate area and centroid
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct3">
          Check if geometries intersect
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="wrong1">
          Time series forecasting
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 18 -->
    <div class="question-block">
      <h3>18. How can you extract climate data at specific point locations from a NetCDF file?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q18" value="wrong1">
          Use gdf.plot()
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="correct">
          Use xarray's .sel() with latitude/longitude coordinates
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong2">
          Use GeoPandas overlay()
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong3">
          NetCDF files cannot be used with point data
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 19 -->
    <div class="question-block">
      <h3>19. What is the purpose of the bounds attribute in a GeoDataFrame?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q19" value="wrong1">
          Sets the plot limits
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="correct">
          Returns the min/max coordinates (minx, miny, maxx, maxy) of geometries
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong2">
          Defines the CRS boundaries
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong3">
          Clips geometries to a boundary
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 20 -->
    <div class="question-block">
      <h3>20. Which combination of libraries is commonly used together for climate data visualization with maps?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q20" value="wrong1">
          GeoPandas + Pandas
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="correct">
          GeoPandas + Cartopy + Xarray
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong2">
          GeoPandas + TensorFlow
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong3">
          GeoPandas + Django
        </label>
      </div>
      <div class="feedback"></div>
    </div>

  </form>

  <div class="quiz-controls">
    <button id="submit-btn" class="btn btn-primary">Submit Quiz</button>
    <button id="reset-btn" class="btn btn-secondary">Reset</button>
  </div>

  <div id="quiz-results">
    <h2>Quiz Results</h2>
    <div class="score-display" id="score-display"></div>
    <p id="result-message"></p>
    <div class="quiz-controls">
      <button id="review-btn" class="btn btn-primary">Review Answers</button>
      <button id="retake-btn" class="btn btn-secondary">Retake Quiz</button>
    </div>
  </div>

</div>

<script>
(function() {
  const quizForm = document.getElementById('geopandas-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>GeoDataFrame has a geometry column and CRS metadata</strong> is correct! This is the key difference that enables spatial operations.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>Shapely</strong> is correct! Shapely provides geometric objects (Point, LineString, Polygon) used in GeoPandas.'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ <strong>Coordinate Reference System</strong> is correct! CRS defines how coordinates relate to locations on Earth.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>gdf.to_crs()</strong> is correct! This method reprojects geometries to a different coordinate reference system.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>EPSG:4326</strong> is correct! This is the WGS84 geographic coordinate system commonly used for latitude/longitude.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>buffer()</strong> is correct! Buffer creates a zone around geometries at a specified distance (useful for proximity analysis).'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>Combines geometries based on an attribute</strong> is correct! Dissolve is like a spatial groupby that merges geometries.'
    },
    q8: {
      correct: ['correct1', 'correct2'],
      feedback: '✅ <strong>sjoin() and sjoin_nearest()</strong> are correct! These methods perform spatial joins based on location relationships.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>To perform spatial set operations</strong> is correct! Overlay performs union, intersection, difference, or symmetric_difference.'
    },
    q10: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Shapefile, GeoJSON, and GeoPackage</strong> are all correct! GeoPandas supports many vector formats through GDAL/Fiona.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>Point(longitude, latitude)</strong> is correct! Note: Shapely uses (x, y) order which is (lon, lat) for geographic coordinates.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ <strong>To add geospatial raster capabilities to xarray</strong> is correct! Rioxarray enables CRS-aware operations on xarray datasets.'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ <strong>Salem</strong> is correct! Salem provides tools for masking and subsetting climate data using shapefiles.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>Creates a map visualization of the geometries</strong> is correct! GeoDataFrame.plot() creates spatial maps using matplotlib.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>Geographic CRS uses degrees, not meters</strong> is correct! Use projected CRS (like UTM) for accurate distance calculations.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>A rectangular polygon from min/max coordinates</strong> is correct! box(minx, miny, maxx, maxy) creates a bounding box.'
    },
    q17: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Spatial aggregation, area/centroid calculation, and intersection checks</strong> are all correct! GeoPandas supports many spatial operations.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ <strong>Use xarray\'s .sel() with coordinates</strong> is correct! You can select data at specific lat/lon points from NetCDF files.'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ <strong>Returns the min/max coordinates</strong> is correct! bounds gives (minx, miny, maxx, maxy) for each geometry.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>GeoPandas + Cartopy + Xarray</strong> is correct! This combination enables professional climate data mapping and visualization.'
    }
  };

  submitBtn.addEventListener('click', function() {
    let score = 0;
    let total = Object.keys(answers).length;
    
    Object.keys(answers).forEach(function(qId) {
      const questionBlock = document.querySelector(`[name="${qId}"]`).closest('.question-block');
      const feedbackDiv = questionBlock.querySelector('.feedback');
      const answer = answers[qId];
      
      let isCorrect = false;
      
      if (Array.isArray(answer.correct)) {
        // Multiple selection question
        const selected = Array.from(document.querySelectorAll(`[name="${qId}"]:checked`))
          .map(cb => cb.value)
          .sort();
        const correct = answer.correct.sort();
        isCorrect = JSON.stringify(selected) === JSON.stringify(correct);
      } else {
        // Single selection question
        const selected = document.querySelector(`[name="${qId}"]:checked`);
        isCorrect = selected && selected.value === answer.correct;
      }
      
      if (isCorrect) {
        score++;
        feedbackDiv.className = 'feedback correct';
        feedbackDiv.innerHTML = answer.feedback;
      } else {
        feedbackDiv.className = 'feedback incorrect';
        feedbackDiv.innerHTML = '❌ ' + answer.feedback;
      }
      
      feedbackDiv.style.display = 'block';
    });
    
    displayResults(score, total);
  });

  function displayResults(score, total) {
    const percentage = (score / total) * 100;
    const scoreDisplay = document.getElementById('score-display');
    const resultMessage = document.getElementById('result-message');
    
    scoreDisplay.textContent = `${score} / ${total} (${percentage.toFixed(0)}%)`;
    
    if (percentage >= 90) {
      resultMessage.textContent = '🎉 Outstanding! You have mastered GeoPandas and geospatial data handling!';
    } else if (percentage >= 75) {
      resultMessage.textContent = '👍 Great work! You have a solid understanding of GeoPandas.';
    } else if (percentage >= 60) {
      resultMessage.textContent = '✅ Good effort! Review the material and try again to improve.';
    } else {
      resultMessage.textContent = '📚 Keep practicing! Review the tutorial and work through the examples.';
    }
    
    resultsSection.style.display = 'block';
    submitBtn.style.display = 'none';
    window.scrollTo({top: resultsSection.offsetTop - 100, behavior: 'smooth'});
  }

  reviewBtn.addEventListener('click', function() {
    resultsSection.style.display = 'none';
    submitBtn.style.display = 'inline-block';
    window.scrollTo({top: 0, behavior: 'smooth'});
  });

  function resetQuiz() {
    quizForm.reset();
    document.querySelectorAll('.feedback').forEach(function(feedback) {
      feedback.style.display = 'none';
    });
    resultsSection.style.display = 'none';
    submitBtn.style.display = 'inline-block';
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  resetBtn.addEventListener('click', resetQuiz);
  retakeBtn.addEventListener('click', resetQuiz);
})();
</script>


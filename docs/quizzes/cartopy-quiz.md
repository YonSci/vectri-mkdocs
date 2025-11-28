# Cartopy Quiz

Test your understanding of Cartopy, map projections, and climate data visualization!

---

<style>
  .quiz-container {
    max-width: 900px;
    margin: 2rem auto;
    font-family: 'Roboto', sans-serif;
  }
  
  .question-block {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
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
    border-color: #4facfe;
    background-color: #f0f9ff;
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
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
  }
  
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(79, 172, 254, 0.4);
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
    color: #4facfe;
    margin-bottom: 1rem;
  }
  
  .score-display {
    font-size: 2.5rem;
    font-weight: bold;
    color: #00f2fe;
    margin: 1rem 0;
  }
  
  .note {
    background-color: #e3f2fd;
    border-left: 4px solid #4facfe;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
  }
</style>

<div class="quiz-container">
  <div class="note">
    <strong>📝 Note:</strong> This quiz contains 20 questions including multiple choice and multiple selection questions. Some questions may have more than one correct answer. Select all that apply for those questions.
  </div>

  <form id="cartopy-quiz">
    
    <!-- Question 1 -->
    <div class="question-block">
      <h3>1. What is the primary purpose of Cartopy?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q1" value="wrong1">
          To create statistical plots
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="correct">
          To create maps and perform geospatial data visualization with map projections
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong2">
          To process raster data
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong3">
          To handle vector geometries
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 2 -->
    <div class="question-block">
      <h3>2. What does the projection parameter specify when creating a map with Cartopy?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q2" value="wrong1">
          The coordinate system of the data
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="correct">
          The coordinate system used to display the map (axes)
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong2">
          The data source location
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong3">
          The resolution of the map
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 3 -->
    <div class="question-block">
      <h3>3. What does the transform parameter specify when plotting data on a Cartopy map?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q3" value="wrong1">
          How to display the map
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="correct">
          The coordinate system of the input data
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="wrong2">
          The map scale
        </label>
        <label class="option-label">
          <input type="radio" name="q3" value="wrong3">
          The color transformation
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 4 -->
    <div class="question-block">
      <h3>4. Which Cartopy projection represents latitude/longitude as a simple rectangular grid?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q4" value="wrong1">
          ccrs.Robinson()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="correct">
          ccrs.PlateCarree()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong2">
          ccrs.Mercator()
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong3">
          ccrs.Orthographic()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 5 -->
    <div class="question-block">
      <h3>5. Which projection shows the Earth as it appears from space (a globe view)?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q5" value="wrong1">
          ccrs.PlateCarree()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="correct">
          ccrs.Orthographic()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong2">
          ccrs.Robinson()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong3">
          ccrs.LambertConformal()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 6 -->
    <div class="question-block">
      <h3>6. Which projection is commonly used for mid-latitude regions and weather maps?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q6" value="wrong1">
          ccrs.Orthographic()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="correct">
          ccrs.LambertConformal()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong2">
          ccrs.PlateCarree()
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong3">
          ccrs.Stereographic()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 7 -->
    <div class="question-block">
      <h3>7. What does the set_extent() method do?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q7" value="wrong1">
          Sets the figure size
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="correct">
          Defines the geographic bounds (min/max lon, min/max lat) of the map view
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong2">
          Changes the projection
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong3">
          Sets the color range
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 8 -->
    <div class="question-block">
      <h3>8. Which Cartopy features can be added to maps? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q8" value="correct1">
          Coastlines
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="correct2">
          Borders
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="correct3">
          Land and ocean
        </label>
        <label class="option-label">
          <input type="checkbox" name="q8" value="wrong1">
          3D terrain
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 9 -->
    <div class="question-block">
      <h3>9. What is Natural Earth in the context of Cartopy?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q9" value="wrong1">
          A color scheme for maps
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="correct">
          A public domain map dataset with physical and cultural features
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong2">
          A map projection
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong3">
          A Python library for maps
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 10 -->
    <div class="question-block">
      <h3>10. How do you add coastlines to a Cartopy map?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q10" value="wrong1">
          ax.add_coastlines()
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="correct">
          ax.coastlines()
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="wrong2">
          ax.plot_coastlines()
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="wrong3">
          ax.draw_coastlines()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 11 -->
    <div class="question-block">
      <h3>11. What parameter controls the detail level of Natural Earth features (e.g., '110m', '50m', '10m')?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q11" value="wrong1">
          scale
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="correct">
          resolution
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong2">
          quality
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong3">
          detail
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 12 -->
    <div class="question-block">
      <h3>12. What does ax.gridlines() add to a map?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q12" value="wrong1">
          A data grid
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="correct">
          Latitude/longitude grid lines and optionally labels
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong2">
          A coordinate system
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong3">
          A plotting grid for subplots
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 13 -->
    <div class="question-block">
      <h3>13. Which module provides access to Natural Earth shapefiles in Cartopy?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q13" value="wrong1">
          cartopy.data
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="correct">
          cartopy.io.shapereader
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong2">
          cartopy.shapefile
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong3">
          cartopy.features
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 14 -->
    <div class="question-block">
      <h3>14. When plotting climate data in lat/lon coordinates on a map, what should the transform parameter be?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q14" value="wrong1">
          The same as the projection
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="correct">
          ccrs.PlateCarree() (since data is in lat/lon)
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong2">
          ccrs.Mercator()
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong3">
          No transform needed
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 15 -->
    <div class="question-block">
      <h3>15. What is the purpose of the add_feature() method?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q15" value="wrong1">
          To add data to the map
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="correct">
          To add cartographic features (land, ocean, borders, etc.) to the map
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong2">
          To add a colorbar
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong3">
          To add a legend
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 16 -->
    <div class="question-block">
      <h3>16. Which Cartopy classes are used for formatting gridline labels? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q16" value="correct1">
          LongitudeFormatter
        </label>
        <label class="option-label">
          <input type="checkbox" name="q16" value="correct2">
          LatitudeFormatter
        </label>
        <label class="option-label">
          <input type="checkbox" name="q16" value="wrong1">
          CoordinateFormatter
        </label>
        <label class="option-label">
          <input type="checkbox" name="q16" value="wrong2">
          MapFormatter
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 17 -->
    <div class="question-block">
      <h3>17. What is the Robinson projection commonly used for?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q17" value="wrong1">
          Polar regions
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="correct">
          World maps with balanced distortion
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="wrong2">
          Regional weather maps
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="wrong3">
          Navigation charts
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 18 -->
    <div class="question-block">
      <h3>18. How do you create a GeoAxes (map axes) in Matplotlib with Cartopy?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q18" value="wrong1">
          plt.axes(map=True)
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="correct">
          plt.axes(projection=ccrs.SomeProjection())
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong2">
          plt.geoaxes()
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong3">
          plt.map()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 19 -->
    <div class="question-block">
      <h3>19. What advantages does Cartopy offer for climate scientists? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q19" value="correct1">
          Proper handling of map projections
        </label>
        <label class="option-label">
          <input type="checkbox" name="q19" value="correct2">
          Integration with Matplotlib
        </label>
        <label class="option-label">
          <input type="checkbox" name="q19" value="correct3">
          Built-in cartographic features (coastlines, borders)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q19" value="wrong1">
          Machine learning capabilities
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 20 -->
    <div class="question-block">
      <h3>20. What happens if you forget to specify the transform parameter when plotting data?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q20" value="wrong1">
          The plot will work correctly
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="correct">
          Cartopy assumes data is in the same CRS as the projection, potentially causing misplacement
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong2">
          An error will be raised
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong3">
          The data will not be plotted
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
  const quizForm = document.getElementById('cartopy-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>To create maps with map projections</strong> is correct! Cartopy specializes in geospatial visualization and cartographic projections.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>The coordinate system for displaying the map</strong> is correct! The projection parameter defines how the axes/map appears.'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ <strong>The coordinate system of the input data</strong> is correct! Transform tells Cartopy how to interpret your data coordinates.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>ccrs.PlateCarree()</strong> is correct! Plate Carrée is an equirectangular projection where lon/lat form a rectangular grid.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>ccrs.Orthographic()</strong> is correct! Orthographic projection shows Earth as viewed from space (globe perspective).'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>ccrs.LambertConformal()</strong> is correct! Lambert Conformal Conic is ideal for mid-latitude regions and weather maps.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>Defines the geographic bounds of the map view</strong> is correct! set_extent([lon_min, lon_max, lat_min, lat_max]) zooms to a region.'
    },
    q8: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Coastlines, borders, land and ocean</strong> are all correct! Cartopy provides these Natural Earth features.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>A public domain map dataset</strong> is correct! Natural Earth provides free vector and raster map data at multiple resolutions.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ <strong>ax.coastlines()</strong> is correct! This method adds coastline features to the map.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>resolution</strong> is correct! Common values are "110m" (coarse), "50m" (medium), "10m" (fine).'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ <strong>Latitude/longitude grid lines</strong> is correct! Gridlines help read coordinates and orient the map.'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ <strong>cartopy.io.shapereader</strong> is correct! This module provides access to Natural Earth shapefiles.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>ccrs.PlateCarree()</strong> is correct! Lat/lon data is in the PlateCarree (equirectangular) coordinate system.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>To add cartographic features</strong> is correct! add_feature() adds physical/cultural features like cfeature.LAND, cfeature.OCEAN.'
    },
    q16: {
      correct: ['correct1', 'correct2'],
      feedback: '✅ <strong>LongitudeFormatter and LatitudeFormatter</strong> are correct! These format gridline labels with proper degree symbols and directions.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ <strong>World maps with balanced distortion</strong> is correct! Robinson projection is a compromise projection good for global views.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ <strong>plt.axes(projection=ccrs.SomeProjection())</strong> is correct! The projection parameter creates a GeoAxes object.'
    },
    q19: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Projection handling, Matplotlib integration, and cartographic features</strong> are all correct! These make Cartopy ideal for climate visualization.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>Cartopy assumes data is in the same CRS as projection</strong> is correct! Always specify transform to avoid misplaced data.'
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
      resultMessage.textContent = '🎉 Excellent! You have mastered Cartopy and map projections!';
    } else if (percentage >= 75) {
      resultMessage.textContent = '👍 Great work! You have a solid understanding of Cartopy.';
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


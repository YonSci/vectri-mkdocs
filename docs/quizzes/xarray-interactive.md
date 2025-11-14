# Xarray Interactive Quiz

Test your Xarray knowledge with this interactive quiz! Select your answers and get instant scoring.

---

<div id="quiz-container">
  <div class="quiz-header">
    <h2>📋 Assessment Guidelines</h2>
    <div class="guidelines-grid">
      <div class="guideline-card">
        <strong>📝 Interactive Format</strong>
        <p>Select answers by clicking radio buttons or checkboxes</p>
      </div>
      <div class="guideline-card">
        <strong>✅ Instant Scoring</strong>
        <p>Submit to see your score and detailed feedback</p>
      </div>
      <div class="guideline-card">
        <strong>🔄 Retake Anytime</strong>
        <p>Reset and try again to improve your score</p>
      </div>
    </div>
  </div>

  <form id="xarray-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Data Structure</h3>
      <p>What is the primary data structure in Xarray for working with multi-dimensional labeled arrays?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> DataFrame</label>
        <label><input type="radio" name="q1" value="correct"> DataArray</label>
        <label><input type="radio" name="q1" value="wrong2"> Series</label>
        <label><input type="radio" name="q1" value="wrong3"> Matrix</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Opening NetCDF Files</h3>
      <p>Which Xarray function is used to open a NetCDF file?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> xr.read_netcdf()</label>
        <label><input type="radio" name="q2" value="correct"> xr.open_dataset()</label>
        <label><input type="radio" name="q2" value="wrong2"> xr.load_netcdf()</label>
        <label><input type="radio" name="q2" value="wrong3"> xr.open_file()</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: Selecting Data</h3>
      <p>How do you select data for a specific time period in Xarray?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q3" value="wrong1"> ds.filter(time='2020')</label>
        <label><input type="radio" name="q3" value="wrong2"> ds.query(time='2020')</label>
        <label><input type="radio" name="q3" value="correct"> ds.sel(time='2020')</label>
        <label><input type="radio" name="q3" value="wrong3"> ds.select(time='2020')</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: Aggregation Operations</h3>
      <p>Which method calculates the mean temperature across all time steps?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> ds.temperature.average(dim='time')</label>
        <label><input type="radio" name="q4" value="correct"> ds.temperature.mean(dim='time')</label>
        <label><input type="radio" name="q4" value="wrong2"> ds.temperature.avg(axis='time')</label>
        <label><input type="radio" name="q4" value="wrong3"> ds.temperature.reduce_mean('time')</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: Multiple Select</h3>
      <p><strong>Select ALL</strong> valid Xarray aggregation methods:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q5" value="correct1"> mean()</label>
        <label><input type="checkbox" name="q5" value="correct2"> sum()</label>
        <label><input type="checkbox" name="q5" value="wrong1"> average()</label>
        <label><input type="checkbox" name="q5" value="correct3"> std()</label>
        <label><input type="checkbox" name="q5" value="correct4"> median()</label>
        <label><input type="checkbox" name="q5" value="wrong2"> avg()</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: True or False</h3>
      <p>Xarray automatically aligns data based on coordinate labels when performing operations.</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="correct"> True</label>
        <label><input type="radio" name="q6" value="wrong"> False</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Masking Data</h3>
      <p>How do you mask temperature values below 0°C in Xarray?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> ds.temperature.filter(lambda x: x >= 0)</label>
        <label><input type="radio" name="q7" value="wrong2"> ds.temperature.mask(ds.temperature < 0)</label>
        <label><input type="radio" name="q7" value="correct"> ds.temperature.where(ds.temperature >= 0)</label>
        <label><input type="radio" name="q7" value="wrong3"> ds.temperature.query('temperature >= 0')</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Multiple Files</h3>
      <p>Which function opens multiple NetCDF files at once?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> xr.open_multiple()</label>
        <label><input type="radio" name="q8" value="wrong2"> xr.concat_datasets()</label>
        <label><input type="radio" name="q8" value="correct"> xr.open_mfdataset()</label>
        <label><input type="radio" name="q8" value="wrong3"> xr.merge_files()</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Interpolation</h3>
      <p>How do you interpolate data to new coordinates in Xarray?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> ds.regrid(new_coords)</label>
        <label><input type="radio" name="q9" value="correct"> ds.interp(lat=new_lats, lon=new_lons)</label>
        <label><input type="radio" name="q9" value="wrong2"> ds.resample(lat=new_lats, lon=new_lons)</label>
        <label><input type="radio" name="q9" value="wrong3"> ds.interpolate(coords={'lat': new_lats})</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Saving Data</h3>
      <p>What's the correct way to save an Xarray Dataset to NetCDF?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q10" value="wrong1"> ds.save('output.nc')</label>
        <label><input type="radio" name="q10" value="wrong2"> ds.write_netcdf('output.nc')</label>
        <label><input type="radio" name="q10" value="correct"> ds.to_netcdf('output.nc')</label>
        <label><input type="radio" name="q10" value="wrong3"> ds.export('output.nc')</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <div class="quiz-actions">
      <button type="button" id="submit-btn" class="btn-submit">Submit Quiz</button>
      <button type="button" id="reset-btn" class="btn-reset">Reset Quiz</button>
    </div>

  </form>

  <!-- Results Section -->
  <div id="quiz-results" class="quiz-results" style="display: none;">
    <h2>📊 Quiz Results</h2>
    <div class="results-grid">
      <div class="result-card">
        <div class="result-value" id="score-value">0/10</div>
        <div class="result-label">Your Score</div>
      </div>
      <div class="result-card">
        <div class="result-value" id="percentage-value">0%</div>
        <div class="result-label">Percentage</div>
      </div>
      <div class="result-card">
        <div class="result-value" id="grade-value">-</div>
        <div class="result-label">Grade</div>
      </div>
    </div>
    <div class="performance-message" id="performance-message"></div>
    <div class="results-actions">
      <button type="button" id="review-btn" class="btn-review">Review Answers</button>
      <button type="button" id="retake-btn" class="btn-retake">Retake Quiz</button>
    </div>
  </div>
</div>

<!-- Quiz JavaScript -->
<script>
(function() {
  const quizForm = document.getElementById('xarray-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>DataArray</strong> is correct! It\'s the primary structure for multi-dimensional labeled arrays in Xarray.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>xr.open_dataset()</strong> is correct! This is the standard function to open NetCDF files.'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ <strong>ds.sel()</strong> is correct! Use sel() for label-based indexing in Xarray.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>ds.temperature.mean(dim="time")</strong> is correct! mean() calculates the average along specified dimensions.'
    },
    q5: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>mean(), sum(), std(), median()</strong> are all valid. average() and avg() are not standard Xarray methods.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>True</strong> is correct! Xarray automatically aligns data based on coordinate labels - a powerful feature!'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>where()</strong> is correct! It keeps values where the condition is True and replaces others with NaN.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ <strong>xr.open_mfdataset()</strong> is correct! mf stands for "multi-file dataset".'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>interp()</strong> is correct! It performs interpolation to new coordinate values.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ <strong>to_netcdf()</strong> is correct! This writes the dataset to a NetCDF file.'
    }
  };

  // Submit quiz
  submitBtn.addEventListener('click', function() {
    let score = 0;
    let totalQuestions = 10;
    
    // Check each question
    for (let i = 1; i <= totalQuestions; i++) {
      const qName = 'q' + i;
      const feedback = document.getElementById('feedback-' + qName);
      
      if (qName === 'q5') {
        // Multiple select question
        const selected = Array.from(document.querySelectorAll('input[name="' + qName + '"]:checked'))
          .map(input => input.value);
        const correct = answers[qName].correct;
        
        const isCorrect = selected.length === correct.length && 
          selected.every(val => correct.includes(val)) &&
          correct.every(val => selected.includes(val));
        
        if (isCorrect) {
          score++;
          feedback.innerHTML = '<div class="feedback-correct">' + answers[qName].feedback + '</div>';
        } else {
          feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. The correct answers are: mean(), sum(), std(), median()</div>';
        }
      } else {
        // Single select question
        const selected = document.querySelector('input[name="' + qName + '"]:checked');
        if (selected) {
          if (selected.value === answers[qName].correct) {
            score++;
            feedback.innerHTML = '<div class="feedback-correct">' + answers[qName].feedback + '</div>';
          } else {
            feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. ' + answers[qName].feedback.replace('✅', '') + '</div>';
          }
        } else {
          feedback.innerHTML = '<div class="feedback-wrong">❌ No answer selected.</div>';
        }
      }
    }
    
    // Display results
    displayResults(score, totalQuestions);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  });

  // Display results
  function displayResults(score, total) {
    const percentage = Math.round((score / total) * 100);
    let grade, message, color;
    
    if (percentage >= 90) {
      grade = 'A (Excellent)';
      message = '🎉 Outstanding! You have a strong understanding of Xarray. You\'re ready for the workshop labs!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid foundation. Review the questions you missed and you\'ll be all set.';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep practicing! Review the Xarray documentation and retake the quiz.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Review the basics and try again. Don\'t worry - practice makes perfect!';
      color = '#ff9800';
    }
    
    document.getElementById('score-value').textContent = score + '/' + total;
    document.getElementById('percentage-value').textContent = percentage + '%';
    document.getElementById('grade-value').textContent = grade;
    document.getElementById('grade-value').style.color = color;
    document.getElementById('performance-message').innerHTML = '<p style="font-size: 1.1rem; padding: 1rem; background: ' + color + '22; border-left: 4px solid ' + color + '; border-radius: 4px;">' + message + '</p>';
    
    resultsSection.style.display = 'block';
    submitBtn.style.display = 'none';
  }

  // Review answers
  reviewBtn.addEventListener('click', function() {
    quizForm.scrollIntoView({ behavior: 'smooth' });
  });

  // Reset quiz
  function resetQuiz() {
    quizForm.reset();
    resultsSection.style.display = 'none';
    submitBtn.style.display = 'inline-block';
    
    // Clear all feedback
    document.querySelectorAll('.feedback').forEach(feedback => {
      feedback.innerHTML = '';
    });
    
    // Scroll to top
    document.getElementById('quiz-container').scrollIntoView({ behavior: 'smooth' });
  }

  resetBtn.addEventListener('click', resetQuiz);
  retakeBtn.addEventListener('click', resetQuiz);
})();
</script>

<!-- Quiz Styles -->
<style>
.quiz-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.quiz-header h2 {
  margin-top: 0;
  color: white !important;
}

.guidelines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.guideline-card {
  background: rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.guideline-card strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.guideline-card p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.95;
}

.quiz-question {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-left: 4px solid #3f51b5;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #c5cae9;
}

.quiz-question h3 {
  color: #3f51b5;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-question h3 {
  color: #c5cae9;
}

.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.quiz-options label {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quiz-options label:hover {
  background: #f5f5f5;
  border-color: #3f51b5;
}

[data-md-color-scheme="slate"] .quiz-options label {
  border-color: #455a64;
}

[data-md-color-scheme="slate"] .quiz-options label:hover {
  background: #37474f;
  border-color: #c5cae9;
}

.quiz-options input[type="radio"],
.quiz-options input[type="checkbox"] {
  margin-right: 0.75rem;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.feedback {
  margin-top: 1rem;
  min-height: 20px;
}

.feedback-correct {
  padding: 1rem;
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  border-radius: 4px;
  color: #2e7d32;
}

[data-md-color-scheme="slate"] .feedback-correct {
  background: #1b5e20;
  color: #a5d6a7;
}

.feedback-wrong {
  padding: 1rem;
  background: #ffebee;
  border-left: 4px solid #f44336;
  border-radius: 4px;
  color: #c62828;
}

[data-md-color-scheme="slate"] .feedback-wrong {
  background: #b71c1c;
  color: #ef9a9a;
}

.quiz-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
}

.btn-submit,
.btn-reset,
.btn-review,
.btn-retake {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit {
  background: #4caf50;
  color: white;
}

.btn-submit:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-reset,
.btn-retake {
  background: #ff9800;
  color: white;
}

.btn-reset:hover,
.btn-retake:hover {
  background: #f57c00;
  transform: translateY(-2px);
}

.btn-review {
  background: #2196f3;
  color: white;
}

.btn-review:hover {
  background: #1976d2;
  transform: translateY(-2px);
}

.quiz-results {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
  border-radius: 12px;
  margin-top: 2rem;
}

[data-md-color-scheme="slate"] .quiz-results {
  background: linear-gradient(135deg, #263238 0%, #37474f 100%);
}

.quiz-results h2 {
  text-align: center;
  color: #3f51b5;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-results h2 {
  color: #c5cae9;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.result-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

[data-md-color-scheme="slate"] .result-card {
  background: #1a1f24;
}

.result-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #3f51b5;
}

.result-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

[data-md-color-scheme="slate"] .result-label {
  color: #b0b0b0;
}

.performance-message {
  margin: 2rem 0;
}

.results-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

@media screen and (max-width: 768px) {
  .quiz-actions,
  .results-actions {
    flex-direction: column;
  }
  
  .btn-submit,
  .btn-reset,
  .btn-review,
  .btn-retake {
    width: 100%;
  }
}
</style>

---

## 💡 Tips for Success

- Read each question carefully
- Don't rush - take your time
- For multiple select questions, select ALL correct answers
- Review your answers before submitting
- Check the feedback to understand concepts better
- Retake the quiz to improve your score!

---

## 📚 Additional Resources

- [Xarray Documentation](https://docs.xarray.dev/)
- [Xarray Tutorial](https://tutorial.xarray.dev/)
- Workshop Lab Exercises (Day 2 & 3)


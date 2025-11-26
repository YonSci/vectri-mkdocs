# Pandas for Climate Scientists Interactive Quiz

Test your Pandas knowledge for climate data analysis with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="pandas-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Data Structures</h3>
      <p>What are the two main data structures in Pandas?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> Array and Matrix</label>
        <label><input type="radio" name="q1" value="correct"> Series and DataFrame</label>
        <label><input type="radio" name="q1" value="wrong2"> List and Dictionary</label>
        <label><input type="radio" name="q1" value="wrong3"> Table and Column</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Series Definition</h3>
      <p>A Pandas Series is best described as:</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> A two-dimensional table</label>
        <label><input type="radio" name="q2" value="correct"> A one-dimensional labeled array</label>
        <label><input type="radio" name="q2" value="wrong2"> A three-dimensional array</label>
        <label><input type="radio" name="q2" value="wrong3"> A dictionary-like structure</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: DataFrame Structure</h3>
      <p>A Pandas DataFrame is:</p>
      <div class="quiz-options">
        <label><input type="radio" name="q3" value="wrong1"> A one-dimensional array</label>
        <label><input type="radio" name="q3" value="correct"> A two-dimensional table-like data structure</label>
        <label><input type="radio" name="q3" value="wrong2"> A NumPy array wrapper</label>
        <label><input type="radio" name="q3" value="wrong3"> A Python list of lists</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: Viewing Data - Multiple Select</h3>
      <p><strong>Select ALL</strong> methods that can view the first few rows of a DataFrame:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q4" value="correct1"> df.head()</label>
        <label><input type="checkbox" name="q4" value="wrong1"> df.first()</label>
        <label><input type="checkbox" name="q4" value="wrong2"> df.top()</label>
        <label><input type="checkbox" name="q4" value="correct2"> df.head(10)</label>
        <label><input type="checkbox" name="q4" value="wrong3"> df.show()</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: DataFrame Information</h3>
      <p>Which method displays information about a DataFrame including data types and non-null counts?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q5" value="wrong1"> df.describe()</label>
        <label><input type="radio" name="q5" value="correct"> df.info()</label>
        <label><input type="radio" name="q5" value="wrong2"> df.summary()</label>
        <label><input type="radio" name="q5" value="wrong3"> df.details()</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: Statistical Summary</h3>
      <p>Which method provides statistical summary (count, mean, std, min, max, etc.) of numeric columns?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> df.stats()</label>
        <label><input type="radio" name="q6" value="correct"> df.describe()</label>
        <label><input type="radio" name="q6" value="wrong2"> df.summary()</label>
        <label><input type="radio" name="q6" value="wrong3"> df.statistics()</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Accessing Columns</h3>
      <p>How do you select a single column 'temperature' from a DataFrame df?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> df.get('temperature')</label>
        <label><input type="radio" name="q7" value="correct"> df['temperature'] or df.temperature</label>
        <label><input type="radio" name="q7" value="wrong2"> df.select('temperature')</label>
        <label><input type="radio" name="q7" value="wrong3"> df.column('temperature')</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Adding Columns</h3>
      <p>How do you add a new column 'temp_f' to convert Celsius to Fahrenheit?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> df.add_column('temp_f', df['temp_c'] * 9/5 + 32)</label>
        <label><input type="radio" name="q8" value="correct"> df['temp_f'] = df['temp_c'] * 9/5 + 32</label>
        <label><input type="radio" name="q8" value="wrong2"> df.insert('temp_f', df['temp_c'] * 9/5 + 32)</label>
        <label><input type="radio" name="q8" value="wrong3"> df.new_column('temp_f', df['temp_c'] * 9/5 + 32)</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Dropping Columns</h3>
      <p>Which parameter must you use with drop() to remove columns (not rows)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> axis=0</label>
        <label><input type="radio" name="q9" value="correct"> axis=1</label>
        <label><input type="radio" name="q9" value="wrong2"> columns=True</label>
        <label><input type="radio" name="q9" value="wrong3"> direction='column'</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Reading Files - Multiple Select</h3>
      <p><strong>Select ALL</strong> valid Pandas functions for reading files:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q10" value="correct1"> pd.read_csv()</label>
        <label><input type="checkbox" name="q10" value="correct2"> pd.read_excel()</label>
        <label><input type="checkbox" name="q10" value="correct3"> pd.read_json()</label>
        <label><input type="checkbox" name="q10" value="wrong1"> pd.read_txt()</label>
        <label><input type="checkbox" name="q10" value="wrong2"> pd.load_csv()</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 -->
    <div class="quiz-question">
      <h3>Question 11: Writing Files</h3>
      <p>Which method saves a DataFrame to a CSV file?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q11" value="wrong1"> df.save_csv()</label>
        <label><input type="radio" name="q11" value="correct"> df.to_csv()</label>
        <label><input type="radio" name="q11" value="wrong2"> df.write_csv()</label>
        <label><input type="radio" name="q11" value="wrong3"> df.export_csv()</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 -->
    <div class="quiz-question">
      <h3>Question 12: Filtering Data</h3>
      <p>How do you filter rows where temperature is greater than 30?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q12" value="wrong1"> df.filter(df['temperature'] > 30)</label>
        <label><input type="radio" name="q12" value="correct"> df[df['temperature'] > 30]</label>
        <label><input type="radio" name="q12" value="wrong2"> df.where(df['temperature'] > 30)</label>
        <label><input type="radio" name="q12" value="wrong3"> df.select(df['temperature'] > 30)</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 -->
    <div class="quiz-question">
      <h3>Question 13: Sorting Data</h3>
      <p>Which method sorts a DataFrame by a column?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q13" value="wrong1"> df.sort()</label>
        <label><input type="radio" name="q13" value="correct"> df.sort_values()</label>
        <label><input type="radio" name="q13" value="wrong2"> df.order_by()</label>
        <label><input type="radio" name="q13" value="wrong3"> df.arrange()</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 -->
    <div class="quiz-question">
      <h3>Question 14: Aggregation Functions - Multiple Select</h3>
      <p><strong>Select ALL</strong> valid Pandas aggregation methods:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q14" value="correct1"> df.mean()</label>
        <label><input type="checkbox" name="q14" value="correct2"> df.sum()</label>
        <label><input type="checkbox" name="q14" value="correct3"> df.max()</label>
        <label><input type="checkbox" name="q14" value="correct4"> df.std()</label>
        <label><input type="checkbox" name="q14" value="wrong1"> df.average()</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 -->
    <div class="quiz-question">
      <h3>Question 15: GroupBy Operations</h3>
      <p>What does the groupby() method do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q15" value="wrong1"> Sorts data by groups</label>
        <label><input type="radio" name="q15" value="correct"> Groups data and allows aggregation on each group</label>
        <label><input type="radio" name="q15" value="wrong2"> Filters data by groups</label>
        <label><input type="radio" name="q15" value="wrong3"> Renames columns by groups</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 -->
    <div class="quiz-question">
      <h3>Question 16: Handling Missing Data</h3>
      <p>Which method removes rows with any missing values (NaN)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q16" value="wrong1"> df.remove_na()</label>
        <label><input type="radio" name="q16" value="correct"> df.dropna()</label>
        <label><input type="radio" name="q16" value="wrong2"> df.delete_na()</label>
        <label><input type="radio" name="q16" value="wrong3"> df.clean()</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
    </div>

    <!-- Question 17 -->
    <div class="quiz-question">
      <h3>Question 17: Filling Missing Data</h3>
      <p>Which method fills missing values with a specific value?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q17" value="wrong1"> df.replace_na()</label>
        <label><input type="radio" name="q17" value="correct"> df.fillna()</label>
        <label><input type="radio" name="q17" value="wrong2"> df.fill()</label>
        <label><input type="radio" name="q17" value="wrong3"> df.substitute()</label>
      </div>
      <div class="feedback" id="feedback-q17"></div>
    </div>

    <!-- Question 18 -->
    <div class="quiz-question">
      <h3>Question 18: Renaming Columns</h3>
      <p>How do you rename a column 'temp' to 'temperature'?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q18" value="wrong1"> df.change_name('temp', 'temperature')</label>
        <label><input type="radio" name="q18" value="correct"> df.rename(columns={'temp': 'temperature'})</label>
        <label><input type="radio" name="q18" value="wrong2"> df['temp'].name = 'temperature'</label>
        <label><input type="radio" name="q18" value="wrong3"> df.rename_column('temp', 'temperature')</label>
      </div>
      <div class="feedback" id="feedback-q18"></div>
    </div>

    <!-- Question 19 -->
    <div class="quiz-question">
      <h3>Question 19: loc vs iloc</h3>
      <p>What is the main difference between loc and iloc?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q19" value="wrong1"> They are identical</label>
        <label><input type="radio" name="q19" value="correct"> loc uses labels, iloc uses integer positions</label>
        <label><input type="radio" name="q19" value="wrong2"> loc is faster than iloc</label>
        <label><input type="radio" name="q19" value="wrong3"> iloc is for columns, loc is for rows</label>
      </div>
      <div class="feedback" id="feedback-q19"></div>
    </div>

    <!-- Question 20 -->
    <div class="quiz-question">
      <h3>Question 20: True or False</h3>
      <p>Pandas DataFrames can contain columns with different data types (e.g., integers, floats, strings).</p>
      <div class="quiz-options">
        <label><input type="radio" name="q20" value="correct"> True</label>
        <label><input type="radio" name="q20" value="wrong"> False</label>
      </div>
      <div class="feedback" id="feedback-q20"></div>
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
        <div class="result-value" id="score-value">0/20</div>
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
  const quizForm = document.getElementById('pandas-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>Series and DataFrame</strong> is correct! These are the two fundamental data structures in Pandas.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ Correct! A <strong>Series is a one-dimensional labeled array</strong>, like a single column in a spreadsheet.'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ Correct! A <strong>DataFrame is a two-dimensional table</strong>, like a spreadsheet with rows and columns.'
    },
    q4: {
      correct: ['correct1', 'correct2'],
      feedback: '✅ Correct! <strong>df.head()</strong> shows first 5 rows by default, <strong>df.head(10)</strong> shows first 10 rows.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>df.info()</strong> is correct! It displays column names, data types, non-null counts, and memory usage.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>df.describe()</strong> is correct! It provides statistical summary including count, mean, std, min, quartiles, and max.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ Correct! Use <strong>df["temperature"]</strong> or <strong>df.temperature</strong> (dot notation works if column name has no spaces).'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>df["temp_f"] = df["temp_c"] * 9/5 + 32</strong> creates a new column with the conversion formula.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>axis=1</strong> is correct! axis=0 drops rows, axis=1 drops columns. Remember: 0=rows, 1=columns.'
    },
    q10: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! <strong>read_csv(), read_excel(), and read_json()</strong> are all valid. read_txt() doesn\'t exist.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>df.to_csv()</strong> is correct! Most Pandas export methods follow the to_* pattern (to_csv, to_excel, to_json).'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>df[df["temperature"] > 30]</strong> uses boolean indexing to filter rows based on conditions.'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ <strong>df.sort_values()</strong> is correct! Specify the column with by= parameter, e.g., df.sort_values(by="temperature").'
    },
    q14: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>mean(), sum(), max(), and std()</strong> are all aggregation methods. average() is not a Pandas method.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>groupby()</strong> groups data by unique values and allows you to perform aggregations on each group.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>df.dropna()</strong> is correct! It removes rows (or columns with axis=1) containing missing values.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ <strong>df.fillna()</strong> is correct! You can fill with a value, forward fill (ffill), or backward fill (bfill).'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>df.rename(columns={"temp": "temperature"})</strong> renames columns using a dictionary mapping.'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>loc uses label-based indexing</strong> (column/row names), <strong>iloc uses integer position</strong> (0, 1, 2...).'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>True</strong> is correct! Unlike NumPy arrays, DataFrames can have different data types in different columns.'
    }
  };

  // Submit quiz
  submitBtn.addEventListener('click', function() {
    let score = 0;
    let totalQuestions = 20;
    
    // Check each question
    for (let i = 1; i <= totalQuestions; i++) {
      const qName = 'q' + i;
      const feedback = document.getElementById('feedback-' + qName);
      
      if (qName === 'q4' || qName === 'q10' || qName === 'q14') {
        // Multiple select questions
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
          feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. ' + answers[qName].feedback.replace('✅ Correct! ', '') + '</div>';
        }
      } else {
        // Single select question
        const selected = document.querySelector('input[name="' + qName + '"]:checked');
        if (selected) {
          if (selected.value === answers[qName].correct) {
            score++;
            feedback.innerHTML = '<div class="feedback-correct">' + answers[qName].feedback + '</div>';
          } else {
            feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. ' + answers[qName].feedback.replace('✅', '').replace('Correct!', 'The correct answer is:') + '</div>';
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
      message = '🎉 Outstanding! You have excellent Pandas skills for climate data analysis. You\'re ready to work with real weather datasets!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid understanding of Pandas fundamentals. Review the questions you missed and keep practicing!';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep practicing! Work through the Pandas tutorial examples and experiment with DataFrames.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Pandas is essential for climate data analysis. Review the tutorial and practice with small datasets.';
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
  background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
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
  font-size: 1.0rem;
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
  border-left: 4px solid #9c27b0;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #ba68c8;
}

.quiz-question h3 {
  color: #9c27b0;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-question h3 {
  color: #ba68c8;
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
  border-color: #9c27b0;
}

[data-md-color-scheme="slate"] .quiz-options label {
  border-color: #455a64;
}

[data-md-color-scheme="slate"] .quiz-options label:hover {
  background: #37474f;
  border-color: #ba68c8;
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
  color: #9c27b0;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-results h2 {
  color: #ba68c8;
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
  color: #9c27b0;
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

- Think about DataFrame structure and operations
- Remember that axis=0 refers to rows, axis=1 refers to columns
- Understand the difference between loc (labels) and iloc (positions)
- For multiple select questions, select ALL correct answers
- Know common methods for viewing, filtering, and aggregating data
- Practice with real climate datasets to reinforce concepts!

---

## 📚 Additional Resources

- [Pandas Tutorial](../day2/04-Pandas_for_Climate_and_Meteorology_Workshop.md)
- [Official Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Getting Started](https://pandas.pydata.org/getting_started.html)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

---

## 🚀 Key Concepts Covered

This quiz tests your understanding of:

1. **Data Structures** - Series and DataFrame
2. **Viewing Data** - head(), tail(), info(), describe()
3. **Accessing Data** - Column selection, loc, iloc
4. **Adding/Removing** - New columns, dropping columns/rows
5. **File I/O** - read_csv(), to_csv(), read_excel(), read_json()
6. **Filtering** - Boolean indexing for conditional selection
7. **Sorting** - sort_values() method
8. **Aggregations** - mean(), sum(), max(), std()
9. **GroupBy** - Grouping and aggregating data
10. **Missing Data** - dropna(), fillna()
11. **Renaming** - Column renaming with rename()
12. **Data Types** - Heterogeneous columns in DataFrames

---

**Good luck! Pandas is your gateway to analyzing climate time series and station data!** 🐼📊


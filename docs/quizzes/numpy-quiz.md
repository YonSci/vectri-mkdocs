# NumPy for Climate Scientists Interactive Quiz

Test your NumPy knowledge for climate data analysis with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="numpy-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Array Dimensions</h3>
      <p>Which attribute returns the number of dimensions of a NumPy array?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> shape</label>
        <label><input type="radio" name="q1" value="correct"> ndim</label>
        <label><input type="radio" name="q1" value="wrong2"> size</label>
        <label><input type="radio" name="q1" value="wrong3"> dimensions</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Array Shape</h3>
      <p>Given <code>arr = np.array([[1, 2, 3], [4, 5, 6]])</code>, what does <code>arr.shape</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> (6,)</label>
        <label><input type="radio" name="q2" value="correct"> (2, 3)</label>
        <label><input type="radio" name="q2" value="wrong2"> (3, 2)</label>
        <label><input type="radio" name="q2" value="wrong3"> 2</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: Creating Arrays - Multiple Select</h3>
      <p><strong>Select ALL</strong> NumPy functions that create arrays:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q3" value="correct1"> np.array()</label>
        <label><input type="checkbox" name="q3" value="correct2"> np.arange()</label>
        <label><input type="checkbox" name="q3" value="correct3"> np.linspace()</label>
        <label><input type="checkbox" name="q3" value="wrong1"> np.create()</label>
        <label><input type="checkbox" name="q3" value="correct4"> np.zeros()</label>
        <label><input type="checkbox" name="q3" value="correct5"> np.ones()</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: np.arange vs np.linspace</h3>
      <p>What is the main difference between <code>np.arange()</code> and <code>np.linspace()</code>?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> They are identical functions</label>
        <label><input type="radio" name="q4" value="correct"> arange uses step size, linspace uses number of points</label>
        <label><input type="radio" name="q4" value="wrong2"> arange is for floats, linspace is for integers</label>
        <label><input type="radio" name="q4" value="wrong3"> linspace is faster than arange</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: Array Creation</h3>
      <p>Which function creates an identity matrix (diagonal matrix with 1s)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q5" value="wrong1"> np.ones()</label>
        <label><input type="radio" name="q5" value="wrong2"> np.diagonal()</label>
        <label><input type="radio" name="q5" value="correct"> np.eye()</label>
        <label><input type="radio" name="q5" value="wrong3"> np.identity_matrix()</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: Random Numbers</h3>
      <p>Which function generates random numbers from a uniform distribution between 0 and 1?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> np.random.normal()</label>
        <label><input type="radio" name="q6" value="correct"> np.random.rand()</label>
        <label><input type="radio" name="q6" value="wrong2"> np.random.randint()</label>
        <label><input type="radio" name="q6" value="wrong3"> np.random.uniform()</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Array Indexing</h3>
      <p>Given <code>arr = np.array([10, 20, 30, 40, 50])</code>, what does <code>arr[1:4]</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> [10, 20, 30]</label>
        <label><input type="radio" name="q7" value="correct"> [20, 30, 40]</label>
        <label><input type="radio" name="q7" value="wrong2"> [20, 30, 40, 50]</label>
        <label><input type="radio" name="q7" value="wrong3"> [30, 40]</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Boolean Masking</h3>
      <p>What does boolean masking (fancy indexing) allow you to do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> Convert arrays to boolean type</label>
        <label><input type="radio" name="q8" value="correct"> Select array elements based on conditions</label>
        <label><input type="radio" name="q8" value="wrong2"> Hide certain array elements</label>
        <label><input type="radio" name="q8" value="wrong3"> Create masked arrays only</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Broadcasting</h3>
      <p>What is broadcasting in NumPy?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> Sending arrays to multiple computers</label>
        <label><input type="radio" name="q9" value="correct"> Automatic expansion of arrays to match shapes for operations</label>
        <label><input type="radio" name="q9" value="wrong2"> Converting arrays to larger data types</label>
        <label><input type="radio" name="q9" value="wrong3"> Sharing arrays across processes</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Vectorization Benefits - Multiple Select</h3>
      <p><strong>Select ALL</strong> advantages of vectorization with NumPy:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q10" value="correct1"> Faster execution than Python loops</label>
        <label><input type="checkbox" name="q10" value="correct2"> More concise code</label>
        <label><input type="checkbox" name="q10" value="wrong1"> Uses more memory</label>
        <label><input type="checkbox" name="q10" value="correct3"> Operations run in compiled C code</label>
        <label><input type="checkbox" name="q10" value="wrong2"> Requires less knowledge of NumPy</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 -->
    <div class="quiz-question">
      <h3>Question 11: Reduction Operations - Multiple Select</h3>
      <p><strong>Select ALL</strong> valid NumPy reduction functions:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q11" value="correct1"> np.mean()</label>
        <label><input type="checkbox" name="q11" value="correct2"> np.sum()</label>
        <label><input type="checkbox" name="q11" value="correct3"> np.std()</label>
        <label><input type="checkbox" name="q11" value="wrong1"> np.average_all()</label>
        <label><input type="checkbox" name="q11" value="correct4"> np.max()</label>
        <label><input type="checkbox" name="q11" value="correct5"> np.min()</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 -->
    <div class="quiz-question">
      <h3>Question 12: Axis Parameter</h3>
      <p>For a 2D array with shape (3, 4), what does <code>arr.sum(axis=0)</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q12" value="wrong1"> Sum of all elements (scalar)</label>
        <label><input type="radio" name="q12" value="correct"> Array of shape (4,) - sum along rows</label>
        <label><input type="radio" name="q12" value="wrong2"> Array of shape (3,) - sum along columns</label>
        <label><input type="radio" name="q12" value="wrong3"> The first row of the array</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 -->
    <div class="quiz-question">
      <h3>Question 13: Weighted Averages</h3>
      <p>In climate data analysis, why do we use area weights when computing global averages?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q13" value="wrong1"> To make calculations faster</label>
        <label><input type="radio" name="q13" value="correct"> To account for different grid cell sizes at different latitudes</label>
        <label><input type="radio" name="q13" value="wrong2"> To remove outliers from the data</label>
        <label><input type="radio" name="q13" value="wrong3"> To normalize temperature values</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 -->
    <div class="quiz-question">
      <h3>Question 14: Linear Algebra</h3>
      <p>Which NumPy function computes matrix multiplication?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q14" value="wrong1"> np.multiply()</label>
        <label><input type="radio" name="q14" value="wrong2"> arr1 * arr2</label>
        <label><input type="radio" name="q14" value="correct"> np.dot() or arr1 @ arr2</label>
        <label><input type="radio" name="q14" value="wrong3"> np.cross()</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 -->
    <div class="quiz-question">
      <h3>Question 15: Saving Arrays</h3>
      <p>Which function saves a NumPy array to a .npy file?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q15" value="wrong1"> np.write()</label>
        <label><input type="radio" name="q15" value="correct"> np.save()</label>
        <label><input type="radio" name="q15" value="wrong2"> np.savez()</label>
        <label><input type="radio" name="q15" value="wrong3"> np.tofile()</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 -->
    <div class="quiz-question">
      <h3>Question 16: Loading Arrays</h3>
      <p>Which function loads a NumPy array from a .npy file?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q16" value="wrong1"> np.read()</label>
        <label><input type="radio" name="q16" value="correct"> np.load()</label>
        <label><input type="radio" name="q16" value="wrong2"> np.open()</label>
        <label><input type="radio" name="q16" value="wrong3"> np.fromfile()</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
    </div>

    <!-- Question 17 -->
    <div class="quiz-question">
      <h3>Question 17: DateTime Arrays</h3>
      <p>Which NumPy data type is used for working with dates and times?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q17" value="wrong1"> np.date</label>
        <label><input type="radio" name="q17" value="correct"> np.datetime64</label>
        <label><input type="radio" name="q17" value="wrong2"> np.timestamp</label>
        <label><input type="radio" name="q17" value="wrong3"> np.time</label>
      </div>
      <div class="feedback" id="feedback-q17"></div>
    </div>

    <!-- Question 18 -->
    <div class="quiz-question">
      <h3>Question 18: Array Reshaping</h3>
      <p>Given an array with 12 elements, which shape is NOT valid for reshaping?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q18" value="wrong1"> (3, 4)</label>
        <label><input type="radio" name="q18" value="wrong2"> (2, 6)</label>
        <label><input type="radio" name="q18" value="correct"> (3, 5)</label>
        <label><input type="radio" name="q18" value="wrong3"> (12, 1)</label>
      </div>
      <div class="feedback" id="feedback-q18"></div>
    </div>

    <!-- Question 19 -->
    <div class="quiz-question">
      <h3>Question 19: Element-wise Operations</h3>
      <p>What does the <code>*</code> operator do when applied to two NumPy arrays?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q19" value="wrong1"> Matrix multiplication</label>
        <label><input type="radio" name="q19" value="correct"> Element-wise multiplication</label>
        <label><input type="radio" name="q19" value="wrong2"> Cross product</label>
        <label><input type="radio" name="q19" value="wrong3"> Dot product</label>
      </div>
      <div class="feedback" id="feedback-q19"></div>
    </div>

    <!-- Question 20 -->
    <div class="quiz-question">
      <h3>Question 20: True or False</h3>
      <p>NumPy arrays can contain elements of different data types (like Python lists).</p>
      <div class="quiz-options">
        <label><input type="radio" name="q20" value="wrong"> True</label>
        <label><input type="radio" name="q20" value="correct"> False</label>
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
  const quizForm = document.getElementById('numpy-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>ndim</strong> is correct! It returns the number of dimensions (axes) of the array.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>(2, 3)</strong> is correct! The array has 2 rows and 3 columns, so shape is (2, 3).'
    },
    q3: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4', 'correct5'],
      feedback: '✅ Correct! <strong>array(), arange(), linspace(), zeros(), and ones()</strong> all create NumPy arrays. create() is not a NumPy function.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>arange()</strong> uses step size, while <strong>linspace()</strong> specifies the number of points between start and stop.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>np.eye()</strong> is correct! It creates an identity matrix with 1s on the diagonal and 0s elsewhere.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>np.random.rand()</strong> is correct! It generates random floats from a uniform distribution in [0, 1).'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>[20, 30, 40]</strong> is correct! Slicing [1:4] includes indices 1, 2, 3 but excludes 4.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ Correct! Boolean masking allows you to <strong>select elements based on conditions</strong>, like arr[arr > 10].'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ Correct! Broadcasting is NumPy\'s <strong>automatic expansion of arrays</strong> to compatible shapes for element-wise operations.'
    },
    q10: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! Vectorization provides <strong>faster execution, concise code, and uses compiled C</strong>. It\'s actually more memory efficient than loops.'
    },
    q11: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4', 'correct5'],
      feedback: '✅ Correct! <strong>mean(), sum(), std(), max(), and min()</strong> are all reduction functions. average_all() doesn\'t exist.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>axis=0</strong> sums along rows (down the columns), resulting in shape (4,) for a (3, 4) array.'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ Correct! Area weights account for <strong>grid cell size differences at different latitudes</strong> (cells near poles are smaller).'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>np.dot()</strong> or the <strong>@ operator</strong> perform matrix multiplication. * does element-wise multiplication.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>np.save()</strong> is correct! It saves a single array to a .npy file in NumPy\'s binary format.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>np.load()</strong> is correct! It loads arrays from .npy or .npz files.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ <strong>np.datetime64</strong> is correct! It\'s NumPy\'s data type for handling dates and times with various units.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>(3, 5)</strong> = 15 elements, but the original array has 12 elements. The total must match!'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ Correct! The <strong>* operator performs element-wise multiplication</strong>. Use @ or np.dot() for matrix multiplication.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>False</strong> is correct! NumPy arrays are homogeneous - all elements must have the same data type (dtype).'
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
      
      if (qName === 'q3' || qName === 'q10' || qName === 'q11') {
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
      message = '🎉 Outstanding! You have excellent NumPy skills for climate data analysis. You\'re ready to work with real climate datasets!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid grasp of NumPy fundamentals. Review the questions you missed and practice more!';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep practicing! Work through the NumPy tutorial examples and experiment with array operations.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! NumPy is fundamental for climate data analysis. Review the tutorial and practice with small examples.';
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
  background: linear-gradient(135deg, #f57c00 0%, #e65100 100%);
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
  border-left: 4px solid #f57c00;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #ffb74d;
}

.quiz-question h3 {
  color: #f57c00;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-question h3 {
  color: #ffb74d;
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
  border-color: #f57c00;
}

[data-md-color-scheme="slate"] .quiz-options label {
  border-color: #455a64;
}

[data-md-color-scheme="slate"] .quiz-options label:hover {
  background: #37474f;
  border-color: #ffb74d;
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
  color: #f57c00;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-results h2 {
  color: #ffb74d;
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
  color: #f57c00;
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

- Think about array shapes and dimensions carefully
- Remember that NumPy uses 0-based indexing
- Understand the difference between element-wise and matrix operations
- For multiple select questions, select ALL correct answers
- Pay attention to axis parameters in reduction operations
- Consider when to use broadcasting vs explicit loops
- Practice with small examples to verify your understanding!

---

## 📚 Additional Resources

- [NumPy Tutorial](../day2/03-Numpy_for_Climate_and_Meteorology_Workshop.md)
- [Official NumPy Documentation](https://numpy.org/doc/)
- [NumPy for Absolute Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy Tutorial - W3Schools](https://www.w3schools.com/python/numpy/)
- [SciPy Lectures - NumPy](https://scipy-lectures.org/intro/numpy/index.html)

---

## 🚀 Key Concepts Covered

This quiz tests your understanding of:

1. **Array Basics** - ndim, shape, size, dtype
2. **Array Creation** - array(), arange(), linspace(), zeros(), ones(), eye()
3. **Random Numbers** - Uniform and Gaussian distributions
4. **Indexing & Slicing** - Basic and advanced indexing
5. **Boolean Masking** - Conditional selection
6. **Broadcasting** - Automatic shape matching
7. **Vectorization** - Fast operations without loops
8. **Reductions** - mean(), sum(), std(), max(), min() with axis parameter
9. **Area Weighting** - Climate data specific considerations
10. **Linear Algebra** - Matrix operations, dot products
11. **I/O Operations** - save(), load()
12. **DateTime** - Working with temporal data
13. **Array Manipulation** - Reshaping and element-wise operations

---

**Good luck! NumPy is the foundation for all climate data analysis in Python!** 🔢📊


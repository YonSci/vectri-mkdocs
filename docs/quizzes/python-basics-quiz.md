# Python Basics Interactive Quiz

Test your Python programming knowledge with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="python-basics-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Python Comments</h3>
      <p>Which symbol is used to write a single-line comment in Python?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> //</label>
        <label><input type="radio" name="q1" value="correct"> #</label>
        <label><input type="radio" name="q1" value="wrong2"> /* */</label>
        <label><input type="radio" name="q1" value="wrong3"> --</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Indentation</h3>
      <p>In Python, what is the standard number of spaces for indentation?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> 2 spaces</label>
        <label><input type="radio" name="q2" value="correct"> 4 spaces</label>
        <label><input type="radio" name="q2" value="wrong2"> 8 spaces</label>
        <label><input type="radio" name="q2" value="wrong3"> Indentation doesn't matter in Python</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: Variable Types - Multiple Select</h3>
      <p><strong>Select ALL</strong> valid Python data types for numbers:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q3" value="correct1"> int</label>
        <label><input type="checkbox" name="q3" value="correct2"> float</label>
        <label><input type="checkbox" name="q3" value="correct3"> complex</label>
        <label><input type="checkbox" name="q3" value="wrong1"> decimal</label>
        <label><input type="checkbox" name="q3" value="wrong2"> number</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: String Indexing</h3>
      <p>Given the string <code>text = "Python"</code>, what does <code>text[1]</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> P</label>
        <label><input type="radio" name="q4" value="correct"> y</label>
        <label><input type="radio" name="q4" value="wrong2"> t</label>
        <label><input type="radio" name="q4" value="wrong3"> h</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: Lists</h3>
      <p>Which method adds an element to the END of a list?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q5" value="wrong1"> add()</label>
        <label><input type="radio" name="q5" value="correct"> append()</label>
        <label><input type="radio" name="q5" value="wrong2"> insert()</label>
        <label><input type="radio" name="q5" value="wrong3"> extend()</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: List Slicing</h3>
      <p>Given <code>numbers = [0, 1, 2, 3, 4, 5]</code>, what does <code>numbers[1:4]</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> [0, 1, 2, 3]</label>
        <label><input type="radio" name="q6" value="correct"> [1, 2, 3]</label>
        <label><input type="radio" name="q6" value="wrong2"> [1, 2, 3, 4]</label>
        <label><input type="radio" name="q6" value="wrong3"> [2, 3, 4]</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Dictionaries</h3>
      <p>How do you access the value associated with the key "temperature" in <code>data = {"temperature": 25, "humidity": 60}</code>?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> data.temperature</label>
        <label><input type="radio" name="q7" value="correct"> data["temperature"]</label>
        <label><input type="radio" name="q7" value="wrong2"> data(temperature)</label>
        <label><input type="radio" name="q7" value="wrong3"> data->temperature</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Mutable vs Immutable - Multiple Select</h3>
      <p><strong>Select ALL</strong> data structures that are MUTABLE (can be changed after creation):</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q8" value="correct1"> Lists</label>
        <label><input type="checkbox" name="q8" value="correct2"> Dictionaries</label>
        <label><input type="checkbox" name="q8" value="wrong1"> Tuples</label>
        <label><input type="checkbox" name="q8" value="correct3"> Sets</label>
        <label><input type="checkbox" name="q8" value="wrong2"> Strings</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Comparison Operators</h3>
      <p>What does the operator <code>==</code> do in Python?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> Assigns a value to a variable</label>
        <label><input type="radio" name="q9" value="correct"> Checks if two values are equal</label>
        <label><input type="radio" name="q9" value="wrong2"> Checks if two values are identical objects</label>
        <label><input type="radio" name="q9" value="wrong3"> Performs mathematical addition</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: For Loops</h3>
      <p>What is the output of this code?<br><code>for i in range(3):<br>&nbsp;&nbsp;&nbsp;&nbsp;print(i)</code></p>
      <div class="quiz-options">
        <label><input type="radio" name="q10" value="wrong1"> 1 2 3</label>
        <label><input type="radio" name="q10" value="correct"> 0 1 2</label>
        <label><input type="radio" name="q10" value="wrong2"> 0 1 2 3</label>
        <label><input type="radio" name="q10" value="wrong3"> 1 2</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 -->
    <div class="quiz-question">
      <h3>Question 11: Functions</h3>
      <p>Which keyword is used to define a function in Python?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q11" value="wrong1"> function</label>
        <label><input type="radio" name="q11" value="correct"> def</label>
        <label><input type="radio" name="q11" value="wrong2"> func</label>
        <label><input type="radio" name="q11" value="wrong3"> define</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 -->
    <div class="quiz-question">
      <h3>Question 12: Lambda Functions</h3>
      <p>What is a lambda function in Python?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q12" value="wrong1"> A function that uses Greek letters</label>
        <label><input type="radio" name="q12" value="correct"> A small anonymous function defined with lambda keyword</label>
        <label><input type="radio" name="q12" value="wrong2"> A function that returns multiple values</label>
        <label><input type="radio" name="q12" value="wrong3"> A recursive function</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 -->
    <div class="quiz-question">
      <h3>Question 13: Built-in Functions - Multiple Select</h3>
      <p><strong>Select ALL</strong> valid Python built-in functions:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q13" value="correct1"> map()</label>
        <label><input type="checkbox" name="q13" value="correct2"> filter()</label>
        <label><input type="checkbox" name="q13" value="correct3"> len()</label>
        <label><input type="checkbox" name="q13" value="wrong1"> size()</label>
        <label><input type="checkbox" name="q13" value="correct4"> sum()</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 -->
    <div class="quiz-question">
      <h3>Question 14: List Comprehension</h3>
      <p>What does this list comprehension produce?<br><code>[x**2 for x in range(4)]</code></p>
      <div class="quiz-options">
        <label><input type="radio" name="q14" value="wrong1"> [0, 1, 2, 3]</label>
        <label><input type="radio" name="q14" value="correct"> [0, 1, 4, 9]</label>
        <label><input type="radio" name="q14" value="wrong2"> [1, 4, 9, 16]</label>
        <label><input type="radio" name="q14" value="wrong3"> [2, 4, 6, 8]</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 -->
    <div class="quiz-question">
      <h3>Question 15: Enumerate Function</h3>
      <p>What does the <code>enumerate()</code> function return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q15" value="wrong1"> Only the indices of items</label>
        <label><input type="radio" name="q15" value="correct"> Pairs of (index, value) for each item</label>
        <label><input type="radio" name="q15" value="wrong2"> The count of items in a sequence</label>
        <label><input type="radio" name="q15" value="wrong3"> A sorted list of items</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 -->
    <div class="quiz-question">
      <h3>Question 16: Zip Function</h3>
      <p>What does <code>list(zip([1, 2], ['a', 'b']))</code> return?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q16" value="wrong1"> [1, 2, 'a', 'b']</label>
        <label><input type="radio" name="q16" value="correct"> [(1, 'a'), (2, 'b')]</label>
        <label><input type="radio" name="q16" value="wrong2"> [[1, 'a'], [2, 'b']]</label>
        <label><input type="radio" name="q16" value="wrong3"> {1: 'a', 2: 'b'}</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
    </div>

    <!-- Question 17 -->
    <div class="quiz-question">
      <h3>Question 17: Modules</h3>
      <p>How do you import a specific function called <code>sqrt</code> from the <code>math</code> module?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q17" value="wrong1"> import math.sqrt</label>
        <label><input type="radio" name="q17" value="correct"> from math import sqrt</label>
        <label><input type="radio" name="q17" value="wrong2"> import sqrt from math</label>
        <label><input type="radio" name="q17" value="wrong3"> using math.sqrt</label>
      </div>
      <div class="feedback" id="feedback-q17"></div>
    </div>

    <!-- Question 18 -->
    <div class="quiz-question">
      <h3>Question 18: Error Types - Multiple Select</h3>
      <p><strong>Select ALL</strong> common Python error types:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q18" value="correct1"> SyntaxError</label>
        <label><input type="checkbox" name="q18" value="correct2"> NameError</label>
        <label><input type="checkbox" name="q18" value="correct3"> TypeError</label>
        <label><input type="checkbox" name="q18" value="correct4"> IndexError</label>
        <label><input type="checkbox" name="q18" value="wrong1"> LogicError</label>
      </div>
      <div class="feedback" id="feedback-q18"></div>
    </div>

    <!-- Question 19 -->
    <div class="quiz-question">
      <h3>Question 19: Exception Handling</h3>
      <p>Which keyword is used to catch exceptions in Python?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q19" value="wrong1"> catch</label>
        <label><input type="radio" name="q19" value="correct"> except</label>
        <label><input type="radio" name="q19" value="wrong2"> error</label>
        <label><input type="radio" name="q19" value="wrong3"> handle</label>
      </div>
      <div class="feedback" id="feedback-q19"></div>
    </div>

    <!-- Question 20 -->
    <div class="quiz-question">
      <h3>Question 20: True or False</h3>
      <p>In Python, lists can contain elements of different data types (e.g., integers, strings, and floats together).</p>
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
  const quizForm = document.getElementById('python-basics-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>#</strong> is correct! The hash/pound symbol is used for single-line comments in Python.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>4 spaces</strong> is correct! PEP 8 (Python style guide) recommends 4 spaces for indentation.'
    },
    q3: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! <strong>int, float, and complex</strong> are the three numeric types in Python.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>"y"</strong> is correct! Python uses 0-based indexing, so text[1] returns the second character.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>append()</strong> is correct! It adds a single element to the end of a list.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>[1, 2, 3]</strong> is correct! Slicing [1:4] includes index 1, 2, 3 but excludes 4.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>data["temperature"]</strong> is correct! Dictionary values are accessed using square brackets with the key.'
    },
    q8: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! <strong>Lists, dictionaries, and sets</strong> are mutable. Tuples and strings are immutable.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>Checks if two values are equal</strong> is correct! == is the equality comparison operator, while = is assignment.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ <strong>0 1 2</strong> is correct! range(3) generates numbers from 0 to 2 (3 is excluded).'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>def</strong> is correct! Functions are defined using the def keyword followed by the function name.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ Correct! A <strong>lambda function</strong> is a small anonymous function defined inline using the lambda keyword.'
    },
    q13: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>map(), filter(), len(), and sum()</strong> are all built-in Python functions. size() is not.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>[0, 1, 4, 9]</strong> is correct! List comprehension squares each number: 0²=0, 1²=1, 2²=4, 3²=9.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>enumerate()</strong> returns pairs of (index, value) for iteration, useful when you need both.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>[(1, "a"), (2, "b")]</strong> is correct! zip() pairs elements from multiple iterables into tuples.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ <strong>from math import sqrt</strong> is correct! This imports only the sqrt function, not the entire module.'
    },
    q18: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>SyntaxError, NameError, TypeError, and IndexError</strong> are common Python exceptions. LogicError is not a standard Python error.'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ <strong>except</strong> is correct! Python uses try-except blocks for exception handling (not try-catch like some languages).'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>True</strong> is correct! Python lists are heterogeneous - they can contain mixed data types like [1, "hello", 3.14].'
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
      
      if (qName === 'q3' || qName === 'q8' || qName === 'q13' || qName === 'q18') {
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
      message = '🎉 Outstanding! You have mastered Python basics. You\'re ready for more advanced topics and climate data analysis!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid foundation in Python. Review the questions you missed and keep practicing.';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep practicing! Review the Python basics tutorial and try coding examples yourself.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Review the Python basics carefully and practice writing code. Programming takes time - don\'t give up!';
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
  background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
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
  border-left: 4px solid #2196f3;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #64b5f6;
}

.quiz-question h3 {
  color: #2196f3;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-question h3 {
  color: #64b5f6;
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
  border-color: #2196f3;
}

[data-md-color-scheme="slate"] .quiz-options label {
  border-color: #455a64;
}

[data-md-color-scheme="slate"] .quiz-options label:hover {
  background: #37474f;
  border-color: #64b5f6;
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
  color: #2196f3;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-results h2 {
  color: #64b5f6;
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
  color: #2196f3;
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

- Think about Python syntax rules before answering
- Remember that Python is 0-indexed (counting starts at 0)
- Pay attention to mutable vs immutable data types
- For multiple select questions, select ALL correct answers
- Consider the difference between similar functions (e.g., append vs extend)
- Review your answers before submitting
- Practice writing actual Python code to reinforce concepts!

---

## 📚 Additional Resources

- [Python Basics Tutorial](../day2/02-Python_Basics_for_Climate_and_Meteorology_Workshop.md)
- [Python Setup Guide](../day2/01-Python_Setup_for_Climate_and_Meteorology_Workshop.md)
- [Official Python Documentation](https://docs.python.org/3/)
- [Python for Data Science](https://www.python.org/about/gettingstarted/)
- Practice on [Python.org Interactive Shell](https://www.python.org/shell/)

---

## 🚀 Key Concepts Covered

This quiz tests your understanding of:

1. **Syntax & Structure** - Comments, indentation, keywords
2. **Variables & Types** - int, float, complex, strings
3. **Data Structures** - Lists, dictionaries, tuples, sets
4. **Operators** - Comparison and logical operators
5. **Control Flow** - if statements, for loops, while loops
6. **Functions** - Definition, lambda functions
7. **Built-in Functions** - map(), filter(), len(), sum()
8. **Advanced Features** - List comprehensions, enumerate, zip
9. **Modules** - Importing and using modules
10. **Error Handling** - Common errors and exception handling

---

**Good luck! Python is a powerful tool for climate data analysis!** 🐍📊


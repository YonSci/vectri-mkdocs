# VECTRI Introduction Quiz

Test your understanding of VECTRI with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="vectri-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Why was VECTRI originally developed?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> To replace all existing malaria models with a faster solver</label>
        <label><input type="radio" name="q1" value="wrong2"> To create a model that could be run only through a graphical interface</label>
        <label><input type="radio" name="q1" value="correct"> To address limitations in the Liverpool Malaria Model (LMM), especially the lack of population density and openness of the code</label>
        <label><input type="radio" name="q1" value="wrong3"> To simulate all infectious diseases at once</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: In the original project context, what key scientific question motivated the creation of VECTRI?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> How climate change affects dengue only</label>
        <label><input type="radio" name="q2" value="correct"> Differences between urban, peri-urban and rural transmission of malaria</label>
        <label><input type="radio" name="q2" value="wrong2"> How to optimize Fortran compilers for disease models</label>
        <label><input type="radio" name="q2" value="wrong3"> How bednets change mosquito genetics</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: What was a major limitation of the Liverpool Malaria Model (LMM) noted by Adrian?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q3" value="wrong1"> It could not run on Linux</label>
        <label><input type="radio" name="q3" value="correct"> It assumed 100 people per grid box and did not explicitly use population density datasets</label>
        <label><input type="radio" name="q3" value="wrong2"> It required too much disk space</label>
        <label><input type="radio" name="q3" value="wrong3"> It did not include any climate variables</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: What key aspect of LMM prevented Adrian from easily modifying or extending it?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> The code was only written in Python</label>
        <label><input type="radio" name="q4" value="wrong2"> It required a supercomputer to run</label>
        <label><input type="radio" name="q4" value="correct"> Only an executable was provided, not the source code</label>
        <label><input type="radio" name="q4" value="wrong3"> It had no parameter settings at all</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: Which of the following best describes what VECTRI *is*?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q5" value="wrong1"> A point-and-click GUI tool with no need for programming</label>
        <label><input type="radio" name="q5" value="correct"> A gridded, climate-driven model of mosquito life cycles with parameterizations for various Anopheles and Aedes species</label>
        <label><input type="radio" name="q5" value="wrong2"> A pure human health-care delivery simulation with no mosquitoes</label>
        <label><input type="radio" name="q5" value="wrong3"> A general economic model for health financing</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: At present, which disease is explicitly represented in VECTRI when modelling Anopheles mosquitoes?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> Dengue</label>
        <label><input type="radio" name="q6" value="correct"> Malaria</label>
        <label><input type="radio" name="q6" value="wrong2"> Cholera</label>
        <label><input type="radio" name="q6" value="wrong3"> Zika</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Why does VECTRI use first-order accurate numerical solvers?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> They are the only solvers available in Fortran</label>
        <label><input type="radio" name="q7" value="wrong2"> They guarantee exact solutions for all parameters</label>
        <label><input type="radio" name="q7" value="correct"> They are fast, and uncertainties in parameters and processes are considered larger than numerical errors</label>
        <label><input type="radio" name="q7" value="wrong3"> They allow the model to ignore climate data</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Which of the following best describes the support status of VECTRI from the developers?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> Fully supported with guaranteed quick responses</label>
        <label><input type="radio" name="q8" value="wrong2"> Supported 24/7 by a large helpdesk</label>
        <label><input type="radio" name="q8" value="correct"> Provided "as-is", with only limited, non-guaranteed help from a small research group</label>
        <label><input type="radio" name="q8" value="wrong3"> Supported only if users pay for a license</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Which statement best describes the current operational readiness of VECTRI?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> It is fully validated for operational decision-making without calibration</label>
        <label><input type="radio" name="q9" value="correct"> It should be used primarily as a research tool and carefully tested and calibrated before any operational use</label>
        <label><input type="radio" name="q9" value="wrong2"> It cannot be used for research at all</label>
        <label><input type="radio" name="q9" value="wrong3"> It already includes all real-world interventions and treatments</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Which programming language and environment are most directly associated with running VECTRI?</h3>
      <div class="quiz-options">
        <label><input type="radio" name="q10" value="wrong1"> Java and Windows only</label>
        <label><input type="radio" name="q10" value="wrong2"> R and macOS only</label>
        <label><input type="radio" name="q10" value="correct"> Fortran, with familiarity with Linux being helpful</label>
        <label><input type="radio" name="q10" value="wrong3"> JavaScript in a web browser</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 11: What problem(s) with the LMM motivated Adrian to create VECTRI? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q11" value="correct1"> Lack of explicit human population density representation</label>
        <label><input type="checkbox" name="q11" value="correct2"> Source code not being openly available</label>
        <label><input type="checkbox" name="q11" value="wrong1"> Inability to change parameter settings at all</label>
        <label><input type="checkbox" name="q11" value="correct3"> Difficulty in adding new functionality or checking the correctness of calculations</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 12: Which characteristics make VECTRI a *community model*? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q12" value="correct1"> The source code is visible and can be inspected</label>
        <label><input type="checkbox" name="q12" value="correct2"> Users can change the source code</label>
        <label><input type="checkbox" name="q12" value="correct3"> Users can pass the model to their friends/colleagues</label>
        <label><input type="checkbox" name="q12" value="wrong1"> It is strictly proprietary and closed</label>
        <label><input type="checkbox" name="q12" value="correct4"> Users are encouraged to contribute improvements back to a shared version</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 13: According to the description, which of the following are true about what VECTRI *is*? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q13" value="correct1"> A gridded model focused on climate impacts on mosquito life cycles</label>
        <label><input type="checkbox" name="q13" value="correct2"> Able to run on regional, national, or continental scales</label>
        <label><input type="checkbox" name="q13" value="correct3"> Limited (currently) to modelling one vector at a time</label>
        <label><input type="checkbox" name="q13" value="correct4"> Able to run at resolutions down to about 1 km</label>
        <label><input type="checkbox" name="q13" value="wrong1"> A model that already includes multiple diseases beyond malaria</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 14: Which characteristics describe what VECTRI *is not*? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q14" value="correct1"> A fully supported, ready-to-use operational tool with guaranteed assistance</label>
        <label><input type="checkbox" name="q14" value="correct2"> A simple "point and click to run" model</label>
        <label><input type="checkbox" name="q14" value="correct3"> A model that developers accept responsibility for in operational planning environments without conditions</label>
        <label><input type="checkbox" name="q14" value="correct4"> A tool that should be deployed operationally without prior testing and calibration</label>
        <label><input type="checkbox" name="q14" value="wrong1"> A model provided "as-is" by a small research group</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 15: Which limitations or cautions are explicitly mentioned about using VECTRI outputs? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q15" value="correct1"> Predicted clinical case counts will likely be higher than observed</label>
        <label><input type="checkbox" name="q15" value="correct2"> The model neglects interventions, treatment, and other factors that reduce observed case counts</label>
        <label><input type="checkbox" name="q15" value="correct3"> Bednet and SIT (Sterile Insect Technique) interventions in the model are not well tested</label>
        <label><input type="checkbox" name="q15" value="wrong1"> The developers guarantee responsibility for how the model is used operationally</label>
        <label><input type="checkbox" name="q15" value="correct4"> The model should be well tested and calibrated before any operational use</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 - Multiple Select -->
    <div class="quiz-question">
      <h3>Question 16: Which of the following best describe practical requirements or skills that are helpful for using VECTRI? <strong>(Select all that apply)</strong></h3>
      <div class="quiz-options">
        <label><input type="checkbox" name="q16" value="correct1"> Some familiarity with Linux</label>
        <label><input type="checkbox" name="q16" value="correct2"> Ability to work with Fortran-based code</label>
        <label><input type="checkbox" name="q16" value="wrong1"> Expectation of a full graphical user interface for all tasks</label>
        <label><input type="checkbox" name="q16" value="correct3"> Willingness to work without a polished "point and click" experience</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
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
        <div class="result-value" id="score-value">0/16</div>
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
  const quizForm = document.getElementById('vectri-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ Correct! VECTRI was created to fix key limitations in LMM: no explicit population density & no open source code for modification.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ Correct! The project task was to study urban vs peri-urban vs rural malaria transmission.'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ Correct! LMM assumed 100 people per grid box and did not explicitly use population density, making dilution effects unclear.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ Correct! Only the executable was available, so Adrian couldn\'t inspect or modify the source code.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ Correct! The text clearly describes VECTRI as a gridded, climate-driven mosquito life-cycle model.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ Correct! Currently, only malaria is represented when modelling Anopheles.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ Correct! The philosophy: use fast first-order solvers because parameter/process uncertainty is larger than numerical error.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ Correct! The model is provided "as-is" by a very small research group; support is not guaranteed.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ Correct! The text stresses VECTRI is a research tool and must be tested & calibrated before operational use.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ Correct! VECTRI is Fortran-based, and some Linux familiarity is helpful (though not strictly essential).'
    },
    q11: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! LMM did not use explicit population density, only an executable was distributed (no source code), and without code access, adding functionality or verifying calculations was difficult.'
    },
    q12: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! The source is open; users can inspect and modify it, share the model, and contribute improvements back.'
    },
    q13: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! VECTRI focuses on climate impacts on mosquito life cycles, runs on regional to continental scales, models one vector at a time, and can run down to 1 km resolution.'
    },
    q14: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! VECTRI is NOT a fully supported operational tool, NOT point-and-click, developers do NOT accept responsibility for operational use, and it should NOT be deployed without testing.'
    },
    q15: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! Predicted cases are higher than observed because interventions/treatment are neglected, bednet/SIT interventions are not well tested, and calibration/testing are required before operational use.'
    },
    q16: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! Linux familiarity is helpful, the model is Fortran-based, and it is NOT a "point and click" model.'
    }
  };

  // Submit quiz
  submitBtn.addEventListener('click', function() {
    let score = 0;
    let totalQuestions = 16;
    
    // Check each question
    for (let i = 1; i <= totalQuestions; i++) {
      const qName = 'q' + i;
      const feedback = document.getElementById('feedback-' + qName);
      
      if (i >= 11) {
        // Multiple select questions (Q11-Q16)
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
          feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. Review the text to find all correct answers.</div>';
        }
      } else {
        // Single select questions (Q1-Q10)
        const selected = document.querySelector('input[name="' + qName + '"]:checked');
        if (selected) {
          if (selected.value === answers[qName].correct) {
            score++;
            feedback.innerHTML = '<div class="feedback-correct">' + answers[qName].feedback + '</div>';
          } else {
            feedback.innerHTML = '<div class="feedback-wrong">❌ Incorrect. ' + answers[qName].feedback.replace('✅ Correct!', '') + '</div>';
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
      message = '🎉 Outstanding! You have an excellent understanding of VECTRI. You\'re ready to dive into the practical sessions!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid foundation. Review the questions you missed and you\'ll be all set.';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep studying! Review the VECTRI introduction and retake the quiz.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Review the material carefully and try again. Don\'t worry - practice makes perfect!';
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

</div>

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

- [VECTRI Online Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)
- [VECTRI PDF Manual](../pdfs/VECTRI_manual_v1.6.pdf)
- [Back to VECTRI Introduction](../day1/01-vectri-intro.md)
- Workshop Lab Exercises (Days 2-5)


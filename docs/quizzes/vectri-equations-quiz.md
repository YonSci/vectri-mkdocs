# VECTRI Core Equations Quiz

Test your understanding of VECTRI model equations, parameters, and physical processes!

---

<style>
  .quiz-container {
    max-width: 900px;
    margin: 2rem auto;
    font-family: 'Roboto', sans-serif;
  }
  
  .question-block {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    border-color: #667eea;
    background-color: #f5f7ff;
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
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
    color: #667eea;
    margin-bottom: 1rem;
  }
  
  .score-display {
    font-size: 2.5rem;
    font-weight: bold;
    color: #764ba2;
    margin: 1rem 0;
  }
  
  .note {
    background-color: #e7f3ff;
    border-left: 4px solid #667eea;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
  }
</style>

<div class="quiz-container">
  <div class="note">
    <strong>📝 Note:</strong> This quiz contains 20 questions including multiple choice and multiple selection questions. Some questions may have more than one correct answer. Select all that apply for those questions.
  </div>

  <form id="vectri-equations-quiz">
    
    <!-- Question 1 -->
    <div class="question-block">
      <h3>1. What is the minimum water temperature (T_L_min) required for larval development in VECTRI?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q1" value="wrong1">
          10.0°C
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong2">
          7.7°C
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="correct">
          16.0°C
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong3">
          20.0°C
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 2 -->
    <div class="question-block">
      <h3>2. The larval development rate (R_L) represents:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q2" value="wrong1">
          The number of larvae produced per day
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="correct">
          The fraction of the larval life cycle completed per day
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong2">
          The survival probability of larvae
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong3">
          The total number of days for development
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 3 -->
    <div class="question-block">
      <h3>3. Which factors affect larval survival in VECTRI? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct1">
          Crowding (larval biomass density)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct2">
          Rainfall flushing
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct3">
          Pond coverage fraction
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="wrong1">
          Adult mosquito density
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 4 -->
    <div class="question-block">
      <h3>4. What happens to larvae when water temperature exceeds T_L_max (37°C)?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q4" value="wrong1">
          Development accelerates dramatically
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="correct">
          No larvae survive (lethal temperature)
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong2">
          Development continues at maximum rate
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong3">
          Development slows but continues
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 5 -->
    <div class="question-block">
      <h3>5. The gonotrophic cycle in VECTRI represents:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q5" value="wrong1">
          The time for larvae to develop
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="correct">
          The time between blood meals and egg development
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong2">
          The time for parasites to develop in mosquitoes
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong3">
          The lifespan of adult mosquitoes
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 6 -->
    <div class="question-block">
      <h3>6. What is the minimum temperature (T_gono_min) for the gonotrophic cycle?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q6" value="wrong1">
          16.0°C
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="correct">
          7.7°C
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong2">
          10.0°C
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong3">
          20.0°C
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 7 -->
    <div class="question-block">
      <h3>7. The Extrinsic Incubation Period (EIP) is:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q7" value="wrong1">
          The time eggs take to hatch
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="correct">
          The time for parasites to develop inside mosquitoes
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong2">
          The time between blood meals
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong3">
          The incubation period in humans
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 8 -->
    <div class="question-block">
      <h3>8. For malaria transmission to occur, which condition must be met?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q8" value="wrong1">
          Water temperature must exceed 30°C
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="correct">
          Mosquito lifespan must exceed EIP
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="wrong2">
          Pond coverage must be at maximum
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="wrong3">
          Rainfall must be constant
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 9 -->
    <div class="question-block">
      <h3>9. The Martens II equation in VECTRI is used to calculate:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q9" value="wrong1">
          Larval development rate
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="correct">
          Adult mosquito daily survival probability
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong2">
          Egg laying rate
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong3">
          Biting rate
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 10 -->
    <div class="question-block">
      <h3>10. Indoor temperature (T_indoor) is calculated using: (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct1">
          Outdoor air temperature (T2m)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct2">
          An intercept parameter (T0_indoor = 10.33°C)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="correct3">
          A slope parameter (K_indoor = 0.58)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q10" value="wrong1">
          Water temperature
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 11 -->
    <div class="question-block">
      <h3>11. What does the parameter beta_indoor represent?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q11" value="wrong1">
          The temperature difference between indoors and outdoors
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="correct">
          The fraction of time mosquitoes spend indoors
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong2">
          The indoor survival probability
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong3">
          The indoor biting rate
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 12 -->
    <div class="question-block">
      <h3>12. The pond water balance in VECTRI includes: (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q12" value="correct1">
          Rainfall inflow
        </label>
        <label class="option-label">
          <input type="checkbox" name="q12" value="correct2">
          Evaporation
        </label>
        <label class="option-label">
          <input type="checkbox" name="q12" value="correct3">
          Infiltration
        </label>
        <label class="option-label">
          <input type="checkbox" name="q12" value="wrong1">
          Ocean currents
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 13 -->
    <div class="question-block">
      <h3>13. What is w_max in the pond hydrology model?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q13" value="wrong1">
          Maximum water depth in meters
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="correct">
          Maximum fractional pond coverage (typically 0.04 or 4%)
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong2">
          Maximum rainfall rate
        </label>
        <label class="option-label">
          <input type="radio" name="q13" value="wrong3">
          Maximum evaporation rate
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 14 -->
    <div class="question-block">
      <h3>14. Heavy rainfall affects larvae primarily through:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q14" value="wrong1">
          Increasing crowding
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="correct">
          Flushing (washing larvae out of breeding sites)
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong2">
          Decreasing temperature
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong3">
          Increasing food availability
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 15 -->
    <div class="question-block">
      <h3>15. The parameter tau_zoo relates to:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q15" value="wrong1">
          Temperature threshold
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="correct">
          Zoophily/anthropophily (preference for animal vs human hosts)
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong2">
          Larval development time
        </label>
        <label class="option-label">
          <input type="radio" name="q15" value="wrong3">
          Pond evaporation rate
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 16 -->
    <div class="question-block">
      <h3>16. The daily Entomological Inoculation Rate (EIR_d) is calculated as:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q16" value="wrong1">
          Number of mosquitoes × survival probability
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="correct">
          Human biting rate × CSPR (infectious fraction)
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong2">
          Temperature × rainfall
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong3">
          Larval density × emergence rate
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 17 -->
    <div class="question-block">
      <h3>17. As temperature increases from 20°C to 30°C: (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct1">
          Larval development accelerates
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct2">
          EIP (parasite development) shortens
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="correct3">
          Gonotrophic cycle shortens
        </label>
        <label class="option-label">
          <input type="checkbox" name="q17" value="wrong1">
          All processes slow down
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 18 -->
    <div class="question-block">
      <h3>18. What is the relationship between mosquito lifespan and daily survival probability (P_V_surv)?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q18" value="wrong1">
          Lifespan = P_V_surv
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="correct">
          Lifespan ≈ 1 / (1 - P_V_surv)
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong2">
          Lifespan = 1 / P_V_surv
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong3">
          Lifespan = P_V_surv × temperature
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 19 -->
    <div class="question-block">
      <h3>19. Crowding effects on larvae occur when:</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q19" value="wrong1">
          Rainfall is too high
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="correct">
          Larval biomass approaches the carrying capacity (M_L_max × w)
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong2">
          Temperature is too low
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong3">
          Adult mosquitoes are too dense
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 20 -->
    <div class="question-block">
      <h3>20. Which visualization shows the relationship between breeding habitat and rainfall?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q20" value="wrong1">
          Temperature dynamics plot
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="correct">
          Rainfall, water balance, and pond fraction plot
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong2">
          EIP vs lifespan plot
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong3">
          Transmission metrics plot
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
  const quizForm = document.getElementById('vectri-equations-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>16.0°C</strong> is correct! This is T_L_min, the minimum water temperature for larval development.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>Fraction of life cycle completed per day</strong> is correct! R_L tells us what proportion of development occurs each day.'
    },
    q3: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Crowding, rainfall flushing, and pond coverage</strong> all affect larval survival! These factors interact to determine P_L_surv.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>No larvae survive</strong> is correct! T_L_max = 37°C is the lethal upper temperature limit.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>Time between blood meals and egg development</strong> is correct! The gonotrophic cycle is a key component of adult mosquito biology.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>7.7°C</strong> is correct! This is T_gono_min, the minimum temperature for egg development.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>Time for parasites to develop inside mosquitoes</strong> is correct! EIP determines how long before an infected mosquito can transmit malaria.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ <strong>Mosquito lifespan must exceed EIP</strong> is correct! Mosquitoes must survive long enough for parasites to complete development.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>Adult mosquito daily survival probability</strong> is correct! The Martens II equation relates survival to temperature.'
    },
    q10: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>All three parameters</strong> are used! T_indoor = T0_indoor + K_indoor × T2m.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>Fraction of time spent indoors</strong> is correct! This determines the effective temperature mosquitoes experience.'
    },
    q12: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>Rainfall, evaporation, and infiltration</strong> are all components! These determine pond dynamics: dw/dt = K_w × [rain×(w_max - w) - w×(E + I)].'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ <strong>Maximum fractional pond coverage</strong> is correct! w_max is typically 0.04 (4% of the grid cell).'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>Flushing</strong> is correct! Heavy rainfall washes larvae out of breeding sites, especially early instars.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>Zoophily/anthropophily</strong> is correct! tau_zoo scales the preference for human vs animal hosts.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>Human biting rate × CSPR</strong> is correct! EIR_d = hbr × CSPR gives infectious bites per person per day.'
    },
    q17: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>All three processes accelerate</strong> with increasing temperature! Higher temperatures speed up biological rates.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ <strong>Lifespan ≈ 1 / (1 - P_V_surv)</strong> is correct! This gives the expected number of days an adult survives.'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ <strong>When biomass approaches carrying capacity</strong> is correct! Crowding reduces survival when M_L approaches w × M_L_max.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>Rainfall, water balance, and pond fraction plot</strong> is correct! This visualization shows how rainfall drives breeding habitat availability.'
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
      resultMessage.textContent = '🎉 Outstanding! You have excellent understanding of VECTRI equations!';
    } else if (percentage >= 75) {
      resultMessage.textContent = '👍 Great work! You have a solid grasp of VECTRI core concepts.';
    } else if (percentage >= 60) {
      resultMessage.textContent = '✅ Good effort! Review the material and try again to improve your score.';
    } else {
      resultMessage.textContent = '📚 Keep studying! Review the tutorial and try the quiz again.';
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


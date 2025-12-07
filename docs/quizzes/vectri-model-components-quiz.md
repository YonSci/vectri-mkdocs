# VECTRI Model Components Interactive Quiz

Test your understanding of VECTRI's biological and physical components with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="vectri-components-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Larval Development Rate</h3>
      <p>The larval development rate (R_L) depends primarily on which factor?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> Food availability in ponds</label>
        <label><input type="radio" name="q1" value="correct"> Water temperature</label>
        <label><input type="radio" name="q1" value="wrong2"> Human population density</label>
        <label><input type="radio" name="q1" value="wrong3"> Rainfall amount</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Degree-Days Parameter</h3>
      <p>According to Jepson (1947), what is the value of K_L (degree-days required for larval development)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> 200 degree-days</label>
        <label><input type="radio" name="q2" value="correct"> 90.9 degree-days</label>
        <label><input type="radio" name="q2" value="wrong2"> 111 degree-days</label>
        <label><input type="radio" name="q2" value="wrong3"> 37.1 degree-days</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: Larval Mortality Factors - Multiple Select</h3>
      <p><strong>Select ALL</strong> factors that contribute to larval mortality in VECTRI:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q3" value="correct1"> Crowding (resource limitation)</label>
        <label><input type="checkbox" name="q3" value="correct2"> Rainfall-driven flushing</label>
        <label><input type="checkbox" name="q3" value="correct3"> Lethal temperature cutoff</label>
        <label><input type="checkbox" name="q3" value="wrong1"> Wind speed</label>
        <label><input type="checkbox" name="q3" value="correct4"> Base survival rate</label>
        <label><input type="checkbox" name="q3" value="wrong2"> Lunar phase</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: Base Larval Survival</h3>
      <p>What is the approximate base daily survival rate for larvae in "good" conditions?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> 0.95</label>
        <label><input type="radio" name="q4" value="correct"> 0.825</label>
        <label><input type="radio" name="q4" value="wrong2"> 0.60</label>
        <label><input type="radio" name="q4" value="wrong3"> 0.40</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: Flushing Effect</h3>
      <p>Which larval stage is MOST affected by rainfall-driven flushing?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q5" value="correct"> Early larvae (L_f ≈ 0)</label>
        <label><input type="radio" name="q5" value="wrong1"> Mid-stage larvae (L_f ≈ 0.5)</label>
        <label><input type="radio" name="q5" value="wrong2"> Late larvae (L_f = 1)</label>
        <label><input type="radio" name="q5" value="wrong3"> All stages equally</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: Gonotrophic Cycle</h3>
      <p>The gonotrophic cycle represents the time from:</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> Egg laying to adult emergence</label>
        <label><input type="radio" name="q6" value="correct"> Blood meal to egg laying</label>
        <label><input type="radio" name="q6" value="wrong2"> Larval hatching to pupation</label>
        <label><input type="radio" name="q6" value="wrong3"> Adult emergence to first blood meal</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Eggs Per Cycle</h3>
      <p>How many female eggs does each completed gonotrophic cycle typically produce?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> 40</label>
        <label><input type="radio" name="q7" value="correct"> 80</label>
        <label><input type="radio" name="q7" value="wrong2"> 160</label>
        <label><input type="radio" name="q7" value="wrong3"> 200</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Sporogonic Cycle</h3>
      <p>What does the Extrinsic Incubation Period (EIP) represent?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> Time from mosquito bite to human symptoms</label>
        <label><input type="radio" name="q8" value="correct"> Time for parasite to develop inside the mosquito</label>
        <label><input type="radio" name="q8" value="wrong2"> Duration of larval development</label>
        <label><input type="radio" name="q8" value="wrong3"> Length of the gonotrophic cycle</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Temperature and EIP</h3>
      <p>What happens to the EIP at 20°C compared to 25°C?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> EIP becomes shorter (faster development)</label>
        <label><input type="radio" name="q9" value="correct"> EIP becomes much longer (~28 days vs ~12 days)</label>
        <label><input type="radio" name="q9" value="wrong2"> EIP stays the same</label>
        <label><input type="radio" name="q9" value="wrong3"> EIP becomes zero (no development)</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Vector Survival - Multiple Select</h3>
      <p><strong>Select ALL</strong> true statements about adult mosquito survival in VECTRI:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q10" value="correct1"> Survival depends on temperature</label>
        <label><input type="checkbox" name="q10" value="correct2"> The Martens II formulation produces a bell-shaped relationship</label>
        <label><input type="checkbox" name="q10" value="wrong1"> Survival is highest at extreme temperatures</label>
        <label><input type="checkbox" name="q10" value="correct3"> Higher survival occurs at mid-temperatures (~20-25°C)</label>
        <label><input type="checkbox" name="q10" value="wrong2"> Survival is independent of temperature</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 -->
    <div class="quiz-question">
      <h3>Question 11: Expected Lifespan</h3>
      <p>If daily survival probability is 0.9, what is the approximate expected mosquito lifespan?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q11" value="wrong1"> 5 days</label>
        <label><input type="radio" name="q11" value="correct"> 10 days</label>
        <label><input type="radio" name="q11" value="wrong2"> 15 days</label>
        <label><input type="radio" name="q11" value="wrong3"> 20 days</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 -->
    <div class="quiz-question">
      <h3>Question 12: Indoor Temperature</h3>
      <p>How does indoor temperature typically compare to outdoor temperature in VECTRI?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q12" value="wrong1"> Always cooler than outdoor</label>
        <label><input type="radio" name="q12" value="wrong2"> Always warmer than outdoor</label>
        <label><input type="radio" name="q12" value="correct"> Warmer when cool outside, potentially cooler when very hot outside</label>
        <label><input type="radio" name="q12" value="wrong3"> Exactly the same as outdoor</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 -->
    <div class="quiz-question">
      <h3>Question 13: Human Biting Rate</h3>
      <p>What happens to mosquito biting behavior at LOW human population densities?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q13" value="correct"> Many bites go to animals (zoophilic feeding)</label>
        <label><input type="radio" name="q13" value="wrong1"> All bites are on humans</label>
        <label><input type="radio" name="q13" value="wrong2"> Mosquitoes don't bite at all</label>
        <label><input type="radio" name="q13" value="wrong3"> Biting rate increases dramatically</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 -->
    <div class="quiz-question">
      <h3>Question 14: Daily EIR</h3>
      <p>The daily Entomological Inoculation Rate (EIR) is calculated as:</p>
      <div class="quiz-options">
        <label><input type="radio" name="q14" value="wrong1"> Number of mosquitoes per person</label>
        <label><input type="radio" name="q14" value="correct"> Human biting rate × CSPR (fraction of infectious mosquitoes)</label>
        <label><input type="radio" name="q14" value="wrong2"> Larval density × survival rate</label>
        <label><input type="radio" name="q14" value="wrong3"> Total mosquito population / human population</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 -->
    <div class="quiz-question">
      <h3>Question 15: Immunity Dynamics</h3>
      <p>At an annual EIR of ~100, approximately what percentage of individuals become clinically immune?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q15" value="wrong1"> 50%</label>
        <label><input type="radio" name="q15" value="wrong2"> 75%</label>
        <label><input type="radio" name="q15" value="correct"> 95%</label>
        <label><input type="radio" name="q15" value="wrong3"> 100%</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 -->
    <div class="quiz-question">
      <h3>Question 16: Surface Hydrology Components - Multiple Select</h3>
      <p><strong>Select ALL</strong> components that contribute to total breeding area (w):</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q16" value="correct1"> Permanent water bodies (w_perm)</label>
        <label><input type="checkbox" name="q16" value="correct2"> Temporary rainfall-driven ponds (w_pond)</label>
        <label><input type="checkbox" name="q16" value="wrong1"> Indoor water containers</label>
        <label><input type="checkbox" name="q16" value="wrong2"> Atmospheric moisture</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
    </div>

    <!-- Question 17 -->
    <div class="quiz-question">
      <h3>Question 17: Water Balance</h3>
      <p>What causes temporary ponds to shrink in the VECTRI water balance model?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q17" value="wrong1"> Only evaporation</label>
        <label><input type="radio" name="q17" value="wrong2"> Only infiltration</label>
        <label><input type="radio" name="q17" value="correct"> Both evaporation and infiltration</label>
        <label><input type="radio" name="q17" value="wrong3"> Human water extraction</label>
      </div>
      <div class="feedback" id="feedback-q17"></div>
    </div>

    <!-- Question 18 -->
    <div class="quiz-question">
      <h3>Question 18: Carrying Capacity Effect</h3>
      <p>If w (breeding area fraction) is SMALL, what happens to larval survival?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q18" value="wrong1"> Survival increases due to less competition</label>
        <label><input type="radio" name="q18" value="correct"> Survival decreases due to stronger crowding</label>
        <label><input type="radio" name="q18" value="wrong2"> Survival is unaffected</label>
        <label><input type="radio" name="q18" value="wrong3"> Development rate increases</label>
      </div>
      <div class="feedback" id="feedback-q18"></div>
    </div>

    <!-- Question 19 -->
    <div class="quiz-question">
      <h3>Question 19: Semi-Arid vs Humid Regions</h3>
      <p>In semi-arid regions with intense but short rainstorms, what typically limits transmission?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q19" value="wrong1"> Too much water available</label>
        <label><input type="radio" name="q19" value="correct"> Ponds dry out before larvae can complete development</label>
        <label><input type="radio" name="q19" value="wrong2"> Temperature is always too low</label>
        <label><input type="radio" name="q19" value="wrong3"> No human population present</label>
      </div>
      <div class="feedback" id="feedback-q19"></div>
    </div>

    <!-- Question 20 -->
    <div class="quiz-question">
      <h3>Question 20: True or False</h3>
      <p>In VECTRI, egg and pupa stages are temperature-dependent with variable durations.</p>
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
  const quizForm = document.getElementById('vectri-components-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>Water temperature</strong> is correct! Larval development is primarily temperature-driven via a degree-day relationship.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>90.9 degree-days</strong> is correct! Jepson (1947) gives K_L = 90.9, leading to faster development than Bayoh & Lindsay (200).'
    },
    q3: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>Crowding, flushing, lethal temperature, and base survival</strong> all affect larval mortality. Wind and lunar phase are not modeled.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>0.825</strong> is correct! This is the base daily survival probability in good conditions without crowding or flushing.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>Early larvae</strong> is correct! Early-stage larvae (L_f ≈ 0) are most vulnerable to rainfall flushing. Late larvae (L_f = 1) have no extra flushing mortality.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>Blood meal to egg laying</strong> is correct! The gonotrophic cycle is the time from blood feeding to oviposition.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>80 female eggs</strong> is correct! Each cycle produces ~80 female eggs (160 total with 50:50 sex ratio).'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ Correct! The <strong>EIP</strong> is the time for the malaria parasite to develop inside the mosquito from gametocyte ingestion to infectious sporozoites.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ Correct! At cooler temperatures, the EIP becomes much longer (~28 days at 20°C vs ~12 days at 25°C), often exceeding mosquito lifespan.'
    },
    q10: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! Survival <strong>depends on temperature</strong>, follows a <strong>bell-shaped curve (Martens II)</strong>, with <strong>highest survival at mid-temperatures</strong>.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>10 days</strong> is correct! Expected lifespan ≈ 1/(1-P_surv) = 1/(1-0.9) = 10 days.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ Correct! Indoor temperature is <strong>warmer when cool outside</strong> and potentially <strong>cooler when very hot</strong> (thick walls, shading).'
    },
    q13: {
      correct: 'correct',
      feedback: '✅ Correct! At low human densities, mosquitoes exhibit <strong>zoophilic feeding</strong> - many bites go to animals instead of humans.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ Correct! Daily EIR = <strong>human biting rate × CSPR</strong>, where CSPR is the fraction of infectious mosquitoes.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>95%</strong> is correct! At an annual EIR of ~100, approximately 95% of individuals become clinically immune.'
    },
    q16: {
      correct: ['correct1', 'correct2'],
      feedback: '✅ Correct! Total breeding area w = <strong>w_perm + w_pond</strong>, consisting of permanent and temporary water bodies.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ Correct! Ponds shrink via <strong>both evaporation and infiltration</strong>, with infiltration typically being larger (~200-250 mm/day).'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ Correct! When w is small, the same larval biomass means <strong>stronger crowding and lower survival</strong> (1 - M_L/(w·M_Lmax)).'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ Correct! In semi-arid regions, <strong>ponds dry out before larvae complete development</strong>, limiting transmission despite high rainfall intensity.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>False</strong> is correct! Egg and pupa stages are each fixed at 1 day (temperature-independent) because the daily time step is too coarse.'
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
      
      if (qName === 'q3' || qName === 'q10' || qName === 'q16') {
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
      message = '🎉 Outstanding! You have an excellent understanding of VECTRI model components. You\'re ready to work with the model!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid grasp of the model components. Review the questions you missed and you\'ll be all set.';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep studying! Review the model components documentation and retake the quiz.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Review the VECTRI model components carefully and try again. Focus on understanding the biological and physical processes.';
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
  border-left: 4px solid #00897b;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #4db6ac;
}

.quiz-question h3 {
  color: #00897b;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-question h3 {
  color: #4db6ac;
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
  border-color: #00897b;
}

[data-md-color-scheme="slate"] .quiz-options label {
  border-color: #455a64;
}

[data-md-color-scheme="slate"] .quiz-options label:hover {
  background: #37474f;
  border-color: #4db6ac;
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
  color: #00897b;
  margin-top: 0;
}

[data-md-color-scheme="slate"] .quiz-results h2 {
  color: #4db6ac;
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
  color: #00897b;
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

- Read each question carefully - many involve specific numerical values
- Think about the biological and physical processes before answering
- For multiple select questions, select ALL correct answers
- Remember the interconnections between components (e.g., temperature affects development, survival, and EIP)
- Review your answers before submitting
- Check the feedback to deepen your understanding
- Retake the quiz to improve your score!

---

## 📚 Additional Resources

- [VECTRI Model Components Guide](../day1/06-vectri_model_components_larvae_to_hydrology.md)
- [VECTRI Introduction](../day1/03-vectri-intro.md)
- Original VECTRI publications (Tompkins & Ermert 2013, and references therein)
- Workshop Lab Exercises

---

## 🚀 Key Concepts Covered

This quiz tests your understanding of:

1. **Larval Development** - Temperature-driven degree-day relationships
2. **Larval Mortality** - Crowding, flushing, and temperature limits
3. **Gonotrophic Cycle** - Blood meal to egg laying
4. **Sporogonic Cycle** - Parasite development in mosquitoes (EIP)
5. **Vector Survival** - Temperature-dependent adult mortality
6. **Indoor Temperatures** - Mosquito resting behavior
7. **Host Community** - Biting rates and EIR
8. **Immunity** - Acquisition and loss with exposure
9. **Surface Hydrology** - Rainfall-driven breeding habitat dynamics

---

**Good luck! Understanding these components is key to using VECTRI effectively!** 🦟🔬


# Linux Commands Interactive Quiz

Test your Linux command knowledge with this interactive quiz! Select your answers and get instant scoring.

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

  <form id="linux-quiz">
    
    <!-- Question 1 -->
    <div class="quiz-question">
      <h3>Question 1: Print Working Directory</h3>
      <p>Which command shows your current location in the file system?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q1" value="wrong1"> whereami</label>
        <label><input type="radio" name="q1" value="correct"> pwd</label>
        <label><input type="radio" name="q1" value="wrong2"> cwd</label>
        <label><input type="radio" name="q1" value="wrong3"> location</label>
      </div>
      <div class="feedback" id="feedback-q1"></div>
    </div>

    <!-- Question 2 -->
    <div class="quiz-question">
      <h3>Question 2: Listing Files</h3>
      <p>Which command option shows file sizes in human-readable format (KB, MB, GB)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q2" value="wrong1"> ls -s</label>
        <label><input type="radio" name="q2" value="wrong2"> ls -r</label>
        <label><input type="radio" name="q2" value="correct"> ls -lh</label>
        <label><input type="radio" name="q2" value="wrong3"> ls -size</label>
      </div>
      <div class="feedback" id="feedback-q2"></div>
    </div>

    <!-- Question 3 -->
    <div class="quiz-question">
      <h3>Question 3: Navigation</h3>
      <p>What does <code>cd ..</code> do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q3" value="wrong1"> Goes to the home directory</label>
        <label><input type="radio" name="q3" value="correct"> Goes up one directory level</label>
        <label><input type="radio" name="q3" value="wrong2"> Goes to the previous directory</label>
        <label><input type="radio" name="q3" value="wrong3"> Stays in current directory</label>
      </div>
      <div class="feedback" id="feedback-q3"></div>
    </div>

    <!-- Question 4 -->
    <div class="quiz-question">
      <h3>Question 4: Creating Directories</h3>
      <p>Which command creates nested directories (parent folders if they don't exist)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q4" value="wrong1"> mkdir -r a/b/c</label>
        <label><input type="radio" name="q4" value="correct"> mkdir -p a/b/c</label>
        <label><input type="radio" name="q4" value="wrong2"> mkdir --recursive a/b/c</label>
        <label><input type="radio" name="q4" value="wrong3"> mkdir -f a/b/c</label>
      </div>
      <div class="feedback" id="feedback-q4"></div>
    </div>

    <!-- Question 5 -->
    <div class="quiz-question">
      <h3>Question 5: File Operations - Multiple Select</h3>
      <p><strong>Select ALL</strong> commands that can be used to view file contents:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q5" value="correct1"> cat</label>
        <label><input type="checkbox" name="q5" value="correct2"> less</label>
        <label><input type="checkbox" name="q5" value="wrong1"> ls</label>
        <label><input type="checkbox" name="q5" value="correct3"> head</label>
        <label><input type="checkbox" name="q5" value="correct4"> tail</label>
        <label><input type="checkbox" name="q5" value="wrong2"> cd</label>
      </div>
      <div class="feedback" id="feedback-q5"></div>
    </div>

    <!-- Question 6 -->
    <div class="quiz-question">
      <h3>Question 6: Removing Files</h3>
      <p>What does <code>rm -rf</code> do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q6" value="wrong1"> Removes a single file</label>
        <label><input type="radio" name="q6" value="wrong2"> Renames files</label>
        <label><input type="radio" name="q6" value="correct"> Force removes directories and files without confirmation</label>
        <label><input type="radio" name="q6" value="wrong3"> Recovers deleted files</label>
      </div>
      <div class="feedback" id="feedback-q6"></div>
    </div>

    <!-- Question 7 -->
    <div class="quiz-question">
      <h3>Question 7: Copying Files</h3>
      <p>How do you copy a folder and all its contents?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q7" value="wrong1"> cp folder1 folder2</label>
        <label><input type="radio" name="q7" value="correct"> cp -r folder1 folder2</label>
        <label><input type="radio" name="q7" value="wrong2"> cp -a folder1 folder2</label>
        <label><input type="radio" name="q7" value="wrong3"> copy folder1 folder2</label>
      </div>
      <div class="feedback" id="feedback-q7"></div>
    </div>

    <!-- Question 8 -->
    <div class="quiz-question">
      <h3>Question 8: Finding Files</h3>
      <p>Which command searches for text within files?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q8" value="wrong1"> find</label>
        <label><input type="radio" name="q8" value="correct"> grep</label>
        <label><input type="radio" name="q8" value="wrong2"> search</label>
        <label><input type="radio" name="q8" value="wrong3"> locate</label>
      </div>
      <div class="feedback" id="feedback-q8"></div>
    </div>

    <!-- Question 9 -->
    <div class="quiz-question">
      <h3>Question 9: Redirection</h3>
      <p>What does the <code>></code> symbol do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q9" value="wrong1"> Appends output to a file</label>
        <label><input type="radio" name="q9" value="correct"> Writes output to a file (overwrites existing content)</label>
        <label><input type="radio" name="q9" value="wrong2"> Reads input from a file</label>
        <label><input type="radio" name="q9" value="wrong3"> Pipes output to another command</label>
      </div>
      <div class="feedback" id="feedback-q9"></div>
    </div>

    <!-- Question 10 -->
    <div class="quiz-question">
      <h3>Question 10: Environment Variables</h3>
      <p>How do you set an environment variable permanently in bash?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q10" value="wrong1"> export MYVAR="value" in the terminal</label>
        <label><input type="radio" name="q10" value="correct"> Add export MYVAR="value" to ~/.bashrc and run source ~/.bashrc</label>
        <label><input type="radio" name="q10" value="wrong2"> set MYVAR="value"</label>
        <label><input type="radio" name="q10" value="wrong3"> MYVAR="value" in the terminal</label>
      </div>
      <div class="feedback" id="feedback-q10"></div>
    </div>

    <!-- Question 11 -->
    <div class="quiz-question">
      <h3>Question 11: Git Commands</h3>
      <p>Which command is used to download a repository for the first time?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q11" value="wrong1"> git pull</label>
        <label><input type="radio" name="q11" value="wrong2"> git download</label>
        <label><input type="radio" name="q11" value="correct"> git clone</label>
        <label><input type="radio" name="q11" value="wrong3"> git fetch</label>
      </div>
      <div class="feedback" id="feedback-q11"></div>
    </div>

    <!-- Question 12 -->
    <div class="quiz-question">
      <h3>Question 12: Permissions</h3>
      <p>What does <code>chmod +x script.sh</code> do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q12" value="wrong1"> Deletes the script</label>
        <label><input type="radio" name="q12" value="correct"> Makes the script executable</label>
        <label><input type="radio" name="q12" value="wrong2"> Encrypts the script</label>
        <label><input type="radio" name="q12" value="wrong3"> Copies the script</label>
      </div>
      <div class="feedback" id="feedback-q12"></div>
    </div>

    <!-- Question 13 -->
    <div class="quiz-question">
      <h3>Question 13: Process Management - Multiple Select</h3>
      <p><strong>Select ALL</strong> commands that can terminate processes:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q13" value="correct1"> kill</label>
        <label><input type="checkbox" name="q13" value="wrong1"> stop</label>
        <label><input type="checkbox" name="q13" value="correct2"> pkill</label>
        <label><input type="checkbox" name="q13" value="correct3"> kill -9</label>
        <label><input type="checkbox" name="q13" value="wrong2"> terminate</label>
        <label><input type="checkbox" name="q13" value="wrong3"> end</label>
      </div>
      <div class="feedback" id="feedback-q13"></div>
    </div>

    <!-- Question 14 -->
    <div class="quiz-question">
      <h3>Question 14: Disk Usage</h3>
      <p>Which command shows disk space usage in human-readable format?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q14" value="wrong1"> disk -h</label>
        <label><input type="radio" name="q14" value="correct"> df -h</label>
        <label><input type="radio" name="q14" value="wrong2"> du -h</label>
        <label><input type="radio" name="q14" value="wrong3"> space -h</label>
      </div>
      <div class="feedback" id="feedback-q14"></div>
    </div>

    <!-- Question 15 -->
    <div class="quiz-question">
      <h3>Question 15: Archiving Files</h3>
      <p>Which command extracts a gzipped tarball?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q15" value="wrong1"> tar -czvf file.tar.gz</label>
        <label><input type="radio" name="q15" value="correct"> tar -xzvf file.tar.gz</label>
        <label><input type="radio" name="q15" value="wrong2"> untar file.tar.gz</label>
        <label><input type="radio" name="q15" value="wrong3"> extract file.tar.gz</label>
      </div>
      <div class="feedback" id="feedback-q15"></div>
    </div>

    <!-- Question 16 -->
    <div class="quiz-question">
      <h3>Question 16: Symbolic Links</h3>
      <p>What command creates a symbolic link?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q16" value="wrong1"> link -s source target</label>
        <label><input type="radio" name="q16" value="correct"> ln -s source target</label>
        <label><input type="radio" name="q16" value="wrong2"> symlink source target</label>
        <label><input type="radio" name="q16" value="wrong3"> mklink source target</label>
      </div>
      <div class="feedback" id="feedback-q16"></div>
    </div>

    <!-- Question 17 -->
    <div class="quiz-question">
      <h3>Question 17: Pipes</h3>
      <p>What does the pipe symbol <code>|</code> do?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q17" value="wrong1"> Writes output to a file</label>
        <label><input type="radio" name="q17" value="wrong2"> Appends output to a file</label>
        <label><input type="radio" name="q17" value="correct"> Sends output of one command as input to another</label>
        <label><input type="radio" name="q17" value="wrong3"> Separates commands to run sequentially</label>
      </div>
      <div class="feedback" id="feedback-q17"></div>
    </div>

    <!-- Question 18 -->
    <div class="quiz-question">
      <h3>Question 18: Hidden Files</h3>
      <p>Which command option shows hidden files (those starting with a dot)?</p>
      <div class="quiz-options">
        <label><input type="radio" name="q18" value="wrong1"> ls -h</label>
        <label><input type="radio" name="q18" value="correct"> ls -a</label>
        <label><input type="radio" name="q18" value="wrong2"> ls -hidden</label>
        <label><input type="radio" name="q18" value="wrong3"> ls --all-files</label>
      </div>
      <div class="feedback" id="feedback-q18"></div>
    </div>

    <!-- Question 19 -->
    <div class="quiz-question">
      <h3>Question 19: Downloading Files - Multiple Select</h3>
      <p><strong>Select ALL</strong> commands that can download files from the web:</p>
      <div class="quiz-options">
        <label><input type="checkbox" name="q19" value="correct1"> wget</label>
        <label><input type="checkbox" name="q19" value="correct2"> curl -O</label>
        <label><input type="checkbox" name="q19" value="wrong1"> download</label>
        <label><input type="checkbox" name="q19" value="wrong2"> get</label>
        <label><input type="checkbox" name="q19" value="wrong3"> fetch</label>
      </div>
      <div class="feedback" id="feedback-q19"></div>
    </div>

    <!-- Question 20 -->
    <div class="quiz-question">
      <h3>Question 20: True or False</h3>
      <p>The command <code>rm -rf /</code> is safe to run and will only delete files in the current directory.</p>
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
  const quizForm = document.getElementById('linux-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>pwd</strong> is correct! It stands for "Print Working Directory" and shows your current location.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>ls -lh</strong> is correct! The -l gives long format and -h makes sizes human-readable (KB, MB, GB).'
    },
    q3: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>cd ..</strong> moves up one directory level in the file system hierarchy.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>mkdir -p</strong> is correct! The -p flag creates parent directories as needed.'
    },
    q5: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ Correct! <strong>cat, less, head, tail</strong> all view file contents. ls lists files, cd changes directory.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>rm -rf</strong> force removes directories/files without prompts. Use with extreme caution!'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>cp -r</strong> is correct! The -r flag means recursive, copying folders and all contents.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ <strong>grep</strong> is correct! It searches for text patterns within files.'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ Correct! The <strong>></strong> symbol redirects output to a file and overwrites existing content.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ Correct! Adding to <strong>~/.bashrc</strong> and sourcing it makes variables permanent across sessions.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>git clone</strong> is correct! It downloads a repository for the first time.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ Correct! <strong>chmod +x</strong> makes a file executable so you can run it as a program.'
    },
    q13: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ Correct! <strong>kill, pkill, kill -9</strong> all terminate processes. The others are not valid commands.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>df -h</strong> is correct! It shows Disk Free space in human-readable format.'
    },
    q15: {
      correct: 'correct',
      feedback: '✅ <strong>tar -xzvf</strong> is correct! x=extract, z=gzip, v=verbose, f=file.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>ln -s</strong> is correct! It creates a symbolic link (soft link) to a file or directory.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ Correct! The <strong>pipe |</strong> sends output from one command as input to another command.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ <strong>ls -a</strong> is correct! The -a flag shows All files including hidden ones.'
    },
    q19: {
      correct: ['correct1', 'correct2'],
      feedback: '✅ Correct! <strong>wget</strong> and <strong>curl -O</strong> both download files from URLs.'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>False</strong> is correct! rm -rf / is EXTREMELY DANGEROUS and would try to delete your entire system!'
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
      
      if (qName === 'q5' || qName === 'q13' || qName === 'q19') {
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
      message = '🎉 Outstanding! You have mastered Linux commands for VECTRI. You\'re ready to work efficiently in the terminal!';
      color = '#4caf50';
    } else if (percentage >= 70) {
      grade = 'B (Good)';
      message = '👍 Good work! You have a solid grasp of Linux basics. Review the questions you missed and you\'ll be all set.';
      color = '#8bc34a';
    } else if (percentage >= 50) {
      grade = 'C (Fair)';
      message = '📚 Not bad, but keep practicing! Review the Linux commands guide and retake the quiz.';
      color = '#ffc107';
    } else {
      grade = 'D (Needs Work)';
      message = '💪 Keep learning! Review the basic Linux commands tutorial and practice in your terminal. Don\'t worry - practice makes perfect!';
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
  border-left: 4px solid #ff6f00;
}

[data-md-color-scheme="slate"] .quiz-question {
  background: #263238;
  border-left-color: #ffb74d;
}

.quiz-question h3 {
  color: #ff6f00;
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
  border-color: #ff6f00;
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
  color: #ff6f00;
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
  color: #ff6f00;
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
- Think about what each command does before answering
- For multiple select questions, select ALL correct answers
- Remember that Linux commands are case-sensitive
- Review your answers before submitting
- Check the feedback to understand concepts better
- Retake the quiz to improve your score!

---

## 📚 Additional Resources

- [Basic Linux Commands Guide](../day2/04-basic-linux-commands.md)
- [Linux Command Line Basics - Ubuntu Tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)
- [The Linux Command Line (Free Book)](http://linuxcommand.org/tlcl.php)
- Practice in your terminal every day!

---

## 🚀 Next Steps

After mastering these commands:

1. Practice in your own terminal
2. Try the hands-on exercises in the [Basic Linux Commands guide](../day2/04-basic-linux-commands.md)
3. Set up your VECTRI environment
4. Explore more advanced commands like `awk`, `sed`, and shell scripting

---

**Good luck! Remember: The best way to learn Linux is to use it!** 🐧


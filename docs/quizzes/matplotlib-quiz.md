# Matplotlib Quiz

Test your understanding of Matplotlib plotting and visualization techniques!

---

<style>
  .quiz-container {
    max-width: 900px;
    margin: 2rem auto;
    font-family: 'Roboto', sans-serif;
  }
  
  .question-block {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
    border-color: #f093fb;
    background-color: #fef5ff;
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
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
  }
  
  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(240, 147, 251, 0.4);
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
    color: #f093fb;
    margin-bottom: 1rem;
  }
  
  .score-display {
    font-size: 2.5rem;
    font-weight: bold;
    color: #f5576c;
    margin: 1rem 0;
  }
  
  .note {
    background-color: #fff3cd;
    border-left: 4px solid #f093fb;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
  }
</style>

<div class="quiz-container">
  <div class="note">
    <strong>📝 Note:</strong> This quiz contains 20 questions including multiple choice and multiple selection questions. Some questions may have more than one correct answer. Select all that apply for those questions.
  </div>

  <form id="matplotlib-quiz">
    
    <!-- Question 1 -->
    <div class="question-block">
      <h3>1. Which function creates a new figure in Matplotlib?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q1" value="correct">
          plt.figure()
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong1">
          plt.create()
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong2">
          plt.new_figure()
        </label>
        <label class="option-label">
          <input type="radio" name="q1" value="wrong3">
          plt.plot()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 2 -->
    <div class="question-block">
      <h3>2. What does plt.show() do?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q2" value="wrong1">
          Saves the figure to a file
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="correct">
          Displays the figure on screen
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong2">
          Creates a new figure
        </label>
        <label class="option-label">
          <input type="radio" name="q2" value="wrong3">
          Closes all figures
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 3 -->
    <div class="question-block">
      <h3>3. Which functions add labels and titles to a plot? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct1">
          plt.xlabel()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct2">
          plt.ylabel()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="correct3">
          plt.title()
        </label>
        <label class="option-label">
          <input type="checkbox" name="q3" value="wrong1">
          plt.label()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 4 -->
    <div class="question-block">
      <h3>4. What type of plot is created with plt.scatter()?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q4" value="wrong1">
          Line plot
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="correct">
          Scatter plot
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong2">
          Bar chart
        </label>
        <label class="option-label">
          <input type="radio" name="q4" value="wrong3">
          Histogram
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 5 -->
    <div class="question-block">
      <h3>5. Which function is used to create a histogram?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q5" value="wrong1">
          plt.bar()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="correct">
          plt.hist()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong2">
          plt.histogram()
        </label>
        <label class="option-label">
          <input type="radio" name="q5" value="wrong3">
          plt.distribution()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 6 -->
    <div class="question-block">
      <h3>6. What is the difference between plt.bar() and plt.barh()?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q6" value="wrong1">
          No difference, they're the same
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="correct">
          plt.bar() creates vertical bars, plt.barh() creates horizontal bars
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong2">
          plt.bar() is for single series, plt.barh() is for multiple series
        </label>
        <label class="option-label">
          <input type="radio" name="q6" value="wrong3">
          plt.barh() is deprecated
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 7 -->
    <div class="question-block">
      <h3>7. Which function creates a box plot?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q7" value="wrong1">
          plt.box()
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="correct">
          plt.boxplot()
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong2">
          plt.violin()
        </label>
        <label class="option-label">
          <input type="radio" name="q7" value="wrong3">
          plt.whisker()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 8 -->
    <div class="question-block">
      <h3>8. What does the alpha parameter control in plotting functions?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q8" value="wrong1">
          Line width
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="correct">
          Transparency (0=fully transparent, 1=fully opaque)
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="wrong2">
          Marker size
        </label>
        <label class="option-label">
          <input type="radio" name="q8" value="wrong3">
          Color intensity
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 9 -->
    <div class="question-block">
      <h3>9. Which function is used to display 2D arrays as images or heatmaps?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q9" value="wrong1">
          plt.heatmap()
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="correct">
          plt.imshow()
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong2">
          plt.image()
        </label>
        <label class="option-label">
          <input type="radio" name="q9" value="wrong3">
          plt.array()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 10 -->
    <div class="question-block">
      <h3>10. What does plt.colorbar() add to a plot?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q10" value="wrong1">
          A color legend
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="correct">
          A color scale showing the mapping of values to colors
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="wrong2">
          A colored grid
        </label>
        <label class="option-label">
          <input type="radio" name="q10" value="wrong3">
          A color palette selector
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 11 -->
    <div class="question-block">
      <h3>11. How do you create multiple subplots in a single figure?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q11" value="wrong1">
          plt.multi_plot()
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="correct">
          plt.subplots()
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong2">
          plt.panels()
        </label>
        <label class="option-label">
          <input type="radio" name="q11" value="wrong3">
          plt.grid()
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 12 -->
    <div class="question-block">
      <h3>12. What does ax.twinx() do?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q12" value="wrong1">
          Creates a mirror image of the plot
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="correct">
          Creates a second y-axis sharing the same x-axis
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong2">
          Duplicates the current axes
        </label>
        <label class="option-label">
          <input type="radio" name="q12" value="wrong3">
          Inverts the x-axis
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 13 -->
    <div class="question-block">
      <h3>13. Which parameters are commonly used in plt.subplots()? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q13" value="correct1">
          nrows (number of rows)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q13" value="correct2">
          ncols (number of columns)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q13" value="correct3">
          figsize (figure size)
        </label>
        <label class="option-label">
          <input type="checkbox" name="q13" value="wrong1">
          nplots (number of plots)
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 14 -->
    <div class="question-block">
      <h3>14. What does plt.tight_layout() do?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q14" value="wrong1">
          Compresses the figure vertically
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="correct">
          Automatically adjusts subplot parameters to prevent overlapping
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong2">
          Removes all white space
        </label>
        <label class="option-label">
          <input type="radio" name="q14" value="wrong3">
          Makes lines thinner
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 15 -->
    <div class="question-block">
      <h3>15. Which file formats can Matplotlib save figures to? (Select all that apply)</h3>
      <div class="options">
        <label class="option-label">
          <input type="checkbox" name="q15" value="correct1">
          PNG
        </label>
        <label class="option-label">
          <input type="checkbox" name="q15" value="correct2">
          PDF
        </label>
        <label class="option-label">
          <input type="checkbox" name="q15" value="correct3">
          SVG
        </label>
        <label class="option-label">
          <input type="checkbox" name="q15" value="correct4">
          EPS
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 16 -->
    <div class="question-block">
      <h3>16. What parameter in plt.savefig() controls the resolution of the saved figure?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q16" value="wrong1">
          resolution
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="correct">
          dpi
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong2">
          quality
        </label>
        <label class="option-label">
          <input type="radio" name="q16" value="wrong3">
          pixels
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 17 -->
    <div class="question-block">
      <h3>17. What does the extent parameter in plt.imshow() control?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q17" value="wrong1">
          The size of the figure
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="correct">
          The coordinate bounds of the image (left, right, bottom, top)
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="wrong2">
          The zoom level
        </label>
        <label class="option-label">
          <input type="radio" name="q17" value="wrong3">
          The color range
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 18 -->
    <div class="question-block">
      <h3>18. What is GridSpec used for?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q18" value="wrong1">
          Creating grid lines on plots
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="correct">
          Creating complex subplot layouts with varying sizes
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong2">
          Specifying coordinate grids for data
        </label>
        <label class="option-label">
          <input type="radio" name="q18" value="wrong3">
          Setting grid spacing in plots
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 19 -->
    <div class="question-block">
      <h3>19. What does the bins parameter control in plt.hist()?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q19" value="wrong1">
          The height of bars
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="correct">
          The number or edges of bins for grouping data
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong2">
          The width of the figure
        </label>
        <label class="option-label">
          <input type="radio" name="q19" value="wrong3">
          The color scheme
        </label>
      </div>
      <div class="feedback"></div>
    </div>

    <!-- Question 20 -->
    <div class="question-block">
      <h3>20. What is the purpose of plt.grid(True)?</h3>
      <div class="options">
        <label class="option-label">
          <input type="radio" name="q20" value="wrong1">
          Creates a subplot grid
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="correct">
          Adds grid lines to the plot for easier reading
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong2">
          Aligns multiple plots
        </label>
        <label class="option-label">
          <input type="radio" name="q20" value="wrong3">
          Creates a data grid
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
  const quizForm = document.getElementById('matplotlib-quiz');
  const submitBtn = document.getElementById('submit-btn');
  const resetBtn = document.getElementById('reset-btn');
  const resultsSection = document.getElementById('quiz-results');
  const reviewBtn = document.getElementById('review-btn');
  const retakeBtn = document.getElementById('retake-btn');

  // Correct answers and feedback
  const answers = {
    q1: {
      correct: 'correct',
      feedback: '✅ <strong>plt.figure()</strong> is correct! This function creates a new figure object.'
    },
    q2: {
      correct: 'correct',
      feedback: '✅ <strong>Displays the figure on screen</strong> is correct! plt.show() renders and displays all active figures.'
    },
    q3: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>plt.xlabel(), plt.ylabel(), and plt.title()</strong> are all correct! These functions add labels and titles to plots.'
    },
    q4: {
      correct: 'correct',
      feedback: '✅ <strong>Scatter plot</strong> is correct! plt.scatter() creates scatter plots showing relationships between two variables.'
    },
    q5: {
      correct: 'correct',
      feedback: '✅ <strong>plt.hist()</strong> is correct! This function creates histograms to visualize data distributions.'
    },
    q6: {
      correct: 'correct',
      feedback: '✅ <strong>plt.bar() creates vertical bars, plt.barh() creates horizontal bars</strong> is correct! The "h" stands for horizontal.'
    },
    q7: {
      correct: 'correct',
      feedback: '✅ <strong>plt.boxplot()</strong> is correct! This function creates box-and-whisker plots for statistical visualization.'
    },
    q8: {
      correct: 'correct',
      feedback: '✅ <strong>Transparency</strong> is correct! Alpha ranges from 0 (fully transparent) to 1 (fully opaque).'
    },
    q9: {
      correct: 'correct',
      feedback: '✅ <strong>plt.imshow()</strong> is correct! This function displays 2D arrays as images, heatmaps, or Hovmöller diagrams.'
    },
    q10: {
      correct: 'correct',
      feedback: '✅ <strong>A color scale showing the mapping of values to colors</strong> is correct! Colorbars help interpret heatmaps and images.'
    },
    q11: {
      correct: 'correct',
      feedback: '✅ <strong>plt.subplots()</strong> is correct! This function creates a figure with multiple subplots in a grid layout.'
    },
    q12: {
      correct: 'correct',
      feedback: '✅ <strong>Creates a second y-axis sharing the same x-axis</strong> is correct! Useful for plotting two variables with different scales.'
    },
    q13: {
      correct: ['correct1', 'correct2', 'correct3'],
      feedback: '✅ <strong>nrows, ncols, and figsize</strong> are all correct! These parameters control the subplot grid layout and figure dimensions.'
    },
    q14: {
      correct: 'correct',
      feedback: '✅ <strong>Automatically adjusts subplot parameters to prevent overlapping</strong> is correct! tight_layout() optimizes spacing.'
    },
    q15: {
      correct: ['correct1', 'correct2', 'correct3', 'correct4'],
      feedback: '✅ <strong>PNG, PDF, SVG, and EPS</strong> are all correct! Matplotlib supports many raster and vector formats.'
    },
    q16: {
      correct: 'correct',
      feedback: '✅ <strong>dpi</strong> is correct! DPI (dots per inch) controls the resolution. Higher values = higher resolution.'
    },
    q17: {
      correct: 'correct',
      feedback: '✅ <strong>The coordinate bounds of the image</strong> is correct! extent=[left, right, bottom, top] sets axis labels for spatial data.'
    },
    q18: {
      correct: 'correct',
      feedback: '✅ <strong>Creating complex subplot layouts with varying sizes</strong> is correct! GridSpec allows flexible subplot arrangements.'
    },
    q19: {
      correct: 'correct',
      feedback: '✅ <strong>The number or edges of bins for grouping data</strong> is correct! bins can be an integer (number of bins) or array (bin edges).'
    },
    q20: {
      correct: 'correct',
      feedback: '✅ <strong>Adds grid lines to the plot</strong> is correct! Grid lines help read values from the plot more easily.'
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
      resultMessage.textContent = '🎉 Excellent! You have mastered Matplotlib plotting!';
    } else if (percentage >= 75) {
      resultMessage.textContent = '👍 Great work! You have a solid understanding of Matplotlib.';
    } else if (percentage >= 60) {
      resultMessage.textContent = '✅ Good effort! Review the material and try again to improve.';
    } else {
      resultMessage.textContent = '📚 Keep practicing! Review the tutorial and examples.';
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


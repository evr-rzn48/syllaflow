import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Enhanced SyllaFlow Webapp with Expanded Features
// Integrating larger word canvas, comprehensive library, and KDP generation

const EnhancedSyllaFlow = () => {
  const [gameState, setGameState] = useState('welcome');
  const [currentPuzzle, setCurrentPuzzle] = useState(null);
  const [foundWords, setFoundWords] = useState([]);
  const [selectedCells, setSelectedCells] = useState([]);
  const [isSelecting, setIsSelecting] = useState(false);
  const [wordLibrary, setWordLibrary] = useState(null);
  const [canvasSize, setCanvasSize] = useState('medium');
  const [difficulty, setDifficulty] = useState('beginner');
  const [theme, setTheme] = useState('mindfulness_core');
  const [journalPrompts, setJournalPrompts] = useState([]);
  const [meditationGuide, setMeditationGuide] = useState('');
  const [progress, setProgress] = useState({ level: 1, experience: 0, streak: 0 });
  const [kdpMode, setKdpMode] = useState(false);
  const [generatedBooks, setGeneratedBooks] = useState([]);
  const gridRef = useRef(null);

  // Canvas size configurations
  const canvasSizes = {
    small: { width: 12, height: 12, cellSize: 35 },
    medium: { width: 15, height: 15, cellSize: 32 },
    large: { width: 18, height: 18, cellSize: 28 },
    extra_large: { width: 20, height: 20, cellSize: 25 },
    massive: { width: 25, height: 25, cellSize: 20 }
  };

  // Enhanced word library with comprehensive categories
  const enhancedWordLibrary = {
    mindfulness_core: [
      { word: 'MEDITATION', syllables: ['MED', 'I', 'TA', 'TION'], definition: 'A practice of focused attention to achieve mental clarity', prompt: 'How does stillness speak to you?' },
      { word: 'AWARENESS', syllables: ['A', 'WARE', 'NESS'], definition: 'The quality of being conscious and mindful', prompt: 'What are you becoming aware of right now?' },
      { word: 'PRESENCE', syllables: ['PRES', 'ENCE'], definition: 'The state of being fully here and now', prompt: 'Where do you feel most present?' },
      { word: 'COMPASSION', syllables: ['COM', 'PAS', 'SION'], definition: 'Sympathetic concern for the sufferings of others', prompt: 'How can you extend compassion to yourself today?' },
      { word: 'GRATITUDE', syllables: ['GRAT', 'I', 'TUDE'], definition: 'The quality of being thankful', prompt: 'What fills your heart with gratitude?' },
      { word: 'MINDFULNESS', syllables: ['MIND', 'FUL', 'NESS'], definition: 'The practice of purposeful, non-judgmental awareness', prompt: 'How does mindfulness change your experience?' }
    ],
    emotional_intelligence: [
      { word: 'EMPATHY', syllables: ['EM', 'PA', 'THY'], definition: 'The ability to understand and share feelings of others', prompt: 'How do you cultivate deeper empathy?' },
      { word: 'RESILIENCE', syllables: ['RE', 'SIL', 'IENCE'], definition: 'The capacity to recover quickly from difficulties', prompt: 'What makes you resilient in challenging times?' },
      { word: 'VULNERABILITY', syllables: ['VUL', 'NER', 'A', 'BIL', 'I', 'TY'], definition: 'The quality of being open to emotional exposure', prompt: 'Where does vulnerability lead to strength?' },
      { word: 'AUTHENTICITY', syllables: ['AU', 'THEN', 'TIC', 'I', 'TY'], definition: 'The quality of being genuine and true to oneself', prompt: 'What does authentic living mean to you?' }
    ],
    creative_expression: [
      { word: 'IMAGINATION', syllables: ['I', 'MAG', 'I', 'NA', 'TION'], definition: 'The faculty of forming new ideas or images', prompt: 'How does imagination expand your reality?' },
      { word: 'INSPIRATION', syllables: ['IN', 'SPI', 'RA', 'TION'], definition: 'The process of being mentally stimulated to create', prompt: 'What ignites your creative fire?' },
      { word: 'CREATIVITY', syllables: ['CRE', 'A', 'TIV', 'I', 'TY'], definition: 'The use of imagination to produce original ideas', prompt: 'How do you nurture your creative spirit?' },
      { word: 'EXPRESSION', syllables: ['EX', 'PRES', 'SION'], definition: 'The process of making thoughts and feelings known', prompt: 'What wants to be expressed through you?' }
    ],
    wisdom_traditions: [
      { word: 'DHARMA', syllables: ['DHAR', 'MA'], definition: 'Righteous living and natural law in Hindu and Buddhist tradition', prompt: 'How do you align with your dharma?' },
      { word: 'UBUNTU', syllables: ['U', 'BUN', 'TU'], definition: 'African philosophy meaning "I am because we are"', prompt: 'How does ubuntu manifest in your relationships?' },
      { word: 'SATORI', syllables: ['SA', 'TO', 'RI'], definition: 'Sudden enlightenment in Zen Buddhism', prompt: 'What moments of clarity have transformed you?' },
      { word: 'GNOSIS', syllables: ['GNO', 'SIS'], definition: 'Spiritual knowledge of divine mysteries', prompt: 'What inner knowing guides your path?' }
    ]
  };

  // Meditation templates for different themes
  const meditationTemplates = {
    mindfulness_core: {
      title: "Breath Awareness Meditation",
      guide: "Settle into a comfortable position. Close your eyes gently. Begin to notice your natural breath without changing it. As you discover each word in the puzzle, let it become an anchor for your attention. When your mind wanders, gently return to the breath and the present moment of discovery.",
      duration: "10-15 minutes"
    },
    emotional_intelligence: {
      title: "Heart-Centered Meditation",
      guide: "Place your hand on your heart and feel its rhythm. As you search for words, let each discovery open your heart a little more. Notice what emotions arise with each word. Welcome them with kindness and curiosity.",
      duration: "12-18 minutes"
    },
    creative_expression: {
      title: "Creative Flow Meditation",
      guide: "Imagine your mind as a vast canvas. As you find each word, see it painting itself across this inner landscape. Let your intuition guide your search. Trust the creative intelligence that flows through you.",
      duration: "15-20 minutes"
    },
    wisdom_traditions: {
      title: "Ancient Wisdom Meditation",
      guide: "Connect with the lineage of wisdom keepers who have walked before us. As you discover each word, feel its ancient roots and timeless truth. Let the wisdom of ages flow through your awareness.",
      duration: "20-25 minutes"
    }
  };

  // Journal prompt generators
  const journalPromptGenerators = {
    discovery: [
      "Which word called to you most strongly? What message does it hold?",
      "How did the syllable breaks change your experience of finding words?",
      "What patterns did you notice in your search strategy?",
      "Which word challenged you the most? What did that teach you?"
    ],
    integration: [
      "How can you embody today's discovered words in your daily life?",
      "What would change if you lived from the wisdom of these words?",
      "Which word wants to be your companion this week?",
      "How do these words connect to your current life journey?"
    ],
    reflection: [
      "What emotions arose during your word discovery practice?",
      "How did mindful searching differ from regular puzzle solving?",
      "What insights emerged in the spaces between finding words?",
      "How has your relationship with language evolved through this practice?"
    ]
  };

  // Initialize word library on component mount
  useEffect(() => {
    loadWordLibrary();
  }, []);

  const loadWordLibrary = async () => {
    try {
      // In a real implementation, this would fetch from your comprehensive library
      setWordLibrary(enhancedWordLibrary);
    } catch (error) {
      console.error('Error loading word library:', error);
      setWordLibrary(enhancedWordLibrary); // Fallback to local library
    }
  };

  // Enhanced puzzle generation with syllable-aware placement
  const generateEnhancedPuzzle = (selectedTheme, selectedDifficulty, selectedSize) => {
    const words = wordLibrary[selectedTheme] || wordLibrary.mindfulness_core;
    const { width, height } = canvasSizes[selectedSize];
    
    // Determine word count based on difficulty
    const wordCounts = {
      beginner: Math.min(8, words.length),
      intermediate: Math.min(12, words.length),
      advanced: Math.min(15, words.length)
    };
    
    const selectedWords = words.slice(0, wordCounts[selectedDifficulty]);
    const grid = Array(height).fill().map(() => Array(width).fill(''));
    const placedWords = [];

    // Enhanced syllable-aware word placement
    selectedWords.forEach(wordData => {
      const placement = placeSyllableAwareWord(grid, wordData, selectedDifficulty);
      if (placement) {
        placedWords.push({
          ...wordData,
          ...placement
        });
      }
    });

    // Fill empty cells with random letters
    fillEmptyCells(grid);

    // Generate contextual prompts and meditation
    const contextualPrompts = generateContextualPrompts(placedWords, selectedTheme);
    const meditation = meditationTemplates[selectedTheme] || meditationTemplates.mindfulness_core;

    return {
      grid,
      words: placedWords,
      theme: selectedTheme,
      difficulty: selectedDifficulty,
      size: selectedSize,
      prompts: contextualPrompts,
      meditation: meditation,
      estimatedTime: calculateEstimatedTime(selectedDifficulty, placedWords.length)
    };
  };

  // Enhanced syllable-aware word placement algorithm
  const placeSyllableAwareWord = (grid, wordData, difficulty) => {
    const { word, syllables } = wordData;
    const directions = getDirectionsForDifficulty(difficulty);
    const maxAttempts = 100;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const startRow = Math.floor(Math.random() * grid.length);
      const startCol = Math.floor(Math.random() * grid[0].length);
      
      // Generate direction sequence for syllables
      const directionSequence = generateSyllableDirections(syllables, directions);
      
      if (canPlaceSyllableWord(grid, word, syllables, startRow, startCol, directionSequence)) {
        placeSyllableWord(grid, word, syllables, startRow, startCol, directionSequence);
        return {
          startRow,
          startCol,
          directionSequence,
          syllableBreaks: getSyllableBreaks(syllables, startRow, startCol, directionSequence)
        };
      }
    }
    return null;
  };

  const generateSyllableDirections = (syllables, availableDirections) => {
    return syllables.map((_, index) => {
      if (index === 0) {
        return availableDirections[Math.floor(Math.random() * availableDirections.length)];
      } else {
        // Change direction at syllable break
        const newDirections = availableDirections.filter(dir => 
          dir.dr !== syllables[index - 1]?.direction?.dr || 
          dir.dc !== syllables[index - 1]?.direction?.dc
        );
        return newDirections[Math.floor(Math.random() * newDirections.length)] || availableDirections[0];
      }
    });
  };

  const canPlaceSyllableWord = (grid, word, syllables, startRow, startCol, directionSequence) => {
    let currentRow = startRow;
    let currentCol = startCol;
    let charIndex = 0;

    for (let syllableIndex = 0; syllableIndex < syllables.length; syllableIndex++) {
      const syllable = syllables[syllableIndex];
      const direction = directionSequence[syllableIndex];

      for (let charInSyllable = 0; charInSyllable < syllable.length; charInSyllable++) {
        if (currentRow < 0 || currentRow >= grid.length || 
            currentCol < 0 || currentCol >= grid[0].length) {
          return false;
        }

        if (grid[currentRow][currentCol] !== '' && 
            grid[currentRow][currentCol] !== word[charIndex]) {
          return false;
        }

        if (charInSyllable < syllable.length - 1) {
          currentRow += direction.dr;
          currentCol += direction.dc;
        }
        charIndex++;
      }

      // Move to next syllable starting position
      if (syllableIndex < syllables.length - 1) {
        currentRow += direction.dr;
        currentCol += direction.dc;
      }
    }

    return true;
  };

  const placeSyllableWord = (grid, word, syllables, startRow, startCol, directionSequence) => {
    let currentRow = startRow;
    let currentCol = startCol;
    let charIndex = 0;

    for (let syllableIndex = 0; syllableIndex < syllables.length; syllableIndex++) {
      const syllable = syllables[syllableIndex];
      const direction = directionSequence[syllableIndex];

      for (let charInSyllable = 0; charInSyllable < syllable.length; charInSyllable++) {
        grid[currentRow][currentCol] = word[charIndex];
        
        if (charInSyllable < syllable.length - 1) {
          currentRow += direction.dr;
          currentCol += direction.dc;
        }
        charIndex++;
      }

      // Move to next syllable starting position
      if (syllableIndex < syllables.length - 1) {
        currentRow += direction.dr;
        currentCol += direction.dc;
      }
    }
  };

  const getSyllableBreaks = (syllables, startRow, startCol, directionSequence) => {
    const breaks = [];
    let currentRow = startRow;
    let currentCol = startCol;

    for (let syllableIndex = 0; syllableIndex < syllables.length; syllableIndex++) {
      const syllable = syllables[syllableIndex];
      const direction = directionSequence[syllableIndex];
      const syllablePositions = [];

      for (let charInSyllable = 0; charInSyllable < syllable.length; charInSyllable++) {
        syllablePositions.push({ row: currentRow, col: currentCol });
        
        if (charInSyllable < syllable.length - 1) {
          currentRow += direction.dr;
          currentCol += direction.dc;
        }
      }

      breaks.push({
        syllable,
        positions: syllablePositions,
        direction
      });

      // Move to next syllable starting position
      if (syllableIndex < syllables.length - 1) {
        currentRow += direction.dr;
        currentCol += direction.dc;
      }
    }

    return breaks;
  };

  const getDirectionsForDifficulty = (difficulty) => {
    const baseDirections = [
      { dr: 0, dc: 1 },   // right
      { dr: 1, dc: 0 },   // down
      { dr: 0, dc: -1 },  // left
      { dr: -1, dc: 0 }   // up
    ];

    const diagonalDirections = [
      { dr: 1, dc: 1 },   // down-right
      { dr: 1, dc: -1 },  // down-left
      { dr: -1, dc: 1 },  // up-right
      { dr: -1, dc: -1 }  // up-left
    ];

    switch (difficulty) {
      case 'beginner':
        return baseDirections.slice(0, 2); // only right and down
      case 'intermediate':
        return baseDirections;
      case 'advanced':
        return [...baseDirections, ...diagonalDirections];
      default:
        return baseDirections;
    }
  };

  const fillEmptyCells = (grid) => {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let row = 0; row < grid.length; row++) {
      for (let col = 0; col < grid[0].length; col++) {
        if (grid[row][col] === '') {
          grid[row][col] = letters[Math.floor(Math.random() * letters.length)];
        }
      }
    }
  };

  const generateContextualPrompts = (words, theme) => {
    const themePrompts = journalPromptGenerators;
    const selectedPrompts = [];
    
    // Add discovery prompts
    selectedPrompts.push(themePrompts.discovery[Math.floor(Math.random() * themePrompts.discovery.length)]);
    
    // Add integration prompts
    selectedPrompts.push(themePrompts.integration[Math.floor(Math.random() * themePrompts.integration.length)]);
    
    // Add word-specific prompts
    words.slice(0, 2).forEach(word => {
      if (word.prompt) {
        selectedPrompts.push(word.prompt);
      }
    });

    return selectedPrompts;
  };

  const calculateEstimatedTime = (difficulty, wordCount) => {
    const baseTimes = {
      beginner: 15,
      intermediate: 25,
      advanced: 35
    };
    return baseTimes[difficulty] + (wordCount * 2);
  };

  // KDP Book Generation Functions
  const generateKDPBook = async (theme, difficulty, bookCount = 50) => {
    setKdpMode(true);
    
    const bookData = {
      title: `SyllaFlow ${theme.replace('_', ' ').toUpperCase()} Collection`,
      subtitle: "Mindful Word Discovery Puzzles for Contemplative Practice",
      theme,
      difficulty,
      puzzleCount: bookCount,
      puzzles: []
    };

    // Generate multiple puzzles for the book
    for (let i = 0; i < bookCount; i++) {
      const puzzle = generateEnhancedPuzzle(theme, difficulty, 'medium');
      bookData.puzzles.push({
        ...puzzle,
        id: i + 1,
        title: `Mindful Discovery ${i + 1}`
      });
    }

    // Simulate book generation process
    const generatedBook = {
      id: Date.now(),
      ...bookData,
      status: 'generated',
      createdAt: new Date().toISOString(),
      downloadUrl: '#', // In real implementation, this would be the actual PDF URL
      metadata: {
        pageCount: bookCount * 2 + 10, // Puzzles + solutions + intro
        targetAudience: getTargetAudience(theme),
        keywords: getKDPKeywords(theme),
        description: generateBookDescription(theme, difficulty)
      }
    };

    setGeneratedBooks(prev => [...prev, generatedBook]);
    setKdpMode(false);
    
    return generatedBook;
  };

  const getTargetAudience = (theme) => {
    const audiences = {
      mindfulness_core: "Adults seeking stress relief and mindfulness practice",
      emotional_intelligence: "Individuals focused on emotional growth and self-awareness",
      creative_expression: "Artists, writers, and creative professionals",
      wisdom_traditions: "Spiritual seekers and philosophy enthusiasts"
    };
    return audiences[theme] || audiences.mindfulness_core;
  };

  const getKDPKeywords = (theme) => {
    const keywordSets = {
      mindfulness_core: ["mindfulness", "meditation", "word search", "stress relief", "awareness"],
      emotional_intelligence: ["emotional intelligence", "self-awareness", "empathy", "resilience"],
      creative_expression: ["creativity", "inspiration", "artistic practice", "imagination"],
      wisdom_traditions: ["wisdom", "spirituality", "philosophy", "ancient teachings"]
    };
    return keywordSets[theme] || keywordSets.mindfulness_core;
  };

  const generateBookDescription = (theme, difficulty) => {
    return `Discover the transformative power of mindful word searching with this collection of syllable-aware puzzles. Each puzzle features our unique directional change system that creates natural meditation moments as you discover words related to ${theme.replace('_', ' ')}. Perfect for ${difficulty} level practitioners seeking both entertainment and spiritual growth.`;
  };

  // Game interaction handlers
  const startNewPuzzle = () => {
    if (!wordLibrary) {
      loadWordLibrary();
      return;
    }

    const puzzle = generateEnhancedPuzzle(theme, difficulty, canvasSize);
    setCurrentPuzzle(puzzle);
    setFoundWords([]);
    setSelectedCells([]);
    setJournalPrompts(puzzle.prompts);
    setMeditationGuide(puzzle.meditation);
    setGameState('playing');
  };

  const handleCellClick = (row, col) => {
    if (!isSelecting) {
      setSelectedCells([{ row, col }]);
      setIsSelecting(true);
    } else {
      const newSelection = [...selectedCells, { row, col }];
      setSelectedCells(newSelection);
      checkForWord(newSelection);
    }
  };

  const checkForWord = (selection) => {
    if (!currentPuzzle) return;

    const selectedLetters = selection.map(cell => 
      currentPuzzle.grid[cell.row][cell.col]
    ).join('');

    const foundWord = currentPuzzle.words.find(word => 
      word.word === selectedLetters || word.word === selectedLetters.split('').reverse().join('')
    );

    if (foundWord && !foundWords.includes(foundWord.word)) {
      setFoundWords(prev => [...prev, foundWord.word]);
      setProgress(prev => ({
        ...prev,
        experience: prev.experience + 10,
        streak: prev.streak + 1
      }));
      
      // Check if puzzle is complete
      if (foundWords.length + 1 === currentPuzzle.words.length) {
        setGameState('completed');
      }
    }

    setSelectedCells([]);
    setIsSelecting(false);
  };

  // Render functions
  const renderWelcomeScreen = () => (
    <div className="welcome-screen">
      <div className="welcome-content">
        <h1 className="app-title">
          <span className="sylla">Sylla</span><span className="flow">Flow</span>
        </h1>
        <p className="app-subtitle">Mindful Word Discovery Through Syllable Awareness</p>
        
        <div className="council-wisdom">
          <p className="wisdom-text">
            "In the space between syllables, we find the breath of language itself." 
            <span className="wisdom-attribution">- Council of Consciousness</span>
          </p>
        </div>

        <div className="configuration-panel">
          <div className="config-section">
            <label>Canvas Size:</label>
            <select value={canvasSize} onChange={(e) => setCanvasSize(e.target.value)}>
              <option value="small">Small (12×12)</option>
              <option value="medium">Medium (15×15)</option>
              <option value="large">Large (18×18)</option>
              <option value="extra_large">Extra Large (20×20)</option>
              <option value="massive">Massive (25×25)</option>
            </select>
          </div>

          <div className="config-section">
            <label>Difficulty:</label>
            <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="config-section">
            <label>Theme:</label>
            <select value={theme} onChange={(e) => setTheme(e.target.value)}>
              <option value="mindfulness_core">Mindfulness Core</option>
              <option value="emotional_intelligence">Emotional Intelligence</option>
              <option value="creative_expression">Creative Expression</option>
              <option value="wisdom_traditions">Wisdom Traditions</option>
            </select>
          </div>
        </div>

        <div className="action-buttons">
          <button className="primary-button" onClick={startNewPuzzle}>
            Begin Mindful Discovery
          </button>
          
          <button className="secondary-button" onClick={() => setGameState('kdp')}>
            Generate KDP Books
          </button>
        </div>

        <div className="progress-display">
          <div className="progress-item">
            <span className="progress-label">Level:</span>
            <span className="progress-value">{progress.level}</span>
          </div>
          <div className="progress-item">
            <span className="progress-label">Experience:</span>
            <span className="progress-value">{progress.experience}</span>
          </div>
          <div className="progress-item">
            <span className="progress-label">Streak:</span>
            <span className="progress-value">{progress.streak}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderGameScreen = () => {
    if (!currentPuzzle) return null;

    const { cellSize } = canvasSizes[canvasSize];

    return (
      <div className="game-screen">
        <div className="game-header">
          <h2>Mindful Discovery - {currentPuzzle.theme.replace('_', ' ').toUpperCase()}</h2>
          <div className="game-info">
            <span>Difficulty: {currentPuzzle.difficulty}</span>
            <span>Found: {foundWords.length}/{currentPuzzle.words.length}</span>
            <span>Time: {currentPuzzle.estimatedTime} min</span>
          </div>
        </div>

        <div className="game-content">
          <div className="puzzle-area">
            <div 
              className="word-grid"
              ref={gridRef}
              style={{
                gridTemplateColumns: `repeat(${currentPuzzle.grid[0].length}, ${cellSize}px)`,
                gridTemplateRows: `repeat(${currentPuzzle.grid.length}, ${cellSize}px)`
              }}
            >
              {currentPuzzle.grid.map((row, rowIndex) =>
                row.map((cell, colIndex) => (
                  <div
                    key={`${rowIndex}-${colIndex}`}
                    className={`grid-cell ${
                      selectedCells.some(selected => 
                        selected.row === rowIndex && selected.col === colIndex
                      ) ? 'selected' : ''
                    }`}
                    onClick={() => handleCellClick(rowIndex, colIndex)}
                    style={{
                      width: `${cellSize}px`,
                      height: `${cellSize}px`,
                      fontSize: `${cellSize * 0.6}px`
                    }}
                  >
                    {cell}
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="sidebar">
            <div className="words-to-find">
              <h3>Words to Discover</h3>
              <div className="word-list">
                {currentPuzzle.words.map((wordData, index) => (
                  <div 
                    key={index}
                    className={`word-item ${foundWords.includes(wordData.word) ? 'found' : ''}`}
                  >
                    <span className="word">{wordData.word}</span>
                    <span className="syllables">({wordData.syllables.join('-')})</span>
                    {foundWords.includes(wordData.word) && (
                      <div className="word-details">
                        <p className="definition">{wordData.definition}</p>
                        <p className="prompt">{wordData.prompt}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="meditation-guide">
              <h3>{currentPuzzle.meditation.title}</h3>
              <p className="meditation-text">{currentPuzzle.meditation.guide}</p>
              <span className="duration">Duration: {currentPuzzle.meditation.duration}</span>
            </div>
          </div>
        </div>

        <div className="game-actions">
          <button onClick={() => setGameState('welcome')}>New Puzzle</button>
          <button onClick={() => setGameState('journal')}>Journal Integration</button>
        </div>
      </div>
    );
  };

  const renderKDPScreen = () => (
    <div className="kdp-screen">
      <div className="kdp-header">
        <h2>Amazon KDP Book Generator</h2>
        <p>Create professional puzzle books for Amazon KDP publishing</p>
      </div>

      <div className="kdp-content">
        <div className="generation-panel">
          <h3>Generate New Book</h3>
          
          <div className="kdp-config">
            <div className="config-row">
              <label>Theme:</label>
              <select value={theme} onChange={(e) => setTheme(e.target.value)}>
                <option value="mindfulness_core">Mindfulness Core</option>
                <option value="emotional_intelligence">Emotional Intelligence</option>
                <option value="creative_expression">Creative Expression</option>
                <option value="wisdom_traditions">Wisdom Traditions</option>
              </select>
            </div>

            <div className="config-row">
              <label>Difficulty:</label>
              <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="config-row">
              <label>Puzzle Count:</label>
              <select defaultValue="50">
                <option value="25">25 Puzzles</option>
                <option value="50">50 Puzzles</option>
                <option value="75">75 Puzzles</option>
                <option value="100">100 Puzzles</option>
              </select>
            </div>
          </div>

          <button 
            className="generate-button"
            onClick={() => generateKDPBook(theme, difficulty)}
            disabled={kdpMode}
          >
            {kdpMode ? 'Generating...' : 'Generate KDP Book'}
          </button>
        </div>

        <div className="generated-books">
          <h3>Generated Books</h3>
          {generatedBooks.length === 0 ? (
            <p>No books generated yet. Create your first KDP puzzle book!</p>
          ) : (
            <div className="book-list">
              {generatedBooks.map(book => (
                <div key={book.id} className="book-item">
                  <div className="book-info">
                    <h4>{book.title}</h4>
                    <p>{book.subtitle}</p>
                    <div className="book-meta">
                      <span>Theme: {book.theme.replace('_', ' ')}</span>
                      <span>Difficulty: {book.difficulty}</span>
                      <span>Puzzles: {book.puzzleCount}</span>
                      <span>Pages: {book.metadata.pageCount}</span>
                    </div>
                  </div>
                  <div className="book-actions">
                    <button className="download-button">Download PDF</button>
                    <button className="metadata-button">View Metadata</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="kdp-actions">
        <button onClick={() => setGameState('welcome')}>Back to SyllaFlow</button>
      </div>
    </div>
  );

  const renderJournalScreen = () => (
    <div className="journal-screen">
      <div className="journal-header">
        <h2>AlignFlow Journal Integration</h2>
        <p>Deepen your practice through reflective writing</p>
      </div>

      <div className="journal-content">
        <div className="meditation-section">
          <h3>Today's Meditation</h3>
          <div className="meditation-card">
            <h4>{meditationGuide.title}</h4>
            <p>{meditationGuide.guide}</p>
            <span className="duration">Duration: {meditationGuide.duration}</span>
          </div>
        </div>

        <div className="prompts-section">
          <h3>Reflection Prompts</h3>
          <div className="prompts-list">
            {journalPrompts.map((prompt, index) => (
              <div key={index} className="prompt-card">
                <p className="prompt-text">{prompt}</p>
                <textarea 
                  className="journal-input"
                  placeholder="Write your reflection here..."
                  rows="4"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="integration-section">
          <h3>Daily Integration</h3>
          <div className="integration-card">
            <p>How will you carry today's word wisdom into your life?</p>
            <textarea 
              className="integration-input"
              placeholder="Set your intention for integration..."
              rows="3"
            />
          </div>
        </div>
      </div>

      <div className="journal-actions">
        <button className="save-button">Save to AlignFlow</button>
        <button onClick={() => setGameState('playing')}>Continue Playing</button>
        <button onClick={() => setGameState('welcome')}>New Session</button>
      </div>
    </div>
  );

  // Main render
  return (
    <div className="syllaflow-app">
      {gameState === 'welcome' && renderWelcomeScreen()}
      {gameState === 'playing' && renderGameScreen()}
      {gameState === 'completed' && renderGameScreen()}
      {gameState === 'kdp' && renderKDPScreen()}
      {gameState === 'journal' && renderJournalScreen()}
    </div>
  );
};

export default EnhancedSyllaFlow;

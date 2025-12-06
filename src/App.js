import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Import the SyllaFlow algorithm (we'll create a simplified version for the frontend)
const SyllaFlowEngine = {
  // Mindfulness word database
  mindfulnessWords: {
    "meditation": {
      syllables: ["med", "i", "ta", "tion"],
      definition: "The practice of focused attention and awareness",
      etymology: { root: "Latin meditatus", meaning: "to think over, consider" },
      origin: "Latin",
      mindfulnessPrompt: "How does your meditation practice create space for awareness?",
      associations: ["contemplation", "reflection", "stillness", "presence"]
    },
    "compassion": {
      syllables: ["com", "pas", "sion"],
      definition: "Sympathetic concern for the sufferings of others",
      etymology: { root: "Latin compassio", meaning: "suffering with" },
      origin: "Latin",
      mindfulnessPrompt: "Where can you extend compassion to yourself today?",
      associations: ["empathy", "kindness", "understanding", "love"]
    },
    "awareness": {
      syllables: ["a", "ware", "ness"],
      definition: "Knowledge or perception of a situation or fact",
      etymology: { root: "Old English gewær", meaning: "wary, cautious" },
      origin: "Germanic",
      mindfulnessPrompt: "What are you becoming more aware of in this moment?",
      associations: ["consciousness", "mindfulness", "attention", "presence"]
    },
    "gratitude": {
      syllables: ["grat", "i", "tude"],
      definition: "The quality of being thankful and appreciative",
      etymology: { root: "Latin gratitudo", meaning: "thankfulness" },
      origin: "Latin",
      mindfulnessPrompt: "What small blessing can you acknowledge with gratitude?",
      associations: ["thankfulness", "appreciation", "blessing", "joy"]
    },
    "serenity": {
      syllables: ["se", "ren", "i", "ty"],
      definition: "The state of being calm, peaceful, and untroubled",
      etymology: { root: "Latin serenus", meaning: "clear, unclouded" },
      origin: "Latin",
      mindfulnessPrompt: "How can you cultivate serenity amidst life's challenges?",
      associations: ["peace", "tranquility", "calm", "stillness"]
    },
    "wisdom": {
      syllables: ["wis", "dom"],
      definition: "The quality of having experience, knowledge, and good judgment",
      etymology: { root: "Old English wisdom", meaning: "knowledge, learning" },
      origin: "Germanic",
      mindfulnessPrompt: "What wisdom is emerging from your current experiences?",
      associations: ["insight", "understanding", "knowledge", "discernment"]
    },
    "presence": {
      syllables: ["pres", "ence"],
      definition: "The state of existing, occurring, or being present",
      etymology: { root: "Latin praesentia", meaning: "being before" },
      origin: "Latin",
      mindfulnessPrompt: "How fully can you inhabit this present moment?",
      associations: ["awareness", "attention", "mindfulness", "being"]
    },
    "mindfulness": {
      syllables: ["mind", "ful", "ness"],
      definition: "The practice of being aware and present in the current moment",
      etymology: { root: "Old English gemynd", meaning: "memory, thought" },
      origin: "Germanic",
      mindfulnessPrompt: "How does mindfulness transform your relationship with thoughts?",
      associations: ["awareness", "attention", "presence", "consciousness"]
    }
  },

  // Generate a simplified grid for demonstration
  generateGrid: function(words, size = 12) {
    const grid = Array(size).fill().map(() => Array(size).fill(''));
    const placedWords = [];
    const directions = [
      [0, 1], [0, -1], [1, 0], [-1, 0],  // horizontal and vertical
      [1, 1], [1, -1], [-1, 1], [-1, -1] // diagonals
    ];

    words.forEach(word => {
      if (this.mindfulnessWords[word]) {
        const wordData = this.mindfulnessWords[word];
        const placed = this.placeWordInGrid(grid, word, wordData, directions, size);
        if (placed) {
          placedWords.push({
            word,
            ...wordData,
            placement: placed
          });
        }
      }
    });

    // Fill empty spaces with random letters
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        if (grid[i][j] === '') {
          grid[i][j] = String.fromCharCode(97 + Math.floor(Math.random() * 26));
        }
      }
    }

    return { grid, placedWords };
  },

  placeWordInGrid: function(grid, word, wordData, directions, size) {
    const maxAttempts = 50;
    
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const startRow = Math.floor(Math.random() * size);
      const startCol = Math.floor(Math.random() * size);
      
      // Generate path with direction changes at syllable boundaries
      const path = this.generateSyllablePath(word, wordData.syllables, startRow, startCol, directions, size);
      
      if (path && this.canPlaceWord(grid, word, path)) {
        // Place the word
        for (let i = 0; i < word.length; i++) {
          const [row, col] = path[i];
          grid[row][col] = word[i].toLowerCase();
        }
        return { path, syllables: wordData.syllables };
      }
    }
    return null;
  },

  generateSyllablePath: function(word, syllables, startRow, startCol, directions, size) {
    const path = [];
    let currentRow = startRow;
    let currentCol = startCol;
    let charIndex = 0;

    for (let syllableIndex = 0; syllableIndex < syllables.length; syllableIndex++) {
      const syllable = syllables[syllableIndex];
      const direction = directions[Math.floor(Math.random() * directions.length)];
      const [dr, dc] = direction;

      // Place each character of the syllable
      for (let i = 0; i < syllable.length; i++) {
        if (currentRow < 0 || currentRow >= size || currentCol < 0 || currentCol >= size) {
          return null; // Out of bounds
        }
        
        path.push([currentRow, currentCol, syllableIndex, i]);
        charIndex++;
        
        // Move to next position (except for last character of last syllable)
        if (charIndex < word.length) {
          currentRow += dr;
          currentCol += dc;
        }
      }
    }

    return path;
  },

  canPlaceWord: function(grid, word, path) {
    for (let i = 0; i < path.length; i++) {
      const [row, col] = path[i];
      if (grid[row][col] !== '' && grid[row][col] !== word[i].toLowerCase()) {
        return false;
      }
    }
    return true;
  }
};

function App() {
  const [puzzle, setPuzzle] = useState(null);
  const [selectedWords, setSelectedWords] = useState([]);
  const [foundWords, setFoundWords] = useState([]);
  const [currentSelection, setCurrentSelection] = useState([]);
  const [isSelecting, setIsSelecting] = useState(false);
  const [selectedWord, setSelectedWord] = useState(null);
  const [showMindfulnessPrompt, setShowMindfulnessPrompt] = useState(false);
  const [gamePhase, setGamePhase] = useState('centering'); // centering, playing, reflecting
  const gridRef = useRef(null);

  const defaultWords = ['meditation', 'compassion', 'awareness', 'gratitude', 'serenity', 'wisdom', 'presence', 'mindfulness'];

  useEffect(() => {
    generateNewPuzzle();
  }, []);

  const generateNewPuzzle = () => {
    const puzzleData = SyllaFlowEngine.generateGrid(defaultWords);
    setPuzzle(puzzleData);
    setFoundWords([]);
    setSelectedWords([]);
    setCurrentSelection([]);
    setSelectedWord(null);
    setGamePhase('centering');
  };

  const handleCellClick = (row, col) => {
    if (gamePhase !== 'playing') return;

    const cellKey = `${row}-${col}`;
    
    if (!isSelecting) {
      setIsSelecting(true);
      setCurrentSelection([cellKey]);
    } else {
      if (currentSelection.includes(cellKey)) {
        // End selection
        checkWordSelection();
        setIsSelecting(false);
        setCurrentSelection([]);
      } else {
        setCurrentSelection([...currentSelection, cellKey]);
      }
    }
  };

  const checkWordSelection = () => {
    if (!puzzle) return;

    const selectedLetters = currentSelection.map(cellKey => {
      const [row, col] = cellKey.split('-').map(Number);
      return puzzle.grid[row][col];
    }).join('');

    // Check if selected letters form a word
    const foundWord = puzzle.placedWords.find(wordData => {
      return wordData.word === selectedLetters || wordData.word === selectedLetters.split('').reverse().join('');
    });

    if (foundWord && !foundWords.includes(foundWord.word)) {
      setFoundWords([...foundWords, foundWord.word]);
      setSelectedWord(foundWord);
      setShowMindfulnessPrompt(true);
      
      // Check if all words found
      if (foundWords.length + 1 === puzzle.placedWords.length) {
        setTimeout(() => setGamePhase('reflecting'), 2000);
      }
    }
  };

  const startGame = () => {
    setGamePhase('playing');
  };

  const renderCenteringPhase = () => (
    <div className="centering-phase">
      <div className="centering-content">
        <h2>🌟 Welcome to SyllaFlow 🌟</h2>
        <p className="centering-text">
          Take a moment to center yourself. Notice your breath, feel your body, and set an intention for mindful discovery.
        </p>
        <div className="breathing-guide">
          <div className="breath-circle"></div>
          <p>Breathe in... and out... When you're ready, begin your journey.</p>
        </div>
        <button className="start-button" onClick={startGame}>
          Begin Mindful Discovery
        </button>
      </div>
    </div>
  );

  const renderReflectionPhase = () => (
    <div className="reflection-phase">
      <div className="reflection-content">
        <h2>🧘 Reflection & Integration 🧘</h2>
        <p>Congratulations on completing your SyllaFlow journey!</p>
        <div className="reflection-prompts">
          <h3>Reflection Prompts:</h3>
          <ul>
            <li>Which word resonated most deeply with you today?</li>
            <li>What did you notice about your mind during the search?</li>
            <li>How can you carry this focused attention into your day?</li>
          </ul>
        </div>
        <div className="found-words-summary">
          <h3>Words You Discovered:</h3>
          <div className="words-grid">
            {foundWords.map(word => (
              <div key={word} className="found-word-card">
                <h4>{word}</h4>
                <p>{SyllaFlowEngine.mindfulnessWords[word]?.mindfulnessPrompt}</p>
              </div>
            ))}
          </div>
        </div>
        <button className="new-puzzle-button" onClick={generateNewPuzzle}>
          Begin New Journey
        </button>
      </div>
    </div>
  );

  const renderGrid = () => {
    if (!puzzle) return null;

    return (
      <div className="grid-container" ref={gridRef}>
        {puzzle.grid.map((row, rowIndex) => (
          <div key={rowIndex} className="grid-row">
            {row.map((cell, colIndex) => {
              const cellKey = `${rowIndex}-${colIndex}`;
              const isSelected = currentSelection.includes(cellKey);
              const isFound = foundWords.some(word => {
                const wordData = puzzle.placedWords.find(w => w.word === word);
                return wordData?.placement?.path?.some(([r, c]) => r === rowIndex && c === colIndex);
              });

              return (
                <div
                  key={colIndex}
                  className={`grid-cell ${isSelected ? 'selected' : ''} ${isFound ? 'found' : ''}`}
                  onClick={() => handleCellClick(rowIndex, colIndex)}
                >
                  {cell.toUpperCase()}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    );
  };

  const renderWordList = () => {
    if (!puzzle) return null;

    return (
      <div className="word-list">
        <h3>Mindful Words to Discover</h3>
        <div className="words-container">
          {puzzle.placedWords.map(wordData => (
            <div
              key={wordData.word}
              className={`word-item ${foundWords.includes(wordData.word) ? 'found' : ''}`}
            >
              <span className="word-text">{wordData.word}</span>
              <div className="syllables">
                {wordData.syllables.map((syllable, index) => (
                  <span key={index} className="syllable">
                    {syllable}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (gamePhase === 'centering') {
    return (
      <div className="App">
        {renderCenteringPhase()}
      </div>
    );
  }

  if (gamePhase === 'reflecting') {
    return (
      <div className="App">
        {renderReflectionPhase()}
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌸 SyllaFlow: Mindful Word Discovery 🌸</h1>
        <p className="subtitle">Where syllables guide your journey to awareness</p>
      </header>

      <main className="game-container">
        <div className="game-area">
          <div className="puzzle-section">
            {renderGrid()}
          </div>
          
          <div className="sidebar">
            {renderWordList()}
            
            <div className="progress-section">
              <h3>Progress</h3>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${(foundWords.length / (puzzle?.placedWords.length || 1)) * 100}%` }}
                ></div>
              </div>
              <p>{foundWords.length} of {puzzle?.placedWords.length || 0} words found</p>
            </div>

            <div className="mindfulness-reminder">
              <h4>🧘 Mindful Reminder</h4>
              <p>Notice your breath as you search. Each word is a doorway to deeper awareness.</p>
            </div>
          </div>
        </div>
      </main>

      {showMindfulnessPrompt && selectedWord && (
        <div className="mindfulness-modal" onClick={() => setShowMindfulnessPrompt(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>✨ Word Discovered: {selectedWord.word} ✨</h3>
            <div className="word-details">
              <p className="definition"><strong>Definition:</strong> {selectedWord.definition}</p>
              <p className="etymology">
                <strong>Etymology:</strong> {selectedWord.etymology.root} - {selectedWord.etymology.meaning}
              </p>
              <div className="mindfulness-prompt">
                <h4>Mindfulness Reflection:</h4>
                <p>{selectedWord.mindfulnessPrompt}</p>
              </div>
              <div className="associations">
                <h4>Related Concepts:</h4>
                <div className="association-tags">
                  {selectedWord.associations.map(assoc => (
                    <span key={assoc} className="association-tag">{assoc}</span>
                  ))}
                </div>
              </div>
            </div>
            <button onClick={() => setShowMindfulnessPrompt(false)}>Continue Journey</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

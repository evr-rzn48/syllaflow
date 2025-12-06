// SyllaFlow Embeddable Widget for elv48.me Integration
// Designed to work seamlessly within WordPress/WooCommerce environment

import React, { useState, useEffect } from 'react';
import { useAlignFlowIntegration } from './AlignFlowIntegration';

const EmbeddableWidget = ({ 
  config = {},
  onWordDiscovered = null,
  onSessionComplete = null,
  onJournalEntry = null 
}) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [currentView, setCurrentView] = useState('game'); // 'game', 'reflection', 'summary'
  const [gameState, setGameState] = useState({
    isPlaying: false,
    currentWord: null,
    wordsFound: [],
    timeElapsed: 0
  });

  const {
    isConnected,
    sessionSummary,
    recordWord,
    addReflection,
    recordInsight,
    createJournalEntry,
    getSessionSummary,
    exportSession
  } = useAlignFlowIntegration();

  // Widget configuration with defaults
  const widgetConfig = {
    theme: 'alignflow', // 'alignflow', 'minimal', 'dark'
    size: 'medium', // 'small', 'medium', 'large', 'fullscreen'
    position: 'bottom-right', // 'bottom-right', 'bottom-left', 'center', 'inline'
    autoMinimize: true,
    showProgress: true,
    enableReflections: true,
    enableJournalExport: true,
    ...config
  };

  // Handle word discovery
  const handleWordFound = (wordData) => {
    const discoveryEntry = recordWord(wordData);
    setGameState(prev => ({
      ...prev,
      wordsFound: [...prev.wordsFound, discoveryEntry],
      currentWord: wordData
    }));

    // Trigger external callback
    if (onWordDiscovered) {
      onWordDiscovered(wordData, discoveryEntry);
    }

    // Show reflection prompt if enabled
    if (widgetConfig.enableReflections) {
      setTimeout(() => {
        setCurrentView('reflection');
      }, 1000);
    }
  };

  // Handle reflection submission
  const handleReflectionSubmit = (reflection) => {
    const wordIndex = gameState.wordsFound.length - 1;
    addReflection(wordIndex, reflection);
    setCurrentView('game');
  };

  // Handle session completion
  const handleSessionComplete = () => {
    const summary = getSessionSummary();
    setCurrentView('summary');
    
    if (onSessionComplete) {
      onSessionComplete(summary);
    }
  };

  // Handle journal entry creation
  const handleCreateJournalEntry = (entryData) => {
    const journalEntry = createJournalEntry(entryData);
    
    if (onJournalEntry) {
      onJournalEntry(journalEntry);
    }

    // Trigger AlignFlow journal integration
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('alignflow:newJournalEntry', {
        detail: journalEntry
      }));
    }
  };

  // Widget styles based on configuration
  const getWidgetStyles = () => {
    const baseStyles = {
      position: widgetConfig.position === 'inline' ? 'relative' : 'fixed',
      zIndex: 1000,
      borderRadius: '12px',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
      transition: 'all 0.3s ease',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    };

    // Position styles
    if (widgetConfig.position === 'bottom-right') {
      baseStyles.bottom = '20px';
      baseStyles.right = '20px';
    } else if (widgetConfig.position === 'bottom-left') {
      baseStyles.bottom = '20px';
      baseStyles.left = '20px';
    } else if (widgetConfig.position === 'center') {
      baseStyles.top = '50%';
      baseStyles.left = '50%';
      baseStyles.transform = 'translate(-50%, -50%)';
    }

    // Size styles
    const sizeMap = {
      small: { width: '300px', height: '400px' },
      medium: { width: '400px', height: '500px' },
      large: { width: '500px', height: '600px' },
      fullscreen: { width: '90vw', height: '90vh', maxWidth: '800px', maxHeight: '700px' }
    };
    
    Object.assign(baseStyles, sizeMap[widgetConfig.size]);

    // Theme styles
    const themeMap = {
      alignflow: {
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: '#ffffff'
      },
      minimal: {
        background: '#ffffff',
        color: '#333333',
        border: '1px solid #e0e0e0'
      },
      dark: {
        background: '#1a1a1a',
        color: '#ffffff',
        border: '1px solid #333333'
      }
    };

    Object.assign(baseStyles, themeMap[widgetConfig.theme]);

    if (isMinimized) {
      baseStyles.width = '60px';
      baseStyles.height = '60px';
      baseStyles.borderRadius = '50%';
      baseStyles.cursor = 'pointer';
    }

    return baseStyles;
  };

  // Render minimized widget
  const renderMinimized = () => (
    <div 
      style={getWidgetStyles()}
      onClick={() => setIsMinimized(false)}
      title="Open SyllaFlow"
    >
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        fontSize: '24px'
      }}>
        🌸
      </div>
    </div>
  );

  // Render game view
  const renderGameView = () => (
    <div style={{ padding: '20px', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px'
      }}>
        <h3 style={{ margin: 0, fontSize: '18px' }}>SyllaFlow</h3>
        <div style={{ display: 'flex', gap: '10px' }}>
          {widgetConfig.autoMinimize && (
            <button 
              onClick={() => setIsMinimized(true)}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                borderRadius: '4px',
                color: 'inherit',
                cursor: 'pointer',
                padding: '4px 8px'
              }}
            >
              −
            </button>
          )}
        </div>
      </div>

      {widgetConfig.showProgress && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ 
            fontSize: '14px', 
            marginBottom: '8px',
            opacity: 0.8
          }}>
            Words Discovered: {gameState.wordsFound.length}
          </div>
          <div style={{
            width: '100%',
            height: '4px',
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '2px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${Math.min((gameState.wordsFound.length / 8) * 100, 100)}%`,
              height: '100%',
              background: 'rgba(255, 255, 255, 0.8)',
              transition: 'width 0.3s ease'
            }} />
          </div>
        </div>
      )}

      <div style={{ 
        flex: 1, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '8px',
        marginBottom: '20px'
      }}>
        {/* Game component would be embedded here */}
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🧩</div>
          <div style={{ fontSize: '16px', opacity: 0.8 }}>
            {gameState.isPlaying ? 'Find words in the syllable flow...' : 'Ready to begin your mindful word journey?'}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button
          onClick={() => setGameState(prev => ({ ...prev, isPlaying: !prev.isPlaying }))}
          style={{
            flex: 1,
            padding: '12px',
            background: 'rgba(255, 255, 255, 0.2)',
            border: 'none',
            borderRadius: '6px',
            color: 'inherit',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          {gameState.isPlaying ? 'Pause' : 'Start'}
        </button>
        
        {gameState.wordsFound.length > 0 && (
          <button
            onClick={handleSessionComplete}
            style={{
              flex: 1,
              padding: '12px',
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              borderRadius: '6px',
              color: 'inherit',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Complete Session
          </button>
        )}
      </div>
    </div>
  );

  // Render reflection view
  const renderReflectionView = () => {
    const [reflection, setReflection] = useState('');
    
    return (
      <div style={{ padding: '20px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <h3 style={{ margin: '0 0 20px 0', fontSize: '18px' }}>
          Reflect on "{gameState.currentWord?.word}"
        </h3>
        
        <div style={{ 
          marginBottom: '20px',
          padding: '16px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '8px',
          fontSize: '14px'
        }}>
          <strong>Definition:</strong> {gameState.currentWord?.definition}
        </div>

        <div style={{ 
          marginBottom: '20px',
          fontSize: '14px',
          opacity: 0.8
        }}>
          {gameState.currentWord?.mindfulnessPrompt}
        </div>

        <textarea
          value={reflection}
          onChange={(e) => setReflection(e.target.value)}
          placeholder="What insights or connections arise for you with this word?"
          style={{
            flex: 1,
            padding: '12px',
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            color: 'inherit',
            fontSize: '14px',
            resize: 'none',
            marginBottom: '20px'
          }}
        />

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setCurrentView('game')}
            style={{
              flex: 1,
              padding: '12px',
              background: 'rgba(255, 255, 255, 0.1)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: '6px',
              color: 'inherit',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Skip
          </button>
          
          <button
            onClick={() => {
              handleReflectionSubmit(reflection);
              setReflection('');
            }}
            disabled={!reflection.trim()}
            style={{
              flex: 1,
              padding: '12px',
              background: reflection.trim() ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.1)',
              border: 'none',
              borderRadius: '6px',
              color: 'inherit',
              cursor: reflection.trim() ? 'pointer' : 'not-allowed',
              fontSize: '14px',
              opacity: reflection.trim() ? 1 : 0.5
            }}
          >
            Save Reflection
          </button>
        </div>
      </div>
    );
  };

  // Render summary view
  const renderSummaryView = () => (
    <div style={{ padding: '20px', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ margin: '0 0 20px 0', fontSize: '18px' }}>Session Complete</h3>
      
      <div style={{ 
        flex: 1,
        marginBottom: '20px'
      }}>
        <div style={{ 
          marginBottom: '16px',
          padding: '12px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '6px',
          fontSize: '14px'
        }}>
          <strong>Words Discovered:</strong> {sessionSummary?.wordsDiscovered || 0}
        </div>
        
        <div style={{ 
          marginBottom: '16px',
          padding: '12px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '6px',
          fontSize: '14px'
        }}>
          <strong>Reflections Added:</strong> {sessionSummary?.reflectionsAdded || 0}
        </div>

        {sessionSummary?.topWords && sessionSummary.topWords.length > 0 && (
          <div style={{ 
            marginBottom: '16px',
            padding: '12px',
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '6px',
            fontSize: '14px'
          }}>
            <strong>Key Words:</strong> {sessionSummary.topWords.map(w => w.word).join(', ')}
          </div>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {widgetConfig.enableJournalExport && (
          <button
            onClick={() => {
              const entryData = {
                title: `SyllaFlow Session - ${new Date().toLocaleDateString()}`,
                content: exportSession('markdown'),
                mood: 'reflective',
                tags: ['syllaflow', 'mindfulness', 'word-discovery']
              };
              handleCreateJournalEntry(entryData);
            }}
            style={{
              padding: '12px',
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              borderRadius: '6px',
              color: 'inherit',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Save to AlignFlow Journal
          </button>
        )}
        
        <button
          onClick={() => {
            setCurrentView('game');
            setGameState({
              isPlaying: false,
              currentWord: null,
              wordsFound: [],
              timeElapsed: 0
            });
          }}
          style={{
            padding: '12px',
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            color: 'inherit',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          Start New Session
        </button>
      </div>
    </div>
  );

  // Main render
  if (isMinimized) {
    return renderMinimized();
  }

  return (
    <div style={getWidgetStyles()}>
      {currentView === 'game' && renderGameView()}
      {currentView === 'reflection' && renderReflectionView()}
      {currentView === 'summary' && renderSummaryView()}
      
      {/* Connection status indicator */}
      {isConnected && (
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: '#4ade80',
          title: 'Connected to AlignFlow'
        }} />
      )}
    </div>
  );
};

// WordPress Shortcode Integration
export const createWordPressShortcode = () => {
  if (typeof window !== 'undefined' && window.wp) {
    // Register [syllaflow] shortcode
    window.wp.hooks.addFilter('syllaflow_shortcode', 'syllaflow', (content, attributes) => {
      const config = {
        theme: attributes.theme || 'alignflow',
        size: attributes.size || 'medium',
        position: 'inline',
        ...attributes
      };
      
      // Create container for React component
      const container = document.createElement('div');
      container.id = `syllaflow-widget-${Date.now()}`;
      
      // Render React component
      import('react-dom').then(ReactDOM => {
        ReactDOM.render(<EmbeddableWidget config={config} />, container);
      });
      
      return container.outerHTML;
    });
  }
};

export default EmbeddableWidget;

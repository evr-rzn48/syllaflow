// AlignFlow Integration Component for SyllaFlow
// Designed for seamless integration with elv48.me AlignFlow journal system

import React, { useState, useEffect } from 'react';

class AlignFlowIntegration {
  constructor() {
    this.journalAPI = null;
    this.sessionData = {};
    this.integrationConfig = {
      apiEndpoint: 'https://elv48.me/api/alignflow',
      sessionTimeout: 30 * 60 * 1000, // 30 minutes
      autoSave: true,
      syncInterval: 5000 // 5 seconds
    };
  }

  // Initialize connection with AlignFlow journal system
  async initializeConnection(userToken = null) {
    try {
      // Check if running in WordPress/WooCommerce environment
      if (typeof window !== 'undefined' && window.wp) {
        this.journalAPI = window.wp.api;
      }
      
      // Initialize session data
      this.sessionData = {
        userId: userToken || this.generateGuestId(),
        sessionId: this.generateSessionId(),
        startTime: new Date().toISOString(),
        wordsDiscovered: [],
        reflections: [],
        insights: [],
        journalEntries: []
      };

      // Set up auto-save if enabled
      if (this.integrationConfig.autoSave) {
        this.startAutoSave();
      }

      return { success: true, sessionId: this.sessionData.sessionId };
    } catch (error) {
      console.error('AlignFlow integration initialization failed:', error);
      return { success: false, error: error.message };
    }
  }

  // Generate unique guest ID for non-authenticated users
  generateGuestId() {
    return 'guest_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Generate unique session ID
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Record word discovery for journal integration
  recordWordDiscovery(wordData) {
    const discoveryEntry = {
      timestamp: new Date().toISOString(),
      word: wordData.word,
      definition: wordData.definition,
      etymology: wordData.etymology,
      syllables: wordData.syllables,
      mindfulnessPrompt: wordData.mindfulnessPrompt,
      userReflection: null,
      emotionalResonance: null,
      personalConnection: null
    };

    this.sessionData.wordsDiscovered.push(discoveryEntry);
    this.triggerJournalSync();
    
    return discoveryEntry;
  }

  // Add user reflection to word discovery
  addReflection(wordIndex, reflection) {
    if (this.sessionData.wordsDiscovered[wordIndex]) {
      this.sessionData.wordsDiscovered[wordIndex].userReflection = reflection;
      this.sessionData.wordsDiscovered[wordIndex].reflectionTime = new Date().toISOString();
      this.triggerJournalSync();
    }
  }

  // Record insight or breakthrough moment
  recordInsight(insightData) {
    const insight = {
      timestamp: new Date().toISOString(),
      type: insightData.type || 'general',
      content: insightData.content,
      relatedWords: insightData.relatedWords || [],
      emotionalState: insightData.emotionalState,
      actionItems: insightData.actionItems || []
    };

    this.sessionData.insights.push(insight);
    this.triggerJournalSync();
    
    return insight;
  }

  // Create journal entry from SyllaFlow session
  createJournalEntry(entryData) {
    const journalEntry = {
      timestamp: new Date().toISOString(),
      sessionId: this.sessionData.sessionId,
      title: entryData.title || `SyllaFlow Session - ${new Date().toLocaleDateString()}`,
      content: entryData.content,
      wordsExplored: this.sessionData.wordsDiscovered.length,
      keyInsights: this.sessionData.insights,
      mood: entryData.mood,
      gratitude: entryData.gratitude || [],
      intentions: entryData.intentions || [],
      tags: ['syllaflow', 'mindfulness', 'word-discovery', ...(entryData.tags || [])]
    };

    this.sessionData.journalEntries.push(journalEntry);
    this.syncWithAlignFlow(journalEntry);
    
    return journalEntry;
  }

  // Sync data with AlignFlow journal system
  async syncWithAlignFlow(data = null) {
    try {
      const syncData = data || this.sessionData;
      
      // If WordPress environment, use REST API
      if (this.journalAPI) {
        const response = await fetch(`${this.integrationConfig.apiEndpoint}/sync`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-WP-Nonce': window.wpApiSettings?.nonce || ''
          },
          body: JSON.stringify({
            sessionData: syncData,
            timestamp: new Date().toISOString()
          })
        });
        
        return await response.json();
      }
      
      // Fallback to localStorage for offline functionality
      localStorage.setItem('syllaflow_session', JSON.stringify(syncData));
      return { success: true, method: 'localStorage' };
      
    } catch (error) {
      console.error('AlignFlow sync failed:', error);
      // Graceful degradation - save to localStorage
      localStorage.setItem('syllaflow_session_backup', JSON.stringify(this.sessionData));
      return { success: false, error: error.message };
    }
  }

  // Trigger sync (debounced)
  triggerJournalSync() {
    if (this.syncTimeout) {
      clearTimeout(this.syncTimeout);
    }
    
    this.syncTimeout = setTimeout(() => {
      this.syncWithAlignFlow();
    }, 1000); // 1 second debounce
  }

  // Start auto-save functionality
  startAutoSave() {
    this.autoSaveInterval = setInterval(() => {
      this.syncWithAlignFlow();
    }, this.integrationConfig.syncInterval);
  }

  // Stop auto-save functionality
  stopAutoSave() {
    if (this.autoSaveInterval) {
      clearInterval(this.autoSaveInterval);
    }
  }

  // Get session summary for journal
  getSessionSummary() {
    return {
      sessionId: this.sessionData.sessionId,
      duration: Date.now() - new Date(this.sessionData.startTime).getTime(),
      wordsDiscovered: this.sessionData.wordsDiscovered.length,
      reflectionsAdded: this.sessionData.wordsDiscovered.filter(w => w.userReflection).length,
      insightsRecorded: this.sessionData.insights.length,
      journalEntriesCreated: this.sessionData.journalEntries.length,
      topWords: this.getTopWords(),
      emotionalJourney: this.getEmotionalJourney()
    };
  }

  // Get most meaningful words from session
  getTopWords() {
    return this.sessionData.wordsDiscovered
      .filter(word => word.userReflection || word.emotionalResonance)
      .sort((a, b) => (b.emotionalResonance || 0) - (a.emotionalResonance || 0))
      .slice(0, 5)
      .map(word => ({
        word: word.word,
        definition: word.definition,
        reflection: word.userReflection
      }));
  }

  // Track emotional journey through session
  getEmotionalJourney() {
    return this.sessionData.wordsDiscovered
      .filter(word => word.emotionalResonance)
      .map(word => ({
        timestamp: word.timestamp,
        word: word.word,
        emotion: word.emotionalResonance
      }));
  }

  // Export session data for external use
  exportSessionData(format = 'json') {
    const exportData = {
      ...this.getSessionSummary(),
      fullSessionData: this.sessionData,
      exportTimestamp: new Date().toISOString()
    };

    switch (format) {
      case 'json':
        return JSON.stringify(exportData, null, 2);
      case 'markdown':
        return this.formatAsMarkdown(exportData);
      case 'csv':
        return this.formatAsCSV(exportData);
      default:
        return exportData;
    }
  }

  // Format session data as markdown for journal
  formatAsMarkdown(data) {
    let markdown = `# SyllaFlow Session - ${new Date(data.fullSessionData.startTime).toLocaleDateString()}\n\n`;
    
    markdown += `**Session Duration:** ${Math.round(data.duration / 60000)} minutes\n`;
    markdown += `**Words Discovered:** ${data.wordsDiscovered}\n`;
    markdown += `**Reflections Added:** ${data.reflectionsAdded}\n\n`;
    
    if (data.topWords.length > 0) {
      markdown += `## Key Words Explored\n\n`;
      data.topWords.forEach(word => {
        markdown += `### ${word.word}\n`;
        markdown += `*${word.definition}*\n\n`;
        if (word.reflection) {
          markdown += `**My Reflection:** ${word.reflection}\n\n`;
        }
      });
    }
    
    if (data.fullSessionData.insights.length > 0) {
      markdown += `## Insights & Breakthroughs\n\n`;
      data.fullSessionData.insights.forEach(insight => {
        markdown += `- ${insight.content}\n`;
      });
      markdown += '\n';
    }
    
    return markdown;
  }

  // Format session data as CSV
  formatAsCSV(data) {
    let csv = 'Word,Definition,Etymology,Reflection,Timestamp\n';
    
    data.fullSessionData.wordsDiscovered.forEach(word => {
      csv += `"${word.word}","${word.definition}","${word.etymology}","${word.userReflection || ''}","${word.timestamp}"\n`;
    });
    
    return csv;
  }

  // Clean up integration
  cleanup() {
    this.stopAutoSave();
    if (this.syncTimeout) {
      clearTimeout(this.syncTimeout);
    }
    
    // Final sync before cleanup
    this.syncWithAlignFlow();
  }
}

// React Hook for AlignFlow Integration
export const useAlignFlowIntegration = () => {
  const [integration, setIntegration] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [sessionSummary, setSessionSummary] = useState(null);

  useEffect(() => {
    const alignFlowIntegration = new AlignFlowIntegration();
    
    alignFlowIntegration.initializeConnection().then(result => {
      if (result.success) {
        setIntegration(alignFlowIntegration);
        setIsConnected(true);
      }
    });

    return () => {
      if (alignFlowIntegration) {
        alignFlowIntegration.cleanup();
      }
    };
  }, []);

  const recordWord = (wordData) => {
    if (integration) {
      return integration.recordWordDiscovery(wordData);
    }
  };

  const addReflection = (wordIndex, reflection) => {
    if (integration) {
      integration.addReflection(wordIndex, reflection);
    }
  };

  const recordInsight = (insightData) => {
    if (integration) {
      return integration.recordInsight(insightData);
    }
  };

  const createJournalEntry = (entryData) => {
    if (integration) {
      return integration.createJournalEntry(entryData);
    }
  };

  const getSessionSummary = () => {
    if (integration) {
      const summary = integration.getSessionSummary();
      setSessionSummary(summary);
      return summary;
    }
  };

  const exportSession = (format = 'json') => {
    if (integration) {
      return integration.exportSessionData(format);
    }
  };

  return {
    isConnected,
    sessionSummary,
    recordWord,
    addReflection,
    recordInsight,
    createJournalEntry,
    getSessionSummary,
    exportSession
  };
};

// WordPress Plugin Integration Helper
export const initializeWordPressIntegration = () => {
  // Check if we're in WordPress environment
  if (typeof window !== 'undefined' && window.wp) {
    // Register SyllaFlow with WordPress
    window.wp.hooks.addAction('syllaflow.wordDiscovered', 'alignflow', (wordData) => {
      // Trigger WordPress event for AlignFlow journal
      const event = new CustomEvent('alignflow:wordDiscovered', {
        detail: wordData
      });
      window.dispatchEvent(event);
    });

    // Register journal entry creation
    window.wp.hooks.addAction('syllaflow.journalEntry', 'alignflow', (entryData) => {
      const event = new CustomEvent('alignflow:journalEntry', {
        detail: entryData
      });
      window.dispatchEvent(event);
    });
  }
};

export default AlignFlowIntegration;

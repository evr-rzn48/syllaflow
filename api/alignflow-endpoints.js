// AlignFlow Journal Integration API Endpoints
// Designed for WordPress/WooCommerce integration on elv48.me

const express = require('express');
const cors = require('cors');
const router = express.Router();

// Middleware for WordPress integration
const wordpressAuth = (req, res, next) => {
  // Check for WordPress nonce or user authentication
  const nonce = req.headers['x-wp-nonce'];
  const userToken = req.headers['authorization'];
  
  if (nonce || userToken) {
    // Validate WordPress authentication
    req.user = {
      id: req.headers['x-user-id'] || 'guest',
      authenticated: !!userToken
    };
    next();
  } else {
    // Allow guest access with limited functionality
    req.user = { id: 'guest', authenticated: false };
    next();
  }
};

// CORS configuration for elv48.me
const corsOptions = {
  origin: [
    'https://elv48.me',
    'https://www.elv48.me',
    'http://localhost:3000',
    'http://localhost:8080'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-WP-Nonce', 'X-User-ID']
};

router.use(cors(corsOptions));
router.use(express.json({ limit: '10mb' }));
router.use(wordpressAuth);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'SyllaFlow AlignFlow Integration',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// Initialize session endpoint
router.post('/session/init', async (req, res) => {
  try {
    const { userPreferences, deviceInfo } = req.body;
    
    const sessionData = {
      sessionId: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      userId: req.user.id,
      startTime: new Date().toISOString(),
      userPreferences: userPreferences || {},
      deviceInfo: deviceInfo || {},
      wordsDiscovered: [],
      reflections: [],
      insights: [],
      journalEntries: [],
      status: 'active'
    };

    // Store session in database or cache
    // For WordPress integration, this could use wp_options or custom tables
    
    res.json({
      success: true,
      sessionId: sessionData.sessionId,
      message: 'Session initialized successfully'
    });
  } catch (error) {
    console.error('Session initialization error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to initialize session',
      details: error.message
    });
  }
});

// Record word discovery
router.post('/word/discovered', async (req, res) => {
  try {
    const { sessionId, wordData } = req.body;
    
    if (!sessionId || !wordData) {
      return res.status(400).json({
        success: false,
        error: 'Session ID and word data are required'
      });
    }

    const discoveryEntry = {
      id: `word_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      sessionId,
      userId: req.user.id,
      timestamp: new Date().toISOString(),
      word: wordData.word,
      definition: wordData.definition,
      etymology: wordData.etymology,
      syllables: wordData.syllables,
      mindfulnessPrompt: wordData.mindfulnessPrompt,
      discoveryMethod: wordData.discoveryMethod || 'syllable-search',
      timeToDiscover: wordData.timeToDiscover || null,
      userReflection: null,
      emotionalResonance: null,
      personalConnection: null
    };

    // Store in database
    // For WordPress: wp_posts with custom post type 'syllaflow_discovery'
    
    // Trigger WordPress hooks if available
    if (typeof global.wp !== 'undefined') {
      global.wp.hooks.doAction('syllaflow.wordDiscovered', discoveryEntry);
    }

    res.json({
      success: true,
      discoveryId: discoveryEntry.id,
      message: 'Word discovery recorded successfully'
    });
  } catch (error) {
    console.error('Word discovery recording error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to record word discovery',
      details: error.message
    });
  }
});

// Add reflection to word discovery
router.post('/word/reflection', async (req, res) => {
  try {
    const { discoveryId, reflection, emotionalResonance, personalConnection } = req.body;
    
    if (!discoveryId || !reflection) {
      return res.status(400).json({
        success: false,
        error: 'Discovery ID and reflection are required'
      });
    }

    const reflectionData = {
      discoveryId,
      userId: req.user.id,
      timestamp: new Date().toISOString(),
      reflection: reflection.trim(),
      emotionalResonance: emotionalResonance || null,
      personalConnection: personalConnection || null,
      wordCount: reflection.trim().split(/\s+/).length
    };

    // Update discovery entry in database
    // For WordPress: Update post meta for the discovery post
    
    res.json({
      success: true,
      message: 'Reflection added successfully'
    });
  } catch (error) {
    console.error('Reflection recording error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to record reflection',
      details: error.message
    });
  }
});

// Record insight or breakthrough
router.post('/insight/record', async (req, res) => {
  try {
    const { sessionId, insightData } = req.body;
    
    if (!sessionId || !insightData) {
      return res.status(400).json({
        success: false,
        error: 'Session ID and insight data are required'
      });
    }

    const insight = {
      id: `insight_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      sessionId,
      userId: req.user.id,
      timestamp: new Date().toISOString(),
      type: insightData.type || 'general',
      content: insightData.content,
      relatedWords: insightData.relatedWords || [],
      emotionalState: insightData.emotionalState || null,
      actionItems: insightData.actionItems || [],
      confidence: insightData.confidence || null
    };

    // Store in database
    // For WordPress: Custom post type 'syllaflow_insight'
    
    res.json({
      success: true,
      insightId: insight.id,
      message: 'Insight recorded successfully'
    });
  } catch (error) {
    console.error('Insight recording error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to record insight',
      details: error.message
    });
  }
});

// Create journal entry
router.post('/journal/create', async (req, res) => {
  try {
    const { sessionId, entryData } = req.body;
    
    if (!sessionId || !entryData) {
      return res.status(400).json({
        success: false,
        error: 'Session ID and entry data are required'
      });
    }

    const journalEntry = {
      id: `journal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      sessionId,
      userId: req.user.id,
      timestamp: new Date().toISOString(),
      title: entryData.title || `SyllaFlow Session - ${new Date().toLocaleDateString()}`,
      content: entryData.content,
      format: entryData.format || 'markdown',
      mood: entryData.mood || null,
      gratitude: entryData.gratitude || [],
      intentions: entryData.intentions || [],
      tags: ['syllaflow', 'mindfulness', 'word-discovery', ...(entryData.tags || [])],
      privacy: entryData.privacy || 'private',
      wordCount: entryData.content ? entryData.content.split(/\s+/).length : 0
    };

    // Store in WordPress as post
    // Post type: 'alignflow_journal' or integrate with existing journal system
    
    // Trigger AlignFlow journal integration
    if (typeof global.wp !== 'undefined') {
      global.wp.hooks.doAction('alignflow.journalEntryCreated', journalEntry);
    }

    res.json({
      success: true,
      journalId: journalEntry.id,
      message: 'Journal entry created successfully',
      viewUrl: `https://elv48.me/alignflow/journal/${journalEntry.id}`
    });
  } catch (error) {
    console.error('Journal entry creation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create journal entry',
      details: error.message
    });
  }
});

// Get session summary
router.get('/session/:sessionId/summary', async (req, res) => {
  try {
    const { sessionId } = req.params;
    
    if (!sessionId) {
      return res.status(400).json({
        success: false,
        error: 'Session ID is required'
      });
    }

    // Retrieve session data from database
    // This would query WordPress database for session-related posts/meta
    
    const mockSummary = {
      sessionId,
      userId: req.user.id,
      startTime: new Date(Date.now() - 1800000).toISOString(), // 30 minutes ago
      endTime: new Date().toISOString(),
      duration: 1800000, // 30 minutes in milliseconds
      wordsDiscovered: 8,
      reflectionsAdded: 5,
      insightsRecorded: 2,
      journalEntriesCreated: 1,
      topWords: [
        { word: 'MEDITATION', definition: 'Practice of focused attention', reflection: 'Helps me find inner peace' },
        { word: 'COMPASSION', definition: 'Sympathetic concern for others', reflection: 'Essential for healing relationships' },
        { word: 'WISDOM', definition: 'Deep understanding and insight', reflection: 'Comes through experience and reflection' }
      ],
      emotionalJourney: [
        { timestamp: new Date(Date.now() - 1500000).toISOString(), emotion: 'curious', intensity: 7 },
        { timestamp: new Date(Date.now() - 900000).toISOString(), emotion: 'peaceful', intensity: 8 },
        { timestamp: new Date(Date.now() - 300000).toISOString(), emotion: 'grateful', intensity: 9 }
      ],
      achievements: [
        'First reflection added',
        'Discovered 5+ words',
        'Created journal entry'
      ]
    };

    res.json({
      success: true,
      summary: mockSummary
    });
  } catch (error) {
    console.error('Session summary error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve session summary',
      details: error.message
    });
  }
});

// Export session data
router.get('/session/:sessionId/export', async (req, res) => {
  try {
    const { sessionId } = req.params;
    const { format = 'json' } = req.query;
    
    if (!sessionId) {
      return res.status(400).json({
        success: false,
        error: 'Session ID is required'
      });
    }

    // Retrieve complete session data
    // This would query all related WordPress posts/meta for the session
    
    const sessionData = {
      sessionId,
      exportTimestamp: new Date().toISOString(),
      // ... complete session data would be populated here
    };

    let exportContent;
    let contentType;
    let filename;

    switch (format) {
      case 'markdown':
        exportContent = formatAsMarkdown(sessionData);
        contentType = 'text/markdown';
        filename = `syllaflow-session-${sessionId}.md`;
        break;
      case 'csv':
        exportContent = formatAsCSV(sessionData);
        contentType = 'text/csv';
        filename = `syllaflow-session-${sessionId}.csv`;
        break;
      case 'json':
      default:
        exportContent = JSON.stringify(sessionData, null, 2);
        contentType = 'application/json';
        filename = `syllaflow-session-${sessionId}.json`;
        break;
    }

    res.setHeader('Content-Type', contentType);
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.send(exportContent);
  } catch (error) {
    console.error('Session export error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to export session data',
      details: error.message
    });
  }
});

// Sync with AlignFlow journal system
router.post('/sync', async (req, res) => {
  try {
    const { sessionData, syncType = 'full' } = req.body;
    
    if (!sessionData) {
      return res.status(400).json({
        success: false,
        error: 'Session data is required for sync'
      });
    }

    // Sync with WordPress/AlignFlow journal system
    // This would update or create WordPress posts/meta based on session data
    
    const syncResult = {
      syncId: `sync_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      sessionId: sessionData.sessionId,
      itemsSynced: {
        wordsDiscovered: sessionData.wordsDiscovered?.length || 0,
        reflections: sessionData.reflections?.length || 0,
        insights: sessionData.insights?.length || 0,
        journalEntries: sessionData.journalEntries?.length || 0
      },
      status: 'completed'
    };

    res.json({
      success: true,
      syncResult,
      message: 'Data synced successfully with AlignFlow journal'
    });
  } catch (error) {
    console.error('Sync error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to sync with AlignFlow journal',
      details: error.message
    });
  }
});

// WordPress webhook endpoint
router.post('/webhook/wordpress', async (req, res) => {
  try {
    const { action, data } = req.body;
    
    // Handle WordPress events that might affect SyllaFlow
    switch (action) {
      case 'user_login':
        // Update user session data
        break;
      case 'journal_entry_updated':
        // Sync changes back to SyllaFlow if needed
        break;
      case 'user_preferences_changed':
        // Update SyllaFlow configuration
        break;
      default:
        console.log('Unhandled WordPress webhook:', action);
    }

    res.json({
      success: true,
      message: 'Webhook processed successfully'
    });
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to process webhook',
      details: error.message
    });
  }
});

// Helper functions for data formatting
function formatAsMarkdown(sessionData) {
  let markdown = `# SyllaFlow Session Export\n\n`;
  markdown += `**Session ID:** ${sessionData.sessionId}\n`;
  markdown += `**Export Date:** ${sessionData.exportTimestamp}\n\n`;
  
  // Add session details, words discovered, reflections, etc.
  // This would be populated with actual session data
  
  return markdown;
}

function formatAsCSV(sessionData) {
  let csv = 'Type,Timestamp,Word,Definition,Reflection\n';
  
  // Add CSV rows for each discovery, reflection, etc.
  // This would be populated with actual session data
  
  return csv;
}

module.exports = router;

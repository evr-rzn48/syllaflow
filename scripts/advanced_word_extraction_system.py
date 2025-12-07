#!/usr/bin/env python3
"""
Advanced Word Extraction and Theme Analysis System for SyllaFlow
Enhanced document processing with mindfulness integration and Council of Consciousness wisdom

This system provides sophisticated word extraction, theme analysis, and content processing
capabilities for SyllaFlow puzzle generation, incorporating advanced linguistic analysis
and mindfulness principles.

Council of Consciousness Integration:
- Rick Rubin: Authentic simplicity in content extraction
- Angela Davis: Accessible and inclusive language processing
- Octavia Butler: Transformational possibilities through linguistic analysis
- Wayne Dyer: Wisdom extraction from diverse content sources
- Saul Williams: Cultural bridge-building through language diversity
"""

import re
import json
import logging
import nltk
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
from collections import Counter, defaultdict
import math

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

class ContentType(Enum):
    """Types of content for specialized processing"""
    MINDFULNESS = "mindfulness"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    SPIRITUAL = "spiritual"
    PHILOSOPHICAL = "philosophical"
    SCIENTIFIC = "scientific"
    LITERARY = "literary"
    GENERAL = "general"

class DifficultyLevel(Enum):
    """Difficulty levels for puzzle generation"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class WordAnalysis:
    """Comprehensive analysis of a single word"""
    word: str
    syllables: List[str]
    syllable_count: int
    part_of_speech: str
    frequency: int
    complexity_score: float
    mindfulness_relevance: float
    themes: List[str]
    etymology_hints: List[str]
    meditation_prompt: str
    journal_integration: str

@dataclass
class ThemeAnalysis:
    """Analysis of thematic content"""
    theme_name: str
    keywords: List[str]
    relevance_score: float
    word_count: int
    mindfulness_connection: str
    meditation_focus: str
    journal_prompts: List[str]

@dataclass
class ContentAnalysis:
    """Comprehensive content analysis results"""
    content_type: ContentType
    difficulty_level: DifficultyLevel
    word_analyses: List[WordAnalysis]
    theme_analyses: List[ThemeAnalysis]
    overall_complexity: float
    mindfulness_integration_score: float
    recommended_puzzle_types: List[str]
    council_wisdom: Dict[str, str]

class AdvancedWordExtractor:
    """
    Advanced word extraction system with mindfulness integration
    
    This class provides sophisticated linguistic analysis, theme extraction,
    and content processing capabilities for SyllaFlow puzzle generation.
    """
    
    def __init__(self):
        """Initialize the advanced word extraction system"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize stop words
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize mindfulness vocabulary
        self.mindfulness_vocabulary = self._load_mindfulness_vocabulary()
        
        # Initialize theme patterns
        self.theme_patterns = self._load_theme_patterns()
        
        # Initialize Council of Consciousness wisdom
        self.council_wisdom = self._load_council_wisdom()
        
        # Initialize syllable processor
        self.syllable_processor = AdvancedSyllableProcessor()
        
        self.logger.info("Advanced Word Extraction System initialized")
    
    def _load_mindfulness_vocabulary(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive mindfulness vocabulary with metadata"""
        return {
            # Core Mindfulness Terms
            "awareness": {
                "category": "core_mindfulness",
                "relevance": 1.0,
                "meditation_focus": "Present moment consciousness",
                "etymology": "Old English 'gewær' - watchful, cautious",
                "journal_prompt": "What am I becoming aware of in this moment?"
            },
            "presence": {
                "category": "core_mindfulness",
                "relevance": 1.0,
                "meditation_focus": "Being fully here and now",
                "etymology": "Latin 'praesentia' - being before",
                "journal_prompt": "How can I cultivate deeper presence today?"
            },
            "meditation": {
                "category": "practice",
                "relevance": 1.0,
                "meditation_focus": "Contemplative practice",
                "etymology": "Latin 'meditatus' - to think over",
                "journal_prompt": "What insights arise from my meditation practice?"
            },
            "compassion": {
                "category": "emotional_intelligence",
                "relevance": 0.9,
                "meditation_focus": "Loving-kindness cultivation",
                "etymology": "Latin 'compassio' - suffering with",
                "journal_prompt": "How can I extend compassion to myself and others?"
            },
            "wisdom": {
                "category": "wisdom_traditions",
                "relevance": 0.9,
                "meditation_focus": "Deep understanding cultivation",
                "etymology": "Old English 'wisdom' - knowledge, learning",
                "journal_prompt": "What wisdom is emerging from my experience?"
            },
            "transformation": {
                "category": "growth",
                "relevance": 0.8,
                "meditation_focus": "Change and evolution",
                "etymology": "Latin 'transformare' - to change shape",
                "journal_prompt": "What transformation am I experiencing?"
            },
            "authenticity": {
                "category": "self_discovery",
                "relevance": 0.8,
                "meditation_focus": "True self expression",
                "etymology": "Greek 'authentikos' - original, genuine",
                "journal_prompt": "How am I expressing my authentic self?"
            },
            "creativity": {
                "category": "creative_expression",
                "relevance": 0.7,
                "meditation_focus": "Creative flow cultivation",
                "etymology": "Latin 'creare' - to bring forth",
                "journal_prompt": "What wants to be created through me?"
            },
            "resilience": {
                "category": "strength",
                "relevance": 0.8,
                "meditation_focus": "Inner strength development",
                "etymology": "Latin 'resilire' - to spring back",
                "journal_prompt": "How has my resilience grown through challenges?"
            },
            "interconnection": {
                "category": "unity",
                "relevance": 0.9,
                "meditation_focus": "Universal connection",
                "etymology": "Latin 'inter' + 'connexio' - between connection",
                "journal_prompt": "How do I experience my connection to all life?"
            }
        }
    
    def _load_theme_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load theme patterns for content analysis"""
        return {
            "mindfulness_core": {
                "keywords": ["mindful", "aware", "present", "conscious", "attention", "focus"],
                "meditation_focus": "Present moment awareness",
                "journal_prompts": [
                    "What does mindfulness mean to me today?",
                    "How can I bring more awareness to daily activities?",
                    "What patterns of attention am I noticing?"
                ]
            },
            "emotional_wisdom": {
                "keywords": ["emotion", "feeling", "heart", "compassion", "empathy", "love"],
                "meditation_focus": "Emotional intelligence and heart wisdom",
                "journal_prompts": [
                    "What emotions are present for me right now?",
                    "How can I respond to emotions with wisdom?",
                    "What is my heart teaching me?"
                ]
            },
            "spiritual_growth": {
                "keywords": ["spirit", "soul", "divine", "sacred", "transcend", "enlighten"],
                "meditation_focus": "Spiritual development and connection",
                "journal_prompts": [
                    "How am I growing spiritually?",
                    "What feels sacred in my life?",
                    "How do I connect with the divine?"
                ]
            },
            "creative_expression": {
                "keywords": ["create", "art", "express", "imagine", "inspire", "vision"],
                "meditation_focus": "Creative flow and artistic expression",
                "journal_prompts": [
                    "What wants to be created through me?",
                    "How does creativity serve my growth?",
                    "What inspires my creative expression?"
                ]
            },
            "wisdom_traditions": {
                "keywords": ["wisdom", "tradition", "ancient", "teaching", "philosophy", "truth"],
                "meditation_focus": "Timeless wisdom and universal truths",
                "journal_prompts": [
                    "What wisdom traditions speak to me?",
                    "How do ancient teachings apply to modern life?",
                    "What universal truths am I discovering?"
                ]
            },
            "transformation_growth": {
                "keywords": ["transform", "change", "grow", "evolve", "develop", "journey"],
                "meditation_focus": "Personal transformation and growth",
                "journal_prompts": [
                    "How am I transforming?",
                    "What growth edges am I exploring?",
                    "What is my transformation teaching others?"
                ]
            }
        }
    
    def _load_council_wisdom(self) -> Dict[str, str]:
        """Load Council of Consciousness wisdom for content analysis"""
        return {
            "rick_rubin": "Strip away the unnecessary to reveal the essential truth in every word",
            "angela_davis": "Ensure language serves liberation and accessibility for all people",
            "octavia_butler": "See the transformational possibilities hidden within every text",
            "wayne_dyer": "Extract wisdom that serves the highest good of all beings",
            "saul_williams": "Bridge cultures and communities through the power of language",
            "bruce_lee": "Adapt analysis to the unique flow of each document",
            "kobe_bryant": "Pursue excellence in every aspect of content processing",
            "william_donahue": "Recognize the sacred geometry within linguistic patterns",
            "morgueofficial": "Find the contemporary wisdom in ancient and modern texts",
            "rodney_mullen": "Innovate new ways to understand and process language"
        }
    
    def analyze_content(self, 
                       text: str, 
                       content_type: Optional[ContentType] = None) -> ContentAnalysis:
        """
        Perform comprehensive content analysis for puzzle generation
        
        Args:
            text: The text content to analyze
            content_type: Optional content type hint
            
        Returns:
            ContentAnalysis object with comprehensive results
        """
        self.logger.info("Starting comprehensive content analysis")
        
        # Detect content type if not provided
        if content_type is None:
            content_type = self._detect_content_type(text)
        
        # Extract and analyze words
        word_analyses = self._analyze_words(text)
        
        # Analyze themes
        theme_analyses = self._analyze_themes(text, word_analyses)
        
        # Calculate overall metrics
        overall_complexity = self._calculate_overall_complexity(word_analyses)
        mindfulness_score = self._calculate_mindfulness_integration_score(word_analyses, theme_analyses)
        
        # Determine difficulty level
        difficulty_level = self._determine_difficulty_level(overall_complexity, mindfulness_score)
        
        # Recommend puzzle types
        recommended_puzzles = self._recommend_puzzle_types(word_analyses, theme_analyses, difficulty_level)
        
        # Apply Council of Consciousness wisdom
        council_insights = self._apply_council_wisdom(text, word_analyses, theme_analyses)
        
        return ContentAnalysis(
            content_type=content_type,
            difficulty_level=difficulty_level,
            word_analyses=word_analyses,
            theme_analyses=theme_analyses,
            overall_complexity=overall_complexity,
            mindfulness_integration_score=mindfulness_score,
            recommended_puzzle_types=recommended_puzzles,
            council_wisdom=council_insights
        )
    
    def _detect_content_type(self, text: str) -> ContentType:
        """Detect the type of content based on linguistic patterns"""
        text_lower = text.lower()
        
        # Count indicators for each content type
        type_scores = {
            ContentType.MINDFULNESS: 0,
            ContentType.SPIRITUAL: 0,
            ContentType.ACADEMIC: 0,
            ContentType.CREATIVE: 0,
            ContentType.PHILOSOPHICAL: 0,
            ContentType.SCIENTIFIC: 0,
            ContentType.LITERARY: 0
        }
        
        # Mindfulness indicators
        mindfulness_terms = ["mindful", "meditation", "awareness", "present", "conscious", "breath"]
        type_scores[ContentType.MINDFULNESS] = sum(text_lower.count(term) for term in mindfulness_terms)
        
        # Spiritual indicators
        spiritual_terms = ["spirit", "soul", "divine", "sacred", "enlighten", "transcend"]
        type_scores[ContentType.SPIRITUAL] = sum(text_lower.count(term) for term in spiritual_terms)
        
        # Academic indicators
        academic_terms = ["research", "study", "analysis", "theory", "hypothesis", "methodology"]
        type_scores[ContentType.ACADEMIC] = sum(text_lower.count(term) for term in academic_terms)
        
        # Creative indicators
        creative_terms = ["create", "art", "imagine", "inspire", "express", "vision"]
        type_scores[ContentType.CREATIVE] = sum(text_lower.count(term) for term in creative_terms)
        
        # Philosophical indicators
        philosophical_terms = ["philosophy", "wisdom", "truth", "meaning", "existence", "reality"]
        type_scores[ContentType.PHILOSOPHICAL] = sum(text_lower.count(term) for term in philosophical_terms)
        
        # Scientific indicators
        scientific_terms = ["science", "experiment", "data", "evidence", "quantum", "energy"]
        type_scores[ContentType.SCIENTIFIC] = sum(text_lower.count(term) for term in scientific_terms)
        
        # Literary indicators
        literary_terms = ["story", "narrative", "character", "plot", "metaphor", "symbol"]
        type_scores[ContentType.LITERARY] = sum(text_lower.count(term) for term in literary_terms)
        
        # Return the type with the highest score
        max_type = max(type_scores, key=type_scores.get)
        return max_type if type_scores[max_type] > 0 else ContentType.GENERAL
    
    def _analyze_words(self, text: str) -> List[WordAnalysis]:
        """Analyze individual words for puzzle generation"""
        # Tokenize and clean text
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and len(word) >= 3]
        words = [word for word in words if word not in self.stop_words]
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Get POS tags
        pos_tags = dict(pos_tag(words))
        
        word_analyses = []
        
        # Analyze top words (limit to prevent overwhelming results)
        for word, frequency in word_freq.most_common(100):
            analysis = self._analyze_single_word(word, frequency, pos_tags.get(word, 'NN'))
            word_analyses.append(analysis)
        
        return word_analyses
    
    def _analyze_single_word(self, word: str, frequency: int, pos: str) -> WordAnalysis:
        """Perform detailed analysis of a single word"""
        # Get syllable information
        syllables = self.syllable_processor.split_syllables(word)
        syllable_count = len(syllables)
        
        # Calculate complexity score
        complexity_score = self._calculate_word_complexity(word, syllable_count, pos)
        
        # Calculate mindfulness relevance
        mindfulness_relevance = self._calculate_mindfulness_relevance(word)
        
        # Identify themes
        themes = self._identify_word_themes(word)
        
        # Generate etymology hints
        etymology_hints = self._generate_etymology_hints(word)
        
        # Generate meditation prompt
        meditation_prompt = self._generate_meditation_prompt(word)
        
        # Generate journal integration
        journal_integration = self._generate_journal_integration(word)
        
        return WordAnalysis(
            word=word,
            syllables=syllables,
            syllable_count=syllable_count,
            part_of_speech=pos,
            frequency=frequency,
            complexity_score=complexity_score,
            mindfulness_relevance=mindfulness_relevance,
            themes=themes,
            etymology_hints=etymology_hints,
            meditation_prompt=meditation_prompt,
            journal_integration=journal_integration
        )
    
    def _calculate_word_complexity(self, word: str, syllable_count: int, pos: str) -> float:
        """Calculate complexity score for a word"""
        # Base complexity from length and syllables
        length_score = min(len(word) / 15, 1.0)  # Normalize to 0-1
        syllable_score = min(syllable_count / 6, 1.0)  # Normalize to 0-1
        
        # POS complexity weights
        pos_weights = {
            'NN': 0.5,   # Noun
            'VB': 0.6,   # Verb
            'JJ': 0.7,   # Adjective
            'RB': 0.8,   # Adverb
            'VBG': 0.9,  # Gerund
            'VBN': 0.9   # Past participle
        }
        
        pos_score = pos_weights.get(pos[:2], 0.5)
        
        # Combine scores
        complexity = (length_score + syllable_score + pos_score) / 3
        return min(complexity, 1.0)
    
    def _calculate_mindfulness_relevance(self, word: str) -> float:
        """Calculate how relevant a word is to mindfulness practice"""
        if word in self.mindfulness_vocabulary:
            return self.mindfulness_vocabulary[word]["relevance"]
        
        # Check for partial matches
        relevance = 0.0
        for mindful_word, data in self.mindfulness_vocabulary.items():
            if mindful_word in word or word in mindful_word:
                relevance = max(relevance, data["relevance"] * 0.7)
        
        # Check theme patterns
        for theme, pattern_data in self.theme_patterns.items():
            if any(keyword in word for keyword in pattern_data["keywords"]):
                relevance = max(relevance, 0.5)
        
        return relevance
    
    def _identify_word_themes(self, word: str) -> List[str]:
        """Identify themes associated with a word"""
        themes = []
        
        for theme_name, pattern_data in self.theme_patterns.items():
            if any(keyword in word for keyword in pattern_data["keywords"]):
                themes.append(theme_name)
        
        # Check mindfulness vocabulary categories
        if word in self.mindfulness_vocabulary:
            category = self.mindfulness_vocabulary[word]["category"]
            if category not in themes:
                themes.append(category)
        
        return themes
    
    def _generate_etymology_hints(self, word: str) -> List[str]:
        """Generate etymology hints for a word"""
        if word in self.mindfulness_vocabulary:
            etymology = self.mindfulness_vocabulary[word]["etymology"]
            return [etymology]
        
        # Generate basic etymology hints based on common patterns
        hints = []
        
        # Common prefixes and their meanings
        prefixes = {
            'un': 'not, opposite of',
            're': 'again, back',
            'pre': 'before',
            'dis': 'not, opposite of',
            'mis': 'wrongly',
            'over': 'too much',
            'under': 'too little',
            'out': 'beyond',
            'up': 'higher'
        }
        
        for prefix, meaning in prefixes.items():
            if word.startswith(prefix):
                hints.append(f"Prefix '{prefix}' means '{meaning}'")
        
        # Common suffixes and their meanings
        suffixes = {
            'ness': 'state or quality of',
            'ment': 'result or process',
            'tion': 'action or process',
            'able': 'capable of being',
            'ful': 'full of',
            'less': 'without',
            'ly': 'in the manner of'
        }
        
        for suffix, meaning in suffixes.items():
            if word.endswith(suffix):
                hints.append(f"Suffix '{suffix}' means '{meaning}'")
        
        return hints if hints else ["Explore the roots and origins of this word"]
    
    def _generate_meditation_prompt(self, word: str) -> str:
        """Generate a meditation prompt for a word"""
        if word in self.mindfulness_vocabulary:
            return self.mindfulness_vocabulary[word]["journal_prompt"]
        
        # Generate contextual prompts based on word characteristics
        prompts = [
            f"Breathe deeply and contemplate the essence of '{word}'",
            f"How does the word '{word}' resonate in your body?",
            f"What wisdom does '{word}' offer your journey?",
            f"Sit quietly and let '{word}' reveal its deeper meaning",
            f"How might '{word}' guide your mindful awareness?"
        ]
        
        # Choose prompt based on word hash for consistency
        prompt_index = hash(word) % len(prompts)
        return prompts[prompt_index]
    
    def _generate_journal_integration(self, word: str) -> str:
        """Generate journal integration suggestion for a word"""
        integrations = [
            f"Write about how '{word}' appears in your daily life",
            f"Explore the relationship between '{word}' and your personal growth",
            f"Reflect on a time when '{word}' was particularly meaningful",
            f"Consider how '{word}' connects to your values and intentions",
            f"Describe how embodying '{word}' might transform your experience"
        ]
        
        # Choose integration based on word hash for consistency
        integration_index = hash(word) % len(integrations)
        return integrations[integration_index]
    
    def _analyze_themes(self, text: str, word_analyses: List[WordAnalysis]) -> List[ThemeAnalysis]:
        """Analyze thematic content in the text"""
        theme_scores = defaultdict(float)
        theme_words = defaultdict(list)
        
        # Collect theme information from word analyses
        for word_analysis in word_analyses:
            for theme in word_analysis.themes:
                theme_scores[theme] += word_analysis.mindfulness_relevance * word_analysis.frequency
                theme_words[theme].append(word_analysis.word)
        
        theme_analyses = []
        
        for theme_name, score in theme_scores.items():
            if theme_name in self.theme_patterns:
                pattern_data = self.theme_patterns[theme_name]
                
                theme_analysis = ThemeAnalysis(
                    theme_name=theme_name,
                    keywords=theme_words[theme_name],
                    relevance_score=min(score / 10, 1.0),  # Normalize
                    word_count=len(theme_words[theme_name]),
                    mindfulness_connection=pattern_data["meditation_focus"],
                    meditation_focus=pattern_data["meditation_focus"],
                    journal_prompts=pattern_data["journal_prompts"]
                )
                
                theme_analyses.append(theme_analysis)
        
        # Sort by relevance score
        theme_analyses.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return theme_analyses[:10]  # Return top 10 themes
    
    def _calculate_overall_complexity(self, word_analyses: List[WordAnalysis]) -> float:
        """Calculate overall complexity of the content"""
        if not word_analyses:
            return 0.0
        
        complexity_scores = [wa.complexity_score for wa in word_analyses]
        return sum(complexity_scores) / len(complexity_scores)
    
    def _calculate_mindfulness_integration_score(self, 
                                               word_analyses: List[WordAnalysis], 
                                               theme_analyses: List[ThemeAnalysis]) -> float:
        """Calculate how well the content integrates with mindfulness practice"""
        if not word_analyses:
            return 0.0
        
        # Word-level mindfulness relevance
        word_mindfulness = sum(wa.mindfulness_relevance for wa in word_analyses) / len(word_analyses)
        
        # Theme-level mindfulness relevance
        if theme_analyses:
            theme_mindfulness = sum(ta.relevance_score for ta in theme_analyses) / len(theme_analyses)
        else:
            theme_mindfulness = 0.0
        
        # Combined score
        return (word_mindfulness + theme_mindfulness) / 2
    
    def _determine_difficulty_level(self, complexity: float, mindfulness_score: float) -> DifficultyLevel:
        """Determine appropriate difficulty level for puzzle generation"""
        combined_score = (complexity + mindfulness_score) / 2
        
        if combined_score < 0.3:
            return DifficultyLevel.BEGINNER
        elif combined_score < 0.6:
            return DifficultyLevel.INTERMEDIATE
        elif combined_score < 0.8:
            return DifficultyLevel.ADVANCED
        else:
            return DifficultyLevel.EXPERT
    
    def _recommend_puzzle_types(self, 
                               word_analyses: List[WordAnalysis], 
                               theme_analyses: List[ThemeAnalysis],
                               difficulty_level: DifficultyLevel) -> List[str]:
        """Recommend appropriate puzzle types based on content analysis"""
        recommendations = []
        
        # Always recommend SyllaFlow as primary puzzle type
        recommendations.append("syllaflow")
        
        # Analyze word characteristics for additional recommendations
        avg_word_length = sum(len(wa.word) for wa in word_analyses) / len(word_analyses) if word_analyses else 0
        avg_syllables = sum(wa.syllable_count for wa in word_analyses) / len(word_analyses) if word_analyses else 0
        
        # Word search recommendations
        if avg_word_length >= 6 and len(word_analyses) >= 20:
            recommendations.append("word_search")
        
        # Crossword recommendations
        if avg_syllables >= 2 and len(theme_analyses) >= 3:
            recommendations.append("crossword")
        
        # Anagram recommendations
        if avg_word_length >= 5 and difficulty_level in [DifficultyLevel.INTERMEDIATE, DifficultyLevel.ADVANCED]:
            recommendations.append("anagram")
        
        # Word scramble recommendations
        if difficulty_level == DifficultyLevel.BEGINNER:
            recommendations.append("word_scramble")
        
        return recommendations
    
    def _apply_council_wisdom(self, 
                            text: str, 
                            word_analyses: List[WordAnalysis], 
                            theme_analyses: List[ThemeAnalysis]) -> Dict[str, str]:
        """Apply Council of Consciousness wisdom to content analysis"""
        insights = {}
        
        # Rick Rubin: Simplicity and essence
        essential_words = [wa.word for wa in word_analyses if wa.mindfulness_relevance > 0.7]
        insights["rick_rubin"] = f"Essential words for authentic expression: {', '.join(essential_words[:5])}"
        
        # Angela Davis: Accessibility and liberation
        accessible_words = [wa.word for wa in word_analyses if wa.complexity_score < 0.5]
        insights["angela_davis"] = f"Accessible words for inclusive practice: {', '.join(accessible_words[:5])}"
        
        # Octavia Butler: Transformation possibilities
        transformative_themes = [ta.theme_name for ta in theme_analyses if "transform" in ta.theme_name or "growth" in ta.theme_name]
        insights["octavia_butler"] = f"Transformational themes discovered: {', '.join(transformative_themes)}"
        
        # Wayne Dyer: Wisdom extraction
        wisdom_words = [wa.word for wa in word_analyses if any("wisdom" in theme for theme in wa.themes)]
        insights["wayne_dyer"] = f"Wisdom-bearing words: {', '.join(wisdom_words[:5])}"
        
        # Saul Williams: Cultural bridge-building
        diverse_themes = [ta.theme_name for ta in theme_analyses]
        insights["saul_williams"] = f"Cultural bridge themes: {', '.join(diverse_themes[:3])}"
        
        return insights
    
    def export_for_syllaflow(self, analysis: ContentAnalysis) -> Dict[str, Any]:
        """Export analysis results in SyllaFlow-compatible format"""
        return {
            "content_analysis": {
                "content_type": analysis.content_type.value,
                "difficulty_level": analysis.difficulty_level.value,
                "overall_complexity": analysis.overall_complexity,
                "mindfulness_integration_score": analysis.mindfulness_integration_score
            },
            "words": [
                {
                    "word": wa.word,
                    "syllables": wa.syllables,
                    "syllable_count": wa.syllable_count,
                    "complexity_score": wa.complexity_score,
                    "mindfulness_relevance": wa.mindfulness_relevance,
                    "meditation_prompt": wa.meditation_prompt,
                    "journal_integration": wa.journal_integration,
                    "themes": wa.themes
                }
                for wa in analysis.word_analyses
            ],
            "themes": [
                {
                    "name": ta.theme_name,
                    "relevance_score": ta.relevance_score,
                    "meditation_focus": ta.meditation_focus,
                    "journal_prompts": ta.journal_prompts,
                    "keywords": ta.keywords
                }
                for ta in analysis.theme_analyses
            ],
            "puzzle_recommendations": analysis.recommended_puzzle_types,
            "council_wisdom": analysis.council_wisdom
        }

class AdvancedSyllableProcessor:
    """
    Advanced syllable processing with linguistic rules
    
    Enhanced syllable detection using phonetic patterns and linguistic rules
    for accurate syllable-based directional word search mechanics.
    """
    
    def __init__(self):
        """Initialize advanced syllable processor"""
        self.vowels = set('aeiouAEIOU')
        self.consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        
        # Common consonant clusters that don't split syllables
        self.consonant_clusters = {
            'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr',
            'sc', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'tr', 'tw',
            'th', 'ch', 'sh', 'wh', 'ph', 'gh', 'ck', 'ng'
        }
        
        # Silent letter patterns
        self.silent_patterns = {
            'e$': r'e$',  # Silent e at end
            'ed$': r'ed$',  # Silent ed at end (usually)
            'le$': r'le$'   # Silent le at end
        }
    
    def split_syllables(self, word: str) -> List[str]:
        """Split word into syllables using advanced linguistic rules"""
        word = word.lower().strip()
        
        if len(word) <= 2:
            return [word]
        
        # Handle special cases
        if word.endswith('le') and len(word) > 3 and word[-3] in self.consonants:
            # Handle -ble, -ple, -tle patterns
            return self._split_consonant_le(word)
        
        syllables = []
        current_syllable = ""
        i = 0
        
        while i < len(word):
            char = word[i]
            current_syllable += char
            
            # Look ahead for syllable boundaries
            if i < len(word) - 1:
                if self._is_syllable_boundary(word, i):
                    syllables.append(current_syllable)
                    current_syllable = ""
            
            i += 1
        
        # Add remaining characters
        if current_syllable:
            if syllables:
                syllables[-1] += current_syllable
            else:
                syllables.append(current_syllable)
        
        # Post-process to ensure valid syllables
        syllables = self._post_process_syllables(syllables)
        
        return syllables if syllables else [word]
    
    def _is_syllable_boundary(self, word: str, position: int) -> bool:
        """Determine if position represents a syllable boundary"""
        if position >= len(word) - 1:
            return False
        
        current = word[position]
        next_char = word[position + 1]
        
        # Vowel-consonant boundary
        if current in self.vowels and next_char in self.consonants:
            # Check for consonant clusters
            if position + 2 < len(word):
                cluster = word[position + 1:position + 3]
                if cluster.lower() in self.consonant_clusters:
                    return False
            
            # Check for double consonants
            if position + 2 < len(word) and word[position + 1] == word[position + 2]:
                return True
            
            return True
        
        # Consonant-vowel boundary (less common split point)
        if current in self.consonants and next_char in self.vowels:
            # Only split if we have a vowel before the consonant
            if position > 0 and word[position - 1] in self.vowels:
                return True
        
        return False
    
    def _split_consonant_le(self, word: str) -> List[str]:
        """Handle words ending in consonant + le"""
        if len(word) <= 3:
            return [word]
        
        # Split before the consonant + le
        split_point = len(word) - 3
        return [word[:split_point], word[split_point:]]
    
    def _post_process_syllables(self, syllables: List[str]) -> List[str]:
        """Post-process syllables to ensure validity"""
        if not syllables:
            return syllables
        
        processed = []
        
        for i, syllable in enumerate(syllables):
            # Ensure each syllable has at least one vowel (except for final syllables)
            if not any(char in self.vowels for char in syllable):
                if i > 0:
                    # Merge with previous syllable
                    processed[-1] += syllable
                elif i < len(syllables) - 1:
                    # Merge with next syllable
                    syllables[i + 1] = syllable + syllables[i + 1]
                else:
                    # Keep as is if it's the only syllable
                    processed.append(syllable)
            else:
                processed.append(syllable)
        
        return processed

def main():
    """Test the advanced word extraction system"""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize the system
    extractor = AdvancedWordExtractor()
    
    # Test with sample mindfulness content
    test_content = """
    Mindfulness is the practice of purposeful, non-judgmental awareness of the present moment.
    Through meditation and contemplation, we cultivate wisdom, compassion, and authentic presence.
    This transformative journey involves breathing exercises, mindful observation, and deep reflection.
    
    As we develop our practice, we discover inner peace, resilience, and profound interconnection
    with all life. The path of mindfulness leads to greater creativity, emotional intelligence,
    and spiritual awakening. Each moment offers an opportunity for growth and transformation.
    """
    
    print("=== Advanced Word Extraction System Test ===")
    
    try:
        # Perform comprehensive analysis
        analysis = extractor.analyze_content(test_content)
        
        print(f"Content Type: {analysis.content_type.value}")
        print(f"Difficulty Level: {analysis.difficulty_level.value}")
        print(f"Overall Complexity: {analysis.overall_complexity:.2f}")
        print(f"Mindfulness Integration Score: {analysis.mindfulness_integration_score:.2f}")
        
        print(f"\nTop 10 Words:")
        for i, word_analysis in enumerate(analysis.word_analyses[:10], 1):
            print(f"{i}. {word_analysis.word} (syllables: {'-'.join(word_analysis.syllables)})")
            print(f"   Complexity: {word_analysis.complexity_score:.2f}, Mindfulness: {word_analysis.mindfulness_relevance:.2f}")
            print(f"   Meditation: {word_analysis.meditation_prompt}")
        
        print(f"\nTop Themes:")
        for theme_analysis in analysis.theme_analyses[:5]:
            print(f"- {theme_analysis.theme_name} (score: {theme_analysis.relevance_score:.2f})")
            print(f"  Focus: {theme_analysis.meditation_focus}")
        
        print(f"\nRecommended Puzzle Types: {', '.join(analysis.recommended_puzzle_types)}")
        
        print(f"\nCouncil of Consciousness Insights:")
        for persona, insight in analysis.council_wisdom.items():
            print(f"- {persona}: {insight}")
        
        # Export for SyllaFlow
        export_data = extractor.export_for_syllaflow(analysis)
        print(f"\nExport data contains {len(export_data['words'])} words and {len(export_data['themes'])} themes")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

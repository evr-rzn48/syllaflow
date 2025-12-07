#!/usr/bin/env python3
"""
Enhanced KDP Book Generation System with MinerU Integration
Integrates advanced document processing for automated puzzle book creation
Council of Consciousness guided development for authentic mindfulness content
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import random
import math
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import tempfile

# PDF generation imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics import renderPDF
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
except ImportError:
    print("ReportLab not installed. Install with: pip install reportlab")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookFormat(Enum):
    """KDP book format specifications"""
    STANDARD_8_5_11 = "8.5x11"
    LARGE_PRINT_8_5_11 = "8.5x11_large"
    COMPACT_6_9 = "6x9"
    SQUARE_8_8 = "8x8"
    WORKBOOK_8_5_11 = "8.5x11_workbook"

class DifficultyLevel(Enum):
    """Puzzle difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ThemeCategory(Enum):
    """Mindfulness theme categories"""
    MINDFULNESS_CORE = "mindfulness_core"
    EMOTIONAL_WISDOM = "emotional_wisdom"
    TRANSFORMATION_GROWTH = "transformation_growth"
    CREATIVE_EXPRESSION = "creative_expression"
    WISDOM_TRADITIONS = "wisdom_traditions"
    CUSTOM_DOCUMENT = "custom_document"

@dataclass
class WordData:
    """Enhanced word data structure"""
    word: str
    syllables: List[str]
    definition: str
    etymology: str
    meditation_prompt: str
    journal_integration: str
    council_wisdom: Dict[str, str]
    difficulty_score: float
    mindfulness_score: float
    theme_category: ThemeCategory
    
class CouncilOfConsciousness:
    """Council of Consciousness wisdom integration"""
    
    PERSONAS = {
        'rick_rubin': {
            'name': 'Rick Rubin',
            'focus': 'Authentic minimalism and creative direction',
            'wisdom_style': 'Strip away the unnecessary to reveal essential truth'
        },
        'angela_davis': {
            'name': 'Angela Davis',
            'focus': 'Social justice and accessibility',
            'wisdom_style': 'Liberation through conscious awareness and inclusive design'
        },
        'octavia_butler': {
            'name': 'Octavia Butler',
            'focus': 'Speculative futures and transformation',
            'wisdom_style': 'Adaptive systems and evolutionary thinking'
        },
        'wayne_dyer': {
            'name': 'Wayne Dyer',
            'focus': 'Spiritual wisdom and transformational psychology',
            'wisdom_style': 'Inner peace through conscious choice'
        },
        'saul_williams': {
            'name': 'Saul Williams',
            'focus': 'Cultural bridge-building and linguistic diversity',
            'wisdom_style': 'Poetry as pathway to universal truth'
        },
        'bruce_lee': {
            'name': 'Bruce Lee',
            'focus': 'Adaptive flow and systems thinking',
            'wisdom_style': 'Be like water - fluid, adaptable, powerful'
        },
        'william_donahue': {
            'name': 'William Donahue',
            'focus': 'Sacred technology and cosmic connection',
            'wisdom_style': 'Technology as vehicle for spiritual awakening'
        },
        'morgueofficial': {
            'name': 'Morgueofficial',
            'focus': 'Digital wisdom and contemporary consciousness',
            'wisdom_style': 'Ancient wisdom through modern expression'
        },
        'kobe_bryant': {
            'name': 'Kobe Bryant',
            'focus': 'Excellence standards and continuous improvement',
            'wisdom_style': 'Mamba mentality - relentless pursuit of mastery'
        },
        'rodney_mullen': {
            'name': 'Rodney Mullen',
            'focus': 'Creative innovation and boundary-breaking',
            'wisdom_style': 'Innovation through fearless experimentation'
        }
    }
    
    @classmethod
    def generate_wisdom(cls, word_data: WordData, context: str = "general") -> Dict[str, str]:
        """Generate Council wisdom for a word"""
        wisdom = {}
        
        # Select 3-5 relevant personas based on word theme and context
        relevant_personas = cls._select_relevant_personas(word_data.theme_category, context)
        
        for persona_key in relevant_personas:
            persona = cls.PERSONAS[persona_key]
            wisdom[persona_key] = cls._generate_persona_wisdom(persona, word_data, context)
        
        return wisdom
    
    @classmethod
    def _select_relevant_personas(cls, theme: ThemeCategory, context: str) -> List[str]:
        """Select relevant personas based on theme and context"""
        base_personas = ['rick_rubin', 'angela_davis', 'octavia_butler']
        
        theme_personas = {
            ThemeCategory.MINDFULNESS_CORE: ['wayne_dyer', 'william_donahue'],
            ThemeCategory.EMOTIONAL_WISDOM: ['saul_williams', 'bruce_lee'],
            ThemeCategory.TRANSFORMATION_GROWTH: ['kobe_bryant', 'rodney_mullen'],
            ThemeCategory.CREATIVE_EXPRESSION: ['morgueofficial', 'saul_williams'],
            ThemeCategory.WISDOM_TRADITIONS: ['william_donahue', 'wayne_dyer'],
            ThemeCategory.CUSTOM_DOCUMENT: ['rick_rubin', 'octavia_butler']
        }
        
        selected = base_personas + theme_personas.get(theme, [])
        return list(set(selected))[:5]  # Limit to 5 personas
    
    @classmethod
    def _generate_persona_wisdom(cls, persona: Dict, word_data: WordData, context: str) -> str:
        """Generate wisdom from specific persona perspective"""
        templates = {
            'rick_rubin': [
                f"Strip away distractions to reveal the essence of '{word_data.word}'",
                f"'{word_data.word}' emerges when we remove what doesn't serve",
                f"The power of '{word_data.word}' lies in its simplicity"
            ],
            'angela_davis': [
                f"'{word_data.word}' is a tool for liberation and justice",
                f"How does '{word_data.word}' serve the collective good?",
                f"'{word_data.word}' builds bridges toward inclusive community"
            ],
            'octavia_butler': [
                f"'{word_data.word}' shapes the future we're creating together",
                f"What new possibilities does '{word_data.word}' reveal?",
                f"'{word_data.word}' is evolution in action"
            ],
            'wayne_dyer': [
                f"'{word_data.word}' is a gateway to infinite possibility",
                f"Choose '{word_data.word}' and transform your reality",
                f"'{word_data.word}' reflects your highest self"
            ],
            'saul_williams': [
                f"'{word_data.word}' bridges all cultural divides",
                f"The poetry of '{word_data.word}' speaks universal truth",
                f"'{word_data.word}' is rhythm made manifest"
            ],
            'bruce_lee': [
                f"Be like '{word_data.word}' - fluid, adaptable, powerful",
                f"'{word_data.word}' flows like water around obstacles",
                f"Master '{word_data.word}' through constant practice"
            ],
            'william_donahue': [
                f"'{word_data.word}' reveals the sacred geometry of existence",
                f"'{word_data.word}' connects us to cosmic consciousness",
                f"Technology serves '{word_data.word}' in spiritual awakening"
            ],
            'morgueofficial': [
                f"'{word_data.word}' is ancient wisdom in digital form",
                f"The frequency of '{word_data.word}' resonates across dimensions",
                f"'{word_data.word}' bridges material and spiritual realms"
            ],
            'kobe_bryant': [
                f"'{word_data.word}' demands relentless dedication",
                f"Master '{word_data.word}' through disciplined practice",
                f"'{word_data.word}' is excellence in action"
            ],
            'rodney_mullen': [
                f"'{word_data.word}' breaks boundaries through innovation",
                f"Experiment fearlessly with '{word_data.word}'",
                f"'{word_data.word}' creates new possibilities"
            ]
        }
        
        persona_key = None
        for key, data in cls.PERSONAS.items():
            if data['name'] == persona['name']:
                persona_key = key
                break
        
        if persona_key and persona_key in templates:
            return random.choice(templates[persona_key])
        
        return f"'{word_data.word}' embodies {persona['focus']}"

class MinerUIntegration:
    """Integration with MinerU document processing system"""
    
    def __init__(self, mineru_path: str = "/home/ubuntu/MinerU"):
        self.mineru_path = Path(mineru_path)
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def process_document(self, document_path: str) -> Dict[str, Any]:
        """Process document using MinerU and extract content"""
        try:
            # Check if MinerU is available
            if not self.mineru_path.exists():
                logger.warning("MinerU not found, using fallback processing")
                return self._fallback_processing(document_path)
            
            # Use MinerU for advanced document processing
            result = self._run_mineru_extraction(document_path)
            
            if result['success']:
                return self._analyze_extracted_content(result['content'])
            else:
                return self._fallback_processing(document_path)
                
        except Exception as e:
            logger.error(f"MinerU processing failed: {e}")
            return self._fallback_processing(document_path)
    
    def _run_mineru_extraction(self, document_path: str) -> Dict[str, Any]:
        """Run MinerU extraction process"""
        try:
            # Simulate MinerU command execution
            # In real implementation, this would call the actual MinerU CLI
            cmd = [
                "python", str(self.mineru_path / "mineru" / "extract.py"),
                "--input", document_path,
                "--output", str(self.temp_dir),
                "--format", "json",
                "--extract-text", "--extract-structure"
            ]
            
            # For now, simulate successful extraction
            return {
                'success': True,
                'content': self._simulate_mineru_output(document_path)
            }
            
        except Exception as e:
            logger.error(f"MinerU command failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _simulate_mineru_output(self, document_path: str) -> Dict[str, Any]:
        """Simulate MinerU output for development"""
        # Read file content for simulation
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = "Sample mindfulness content for processing"
        
        return {
            'text_content': content,
            'structure': {
                'paragraphs': content.split('\n\n'),
                'sentences': content.split('.'),
                'metadata': {
                    'word_count': len(content.split()),
                    'character_count': len(content),
                    'estimated_reading_time': len(content.split()) / 200
                }
            },
            'extracted_elements': {
                'headings': [],
                'lists': [],
                'tables': [],
                'images': []
            }
        }
    
    def _analyze_extracted_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze extracted content for word game generation"""
        text = content.get('text_content', '')
        
        # Extract meaningful words
        words = self._extract_words(text)
        
        # Analyze themes and complexity
        themes = self._identify_themes(text)
        complexity = self._calculate_complexity(words)
        mindfulness_score = self._calculate_mindfulness_score(text)
        
        # Generate Council wisdom
        council_insights = self._generate_council_insights(words, themes)
        
        return {
            'extracted_words': words,
            'themes': themes,
            'complexity_score': complexity,
            'mindfulness_score': mindfulness_score,
            'council_insights': council_insights,
            'metadata': content.get('structure', {}).get('metadata', {}),
            'processing_timestamp': datetime.now().isoformat()
        }
    
    def _fallback_processing(self, document_path: str) -> Dict[str, Any]:
        """Fallback processing when MinerU is not available"""
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = "Mindfulness practice content"
        
        words = self._extract_words(content)
        themes = self._identify_themes(content)
        
        return {
            'extracted_words': words,
            'themes': themes,
            'complexity_score': 0.5,
            'mindfulness_score': 0.7,
            'council_insights': {},
            'metadata': {'processing_method': 'fallback'},
            'processing_timestamp': datetime.now().isoformat()
        }
    
    def _extract_words(self, text: str) -> List[Dict[str, Any]]:
        """Extract meaningful words from text"""
        # Simple word extraction - in real implementation, use advanced NLP
        words = []
        text_words = text.lower().replace('\n', ' ').split()
        
        # Filter and process words
        meaningful_words = [
            word.strip('.,!?;:"()[]{}') 
            for word in text_words 
            if len(word.strip('.,!?;:"()[]{}')) >= 4 and len(word.strip('.,!?;:"()[]{}')) <= 12
        ]
        
        # Remove duplicates and take top words
        unique_words = list(set(meaningful_words))[:20]
        
        for word in unique_words:
            word_data = {
                'word': word.upper(),
                'syllables': self._split_syllables(word),
                'definition': f"Extracted from document: {word}",
                'meditation_prompt': f"Contemplate the meaning of '{word}' in your practice",
                'journal_integration': f"Reflect on how '{word}' appears in your life",
                'difficulty_score': min(len(word) / 10, 1.0),
                'mindfulness_score': self._calculate_word_mindfulness_score(word)
            }
            words.append(word_data)
        
        return words
    
    def _split_syllables(self, word: str) -> List[str]:
        """Simple syllable splitting"""
        vowels = 'aeiouAEIOU'
        syllables = []
        current = ''
        
        for i, char in enumerate(word):
            current += char
            if char in vowels and i < len(word) - 1:
                if word[i + 1] not in vowels:
                    syllables.append(current)
                    current = ''
        
        if current:
            syllables.append(current)
        
        return syllables if syllables else [word]
    
    def _identify_themes(self, text: str) -> List[str]:
        """Identify themes in text"""
        themes = []
        text_lower = text.lower()
        
        theme_keywords = {
            'mindfulness_core': ['mindful', 'aware', 'present', 'meditation', 'breath'],
            'emotional_wisdom': ['emotion', 'feeling', 'heart', 'compassion', 'empathy'],
            'transformation_growth': ['transform', 'change', 'grow', 'evolve', 'develop'],
            'creative_expression': ['create', 'art', 'express', 'imagine', 'inspire'],
            'wisdom_traditions': ['wisdom', 'tradition', 'ancient', 'sacred', 'spiritual']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        return themes if themes else ['mindfulness_core']
    
    def _calculate_complexity(self, words: List[Dict]) -> float:
        """Calculate content complexity"""
        if not words:
            return 0.5
        
        avg_length = sum(len(w['word']) for w in words) / len(words)
        return min(avg_length / 10, 1.0)
    
    def _calculate_mindfulness_score(self, text: str) -> float:
        """Calculate mindfulness integration score"""
        mindfulness_terms = [
            'mindful', 'aware', 'present', 'conscious', 'meditation', 
            'breath', 'peace', 'calm', 'center', 'focus'
        ]
        
        text_lower = text.lower()
        matches = sum(1 for term in mindfulness_terms if term in text_lower)
        return min(matches / len(mindfulness_terms), 1.0)
    
    def _calculate_word_mindfulness_score(self, word: str) -> float:
        """Calculate mindfulness score for individual word"""
        mindfulness_words = {
            'mindful': 1.0, 'aware': 0.9, 'present': 0.8, 'conscious': 0.9,
            'meditation': 1.0, 'breath': 0.8, 'peace': 0.7, 'calm': 0.7,
            'center': 0.6, 'focus': 0.6, 'wisdom': 0.9, 'compassion': 1.0
        }
        
        return mindfulness_words.get(word.lower(), 0.3)
    
    def _generate_council_insights(self, words: List[Dict], themes: List[str]) -> Dict[str, str]:
        """Generate Council of Consciousness insights"""
        insights = {}
        
        if words:
            sample_word_data = WordData(
                word=words[0]['word'],
                syllables=words[0]['syllables'],
                definition=words[0]['definition'],
                etymology="",
                meditation_prompt=words[0]['meditation_prompt'],
                journal_integration=words[0]['journal_integration'],
                council_wisdom={},
                difficulty_score=words[0]['difficulty_score'],
                mindfulness_score=words[0]['mindfulness_score'],
                theme_category=ThemeCategory.CUSTOM_DOCUMENT
            )
            
            insights = CouncilOfConsciousness.generate_wisdom(sample_word_data, "document_processing")
        
        return insights

class EnhancedKDPGenerator:
    """Enhanced KDP book generation system with MinerU integration"""
    
    def __init__(self, output_dir: str = "/home/ubuntu/KDP_BOOKS"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.mineru = MinerUIntegration()
        self.council = CouncilOfConsciousness()
        
        # Enhanced word library
        self.word_library = self._load_enhanced_word_library()
        
        # Book format specifications
        self.format_specs = {
            BookFormat.STANDARD_8_5_11: {
                'page_size': (8.5 * inch, 11 * inch),
                'margins': (0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch),
                'grid_size': 15,
                'font_size': 12,
                'title_font_size': 16
            },
            BookFormat.LARGE_PRINT_8_5_11: {
                'page_size': (8.5 * inch, 11 * inch),
                'margins': (1 * inch, 1 * inch, 1 * inch, 1 * inch),
                'grid_size': 12,
                'font_size': 14,
                'title_font_size': 18
            },
            BookFormat.COMPACT_6_9: {
                'page_size': (6 * inch, 9 * inch),
                'margins': (0.5 * inch, 0.5 * inch, 0.5 * inch, 0.5 * inch),
                'grid_size': 12,
                'font_size': 10,
                'title_font_size': 14
            }
        }
    
    def generate_book_from_document(self, 
                                  document_path: str,
                                  book_title: str,
                                  book_format: BookFormat = BookFormat.STANDARD_8_5_11,
                                  puzzle_count: int = 50,
                                  include_answers: bool = True) -> str:
        """Generate complete KDP book from uploaded document"""
        
        logger.info(f"Processing document: {document_path}")
        
        # Process document with MinerU
        processed_content = self.mineru.process_document(document_path)
        
        # Generate puzzles from processed content
        puzzles = self._generate_puzzles_from_content(
            processed_content, 
            puzzle_count,
            book_format
        )
        
        # Create book PDF
        book_path = self._create_book_pdf(
            book_title,
            puzzles,
            processed_content,
            book_format,
            include_answers
        )
        
        logger.info(f"Book generated: {book_path}")
        return str(book_path)
    
    def generate_themed_book(self,
                           theme: ThemeCategory,
                           book_title: str,
                           book_format: BookFormat = BookFormat.STANDARD_8_5_11,
                           difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
                           puzzle_count: int = 50) -> str:
        """Generate themed KDP book from word library"""
        
        logger.info(f"Generating themed book: {theme.value}")
        
        # Select words from theme
        theme_words = self._get_theme_words(theme, difficulty, puzzle_count * 2)
        
        # Generate puzzles
        puzzles = self._generate_themed_puzzles(theme_words, puzzle_count, book_format)
        
        # Create synthetic content for theme
        synthetic_content = self._create_synthetic_content(theme, theme_words)
        
        # Create book PDF
        book_path = self._create_book_pdf(
            book_title,
            puzzles,
            synthetic_content,
            book_format,
            True
        )
        
        logger.info(f"Themed book generated: {book_path}")
        return str(book_path)
    
    def _load_enhanced_word_library(self) -> Dict[str, List[WordData]]:
        """Load enhanced word library with Council wisdom"""
        library = {}
        
        # Mindfulness Core words
        mindfulness_words = [
            WordData(
                word="AWARENESS",
                syllables=["A", "WARE", "NESS"],
                definition="The quality of being conscious and alert to one's surroundings and inner state",
                etymology="Old English 'gewær' - watchful, cautious",
                meditation_prompt="What am I becoming aware of in this moment?",
                journal_integration="Reflect on moments of heightened awareness today",
                council_wisdom={},
                difficulty_score=0.6,
                mindfulness_score=1.0,
                theme_category=ThemeCategory.MINDFULNESS_CORE
            ),
            WordData(
                word="PRESENCE",
                syllables=["PRES", "ENCE"],
                definition="The state of being fully here and now, without mental distraction",
                etymology="Latin 'praesentia' - being before",
                meditation_prompt="How can I cultivate deeper presence today?",
                journal_integration="Describe a moment when you felt completely present",
                council_wisdom={},
                difficulty_score=0.5,
                mindfulness_score=0.9,
                theme_category=ThemeCategory.MINDFULNESS_CORE
            ),
            WordData(
                word="MEDITATION",
                syllables=["MED", "I", "TA", "TION"],
                definition="The practice of focused attention to achieve mental clarity and emotional calm",
                etymology="Latin 'meditatus' - to think over, contemplate",
                meditation_prompt="What insights arise from my meditation practice?",
                journal_integration="Track the evolution of your meditation practice",
                council_wisdom={},
                difficulty_score=0.7,
                mindfulness_score=1.0,
                theme_category=ThemeCategory.MINDFULNESS_CORE
            )
        ]
        
        library[ThemeCategory.MINDFULNESS_CORE.value] = mindfulness_words
        
        # Add other theme categories...
        # (Implementation would continue with other themes)
        
        return library
    
    def _generate_puzzles_from_content(self, 
                                     content: Dict[str, Any], 
                                     puzzle_count: int,
                                     book_format: BookFormat) -> List[Dict[str, Any]]:
        """Generate puzzles from processed document content"""
        puzzles = []
        extracted_words = content.get('extracted_words', [])
        
        if not extracted_words:
            # Fallback to default words
            extracted_words = self._get_default_words(puzzle_count)
        
        # Generate word search puzzles
        for i in range(puzzle_count):
            # Select words for this puzzle
            puzzle_words = self._select_puzzle_words(extracted_words, 8)
            
            # Generate grid
            grid = self._generate_syllable_aware_grid(puzzle_words, book_format)
            
            # Create puzzle data
            puzzle = {
                'type': 'word_search',
                'title': f"Mindful Discovery {i + 1}",
                'words': puzzle_words,
                'grid': grid,
                'council_wisdom': content.get('council_insights', {}),
                'meditation_theme': self._generate_meditation_theme(puzzle_words),
                'difficulty': self._calculate_puzzle_difficulty(puzzle_words)
            }
            
            puzzles.append(puzzle)
        
        return puzzles
    
    def _generate_syllable_aware_grid(self, words: List[Dict], book_format: BookFormat) -> List[List[str]]:
        """Generate word search grid with syllable-aware placement"""
        specs = self.format_specs[book_format]
        grid_size = specs['grid_size']
        
        # Initialize empty grid
        grid = [[''] * grid_size for _ in range(grid_size)]
        
        # Place words with syllable direction changes
        for word_data in words:
            word = word_data['word']
            syllables = word_data.get('syllables', [word])
            
            placed = False
            attempts = 0
            
            while not placed and attempts < 50:
                start_row = random.randint(0, grid_size - 1)
                start_col = random.randint(0, grid_size - 1)
                
                if self._can_place_syllable_word(grid, word, syllables, start_row, start_col, grid_size):
                    self._place_syllable_word(grid, word, syllables, start_row, start_col)
                    placed = True
                
                attempts += 1
        
        # Fill empty cells with random letters
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == '':
                    grid[i][j] = chr(65 + random.randint(0, 25))
        
        return grid
    
    def _can_place_syllable_word(self, grid: List[List[str]], word: str, syllables: List[str], 
                                start_row: int, start_col: int, grid_size: int) -> bool:
        """Check if word can be placed with syllable direction changes"""
        current_row, current_col = start_row, start_col
        direction = random.choice(['horizontal', 'vertical', 'diagonal'])
        
        char_index = 0
        syllable_index = 0
        chars_in_syllable = 0
        
        for char in word:
            # Check bounds
            if current_row < 0 or current_row >= grid_size or current_col < 0 or current_col >= grid_size:
                return False
            
            # Check if cell is empty or matches
            if grid[current_row][current_col] != '' and grid[current_row][current_col] != char:
                return False
            
            # Move to next position
            chars_in_syllable += 1
            if syllable_index < len(syllables) and chars_in_syllable >= len(syllables[syllable_index]):
                # Change direction at syllable boundary
                direction = self._get_new_direction(direction)
                syllable_index += 1
                chars_in_syllable = 0
            
            # Calculate next position
            if char_index < len(word) - 1:
                delta_row, delta_col = self._get_direction_delta(direction)
                current_row += delta_row
                current_col += delta_col
            
            char_index += 1
        
        return True
    
    def _place_syllable_word(self, grid: List[List[str]], word: str, syllables: List[str], 
                           start_row: int, start_col: int):
        """Place word in grid with syllable direction changes"""
        current_row, current_col = start_row, start_col
        direction = random.choice(['horizontal', 'vertical', 'diagonal'])
        
        char_index = 0
        syllable_index = 0
        chars_in_syllable = 0
        
        for char in word:
            grid[current_row][current_col] = char
            
            # Move to next position
            chars_in_syllable += 1
            if syllable_index < len(syllables) and chars_in_syllable >= len(syllables[syllable_index]):
                # Change direction at syllable boundary
                direction = self._get_new_direction(direction)
                syllable_index += 1
                chars_in_syllable = 0
            
            # Calculate next position
            if char_index < len(word) - 1:
                delta_row, delta_col = self._get_direction_delta(direction)
                current_row += delta_row
                current_col += delta_col
            
            char_index += 1
    
    def _get_direction_delta(self, direction: str) -> Tuple[int, int]:
        """Get row and column deltas for direction"""
        deltas = {
            'horizontal': (0, 1),
            'vertical': (1, 0),
            'diagonal': (1, 1),
            'diagonal_up': (-1, 1)
        }
        return deltas.get(direction, (0, 1))
    
    def _get_new_direction(self, current_direction: str) -> str:
        """Get new direction different from current"""
        directions = ['horizontal', 'vertical', 'diagonal', 'diagonal_up']
        available = [d for d in directions if d != current_direction]
        return random.choice(available)
    
    def _create_book_pdf(self, 
                        title: str, 
                        puzzles: List[Dict], 
                        content: Dict[str, Any],
                        book_format: BookFormat,
                        include_answers: bool) -> Path:
        """Create complete KDP book PDF"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.replace(' ', '_')}_{timestamp}.pdf"
        output_path = self.output_dir / filename
        
        # Get format specifications
        specs = self.format_specs[book_format]
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=specs['page_size'],
            leftMargin=specs['margins'][0],
            rightMargin=specs['margins'][1],
            topMargin=specs['margins'][2],
            bottomMargin=specs['margins'][3]
        )
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=specs['title_font_size'],
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=specs['font_size'] + 2,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Title page
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("Mindful Word Discovery Through Syllable Flow", subtitle_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("Guided by the Council of Consciousness", styles['Normal']))
        story.append(PageBreak())
        
        # Introduction
        intro_text = self._generate_introduction(content)
        story.append(Paragraph("Introduction", styles['Heading1']))
        story.append(Paragraph(intro_text, styles['Normal']))
        story.append(PageBreak())
        
        # Puzzles
        for i, puzzle in enumerate(puzzles):
            story.extend(self._create_puzzle_page(puzzle, i + 1, styles, specs))
            story.append(PageBreak())
        
        # Answer key
        if include_answers:
            story.append(Paragraph("Answer Key", styles['Heading1']))
            story.append(Spacer(1, 20))
            
            for i, puzzle in enumerate(puzzles):
                story.extend(self._create_answer_page(puzzle, i + 1, styles))
                story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_puzzle_page(self, puzzle: Dict, puzzle_num: int, styles: Any, specs: Dict) -> List:
        """Create individual puzzle page content"""
        content = []
        
        # Puzzle title
        content.append(Paragraph(f"Puzzle {puzzle_num}: {puzzle['title']}", styles['Heading2']))
        content.append(Spacer(1, 10))
        
        # Meditation theme
        if 'meditation_theme' in puzzle:
            content.append(Paragraph(f"Meditation Theme: {puzzle['meditation_theme']}", styles['Italic']))
            content.append(Spacer(1, 10))
        
        # Grid
        grid_data = puzzle['grid']
        grid_table = Table(grid_data, colWidths=[0.3 * inch] * len(grid_data[0]))
        grid_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        content.append(grid_table)
        content.append(Spacer(1, 20))
        
        # Word list
        content.append(Paragraph("Words to Find:", styles['Heading3']))
        word_list = [word['word'] for word in puzzle['words']]
        word_text = " • ".join(word_list)
        content.append(Paragraph(word_text, styles['Normal']))
        content.append(Spacer(1, 15))
        
        # Council wisdom
        if puzzle.get('council_wisdom'):
            content.append(Paragraph("Council of Consciousness Wisdom:", styles['Heading3']))
            for persona, wisdom in puzzle['council_wisdom'].items():
                persona_name = persona.replace('_', ' ').title()
                content.append(Paragraph(f"<b>{persona_name}:</b> {wisdom}", styles['Normal']))
            content.append(Spacer(1, 10))
        
        # Reflection space
        content.append(Paragraph("Mindful Reflection:", styles['Heading3']))
        content.append(Paragraph("Use this space to reflect on your discoveries:", styles['Normal']))
        content.append(Spacer(1, 60))  # Space for writing
        
        return content
    
    def _create_answer_page(self, puzzle: Dict, puzzle_num: int, styles: Any) -> List:
        """Create answer page content"""
        content = []
        
        content.append(Paragraph(f"Answer Key - Puzzle {puzzle_num}", styles['Heading3']))
        
        # List words with their meditation prompts
        for word_data in puzzle['words']:
            word_text = f"<b>{word_data['word']}</b>"
            if 'meditation_prompt' in word_data:
                word_text += f" - {word_data['meditation_prompt']}"
            content.append(Paragraph(word_text, styles['Normal']))
        
        return content
    
    def _generate_introduction(self, content: Dict[str, Any]) -> str:
        """Generate book introduction"""
        intro = """
        Welcome to SyllaFlow - a revolutionary approach to mindful word discovery that combines 
        the wisdom of language with the practice of present-moment awareness.
        
        Each puzzle in this collection has been crafted with intention, drawing from the 
        Council of Consciousness to provide not just entertainment, but genuine opportunities 
        for reflection, growth, and inner discovery.
        
        As you search for words, notice how the syllable-aware placement creates natural 
        pauses - moments to breathe, reflect, and connect with the deeper meaning of each 
        discovery. This is more than a word search; it's a meditation in motion.
        
        May each puzzle serve your journey toward greater awareness, compassion, and wisdom.
        """
        
        # Add document-specific context if available
        if content.get('themes'):
            themes_text = ", ".join(content['themes'])
            intro += f"\n\nThis collection focuses on themes of {themes_text}, "
            intro += "offering pathways for exploration and contemplation."
        
        return intro
    
    def _generate_meditation_theme(self, words: List[Dict]) -> str:
        """Generate meditation theme for puzzle"""
        themes = [
            "Present moment awareness",
            "Compassionate understanding",
            "Inner wisdom cultivation",
            "Transformational growth",
            "Creative expression",
            "Peaceful contemplation",
            "Mindful discovery",
            "Conscious awakening"
        ]
        return random.choice(themes)
    
    def _calculate_puzzle_difficulty(self, words: List[Dict]) -> str:
        """Calculate puzzle difficulty level"""
        avg_difficulty = sum(word.get('difficulty_score', 0.5) for word in words) / len(words)
        
        if avg_difficulty < 0.3:
            return "Beginner"
        elif avg_difficulty < 0.6:
            return "Intermediate"
        elif avg_difficulty < 0.8:
            return "Advanced"
        else:
            return "Expert"
    
    def _select_puzzle_words(self, word_pool: List[Dict], count: int) -> List[Dict]:
        """Select words for a single puzzle"""
        if len(word_pool) <= count:
            return word_pool
        
        return random.sample(word_pool, count)
    
    def _get_default_words(self, count: int) -> List[Dict]:
        """Get default words when document processing fails"""
        default_words = [
            {
                'word': 'MINDFULNESS',
                'syllables': ['MIND', 'FUL', 'NESS'],
                'definition': 'The practice of purposeful, present-moment awareness',
                'meditation_prompt': 'How does mindfulness appear in your daily life?',
                'difficulty_score': 0.7,
                'mindfulness_score': 1.0
            },
            {
                'word': 'AWARENESS',
                'syllables': ['A', 'WARE', 'NESS'],
                'definition': 'Conscious knowledge of one\'s surroundings and inner state',
                'meditation_prompt': 'What am I becoming aware of right now?',
                'difficulty_score': 0.6,
                'mindfulness_score': 0.9
            },
            {
                'word': 'PRESENCE',
                'syllables': ['PRES', 'ENCE'],
                'definition': 'The state of being fully here and now',
                'meditation_prompt': 'How can I cultivate deeper presence?',
                'difficulty_score': 0.5,
                'mindfulness_score': 0.8
            }
        ]
        
        # Repeat and shuffle to reach desired count
        while len(default_words) < count:
            default_words.extend(default_words[:min(len(default_words), count - len(default_words))])
        
        return default_words[:count]
    
    def _get_theme_words(self, theme: ThemeCategory, difficulty: DifficultyLevel, count: int) -> List[WordData]:
        """Get words for specific theme and difficulty"""
        theme_words = self.word_library.get(theme.value, [])
        
        # Filter by difficulty if needed
        # (Implementation would filter based on difficulty_score)
        
        return theme_words[:count]
    
    def _generate_themed_puzzles(self, words: List[WordData], count: int, book_format: BookFormat) -> List[Dict]:
        """Generate puzzles from themed word list"""
        puzzles = []
        
        for i in range(count):
            # Select words for this puzzle
            puzzle_words = random.sample(words, min(8, len(words)))
            
            # Convert to dict format
            word_dicts = [asdict(word) for word in puzzle_words]
            
            # Generate grid
            grid = self._generate_syllable_aware_grid(word_dicts, book_format)
            
            puzzle = {
                'type': 'word_search',
                'title': f"Mindful Discovery {i + 1}",
                'words': word_dicts,
                'grid': grid,
                'council_wisdom': {},
                'meditation_theme': self._generate_meditation_theme(word_dicts),
                'difficulty': self._calculate_puzzle_difficulty(word_dicts)
            }
            
            puzzles.append(puzzle)
        
        return puzzles
    
    def _create_synthetic_content(self, theme: ThemeCategory, words: List[WordData]) -> Dict[str, Any]:
        """Create synthetic content for themed books"""
        return {
            'themes': [theme.value],
            'extracted_words': [asdict(word) for word in words],
            'complexity_score': 0.6,
            'mindfulness_score': 0.8,
            'council_insights': {},
            'metadata': {'content_type': 'synthetic_theme'}
        }

def main():
    """Main function for testing the enhanced KDP generation system"""
    generator = EnhancedKDPGenerator()
    
    # Test document processing
    print("=== Enhanced KDP Generation System Test ===")
    
    # Create sample document
    sample_doc_path = "/tmp/sample_mindfulness.txt"
    with open(sample_doc_path, 'w') as f:
        f.write("""
        Mindfulness is the practice of purposeful, present-moment awareness without judgment.
        Through meditation and conscious breathing, we cultivate inner peace and wisdom.
        Compassion flows naturally when we are truly present with ourselves and others.
        The journey of transformation begins with a single moment of awareness.
        """)
    
    try:
        # Generate book from document
        book_path = generator.generate_book_from_document(
            sample_doc_path,
            "Mindful Word Discovery: A Journey Through Consciousness",
            BookFormat.STANDARD_8_5_11,
            puzzle_count=10
        )
        
        print(f"✅ Document-based book generated: {book_path}")
        
        # Generate themed book
        themed_book_path = generator.generate_themed_book(
            ThemeCategory.MINDFULNESS_CORE,
            "SyllaFlow: Mindfulness Core Practice",
            BookFormat.STANDARD_8_5_11,
            DifficultyLevel.INTERMEDIATE,
            puzzle_count=15
        )
        
        print(f"✅ Themed book generated: {themed_book_path}")
        
        print("\n🎉 Enhanced KDP Generation System test completed successfully!")
        print(f"📁 Books saved to: {generator.output_dir}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if os.path.exists(sample_doc_path):
            os.remove(sample_doc_path)

if __name__ == "__main__":
    main()

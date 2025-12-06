#!/usr/bin/env python3
"""
SyllaFlow: Core Algorithm for Syllable-Based Word Search Generation
A sophisticated system for creating word search puzzles where direction changes at syllable boundaries.

This module provides:
- Advanced syllable detection using multiple linguistic approaches
- Intelligent grid generation with spatial optimization
- Etymology and word origin integration
- Mindfulness-focused word selection and theming
- Adaptive difficulty scaling
"""

import re
import random
import json
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import math

class Direction(Enum):
    """Eight possible directions for word placement in the grid"""
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DOWN = (1, 0)
    UP = (-1, 0)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (1, -1)
    UP_RIGHT = (-1, 1)
    UP_LEFT = (-1, -1)

class WordOrigin(Enum):
    """Etymology categories for word classification"""
    LATIN = "latin"
    GREEK = "greek"
    GERMANIC = "germanic"
    FRENCH = "french"
    SANSKRIT = "sanskrit"
    ARABIC = "arabic"
    NATIVE_AMERICAN = "native_american"
    MODERN = "modern"

class DifficultyLevel(Enum):
    """Difficulty levels for adaptive puzzle generation"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class SyllableSegment:
    """Represents a single syllable within a word"""
    text: str
    start_pos: int
    end_pos: int
    stress_level: int  # 0=unstressed, 1=secondary, 2=primary
    phonetic: str = ""

@dataclass
class WordData:
    """Complete information about a word for puzzle generation"""
    word: str
    syllables: List[SyllableSegment]
    definition: str
    etymology: Dict[str, str]
    origin: WordOrigin
    difficulty: DifficultyLevel
    mindfulness_prompt: str
    associations: List[str]
    rhyme_pattern: str
    
@dataclass
class GridPosition:
    """Position and direction information for grid placement"""
    row: int
    col: int
    direction: Direction

@dataclass
class PlacedWord:
    """Information about a word placed in the grid"""
    word_data: WordData
    segments: List[Tuple[GridPosition, str]]  # (position, syllable_text)
    start_position: GridPosition
    total_length: int

class SyllableDetector:
    """Advanced syllable detection using multiple linguistic approaches"""
    
    def __init__(self):
        # Common syllable patterns and rules
        self.vowel_groups = ['a', 'e', 'i', 'o', 'u', 'y']
        self.consonant_clusters = [
            'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 
            'sc', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'tr', 'tw', 'th', 
            'ch', 'sh', 'wh', 'ph', 'gh'
        ]
        
        # Common prefixes and suffixes that form syllable boundaries
        self.prefixes = [
            'un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'up', 'in',
            'im', 'il', 'ir', 'non', 'anti', 'de', 'ex', 'sub', 'super', 'inter'
        ]
        
        self.suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 
            'ful', 'less', 'able', 'ible', 'ous', 'ious', 'eous', 'ive', 'ative'
        ]
        
        # Mindfulness-themed word database with etymology
        self.mindfulness_words = {
            "meditation": {
                "syllables": ["med", "i", "ta", "tion"],
                "definition": "The practice of focused attention and awareness",
                "etymology": {"root": "Latin meditatus", "meaning": "to think over, consider"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "How does your meditation practice create space for awareness?",
                "associations": ["contemplation", "reflection", "stillness", "presence"],
                "rhyme_pattern": "ation"
            },
            "compassion": {
                "syllables": ["com", "pas", "sion"],
                "definition": "Sympathetic concern for the sufferings of others",
                "etymology": {"root": "Latin compassio", "meaning": "suffering with"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "Where can you extend compassion to yourself today?",
                "associations": ["empathy", "kindness", "understanding", "love"],
                "rhyme_pattern": "asion"
            },
            "awareness": {
                "syllables": ["a", "ware", "ness"],
                "definition": "Knowledge or perception of a situation or fact",
                "etymology": {"root": "Old English gewær", "meaning": "wary, cautious"},
                "origin": WordOrigin.GERMANIC,
                "mindfulness_prompt": "What are you becoming more aware of in this moment?",
                "associations": ["consciousness", "mindfulness", "attention", "presence"],
                "rhyme_pattern": "areness"
            },
            "gratitude": {
                "syllables": ["grat", "i", "tude"],
                "definition": "The quality of being thankful and appreciative",
                "etymology": {"root": "Latin gratitudo", "meaning": "thankfulness"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "What small blessing can you acknowledge with gratitude?",
                "associations": ["thankfulness", "appreciation", "blessing", "joy"],
                "rhyme_pattern": "itude"
            },
            "serenity": {
                "syllables": ["se", "ren", "i", "ty"],
                "definition": "The state of being calm, peaceful, and untroubled",
                "etymology": {"root": "Latin serenus", "meaning": "clear, unclouded"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "How can you cultivate serenity amidst life's challenges?",
                "associations": ["peace", "tranquility", "calm", "stillness"],
                "rhyme_pattern": "enity"
            },
            "wisdom": {
                "syllables": ["wis", "dom"],
                "definition": "The quality of having experience, knowledge, and good judgment",
                "etymology": {"root": "Old English wisdom", "meaning": "knowledge, learning"},
                "origin": WordOrigin.GERMANIC,
                "mindfulness_prompt": "What wisdom is emerging from your current experiences?",
                "associations": ["insight", "understanding", "knowledge", "discernment"],
                "rhyme_pattern": "isdom"
            },
            "presence": {
                "syllables": ["pres", "ence"],
                "definition": "The state of existing, occurring, or being present in a place or thing",
                "etymology": {"root": "Latin praesentia", "meaning": "being before"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "How fully can you inhabit this present moment?",
                "associations": ["awareness", "attention", "mindfulness", "being"],
                "rhyme_pattern": "esence"
            },
            "equanimity": {
                "syllables": ["e", "qua", "nim", "i", "ty"],
                "definition": "Mental calmness and composure, especially in difficult situations",
                "etymology": {"root": "Latin aequanimitas", "meaning": "evenness of mind"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "Where can you practice equanimity in your daily life?",
                "associations": ["balance", "composure", "steadiness", "calm"],
                "rhyme_pattern": "imity"
            },
            "mindfulness": {
                "syllables": ["mind", "ful", "ness"],
                "definition": "The practice of being aware and present in the current moment",
                "etymology": {"root": "Old English gemynd", "meaning": "memory, thought"},
                "origin": WordOrigin.GERMANIC,
                "mindfulness_prompt": "How does mindfulness transform your relationship with thoughts?",
                "associations": ["awareness", "attention", "presence", "consciousness"],
                "rhyme_pattern": "ulness"
            },
            "tranquility": {
                "syllables": ["tran", "quil", "i", "ty"],
                "definition": "The quality or state of being tranquil; calm",
                "etymology": {"root": "Latin tranquillitas", "meaning": "calmness, stillness"},
                "origin": WordOrigin.LATIN,
                "mindfulness_prompt": "What practices help you access inner tranquility?",
                "associations": ["peace", "serenity", "calm", "stillness"],
                "rhyme_pattern": "ility"
            }
        }
    
    def detect_syllables(self, word: str) -> List[SyllableSegment]:
        """
        Detect syllables in a word using multiple linguistic approaches
        """
        word = word.lower().strip()
        
        # Check if word is in our curated database
        if word in self.mindfulness_words:
            syllable_texts = self.mindfulness_words[word]["syllables"]
            segments = []
            pos = 0
            for i, syll_text in enumerate(syllable_texts):
                start_pos = pos
                end_pos = pos + len(syll_text)
                stress = 2 if i == 0 else 1  # Simple stress assignment
                segments.append(SyllableSegment(syll_text, start_pos, end_pos, stress))
                pos = end_pos
            return segments
        
        # Fallback to algorithmic detection
        return self._algorithmic_syllable_detection(word)
    
    def _algorithmic_syllable_detection(self, word: str) -> List[SyllableSegment]:
        """
        Algorithmic syllable detection for words not in database
        """
        # Simple vowel-based syllable detection with consonant cluster handling
        syllables = []
        current_syllable = ""
        vowel_count = 0
        
        i = 0
        while i < len(word):
            char = word[i]
            current_syllable += char
            
            if char.lower() in self.vowel_groups:
                vowel_count += 1
                
                # Look ahead for syllable boundary
                if i + 1 < len(word):
                    next_char = word[i + 1]
                    if next_char.lower() not in self.vowel_groups and vowel_count > 0:
                        # Check for consonant clusters
                        consonant_cluster = ""
                        j = i + 1
                        while j < len(word) and word[j].lower() not in self.vowel_groups:
                            consonant_cluster += word[j]
                            j += 1
                        
                        # Split consonant cluster appropriately
                        if len(consonant_cluster) > 1:
                            split_point = len(consonant_cluster) // 2
                            current_syllable += consonant_cluster[:split_point]
                            
                            # Create syllable segment
                            start_pos = len(''.join([s.text for s in syllables]))
                            segments = SyllableSegment(
                                current_syllable, 
                                start_pos, 
                                start_pos + len(current_syllable),
                                1
                            )
                            syllables.append(segments)
                            
                            current_syllable = consonant_cluster[split_point:]
                            vowel_count = 0
                            i = j - len(consonant_cluster) + split_point - 1
            
            i += 1
        
        # Add final syllable
        if current_syllable:
            start_pos = len(''.join([s.text for s in syllables]))
            syllables.append(SyllableSegment(
                current_syllable, 
                start_pos, 
                start_pos + len(current_syllable),
                2 if len(syllables) == 0 else 1
            ))
        
        return syllables if syllables else [SyllableSegment(word, 0, len(word), 2)]

class GridGenerator:
    """Generates optimized grids for syllable-based word search puzzles"""
    
    def __init__(self, width: int = 15, height: int = 15):
        self.width = width
        self.height = height
        self.grid = [['' for _ in range(width)] for _ in range(height)]
        self.placed_words: List[PlacedWord] = []
        self.syllable_detector = SyllableDetector()
    
    def generate_puzzle(self, word_list: List[str], difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE) -> Dict:
        """
        Generate a complete syllable-based word search puzzle
        """
        # Convert words to WordData objects
        word_data_list = []
        for word in word_list:
            word_data = self._create_word_data(word, difficulty)
            if word_data:
                word_data_list.append(word_data)
        
        # Sort words by complexity for optimal placement
        word_data_list.sort(key=lambda w: len(w.word), reverse=True)
        
        # Reset grid
        self.grid = [['' for _ in range(self.width)] for _ in range(self.height)]
        self.placed_words = []
        
        # Place words in grid
        for word_data in word_data_list:
            if self._place_word_in_grid(word_data):
                continue
        
        # Fill empty spaces with random letters
        self._fill_empty_spaces()
        
        # Generate puzzle metadata
        puzzle_data = {
            "grid": self.grid,
            "words": [asdict(pw.word_data) for pw in self.placed_words],
            "placed_words": [self._serialize_placed_word(pw) for pw in self.placed_words],
            "difficulty": difficulty.value,
            "dimensions": {"width": self.width, "height": self.height},
            "theme": "mindfulness_awareness",
            "mindfulness_integration": self._generate_mindfulness_integration()
        }
        
        return puzzle_data
    
    def _create_word_data(self, word: str, difficulty: DifficultyLevel) -> Optional[WordData]:
        """
        Create WordData object from word string
        """
        word = word.lower().strip()
        syllables = self.syllable_detector.detect_syllables(word)
        
        # Get word information from database or create default
        if word in self.syllable_detector.mindfulness_words:
            word_info = self.syllable_detector.mindfulness_words[word]
            return WordData(
                word=word,
                syllables=syllables,
                definition=word_info["definition"],
                etymology=word_info["etymology"],
                origin=word_info["origin"],
                difficulty=difficulty,
                mindfulness_prompt=word_info["mindfulness_prompt"],
                associations=word_info["associations"],
                rhyme_pattern=word_info["rhyme_pattern"]
            )
        else:
            # Create basic word data for unknown words
            return WordData(
                word=word,
                syllables=syllables,
                definition=f"Explore the meaning of '{word}' in your mindfulness practice",
                etymology={"root": "Unknown", "meaning": "To be discovered"},
                origin=WordOrigin.MODERN,
                difficulty=difficulty,
                mindfulness_prompt=f"How does the word '{word}' resonate with your current experience?",
                associations=[],
                rhyme_pattern=""
            )
    
    def _place_word_in_grid(self, word_data: WordData) -> bool:
        """
        Attempt to place a word in the grid with syllable-based direction changes
        """
        max_attempts = 100
        
        for attempt in range(max_attempts):
            # Choose random starting position
            start_row = random.randint(0, self.height - 1)
            start_col = random.randint(0, self.width - 1)
            
            # Generate path for syllables
            path = self._generate_syllable_path(word_data, start_row, start_col)
            
            if path and self._can_place_word_at_path(word_data.word, path):
                # Place the word
                placed_word = self._place_word_at_path(word_data, path)
                self.placed_words.append(placed_word)
                return True
        
        return False
    
    def _generate_syllable_path(self, word_data: WordData, start_row: int, start_col: int) -> Optional[List[Tuple[int, int, Direction]]]:
        """
        Generate a path through the grid that changes direction at syllable boundaries
        """
        path = []
        current_row, current_col = start_row, start_col
        
        for i, syllable in enumerate(word_data.syllables):
            # Choose direction for this syllable (different from previous if possible)
            available_directions = list(Direction)
            if i > 0:
                # Try to avoid same direction as previous syllable
                prev_direction = path[-1][2] if path else None
                if prev_direction in available_directions:
                    available_directions.remove(prev_direction)
            
            direction = random.choice(available_directions)
            
            # Calculate positions for this syllable
            syllable_positions = []
            temp_row, temp_col = current_row, current_col
            
            for char in syllable.text:
                if not self._is_valid_position(temp_row, temp_col):
                    return None
                
                syllable_positions.append((temp_row, temp_col, direction))
                
                # Move to next position
                dr, dc = direction.value
                temp_row += dr
                temp_col += dc
            
            path.extend(syllable_positions)
            current_row, current_col = temp_row, temp_col
        
        return path
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= row < self.height and 0 <= col < self.width
    
    def _can_place_word_at_path(self, word: str, path: List[Tuple[int, int, Direction]]) -> bool:
        """Check if word can be placed at the given path"""
        if len(path) != len(word):
            return False
        
        for i, (row, col, direction) in enumerate(path):
            if not self._is_valid_position(row, col):
                return False
            
            # Check if position is empty or contains the same letter
            if self.grid[row][col] != '' and self.grid[row][col] != word[i]:
                return False
        
        return True
    
    def _place_word_at_path(self, word_data: WordData, path: List[Tuple[int, int, Direction]]) -> PlacedWord:
        """Place word at the specified path and return PlacedWord object"""
        segments = []
        current_syllable_idx = 0
        chars_in_current_syllable = 0
        
        for i, (row, col, direction) in enumerate(path):
            char = word_data.word[i]
            self.grid[row][col] = char
            
            # Determine which syllable this character belongs to
            if current_syllable_idx < len(word_data.syllables):
                current_syllable = word_data.syllables[current_syllable_idx]
                if chars_in_current_syllable >= len(current_syllable.text):
                    current_syllable_idx += 1
                    chars_in_current_syllable = 0
                    if current_syllable_idx < len(word_data.syllables):
                        current_syllable = word_data.syllables[current_syllable_idx]
                
                syllable_text = current_syllable.text if current_syllable_idx < len(word_data.syllables) else ""
                chars_in_current_syllable += 1
            else:
                syllable_text = ""
            
            segments.append((GridPosition(row, col, direction), syllable_text))
        
        start_position = GridPosition(path[0][0], path[0][1], path[0][2])
        
        return PlacedWord(
            word_data=word_data,
            segments=segments,
            start_position=start_position,
            total_length=len(word_data.word)
        )
    
    def _fill_empty_spaces(self):
        """Fill empty grid spaces with random letters"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == '':
                    self.grid[row][col] = random.choice(letters)
    
    def _serialize_placed_word(self, placed_word: PlacedWord) -> Dict:
        """Serialize PlacedWord for JSON output"""
        return {
            "word": placed_word.word_data.word,
            "syllables": [s.text for s in placed_word.word_data.syllables],
            "start_position": {
                "row": placed_word.start_position.row,
                "col": placed_word.start_position.col,
                "direction": placed_word.start_position.direction.name
            },
            "segments": [
                {
                    "position": {"row": pos.row, "col": pos.col, "direction": pos.direction.name},
                    "syllable": syllable
                }
                for pos, syllable in placed_word.segments
            ],
            "total_length": placed_word.total_length
        }
    
    def _generate_mindfulness_integration(self) -> Dict:
        """Generate mindfulness integration activities for the puzzle"""
        return {
            "pre_puzzle_centering": {
                "instruction": "Take three conscious breaths and set an intention for mindful discovery",
                "duration": "1-2 minutes"
            },
            "during_puzzle_awareness": {
                "instruction": "Notice when you feel frustrated or excited. Return to breath awareness.",
                "reminders": ["Breathe with each word discovery", "Celebrate small victories mindfully"]
            },
            "post_puzzle_reflection": {
                "prompts": [
                    "Which word resonated most deeply with you today?",
                    "What did you notice about your mind during the search?",
                    "How can you carry this focused attention into your day?"
                ],
                "journaling_time": "5-10 minutes"
            },
            "etymology_exploration": {
                "instruction": "Choose one word and explore its origins and personal meaning",
                "activity": "Write about how the word's history connects to your life"
            }
        }

def main():
    """Demonstration of the SyllaFlow algorithm"""
    print("🌟 SyllaFlow: Syllable-Based Word Search Generator 🌟\n")
    
    # Create generator
    generator = GridGenerator(12, 12)
    
    # Sample mindfulness word list
    sample_words = [
        "meditation", "compassion", "awareness", "gratitude", 
        "serenity", "wisdom", "presence", "mindfulness"
    ]
    
    print("Generating puzzle with words:", ", ".join(sample_words))
    print("This may take a moment as we optimize syllable placement...\n")
    
    # Generate puzzle
    puzzle = generator.generate_puzzle(sample_words, DifficultyLevel.INTERMEDIATE)
    
    # Display results
    print("📊 Generated Puzzle Grid:")
    print("=" * 40)
    for row in puzzle["grid"]:
        print(" ".join(row).upper())
    
    print(f"\n✅ Successfully placed {len(puzzle['words'])} words")
    print("\n📝 Word List with Syllable Information:")
    print("=" * 50)
    
    for word_info in puzzle["words"]:
        syllables = " • ".join([s["text"] for s in word_info["syllables"]])
        print(f"🔤 {word_info['word'].upper()}")
        print(f"   Syllables: {syllables}")
        print(f"   Definition: {word_info['definition']}")
        print(f"   Origin: {word_info['origin']}")
        print(f"   Mindfulness Prompt: {word_info['mindfulness_prompt']}")
        print()
    
    print("🧘 Mindfulness Integration Activities:")
    print("=" * 40)
    integration = puzzle["mindfulness_integration"]
    print(f"Pre-puzzle: {integration['pre_puzzle_centering']['instruction']}")
    print(f"During: {integration['during_puzzle_awareness']['instruction']}")
    print(f"Post-puzzle reflection prompts:")
    for prompt in integration["post_puzzle_reflection"]["prompts"]:
        print(f"  • {prompt}")
    
    # Save puzzle data
    with open('/home/ubuntu/sample_syllaflow_puzzle.json', 'w') as f:
        json.dump(puzzle, f, indent=2, default=str)
    
    print(f"\n💾 Puzzle data saved to: sample_syllaflow_puzzle.json")
    print("🎯 Ready for webapp integration!")

if __name__ == "__main__":
    main()

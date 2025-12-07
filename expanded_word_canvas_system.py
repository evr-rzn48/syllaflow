#!/usr/bin/env python3
"""
SyllaFlow Expanded Word Canvas System
Enhanced algorithm with larger grids and comprehensive word library integration

Developed by the Council of Consciousness
Featuring Angela Davis (accessibility), Octavia Butler (adaptive systems), 
Rick Rubin (authentic minimalism), and the complete 10-persona collective
"""

import json
import random
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import math

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    MASTER = "master"

class GridSize(Enum):
    SMALL = (12, 12)      # Original size
    MEDIUM = (16, 16)     # Enhanced size
    LARGE = (20, 20)      # Expanded size
    EXTRA_LARGE = (24, 24) # Maximum size

class Direction(Enum):
    HORIZONTAL = (0, 1)
    VERTICAL = (1, 0)
    DIAGONAL_DOWN = (1, 1)
    DIAGONAL_UP = (-1, 1)
    REVERSE_HORIZONTAL = (0, -1)
    REVERSE_VERTICAL = (-1, 0)
    REVERSE_DIAGONAL_DOWN = (-1, -1)
    REVERSE_DIAGONAL_UP = (1, -1)

@dataclass
class WordData:
    """Enhanced word data structure with comprehensive metadata"""
    word: str
    definition: str
    etymology: str
    pronunciation: str
    syllables: List[str]
    difficulty: DifficultyLevel
    category: str
    mindfulness_prompt: str
    journal_integration: str
    meditation_template: str
    word_associations: List[str]
    rhyme_patterns: List[str]
    emotional_resonance: str
    cultural_context: str
    usage_examples: List[str]

@dataclass
class SyllableSegment:
    """Represents a syllable segment with directional change"""
    syllable: str
    start_pos: Tuple[int, int]
    direction: Direction
    letters: List[Tuple[int, int, str]]  # (row, col, letter)

@dataclass
class PlacedWord:
    """Represents a word placed in the grid with syllable awareness"""
    word_data: WordData
    segments: List[SyllableSegment]
    total_positions: List[Tuple[int, int]]
    discovery_order: Optional[int] = None

class ExpandedWordCanvas:
    """Enhanced word canvas with larger grids and sophisticated algorithms"""
    
    def __init__(self, grid_size: GridSize = GridSize.MEDIUM, difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE):
        self.rows, self.cols = grid_size.value
        self.difficulty = difficulty
        self.grid = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.placed_words: List[PlacedWord] = []
        self.word_library = self._initialize_comprehensive_library()
        self.syllable_patterns = self._initialize_syllable_patterns()
        
    def _initialize_comprehensive_library(self) -> Dict[str, List[WordData]]:
        """Initialize comprehensive word library with enhanced metadata"""
        return {
            "mindfulness_core": [
                WordData(
                    word="MEDITATION",
                    definition="A practice of focused attention to achieve mental clarity and emotional calm",
                    etymology="From Latin 'meditatio' meaning 'thinking over, contemplation'",
                    pronunciation="/ˌmedɪˈteɪʃən/",
                    syllables=["MED", "I", "TA", "TION"],
                    difficulty=DifficultyLevel.BEGINNER,
                    category="mindfulness_core",
                    mindfulness_prompt="How does stillness speak to you in this moment?",
                    journal_integration="Reflect on your relationship with silence and inner peace",
                    meditation_template="Breathe into the space between thoughts, finding the meditation that lives within you",
                    word_associations=["stillness", "awareness", "presence", "breath", "peace"],
                    rhyme_patterns=["station", "creation", "foundation", "inspiration"],
                    emotional_resonance="Calming, centering, grounding",
                    cultural_context="Universal practice found across cultures and traditions",
                    usage_examples=["Daily meditation practice", "Walking meditation", "Loving-kindness meditation"]
                ),
                WordData(
                    word="AWARENESS",
                    definition="The quality of being conscious and mindful of one's surroundings and inner state",
                    etymology="From Old English 'gewær' meaning 'wary, cautious, aware'",
                    pronunciation="/əˈwɛrnəs/",
                    syllables=["A", "WARE", "NESS"],
                    difficulty=DifficultyLevel.BEGINNER,
                    category="mindfulness_core",
                    mindfulness_prompt="What are you becoming aware of right now?",
                    journal_integration="Notice what you notice - track your expanding awareness",
                    meditation_template="Rest in the spacious awareness that notices all experiences",
                    word_associations=["consciousness", "attention", "mindfulness", "presence", "observation"],
                    rhyme_patterns=["fairness", "rareness", "bareness"],
                    emotional_resonance="Expansive, illuminating, clarifying",
                    cultural_context="Central concept in mindfulness and contemplative traditions",
                    usage_examples=["Self-awareness practice", "Environmental awareness", "Emotional awareness"]
                ),
                WordData(
                    word="COMPASSION",
                    definition="Sympathetic concern for the sufferings of others, coupled with action to help",
                    etymology="From Latin 'compassio' meaning 'suffering with'",
                    pronunciation="/kəmˈpæʃən/",
                    syllables=["COM", "PAS", "SION"],
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    category="mindfulness_core",
                    mindfulness_prompt="How can you extend compassion to yourself and others today?",
                    journal_integration="Explore moments when compassion arose naturally in your experience",
                    meditation_template="Breathe in suffering, breathe out relief and loving-kindness",
                    word_associations=["kindness", "empathy", "love", "understanding", "mercy"],
                    rhyme_patterns=["passion", "fashion", "ration"],
                    emotional_resonance="Warm, healing, connecting",
                    cultural_context="Universal virtue emphasized across spiritual and ethical traditions",
                    usage_examples=["Self-compassion practice", "Compassionate communication", "Compassionate action"]
                )
            ],
            "emotional_intelligence": [
                WordData(
                    word="RESILIENCE",
                    definition="The ability to recover quickly from difficulties and adapt to challenging circumstances",
                    etymology="From Latin 'resilire' meaning 'to rebound, recoil'",
                    pronunciation="/rɪˈzɪljəns/",
                    syllables=["RE", "SIL", "IENCE"],
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    category="emotional_intelligence",
                    mindfulness_prompt="What inner strength can you draw upon in this moment?",
                    journal_integration="Reflect on times when you bounced back from adversity",
                    meditation_template="Feel your inner strength like a flexible tree that bends but doesn't break",
                    word_associations=["strength", "flexibility", "recovery", "adaptation", "endurance"],
                    rhyme_patterns=["brilliance", "resilience"],
                    emotional_resonance="Empowering, stabilizing, hopeful",
                    cultural_context="Valued across cultures as essential life skill",
                    usage_examples=["Building emotional resilience", "Community resilience", "Psychological resilience"]
                ),
                WordData(
                    word="VULNERABILITY",
                    definition="The quality of being open to emotional or physical harm; authentic openness",
                    etymology="From Latin 'vulnerabilis' meaning 'wounding'",
                    pronunciation="/ˌvʌlnərəˈbɪlɪti/",
                    syllables=["VUL", "NER", "A", "BIL", "I", "TY"],
                    difficulty=DifficultyLevel.ADVANCED,
                    category="emotional_intelligence",
                    mindfulness_prompt="Where can you practice courageous authenticity today?",
                    journal_integration="Explore the relationship between vulnerability and connection",
                    meditation_template="Breathe into your tender heart, honoring both strength and softness",
                    word_associations=["authenticity", "courage", "openness", "tenderness", "truth"],
                    rhyme_patterns=["capability", "reliability", "availability"],
                    emotional_resonance="Tender, brave, connecting",
                    cultural_context="Increasingly recognized as strength rather than weakness",
                    usage_examples=["Emotional vulnerability", "Vulnerable leadership", "Vulnerable communication"]
                )
            ],
            "creative_expression": [
                WordData(
                    word="IMAGINATION",
                    definition="The faculty of forming new ideas, images, or concepts not present to the senses",
                    etymology="From Latin 'imaginatio' meaning 'a picturing to oneself'",
                    pronunciation="/ɪˌmædʒɪˈneɪʃən/",
                    syllables=["I", "MAG", "I", "NA", "TION"],
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    category="creative_expression",
                    mindfulness_prompt="What new possibilities are emerging in your awareness?",
                    journal_integration="Capture the images and ideas that arise spontaneously",
                    meditation_template="Rest in the creative space where all possibilities exist",
                    word_associations=["creativity", "vision", "innovation", "dreams", "possibility"],
                    rhyme_patterns=["creation", "inspiration", "manifestation"],
                    emotional_resonance="Expansive, playful, inspiring",
                    cultural_context="Celebrated as essential human capacity across cultures",
                    usage_examples=["Creative imagination", "Moral imagination", "Scientific imagination"]
                ),
                WordData(
                    word="AUTHENTICITY",
                    definition="The quality of being genuine, real, and true to one's own personality and values",
                    etymology="From Greek 'authentikos' meaning 'original, genuine'",
                    pronunciation="/ˌɔθənˈtɪsɪti/",
                    syllables=["AU", "THEN", "TIC", "I", "TY"],
                    difficulty=DifficultyLevel.ADVANCED,
                    category="creative_expression",
                    mindfulness_prompt="How can you express your truest self today?",
                    journal_integration="Explore moments when you felt most authentically yourself",
                    meditation_template="Breathe into your essential nature, beyond all masks and roles",
                    word_associations=["genuineness", "truth", "integrity", "realness", "honesty"],
                    rhyme_patterns=["elasticity", "plasticity", "domesticity"],
                    emotional_resonance="Liberating, grounding, empowering",
                    cultural_context="Increasingly valued in personal development and leadership",
                    usage_examples=["Authentic leadership", "Authentic expression", "Authentic relationships"]
                )
            ],
            "wisdom_traditions": [
                WordData(
                    word="EQUANIMITY",
                    definition="Mental calmness and composure, especially in difficult situations",
                    etymology="From Latin 'aequanimitas' meaning 'evenness of mind'",
                    pronunciation="/ˌiːkwəˈnɪmɪti/",
                    syllables=["E", "QUAN", "IM", "I", "TY"],
                    difficulty=DifficultyLevel.ADVANCED,
                    category="wisdom_traditions",
                    mindfulness_prompt="How can you find balance amidst life's changing conditions?",
                    journal_integration="Notice moments of natural balance and inner stability",
                    meditation_template="Rest in the unchanging awareness that remains steady through all experiences",
                    word_associations=["balance", "serenity", "stability", "peace", "composure"],
                    rhyme_patterns=["serenity", "clarity", "rarity"],
                    emotional_resonance="Stabilizing, peaceful, wise",
                    cultural_context="Central virtue in Buddhist and Stoic traditions",
                    usage_examples=["Emotional equanimity", "Spiritual equanimity", "Mental equanimity"]
                )
            ]
        }
    
    def _initialize_syllable_patterns(self) -> Dict[str, List[str]]:
        """Initialize syllable patterns for enhanced word placement"""
        return {
            "common_prefixes": ["UN", "RE", "IN", "DIS", "EN", "NON", "PRE", "ANTI"],
            "common_suffixes": ["ING", "TION", "NESS", "MENT", "ABLE", "IBLE", "IOUS", "EOUS"],
            "vowel_patterns": ["A", "E", "I", "O", "U", "Y"],
            "consonant_clusters": ["TH", "CH", "SH", "PH", "GH", "CK", "NG", "ST", "TR", "BR"]
        }
    
    def get_words_by_difficulty(self, difficulty: DifficultyLevel, count: int = 8) -> List[WordData]:
        """Get words filtered by difficulty level"""
        all_words = []
        for category_words in self.word_library.values():
            all_words.extend([w for w in category_words if w.difficulty == difficulty])
        
        # Ensure we have enough words
        if len(all_words) < count:
            # Add words from adjacent difficulty levels
            adjacent_difficulties = {
                DifficultyLevel.BEGINNER: [DifficultyLevel.INTERMEDIATE],
                DifficultyLevel.INTERMEDIATE: [DifficultyLevel.BEGINNER, DifficultyLevel.ADVANCED],
                DifficultyLevel.ADVANCED: [DifficultyLevel.INTERMEDIATE, DifficultyLevel.MASTER],
                DifficultyLevel.MASTER: [DifficultyLevel.ADVANCED]
            }
            
            for adj_diff in adjacent_difficulties.get(difficulty, []):
                for category_words in self.word_library.values():
                    all_words.extend([w for w in category_words if w.difficulty == adj_diff])
        
        return random.sample(all_words, min(count, len(all_words)))
    
    def syllable_aware_placement(self, word_data: WordData) -> Optional[PlacedWord]:
        """Place word with syllable-aware directional changes"""
        max_attempts = 100
        
        for _ in range(max_attempts):
            # Choose random starting position
            start_row = random.randint(0, self.rows - 1)
            start_col = random.randint(0, self.cols - 1)
            
            # Try to place word with syllable segments
            placed_word = self._attempt_syllable_placement(word_data, start_row, start_col)
            if placed_word:
                return placed_word
        
        return None
    
    def _attempt_syllable_placement(self, word_data: WordData, start_row: int, start_col: int) -> Optional[PlacedWord]:
        """Attempt to place word with syllable-based direction changes"""
        segments = []
        current_row, current_col = start_row, start_col
        all_positions = []
        
        for i, syllable in enumerate(word_data.syllables):
            # Choose direction for this syllable (change direction at syllable boundaries)
            if i == 0:
                # First syllable can go in any direction
                direction = random.choice(list(Direction))
            else:
                # Subsequent syllables change direction
                available_directions = self._get_available_directions(current_row, current_col, len(syllable))
                if not available_directions:
                    return None
                direction = random.choice(available_directions)
            
            # Calculate positions for this syllable
            syllable_positions = []
            temp_row, temp_col = current_row, current_col
            
            for letter in syllable:
                # Check if position is valid and available
                if not self._is_valid_position(temp_row, temp_col):
                    return None
                
                if self.grid[temp_row][temp_col] != '' and self.grid[temp_row][temp_col] != letter:
                    return None
                
                syllable_positions.append((temp_row, temp_col, letter))
                all_positions.append((temp_row, temp_col))
                
                # Move to next position
                dr, dc = direction.value
                temp_row += dr
                temp_col += dc
            
            # Create syllable segment
            segment = SyllableSegment(
                syllable=syllable,
                start_pos=(current_row, current_col),
                direction=direction,
                letters=syllable_positions
            )
            segments.append(segment)
            
            # Update current position for next syllable (last letter of current syllable)
            if syllable_positions:
                current_row, current_col = syllable_positions[-1][0], syllable_positions[-1][1]
                # Move one more step for next syllable start
                dr, dc = direction.value
                current_row += dr
                current_col += dc
        
        return PlacedWord(
            word_data=word_data,
            segments=segments,
            total_positions=all_positions
        )
    
    def _get_available_directions(self, row: int, col: int, length: int) -> List[Direction]:
        """Get directions that can accommodate the given length from position"""
        available = []
        
        for direction in Direction:
            dr, dc = direction.value
            valid = True
            
            # Check if we can place 'length' letters in this direction
            for i in range(length):
                new_row = row + (dr * i)
                new_col = col + (dc * i)
                
                if not self._is_valid_position(new_row, new_col):
                    valid = False
                    break
            
            if valid:
                available.append(direction)
        
        return available
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def place_word_in_grid(self, placed_word: PlacedWord) -> bool:
        """Actually place the word in the grid"""
        # First, verify all positions are still available
        for row, col in placed_word.total_positions:
            letter_at_pos = None
            for segment in placed_word.segments:
                for pos_row, pos_col, letter in segment.letters:
                    if pos_row == row and pos_col == col:
                        letter_at_pos = letter
                        break
            
            if self.grid[row][col] != '' and self.grid[row][col] != letter_at_pos:
                return False
        
        # Place the letters
        for segment in placed_word.segments:
            for row, col, letter in segment.letters:
                self.grid[row][col] = letter
        
        self.placed_words.append(placed_word)
        return True
    
    def fill_empty_cells(self):
        """Fill empty cells with random letters, considering syllable patterns"""
        vowels = ['A', 'E', 'I', 'O', 'U']
        consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == '':
                    # Use weighted selection to create more natural letter distribution
                    if random.random() < 0.4:  # 40% chance for vowel
                        self.grid[row][col] = random.choice(vowels)
                    else:
                        self.grid[row][col] = random.choice(consonants)
    
    def generate_expanded_canvas(self, word_count: int = 8) -> Dict:
        """Generate expanded word canvas with comprehensive metadata"""
        # Get words for current difficulty
        selected_words = self.get_words_by_difficulty(self.difficulty, word_count)
        
        # Place words with syllable awareness
        successfully_placed = []
        for word_data in selected_words:
            placed_word = self.syllable_aware_placement(word_data)
            if placed_word and self.place_word_in_grid(placed_word):
                successfully_placed.append(placed_word)
        
        # Fill empty cells
        self.fill_empty_cells()
        
        # Generate comprehensive output
        return {
            "grid_data": {
                "size": {"rows": self.rows, "cols": self.cols},
                "difficulty": self.difficulty.value,
                "grid": self.grid,
                "cell_count": self.rows * self.cols
            },
            "words": [
                {
                    "word": pw.word_data.word,
                    "definition": pw.word_data.definition,
                    "etymology": pw.word_data.etymology,
                    "pronunciation": pw.word_data.pronunciation,
                    "syllables": pw.word_data.syllables,
                    "category": pw.word_data.category,
                    "difficulty": pw.word_data.difficulty.value,
                    "mindfulness_prompt": pw.word_data.mindfulness_prompt,
                    "journal_integration": pw.word_data.journal_integration,
                    "meditation_template": pw.word_data.meditation_template,
                    "word_associations": pw.word_data.word_associations,
                    "rhyme_patterns": pw.word_data.rhyme_patterns,
                    "emotional_resonance": pw.word_data.emotional_resonance,
                    "cultural_context": pw.word_data.cultural_context,
                    "usage_examples": pw.word_data.usage_examples,
                    "segments": [
                        {
                            "syllable": seg.syllable,
                            "start_position": seg.start_pos,
                            "direction": seg.direction.name,
                            "positions": [(r, c) for r, c, _ in seg.letters]
                        }
                        for seg in pw.segments
                    ],
                    "total_positions": pw.total_positions
                }
                for pw in successfully_placed
            ],
            "metadata": {
                "words_placed": len(successfully_placed),
                "words_requested": word_count,
                "placement_success_rate": len(successfully_placed) / word_count if word_count > 0 else 0,
                "grid_utilization": sum(1 for row in self.grid for cell in row if cell != '') / (self.rows * self.cols),
                "syllable_segments_total": sum(len(pw.segments) for pw in successfully_placed),
                "average_word_length": sum(len(pw.word_data.word) for pw in successfully_placed) / len(successfully_placed) if successfully_placed else 0,
                "categories_represented": list(set(pw.word_data.category for pw in successfully_placed)),
                "difficulty_distribution": {
                    diff.value: sum(1 for pw in successfully_placed if pw.word_data.difficulty == diff)
                    for diff in DifficultyLevel
                }
            },
            "canvas_config": {
                "syllable_direction_changes": True,
                "mindfulness_integration": True,
                "journal_prompts_included": True,
                "meditation_templates_included": True,
                "word_associations_included": True,
                "cultural_context_included": True,
                "accessibility_optimized": True,  # Angela Davis influence
                "adaptive_difficulty": True,      # Octavia Butler influence
                "authentic_minimalism": True     # Rick Rubin influence
            }
        }

def create_sample_canvases():
    """Create sample canvases for different configurations"""
    configurations = [
        (GridSize.MEDIUM, DifficultyLevel.BEGINNER, 6),
        (GridSize.LARGE, DifficultyLevel.INTERMEDIATE, 8),
        (GridSize.EXTRA_LARGE, DifficultyLevel.ADVANCED, 10)
    ]
    
    results = {}
    
    for grid_size, difficulty, word_count in configurations:
        print(f"\\nGenerating {grid_size.name} canvas with {difficulty.value} difficulty...")
        
        canvas = ExpandedWordCanvas(grid_size, difficulty)
        result = canvas.generate_expanded_canvas(word_count)
        
        config_name = f"{grid_size.name.lower()}_{difficulty.value}"
        results[config_name] = result
        
        # Print summary
        metadata = result["metadata"]
        print(f"✓ Placed {metadata['words_placed']}/{metadata['words_requested']} words")
        print(f"✓ Grid utilization: {metadata['grid_utilization']:.1%}")
        print(f"✓ Categories: {', '.join(metadata['categories_represented'])}")
        print(f"✓ Syllable segments: {metadata['syllable_segments_total']}")
    
    return results

if __name__ == "__main__":
    print("🌸 SyllaFlow Expanded Word Canvas System")
    print("=" * 50)
    print("Developed by the Council of Consciousness")
    print("Featuring enhanced algorithms with syllable-aware placement")
    print()
    
    # Create sample canvases
    sample_results = create_sample_canvases()
    
    # Save results
    with open('/home/ubuntu/expanded_canvas_samples.json', 'w') as f:
        json.dump(sample_results, f, indent=2)
    
    print(f"\\n✨ Sample canvases saved to: /home/ubuntu/expanded_canvas_samples.json")
    print("\\n🎯 Key Features Implemented:")
    print("• Larger grid sizes (up to 24x24)")
    print("• Syllable-aware directional changes")
    print("• Comprehensive word metadata")
    print("• Mindfulness integration prompts")
    print("• Journal integration templates")
    print("• Cultural context and accessibility")
    print("• Adaptive difficulty systems")
    print("• Enhanced placement algorithms")
    
    print("\\n🌟 Ready for integration with AlignFlow platform!")

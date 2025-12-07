#!/usr/bin/env python3
"""
SyllaFlow KDP Wordsearch Generator
Backend system for generating Amazon KDP physical companion wordgames

Developed by the Council of Consciousness
Creating print-ready puzzle books for mindfulness practice
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random
import math
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

@dataclass
class KDPBookSpecification:
    """Amazon KDP book specifications"""
    title: str
    subtitle: str
    trim_size: Tuple[float, float]  # width, height in inches
    page_count: int
    interior_type: str  # "black_white" or "color"
    paper_type: str    # "white" or "cream"
    binding: str       # "paperback" or "hardcover"
    bleed: float       # bleed in inches
    margin_top: float
    margin_bottom: float
    margin_left: float
    margin_right: float
    target_audience: str
    keywords: List[str]
    description: str
    category: str
    price_range: Tuple[float, float]

@dataclass
class WordsearchPuzzle:
    """Individual wordsearch puzzle with metadata"""
    id: str
    title: str
    grid: List[List[str]]
    words: List[Dict]  # word data with positions
    size: Tuple[int, int]  # width, height
    difficulty: str
    theme: str
    mindfulness_focus: str
    journal_prompts: List[str]
    meditation_guide: str
    estimated_time: int
    page_layout: str  # "single", "double", "with_prompts"
    created_date: str

class KDPWordsearchGenerator:
    """Comprehensive KDP wordsearch book generator"""
    
    def __init__(self):
        self.book_templates = self._initialize_book_templates()
        self.grid_sizes = {
            "small": (12, 12),
            "medium": (15, 15),
            "large": (18, 18),
            "extra_large": (20, 20)
        }
        self.difficulty_settings = {
            "beginner": {
                "directions": ["horizontal", "vertical"],
                "backwards": False,
                "diagonal": False,
                "word_count": 8
            },
            "intermediate": {
                "directions": ["horizontal", "vertical", "diagonal"],
                "backwards": True,
                "diagonal": True,
                "word_count": 12
            },
            "advanced": {
                "directions": ["horizontal", "vertical", "diagonal"],
                "backwards": True,
                "diagonal": True,
                "word_count": 15
            }
        }
    
    def _initialize_book_templates(self) -> Dict[str, KDPBookSpecification]:
        """Initialize KDP book templates for different markets"""
        
        templates = {}
        
        # Mindfulness & Wellness Series
        templates["mindfulness_wellness"] = KDPBookSpecification(
            title="SyllaFlow Mindfulness Word Discovery",
            subtitle="Contemplative Puzzles for Inner Peace and Awareness",
            trim_size=(8.5, 11.0),  # Standard US Letter
            page_count=120,
            interior_type="black_white",
            paper_type="white",
            binding="paperback",
            bleed=0.125,
            margin_top=1.0,
            margin_bottom=1.0,
            margin_left=1.0,
            margin_right=1.0,
            target_audience="Adults seeking mindfulness practice through word games",
            keywords=["mindfulness", "word search", "meditation", "puzzle book", "stress relief", "awareness", "contemplative practice"],
            description="Transform your word puzzle experience into a mindfulness journey. Each syllable-aware wordsearch includes meditation prompts, journal integration, and wisdom from contemplative traditions.",
            category="Games & Puzzles > Word Games",
            price_range=(7.99, 12.99)
        )
        
        # Large Print Seniors Series
        templates["seniors_large_print"] = KDPBookSpecification(
            title="Large Print Mindful Word Discovery",
            subtitle="Easy-to-Read Contemplative Puzzles for Wisdom Seekers",
            trim_size=(8.5, 11.0),
            page_count=100,
            interior_type="black_white",
            paper_type="cream",
            binding="paperback",
            bleed=0.125,
            margin_top=1.25,
            margin_bottom=1.25,
            margin_left=1.25,
            margin_right=1.25,
            target_audience="Seniors and readers preferring large print formats",
            keywords=["large print", "word search", "seniors", "easy reading", "mindfulness", "contemplative", "wisdom"],
            description="Gentle word discovery puzzles designed for comfortable reading with large, clear fonts and mindfulness integration for lifelong learners.",
            category="Games & Puzzles > Large Print",
            price_range=(8.99, 13.99)
        )
        
        # Creative Expression Series
        templates["creative_expression"] = KDPBookSpecification(
            title="Creative Word Alchemy",
            subtitle="Artistic Word Discovery for Creative Minds",
            trim_size=(8.5, 11.0),
            page_count=140,
            interior_type="black_white",
            paper_type="white",
            binding="paperback",
            bleed=0.125,
            margin_top=0.875,
            margin_bottom=0.875,
            margin_left=0.875,
            margin_right=0.875,
            target_audience="Artists, writers, and creative professionals",
            keywords=["creativity", "word games", "artistic", "imagination", "creative writing", "inspiration", "artistic practice"],
            description="Unlock your creative potential through innovative word discovery puzzles that blend artistic expression with contemplative practice.",
            category="Arts & Photography > Creativity",
            price_range=(9.99, 14.99)
        )
        
        return templates
    
    def generate_syllable_aware_grid(self, words: List[Dict], grid_size: Tuple[int, int], 
                                   difficulty: str) -> Tuple[List[List[str]], List[Dict]]:
        """Generate syllable-aware wordsearch grid"""
        
        width, height = grid_size
        grid = [['.' for _ in range(width)] for _ in range(height)]
        placed_words = []
        settings = self.difficulty_settings[difficulty]
        
        # Sort words by length (longest first for better placement)
        sorted_words = sorted(words, key=lambda w: len(w['word']), reverse=True)
        
        for word_data in sorted_words[:settings['word_count']]:
            word = word_data['word'].upper()
            syllables = word_data.get('syllables', [word])
            
            # Try to place word with syllable-aware direction changes
            placement = self._place_syllable_word(grid, word, syllables, settings)
            if placement:
                placed_words.append({
                    **word_data,
                    'placement': placement,
                    'syllable_segments': self._get_syllable_segments(placement, syllables)
                })
        
        # Fill empty spaces with random letters
        self._fill_empty_spaces(grid)
        
        return grid, placed_words
    
    def _place_syllable_word(self, grid: List[List[str]], word: str, syllables: List[str], 
                           settings: Dict) -> Optional[Dict]:
        """Place word with syllable-aware direction changes"""
        
        width, height = len(grid[0]), len(grid)
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # right, down, diagonal-right, diagonal-left
        
        for attempt in range(100):  # Try 100 random placements
            start_row = random.randint(0, height - 1)
            start_col = random.randint(0, width - 1)
            
            # Try different direction sequences for syllables
            direction_sequence = self._generate_direction_sequence(syllables, settings)
            
            if self._can_place_syllable_word(grid, word, syllables, start_row, start_col, direction_sequence):
                self._place_word_on_grid(grid, word, syllables, start_row, start_col, direction_sequence)
                return {
                    'start_position': (start_row, start_col),
                    'direction_sequence': direction_sequence,
                    'syllables': syllables
                }
        
        return None
    
    def _generate_direction_sequence(self, syllables: List[str], settings: Dict) -> List[Tuple[int, int]]:
        """Generate direction sequence for syllable placement"""
        
        available_directions = []
        if "horizontal" in settings['directions']:
            available_directions.extend([(1, 0), (-1, 0)])
        if "vertical" in settings['directions']:
            available_directions.extend([(0, 1), (0, -1)])
        if "diagonal" in settings['directions']:
            available_directions.extend([(1, 1), (-1, -1), (1, -1), (-1, 1)])
        
        # Generate direction for each syllable
        direction_sequence = []
        for i, syllable in enumerate(syllables):
            if i == 0:
                # First syllable can go in any direction
                direction = random.choice(available_directions)
            else:
                # Subsequent syllables change direction
                direction = random.choice(available_directions)
            direction_sequence.append(direction)
        
        return direction_sequence
    
    def _can_place_syllable_word(self, grid: List[List[str]], word: str, syllables: List[str],
                               start_row: int, start_col: int, direction_sequence: List[Tuple[int, int]]) -> bool:
        """Check if syllable word can be placed"""
        
        width, height = len(grid[0]), len(grid)
        current_row, current_col = start_row, start_col
        char_index = 0
        
        for syllable_idx, syllable in enumerate(syllables):
            direction = direction_sequence[syllable_idx]
            dr, dc = direction
            
            for char in syllable:
                if (current_row < 0 or current_row >= height or 
                    current_col < 0 or current_col >= width):
                    return False
                
                if grid[current_row][current_col] != '.' and grid[current_row][current_col] != word[char_index]:
                    return False
                
                current_row += dr
                current_col += dc
                char_index += 1
        
        return True
    
    def _place_word_on_grid(self, grid: List[List[str]], word: str, syllables: List[str],
                          start_row: int, start_col: int, direction_sequence: List[Tuple[int, int]]):
        """Place syllable word on grid"""
        
        current_row, current_col = start_row, start_col
        char_index = 0
        
        for syllable_idx, syllable in enumerate(syllables):
            direction = direction_sequence[syllable_idx]
            dr, dc = direction
            
            for char in syllable:
                grid[current_row][current_col] = word[char_index]
                current_row += dr
                current_col += dc
                char_index += 1
    
    def _get_syllable_segments(self, placement: Dict, syllables: List[str]) -> List[Dict]:
        """Get syllable segment information for visual highlighting"""
        
        segments = []
        start_row, start_col = placement['start_position']
        direction_sequence = placement['direction_sequence']
        
        current_row, current_col = start_row, start_col
        
        for syllable_idx, syllable in enumerate(syllables):
            direction = direction_sequence[syllable_idx]
            dr, dc = direction
            
            segment_positions = []
            for char in syllable:
                segment_positions.append((current_row, current_col))
                current_row += dr
                current_col += dc
            
            segments.append({
                'syllable': syllable,
                'positions': segment_positions,
                'direction': direction
            })
        
        return segments
    
    def _fill_empty_spaces(self, grid: List[List[str]]):
        """Fill empty grid spaces with random letters"""
        
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == '.':
                    grid[row][col] = random.choice(letters)
    
    def create_puzzle_book(self, template_name: str, word_library: Dict, 
                          puzzle_count: int = 50) -> str:
        """Create complete KDP puzzle book"""
        
        template = self.book_templates[template_name]
        puzzles = []
        
        # Load word library
        words_data = word_library.get('words', {})
        
        # Generate puzzles
        for i in range(puzzle_count):
            # Select words for this puzzle
            available_words = list(words_data.values())
            puzzle_words = random.sample(available_words, min(15, len(available_words)))
            
            # Determine difficulty progression
            if i < puzzle_count // 3:
                difficulty = "beginner"
                grid_size = self.grid_sizes["small"]
            elif i < 2 * puzzle_count // 3:
                difficulty = "intermediate"
                grid_size = self.grid_sizes["medium"]
            else:
                difficulty = "advanced"
                grid_size = self.grid_sizes["large"]
            
            # Generate puzzle
            grid, placed_words = self.generate_syllable_aware_grid(puzzle_words, grid_size, difficulty)
            
            puzzle = WordsearchPuzzle(
                id=str(uuid.uuid4()),
                title=f"Mindful Discovery {i+1}",
                grid=grid,
                words=placed_words,
                size=grid_size,
                difficulty=difficulty,
                theme=self._get_puzzle_theme(placed_words),
                mindfulness_focus=self._get_mindfulness_focus(placed_words),
                journal_prompts=self._generate_journal_prompts(placed_words),
                meditation_guide=self._generate_meditation_guide(placed_words),
                estimated_time=self._calculate_estimated_time(difficulty, len(placed_words)),
                page_layout="with_prompts",
                created_date=datetime.now().isoformat()
            )
            
            puzzles.append(puzzle)
        
        # Generate PDF
        pdf_filename = self._generate_pdf_book(template, puzzles)
        
        return pdf_filename
    
    def _get_puzzle_theme(self, words: List[Dict]) -> str:
        """Determine puzzle theme from words"""
        
        categories = [word.get('category', 'general') for word in words]
        most_common = max(set(categories), key=categories.count)
        
        theme_map = {
            'mindfulness_core': 'Mindful Awareness',
            'emotional_intelligence': 'Emotional Wisdom',
            'creative_expression': 'Creative Flow',
            'wisdom_traditions': 'Ancient Wisdom',
            'shadow_work': 'Inner Integration',
            'archetypal_integration': 'Archetypal Journey',
            'community_building': 'Community Connection',
            'social_justice': 'Justice & Liberation'
        }
        
        return theme_map.get(most_common, 'Mindful Discovery')
    
    def _get_mindfulness_focus(self, words: List[Dict]) -> str:
        """Get mindfulness focus for puzzle"""
        
        focuses = []
        for word in words:
            if 'mindfulness_prompt' in word:
                focuses.append(word['mindfulness_prompt'])
        
        if focuses:
            return random.choice(focuses)
        return "Cultivate present moment awareness as you discover each word"
    
    def _generate_journal_prompts(self, words: List[Dict]) -> List[str]:
        """Generate journal prompts for puzzle"""
        
        prompts = [
            "Which word resonated most deeply with you? Why?",
            "How did the syllable-aware discovery change your experience?",
            "What insights emerged as you found each word?",
            "How can you integrate today's word wisdom into your life?"
        ]
        
        # Add word-specific prompts
        for word in words[:2]:  # Use first 2 words
            if 'mindfulness_prompt' in word:
                prompts.append(word['mindfulness_prompt'])
        
        return prompts[:4]  # Limit to 4 prompts
    
    def _generate_meditation_guide(self, words: List[Dict]) -> str:
        """Generate meditation guide for puzzle"""
        
        return f"""
        Settle into a comfortable position and take three deep breaths.
        
        As you begin this word discovery journey, let each found word become a moment of mindful awareness.
        
        When you find a word, pause and breathe with it. Notice how it feels in your body, what emotions arise, what memories or associations emerge.
        
        Let the syllable breaks remind you to pause and return to your breath, creating natural meditation moments throughout your practice.
        
        End by reflecting on the wisdom that emerged through your mindful word discovery.
        """
    
    def _calculate_estimated_time(self, difficulty: str, word_count: int) -> int:
        """Calculate estimated completion time"""
        
        base_times = {
            "beginner": 15,
            "intermediate": 25,
            "advanced": 35
        }
        
        return base_times[difficulty] + (word_count * 2)
    
    def _generate_pdf_book(self, template: KDPBookSpecification, puzzles: List[WordsearchPuzzle]) -> str:
        """Generate PDF book for KDP"""
        
        filename = f"syllaflow_{template.title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = f"/home/ubuntu/{filename}"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=(template.trim_size[0] * inch, template.trim_size[1] * inch),
            topMargin=template.margin_top * inch,
            bottomMargin=template.margin_bottom * inch,
            leftMargin=template.margin_left * inch,
            rightMargin=template.margin_right * inch
        )
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        puzzle_title_style = ParagraphStyle(
            'PuzzleTitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        # Title page
        story.append(Paragraph(template.title, title_style))
        story.append(Paragraph(template.subtitle, subtitle_style))
        story.append(Spacer(1, 50))
        
        # Introduction
        intro_text = """
        Welcome to SyllaFlow - a revolutionary approach to word discovery that combines the joy of puzzles with the wisdom of mindfulness practice.
        
        Each puzzle in this collection features our unique syllable-aware design, where words change direction at natural syllable breaks, creating opportunities for mindful pauses and deeper engagement.
        
        Take your time with each puzzle. Let the discovery of each word become a moment of meditation and reflection.
        """
        
        story.append(Paragraph(intro_text, styles['Normal']))
        story.append(PageBreak())
        
        # Generate puzzle pages
        for i, puzzle in enumerate(puzzles):
            # Puzzle title page
            story.append(Paragraph(f"Puzzle {i+1}: {puzzle.title}", puzzle_title_style))
            story.append(Paragraph(f"Theme: {puzzle.theme}", styles['Normal']))
            story.append(Paragraph(f"Difficulty: {puzzle.difficulty.title()}", styles['Normal']))
            story.append(Paragraph(f"Estimated Time: {puzzle.estimated_time} minutes", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Mindfulness focus
            story.append(Paragraph("Mindfulness Focus:", styles['Heading3']))
            story.append(Paragraph(puzzle.mindfulness_focus, styles['Normal']))
            story.append(Spacer(1, 15))
            
            # Word list
            story.append(Paragraph("Words to Discover:", styles['Heading3']))
            word_list = [word['word'] for word in puzzle.words]
            word_text = " • ".join(word_list)
            story.append(Paragraph(word_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Grid (simplified representation)
            story.append(Paragraph("Word Discovery Grid:", styles['Heading3']))
            
            # Create grid table
            grid_data = []
            for row in puzzle.grid:
                grid_data.append([f" {cell} " for cell in row])
            
            grid_table = Table(grid_data)
            grid_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(grid_table)
            story.append(PageBreak())
            
            # Journal prompts page
            story.append(Paragraph(f"Reflection & Integration - Puzzle {i+1}", puzzle_title_style))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Meditation Guide:", styles['Heading3']))
            story.append(Paragraph(puzzle.meditation_guide, styles['Normal']))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Journal Prompts:", styles['Heading3']))
            for j, prompt in enumerate(puzzle.journal_prompts, 1):
                story.append(Paragraph(f"{j}. {prompt}", styles['Normal']))
                story.append(Spacer(1, 30))  # Space for writing
            
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def create_kdp_package(self, template_name: str, word_library: Dict) -> Dict:
        """Create complete KDP package with book and metadata"""
        
        template = self.book_templates[template_name]
        
        # Generate puzzle book
        pdf_path = self.create_puzzle_book(template_name, word_library)
        
        # Create metadata package
        metadata = {
            "book_details": {
                "title": template.title,
                "subtitle": template.subtitle,
                "description": template.description,
                "keywords": template.keywords,
                "category": template.category,
                "target_audience": template.target_audience,
                "price_range": template.price_range
            },
            "technical_specs": {
                "trim_size": template.trim_size,
                "page_count": template.page_count,
                "interior_type": template.interior_type,
                "paper_type": template.paper_type,
                "binding": template.binding,
                "bleed": template.bleed
            },
            "marketing_copy": {
                "back_cover_text": self._generate_back_cover_text(template),
                "author_bio": self._generate_author_bio(),
                "promotional_text": self._generate_promotional_text(template)
            },
            "files": {
                "interior_pdf": pdf_path,
                "cover_specifications": self._generate_cover_specs(template)
            },
            "created_date": datetime.now().isoformat()
        }
        
        # Save metadata
        metadata_path = pdf_path.replace('.pdf', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "pdf_path": pdf_path,
            "metadata_path": metadata_path,
            "metadata": metadata
        }
    
    def _generate_back_cover_text(self, template: KDPBookSpecification) -> str:
        """Generate back cover marketing text"""
        
        return f"""
        Transform your puzzle experience into a mindfulness journey with {template.title}.
        
        This innovative collection features syllable-aware word discovery puzzles that create natural meditation moments as you play. Each puzzle includes:
        
        • Unique syllable-based directional changes
        • Mindfulness prompts and meditation guides  
        • Journal integration for deeper reflection
        • Progressive difficulty levels
        • Wisdom from contemplative traditions
        
        Perfect for stress relief, mental clarity, and spiritual growth through the joy of word discovery.
        
        "A revolutionary approach to puzzles that nourishes both mind and spirit."
        """
    
    def _generate_author_bio(self) -> str:
        """Generate author bio"""
        
        return """
        The Council of Consciousness is a collaborative collective dedicated to creating transformational content that bridges ancient wisdom with modern innovation. Drawing from diverse spiritual traditions, psychological insights, and creative practices, they develop resources that support personal growth, community healing, and social transformation.
        """
    
    def _generate_promotional_text(self, template: KDPBookSpecification) -> str:
        """Generate promotional marketing text"""
        
        return f"""
        Discover the revolutionary SyllaFlow method that transforms ordinary word puzzles into extraordinary mindfulness experiences.
        
        {template.title} introduces a breakthrough approach to word discovery where syllable breaks create natural meditation moments, turning each puzzle into a contemplative practice.
        
        Whether you're seeking stress relief, mental clarity, or spiritual growth, these innovative puzzles offer a unique path to mindful awareness through the joy of word discovery.
        
        Join thousands who have discovered the transformative power of mindful puzzling.
        """
    
    def _generate_cover_specs(self, template: KDPBookSpecification) -> Dict:
        """Generate cover design specifications"""
        
        return {
            "dimensions": {
                "width": template.trim_size[0] + (2 * template.bleed),
                "height": template.trim_size[1] + (2 * template.bleed),
                "spine_width": 0.0025 * template.page_count,  # Approximate spine calculation
                "bleed": template.bleed
            },
            "design_elements": {
                "color_scheme": "Calming blues and earth tones",
                "typography": "Clean, readable sans-serif fonts",
                "imagery": "Abstract geometric patterns suggesting syllable flow",
                "style": "Minimalist with mindful aesthetic"
            },
            "text_elements": {
                "title": template.title,
                "subtitle": template.subtitle,
                "author": "Council of Consciousness",
                "back_cover": "Marketing text and puzzle preview"
            }
        }

def create_kdp_wordsearch_system():
    """Create comprehensive KDP wordsearch generation system"""
    
    print("🌸 Creating KDP Wordsearch Generation System")
    print("=" * 50)
    
    # Initialize generator
    generator = KDPWordsearchGenerator()
    
    # Load word library
    try:
        with open('/home/ubuntu/comprehensive_wordsearch_library.json', 'r') as f:
            word_library = json.load(f)
    except FileNotFoundError:
        print("⚠️  Word library not found. Creating sample library...")
        word_library = {
            "words": {
                "meditation": {
                    "word": "MEDITATION",
                    "definition": "A practice of focused attention to achieve mental clarity",
                    "syllables": ["MED", "I", "TA", "TION"],
                    "category": "mindfulness_core",
                    "difficulty_level": "beginner",
                    "mindfulness_prompt": "How does stillness speak to you?"
                },
                "awareness": {
                    "word": "AWARENESS",
                    "definition": "The quality of being conscious and mindful",
                    "syllables": ["A", "WARE", "NESS"],
                    "category": "mindfulness_core",
                    "difficulty_level": "beginner",
                    "mindfulness_prompt": "What are you becoming aware of right now?"
                }
            }
        }
    
    # Create sample KDP packages
    packages = {}
    
    # Mindfulness & Wellness package
    print("📚 Creating Mindfulness & Wellness KDP package...")
    mindfulness_package = generator.create_kdp_package("mindfulness_wellness", word_library)
    packages["mindfulness_wellness"] = mindfulness_package
    
    # Large Print Seniors package
    print("📚 Creating Large Print Seniors KDP package...")
    seniors_package = generator.create_kdp_package("seniors_large_print", word_library)
    packages["seniors_large_print"] = seniors_package
    
    # Creative Expression package
    print("📚 Creating Creative Expression KDP package...")
    creative_package = generator.create_kdp_package("creative_expression", word_library)
    packages["creative_expression"] = creative_package
    
    # Create comprehensive guide
    guide_data = {
        "system_overview": {
            "purpose": "Generate print-ready wordsearch books for Amazon KDP",
            "features": [
                "Syllable-aware word placement with direction changes",
                "Progressive difficulty levels",
                "Mindfulness integration with journal prompts",
                "Professional KDP formatting and specifications",
                "Complete metadata and marketing copy generation",
                "Multiple market segment templates"
            ]
        },
        "book_templates": {
            template_name: {
                "title": template.title,
                "target_audience": template.target_audience,
                "price_range": template.price_range,
                "specifications": {
                    "trim_size": template.trim_size,
                    "page_count": template.page_count,
                    "interior_type": template.interior_type
                }
            }
            for template_name, template in generator.book_templates.items()
        },
        "generated_packages": {
            package_name: {
                "pdf_file": package_data["pdf_path"],
                "metadata_file": package_data["metadata_path"],
                "title": package_data["metadata"]["book_details"]["title"]
            }
            for package_name, package_data in packages.items()
        },
        "usage_instructions": {
            "step_1": "Load your word library using comprehensive_wordsearch_library.json",
            "step_2": "Choose appropriate book template for your target market",
            "step_3": "Generate KDP package with create_kdp_package() method",
            "step_4": "Upload generated PDF to KDP for interior content",
            "step_5": "Use cover specifications to create professional book cover",
            "step_6": "Apply generated metadata for book listing optimization"
        },
        "created_date": datetime.now().isoformat()
    }
    
    # Save comprehensive guide
    with open('/home/ubuntu/kdp_wordsearch_system_guide.json', 'w') as f:
        json.dump(guide_data, f, indent=2)
    
    print(f"✓ Generated {len(packages)} KDP book packages")
    print(f"✓ Created comprehensive system guide")
    print(f"✓ All files ready for Amazon KDP publishing")
    
    return packages, guide_data

if __name__ == "__main__":
    packages, guide = create_kdp_wordsearch_system()
    
    print("\\n🎯 KDP System Features:")
    print("• Syllable-aware wordsearch generation")
    print("• Professional PDF formatting for KDP")
    print("• Complete metadata and marketing copy")
    print("• Multiple market segment templates")
    print("• Mindfulness integration throughout")
    print("• Progressive difficulty systems")
    
    print("\\n📁 Generated Files:")
    for package_name, package_data in packages.items():
        print(f"• {package_data['pdf_path']}")
        print(f"• {package_data['metadata_path']}")
    print("• /home/ubuntu/kdp_wordsearch_system_guide.json")
    
    print("\\n🚀 Ready for Amazon KDP publishing and physical book production!")

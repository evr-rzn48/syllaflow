#!/usr/bin/env python3
"""
MinerU Integration Module for SyllaFlow
Advanced document conversion and word extraction for mindfulness puzzle generation

This module integrates MinerU's powerful document conversion capabilities
into SyllaFlow, enabling advanced PDF and document extraction for automated
puzzle generation from complex documents.

Council of Consciousness Integration:
- Rick Rubin: Authentic simplicity in document processing
- Angela Davis: Accessible document conversion for all users
- Octavia Butler: Transformational possibilities through text extraction
- Wayne Dyer: Wisdom extraction from diverse document sources
"""

import os
import sys
import json
import logging
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Add MinerU to Python path
MINERU_PATH = "/home/ubuntu/MinerU"
if MINERU_PATH not in sys.path:
    sys.path.insert(0, MINERU_PATH)

try:
    # Import MinerU components
    from mineru.cli import main as mineru_main
    from mineru.utils import logger
    MINERU_AVAILABLE = True
except ImportError as e:
    logging.warning(f"MinerU not available: {e}")
    MINERU_AVAILABLE = False

class DocumentType(Enum):
    """Supported document types for conversion"""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    TXT = "txt"
    RTF = "rtf"
    HTML = "html"
    MARKDOWN = "md"

class ExtractionMode(Enum):
    """Word extraction modes for different puzzle types"""
    COMPREHENSIVE = "comprehensive"  # All meaningful words
    MINDFULNESS = "mindfulness"      # Mindfulness-related terms
    THEMATIC = "thematic"           # Theme-based extraction
    ACADEMIC = "academic"           # Academic/technical terms
    CREATIVE = "creative"           # Creative/artistic terms

@dataclass
class DocumentMetadata:
    """Metadata extracted from documents"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: List[str] = None
    page_count: int = 0
    word_count: int = 0
    language: Optional[str] = None
    creation_date: Optional[str] = None

@dataclass
class ExtractedContent:
    """Structured content extracted from documents"""
    text: str
    words: List[str]
    themes: List[str]
    metadata: DocumentMetadata
    syllable_data: Dict[str, List[str]]
    mindfulness_terms: List[str]
    complexity_score: float

class MinerUIntegration:
    """
    Advanced document processing integration with MinerU
    
    This class provides sophisticated document conversion and word extraction
    capabilities for SyllaFlow puzzle generation, incorporating mindfulness
    principles and Council of Consciousness wisdom.
    """
    
    def __init__(self, temp_dir: Optional[str] = None):
        """Initialize MinerU integration with optional temporary directory"""
        self.temp_dir = temp_dir or tempfile.mkdtemp(prefix="syllaflow_mineru_")
        self.logger = logging.getLogger(__name__)
        
        # Ensure temp directory exists
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize mindfulness word patterns
        self.mindfulness_patterns = self._load_mindfulness_patterns()
        
        # Initialize syllable processor
        self.syllable_processor = SyllableProcessor()
        
        self.logger.info(f"MinerU Integration initialized with temp dir: {self.temp_dir}")
    
    def _load_mindfulness_patterns(self) -> Dict[str, List[str]]:
        """Load mindfulness-related word patterns for enhanced extraction"""
        return {
            "core_mindfulness": [
                "awareness", "presence", "meditation", "mindful", "conscious",
                "attention", "focus", "breath", "breathing", "centering"
            ],
            "emotional_intelligence": [
                "empathy", "compassion", "kindness", "gratitude", "acceptance",
                "resilience", "vulnerability", "authenticity", "courage"
            ],
            "wisdom_traditions": [
                "dharma", "enlightenment", "awakening", "transformation",
                "transcendence", "unity", "interconnection", "balance"
            ],
            "creative_expression": [
                "creativity", "inspiration", "imagination", "expression",
                "artistry", "innovation", "vision", "manifestation"
            ]
        }
    
    def process_document(self, 
                        file_path: str, 
                        extraction_mode: ExtractionMode = ExtractionMode.COMPREHENSIVE,
                        output_format: str = "json") -> ExtractedContent:
        """
        Process document using MinerU and extract content for puzzle generation
        
        Args:
            file_path: Path to the document to process
            extraction_mode: Mode for word extraction
            output_format: Output format (json, markdown, text)
            
        Returns:
            ExtractedContent object with processed data
        """
        if not MINERU_AVAILABLE:
            raise RuntimeError("MinerU is not available. Please install MinerU first.")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        # Determine document type
        doc_type = self._detect_document_type(file_path)
        
        # Create output directory for MinerU
        output_dir = Path(self.temp_dir) / f"mineru_output_{file_path.stem}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Process document with MinerU
            converted_content = self._run_mineru_conversion(file_path, output_dir)
            
            # Extract and process content
            extracted_content = self._extract_content(
                converted_content, 
                extraction_mode, 
                doc_type
            )
            
            # Add metadata
            extracted_content.metadata = self._extract_metadata(file_path, converted_content)
            
            # Process syllables for SyllaFlow integration
            extracted_content.syllable_data = self.syllable_processor.process_words(
                extracted_content.words
            )
            
            # Identify mindfulness terms
            extracted_content.mindfulness_terms = self._identify_mindfulness_terms(
                extracted_content.words
            )
            
            # Calculate complexity score
            extracted_content.complexity_score = self._calculate_complexity_score(
                extracted_content
            )
            
            self.logger.info(f"Successfully processed document: {file_path}")
            return extracted_content
            
        except Exception as e:
            self.logger.error(f"Error processing document {file_path}: {e}")
            raise
    
    def _detect_document_type(self, file_path: Path) -> DocumentType:
        """Detect document type from file extension"""
        suffix = file_path.suffix.lower()
        type_mapping = {
            '.pdf': DocumentType.PDF,
            '.docx': DocumentType.DOCX,
            '.doc': DocumentType.DOC,
            '.txt': DocumentType.TXT,
            '.rtf': DocumentType.RTF,
            '.html': DocumentType.HTML,
            '.htm': DocumentType.HTML,
            '.md': DocumentType.MARKDOWN,
            '.markdown': DocumentType.MARKDOWN
        }
        return type_mapping.get(suffix, DocumentType.PDF)
    
    def _run_mineru_conversion(self, file_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Run MinerU conversion on the document"""
        try:
            # Prepare MinerU command arguments
            args = [
                str(file_path),
                "--output-dir", str(output_dir),
                "--output-format", "json",
                "--backend", "pipeline"  # Use pipeline backend for better text extraction
            ]
            
            # Run MinerU conversion
            # Note: This is a simplified integration - in production, you'd want to
            # use MinerU's Python API directly rather than subprocess
            result = subprocess.run([
                sys.executable, "-m", "mineru.cli"
            ] + args, 
            capture_output=True, 
            text=True, 
            cwd=MINERU_PATH
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"MinerU conversion failed: {result.stderr}")
            
            # Load the converted content
            content_file = output_dir / f"{file_path.stem}.json"
            if content_file.exists():
                with open(content_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Fallback: create basic content structure
                return {
                    "content": result.stdout,
                    "pages": [],
                    "metadata": {}
                }
                
        except Exception as e:
            self.logger.error(f"MinerU conversion error: {e}")
            # Fallback to basic text extraction
            return self._fallback_text_extraction(file_path)
    
    def _fallback_text_extraction(self, file_path: Path) -> Dict[str, Any]:
        """Fallback text extraction when MinerU is not available"""
        try:
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # For other formats, return basic structure
                content = f"Document: {file_path.name}\nContent extraction requires MinerU installation."
            
            return {
                "content": content,
                "pages": [{"content": content}],
                "metadata": {"source": str(file_path)}
            }
        except Exception as e:
            self.logger.error(f"Fallback extraction failed: {e}")
            return {
                "content": "",
                "pages": [],
                "metadata": {}
            }
    
    def _extract_content(self, 
                        converted_content: Dict[str, Any], 
                        extraction_mode: ExtractionMode,
                        doc_type: DocumentType) -> ExtractedContent:
        """Extract and process content based on extraction mode"""
        
        # Extract raw text
        raw_text = self._extract_raw_text(converted_content)
        
        # Extract words based on mode
        words = self._extract_words(raw_text, extraction_mode)
        
        # Extract themes
        themes = self._extract_themes(raw_text, words)
        
        return ExtractedContent(
            text=raw_text,
            words=words,
            themes=themes,
            metadata=DocumentMetadata(),
            syllable_data={},
            mindfulness_terms=[],
            complexity_score=0.0
        )
    
    def _extract_raw_text(self, converted_content: Dict[str, Any]) -> str:
        """Extract raw text from converted content"""
        text_parts = []
        
        # Extract from main content
        if "content" in converted_content:
            text_parts.append(converted_content["content"])
        
        # Extract from pages
        if "pages" in converted_content:
            for page in converted_content["pages"]:
                if isinstance(page, dict) and "content" in page:
                    text_parts.append(page["content"])
                elif isinstance(page, str):
                    text_parts.append(page)
        
        return "\n".join(text_parts)
    
    def _extract_words(self, text: str, mode: ExtractionMode) -> List[str]:
        """Extract words based on extraction mode"""
        import re
        
        # Basic word extraction
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = list(set(words))  # Remove duplicates
        
        # Filter based on mode
        if mode == ExtractionMode.MINDFULNESS:
            mindfulness_words = []
            for category, patterns in self.mindfulness_patterns.items():
                for word in words:
                    if any(pattern in word for pattern in patterns):
                        mindfulness_words.append(word)
            words = mindfulness_words
        
        elif mode == ExtractionMode.ACADEMIC:
            # Filter for longer, more complex words
            words = [w for w in words if len(w) >= 5]
        
        elif mode == ExtractionMode.CREATIVE:
            # Filter for creative/artistic terms
            creative_indicators = [
                'art', 'create', 'design', 'express', 'imagine', 'inspire',
                'beauty', 'aesthetic', 'vision', 'craft', 'form', 'style'
            ]
            creative_words = []
            for word in words:
                if any(indicator in word for indicator in creative_indicators):
                    creative_words.append(word)
            words = creative_words
        
        # Sort by length and frequency potential
        words.sort(key=lambda x: (len(x), x))
        
        return words[:100]  # Limit to top 100 words
    
    def _extract_themes(self, text: str, words: List[str]) -> List[str]:
        """Extract thematic content from text"""
        themes = []
        
        # Analyze word patterns for themes
        word_freq = {}
        for word in words:
            word_freq[word] = text.lower().count(word)
        
        # Identify top themes based on word frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Group related words into themes
        theme_groups = {
            "mindfulness": ["mind", "aware", "present", "meditat", "breath"],
            "wisdom": ["wisdom", "knowledge", "understand", "insight", "truth"],
            "growth": ["grow", "develop", "transform", "change", "evolve"],
            "connection": ["connect", "relation", "community", "together", "unity"]
        }
        
        for theme, keywords in theme_groups.items():
            theme_score = sum(word_freq.get(word, 0) for word in words 
                            if any(keyword in word for keyword in keywords))
            if theme_score > 0:
                themes.append(theme)
        
        return themes
    
    def _extract_metadata(self, file_path: Path, converted_content: Dict[str, Any]) -> DocumentMetadata:
        """Extract document metadata"""
        metadata = converted_content.get("metadata", {})
        
        return DocumentMetadata(
            title=metadata.get("title", file_path.stem),
            author=metadata.get("author"),
            subject=metadata.get("subject"),
            keywords=metadata.get("keywords", []),
            page_count=len(converted_content.get("pages", [])),
            word_count=len(converted_content.get("content", "").split()),
            language=metadata.get("language", "en"),
            creation_date=metadata.get("creation_date")
        )
    
    def _identify_mindfulness_terms(self, words: List[str]) -> List[str]:
        """Identify mindfulness-related terms from word list"""
        mindfulness_terms = []
        
        for word in words:
            for category, patterns in self.mindfulness_patterns.items():
                if any(pattern in word.lower() for pattern in patterns):
                    mindfulness_terms.append(word)
                    break
        
        return list(set(mindfulness_terms))
    
    def _calculate_complexity_score(self, content: ExtractedContent) -> float:
        """Calculate complexity score for content"""
        # Factors: word length, vocabulary diversity, theme richness
        avg_word_length = sum(len(word) for word in content.words) / len(content.words) if content.words else 0
        vocab_diversity = len(set(content.words)) / len(content.words) if content.words else 0
        theme_richness = len(content.themes) / 10  # Normalize to 0-1 scale
        
        complexity_score = (avg_word_length / 10 + vocab_diversity + theme_richness) / 3
        return min(complexity_score, 1.0)  # Cap at 1.0
    
    def batch_process_documents(self, 
                               file_paths: List[str],
                               extraction_mode: ExtractionMode = ExtractionMode.COMPREHENSIVE) -> List[ExtractedContent]:
        """Process multiple documents in batch"""
        results = []
        
        for file_path in file_paths:
            try:
                result = self.process_document(file_path, extraction_mode)
                results.append(result)
                self.logger.info(f"Processed: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to process {file_path}: {e}")
                # Add empty result to maintain list alignment
                results.append(ExtractedContent(
                    text="", words=[], themes=[], 
                    metadata=DocumentMetadata(), 
                    syllable_data={}, mindfulness_terms=[], 
                    complexity_score=0.0
                ))
        
        return results
    
    def export_for_puzzle_generation(self, 
                                   content: ExtractedContent, 
                                   puzzle_type: str = "syllaflow") -> Dict[str, Any]:
        """Export processed content in format suitable for puzzle generation"""
        
        export_data = {
            "puzzle_type": puzzle_type,
            "source_metadata": {
                "title": content.metadata.title,
                "author": content.metadata.author,
                "word_count": content.metadata.word_count,
                "complexity_score": content.complexity_score
            },
            "word_data": {
                "words": content.words,
                "syllable_data": content.syllable_data,
                "mindfulness_terms": content.mindfulness_terms
            },
            "themes": content.themes,
            "generation_config": {
                "grid_size": "auto",  # Auto-determine based on word count
                "difficulty": self._determine_difficulty(content.complexity_score),
                "mindfulness_integration": len(content.mindfulness_terms) > 0
            }
        }
        
        return export_data
    
    def _determine_difficulty(self, complexity_score: float) -> str:
        """Determine puzzle difficulty based on complexity score"""
        if complexity_score < 0.3:
            return "beginner"
        elif complexity_score < 0.7:
            return "intermediate"
        else:
            return "advanced"
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            self.logger.info(f"Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            self.logger.error(f"Error cleaning up temp directory: {e}")

class SyllableProcessor:
    """
    Advanced syllable processing for SyllaFlow integration
    
    This class handles syllable detection and processing for the unique
    syllable-based directional word search mechanics.
    """
    
    def __init__(self):
        """Initialize syllable processor"""
        self.vowels = set('aeiouAEIOU')
        self.consonant_clusters = [
            'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr',
            'sc', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'tr', 'tw', 'th',
            'ch', 'sh', 'wh', 'ph', 'gh'
        ]
    
    def process_words(self, words: List[str]) -> Dict[str, List[str]]:
        """Process words to extract syllable information"""
        syllable_data = {}
        
        for word in words:
            syllables = self.split_syllables(word)
            syllable_data[word] = syllables
        
        return syllable_data
    
    def split_syllables(self, word: str) -> List[str]:
        """Split word into syllables using advanced heuristics"""
        word = word.lower().strip()
        if len(word) <= 2:
            return [word]
        
        syllables = []
        current_syllable = ""
        
        i = 0
        while i < len(word):
            char = word[i]
            current_syllable += char
            
            # Check for syllable boundary
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
        
        return syllables if syllables else [word]
    
    def _is_syllable_boundary(self, word: str, position: int) -> bool:
        """Determine if position is a syllable boundary"""
        if position >= len(word) - 1:
            return False
        
        current = word[position]
        next_char = word[position + 1]
        
        # Vowel followed by consonant
        if current in self.vowels and next_char not in self.vowels:
            # Check for consonant clusters
            if position + 2 < len(word):
                cluster = word[position + 1:position + 3]
                if cluster in self.consonant_clusters:
                    return False
            return True
        
        return False

def main():
    """Test the MinerU integration module"""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize integration
    integration = MinerUIntegration()
    
    # Test with a sample document (if available)
    test_file = "/home/ubuntu/sample_document.txt"
    
    # Create a test document if it doesn't exist
    if not Path(test_file).exists():
        with open(test_file, 'w') as f:
            f.write("""
            Mindfulness and Meditation: A Path to Inner Peace
            
            Mindfulness is the practice of being fully present and aware in the current moment.
            Through meditation, we cultivate awareness, compassion, and wisdom.
            This transformative practice helps us develop resilience, creativity, and authentic connection.
            
            The journey of mindfulness involves breathing exercises, contemplation, and reflection.
            As we deepen our practice, we discover inner peace, balance, and profound understanding.
            """)
    
    try:
        # Process the document
        result = integration.process_document(
            test_file, 
            ExtractionMode.MINDFULNESS
        )
        
        print("=== MinerU Integration Test Results ===")
        print(f"Words extracted: {len(result.words)}")
        print(f"Sample words: {result.words[:10]}")
        print(f"Themes: {result.themes}")
        print(f"Mindfulness terms: {result.mindfulness_terms}")
        print(f"Complexity score: {result.complexity_score:.2f}")
        
        # Export for puzzle generation
        export_data = integration.export_for_puzzle_generation(result)
        print(f"Export data keys: {list(export_data.keys())}")
        
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        # Cleanup
        integration.cleanup()

if __name__ == "__main__":
    main()

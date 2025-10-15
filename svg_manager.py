#!/usr/bin/env python3
"""
SVG Manager - Extract and restore SVG content from HTML files

This script provides functionality to:
1. Extract all SVG tags from HTML files and store them separately
2. Replace SVGs with unique placeholders containing context information
3. Restore SVGs back to their original positions using the placeholders

Usage:
    python svg_manager.py extract input.html --output svgs.json
    python svg_manager.py restore input.html svgs.json --output restored.html
"""

import re
import json
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


class SVGManager:
    """Manages extraction and restoration of SVG content in HTML files."""
    
    # Regex pattern to match complete SVG tags (including nested content)
    SVG_PATTERN = re.compile(
        r'<svg\s+[^>]*>.*?</svg>',
        re.DOTALL | re.IGNORECASE
    )
    
    # Pattern to match our custom placeholders
    PLACEHOLDER_PATTERN = re.compile(
        r'<!--\s*SVG_PLACEHOLDER_START:([a-f0-9_]+)\s*-->'
        r'.*?'
        r'<!--\s*SVG_PLACEHOLDER_END:\1\s*-->',
        re.DOTALL
    )
    
    def __init__(self, context_chars: int = 150):
        """
        Initialize SVG Manager.
        
        Args:
            context_chars: Number of characters to capture before/after SVG for context
        """
        self.context_chars = context_chars
        
    def _generate_svg_id(self, svg_content: str, index: int) -> str:
        """
        Generate a unique ID for an SVG element.
        
        Args:
            svg_content: The SVG content string
            index: The index of this SVG in the document
            
        Returns:
            Unique identifier string
        """
        # Create hash from SVG content
        content_hash = hashlib.md5(svg_content.encode()).hexdigest()[:8]
        return f"{index:04d}_{content_hash}"
    
    def _extract_context(self, html: str, start_pos: int, end_pos: int) -> Tuple[str, str]:
        """
        Extract context before and after an SVG position.
        
        Args:
            html: The full HTML content
            start_pos: Start position of the SVG
            end_pos: End position of the SVG
            
        Returns:
            Tuple of (context_before, context_after)
        """
        # Extract context before SVG
        context_before_start = max(0, start_pos - self.context_chars)
        context_before = html[context_before_start:start_pos].strip()
        
        # Extract context after SVG
        context_after_end = min(len(html), end_pos + self.context_chars)
        context_after = html[end_pos:context_after_end].strip()
        
        # Clean up context (remove excessive whitespace)
        context_before = re.sub(r'\s+', ' ', context_before)
        context_after = re.sub(r'\s+', ' ', context_after)
        
        return context_before, context_after
    
    def _create_placeholder(self, svg_id: str, context_before: str, context_after: str) -> str:
        """
        Create a placeholder for an SVG element.
        
        Args:
            svg_id: Unique identifier for the SVG
            context_before: Context before the SVG
            context_after: Context after the SVG
            
        Returns:
            Placeholder HTML string
        """
        placeholder = f"""<!-- SVG_PLACEHOLDER_START:{svg_id} -->
<!-- CONTEXT_BEFORE: {context_before[:100]} -->
<!-- CONTEXT_AFTER: {context_after[:100]} -->
<span class="svg-placeholder" data-svg-id="{svg_id}"></span>
<!-- SVG_PLACEHOLDER_END:{svg_id} -->"""
        return placeholder
    
    def extract_svgs(self, html_content: str) -> Tuple[str, List[Dict]]:
        """
        Extract all SVG elements from HTML and replace with placeholders.
        
        Args:
            html_content: The HTML content string
            
        Returns:
            Tuple of (modified_html, svg_data_list)
            - modified_html: HTML with SVGs replaced by placeholders
            - svg_data_list: List of dicts containing SVG data and metadata
        """
        svg_data_list = []
        modified_html = html_content
        offset = 0  # Track position offset due to replacements
        
        # Find all SVG matches
        for index, match in enumerate(self.SVG_PATTERN.finditer(html_content)):
            svg_content = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            
            # Adjust positions for previous replacements
            adjusted_start = start_pos + offset
            adjusted_end = end_pos + offset
            
            # Generate unique ID
            svg_id = self._generate_svg_id(svg_content, index)
            
            # Extract context
            context_before, context_after = self._extract_context(
                html_content, start_pos, end_pos
            )
            
            # Create placeholder
            placeholder = self._create_placeholder(
                svg_id, context_before, context_after
            )
            
            # Replace SVG with placeholder in modified HTML
            modified_html = (
                modified_html[:adjusted_start] + 
                placeholder + 
                modified_html[adjusted_end:]
            )
            
            # Update offset
            offset += len(placeholder) - len(svg_content)
            
            # Store SVG data
            svg_data = {
                'id': svg_id,
                'index': index,
                'svg_content': svg_content,
                'context_before': context_before,
                'context_after': context_after,
                'original_position': {
                    'start': start_pos,
                    'end': end_pos
                }
            }
            svg_data_list.append(svg_data)
        
        return modified_html, svg_data_list
    
    def restore_svgs(self, html_content: str, svg_data_list: List[Dict]) -> str:
        """
        Restore SVG elements from placeholders back into HTML.
        
        Args:
            html_content: HTML content with placeholders
            svg_data_list: List of SVG data from extraction
            
        Returns:
            HTML content with SVGs restored
        """
        restored_html = html_content
        
        # Create a map of svg_id to svg_content for quick lookup
        svg_map = {svg_data['id']: svg_data['svg_content'] 
                   for svg_data in svg_data_list}
        
        # Find and replace all placeholders
        def replace_placeholder(match):
            svg_id = match.group(1)
            if svg_id in svg_map:
                return svg_map[svg_id]
            else:
                # If SVG not found, keep placeholder
                print(f"Warning: SVG with ID {svg_id} not found in data")
                return match.group(0)
        
        restored_html = self.PLACEHOLDER_PATTERN.sub(replace_placeholder, restored_html)
        
        return restored_html
    
    def save_svg_data(self, svg_data_list: List[Dict], output_path: str) -> None:
        """
        Save SVG data to a JSON file.
        
        Args:
            svg_data_list: List of SVG data
            output_path: Path to output JSON file
        """
        data = {
            'metadata': {
                'extraction_date': datetime.now().isoformat(),
                'total_svgs': len(svg_data_list),
                'context_chars': self.context_chars
            },
            'svgs': svg_data_list
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(svg_data_list)} SVG elements to {output_path}")
    
    def load_svg_data(self, input_path: str) -> List[Dict]:
        """
        Load SVG data from a JSON file.
        
        Args:
            input_path: Path to input JSON file
            
        Returns:
            List of SVG data dictionaries
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        svg_data_list = data.get('svgs', [])
        metadata = data.get('metadata', {})
        
        print(f"Loaded {len(svg_data_list)} SVG elements from {input_path}")
        if metadata:
            print(f"  Extraction date: {metadata.get('extraction_date', 'Unknown')}")
        
        return svg_data_list
    
    def get_svg_stats(self, svg_data_list: List[Dict]) -> Dict:
        """
        Get statistics about extracted SVGs.
        
        Args:
            svg_data_list: List of SVG data
            
        Returns:
            Dictionary containing statistics
        """
        if not svg_data_list:
            return {'total': 0}
        
        sizes = [len(svg['svg_content']) for svg in svg_data_list]
        
        stats = {
            'total': len(svg_data_list),
            'min_size': min(sizes),
            'max_size': max(sizes),
            'avg_size': sum(sizes) / len(sizes),
            'total_size': sum(sizes)
        }
        
        return stats


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Extract and restore SVG content from HTML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Extract SVGs from an HTML file:
    python svg_manager.py extract index.html --output svgs.json
  
  Restore SVGs back to HTML:
    python svg_manager.py restore index_with_placeholders.html svgs.json --output restored.html
  
  Show statistics:
    python svg_manager.py stats svgs.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract SVGs from HTML')
    extract_parser.add_argument('input', help='Input HTML file')
    extract_parser.add_argument('--output', '-o', help='Output JSON file for SVG data',
                               default='svgs.json')
    extract_parser.add_argument('--html-output', help='Output HTML file with placeholders',
                               default=None)
    extract_parser.add_argument('--context', type=int, default=150,
                               help='Number of context characters (default: 150)')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore SVGs to HTML')
    restore_parser.add_argument('input', help='Input HTML file with placeholders')
    restore_parser.add_argument('svg_data', help='JSON file containing SVG data')
    restore_parser.add_argument('--output', '-o', help='Output HTML file',
                               default='restored.html')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show SVG statistics')
    stats_parser.add_argument('svg_data', help='JSON file containing SVG data')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = SVGManager(context_chars=getattr(args, 'context', 150))
    
    if args.command == 'extract':
        # Read input HTML
        with open(args.input, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract SVGs
        print(f"Extracting SVGs from {args.input}...")
        modified_html, svg_data_list = manager.extract_svgs(html_content)
        
        # Save SVG data
        manager.save_svg_data(svg_data_list, args.output)
        
        # Save modified HTML if requested
        if args.html_output:
            html_output = args.html_output
        else:
            input_path = Path(args.input)
            html_output = str(input_path.parent / f"{input_path.stem}_with_placeholders{input_path.suffix}")
        
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(modified_html)
        print(f"Saved modified HTML to {html_output}")
        
        # Show stats
        stats = manager.get_svg_stats(svg_data_list)
        print(f"\nStatistics:")
        print(f"  Total SVGs: {stats['total']}")
        print(f"  Total size: {stats.get('total_size', 0):,} bytes")
        if stats['total'] > 0:
            print(f"  Average size: {stats['avg_size']:.0f} bytes")
            print(f"  Size range: {stats['min_size']} - {stats['max_size']} bytes")
    
    elif args.command == 'restore':
        # Read input HTML with placeholders
        with open(args.input, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Load SVG data
        svg_data_list = manager.load_svg_data(args.svg_data)
        
        # Restore SVGs
        print(f"Restoring SVGs to {args.input}...")
        restored_html = manager.restore_svgs(html_content, svg_data_list)
        
        # Save restored HTML
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(restored_html)
        print(f"Saved restored HTML to {args.output}")
    
    elif args.command == 'stats':
        # Load SVG data
        svg_data_list = manager.load_svg_data(args.svg_data)
        
        # Show stats
        stats = manager.get_svg_stats(svg_data_list)
        print(f"\nSVG Statistics:")
        print(f"  Total SVGs: {stats['total']}")
        if stats['total'] > 0:
            print(f"  Total size: {stats['total_size']:,} bytes")
            print(f"  Average size: {stats['avg_size']:.0f} bytes")
            print(f"  Size range: {stats['min_size']} - {stats['max_size']} bytes")
            print(f"\nSVG Details:")
            for i, svg_data in enumerate(svg_data_list[:10]):  # Show first 10
                print(f"  {i+1}. ID: {svg_data['id']}, Size: {len(svg_data['svg_content'])} bytes")
            if len(svg_data_list) > 10:
                print(f"  ... and {len(svg_data_list) - 10} more")


if __name__ == '__main__':
    main()

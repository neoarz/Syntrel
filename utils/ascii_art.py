#!/usr/bin/env python3
# From https://github.com/neoarz/Velora/blob/main/Velora/ui/ascii.py

import math

def gradient_text(text, start_color, end_color):
    def rgb_interp(start, end, t):
        return tuple(int(start[i] + (end[i] - start[i]) * t) for i in range(3))
    lines = text.splitlines()
    gradient_lines = []
    total_chars = sum(len(line) for line in lines if line.strip())
    idx = 0
    for line in lines:
        colored_line = ""
        for char in line:
            if char.strip():
                t = idx / (total_chars - 1)
                r, g, b = rgb_interp(start_color, end_color, t)
                colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                idx += 1
            else:
                colored_line += char
        gradient_lines.append(colored_line)
    return "\n".join(gradient_lines)

def gradient_text_selective(text, start_color, end_color, gradient_word, white_prefix=""):
    def rgb_interp(start, end, t):
        return tuple(int(start[i] + (end[i] - start[i]) * t) for i in range(3))
    
    lines = text.splitlines()
    result_lines = []
    
    for line in lines:
        if gradient_word in line and white_prefix in line:
            prefix_start = line.find(white_prefix)
            word_start = line.find(gradient_word)
            
            if prefix_start != -1 and word_start != -1:
                before_prefix = line[:prefix_start]
                prefix_part = line[prefix_start:word_start]
                word_part = gradient_word
                after_word = line[word_start + len(gradient_word):]
                
                colored_before = ""
                total_chars = sum(1 for char in before_prefix if char.strip())
                idx = 0
                for char in before_prefix:
                    if char.strip():
                        t = idx / max(1, total_chars - 1)
                        r, g, b = rgb_interp(start_color, end_color, t)
                        colored_before += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                        idx += 1
                    else:
                        colored_before += char
                
                white_prefix_colored = f"\033[38;2;255;255;255m{prefix_part}\033[0m"
                
                colored_word = ""
                word_chars = [char for char in word_part if char.strip()]
                for i, char in enumerate(word_part):
                    if char.strip():
                        t = i / max(1, len(word_chars) - 1)
                        r, g, b = rgb_interp(start_color, end_color, t)
                        colored_word += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                    else:
                        colored_word += char
                
                result_lines.append(colored_before + white_prefix_colored + colored_word + after_word)
            else:
                colored_line = ""
                total_chars = sum(1 for char in line if char.strip())
                idx = 0
                for char in line:
                    if char.strip():
                        t = idx / max(1, total_chars - 1)
                        r, g, b = rgb_interp(start_color, end_color, t)
                        colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                        idx += 1
                    else:
                        colored_line += char
                result_lines.append(colored_line)
        else:
            colored_line = ""
            total_chars = sum(1 for char in line if char.strip())
            idx = 0
            for char in line:
                if char.strip():
                    t = idx / max(1, total_chars - 1)
                    r, g, b = rgb_interp(start_color, end_color, t)
                    colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                    idx += 1
                else:
                    colored_line += char
            result_lines.append(colored_line)
    
    return "\n".join(result_lines)


_ascii_art = """
███████╗██╗   ██╗███╗   ██╗████████╗██████╗ ███████╗██╗     
██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝██║     
███████╗ ╚████╔╝ ██╔██╗ ██║   ██║   ██████╔╝█████╗  ██║     
╚════██║  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██╗██╔══╝  ██║     
███████║   ██║   ██║ ╚████║   ██║   ██║  ██║███████╗███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
"""

_start_rgb = (88, 101, 242)   
_end_rgb = (114, 137, 218)   

ascii = gradient_text_selective(_ascii_art, _start_rgb, _end_rgb, "neoarz", "Made by ")

ascii_plain = _ascii_art

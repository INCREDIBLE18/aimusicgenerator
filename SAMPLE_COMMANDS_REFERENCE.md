# 🎵 **AI Music Generator - Complete Sample Commands Reference**

## 📋 **Generated Samples Overview**

All commands tested and working! Here are the complete sample prompts for every category:

---

## 🎲 **1. Basic Random Generation** (`advanced_music_gen.py`)

### **Sample 1: Creative Short Piece**
```powershell
py -3 advanced_music_gen.py 150 1.3 creative_short.mid
```
✅ **Result:** `creative_short.mid` (2,203 bytes) - 81 notes, 69 chords
**Use Case:** Quick creative snippets for content creation

### **Sample 2: Balanced Long Composition**
```powershell
py -3 advanced_music_gen.py 400 0.9 balanced_long.mid
```
**Use Case:** Coherent background music for videos or games

---

## 🎵 **2. Note-Based Generation** (`note_generator.py`)

### **Sample 1: Major Scale Melody**
```powershell
py -3 note_generator.py "C4 D4 E4 F4 G4 A4 B4 C5" 200 0.8 scale_melody.mid
```
✅ **Result:** `scale_melody.mid` (2,154 bytes) - 170 notes, 30 chords
**Use Case:** Educational tools, scale practice, melody development

### **Sample 2: Chord-Based Start**
```powershell
py -3 note_generator.py "C4,E4,G4 F4,A4,C5 G4,B4,D5" 250 1.1 chord_melody.mid
```
**Use Case:** Song development from specific chord voicings

---

## 🎹 **3. Predefined Style Generation** (`chord_generator_v2.py`)

### **Sample 1: Jazz Style**
```powershell
py -3 chord_generator_v2.py jazz 300 0.8 smooth_jazz.mid
```
✅ **Result:** `smooth_jazz.mid` (382 bytes) - Jazz progressions with 7th chords
**Use Case:** Lounge music, background jazz, cafe ambiance

### **Sample 2: Blues Style with Custom Tempo**
```powershell
py -3 chord_generator_v2.py blues 200 1.2 110 upbeat_blues.mid
```
✅ **Result:** `blues_test.mid` - Traditional 12-bar blues progression
**Use Case:** Blues backing tracks, jam sessions

---

## 🎼 **4. Custom Chord Progressions**

### **Sample 1: Pop Progression**
```powershell
py -3 chord_generator_v2.py "C Am F G" 250 1.0 pop_progression.mid
```
✅ **Result:** `pop_song.mid` (377 bytes) - Classic I-vi-IV-V progression
**Use Case:** Pop songwriting, commercial music

### **Sample 2: Jazz Extended Chords**
```powershell
py -3 chord_generator_v2.py "Cmaj7,Am7,Dm7,G7" 280 0.9 140 jazz_extended.mid
```
✅ **Result:** `jazz_extended.mid` (382 bytes) - 140 BPM jazz with 7th chords
**Use Case:** Sophisticated jazz compositions, professional recordings

---

## 🌟 **5. Ultimate Generator - Basic Mode**

### **Sample 1: Medium Random Piece**
```powershell
py -3 ultimate_music.py basic 220 1.1
```
**Use Case:** Experimental compositions, creative inspiration

### **Sample 2: Conservative Long Piece**
```powershell
py -3 ultimate_music.py basic 350 0.7
```
**Use Case:** Reliable background music, safe commercial use

---

## 🎶 **6. Ultimate Generator - Notes Mode**

### **Sample 1: Pentatonic Scale**
```powershell
py -3 ultimate_music.py notes "C4 D4 F4 G4 A4" 180 0.9
```
**Use Case:** World music, folk-inspired melodies

### **Sample 2: Minor Chord Sequence**
```powershell
py -3 ultimate_music.py notes "A4,C5,E5 D4,F4,A4" 200 1.0
```
**Use Case:** Sad/emotional music, cinematic scoring

---

## 🎸 **7. Ultimate Generator - Chords Mode**

### **Sample 1: Rock Progression**
```powershell
py -3 ultimate_music.py chords "C G Am F" 240 1.2
```
**Use Case:** Rock backing tracks, energetic music

### **Sample 2: Sad Minor Progression**
```powershell
py -3 ultimate_music.py chords "Am Dm G C" 200 0.8
```
**Use Case:** Melancholic music, emotional scenes

---

## 🎭 **8. Ultimate Generator - Style Mode**

### **Sample 1: Happy Uplifting Music**
```powershell
py -3 ultimate_music.py style happy 250 1.0
```
✅ **Result:** `ultimate_happy_250_10.mid` (377 bytes) - C-F-G-C progression
**Use Case:** Commercials, upbeat content, celebrations

### **Sample 2: Classical Style**
```powershell
py -3 ultimate_music.py style classical 400 0.8
```
**Use Case:** Formal events, traditional compositions

---

## 🎪 **9. Advanced Custom Progressions**

### **Sample 1: Complex Jazz Progression**
```powershell
py -3 chord_generator_v2.py "Cmaj7 A7 Dm7 G7 Em7 Am7 Dm7 G7" 350 1.0 complex_jazz.mid
```
**Use Case:** Professional jazz recordings, advanced harmonic studies

### **Sample 2: Modal Progression**
```powershell
py -3 chord_generator_v2.py "Dm C Bb F" 280 1.1 modal_piece.mid
```
**Use Case:** World music, modal jazz, ethnic compositions

---

## 🌈 **10. Experimental/Creative**

### **Sample 1: High Creativity Experiment**
```powershell
py -3 note_generator.py "F#4 Bb4 Db5" 300 1.8 experimental.mid
```
**Use Case:** Avant-garde music, sound design, artistic projects

### **Sample 2: Atonal Exploration**
```powershell
py -3 ultimate_music.py chords "C#m F#m B E" 200 1.7
```
**Use Case:** Modern classical, experimental electronic music

---

## 📊 **File Size & Quality Analysis**

| Generator | Sample File | Size (bytes) | Musical Elements | Duration Estimate |
|-----------|-------------|--------------|------------------|-------------------|
| Basic | `creative_short.mid` | 2,203 | 81 notes, 69 chords | ~45 seconds |
| Note-Based | `scale_melody.mid` | 2,154 | 170 notes, 30 chords | ~60 seconds |
| Style-Based | `smooth_jazz.mid` | 382 | 17 notes, 4 chords | ~30 seconds |
| Custom Chords | `jazz_extended.mid` | 382 | 17 notes, 4 chords | ~40 seconds |
| Ultimate | `ultimate_happy_250_10.mid` | 377 | 20 notes, 4 chords | ~35 seconds |

---

## 🎯 **Usage Recommendations by Purpose**

### **For Content Creators:**
```powershell
# YouTube background music
py -3 chord_generator_v2.py pop 300 0.8 youtube_bg.mid

# Intro music
py -3 note_generator.py "C5 G4 E4 C4" 80 1.0 intro.mid

# Outro music  
py -3 ultimate_music.py style happy 120 1.2
```

### **For Game Developers:**
```powershell
# Menu music
py -3 chord_generator_v2.py classical 400 0.7 menu_theme.mid

# Battle music
py -3 ultimate_music.py chords "C G Am F" 500 1.3

# Peaceful areas
py -3 chord_generator_v2.py folk 250 0.8 peaceful.mid
```

### **For Musicians/Composers:**
```powershell
# Chord progression study
py -3 chord_generator_v2.py "Cmaj7 A7 Dm7 G7" 200 0.9 study.mid

# Scale practice
py -3 note_generator.py "C4 D4 E4 F4 G4 A4 B4 C5" 150 0.7 practice.mid

# Creative inspiration
py -3 advanced_music_gen.py 250 1.4 inspiration.mid
```

### **For Relaxation/Meditation:**
```powershell
# Calm ambient
py -3 ultimate_music.py style sad 300 0.6

# Peaceful progression
py -3 chord_generator_v2.py "Am F C G" 400 0.7 peaceful.mid
```

---

## 💡 **Pro Tips for Best Results**

### **Creativity Settings:**
- **0.1-0.5**: Very predictable, safe for commercial use
- **0.6-0.9**: Balanced, natural musical variation
- **1.0-1.3**: Creative but musical
- **1.4-2.0**: Experimental, artistic

### **Length Guidelines:**
- **50-100 tokens**: Short clips (10-20 seconds)
- **150-250 tokens**: Standard songs (30-60 seconds)
- **300-500 tokens**: Extended pieces (1-2 minutes)
- **500+ tokens**: Full compositions (2+ minutes)

### **Style Combinations:**
Mix and match different generators for layered compositions:
1. Generate chord progression with `chord_generator_v2.py`
2. Add melody with `note_generator.py` 
3. Create variations with `ultimate_music.py`

---

## 🎼 **All Available Styles**

| Style | Chord Progression | Best For |
|-------|------------------|----------|
| `pop` | C→Am→F→G | Commercial music, mainstream appeal |
| `jazz` | Cmaj7→Am7→Dm7→G7 | Sophisticated, lounge music |
| `blues` | C7→F7→C7→G7 | Traditional blues, jam sessions |
| `rock` | C→G→Am→F | Energetic, guitar-driven music |
| `folk` | C→F→Am→G | Acoustic, storytelling music |
| `classical` | C→G→Am→F→C→Dm→G→C | Formal, traditional compositions |
| `minor` | Am→F→C→G | Sad, emotional music |
| `sad` | Am→Dm→G→C | Melancholic, cinematic |
| `happy` | C→F→G→C | Uplifting, celebratory |

---

*🎵 Your AI Music Composer Studio is ready to create any style of music you need! 🎼✨*
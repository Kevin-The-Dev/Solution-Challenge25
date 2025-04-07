# Catalysts - AI-Powered Teacher Assistant

## Overview
**Catalysts** is an AI-powered teaching assistant developed for the **Solution Challenge 25** hackathon. It addresses the challenge of overburdened teachers by automating assignment grading and providing personalized feedback to students. Aligned with **UN SDG 4: Quality Education**, this solution reduces educator workload, enhances feedback quality, and promotes inclusive, equitable learning experiences—especially in under-resourced settings.

### Problem Statement
Teachers face significant challenges due to:
- Time-consuming manual grading and feedback processes.
- Large class sizes limiting individualized attention.
- High teacher-to-student ratios in under-resourced schools.
- Students missing personalized guidance critical for academic success.

### Our Solution
Catalysts is an AI-driven platform that:
- **Automates Grading**: Processes essays, STEM problems, and code with NLP/ML models.
- **Delivers Personalized Feedback**: Offers actionable insights (e.g., "Improve your conclusion → See examples").
- **Supports Offline Use**: Ensures accessibility in low-connectivity areas.

#### Unique Selling Points (USP)
- Integrates question paper generation, doubt-solving, and grading in one tool.
- Provides context-aware, real-time feedback—beyond basic automation tools.
- Combines AI efficiency with teacher oversight for accuracy and control.
- Seamlessly integrates with Learning Management Systems (LMS).

---

## Features
| Category              | Features                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| **Automated Assessment** | Instant grading for essays, STEM, and code. Rubric-based scoring. Plagiarism detection. |
| **Personalized Learning** | Tailored feedback with actionable steps. Skill gap analysis. Resource recommendations. |
| **Teacher Empowerment**  | Collaborative feedback editing. Classroom analytics dashboard. Batch processing tools. |
| **Accessibility & Inclusion** | Offline functionality. Multilingual support (10+ languages). Screen-reader compatibility. |
| **Scalable Impact**      | Open-source core. Bias detection in grading algorithms. |

---

## How It Works
- **For Teachers**: Cuts grading time by 70%, improving feedback quality.
- **For Students**: Offers 24/7 personalized learning support.
- **For Schools**: Reduces achievement gaps with data-driven insights.

---

## File Structure

```plaintext
Solution-Challenge25/
├── .vscode/                  # VS Code settings
│   └── settings.json
├── Img/                      # Image assets
│   ├── icons/               # Icon files
│   └── login.jpg            # Login page screenshot
├── Student DB/               # Student-facing HTML pages
│   ├── assessments.html
│   ├── challenges.html
│   ├── download.html
│   ├── lessons.html
│   ├── student_db.html
│   ├── subjects.html
│   ├── support.html
│   └── upload.html
├── Teacher DB/               # Teacher-facing HTML pages
│   ├── assets/              # Additional assets for teacher pages
│   ├── chatbot.html
│   ├── classes.html
│   ├── settings.html
│   ├── staff_room.html
│   ├── students.html
│   ├── support.html
│   └── teacher_db.html
├── chatbot/                  # Chatbot and AI components
│   └── all_codes-master/
│       ├── auto_grader/     # Auto-grading scripts
│       ├── qpm_bot/         # Question paper generation bot
│       └── student_chatbot/ # Student-facing chatbot
├── output/                   # Output files
│   └── kevin.exe            # Executable file (if applicable)
├── README.md                 # Project README
├── index.html                # Main entry point
├── script.js                 # JavaScript logic
└── styles.css                # CSS styling
```

---

## Tech Stack
| Component       | Technologies                                      |
|-----------------|--------------------------------------------------|
| **Frontend**    | HTML, CSS, JavaScript, Bootstrap, React, Streamlit (Demo UI) |
| **Backend**     | Python, Flask, Gemini API (NLP Grading & Feedback) |
| **Deployments** | Streamlit Sharing, Netlify                        |

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for JavaScript frontend)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Kevin-The-Dev/Solution-Challenge25.git
   cd Solution-Challenge25
   ```
2. Install dependencies (if applicable, e.g., for Python scripts):
    ```bash
   pip install -r requirements.txt
   ```
   (Note: Add a requirements.txt file if Python dependencies are used.)



### Running the AI Components
1. Navigate to the chatbot folder
 ```bash
   cd chatbot/all_codes-master
   ```
2. Run the auto-grader or chatbot scripts (e.g., with Python):
 ```bash
   python auto_grader/main.py
   ```

### Demo
- Live MVP: https://cataylyst.netlify.app/
- Demo Video: https://youtu.be/-dIS8nyI8fY
- GitHub Repository: https://github.com/Kevin-The-Dev/Solution-Challenge25

### Team
- Team Name: Catalysts
- Team Leader: Tarnija Malaviya
- Members: Kevin Patel, Kaustubh Upadhyay, Het Patel 

### Future Scope
- Enhance offline capabilities with local AI models.
- Add support for more languages and subjects.
- Integrate with popular LMS platforms like Moodle.


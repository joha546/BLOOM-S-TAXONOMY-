import Constants
import sys
import openai
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QGridLayout,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QTextEdit
)

openai.api_key = Constants.API_kEY

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('what-is-chat-gpt.png').scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        
        self.input_label = QLabel("Ask Your Question Here")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        self.answer_label = QLabel("Answer: ")
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.blooms_level_label = QLabel("Bloom's Taxonomy Level: ")
        self.blooms_level_field = QLabel("")  # To display Bloom's level
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
        """
        QPushButton{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px, 32px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
        }
        QPushButton:hover{
            background-color: #45a049;
        }
        """
        )
        
        
        self.popular_questions_group = QGroupBox("Popular Questions")
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = [
            "What is Machine Learning?",
            "What are the Popular Libraries?",
            "How do I become a Machine Learning Engineer?"
        ]
        self.question_button = []
        
        # Create a layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        
        # Add logo to the layout
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        
        # Add Input Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        layout.addLayout(input_layout)
        layout.addWidget(self.submit_button)
        
        # Add Answer Field
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)

        # Add Bloom's Taxonomy Level Field
        layout.addWidget(self.blooms_level_label)
        layout.addWidget(self.blooms_level_field)

        # Add the popular question Button
        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
            """
            QPushButton{
                background-color: white;
                border: 2px solid;
                color: #00AEFF;
                padding: 10px, 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                }
                QPushButton:hover{
                    background-color:#00AEFF;
                }
            """
            )
            button.clicked.connect(lambda _, q=question: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_button.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout)
        layout.addWidget(self.popular_questions_group)
        
        # Set Layout
        self.setLayout(layout)
        self.setWindowTitle("ChatBot")
        
        # Set Window Properties
        self.setGeometry(200, 200, 600, 600)
        
        # Connect the submit button to the function which queries the OpenAI's API server
        self.submit_button.clicked.connect(self.get_answer)
        
    def get_answer(self):
        try:
            question = self.input_field.text()
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "You are a Machine Learning Engineering Expert. Answer the following questions in a concise way or with bullet points."},
                    {"role": "user", "content": f'{question}'}
                ],
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.7
            )
            answer = completion.choices[0].message.content
            self.answer_field.setText(answer)

            # Determine Bloom's Taxonomy level
            blooms_level = determine_blooms_level(question)
            self.blooms_level_field.setText(blooms_level)
        except Exception as e:
            print(f"Error in API call: {e}")

def determine_blooms_level(question):
    keywords = {
        "remember": ["define", "recall", "list", "identify","name", "recognize", "repeat", "state","select", "describe", "locate", "match"],
        "understand": ["explain", "interpret", "describe", "summarize","paraphrase", "illustrate", "compare", "contrast", "predict","outline", "clarify", "discuss", "estimate"],
        "apply": ["solve", "use", "demonstrate", "apply","implement", "solve","utilize", "execute", "employ", "compute", "practice", "relate", "schedule", "show", "sketch", "modify",],
        "analyze": ["analyze", "compare", "contrast", "diagram","break down", "examine", "investigate", "categorize", "differentiate", "deconstruct", "diagnose", "disciminate", "evaluate", "infer", "organize", "prioritize", "relate", "sepearate", "synthesize"],
        "evaluate": ["evaluate", "assess", "critique", "justify","judge", "appraise", "argue", "defend", "discriminate", "validate", "verify", "support"],
        "create": ["design", "create", "compose", "generate","develop", "formulate", "invent", "compose", "plan", "organize", "build", "devise", "combine", "rearrange", "adapt","assemble"]
    }

    for level, words in keywords.items():
        if any(keyword in question.lower() for keyword in words):
            return level.capitalize()

    return "Unknown"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
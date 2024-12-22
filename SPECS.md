### **Project: Intelligent and Interactive Revision Application**

This application will be **entirely local**, **customizable**, and **modular**, designed to meet your needs for certifications, technical interviews, and general knowledge enhancement. It will rely on a **clear JSON structure** for flashcards and recall data and generate course materials in **Markdown format**. The application will be **developed entirely in English**, with every detail explicitly addressed to ensure clarity and functionality.

---

### **Core Features**

#### **1. Deck Creation and Management**

- **Each deck will be stored in a unique JSON file.**
- Decks include:
    - Flashcards of various types (traditional, code, multi-MCQ, free input).
    - Statistics such as successes, failures, and last review dates.
- The user interface will display:
    - The total number of cards in the deck.
    - The number of cards due for revision now.
    - The number of cards to review later.

---

#### **2. Types of Flashcards**

1. **Traditional Flashcard**:
    
    - **Structure**:
        - A question in text format.
        - An answer in text format.
        - Associated tags for organization.
        - Explanatory feedback.
    - **JSON Example**:
        
        ```json
        {
          "id": "flashcard_001",
          "type": "traditional",
          "question": "What is Amazon S3?",
          "response": "A cloud object storage service.",
          "tags": ["AWS", "S3", "Definition"],
          "feedback": "Amazon S3 is used to store files.",
          "difficulty": "Medium",
          "date_created": "2024-12-20",
          "date_last_reviewed": "2024-12-19",
          "date_next_review": "2024-12-23",
          "statistics": {
            "successes": 5,
            "failures": 2
          },
          "multimedia": {
            "image": null,
            "audio": null,
            "video": null
          }
        }
        ```
        
2. **Code Flashcard**:
    
    - **Advanced Features**:
        - Support for multiple programming languages, including **Python**, **SQL (via DuckDB)**, and **Linux (bash/shell)**.
        - **Validation system**:
            - User-submitted code is validated against a reference code using `try-except` and `assert` methods.
        - A reference code determines whether the user’s input produces the correct output.
    - **JSON Example**:
        
        ```json
        {
          "id": "flashcard_002",
          "type": "code",
          "language": "Python",
          "question": "Write a code that returns 'Hello, World!' in Python.",
          "reference_code": "def hello(): return 'Hello, World!'\nassert hello() == 'Hello, World!'",
          "tags": ["Python", "Basics"],
          "feedback": "This is a correct way to write the code.",
          "difficulty": "Easy",
          "date_created": "2024-12-20",
          "date_last_reviewed": "2024-12-18",
          "date_next_review": "2024-12-22",
          "statistics": {
            "successes": 3,
            "failures": 1
          },
          "multimedia": {
            "image": null,
            "audio": null,
            "video": null
          }
        }
        ```
        
3. **Multi-MCQ (Multiple-choice with Blanks)**:
    
    - **Features**:
        - A text, image, or audio-based question containing blanks that the user must fill.
        - Up to **50 blanks maximum**.
        - Up to **8 choices per blank**.
        - Configuration to define the correct answers for each blank.
    - **JSON Example**:
        
        ```json
        {
          "id": "flashcard_003",
          "type": "multi-mcq",
          "question": "Complete the sentence: [AWS allows you to store __ and manage __.]",
          "choices": [
            ["files", "data", "code", "scripts"],
            ["databases", "infrastructure", "tools"]
          ],
          "correct_answers": [["files", "data"], ["databases"]],
          "tags": ["AWS", "Cloud"],
          "feedback": "AWS allows you to manage data and databases securely.",
          "difficulty": "Hard",
          "date_created": "2024-12-20",
          "date_last_reviewed": null,
          "date_next_review": null,
          "statistics": {
            "successes": 0,
            "failures": 0
          },
          "multimedia": {
            "image": "images/aws_mcq.png",
            "audio": null,
            "video": null
          }
        }
        ```
        
4. **Free Input Flashcard**:
    
    - **Features**:
        - The user can input one or more correct answers (up to **50 maximum**).
        - No predefined choices; the user writes their response directly.
    - **JSON Example**:
        
        ```json
        {
          "id": "flashcard_004",
          "type": "free-input",
          "question": "What are the main features of Amazon S3?",
          "responses": ["Object storage", "High availability", "Scalability"],
          "tags": ["AWS", "S3", "Features"],
          "feedback": "Amazon S3 provides scalable object storage with 99.999999999% availability.",
          "difficulty": "Medium",
          "date_created": "2024-12-20",
          "date_last_reviewed": null,
          "date_next_review": null,
          "statistics": {
            "successes": 0,
            "failures": 0
          },
          "multimedia": {
            "image": null,
            "audio": null,
            "video": null
          }
        }
        ```
        

---

#### **3. Tag Management**

- Flashcards are organized using **tags** and can include up to **five levels of hierarchical sub-tags**.
- **User Interface Features**:
    - Primary tags are displayed by default.
    - A clickable button expands all associated sub-tags.

---

#### **4. Automatic Course Generation**

- Flashcards are grouped **by tags** and exported as a **Markdown file**.
- The generated document is organized hierarchically:
    - Tags.
    - Sub-tags.
    - Sub-sub-tags.
- **Markdown Example**:
    
    ```markdown
    # Course: AWS S3
    
    ## Tag: AWS
    ### Sub-tag: S3
    #### Sub-sub-tag: Security
    
    **Question:** What is Amazon S3?  
    **Answer:** A cloud object storage service.  
    **Feedback:** Amazon S3 is used to store files.
    
    **Question:** What are the security levels in Amazon S3?  
    **Answer:** Access control, client-side encryption, server-side encryption.  
    **Feedback:** S3 supports various security options to meet enterprise needs.
    ```
    

---

### **Recall Storage**

- Recall information will be stored in a **separate JSON file** to avoid overloading the deck files.
- **JSON Example**:
    
    ```json
    {
      "recall_data": [
        {
          "flashcard_id": "flashcard_001",
          "deck_name": "AWS SAA",
          "date_last_reviewed": "2024-12-19",
          "date_next_review": "2024-12-23",
          "statistics": {
            "successes": 5,
            "failures": 2
          }
        }
      ]
    }
    ```
    

---

### **User Interface: Ergonomic and Modern**

1. **General Navigation**:
    
    - A **fixed sidebar menu** provides quick access to:
        - The list of decks.
        - Recall settings.
        - Course management.
2. **Deck View**:
    
    - **Displayed Information**:
        - Statistics such as:
            - Total cards.
            - Cards to review now.
            - Cards to review later.
        - Tags associated with the deck.
    - **Actions**:
        - A **collapsible section** for cards to review and revise now.
        - A **Play button** to sequentially review cards.
3. **Card Review**:
    
    - **Features**:
        - Display tags and sub-tags below each card.
        - Allow users to evaluate the difficulty of the question after responding:
            - Very Easy, Easy, Medium, Hard, Very Hard.
    - **Interface**:
        - Centralized layout for focus.
        - Smooth animations between cards.

---

### **Data Storage and Architecture**

1. **JSON for Decks**: A unique JSON file for each deck.
2. **JSON for Recalls**: A separate file to store recall information.
3. **Markdown for Courses**: Generated files based on tags for comprehensive revision material.



---

### **Important Development Guidelines**

#### **Language and Code Review Requirements**

1. **Language Consistency**
   - The entire project, including code, comments, documentation, and user interface, must be written in English.
   - Variable names, function names, and all other code identifiers must use English terminology.

2. **Code Development Process**
   - Before any code implementation:
     - Thoroughly review the entire SPECS.md file
     - Review all existing code in each directory
     - Avoid any redundancy with existing implementations
     - Only implement specifically requested features
   
3. **File Management**
   - Before creating any new file:
     - Verify that the file doesn't already exist
     - Check for similar files to avoid duplication
     - Ensure the new file follows the project's structure
   
4. **Code Modifications**
   - Do not modify or delete existing code unless explicitly requested
   - Do not create additional features or files beyond what is specifically requested
   - Maintain consistency with existing code structure and patterns

5. **Modularity Requirements**
   - **File Organization**:
     - Each feature and sub-feature must have its own dedicated files
     - Separate HTML files for each distinct functionality
     - Individual JavaScript files for each component's logic
     - Python modules should be feature-specific
   
   - **Component Structure**:
     - HTML: One file per distinct UI component or view
     - JavaScript: Dedicated modules for each feature's functionality
     - Python: Separate modules for each logical component
   
   - **Examples**:
     ```
     features/
     ├── flashcards/
     │   ├── creation/
     │   │   ├── creation.html
     │   │   ├── creation.js
     │   │   └── creation_handler.py
     │   ├── review/
     │   │   ├── review.html
     │   │   ├── review.js
     │   │   └── review_handler.py
     │   └── statistics/
     │       ├── stats.html
     │       ├── stats.js
     │       └── stats_handler.py
     ```

   - **Benefits**:
     - Enhanced maintainability
     - Easier debugging
     - Better code organization
     - Simplified feature updates
     - Improved code reusability

These guidelines must be followed throughout the entire development process to ensure code quality and project consistency.

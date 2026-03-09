# LuxScriptura: Catechism Interpretter & Corrector
Angelina Bojaj
3/09/2026
CSI 5310 Project

**Problem**: Within the Catholic Church and broader Christian discourse, many misunderstandings and misinterpretations arise regarding Catholic teachings. This problem has become more pronounced with the rise of online discussions, social media debates, and generative AI tools that may produce inaccurate theological explanations.

Many individuals—both Catholics and non-Catholics—seek explanations of Church doctrine but struggle to find answers that are both faithful to official teaching and accessible in plain language. While the Catechism of the Catholic Church contains authoritative explanations of doctrine, it is lengthy, structured in theological language, and not always easy for users to interpret or apply to specific questions. LuxScriptura is aimed at resolbing these issues alongside many more.

As a result, there is a need for a tool that can:
- Interpret passages of the Catechism
- Clarify theological meaning
- Detect and correct misinterpretations. For example, if the user states something this is incorrect / heretical, LuxScriptura will correct it by providing the right CCC or Bible Verse.
- Provide explanations grounded in official Church teaching.

**Proposed Method**: Implement using LLM API's alongside Modeling. Through NLP and various other methods taught in class, over time the model will develop to correct and inform the user of any possible misunderstandings their statements may promote. Additionally, to show the effectiveness of LuxScriptura, the correctness of the theology will be graded by percentage. This method is similar to how we code in class with the methods developed independently of provided code is tested for accuarcy and effectiveness. 

- NLP will specifically be used to question the understanding of a given prompt given by a user and interprets the theology surrounding it. While doing so, the text will be processed with parts of the Catechism being taken and then identifying potential similarties between the statement and what the Catechism teaches. 
- LLMs will be used to help explain Catechism passages provided and answer any doctrinal questions. At the same time, it will compare and contrast the users statements that may prose potential heresy's/incorrect statements against the Catholic Church.
- Catechism passages will be retrieved through various methods learned in class (also some by personal knownledge) such as RAG (Retrieval-Augmented Generation), Text Classification, & Vectors.
- Additional methods may be used to help better solve this problem.

**Current Resources / Libraries Planned To Use**:
The Catechism of The Catholic Church: https://github.com/nossbigg/catechism-ccc-json
OpenAI
Google Collab

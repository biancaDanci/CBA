from gensim.summarization import keywords

class KeywordsExtractor:
    def __init__(self, text):
        self.text = text
        self.keywords = []

    def compute(self):
        self.keywords = keywords(self.text, words=3).split('\n')
        return self.keywords

k =KeywordsExtractor("On the other hand, the Computer Science is undeniably the science of the present and, "
                  "beyond all questions, of the future as well. The number of students attending the courses "
                  "in this branch has rapidly increased and it is with absolute certainty that the graduates of Computer "
                  "Science study programs can compete fearlessly and deeply confidently on the international labour market of "
                  "Information Technology.12345678 DISCOVER THE FACULTY OF MATHEMATICS AND COMPUTER "
                  "SCIENCE IN 8 MINUTES! Mathematics and Computer Science "
                     "between Eternity and Effervescence The Faculty of Mathematics "
                  "and Computer Science is today a fortunate blend of tradition, experience and modernity in a large and prestigious "
                  "University.On one hand, all that was discovered in Mathematics along the centuries, even since the times of the ancient "
                  "Egyptians, Arabians and Greeks, all that Euclid, Pythagora Euler or Poincar stated as mathematical truth, remained as "
                  "such. None of these became obsolete; the subsequent discoveries did not revoke anything from Mathematics which kept on "
                  "developing unceasingly. Thus, the Faculty of Mathematics and Computer Science in Cluj-Napoca relies on and draws its vigour "
                  "from a whole school of famous names that starts with M. Hell, F. Riesz, L. Fejer, Gy. Farkas, D. Pompeiu, P. Sergescu, Gh."
                  " Bratu, T. Popoviciu and D.V. Ionescu, F. Rado, to mention only a few "
                  "important scientists and professors.On the other hand, the Computer Science is undeniably the science of the present "
                  "and, beyond all questions, of the future as well. The number of students attending the courses in this branch has rapidly"
                  " increased and it is with absolute certainty that the graduates of Computer Science study programs can compete fearlessly "
                  "and deeply confidently on the international labour market of Information Technology.At the same time, both Mathematics and "
                  "Computer Science from Babes-Bolyai University have at their disposal a wide range of dependable technical and managerial "
                  "facilities such as highly endowed laboratories, well equipped libraries, modern academic and research programmes, "
                  "profitable international cooperation.As a final and reliable argument, worthy reliability gained in time, there are "
                  "generations of graduates of Mathematics and Computer Science study programs, spread all over the country and in the whole "
                  "world, that work for prestigious schools, for strong IT companies, or in different fundamental and applied research fields "
                  "in universities or research institutes from Romania, Western Europe or United States.All these arguments, as well"
                  " as many others that we will leave you the pleasure to discover by yourselves, entitle us to invite you to a passionate "
                  "adventure into the wonderful, abstract world of Mathematics and the perpetually effervescent universe of Computer Science."
                  "On one hand, all that was discovered in Mathematics along the centuries, even since the times of the ancient Egyptians, "
                  "Arabians and Greeks, all that Euclid, Pythagora Euler  stated as mathematical truth, remained as such. None of "
                  "these became obsolete; the subsequent discoveries did not revoke anything from Mathematics which kept on developing "
                  "unceasingly. Thus, the Faculty of Mathematics and Computer Science in Cluj-Napoca relies on and draws its vigour from"
                  " a whole school of famous names that starts with M. Hell, F. Riesz, L. Fejer, Gy. Farkas, D. Pompeiu, P. Sergescu, Gh. "
                  "Bratu, Th.  and proceeds with G. , T. Popoviciu and D.V. Ionescu, F. Rado, to mention only a few"
                  " important scientists and professors.The Faculty of Mathematics and Computer Science is today a fortunate blend of"
                  " tradition, experience and modernity in a large and prestigious University. On the other hand, the Computer Science is "
                  "undeniably the science of the present and, beyond all questions, of the future as well. The number of students attending "
                  "the courses in this branch has rapidly increased and it is with absolute certainty that the graduates of Computer "
                  "Science study programs can compete fearlessly and deeply confidently on the international labour market of Information "
                  "Technology.").compute()
print(k)

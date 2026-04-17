import glob, os
import re
import io

class Normalizer:
    files_list = []
    status = False
    train_text=io.StringIO()
    train_words=[]

    def __init__ (self):
        pass

    def get_status(self):
        return self.status

    def load(self, folder_path):
        print(f"Searching path: {folder_path}")
        for file in glob.glob(f"{folder_path}/*.txt"):
            if file.endswith(".txt"):
                self.files_list.append(file)
                print(f"Found book: {file}")
        
        self.status = len(self.files_list)>0
        #print(f"Status: {self.status}")

    def strip_gutenberg(self, book_text):
        pattern=r"\s*\*\*\*.*?\*\*\*\s*(.*?)\s*\*\*\*.*?\*\*\*\s*"
        serach_res=re.search(pattern, book_text, re.DOTALL)
        return serach_res.group(1)

    def lowercase(self, text):
        return text.lower()

    def remove_punctuation(self, text):
        for char in "~!@#$^&*()-=_+?/.,';:\"[]\><`\|™“”‘’":
            text = text.replace(char, " ")
        # replace multiple spaces with one space
        text=re.sub(r"\s\s+", " ", text)
        return text

    def remove_numbers(self, text):
        for char in "0123456789":               
            text=text.replace(char, " ")
        return text

    def remove_whitespaces(self, text):
        text=re.sub(r"\s\s+", " ", text)
        text.strip()
        return text

    def word_tokenize(self):
        self.train_words = self.train_text.getvalue().split()
        print(f"Total num of words: {len(self.train_words)}")

    def normalize(self):
        os.remove(os.environ.get("TRAIN_TOKENS"))
        for book in self.files_list:
            print(f"Loading book: {book}")
            with open(book, encoding="utf8") as f:
                temp=f.read()
                book_text=self.strip_gutenberg(temp)
                book_text_lines = book_text.splitlines()
                print(f"Numlines {len(book_text_lines)}")

                for i, line in enumerate(book_text_lines):
                    # assume all chars are lower case
                    lineL=self.lowercase(line)
                    lineL=self.remove_punctuation(lineL)
                    lineL=self.remove_numbers(lineL)
                    lineL=self.remove_whitespaces(lineL)
                    book_text_lines[i] = lineL
                    if(book_text_lines[i]!=""):
                        self.train_text.write(" ")
                        self.train_text.write(book_text_lines[i])
                        
                    #final_text_buf.write(lineL)
                    #final_text_buf.write(' ')
                
                # save each processed file for debugging
                with open(f"{book}_.txtp", "w", encoding="utf8") as fw:
                    fw.write("\n".join(book_text_lines))

                # append                
                with open(os.environ.get("TRAIN_TOKENS"), "a", encoding="utf8") as fw:
                    for i, line in enumerate(book_text_lines):
                        if(line != ""):
                            fw.write(line)
                            fw.write("\n")
                    fw.write("\n")
        self.word_tokenize()

if __name__ == "__main__":
    pass
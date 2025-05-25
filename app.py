from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load popular book data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

# Home page
@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        ratings=list(popular_df['avg_ratings'].values)
    )

# Recommendation page
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in pt.index:
        return render_template('recommend.html', message="Sorry, the book you entered was not found in our database.")

    index = pt.index.get_loc(user_input)
    distances = similarity_score[index]
    book_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in book_list:
        book_title = pt.index[i[0]]
        temp_df = books[books['Book-Title'] == book_title]
        temp_df = temp_df.drop_duplicates('Book-Title')
        data.append([
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ])

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

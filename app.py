from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# enumerate를 Jinja2 템플릿에서 사용 가능하도록 등록
app.jinja_env.globals.update(enumerate=enumerate)

# 게시글 데이터를 저장할 리스트
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # 게시글 작성 데이터를 받아서 리스트에 추가
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 작성 시간 추가
        posts.append({'title': title, 'content': content, 'created_at': created_at})
        return redirect(url_for('index'))
    return render_template('post.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    # 특정 ID의 게시글 삭제
    if 0 <= post_id < len(posts):
        posts.pop(post_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 0 <= post_id < len(posts):
        if request.method == 'POST':
            # 수정된 게시글 데이터 반영
            posts[post_id]['title'] = request.form['title']
            posts[post_id]['content'] = request.form['content']
            return redirect(url_for('index'))
        return render_template('edit.html', post=posts[post_id], post_id=post_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint
from flask import flash
from flask import g
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from msucom_qbank.auth import login_required
from msucom_qbank.db import get_db

from loguru import logger
import random as rand

bp = Blueprint('quiz', __name__)


@bp.route('/question_return')
def question_return():
    question = request.args.get("question")
    q_id = request.args.get("id")
    t_no = request.args.get("t_no")
    body = session['body'][int(t_no)-1]
    return render_template('quiz/question_return.html', question_body=body[0], answer=body[1], mcq=body[2], test_no=t_no)


@bp.route('/', methods=['GET', 'POST'])
def index():
    user = ''
    if g.user:
        user = g.user['name']
    if request.method == 'POST':
        if "practice" in request.form:
            return redirect(url_for('quiz.quiz'))
        elif "add" in request.form:
            return redirect(url_for('quiz.add_question'))
    logger.debug(user)
    return render_template('quiz/index.html', user=user)


@bp.route('/exam', methods=['GET', 'POST'])
def exam():
    if 'exam' in session:
        return render_template('quiz/exam.html', qlist=session['exam'])


@bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    rows = list_quizzes()
    requested = []
    body = []
    if request.method == "POST":
        selected = request.get_json()
        for qz in selected:
            requested.extend(get_qID(qz[5]))
        rand.shuffle(requested)
        for count, value in enumerate(requested, start=1):
            value.insert(0, count)
        session['exam'] = requested
        for req in requested:
            body.append(get_question(req[2], req[1]))
        session['body'] = body
        return redirect(url_for('quiz.exam'))
    logger.debug(rows)
    return render_template('quiz/quiz.html', rows=rows)


@bp.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    if request.method == 'POST':
        title = request.form.get("qname")
        question = parse_input(request.form.get("question"))
        course = request.form.get("cname")
        make_table(title, course, question)


    return render_template('quiz/add_question.html')


# <-------------------DB stuff--------------------->


def get_question(q_id, question):
    cur = get_db().cursor()
    body = []
    answer = []
    cur.execute(
        "SELECT question, answer FROM question WHERE quiz_ID = ? and question =?",
        (q_id, question,),
    )
    tmp = cur.fetchone()
    body.append(tmp[0])
    body.append(tmp[1])
    cur.execute("SELECT mcq FROM mcq WHERE q_ID = ?", ((str(q_id)+question),),)
    tmp = cur.fetchall()
    for mcq in tmp:
        answer.append(mcq[0])
    rand.shuffle(answer)
    body.append(answer)
    return body

def get_qID(ql_id):
    cur = get_db().cursor()
    cur.execute("SELECT question, quiz_ID FROM question WHERE quiz_ID=?", (ql_id,),)
    tmp = []
    for win in cur.fetchall():
        tmp.append([win[0], win[1]])
    return tmp


def list_quizzes():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM quiz')
    return cur.fetchall()

def make_table(title, course, question):
    cur = get_db().cursor()
    rank = 0
    cur.execute(
        "INSERT INTO quiz (title, course, user, ranking) VALUES (?, ?, ?, ?)",
        (title, course, g.user['name'], rank),
    )
    q_id = cur.lastrowid
    for q in question:
        cur.execute(
            "INSERT INTO question (quiz_ID, question, answer, course) VALUES (?, ?, ?, ?)",
            (q_id, q[0], q[1][0], course),
        )

        q_ID = str(q_id)+q[0]
        for mcq in q[1][0:]:
            cur.execute(
                "INSERT INTO mcq (q_ID, mcq) VALUES (?, ?)",
                (q_ID, mcq),
            )

    no_q = len(cur.execute("SELECT * from question where quiz_ID=?", (q_id,)).fetchall())

    cur.execute(
        "UPDATE quiz SET no_questions=? WHERE quiz_ID=?", (no_q, q_id),
    )

    get_db().commit()
    return len(cur.fetchall())


def parse_input(u_input):
    qa_in = []
    qa_out = []
    q_ix = u_input.rstrip()
    qa_in = q_ix.split('!!')
    for qa in qa_in:
        q_split = qa.split('$')
        q_tmp = ''.join(q_split[0].splitlines())
        ma_tmp = q_split[1].split('|')
        qa_out.append((q_tmp, ma_tmp))
    return qa_out


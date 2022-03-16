#!/usr/bin/python3

# ~ Flask app "entry point"

import db
import config

from flask import (
	Flask,
	render_template,
	jsonify,
)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.htm', config=config)


@app.route('/summary/<int:ticker_num>/<int:seq_window>')
def summary_by_window(ticker_num, seq_window):
	"""
	Get ticker pts info based on "window":
	default amount of pts since the last detected one.
	"""
	window_finish = db.work_with_db(db.length, ticker_num)
	window_start = window_finish - seq_window + 1
	return jsonify(
		values=db.work_with_db(db.export, ticker_num, window_start, window_finish),
		start=window_start,
		finish=window_finish,
	);


@app.route('/summary/<int:ticker_num>/<int:start_seq>/<int:finish_seq>')
def summary_by_range(ticker_num, start_seq, finish_seq):
	"""
	Get ticker pts info based on "range":
	the start and finish of required pts sequence.
	"""
	# special case, to show the whole graph in real-time:
	if finish_seq == 0:
		finish_seq = db.work_with_db(db.length, ticker_num)
	return jsonify(
		values=db.work_with_db(db.export, ticker_num, start_seq, finish_seq),
	);


# Autorun in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000)

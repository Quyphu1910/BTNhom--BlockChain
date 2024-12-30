from flask import Flask, render_template, request, redirect, url_for, flash
from Blockchain import Blockchain, Transaction

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html',
                         chain=[block.toDict() for block in blockchain.chain],
                         pending_transactions=blockchain.pending_transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    student_id = request.form['student_id']
    course = request.form['course']
    score = float(request.form['score'])
    
    transaction = Transaction(student_id, course, score)
    blockchain.addTransaction(transaction)
    flash('Giao dịch đã được thêm vào danh sách chờ', 'success')
    return redirect(url_for('index'))

@app.route('/mine_block')
def mine_block():
    if blockchain.pending_transactions:
        blockchain.minePendingTransactions()
        flash('Block mới đã được tạo thành công!', 'success')
    else:
        flash('Không có giao dịch nào để tạo block mới', 'warning')
    return redirect(url_for('index'))

@app.route('/validate_chain')
def validate_chain():
    if blockchain.isChainValid():
        flash('Blockchain hợp lệ!', 'success')
    else:
        flash('Blockchain không hợp lệ!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
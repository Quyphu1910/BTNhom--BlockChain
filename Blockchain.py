import hashlib
import time
import uuid
from datetime import datetime

# ============================
# LỚP GIAO DỊCH (Transaction)
# ============================

class Transaction:
    def __init__(self, student_id, course, score):
        # Mã giao dịch duy nhất
        self.transaction_id = str(uuid.uuid4())
        # Mã số sinh viên
        self.student_id = student_id
        # Môn học
        self.course = course
        # Điểm số
        self.score = score
        # Thời gian giao dịch
        self.timestamp = time.time()

    def toDict(self):
        return {
            "transaction_id": self.transaction_id,
            "student_id": self.student_id,
            "course": self.course,
            "score": self.score,
            "timestamp": self.timestamp
        }

    def __repr__(self):
        return f"Transaction(ID={self.transaction_id}, student_id={self.student_id}, course={self.course}, score={self.score}, timestamp={self.timestamp})"

# ============================
# LỚP KHỐI (Block)
# ============================

class Block:
    def __init__(self, index, transactions, previous_hash):
        # Chỉ số của khối
        self.index = index
        # Mã băm của khối trước
        self.previous_hash = previous_hash
        # Thời gian tạo khối
        self.timestamp = time.time()
        # Danh sách giao dịch trong khối
        self.transactions = transactions
        # Mã băm gốc Merkle cho giao dịch
        self.merkle_root = self.calculateMerkleRoot()
        # Số nonce (dùng để đào khối)
        self.nonce = 0
        # Mã băm của khối hiện tại
        self.hash = self.calculateHash()

    def calculateHash(self):
        # Tính toán mã băm cho khối dựa trên nội dung của nó
        block_data = (f"{self.index}"
                      f"{self.merkle_root}"
                      f"{self.timestamp}"
                      f"{self.previous_hash}"
                      f"{self.nonce}")
        return hashlib.sha256(block_data.encode()).hexdigest()

    def calculateMerkleRoot(self):
        # Tạo cây Merkle và tính gốc Merkle từ các giao dịch
        hashes = []
        for tx in self.transactions:
            # Chuyển giao dịch thành dictionary
            transaction_dict = tx.toDict()
            # Chuyển dictionary thành chuỗi
            transaction_string = str(transaction_dict)
            # Mã hóa chuỗi thành bytes
            transaction_bytes = transaction_string.encode()
            # Tính hash
            transaction_hash = hashlib.sha256(transaction_bytes).hexdigest()
            # Thêm hash vào danh sách
            hashes.append(transaction_hash)

        while len(hashes) > 1:
            # Nếu số lượng lẻ, sao chép hash cuối
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            # Ghép đôi và tạo mã băm mới
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            hashes = new_level
        # Nếu không có giao dịch, trả về "0"
        return hashes[0] if hashes else "0"

    def mineBlock(self, difficulty):
        # Đào khối với độ khó xác định
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculateHash()

    def toDict(self):
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "transactions": [tx.toDict() for tx in self.transactions]
        }

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash}, merkle_root={self.merkle_root}, transactions={self.transactions}, timestamp={self.timestamp})"

# ============================
# LỚP CHUỖI KHỐI (Blockchain)
# ============================

class Blockchain:
    def __init__(self):
        # Khởi tạo chuỗi khối với khối khởi nguyên
        self.chain = [self.createGenesisBlock()]
        # Danh sách giao dịch đang chờ
        self.pending_transactions = []
        # Độ khó đào khối
        self.difficulty = 3

    def createGenesisBlock(self):
        # Tạo khối gốc
        return Block(0, [], "0")

    def getLatestBlock(self):
        return self.chain[-1]

    def addTransaction(self, transaction):
        # Thêm giao dịch mới vào danh sách chờ
        self.pending_transactions.append(transaction)

    def minePendingTransactions(self):
        # Tạo khối mới từ danh sách giao dịch chờ xử lý
        if not self.pending_transactions:
            print("Không có giao dịch chờ xử lý.")
            return

        latest_block = self.getLatestBlock()
        new_block = Block(len(self.chain), self.pending_transactions, latest_block.hash)
        new_block.mineBlock(self.difficulty)

        self.chain.append(new_block)
        # Xóa danh sách giao dịch chờ xử lý
        self.pending_transactions = []

        print(f"Block {new_block.index} đã được thêm vào Blockchain!")

    def isChainValid(self):
        # Kiểm tra tính toàn vẹn của chuỗi khối
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Kiểm tra mã băm của khối hiện tại
            if current_block.hash != current_block.calculateHash():
                print(f"Block {current_block.index} đã bị sửa đổi!")
                return False

            # Kiểm tra liên kết với khối trước
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} không khớp với khối trước!")
                return False

        print("Blockchain hợp lệ.")
        return True

    def displayChain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f" - Hash: {block.hash}")
            print(f" - Merkle Root: {block.merkle_root}")
            print(f" - Previous Hash: {block.previous_hash}")
            print(f" - Nonce: {block.nonce}")
            print(f" - Date time: {datetime.fromtimestamp(block.timestamp)}")
            print(f" - Transactions:")
            for tx in block.transactions:
                print(f"    {tx}")
            print("-" * 50)


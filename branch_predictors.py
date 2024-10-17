# Branch Predictor Implementations

# Static Predictor
class StaticPredictor:
    def __init__(self, always_taken=True):
        self.always_taken = always_taken

    def predict(self, address):
        return 1 if self.always_taken else 0

    def update(self, address, actual_outcome):
        # No updates needed for static predictor
        pass


# One-Bit Branch Predictor
class OneBitBranchPredictor:
    def __init__(self):
        self.bht = {}

    def predict(self, address):
        if address not in self.bht:
            self.bht[address] = 1  # Default to taken
        return self.bht[address]

    def update(self, address, actual_outcome):
        self.bht[address] = actual_outcome


# Two-Bit Branch Predictor
class TwoBitBranchPredictor:
    def __init__(self):
        self.bht = {}

    def predict(self, address):
        if address not in self.bht:
            self.bht[address] = 3  # Initialize to strongly taken (11)
        counter = self.bht[address]
        return 1 if counter >= 2 else 0

    def update(self, address, actual_outcome):
        counter = self.bht[address]
        if actual_outcome == 1:
            if counter < 3:
                self.bht[address] += 1
        else:
            if counter > 0:
                self.bht[address] -= 1


# Bimodal Branch Predictor
class BimodalBranchPredictor:
    def __init__(self, table_size=1024):
        self.bht = [3] * table_size  # 2-bit counters initialized to strongly taken (11)
        self.table_size = table_size

    def predict(self, address):
        index = address % self.table_size
        counter = self.bht[index]
        return 1 if counter >= 2 else 0

    def update(self, address, actual_outcome):
        index = address % self.table_size
        counter = self.bht[index]
        if actual_outcome == 1:
            if counter < 3:
                self.bht[index] += 1
        else:
            if counter > 0:
                self.bht[index] -= 1


# GShare Branch Predictor
class GShareBranchPredictor:
    def __init__(self, history_bits=10):
        self.global_history = 0
        self.history_bits = history_bits
        self.bht = [3] * (2 ** history_bits)  # 2-bit counters

    def predict(self, address):
        index = (address ^ self.global_history) % len(self.bht)
        counter = self.bht[index]
        return 1 if counter >= 2 else 0

    def update(self, address, actual_outcome):
        index = (address ^ self.global_history) % len(self.bht)
        counter = self.bht[index]
        if actual_outcome == 1:
            if counter < 3:
                self.bht[index] += 1
        else:
            if counter > 0:
                self.bht[index] -= 1
        self.global_history = ((self.global_history << 1) | actual_outcome) % (2 ** self.history_bits)


# Hybrid Branch Predictor
class HybridBranchPredictor:
    def __init__(self, history_bits=10, table_size=1024):
        self.gshare = GShareBranchPredictor(history_bits)
        self.bimodal = BimodalBranchPredictor(table_size)
        self.choice_table = [1] * table_size  # Choice predictor (1-bit)
        self.table_size = table_size

    def predict(self, address):
        index = address % self.table_size
        if self.choice_table[index] == 0:
            return self.bimodal.predict(address)
        else:
            return self.gshare.predict(address)

    def update(self, address, actual_outcome):
        index = address % self.table_size
        bimodal_prediction = self.bimodal.predict(address)
        gshare_prediction = self.gshare.predict(address)

        # Update the predictor used for the prediction
        if self.choice_table[index] == 0:
            self.bimodal.update(address, actual_outcome)
        else:
            self.gshare.update(address, actual_outcome)

        # Update the choice table based on which predictor was correct
        if bimodal_prediction == actual_outcome and gshare_prediction != actual_outcome:
            self.choice_table[index] = 0
        elif gshare_prediction == actual_outcome and bimodal_prediction != actual_outcome:
            self.choice_table[index] = 1


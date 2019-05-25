from keras.optimizers import *
from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence  import pad_sequences
from semeval_financial_news.Dataset import Dataset


class Model():

    def __init__(self):
        self.vocabulary_size = 10_000
        self.embedding_size = 128
        self.max_len = 25

        model = Sequential()
        model.add(Embedding(self.vocabulary_size, self.embedding_size, input_length=self.max_len))
        model.add(LSTM(512, return_sequences=True, dropout=0.3))
        model.add(LSTM(512, dropout=0.3))
        model.add(Dense(1, activation='sigmoid'))

        self.model = model

    def train(self, X_train, Y_train, X_test, Y_test, batch_size=32, epochs=10):
        t = Tokenizer(num_words=self.vocabulary_size)
        t.fit_on_texts(X_train)
        encoded_train_titles = t.texts_to_sequences(X_train)
        encoded_test_titles = t.texts_to_sequences(X_test)

        X_train = encoded_train_titles
        X_test = encoded_test_titles

        X_train = pad_sequences(X_train, maxlen=self.max_len, value=0)
        X_test = pad_sequences(X_test, maxlen=self.max_len, value=0)

        optimizer = Adam()
        self.model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=batch_size, epochs=epochs)
        self.model.save('./checkpoints/model')

        scores = self.model.evaluate(X_test, Y_test, verbose=0)
        print('Test accuracy:', scores[1])

    def load_model(self, path):
        self.model.load(path)


if __name__ == '__main__':
    dataset = Dataset('./data/headlines_train.json')
    model = Model()
    X_train, Y_train, X_test, Y_test = dataset.train_test_split()
    model.train(X_train, Y_train, X_test, Y_test)
import streamlit as st


def load_vocab(file_path):
    with open(file_path, 'r') as file:
        words = file.read()
    vocab = words.split('\n')
    return vocab


def calc_levenshteindistance(token_1, token_2):
    distance = [[0] * (len(token_2) + 1) for _ in range(len(token_1) + 1)]

    for i in range(len(token_1) + 1):
        distance[i][0] = i

    for j in range(len(token_2) + 1):
        distance[0][j] = j

    for i in range(1, len(token_1) + 1):
        for j in range(1, len(token_2) + 1):
            if token_1[i - 1] == token_2[j - 1]:
                distance[i][j] = distance[i - 1][j - 1]
            else:
                distance[i][j] = 1 + min(distance[i - 1][j],
                                         distance[i][j - 1],
                                         distance[i - 1][j - 1])
    return distance[-1][-1]


def main():
    st.title("Word Correction using Levenshtein Distance")
    text = st.text_input("Type your text here")
    file_path = 'Source/vocab.txt'  # file path of Vocabulary
    result = ''
    distance = []
    if st.button('check'):
        vocab = load_vocab(file_path)
        words = text.split(' ')
        dict_dis = {}
        for word in words:
            distance.clear()
            for vocabulary in vocab:
                distance.append(calc_levenshteindistance(word, vocabulary))
            index = distance.index(min(distance))
            result += vocab[index]
            result += ' '
        st.text(f'Did you mean: {result}')
        for i in range(len(distance)):
            dict_dis[vocab[i]] = distance[i]
        sorted_dict = dict(sorted(dict_dis.items(), key=lambda item: item[1]))
        col1, col2 = st.columns(2)
        with col1:
            st.text("Vocabulary:")
            st.text(vocab)
        with col2:
            st.text("Distance:")
            st.write(sorted_dict)


if __name__ == "__main__":
    main()

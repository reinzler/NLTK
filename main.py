import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pymorphy2
import imageio
from pyrogram import Client
import datetime
import snoop
import time
import taichi as ti
# api_id = 25252235
# api_hash = '74e99fe6d08155ecd9b1a120775e48a2'
# app = Client("my_account", api_id=api_id, api_hash=api_hash)
# # list_of_channels = ["RKadyrov_95","margaritasimonyan","dmitri_kiselev","SolovievLive", "skabeeva"]
list_of_channels = ["skabeeva"]
# # for i in range(len(list_of_channels)):
# #     file_before = open(f"{list_of_channels[i]}_before_24.02.2022.txt", "wb")
# #     file_after = open(f"{list_of_channels[i]}_after_24.02.2022.txt", "wb")
# #     end = datetime.datetime(2022, 2, 24)
# #     async def main():
# #         async with app:
# #             async for message in app.get_chat_history(list_of_channels[i]): #offset_date = end): #reverse = True,):
# #                 if message.text != None and message.date < end:  # Условие не будет выполнено, если message.text = None
# #                     file_before.write(message.text.encode("utf-16"))
# #                 elif message.text != None and message.date >= end:  # Условие не будет выполнено, если message.text = None
# #                     file_after.write(message.text.encode("utf-16"))
# #         file_before.close(),  file_after.close()
# #     app.run(main())
#
# ### Анализ текста, приводим к нулевой форме
start_time = time.time()
for i in range(len(list_of_channels)):
    file_before = open(f"{list_of_channels[i]}_before_24.02.2022.txt", "r", encoding="utf-16")
    file_after = open(f"{list_of_channels[i]}_after_24.02.2022.txt", "r", encoding="utf-16")
    file_frequency_before = open(f"{list_of_channels[i]}_frequency_words_before_24.02.2022.txt", "w", errors='replace')
    file_frequency_after = open(f"{list_of_channels[i]}_frequency_words_after_24.02.2022.txt", "w", errors='replace')
    text_before = file_before.read()
    text_after = file_after.read()
    @snoop
    def text_analys(text_before, text_after):
        text_before = text_before.lower()
        text_after = text_after.lower()
        spec_chars = string.punctuation + '\n\xa0«»\t—…' + u'\ufeff'
        def remove_chars_from_text(text,chars):
            for i in text:
                for k in chars:
                    if i == k:
                        text = text.replace(i, "")
            return text

        text_before = remove_chars_from_text(text_before, spec_chars)
        text_before = remove_chars_from_text(text_before, string.digits)
        text_after = remove_chars_from_text(text_after, spec_chars)
        text_after = remove_chars_from_text(text_after, string.digits)
        russian_stopwords = stopwords.words("russian")
        russian_stopwords.extend(["не","на", "-", "–", "это", "наш","который","такой","самый","мы","свой"])
        text_before_tokens = word_tokenize(text_before)
        text_after_tokens = word_tokenize(text_after)
        text_before_tokens = [token.strip(' ') for token in text_before_tokens if token not in russian_stopwords]
        text_after_tokens = [token.strip(' ') for token in text_after_tokens if token not in russian_stopwords]
        morphem = pymorphy2.MorphAnalyzer()

        @snoop
        def zero_morph(text):
            a = str()
            text = nltk.Text(text)
            for i in text:
                i = morphem.parse(i)[0].normal_form
                a += i + " "
            return a
        text_before = zero_morph(text_before)
        text_after = zero_morph(text_after)

        ### Следующие две строчки собирают обратно слова из токенов
        text_before = nltk.Text(text_before_tokens)
        text_after = nltk.Text(text_after_tokens)
        ### Вывод графика с самыми часто встречающимися словами
        fdist_before = FreqDist(text_before)
        fdist_after = FreqDist(text_after)
        # print(fdist_before.plot(30,cumulative=False))

        for j in fdist_before.most_common(30):
            line_before = ' '.join(str(x) for x in j)
            file_frequency_before.write(line_before + '\n')
        for j in fdist_after.most_common(30):
            line_after = ' '.join(str(x) for x in j)
            file_frequency_after.write(line_after + '\n')

        ### Построение облака слов и запись его в файл
        text_before_raw = " ".join(text_before)
        text_after_raw = " ".join(text_after)
        ### Маска для облака слов
        mask = imageio.v2.imread(r'medvedev.jpg')
        ### Облако слов "до"
        wordcloud = WordCloud(width=2000,
                              height=1500,
                              random_state=1,
                              background_color='white',
                              colormap='Set2',
                              collocations=False,
                              mask=mask).generate(text_before_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        # print(i)
        # name = list_of_channels[i] + "_frequency_words_before_24.02.2022.png"
        plt.savefig(f"{list_of_channels[i]}_frequency_words_before_24.02.2022.png")
        # plt.show()
        plt.close()

        ### Облако слов "после"

        wordcloud = WordCloud(width=2000,
                              height=1500,
                              random_state=1,
                              background_color='white',
                              colormap='Set2',
                              collocations=False,
                              mask=mask).generate(text_after_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")


        # name = list_of_channels[i] + "_frequency_words_after_24.02.2022.png"
        plt.savefig(f"{list_of_channels[i]}_frequency_words_after_24.02.2022.png")
        # plt.show()
        plt.close()

    text_analys(text_before, text_after)
    print("--- %s seconds ---" % (time.time() - start_time))

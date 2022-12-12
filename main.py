import string
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize
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
import os
from deep_translator import GoogleTranslator
morph = pymorphy2.MorphAnalyzer()
mask = imageio.v2.imread(r'medvedev.jpg')

with open("api.txt", "r") as file:
    api_id = int(float(file.readline()))
    api_hash = file.readline()
    print(api_id, api_hash)
app = Client("my_account", api_id=api_id, api_hash=api_hash)
list_of_channels = ["RKadyrov_95","margaritasimonyan","dmitri_kiselev","SolovievLive", "skabeeva"]
for i in range(len(list_of_channels)):
    file_before = open(f"./output/{list_of_channels[i]}_before_24.02.2022.txt", "wb")
    file_after = open(f"./output/{list_of_channels[i]}_after_24.02.2022.txt", "wb")
    end = datetime.datetime(2022, 2, 24)
    async def main():
        async with app:
            async for message in app.get_chat_history(list_of_channels[i]):
            #offset_date = end):  #reverse = True,):
                if message.text != None and message.date < end:  # Условие не будет выполнено, если message.text = None
                    file_before.write(message.text.encode("utf-16"))
                elif message.text != None and message.date >= end:  # Условие не будет выполнено, если message.text = None
                    file_after.write(message.text.encode("utf-16"))
        file_before.close(),  file_after.close()
    app.run(main())

# # ### Анализ текста, приводим к нулевой форме
channels_history_list = []
for root, dirs, files in os.walk("./output/"):
    for name in files:
        if "frequency" not in name and name.endswith(".txt"):
            channels_history_list.append(name)
start_time = time.time()
print(len(channels_history_list))
for i in range(len(channels_history_list)):
    file = open(f"./output/{channels_history_list[i]}", "r", encoding="utf-16")
    text = file.read().lower()
    russian_stopwords = stopwords.words("russian")
    additional_stopwords = {"не", "на", "это", "наш", "который", "такой", "самый", "мы", "свой","https", "t", "me"}
    russian_stopwords = set(stopwords.words("russian"))
    @snoop
    def zero_morph(text):
        words = wordpunct_tokenize(text)
        preprocess_words = [word for word in words if word.isalpha() == True]
        without_stop_words = [word for word in preprocess_words if not word in russian_stopwords]
        output = [morph.parse(word)[0].normal_form for word in without_stop_words if not morph.parse(word)[
            0].normal_form in additional_stopwords]
        return ' '.join(output)

    text = zero_morph(text)
    text = wordpunct_tokenize(text)

    if "before" in channels_history_list[i]:
        fdist = FreqDist(text)
        print(fdist.most_common(30))
        with open(f"./output/{channels_history_list[i][:-4]}_frequency_words.txt", "w", \
                encoding="utf-16") as file:
            for j in fdist.most_common(30):
                line = ' '.join(str(x) for x in j)
                file.write(line + '\n')

        ### Построение облака слов и запись его в файл
        text_raw = " ".join(text)
        ### Маска для облака слов
        mask = imageio.v2.imread(r'medvedev.jpg')
        ### Облако слов "до"
        wordcloud = WordCloud(width=2000,
                              height=1500,
                              random_state=1,
                              background_color='white',
                              colormap='Set2',
                              collocations=False,
                              mask=mask).generate(text_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(f"./output/{channels_history_list[i][:-4]}_frequency_words.png")
        plt.close()
    else:
        fdist = FreqDist(text)
        print(fdist.most_common(30))
        with open(f"./output/{channels_history_list[i][:-4]}_frequency_words.txt", "w", encoding="utf-16") as \
                file:
            for j in fdist.most_common(30):
                line = ' '.join(str(x) for x in j)
                file.write(line + '\n')
        ### Построение облака слов и запись его в файл
        text_raw = " ".join(text)
        ### Маска для облака слов
        mask = imageio.v2.imread(r'medvedev.jpg')
        ### Облако слов "до"
        wordcloud = WordCloud(width=2000,
                              height=1500,
                              random_state=1,
                              background_color='white',
                              colormap='Set2',
                              collocations=False,
                              mask=mask).generate(text_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(f"./output/{channels_history_list[i][:-4]}_frequency_words.png")
        plt.close()
    print("--- %s seconds ---" % (time.time() - start_time))
def translate():
    channels_to_be_translated_list = []
    for root, dirs, files in os.walk("./output/"):
        for name in files:
            if "frequency" in name and name.endswith(".txt"):
                channels_to_be_translated_list.append(name)
    for i in range(len(channels_to_be_translated_list)):
        if "before" in channels_to_be_translated_list[i]:
            with open(f"./output/{channels_to_be_translated_list[i]}", encoding="utf-16") as f:
                before = f.read()
                wordcloud = WordCloud(width=2000,
                                      height=1500,
                                      random_state=1,
                                      background_color='white',
                                      colormap='Set2',
                                      collocations=False,
                                      mask=mask).generate(GoogleTranslator('auto', 'en').translate(before))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.savefig(f"./output/{channels_to_be_translated_list[i]}_en.png".replace(".txt",""))
                plt.close()

        else:
            with open(f"./output/{channels_to_be_translated_list[i]}", encoding="UTF-16") as f:
                after = f.read()
                print(after)
                wordcloud = WordCloud(width=2000,
                                      height=1500,
                                      random_state=1,
                                      background_color='white',
                                      colormap='Set2',
                                      collocations=False,
                                      mask=mask).generate(GoogleTranslator('auto', 'en').translate(after))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.savefig(f"./output/{channels_to_be_translated_list[i]}_en.png".replace(".txt",""))
                plt.close()

translate()






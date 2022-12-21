import string
from nltk import tokenize
from nltk.tokenize import word_tokenize, wordpunct_tokenize, MWETokenizer
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
from tqdm import tqdm

# keyword_processor = KeywordProcessor()
morph = pymorphy2.MorphAnalyzer()
mask = imageio.v2.imread(r'medvedev.jpg')

@snoop
def parse_channel_history():
    with open("api.txt", "r") as file:
        api_id = int(float(file.readline()))
        api_hash = file.readline()

    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    # list_of_channels = ["RKadyrov_95","margaritasimonyan","dmitri_kiselev","SolovievLive", "skabeeva"]
    #list_of_channels = ["margaritasimonyan"]
    # for i in range(len(list_of_channels)):
    #     file_before = open(f"./output/{list_of_channels[i]}_before_24.02.2022.txt", "wb")
    #     file_after = open(f"./output/{list_of_channels[i]}_after_24.02.2022.txt", "wb")
    #     end = datetime.datetime(2022, 2, 24)
    #     async def main():
    #         async with app:
    #             async for message in app.get_chat_history(list_of_channels[i]):
    #             #offset_date = end):  #reverse = True,):
    #                 if message.text != None and message.date < end:  # Условие не будет выполнено, если message.text = None
    #                     file_before.write(message.text.encode("utf-16"))
    #                 elif message.text != None and message.date >= end:  # Условие не будет выполнено, если message.text = None
    #                     file_after.write(message.text.encode("utf-16"))
    #         file_before.close(),  file_after.close()

    # for i in range(len(list_of_channels)):
    #     # file_before = open(f"./output/{list_of_channels[i]}_newspeak_before_24.02.2022.txt", "w", encode='UTF-8')
    #     file_after = open(f"./output/{list_of_channels[i]}_newspeak_after_24.02.2022.txt", "wb")
    #     end = datetime.date(2022, 2, 24)
    #     date_list = [datetime.date(2022, 4, 25), datetime.date(2022, 4, 28), datetime.date(2022, 6, 2),
    #                  datetime.date(2022, 7, 27), datetime.date(2022, 8, 3), datetime.date(2022, 9, 2),
    #                  datetime.date(2022, 9, 9), datetime.date(2022, 11, 25), datetime.date(2022, 11, 28),
    #                  datetime.date(2022, 12, 3), datetime.date(2022, 12, 9), datetime.date(2022, 12, 12),
    #                  datetime.date(2022, 11, 30)]
    #     async def main():
    #         async with app:
    #             async for message in app.get_chat_history(list_of_channels[i]):
    #                 # if message.text != None and message.date < end:  # Условие не будет выполнено, если message.text = None
    #                 #     file_before.write(message.text.encode("utf-8"))
    #                 print(datetime.datetime.date(message.date))
    #                 if message.text != None and datetime.datetime.date(message.date) > end and \
    #                         datetime.datetime.date(message.date) in date_list:  # Условие не
    #                     # будет выполнено, если message.text = None
    #                     file_after.write(message.text.encode("utf-8"))
    #                     # file_after.write(str(message.date).encode("utf-8"))
    #         #file_before.close(),
    #         file_after.close()
    #     app.run(main())


@snoop
def analysis():
    channels_history_list = []
    for root, dirs, files in os.walk("./output/"):
        for name in files:
            if "frequency" not in name and "newspeak" not in name and name.endswith(".txt"):
                channels_history_list.append(name)

    for channel in channels_history_list:
        with open(f"C:\\Users\\Vadik\\PycharmProjects\\NLTK\\output\\{channel}", 'r', encoding="utf-8") as channel_history:
            text = channel_history.read().lower()
        @snoop
        def count_newspeak(text, channel):
            newspeak = {'хлопок', 'задымление', 'подтопление', 'ситуация', 'жесткая посадка', 'касание', 'сближение',
                        'беспорядки', 'экстремизм', 'фейк', 'неонацисты', 'фашисты', 'сатанисты', 'воссоединение',
                        'нам не оставили выбора', 'защита народа Донбасса', 'защита мирного населения', 'идет по плану',
                        'жест доброй воли', 'сщелкивание', 'освобождение', 'террористический акт', 'родная гавань'}
            tokenizer = tokenize.WordPunctTokenizer()
            text_words = tokenizer.tokenize(text)
            tokenizer = MWETokenizer(separator=' ')
            tokenizer.add_mwe(('защита', 'народа', 'донбасса'))
            tokenizer.add_mwe(('защита', 'мирного', 'населения'))
            tokenizer.add_mwe(('идет', 'по', 'плану'))
            tokenizer.add_mwe(('жест', 'доброй', 'воля'))
            tokenizer.add_mwe(('родная', 'гавань'))
            text_after_mwe = tokenizer.tokenize(text_words)
            counted_dict = {}
            global common_list
            common_list = []
            for words in tqdm(newspeak):
                if text_after_mwe.count(words) != 0:
                    counted_dict[words] = text.count(words)
            list_for_dict_and_channel = []
            list_for_dict_and_channel.append(channel.partition("_")[0])
            list_for_dict_and_channel.append(counted_dict)
            common_list.append(list_for_dict_and_channel)
            list_for_dict_and_channel = []
            return counted_dict, sum(counted_dict.values())

        newspeak_output = count_newspeak(text, channel)
        @snoop
        ### Анализ текста, приводим к нулевой форме
        def zero_morph(text):
            russian_stopwords = stopwords.words("russian")
            additional_stopwords = {"не", "на", "это", "наш", "который", "такой", "самый", "мы", "свой", "https", "t", "me"}
            russian_stopwords = set(stopwords.words("russian"))
            words = wordpunct_tokenize(text)
            preprocess_words = [word for word in tqdm(words) if word.isalpha() == True]
            without_stop_words = [word for word in tqdm(preprocess_words) if not word in russian_stopwords]
            output = [morph.parse(word)[0].normal_form for word in tqdm(without_stop_words) if not morph.parse(word)[
                0].normal_form in additional_stopwords]
            return ' '.join(output)

        # text = zero_morph(text)
        # text = wordpunct_tokenize(text)
        def print_and_plot(text,channel):
            if "before" in channel:
                # fdist = FreqDist(text)
                # with open(f"./output/{channel[:-4]}_frequency_words.txt", "w", \
                #         encoding="utf-16") as file:
                #     for j in fdist.most_common(30):
                #         line = ' '.join(str(x) for x in j)
                #         file.write(line + '\n')

                with open(f"./output/{channel[:-4]}_newspeak.txt", "w", \
                          encoding="utf-16") as file:
                    file.write(str(newspeak_output))

                # ### Построение облака слов и запись его в файл
                # text_raw = " ".join(text)
                # ### Маска для облака слов
                # mask = imageio.v2.imread(r'medvedev.jpg')
                # ### Облако слов "до"
                # if len(text_raw) != 0:
                #     wordcloud = WordCloud(width=2000,
                #                           height=1500,
                #                           random_state=1,
                #                           background_color='white',
                #                           colormap='Set2',
                #                           collocations=False,
                #                           mask=mask).generate(text_raw)
                #     plt.imshow(wordcloud, interpolation='bilinear')
                #     plt.axis("off")
                #     plt.savefig(f"./output/{channel[:-4]}_frequency_words.png")
                #     plt.close()
            else:
                # fdist = FreqDist(text)
                # with open(f"./output/{channel[:-4]}_frequency_words.txt", "w", encoding="utf-16") as \
                #         file:
                #     for j in fdist.most_common(30):
                #         line = ' '.join(str(x) for x in j)
                #         file.write(line + '\n')

                with open(f"./output/{channel[:-4]}_newspeak.txt", "w", \
                          encoding="utf-16") as file:
                    print(newspeak_output)
                    file.write(str(newspeak_output))

                # ### Построение облака слов и запись его в файл
                # text_raw = " ".join(text)
                # ### Маска для облака слов
                # mask = imageio.v2.imread(r'medvedev.jpg')
                # ### Облако слов "после"
                # if len(text_raw) != 0:
                #     wordcloud = WordCloud(width=2000,
                #                           height=1500,
                #                           random_state=1,
                #                           background_color='white',
                #                           colormap='Set2',
                #                           collocations=False,
                #                           mask=mask).generate(text_raw)
                #     plt.imshow(wordcloud, interpolation='bilinear')
                #     plt.axis("off")
                #     plt.savefig(f"./output/{channel[:-4]}_frequency_words.png")
                #     plt.close()

        print_and_plot(text,channel)
def count_dicts(common_list):
    result = {}
    for sublist in common_list:
        for i in range(0, len(sublist), 2):
            name = sublist[i]
            d = sublist[i + 1]
            if name in result:
                for key, value in d.items():
                    if key in result[name]:
                        result[name][key] += value
                    else:
                        result[name][key] = value
            else:
                result[name] = d

    return result
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


    # print(len(tokenizer.tokenize(text_words)), text_words.count(('специальная военная операция')))

if __name__ == '__main__':
    start_time = time.time()
    # parse_channel_history()
    analysis()
    # translate()
    print(count_dicts(common_list))

    print("--- %s seconds ---" % (time.time() - start_time))

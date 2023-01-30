
from googletrans import Translator
translator = Translator()
# print(translator.translate('kabel-konektor-kamera', dest='en', src='id').text)

# print(translator.translate("https://www.tokopedia.com/p/perawatan-hewan/perawatan-ayam/obat-vitamin-ayam"[28:].split("/")[-1], dest='en', src='id').text)
print(translator.translate("obat vitamin ayam", dest='en', src='id').text)
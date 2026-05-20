JOTISED_LETTERS = 'еёюяи'
CAN_BE_LONG = 'ʂbpfkstrlmngdz'
CONSONANT_LETTERS = {
    'б',
    'в',
    'г',
    'д',
    'ж',
    'з',
    'й',
    'к',
    'л',
    'м',
    'н',
    'п',
    'р',
    'с',
    'т',
    'ф',
    'х',
    'ц',
    'ч',
    'ш',
    'щ',
}
VOICED_OBSTRUENT_LETTERS = {'б', 'в', 'г', 'д', 'ж', 'з'}
RUSSIAN_LANGUAGE = 'russian'
EPITRAN_RUSSIAN_CYRILLIC = 'rus-Cyrl'
SPACY_RUSSIAN_MODEL = 'ru_core_news_sm'
SPACY_DISABLED_PIPELINES = ('tagger', 'morphologizer', 'attribute_ruler')
TPS_PLANE_MODE = 'plane'
STRESS_ACCURACY_THRESHOLD = 0.86
SECOND_SILENT = ('стн', 'стл', 'здн', 'рдн', 'нтск', 'ндск', 'лвств')
FIRST_SILENT = ('лнц', 'дц', 'вств')
HISSING_REGRESSIVE_DEVOICING = {'сш': 'шш', 'зш': 'шш', 'сж': 'жж', 'сч': 'щ'}
NON_IPA_SYMBOLS = {'t͡ɕʲ': 't͡ɕ', 'ʂʲː': 'ʂ', 'ɕːʲ': 'ɕː', 'ʒ': 'ʐ', 'd͡ʐ': 'd͡ʒ'}
HISSING_IOTATED_IE = {'ʐɨ̆e': 'ʐje', 'ʂɨ̆e': 'ʂje'}

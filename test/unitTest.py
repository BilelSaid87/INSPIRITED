import os
from keras.models import load_model
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
import numpy as np

# def intent(tag_name):
#    def intent_decorator(func):
#      def func_wrapper(*args, **kwargs):
#        if 'positive' in tag_name:
#          os.system('say ' + "test"+ "{0}".format(func(*args, **kwargs)))
#          return 0
#      return func_wrapper
#    return intent_decorator
#
#
#
# @intent('negative')
# def get_fullname():
#   return "Positive Feedback"
#
#
#
# print(get_fullname())
docs = ['Gut gemacht!',
         'Gute Arbeit',
         'Tolle Leistung',
		'Schöne Arbeit',
		'Hervorragend!',
		'Schwach',
		'Schlechte Leistung!',
		'nicht gut',
		'schwache Arbeit',
		'hätte besser machen können.']
docs ={ "Gut": 27,
        "gemacht": 35}
print(docs["Gut"])
arr=[[27, 35], [40, 40], [27, 44], [46, 40], [31], [8], [22, 44], [34, 27], [14, 40], [12, 44, 5, 38]]

model = load_model('kerasKlassifierModel')
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
phrases=['Tolle Arbeit freund']
print(arr[0][0])
#phrase_encoded=[one_hot(phrase, 50) for phrase in phrases]
phrase_encoded=[[12,44]]
print(phrase_encoded)
max_length = 4
phrase_padded = pad_sequences(phrase_encoded, maxlen=max_length, padding='pre')
label = model.predict_classes(phrase_padded)
prob = model.predict_proba(phrase_padded)
print(prob)
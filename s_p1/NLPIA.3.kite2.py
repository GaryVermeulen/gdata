# NLPIA.3.kite.py
# NLPIA 3 kite example

from collections import Counter
from nltk.tokenize import TreebankWordTokenizer



kite_text = """A kite is traditionally a tethered heavier-than-air craft with wing surfaces that react
against the air to create lift and drag. A kite consists of wings, tethers, and anchors.
Kites often have a bridle to guide the face of the kite at the correct angle so the wind
can lift it. A kite’s wing also may be so designed so a bridle is not needed; when
kiting a sailplane for launch, the tether meets the wing at a single point. A kite may
have fixed or moving anchors. Untraditionally in technical kiting, a kite consists of
tether-set-coupled wing sets; even in technical kiting, though, a wing in the system is
still often called the kite.
The lift that sustains the kite in flight is generated when air flows around the kite’s
surface, producing low pressure above and high pressure below the wings. The
interaction with the wind also generates horizontal drag along the direction of the
wind. The resultant force vector from the lift and drag force components is opposed
by the tension of one or more of the lines or tethers to which the kite is attached. The
anchor point of the kite line may be static or moving (such as the towing of a kite by
a running person, boat, free-falling anchors as in paragliders and fugitive parakites
or vehicle).
The same principles of fluid flow apply in liquids and kites are also used under water.
A hybrid tethered craft comprising both a lighter-than-air balloon as well as a kite
lifting surface is called a kytoon.
Kites have a long and varied history and many different types are flown
individually and at festivals worldwide. Kites may be flown for recreation, art or
other practical uses. Sport kites can be flown in aerial ballet, sometimes as part of a
competition. Power kites are multi-line steerable kites designed to generate large forces
which can be used to power activities such as kite surfing, kite landboarding, kite
fishing, kite buggying and a new trend snow kiting. Even Man-lifting kites have
been made."""

kite_history = """Kites were invented in China, where materials ideal for kite building were readily
available: silk fabric for sail material; fine, high-tensile-strength silk for flying line;
and resilient bamboo for a strong, lightweight framework.
The kite has been claimed as the invention of the 5th-century BC Chinese
philosophers Mozi (also Mo Di) and Lu Ban (also Gongshu Ban). By 549 AD
paper kites were certainly being flown, as it was recorded that in that year a paper
kite was used as a message for a rescue mission. Ancient and medieval Chinese
sources describe kites being used for measuring distances, testing the wind, lifting
men, signaling, and communication for military operations. The earliest known
Chinese kites were flat (not bowed) and often rectangular. Later, tailless kites
incorporated a stabilizing bowline. Kites were decorated with mythological motifs
and legendary figures; some were fitted with strings and whistles to make musical
sounds while flying. From China, kites were introduced to Cambodia, Thailand,
India, Japan, Korea and the western world.
After its introduction into India, the kite further evolved into the fighter kite, known
as the patang in India, where thousands are flown every year on festivals such as
Makar Sankranti.
Kites were known throughout Polynesia, as far as New Zealand, with the
assumption being that the knowledge diffused from China along with the people.
Anthropomorphic kites made from cloth and wood were used in religious ceremonies
to send prayers to the gods. Polynesian kite traditions are used by anthropologists get
an idea of early “primitive” Asian traditions that are believed to have at one time
existed in Asia."""

#
if __name__ == "__main__":

    tokenizer = TreebankWordTokenizer()

    kite_intro = kite_text.lower()
    intro_tokens = tokenizer.tokenize(kite_intro)
    kite_history = kite_history.lower()
    history_tokens = tokenizer.tokenize(kite_history)
    intro_total = len(intro_tokens)
    history_total = len(history_tokens)
    print(intro_total)
    print(history_total)

    intro_tf = {}
    history_tf = {}
    intro_counts = Counter(intro_tokens)
    intro_tf['kite'] = intro_counts['kite'] / intro_total
    history_counts = Counter(history_tokens)
    history_tf['kite'] = history_counts['kite'] / history_total

    print('Term Frequency of "kite" in intro is: {:.4f}'.format(intro_tf['kite']))
    print('Term Frequency of "kite" in history is: {:.4f}'.format(history_tf['kite']))

    intro_tf['and'] = intro_counts['and'] / intro_total
    history_tf['and'] = history_counts['and'] / history_total

    print('Term Frequency of "and" in intro is: {:.4f}'.format(intro_tf['and']))
    print('Term Frequency of "and" in history is: {:.4f}'.format(history_tf['and']))
    
    num_docs_containing_and = 0
    for doc in [intro_tokens, history_tokens]:
        if 'and' in doc:
            num_docs_containing_and += 1

    num_docs_containing_kite = 0
    for doc in [intro_tokens, history_tokens]:
        if 'kite' in doc:
            num_docs_containing_kite += 1

    num_docs_containing_china = 0
    for doc in [intro_tokens, history_tokens]:
        if 'china' in doc:
            num_docs_containing_china += 1

    
    intro_tf['china'] = intro_counts['china'] / intro_total
    history_tf['china'] = history_counts['china'] / history_total

    num_docs = 2
    intro_idf = {}
    history_idf = {}
    intro_idf['and'] = num_docs / num_docs_containing_and
    history_idf['and'] = num_docs / num_docs_containing_and
    intro_idf['kite'] = num_docs / num_docs_containing_kite
    history_idf['kite'] = num_docs / num_docs_containing_kite
    intro_idf['china'] = num_docs / num_docs_containing_china
    history_idf['china'] = num_docs / num_docs_containing_china

    intro_tfidf = {}
    intro_tfidf['and'] = intro_tf['and'] * intro_idf['and']
    intro_tfidf['kite'] = intro_tf['kite'] * intro_idf['kite']
    intro_tfidf['china'] = intro_tf['china'] * intro_idf['china']

    history_tfidf = {}
    history_tfidf['and'] = history_tf['and'] * history_idf['and']
    history_tfidf['kite'] = history_tf['kite'] * history_idf['kite']
    history_tfidf['china'] = history_tf['china'] * history_idf['china']

    print(intro_tfidf)
    print(history_tfidf)
    
    
    
    
    
    
    

    

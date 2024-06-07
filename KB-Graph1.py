#  From geeksforgeeks.org
#
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK resources
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')

# Create a small custom dataset with sentences
#data = {
#    'sentence': [&quot;Sandeep Jain founded GeeksforGeeks.&quot;,
#                 &quot;GeeksforGeeks is also known as GFG.&quot;,
#                 &quot;GeeksforGeeks is a website.&quot;, 
#                 &quot;Authors write for GFG.&quot;],
#    'source': [&quot;Sandeep Jain&quot;, &quot;GeeksforGeeks&quot;, &quot;GeeksforGeeks&quot;, &quot;Authors&quot;],
#    'target': [&quot;GeeksforGeeks&quot;, &quot;GFG&quot;, &quot;website&quot;, &quot;GFG&quot;],
#    'relation': [&quot;founded&quot;, &quot;known as&quot;, &quot;is&quot;, &quot;write for&quot;],
#}

data = {
    'sentence': ["Sandeep Jain founded GeeksforGeeks.",
                 "GeeksforGeeks is also known as GFG.",
                 "GeeksforGeeks is a website.", 
                 "Authors write for GFG."],
    'source': ["Sandeep Jain", "GeeksforGeeks", "GeeksforGeeks", "Authors"],
    'target': ["GeeksforGeeks", "GFG", "website", "GFG"],
    'relation': ["founded", "known as", "is", "write for"],
}

df = pd.DataFrame(data)
print(df)
print('--------------------')

# NLP Preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)

# Apply preprocessing to sentences in the dataframe
df['processed_sentence'] = df['sentence'].apply(preprocess_text)
print(df)
print('--------------------')

# Initialize a directed graph
G = nx.DiGraph()

# Add edges to the graph based on predefined source, target and relations
for _, row in df.iterrows():
    source = row['source']
    target = row['target']
    relation = row['relation']

    G.add_node(source)
    G.add_node(target)
    G.add_edge(source, target, relation=relation)

# Visualize the knowledge graph with colored nodes
# Calculate node degrees
node_degrees = dict(G.degree)
# Assign colors based on node degrees
node_colors = ['lightgreen' if degree == max(node_degrees.values()) else 'lightblue' for degree in node_degrees.values()]

# Adjust the layout for better spacing
pos = nx.spring_layout(G, seed=42, k=1.5)

labels = nx.get_edge_attributes(G, 'relation')
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color=node_colors, font_size=8, arrowsize=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
plt.show()


import gensim
import pandas as pd
import gensim.corpora as corpora
import numpy as np
from gensim import corpora
from gensim.corpora import Dictionary
import os
from flaskexample.settings import APP_STATIC
import html
from gensim.utils import simple_preprocess
import re

def ModelIt(input, text):
    # load models
    tag_lda_model = gensim.models.LdaModel.load(os.path.join(APP_STATIC, 'tag_lda_model_new.model'))
    tl_lda_model = gensim.models.LdaModel.load(os.path.join(APP_STATIC, 'tl_lda_model_new.model'))
    ds_lda_model = gensim.models.LdaModel.load(os.path.join(APP_STATIC, 'ds_lda_model_new.model'))
    # load dictionary
    tag_id2word = Dictionary.load(os.path.join(APP_STATIC,'tag_id2word_new.dict'))
    tl_id2word = Dictionary.load(os.path.join(APP_STATIC,'tl_id2word_new.dict'))
    ds_id2word = Dictionary.load(os.path.join(APP_STATIC,'ds_id2word_new.dict'))
    # create corpus
    tag_corpus = [tag_id2word.doc2bow(input)]
    tl_corpus = [tl_id2word.doc2bow(input)]
    ds_corpus = [ds_id2word.doc2bow(input)]
    text_corpus = [ds_id2word.doc2bow(text)]
    # calculate topic -- tag
    top_topic_tag = tag_lda_model[tag_corpus[0]]
    row = sorted(top_topic_tag, key=lambda x: (x[1]), reverse=True)#[top_topic_tl[i][1] for i in range(20)]
    topic_vec_tag = row[0][0]
	
    # calculate topic -- title
    top_topic_tl = tl_lda_model[tl_corpus[0]]
    row = sorted(top_topic_tl, key=lambda x: (x[1]), reverse=True)#[top_topic_tl[i][1] for i in range(20)]
    topic_vec_tl = row[0][0]
	
    # calculate topic -- description
    top_topic_ds = ds_lda_model[ds_corpus[0]]
    row = sorted(top_topic_ds, key=lambda x: (x[1]), reverse=True)#[top_topic_tl[i][1] for i in range(20)]
    topic_vec_ds = row[0][0]
	
	
	# calculate text -- description model
    top_topic_text = ds_lda_model[text_corpus[0]]
    row = sorted(top_topic_text, key=lambda x: (x[1]), reverse=True)#[top_topic_tl[i][1] for i in range(20)]
    topic_vec_text = row[0][0]
	
    return topic_vec_tag, topic_vec_tl, topic_vec_ds, topic_vec_text

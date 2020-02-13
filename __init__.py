# Anki Speed Limit - Stops and reminds the user to not rush through Anki reviews without thinking them through
# Copyright (C) 2020 Jonathan Doliver

from anki import hooks
from aqt import mw # import the main window object (mw) from aqt
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
from math import floor
from random import choice

config = mw.addonManager.getConfig(__name__) # parse config.json

# whether the add-on should take effect
ACTIVE = config['ACTIVE']

# the minimum number of seconds the user should look at a card with each ease
MIN_AGAIN_SECONDS = config['MIN_AGAIN_SECONDS']
MIN_HARD_SECONDS = config['MIN_HARD_SECONDS']
MIN_GOOD_SECONDS = config['MIN_GOOD_SECONDS']
MIN_EASY_SECONDS = config['MIN_EASY_SECONDS']

# the potential messages to be shown when the user continues too quickly
SLOW_DOWN_MESSAGES = config['SLOW_DOWN_MESSAGES']

def show_pop_up(seconds_taken):
    if seconds_taken < 2:
        showInfo( "You only spent a second on this card! %s" % choice(SLOW_DOWN_MESSAGES) )
    else:
        showInfo( "You only spent %d seconds on this card. %s" % ( seconds_taken, choice(SLOW_DOWN_MESSAGES) ) )

def judge_pace_new(card, ease, early): # 2.1.20+
    judge_pace(card, ease)

def judge_pace_old(self, ease): # 2.1.19-
    judge_pace(self.card, ease)

def judge_pace(card, ease):
    if (ease == 1 and card.timeTaken() < MIN_AGAIN_SECONDS * 1000
        or ease == 2 and card.timeTaken() < MIN_HARD_SECONDS * 1000
        or ease == 3 and card.timeTaken() < MIN_GOOD_SECONDS * 1000
        or ease == 4 and card.timeTaken() < MIN_EASY_SECONDS * 1000):
        show_pop_up( floor(card.timeTaken() / 1000) )

try:
    hooks.schedv2_did_answer_review_card.append(judge_pace_new) #2.1.20+
except AttributeError:
    Reviewer._answerCard = hooks.wrap(Reviewer._answerCard, judge_pace_old, "before") #2.1.19-

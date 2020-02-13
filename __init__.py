# Anki Speed Limit - Stops and reminds the user to not rush through Anki reviews without thinking them through
# Copyright (C) 2020 Jonathan Doliver

from anki import hooks
from aqt import mw # import the main window object (mw) from aqt
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
from random import choice

# the minimum number of seconds the user should look at a card
MIN_SECONDS = 10

# the potential messages to be shown when the user continues too quickly
SLOW_DOWN_MESSAGES = [
    "Take your time!",
    "Make sure you're really internalizing the info before continuing!",
    "Consider making a mnemonic device right now to help you remember!",
    "Hold on! Take some time to think about WHY you got it wrong.",
    "Rushing won't help you remember.",
    "Not giving thing all of your attention will only make things take longer.",
    "Haste makes waste!",
    "Slow down there, speedster!"
]

def judge_pace_new(card, ease, early): # 2.1.20+
    judge_pace(card, ease)

def judge_pace_old(self, ease): # 2.1.19-
    judge_pace(self.card, ease)

def judge_pace(card, ease):
    if ease == 1:
        #if mw.col.sched.answerButtons(self.card) == 2:
        if card.timeTaken() < MIN_SECONDS * 1000:
            # show a message box
            showInfo( choice(SLOW_DOWN_MESSAGES) )

try:
    hooks.schedv2_did_answer_review_card.append(judge_pace_new) #2.1.20+
except AttributeError:
    Reviewer._answerCard = hooks.wrap(Reviewer._answerCard, judge_pace_old, "before") #2.1.19-

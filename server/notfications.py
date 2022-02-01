
from os import popen
from os.path import join
from threading import Thread

from playsound import playsound

from data.base import projectRoot


def pushNoteCards(uName:str, cardType:str):

    cmdStr = "notify-send 'Safety Notifications' '{} played a {} card' ".format(
        uName,
        cardType
    )

    wavFile = join(projectRoot(), '72125__kizilsungur__sweetalertsound1.wav')
    wav = lambda: playsound(wavFile)
    
    t = Thread(
        target=wav,
        args=()
    )

    t.start()

    popen(cmdStr)
    return True


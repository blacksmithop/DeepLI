#!/usr/bin/env python
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import sys
from pyfiglet import Figlet
import argparse


class deepli(object):
    """
    Code that runs deepli
    """

    style = style_from_dict(
        {
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        }
    )

    questions = [
        {
            'type': 'input',
            'name': 'command',
            'message': '>',
        }
    ]

    fig = Figlet(font='big')

    @classmethod
    def printDeepli(cls):
        print(cls.fig.renderText('DeepLI'))

    @classmethod
    def splitCommands(cls, commandDict):
        return commandDict['command'].split(" ")

    @classmethod
    def deeplilogic(cls):
        try:
            answers = prompt(cls.questions,style=cls.style)
            #AI logic call for nlp2command will happen here someday!
            command = cls.splitCommands(answers)
            k = subprocess.call(command)
        except Exception as e:
            print(str(e))

    @classmethod
    def run(cls):
        cls.printDeepli()
        while(True):
            cls.deeplilogic()

deepli.run()
#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import subprocess
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import sys
from pyfiglet import Figlet
import argparse
import os



class Deepli(object):
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

    homedir = os.environ['HOME']
    os.chdir(homedir)

    @classmethod
    def printDeepli(cls):
        print(cls.fig.renderText('DeepLI'))

    @classmethod
    def splitCommands(cls, commandDict):
        return commandDict['command'].split(" ")

    @classmethod
    def exitDeepli(cls):
        exit()

    @classmethod
    def changeDirectory(cls, dir):
        try:
            if len(dir) <= 1:
                cd = os.chdir(cls.homedir)
            else:
                cd = os.chdir(dir[1])
        except Exception as e:
            print(str(e))



    @classmethod
    def deeplilogic(cls):
        try:
            answers = prompt(cls.questions,style=cls.style)
            #AI logic call for nlp2command will happen here someday!
            command = cls.splitCommands(answers)
            if command[0].encode("utf-8") == 'exit':
                exit = cls.exitDeepli()
            elif command[0].encode("utf-8") == 'cd':
                cd = cls.changeDirectory(command)
            else:
                k = subprocess.call(command)

        except Exception as e:
            print(str(e))

    @classmethod
    def run(cls):
        cls.printDeepli()
        while(True):
            cls.deeplilogic()

Deepli.run()

#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from pythonbot import bot


class TestBot(unittest.TestCase):

    def setUp(self):
        self.input_file_data = ['first_name,last_name,email,message\n',
                                'Amanda,Moore,Amanda.Moore@domain.com,message\n',
                                'Julia,Jimenez,Julia.Jimenez@domain.com,message\n']
        self.input_list = [{'first_name': 'Amanda', 'last_name': 'Moore',
                            'email': 'Amanda.Moore@domain.com', 'message': 'message'},
                           {'first_name': 'Julia', 'last_name': 'Jimenez',
                            'email': 'Julia.Jimenez@domain.com', 'message': 'message'}]

    @patch('builtins.print')
    def test_make_list_from_csv(self, mock_print):
        actual = bot.make_list_from_csv(self.input_file_data)
        print(actual)
        self.assertEqual(actual, self.input_list)

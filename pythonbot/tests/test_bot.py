#!/usr/bin/env python3
import argparse
import unittest
from unittest.mock import patch

import mock

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
        self.fake_data_dict = {"first_name": ['Kim', 'Chelsea'], "last_name": ['Douglas', 'Skinner'],
                               "email": ['Kim.Douglas@domain.com',
                                         'Chelsea.Skinner@domain.com'],
                               "message": ['message', 'message']}
        self.fake_csv = """first_name,last_name,email,message
Amanda,Moore,Amanda.Moore@domain.com,message
Julia,Jimenez,Julia.Jimenez@domain.com,message
"""

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_parse_args(self, mock_args):
        mock_args.return_value = argparse.Namespace(run='run')
        expected = {'run': 'run'}
        actual = bot.parse_args()
        actual_dict = vars(actual)
        self.assertEqual(actual_dict, expected)

    def test_generate_fake_data(self):
        f_mock = mock.MagicMock()
        f_mock.name.side_effect = ['Kim Douglas', 'Chelsea Skinner']
        actual = bot.generate_fake_data(f_mock, 'message', 2)
        self.assertEqual(actual, self.fake_data_dict)

    def test_read_data_csv(self):
        with patch('builtins.open', mock.mock_open(read_data=self.fake_csv)):
            actual = bot.read_data_csv('data/input.csv')
        self.assertEqual(actual, self.input_file_data)

    def test_read_data_csv_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(SystemExit):
                bot.read_data_csv('data/input.csv')

    def test_read_data_csv_permission_error(self):
        with patch('builtins.open', side_effect=PermissionError):
            with self.assertRaises(SystemExit):
                bot.read_data_csv('data/input.csv')

    def test_read_data_csv_attribute_error(self):
        with patch('builtins.open', side_effect=AttributeError):
            with self.assertRaises(SystemExit):
                bot.read_data_csv('data/input.csv')

    @patch('builtins.print')
    def test_make_list_from_csv(self, mock_print):
        actual = bot.make_list_from_csv(self.input_file_data)
        self.assertEqual(actual, self.input_list)

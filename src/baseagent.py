#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import abc
import logging

# -------------------------------------------------------------------------
#
#  class Agent
#
# -------------------------------------------------------------------------
class BaseAgent(object):
    """
    Class variables: __metaclass__, identifier, parameters, state_variables
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_identifier(self):
        return
    @abc.abstractmethod
    def set_identifier(self, _identifier):
        """
        Class variables: identifier
        Local variables: _identifier
        """
        if not isinstance(_identifier, str):
            raise TypeError
        else:
            self.identifier = _identifier
        return
    identifier = abc.abstractproperty(get_identifier, set_identifier)
    # identifier of the specific agent used for distinguishing agents
    # identifier should be a string

    @abc.abstractmethod
    def get_parameters(self):
        return
    @abc.abstractmethod
    def set_parameters(self, _params):
        """
        Class variables: parameters
        Local variables: _params
        """
        if not isinstance(_params, dict):
            raise TypeError
        else:
            self.parameters = _params
        return
    parameters = abc.abstractproperty(get_parameters, set_parameters)
    # parameters of the agents, store values determining
    # the behaviour of a given agent
    # parameters should be a dictionary

    @abc.abstractmethod
    def append_parameters(self, _params):
        if not isinstance(_variables, dict):
            raise TypeError
        else:
            self.parameters.update(_params)
        return
    # a standard method for adding a parameter
    # without destroying previously set ones

    @abc.abstractmethod
    def get_state_variables(self):
        return
    @abc.abstractmethod
    def set_state_variables(self, _variables):
        """
        Class variables: state_variables
        Local variables: _variables
        """
        if not isinstance(_variables, dict):
            raise TypeError
        else:
            self.state_variables = _variables
        return
    state_variables = abc.abstractproperty(get_state_variables, set_state_variables)
    # state variables of the agents, store values determining
    # the behaviour of a given agent that are bound to change
    # during the simulation
    # state variables should be a dictionary

    @abc.abstractmethod
    def append_state_variables(self, _variables):
        if not isinstance(_variables, dict):
            raise TypeError
        else:
            self.state_variables.update(_variables)
        return
    # a standard method for adding a state variable
    # without destroying previously set ones

    @abc.abstractmethod
    def __init__(self, _identifier, _params, _variables):
        """
        Class variables: parameters, state_variables
        Local variables: _identifier, _params, _variables
        """
        self.set_identifier(_identifier)
        self.parameters = _params
        self.state_variables = _variables
    # a standard method for initialisation of an agent

    @abc.abstractmethod
    def __str__(self):
        """
        Class variables: identifier, parameters, state_variables
        Local variables: ret_str, entry, value
        """
        ret_str = "  <agent identifier='" + self.identifier + "'>\n"
        for entry in self.parameters:
            value = self.parameters[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str += "    <parameter type='agent' name='" + entry + "' value='" + str(value) + "'></parameter>\n"
            else:
                raise TypeError
        for entry in self.state_variables:
            value = self.state_variables[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str += "    <variable name='" + entry + "' value='" + str(value) + "'></variable>\n"
            elif isinstance(value, list):
                ret_str += "    <variable name='" + entry + "' value='[" + str(value[0]) + "," + str(value[1]) + \
                           "]'></variable>\n"
            else:
                raise TypeError
        ret_str += "  </agent>\n"

        return ret_str
    # a standard method for writing a file with
    # all of the agent's variable in a xml styled string

    @abc.abstractproperty
    def accounts(self):
        pass
    # accounts of the agent, used to store transactions between agents

    @abc.abstractmethod
    def get_account(self, _type):
        volume = 0.0

        for transaction in self.accounts:
            if (transaction.type_ == _type):
                volume = volume + float(transaction.amount)

        return volume
    # a standard function returning the value of all transactions
    # of a given type held by the agent

    @abc.abstractmethod
    def get_account_num_transactions(self, _type):
        num_transactions = 0.0

        for transaction in self.accounts:
            if (transaction.type_ == _type):
                num_transactions += 1

        return num_transactions
    # a standard function returning the number of all transactions
    # of a given type held by the agent

    @abc.abstractmethod
    def clear_accounts(self):
        for tranx in self.accounts:
            tranx.__del__()
    # a standard function deleting all transactions of the agent

    @abc.abstractmethod
    def purge_accounts(self):
        new_accounts = []

        for transaction in self.accounts:
            if transaction.amount > 0.0:
                new_accounts.append(transaction)

        self.accounts = new_accounts
    # a standard function deleting all worthless transactions of the agent

    @abc.abstractmethod
    def check_consistency(self, _assets, _liabilities):
        assets = 0.0
        liabilities = 0.0

        for transaction in self.accounts:
            if transaction.type_ in _assets:
                assets = assets + transaction.amount
            if transaction.type_ in _liabilities:
                liabilities = liabilities + transaction.amount

        if assets == liabilities:
            return True
        else:
            return False
    # a standard function determining whether value of all assets
    # and liabilities of the agent are equal
    # types of transactions which constitute aseets and liabilities
    # are given as lists

    @abc.abstractmethod
    def get_parameters_from_file(self, _filename, _environment):
        from xml.etree import ElementTree

        try:
            xmlText = open(_filename).read()
            element = ElementTree.XML(xmlText)
            # we get the identifier
            self.identifier = element.attrib['identifier']
            # and then we're only interested in <parameter> fields
            element = element.findall('parameter')

            # loop over all <parameter> entries in the xml file
            for subelement in element:
                name = subelement.attrib['name']
                value = subelement.attrib['value']
                # add them to parameter list
                self.parameters[name] = float(value)

        except:
            logging.error("    ERROR: %s could not be parsed",  _filename)
    # a standard function reading parameters of the agents from
    # an xml file, looking somewhat like the below
    # <bank identifier='string'>
    #     <parameter name='string' value='string'></parameter>
    # </bank>

    @abc.abstractmethod
    def get_transactions_from_file(self, filename, environment):
        from xml.etree import ElementTree

        try:
            xmlText = open(filename).read()
            element = ElementTree.XML(xmlText)
            # this time we're interested in <transaction> fields
            element = element.findall('transaction')

            # loop over all entries in the xml file
            for subelement in element:
                # we read all the fields
                type_ = str(subelement.attrib['type'])
                asset = str(subelement.attrib['asset'])
                from_ = str(subelement.attrib['from'])
                to = str(subelement.attrib['to'])
                amount = float(subelement.attrib['amount'])
                interest = float(subelement.attrib['interest'])
                maturity = float(subelement.attrib['maturity'])
                time_of_default = float(subelement.attrib['time_of_default'])
                # we find the actual agents by the ID found in the config
                from_ = environment.get_agent_by_id(from_)
                to = environment.get_agent_by_id(to)
                # and add the transaction to the agent's accounts
                self.add_transaction(type_, asset, from_, to, amount, interest, maturity, time_of_default)

        except:
            logging.error("    ERROR: %s could not be parsed",  filename)
    # a standard function for reading transactions from config files, e.g.
    # <transaction type='deposits' asset='' from='bank_test_config_id' to='household_test_config_id' amount='30' interest='0.02' maturity='0' time_of_default='-1'></transaction>
    # assumes different types of agents have different names
    # ie bank1 & household1 and not 1 & 1

    #@abc.abstractmethod
    #def get_best_response(self, opponent_strategy):
    #    pass

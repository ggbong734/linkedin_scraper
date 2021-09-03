from utilities.salesforce import SalesforceAdapter


class UpdateIndexes:
    def __init__(self):
        self.sf = SalesforceAdapter().get_instance()

    def _calculate_indexes(self):
        pass

    def _update_indexes(self):
        pass

    def run(self):
        # get candidates data from Salesforce
        # calculate indexes from the candidates
        self._calculate_indexes()
        # update the data in Salesforce
        self._update_indexes()
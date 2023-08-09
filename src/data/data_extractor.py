class DataExtractor:
    def __init__(self):
        self.data = []

    def add_data(self, site_name, data_dict):
        self.data.append({site_name: data_dict})

    def to_xml(self):
        # Implementa la conversione in formato XML
        pass

    def to_json(self):
        # Implementa la conversione in formato JSON
        pass

    def to_csv(self):
        # Implementa la conversione in formato CSV
        pass
